#!/usr/bin/env python3
"""Reconcile Python effect coverage and inspect target/covariance paths."""
import hashlib
import json
from pathlib import Path

import python_effect_reference_20261020 as exact
import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write

run=extension.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-20/python-effects-v1'
PRIOR=ROOT/'docs/program/execution/2026-10-20/fixest-reuse-v1'
RAW=ROOT/'docs/literature/raw'
OP='SW.CELL.effects_heterogeneity.Python'
OUTPUT=ROOT/f'docs/program/comprehensive-v14/work/{OP}/coverage-review.json'
REVIEWER=dict(name='Codex author/coordinator',kind='author')
read=lambda p:json.loads(p.read_text())
LIMITS=[
    'The five-candidate review is not exhaustive Python coverage; complementary leads and continuous-treatment estimator families remain incompletely inspected.',
    'The preserved search contains ten of23 metadata hits; bibliographic discovery is not technical evidence or a closed software census.',
    'Pinned source reviews and observed installed DoubleML artifacts have different provenance. Complete wheels, dependency locks and transitive rights remain admission work.',
    'No new downloaded package execution; prior seven-configuration DoubleML matching retains only its declared fixed-fold/external-prediction scope.',
    'Exact authored population and covariance identities do not establish native defects, finite calibration or bank return.',
    'Rendered review, Q1/Q5, mandatory repairs and final acceptance remain open.'
]


def main():
    assert not OUTPUT.exists() and not (BASE/'source-audit.json').exists()
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==OP
    matrix=read(ROOT/'docs/program/gap-execution-v13_1/work/SW01/coverage-matrix.json')
    cell=next(c for c in matrix['cells'] if c['id']=='effects_heterogeneity::Python')
    assert cell['candidate_ids']==['inherited:econml','inherited:doubleml','inherited:causalml']
    write(BASE/'inherited-cell.json',cell)
    audit=read(PRIOR/'reader/source-audit.json');verify_bindings(audit)
    selected={s['integrated_citation_key']:s for s in audit['sources'] if s['integrated_citation_key'] in
        ['exec19_econml_source','exec14_causalml_primary','runtime_doubleml_scope',
         'v13_sw_delicatessen','v131_sw_delicatessen','v13_sw_statsmodels','v131_sw_statsmodels']}
    assert len(selected)==7
    search=read(RAW/'v12_sw_cell_effects_heterogeneity_python.json')
    assert search['meta']['count']==23 and len(search['results'])==10
    search_receipt=RAW/'v12_sw_cell_effects_heterogeneity_python.receipt.json'
    write(BASE/'search-review.json',dict(cutoff='2026-10-07',
        original=ref(RAW/'v12_sw_cell_effects_heterogeneity_python.json','Bounded discovery response'),
        receipt=ref(search_receipt,'Original discovery acquisition'),query=search['meta']['x_query'],
        total_metadata_hits=23,inspected_metadata_rows=10,pagination_complete=False,
        new_web_search='Two primary-oriented built-in search queries returned no usable results on20October2026.',
        search_terms=['Python causal effect estimation packages EconML DoubleML CausalML causallib zEpid official',
            'site.statsmodels.org TreatmentEffect aipw effect_group ps_bounds'],
        stopping_rule='One saved first-page search, inherited five-candidate primary audit and targeted local method/covariance inspection; complementary leads remain open.',
        scholarly_claims_from_metadata=False,complete_search=False))
    write(BASE/'plan-review.json',dict(status='pass_to_execute',reviewer=REVIEWER,
        evidence=[ref(BASE/'plan.md','Reviewed coverage and integration plan'),ref(BASE/'inherited-cell.json','Exact inherited scope'),
            ref(BASE/'search-review.json','Cutoff and bounded search limitations'),ref(PRIOR/'reader/source-audit.json','Inherited primary identities')],
        checks=['Keep three inherited engines and two successor candidates in scope.',
            'Inspect target populations, score clipping, weighting and actual final covariance separately.',
            'Record complementary candidates and unresolved evidence without awarding exhaustive coverage.',
            'Use exact authored examples and preserve historical runtime evidence with its limits.']))
    pin='8278e2d218cc85bac2c7af02feb9a19a0e499b04'
    specs=[('v12_gap3_statsmodels_technical','statsmodels/treatment/treatment_effects.py',
        [(219,296),(427,465),(477,529),(541,601),(613,644),(650,718),(790,867),(1053,1365)]),
        ('v12_gap4_statsmodels_gmm','statsmodels/sandbox/regression/gmm.py',
        [(582,646),(1039,1090),(1212,1293)])]
    tree=read(RAW/'v12_sw2_tree_statsmodels.json');assert not tree['truncated']
    blobs={r['path']:r['sha'] for r in tree['tree'] if r['type']=='blob'}
    records=[];extracts=[]
    for prefix,path,spans in specs:
        p=RAW/(prefix+'.txt');rp=RAW/(prefix+'.receipt.json');receipt=read(rp);data=p.read_bytes()
        url=f'https://raw.githubusercontent.com/statsmodels/statsmodels/{pin}/{path}'
        blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert receipt['status']=='saved' and receipt['sha256']==core.sha(p) and receipt['url']==url
        assert blob==blobs[path]
        lines=data.decode().splitlines();anchors=[f'lines{a}-{b}' for a,b in spans]
        records.append(dict(source_identity=url,version_date='2026-10-06T14:46:27Z; commit'+pin,
            local_copy=ref(p,'; '.join(anchors)),receipt=ref(rp,'Authenticated original acquisition'),
            git_blob_sha1=blob,inspected_anchors=anchors,executed=False))
        extracts.append(dict(source=path,local_copy=ref(p,'Inspected code'),ranges=[dict(start=a,end=b,
            text='\n'.join(f'{i+1}: {lines[i]}' for i in range(a-1,b))) for a,b in spans]))
    write(BASE/'inspected-extracts.json',dict(records=extracts,software_executed=False))
    claims=[
        'The selected TreatmentEffect class offers IPW, RA, AIPW, AIPW-WLS and IPW-RA with linear OLS outcome models and explicit all/treated/untreated target choices.',
        'AIPW and AIPW-WLS share target-specific pseudo-outcome terms. WLS uses propensity-derived fitting weights; IPW-RA weights and target-row averaging differ by target population.',
        'Selection probabilities are clipped to ps_bounds, default0.001/0.999, in both point calculations and selected joint moment paths. Clipping is not a demonstration of overlap.',
        'RA/AIPW/WLS joint moments group control and treated rows; selection score rows are reordered to match. Row identities and all nuisance components must share the same order.',
        'The wrappers call joint GMM with maxiter1 and no explicit alternative weights_method; its default is cov. Preliminary HC0/HC1 outcome fits do not establish final clustered or HAC covariance.',
        'GMM covariance recomputes moment covariance from stored fit options. HAC is a separately explicit path with maxlag and kernel; the selected wrappers do not expose it through their signatures.',
        'The selected covariance code centers with the scalar moms.mean(). Its difference from per-column centering is relevant for nonzero moment means; exactly solved zero means remove that distinction.',
        'Inspect rank, optimizer residuals and covariance semantics rather than interpreting an available inverse or a fit result as validated causal inference.'
    ]
    source=dict(integrated_citation_key='exec20_python_effect_source',kind='software_primary_sources',
        title='statsmodels treatment-effect methods and final joint-GMM covariance paths',
        author='statsmodels contributors',year=2026,source_identity='https://github.com/statsmodels/statsmodels',
        version_date='2026-10-06T14:46:27Z; commit'+pin,selected_commit=pin,
        local_copy=ref(RAW/'v12_gap3_statsmodels_technical.txt','Target, fitting, clipping and method call paths'),
        records=records,license=selected['v13_sw_statsmodels']['license'],
        identity_evidence=[ref(RAW/'v12_sw2_cutoff_statsmodels.json','Selected cutoff identity'),
            ref(RAW/'v12_sw2_tree_statsmodels.json','Tree used to authenticate two original blobs')],
        inspected_anchors=[dict(anchor=c,inspection='Selected original source branches') for c in claims],
        supported_claims=claims,limitations=LIMITS,software_executed=False)
    reference=dict(integrated_citation_key='exec20_python_effect_reference',kind='project_authored_exact_reference',
        title='Exact target-population, propensity-clipping and moment-centering references',
        author='Causal banking proposal project',year=2026,source_identity='tools/python_effect_reference_20261020.py',
        version_date='2026-10-20',local_copy=ref(ROOT/'tools/python_effect_reference_20261020.py','calculate and aipw_expectation'),
        inspected_anchors=[dict(anchor='calculate(); aipw_expectation()',inspection='Rational population enumeration and matrix identities')],
        supported_claims=['Imposed risk-group law gives ATE50, ATT65, ATU35. Clipping p1999/2000 to999/1000 with incorrect zero outcome models changes expected score60 to69970/999; at cost65 the net changes from-5 to5035/999. Scalar versus column centering differs by an outer product of column-mean deviations.'],limitations=LIMITS)
    write(BASE/'source-audit.json',dict(sources=[source,reference],inherited_sources=list(selected.values()),
        inspected_claims=claims,cutoff='2026-10-07',limitations=LIMITS))
    write(BASE/'exact-results.json',exact.calculate())
    dml=read(ROOT/'docs/program/execution/2026-10-18/doubleml-reuse/historical-runtime-review.json');verify_bindings(dml)
    assert dml['matched_configurations']==7 and dml['largest_standard_error_difference']<1e-8
    write(BASE/'historical-runtime-review.json',dict(status='preserved_scoped_result',
        evidence=ref(ROOT/'docs/program/execution/2026-10-18/doubleml-reuse/historical-runtime-review.json','Seven fixed-fold/external-prediction comparisons'),
        new_execution=False,limits=dml['limitations']))
    descriptions={
        'EconML':dict(aliases=['py-why/EconML','DML','DynamicDML'],sources=['exec19_econml_source'],
            target='Selected residualized effect model; supplied-X ATE average retains the fitted model and contrast.',
            nuisance='Cross-fitting groups and cv settings must be frozen; group splitting is not a cluster covariance guarantee.',
            uncertainty='Selected static HC0/HC1/nonrobust and dynamic within-group paths have different dependence scopes.',
            route='Conditional original-engine reference/reuse, with effect model, treatment transformation, group/time order and bootstrap contract.') ,
        'DoubleML':dict(aliases=['DoubleML/doubleml-for-py','DoubleMLIRM Python'],sources=['runtime_doubleml_scope'],
            target='Selected IRM ATE/ATTE score; R package and other model families are separate.',
            nuisance='Key external predictions, folds, repetitions, score weights and propensity processing; preserve sampled-unit semantics.',
            uncertainty='Seven historical matched configurations support only fixed identical nuisance predictions/folds; full provenance and adverse cases remain open.',
            route='Reference route with complete hash-pinned distribution and dependency lock still needed.'),
        'CausalML':dict(aliases=['uber/causalml','CausalML T-learner'],sources=['exec14_causalml_primary'],
            target='Selected arm-specific fits, CATE columns and prediction-row average; initially binary treatment.',
            nuisance='Arm mapping, prediction population and stochastic learner seeds require preservation; selected R-learner caller does not alone establish leakage control.',
            uncertainty='Selected base bootstrap resamples rows; prediction intervals and ATE interval formulas have distinct meaning.',
            route='Conditional optional original T-learner wrapper; defer import/dependency and native interval admission.'),
        'Delicatessen':dict(aliases=['pzivich/Delicatessen','MEstimator'],sources=['v13_sw_delicatessen','v131_sw_delicatessen'],
            target='User-specified stacked estimating equations, with target and nuisance components explicitly chosen.',
            nuisance='Joint derivative and moment construction rather than automatic cross-fitting; contribution columns define the sampling units.',
            uncertainty='Inspected sandwich uses supplied contribution-column outer products and permits a pseudoinverse; no inferred panel/HAC dependence.',
            route='Transparent small-model reference with analytic derivatives, independent-unit law and rank diagnostics.'),
        'statsmodels':dict(aliases=['statsmodels TreatmentEffect','sandbox GMM'],sources=['v13_sw_statsmodels','v131_sw_statsmodels'],
            target='Selected all/treated/untreated effects and potential-outcome means; continuous dose-response and CATE are not qualified by this path.',
            nuisance='Parametric arm and selection fits are stacked in joint GMM; clipping, target weights and row grouping are explicit.',
            uncertainty='Final default GMM covariance is cov/HC0; preliminary outcome covariance is not the final dependence correction.',
            route='Conditional point-treatment baseline; require keyed roundtrips, residual/rank diagnostics and explicit covariance qualification.')}
    candidates=[]
    for name,detail in descriptions.items():
        candidates.append(dict(name=name,**detail,source_records=[selected[k] for k in detail['sources']],
            status='selected_primary_scope_reviewed',complete_family=False,absence_claim=False,
            native_admission=False,next_action='Qualify the named target with fixed sample and nuisance identities, declared sampling law, exact oracle, errors and resolved distribution rights.'))
    write(BASE/'candidate-register.json',dict(candidates=candidates,cutoff='2026-10-07',complete_census=False))
    omissions=[dict(candidate=n,evidence=ref(ROOT/f'docs/literature/software/{n}.json','Inherited discovery/identity only'),
        gap='Need target-specific original source inspection and immutable identity; no capability or absence conclusion from this entry.') for n in ['dowhy','zepid','causalpy']]
    omissions += [dict(candidate='causallib',gap='Complementary lead remains unidentified at a selected revision; acquire canonical originals before a technical claim.'),
        dict(candidate='Continuous treatment, targeted learning, survival and other effect families',gap='Do not treat five selected point-treatment paths as full coverage; reconcile task/candidate universe and inspect target-specific originals.'),
        dict(candidate='Search remainder',gap='Saved search first page contains10of23 metadata hits; inspect remaining results and citation/software chaining under the cutoff.')]
    write(BASE/'omissions-register.json',dict(items=omissions,essential_sources_waived=False,absence_claims=False))
    contract=dict(status='proposed_not_implemented',requirements=[
        'Specify ATE/ATT/ATU/CATE/contrast or dose curve, eligible population, treatment/control levels, outcome units and decision time.',
        'Keep sample keys, target masks, nuisance predictions, folds and repetition IDs aligned through any grouping or sorting.',
        'Record original and clipped propensity values, thresholds, counts and weights; clipping changes the score and does not create information.',
        'Freeze estimator-specific weights and aggregation target; never substitute average CATE, projection or subgroup effect for another target silently.',
        'Bind final moment vector, Jacobian, optimizer residual norm, rank and covariance choices; report unavailable uncertainty separately from a point estimate.',
        'Keep cross-fitting partitions, bootstrap sampling units and covariance dependence correction distinct.',
        'Preserve complete runtime provenance and rights; qualify only a named adapter profile against independent exact and generated references.'],integration_allowed=False)
    write(BASE/'conversion-contract.json',contract)
    evidence=[ref(BASE/n,'Python effects review evidence') for n in ['plan-review.json','search-review.json','source-audit.json',
        'inspected-extracts.json','exact-results.json','historical-runtime-review.json','candidate-register.json','omissions-register.json','conversion-contract.json']]
    evidence.append(ref(Path(__file__),'Coverage reconciliation and criteria'))
    trigger='Complete cutoff search and complementary originals; resolve each selected distribution/version; qualify target, clipping, row/nuisance alignment, Jacobian/rank and final covariance before a capability claim. Continue public work independently of bank validation.'
    criteria=[dict(index=0,verdict='inconclusive',finding='Five known candidates and aliases are reconciled, but cutoff search pagination and complementary effect-family originals remain open.'),
        dict(index=1,verdict='pass',finding='Claimed technical scope binds authentic original bytes, versions, hashes and inspected anchors; exact authored witnesses and historical runtime evidence remain distinct.'),
        dict(index=2,verdict='pass',finding='Alternatives, omissions and concrete public continuation actions are explicit; no absence or essential-source waiver is granted.')]
    coverage=dict(operation_id=OP,status='inconclusive',scope='Five-candidate Python effect review with extended target/clipping/covariance inspection',
        reviewer=REVIEWER,cutoff='2026-10-07',candidates=candidates,evidence=evidence,criteria=criteria,
        limitations=LIMITS,revisit_trigger=trigger,capabilities=[],integration_allowed=False,original_gap_qualification=False)
    write(OUTPUT,coverage);write(BASE/'review.json',dict(status='inconclusive',reviewer=REVIEWER,
        reviewed_output=ref(OUTPUT,'Python cell outcome'),findings=claims,evidence=evidence,criteria=criteria,limitations=LIMITS))
    graph,_,_=run.combined(ROOT,state);receipt=run.ledger.receipt_template(run.ledger.operation(graph,OP))
    receipt.update(outcome='inconclusive',execution='performed',scope=coverage['scope'],reviewer=REVIEWER,capabilities=[],
        outputs=[ref(OUTPUT,'Contracted Python coverage review')],limitations=LIMITS,nonexecution_reason='',revisit_trigger=trigger,
        criteria=[dict(c,evidence=evidence+[ref(BASE/'review.json','Author criterion review')]) for c in criteria])
    write(BASE/'operation-receipt.json',receipt);verify_bindings([coverage,receipt])
    print(json.dumps(dict(operation=OP,outcome='inconclusive',candidates=5,new_authenticated_blobs=2,new_native_runs=0)))


if __name__=='__main__':main()
