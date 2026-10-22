#!/usr/bin/env python3
"""Preserve a source-kernel continuation without claiming whole Python IV/RD coverage."""
import hashlib
import json
from pathlib import Path
import python_iv_reference_20261022 as exact
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-22/python-iv-kernels-v1'
PRIOR=ROOT/'docs/program/execution/2026-10-22/python-iv-rd-preflight-v2'
read=lambda p:json.loads(p.read_text())


def main():
    previous=read(PRIOR/'source-audit.json');verify_bindings(previous)
    entries=[];extracts=[]
    specs=[
        ('linearmodels','docs/literature/raw/exec22_pyiv_linearmodels_source_0.txt',[(174,211,'Strictly positive weights normalized by mean; missing removal precedes square-root weighting; regressor/instrument assembly.'),(342,358,'Instrument count and separate full-column-rank checks; no strength guarantee.'),(580,629,'k-class projected solve and LIML kappa; static solve has no error checking.'),(631,716,'Robust covariance default, debiased false; kappa failure can remain NaN for fixed-kappa fit.')]),
        ('linearmodels','docs/literature/raw/exec22_pyiv_linearmodels_source_2.txt',[(277,329,'Scale, residuals, projected Hessian and covariance sandwich.'),(405,417,'Heteroskedastic score meat; not serial correlation correction.'),(517,551,'HAC kernel and optional data-selected bandwidth; preserve realized bandwidth.'),(554,624,'Cluster class documents one or two grouping columns and defaults each row to own cluster.'),(625,687,'Two-way inclusion-exclusion branch despite One-Way name; component corrections and intersection coding.')]),
        ('pyfixest','docs/literature/raw/exec22_pyiv_pyfixest_source_0.txt',[(178,235,'Within transformation and instrument-column removal feed delegated weighted 2SLS.'),(439,480,'Effective F under iid request constructs heteroskedastic meat before scalar diagnostic.'),(484,565,'First-stage restriction test suppresses warnings and returns F scaling with actual p-value; effective F weighted quadratic over trace.')]),
        ('pyfixest',str((BASE/'sources/pyfixest/estimation/internals/fit_.py').relative_to(ROOT)),[(103,162,'Weighted normal-equation first stage and projected fit; residuals stay on response scale and scores include weights.')]),
        ('pyfixest',str((BASE/'sources/pyfixest/estimation/internals/collinearity.py').relative_to(ROOT)),[(1,91,'Unweighted within Gram is sent to delegated core rank selector; named columns/masks retained, warnings on removal and refusal when all removed.')]),
        ('pyfixest',str((BASE/'sources/pyfixest/estimation/post_estimation/wald.py').relative_to(ROOT)),[(12,61,'Restriction shape/rank checks; pseudoinverse covariance quadratic, not automatic covariance validity.'),(64,120,'Both W and W/q retained; chosen F or chi-square distribution controls actual p-value.')]),
        ('pyfixest',str((BASE/'sources/pyfixest/estimation/models/feols_.py').relative_to(ROOT)),[(898,985,'F only for identity restriction and zero RHS; otherwise warning and chi-square. Cluster df2=min groups-1; other df2 uses retained rows/parameters/FE levels.')])]
    selection=read(BASE/'source-selection.json');pin=selection['commit']
    recovered={}
    for s in selection['files']:
        p=BASE/'sources'/s['path'];body=p.read_bytes()
        assert hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()==s['blob']
        recovered[str(p.relative_to(ROOT))]=dict(source_identity=f'https://github.com/py-econometrics/pyfixest/blob/{pin}/'+s['path'],
            local_copy=ref(p,'Original Git-verified source'),git_blob=s['blob'],
            acquisition_receipt=ref(ROOT/'docs/literature/raw'/(s['id']+'.receipt.json'),'Bounded acquisition'))
    for family,path,ranges in specs:
        p=ROOT/path;a=p.read_bytes().decode().split('\n')
        original=next((x for x in previous['sources'] if x['local_copy']['path']==path),None)
        source=dict(original) if original else dict(recovered[path])
        selected=[]
        for lo,hi,finding in ranges:
            assert 1<=lo<=hi<=len(a)
            excerpt='\n'.join(a[lo-1:hi]);e=dict(source=ref(p,'Original source'),lines=[lo,hi],finding=finding,
                excerpt=excerpt,excerpt_sha256=hashlib.sha256(excerpt.encode()).hexdigest())
            extracts.append(e);selected.append(dict(anchor=f'newline lines {lo}-{hi}',finding=finding))
        source.update(family=family,inspected_anchors=selected,supported_claims=[r[2] for r in ranges])
        entries.append(source)
    write(BASE/'inspected-extracts.json',dict(anchors=extracts,native_execution=False))
    write(BASE/'acquisition-review.json',dict(status='pass',files=list(recovered.values()),
        historical_identity=ref(PRIOR/'identity-observations.json','Two cutoff commits'),
        failures=[ref(p,'Preserved sandbox DNS failure') for p in sorted((BASE/'acquisition-local').glob('*.json'))],
        downloaded_code_executed=False))
    write(BASE/'exact-results.json',exact.calculate())
    claims=[
        'linearmodels separately checks design and instrument rank, which does not certify projected rank, strong instruments or exclusion.',
        'Default robust covariance is heteroskedastic; explicit kernel/calendar or clustering is needed for a distinct dependence claim.',
        'Selected clustered covariance contains one/two-column logic even where labels say One-Way; preserve actual grouping specification.',
        'pyfixest delegated weighted 2SLS retains response-scale residuals; column removal and weights must be recorded.',
        'pyfixest selected first-stage helper returns W/q and a p-value from actual chosen distribution; subset restrictions can trigger chi-square with warning suppressed.',
        'A first-stage relevance or overidentification diagnostic is distinct from a coefficient-null weak-IV confidence-set inversion.']
    limitations=['No downloaded software execution, numerical parity, empirical calibration or complete source-graph inspection.',
        'Core collinearity backend, solver backend, broader covariance/weight guards and tests remain unreviewed.',
        'RD, CausalPy IV and complementary candidates still need primary review; Python IV/RD cell remains open.',
        'Pinned commits are not proven equal to inherited package-release bytes; dependency rights/runtime remain unresolved.',
        'Known algebra and diagnostic-distribution examples are authored, not package output or bank evidence.']
    records=[]
    for family,key,title,author in [
        ('linearmodels','exec22_pyiv_kernels_linearmodels','linearmodels cutoff IV rank, fit and covariance paths','Kevin Sheppard and contributors'),
        ('pyfixest','exec22_pyiv_kernels_pyfixest','pyfixest cutoff weighted IV and diagnostic-distribution paths','pyfixest contributors')]:
        identity=next(x for x in read(PRIOR/'identity-observations.json') if x['family']==family)
        records.append(dict(integrated_citation_key=key,kind='software_primary_source',title=title,author=author,year=2026,
            cutoff='2026-10-07',source_identity='https://github.com/'+identity['repository']+'/tree/'+identity['commit'],
            version_date='Repository revision '+identity['commit']+'; '+identity['committed']+'; release equivalence unverified',
            local_copy=ref(BASE/'acquisition-review.json','Original-source and identity binding'),
            primary_sources=[x for x in entries if x['family']==family],
            inspected_anchors=[dict(anchor=e['source']['path']+' '+str(e['lines']),finding=e['finding'],evidence=ref(BASE/'inspected-extracts.json','Verbatim inspected code')) for e in extracts if any(x['family']==family and x['local_copy']['path']==e['source']['path'] for x in entries)],
            supported_claims=claims[:3] if family=='linearmodels' else claims[3:],limitations=limitations))
    records.append(dict(integrated_citation_key='exec22_pyiv_reference',kind='project_derivation',
        title='Projected-rank, exclusion and diagnostic-scaling witnesses',author='Causal banking proposal project',year=2026,
        source_identity='tools/python_iv_reference_20261022.py',version_date='22 October 2026',
        local_copy=ref(ROOT/'tools/python_iv_reference_20261022.py','Authored exact example'),
        inspected_anchors=[ref(BASE/'exact-results.json','Rational IV witness and reference-distribution calculation')],
        supported_claims=['Separate full-column-rank matrices can have zero projected Gram.',
            'A fixed small exclusion violation produces ratios3 and12 as first-stage coefficient shrinks.',
            'W=8 with2 restrictions gives W/q=4 but distinct chi-square2 and F(2,20) p-values.'],limitations=limitations))
    write(BASE/'source-audit.json',dict(sources=records,cutoff='2026-10-07',prior=ref(PRIOR/'source-audit.json','Preserved source/diagnostic and rights inspection')))
    write(BASE/'conversion-contract.json',dict(status='proposed_refinement_not_implemented',integration_allowed=False,
        retain=['Requested and retained rows, columns and instrument definitions; within transforms, weight roles and all defaults.',
            'Separate rank, conditioning, first-stage relevance, exclusion assumptions and identification target.',
            'Covariance family, actual group columns, calendar order, bandwidth, small-sample correction and reference distribution.',
            'For every diagnostic: exact null, restriction matrix, W, W/q, degrees of freedom, p-value and actual distribution.',
            'Capture source warnings; inspect parent result where a helper suppresses warnings or strips distribution metadata.'],
        refuse=['Do not route overidentification property as coefficient-null inversion.',
            'Do not use a singular pseudoinverse Wald result as proof of valid inference.',
            'Do not declare strong or valid instruments from full rank or one F-labelled scalar.',
            'Do not map absent cluster groups to an intended bank calendar; default row clusters are a distinct model.'],
        future=['Inspect delegated core rank/solver code and register matched public/generated designs before numerical claims.',
            'Recover RD and CausalPy IV originals independently; keep all omissions local to their candidate.']))
    action='Recover and inspect Python RD and CausalPy IV originals; complete complementary candidate search. Before any native qualification inspect pyfixest core rank/solver and remaining covariance/weight guards, preserving test null/distribution metadata.'
    evidence=[ref(BASE/n,'Reviewed bounded continuation') for n in ['plan.md','source-audit.json','inspected-extracts.json','acquisition-review.json','exact-results.json','conversion-contract.json']]
    write(BASE/'review.json',dict(operation='SW.CELL.iv_rd_design.Python',status='partial_source_progress_not_coverage_outcome',
        finding='Inspected linearmodels rank/fit/covariance and four Git-verified pyfixest delegates; resolved first-stage F-scaling versus chi-square p-value and two-way covariance branch.',
        findings=claims,evidence=evidence,limitations=limitations,next_action=action,global_blocker=None))
    write(BASE/'progress-receipt.json',dict(finding=read(BASE/'review.json')['finding'],next_action=action,
        evidence=[ref(BASE/'review.json','Kernel continuation'),ref(BASE/'source-audit.json','Pinned original claims')],
        yield_reason='Continue preserving integrated reader/sponsor publication and whole-program refresh; Python coverage remains unfinished, with an exact independent source action.'))
    verify_bindings(read(BASE/'source-audit.json'));print(json.dumps(dict(anchors=len(extracts),new_originals=4,coverage_outcome=False,next_action=action)))


if __name__=='__main__':main()
