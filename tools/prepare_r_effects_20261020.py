#!/usr/bin/env python3
"""Authenticate inspected R sources and preserve a bounded proposal review."""
import hashlib
import json
from pathlib import Path
from urllib.parse import urlsplit
import r_effects_reference_20261020 as exact
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'docs/program/execution/2026-10-19/r-effects-v1'
RAW = ROOT/'docs/literature/raw'
read = lambda p: json.loads(p.read_text())

GROUPS = [
    dict(key='tmle', title='tmle 2.1.1: treatment missingness validation and point-effect path',
        commit='f8d88a07a3d25c96688221b384043eef7a31fe68', date='2025-08-30T15:10:02Z',
        repo='cran/tmle', tree='v12_sw2_tree_tmle', cutoff='v12_sw2_cran_cutoff_tmle',
        files=[('v12_sw2_description_tmle', [(1,25)], 'Version, declared license and scope; metadata only'),
            ('v12_sw2_manual_tmle_1', [(6,26),(32,76),(164,173)], 'Broader Delta wording, outcome missingness and mean-outcome example'),
            ('exec19_rfx_tmle_body', [(953,990),(1701,1786),(1894,1910)],
                'Argument guard rejects missing A or W; A NULL/all zero remapped to constant1; Delta regression conditions on A')],
        claims=['The selected public function does not admit arbitrary NA treatment labels: explicit guard rejects them and preprocessing can fail earlier.',
            'A NULL or all-zero vector is changed to a constant one vector for the no-variation/mean path; it does not reconstruct unknown assignments.',
            'The broader Delta help wording is retained as a discrepancy, not evidence of missing-treatment support.']),
    dict(key='doubleml_r', title='R DoubleML: IRM and PLR scores, cluster splitting and inference limits',
        commit='2a4df4cf2d695b8e29a87c350395445f2e4615f2', date='2026-09-01T06:10:14Z',
        repo='DoubleML/doubleml-for-r', tree='exec19_rfx_doubleml_tree', cutoff='exec19_rfx_doubleml_cutoff',
        files=[('exec19_rfx_dml_0',[(1,40)],'Development version1.0.1.9000; R/mlr3 dependencies and MIT declaration'),
            ('exec19_rfx_dml_1',[(1,2)],'Copyright holder notice only; not full dependency clearance'),
            ('exec19_rfx_dml_2',[(225,329),(398,439)],'Separate nuisance fits, ATE/ATTE scores, propensity clipping and binary treatment restriction'),
            ('exec19_rfx_dml_3',[(477,503)],'Partialling-out and IV-type residual scores'),
            ('exec19_rfx_dml_4',[(441,483),(496,565),(817,839),(972,1022),(1638,1733)],
                'Cluster bootstrap refusal, cluster split, fold-specific tuning option, joint bands and one/two-way variance paths'),
            ('exec19_rfx_dml_6',[(1,76),(335,352)],'mlr3 custom train/test folds and treatment-specific training subsets')],
        claims=['Selected IRM supports ATE/ATTE with distinct nuisances and score equations; it is not a CATE or arbitrary dose curve engine.',
            'Selected PLR partialling-out solves a residual covariance/variance moment; under heterogeneous linear slopes it variance-weights them.',
            'Cluster splitting and one/two-way variance paths exist; multiplier bootstrap explicitly rejects clustered data, while joint intervals require bootstrap.',
            'Nuisance tuning defaults to global; fold-specific tuning is an explicit option. Inner tuning and estimator cross-fitting remain different.']),
    dict(key='causalgps', title='CausalGPS: residual density, weighting and exposure-response path',
        commit='3a837d66e5cb791a310a18b63919abe04b4b290f', date='2026-01-11T20:39:26Z',
        repo='cran/CausalGPS', tree='exec19_rfx_causalgps_tree', cutoff='v12_sw2_cutoff_causalgps',
        files=[('v12_gap3_causalgps_technical',[(64,125)],'Normal density and kernel residual-density branches'),
            ('v12_gap4_causalgps_resid',[(1,13)],'Residual standardization'),
            ('v12_gap4_causalgps_density',[(1,18)],'Kernel density interpolation'),
            ('exec19_rfx_cgps_create_weighting',[(21,34)],'Marginal density divided by stored GPS'),
            ('exec19_rfx_cgps_estimate_erf',[(1,24),(29,124),(125,218)],'Response fitting, nonnegative weights and all-zero fallback'),
            ('exec19_rfx_cgps_generate_pseudo_pop',[(100,170)],'Balance and effective sample size diagnostics'),
            ('exec19_rfx_cgps_trim_it',[(35,76)],'Quantile trimming and complete-case filtering')],
        claims=['The selected kernel path stores density at standardized residuals without a scale divisor; create_weighting divides marginal exposure density by stored GPS.',
            'Under a location-scale law the original-unit density requires a Jacobian; this motivates conditional-scale/unit conformance, not a claim of all-package failure.',
            'Selected ERF paths fit weighted parametric, semiparametric or nonparametric responses; all-zero weights are changed to equal weights.',
            'Balance and effective sample size are diagnostics, not causal identification or calibrated curve uncertainty.']),
    dict(key='causaldrf', title='causaldrf: hi_est dose-grid standardization and get_ci order statistics',
        commit='cb67aca60bc4dbd6792edd062cb7682c656d5908', date='2022-09-29T19:40:10Z',
        repo='cran/causaldrf', tree='exec19_rfx_causaldrf_tree', cutoff='v12_sw2_cutoff_causaldrf',
        files=[('v12_gap3_causaldrf_technical',[(183,239),(263,310),(363,418)],
                'Treatment-model choices, transformed density branches and dose-specific prediction averaging'),
            ('exec19_rfx_cdrf_get_ci',[(1,81)],'Pointwise order statistics of supplied bootstrap coefficient matrices'),
            ('v12_gap4_causaldrf_license',[(1,2)],'Supplementary copyright notice only')],
        claims=['hi_est evaluates its treatment score at each requested dose, predicts outcomes for each row and averages them; it does not use each row observed score for every counterfactual dose.',
            'Log/square-root branches evaluate transformed-scale densities without original-scale Jacobians; at fixed positive dose these factors are constant across covariates, so interpretation requires care.',
            'get_ci consumes externally supplied bootstrap coefficients and sorts each dose column; it is not a bootstrap generator or simultaneous-band procedure.',
            'floor(0.025*B) is zero when B<40; exact index arithmetic motivates a native edge-case check, not a claim that more replicates guarantees valid inference.'])
]


def main():
    assert not (BASE/'source-audit.json').exists()
    excerpts = BASE/'inspected'
    excerpts.mkdir()
    sources, identities = [], []
    for group in GROUPS:
        tree_path = RAW/(group['tree']+'.json')
        tree = read(tree_path)
        assert tree.get('truncated') is False
        blobs = {e['path']:e['sha'] for e in tree['tree'] if e['type']=='blob'}
        originals, anchors = [], []
        for key, spans, claim in group['files']:
            path = RAW/(key+'.txt'); receipt_path = RAW/(key+'.receipt.json')
            receipt = read(receipt_path); data = path.read_bytes()
            assert receipt['status']=='saved' and receipt['sha256']==hashlib.sha256(data).hexdigest()
            assert '/'+group['commit']+'/' in receipt['url']
            relative = receipt['url'].split('/'+group['commit']+'/',1)[1]
            blob = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
            assert blob == blobs[relative], (key, relative)
            lines = data.decode().split('\n')
            for start,end in spans:
                assert 1<=start<=end<=len(lines),(key,start,end,len(lines))
                out = excerpts/f'{key}-{start}-{end}.txt'
                out.write_text('\n'.join(f'{i}: {lines[i-1].rstrip(chr(13))}' for i in range(start,end+1))+'\n')
                anchors.append(dict(original=ref(path,f'LF-delimited lines{start}-{end}'),
                    excerpt=ref(out,'Inspected original lines'),supported_claim=claim))
            originals.append(dict(source_identity=receipt['url'],local_copy=ref(path,claim),
                acquisition=ref(receipt_path,'Bounded collector receipt'),git_blob_sha1=blob,
                accessed_utc=receipt['accessed_utc']))
        source=dict(integrated_citation_key='exec20_rfx_'+group['key'],kind='software_primary_sources',
            title=group['title'],author=group['repo']+' contributors',year=2026,
            source_identity='https://github.com/'+group['repo']+'/tree/'+group['commit'],
            version_date=group['commit']+'; '+group['date']+'; inspected20October2026; cutoff7October2026',
            local_copy=originals[0]['local_copy'],originals=originals,inspected_anchors=anchors,
            supported_claims=group['claims'],identity_evidence=[ref(tree_path,'Complete selected Git tree'),
                ref(RAW/(group['cutoff']+'.json'),'Cutoff commit identity')],
            limitations=['Static primary-source inspection only; no downloaded R implementation executed.',
                'Selected commit observation is not exhaustive release/maintenance history or full distribution rights.'])
        sources.append(source);identities.append(dict(package=group['key'],commit=group['commit'],
            inspected_blobs=len(originals),tree_entries=len(tree['tree']),all_blobs_authenticated=True))
    write(BASE/'exact-results.json',exact.calculate())
    sources.append(dict(integrated_citation_key='exec20_rfx_reference',kind='project_evidence_not_scholarly_paper',
        title='Exact R effect-target, assignment-observation and dose-unit reference laws',
        author='Causal banking proposal project',year=2026,source_identity='tools/r_effects_reference_20261020.py',
        version_date='20 October 2026; authored exact laws',
        local_copy=ref(BASE/'exact-results.json','Exact rational results'),
        code=ref(ROOT/'tools/r_effects_reference_20261020.py','Original reference implementation'),
        inspected_anchors=['calculate: conditional versus pooled slopes, erased assignment labels, continuous response and density weights'],
        supported_claims=['Five stipulated law/index families; no R execution, confidence-coverage or bank-return claim.'],
        limitations=['Population examples and algebra only; all monetary amounts stipulated.']))
    audit=dict(sources=sources,identity_checks=identities,cutoff='2026-10-07',
        date='2026-10-20',anchor_convention='LF-delimited raw-byte lines; CR stripped only for readable excerpts',
        plan=ref(BASE/'plan.json','Reviewed source and proposal plan'),
        prior_search=ref(RAW/'v12_sw_cell_effects_heterogeneity_r.json','Inherited bounded discovery query; metadata only'))
    verify_bindings(audit)
    write(BASE/'source-audit.json',audit)
    omissions=[dict(candidate='bartCause/BART and causalweight',status='uninspected_alternatives',
        route='Acquire cutoff-specific package bodies, target/uncertainty documentation and original methods; inspect before claiming comparative coverage.'),
        dict(candidate='Full R ecosystem aliases and dose-response alternatives',status='search_incomplete',
        route='Extend recorded CRAN/repository and original-method queries with bounded stopping criteria; current seven-family list is not exhaustive.'),
        dict(candidate='tmle missing-treatment documentation',status='guard_resolved_documentation_discrepancy_retained',
        route='Treat arbitrary missing A as unsupported for inspected path; confirm NA/NULL/all-zero fixtures in future native prototype and seek upstream clarification.'),
        dict(candidate='Native R behavior and learner dependencies',status='future_prototype',
        route='Use isolated versioned R environments and the explicit target/units/failure fixtures; do not execute downloaded sources in proposal audit.'),
        dict(candidate='Complete distribution rights',status='unreviewed',
        route='Inspect licenses and notices of complete selected package distributions and transitive learners before any port or deploy decision.'),
        dict(candidate='CausalGPS matching and full curve uncertainty',status='partial_source_path',
        route='Trace matching joins, zero-scale/support edges, smoothing/link-scale behavior and full uncertainty pipeline; no blanket failure finding.'),
        dict(candidate='causaldrf transforms and bootstrap',status='partial_source_path',
        route='Check log/sqrt transformations, outcome representation, positive dose support, native indexing and refit all stages under correct sampling units.')]
    write(BASE/'omissions-register.json',dict(omissions=omissions,absence_claims=[],full_cell_closed=False))
    write(BASE/'conversion-contract.json',dict(status='proposal_only',integration_allowed=False,
        required=['Named estimand and target distribution; distinguish mean conditional slope from variance-weighted projection.',
            'Observed treatment labels, outcome missingness and label-missingness mechanism in separate fields.',
            'Treatment and outcome units, observed support and requested counterfactual grid.',
            'Estimator folds, inner tuning folds, cluster identifiers and prediction provenance.',
            'Truncation, trimming, weighting, cluster inference and unsupported-mode refusal.',
            'Ordinary intervals, pointwise curve intervals and simultaneous bands identified separately.'],
        decisions={'grf':'Wrap for qualified target-specific forests; native port deferred.',
            'DoubleML R':'Wrap selected IRM/PLR and preserve score/fold/cluster refusal semantics; no Python parity inferred.',
            'tmle':'Wrap qualified point treatments with observed A; reject arbitrary missing-A admission.',
            'CausalGPS':'Defer executable adoption pending scale/support and downstream-weight conformance.',
            'causaldrf':'Compare as a parametric dose-response baseline; transformation and full-bootstrap checks precede admission.'},
        evidence=[ref(BASE/'source-audit.json','Authenticated paths'),ref(BASE/'exact-results.json','Authored contract examples')]))
    print(json.dumps(dict(sources=len(sources),identity_checks=identities,omissions=len(omissions))))


if __name__=='__main__':
    main()
