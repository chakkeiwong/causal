"""Bind inspected delegate claims and independent arithmetic without native admission."""
import hashlib,json
from pathlib import Path
import panel_delegate_reference_20261028 as exact
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write
ROOT=Path(__file__).resolve().parents[1];DAY=ROOT/'docs/program/execution/2026-10-28'
BASE=DAY/'panel-delegates-v1';RAW=ROOT/'docs/literature/raw'


def main():
    assert not (BASE/'review.json').exists()
    claims={
      'fastdid':{
        0:[(52,128,'Normalize calendar/event clocks and require uniform spacing'),(136,185,'Exclude unsupported event-specific cells and intersect donor cohort identities'),(191,302,'Direct, target-first base anchor and target-later differencing; equal timing has no separating branch')],
        1:[(18,58,'Transform effects and influence functions with estimated-share contributions'),(124,171,'Balance selector checks cohort extrema, not full surviving interior membership'),(223,301,'Signed period-specific share influence and downstream bootstrap/interval construction')],
        2:[(16,106,'Skip invalid, failed and effective-small group-time cells'),(112,203,'Baseline and control selection with anticipation horizons; final estimator delegated')],
        3:[(1,108,'Argument validation and restrictions on unbalanced DR, covariates and clustering'),(112,256,'Missing/first-period/incomplete-unit exclusions, duplicate detection and integer conversion')]},
      'nonabsdid':{
        0:[(93,192,'Method-specific dispatch, knobs and tidy conversion'),(210,273,'Parsed DCDH horizon call, environment and named extra arguments'),(275,341,'PanelMatch matching defaults and treatment reversal setting'),(344,432,'fect tuning/inference defaults and protected-argument handling')],
        1:[(90,194,'Named/binary/ID preflight and explicit differing missing-data sample warning')],
        2:[(80,181,'Effect-cell schema and conditional normal CI/SE conversion')]},
      'pampe':{
        0:[(1,108,'Single-unit and complete-data checks, selected pre-row model fitting and model-size bound'),(120,257,'Placebo variants and returned model/data without original row vectors')],
        1:[(1,64,'AIC/AICc/BIC calculation including likelihood parameter count')],
        2:[(1,36,'Reconstructed initial rows and fixed-retained-subset leave-one-out refits')]}}
    rows=[]
    for key,files in claims.items():
        ident=next(x for x in json.loads((DAY/'panel-originals-v1/identity-review.json').read_text())['repositories'] if x['candidate']==key)
        tree=json.loads((RAW/f'exec28_panel_{key}_tree.json').read_text());lookup={x['path']:x for x in tree['tree']}
        for j,anchors in files.items():
            stem=f'exec28_panel_{key}_delegate_{j}';p=RAW/(stem+'.txt');receipt=json.loads((RAW/(stem+'.receipt.json')).read_text());data=p.read_bytes()
            upstream=receipt['url'].split(ident['commit']+'/',1)[1]
            blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
            assert blob==lookup[upstream]['sha'] and hashlib.sha256(data).hexdigest()==receipt['sha256']
            lines=data.decode().splitlines();inspected=[]
            for a,b,finding in anchors:
                assert 1<=a<=b<=len(lines)
                inspected.append(dict(lines=[a,b],finding=finding,excerpt_sha256=hashlib.sha256(chr(10).join(lines[a-1:b]).encode()).hexdigest()))
            rows.append(dict(candidate=key,source_identity=receipt['url'],version_date=ident['date']+'; '+ident['commit'],
                local_copy=ref(p,'Exact inspected implementation text'),acquisition_receipt=ref(RAW/(stem+'.receipt.json'),'Observed public acquisition'),
                git_blob_sha1=blob,inspected_anchors=inspected,supported_claims=[x['finding'] for x in inspected],native_execution=False))
    write(BASE/'exact-results.json',exact.calculate())
    sources=[dict(integrated_citation_key='exec28_panel_delegates',kind='software_primary_sources',
        title='Pinned fastdid, nonabsdid and pampe delegate contracts',author='Selected panel package contributors',year=2026,
        source_identity='Ten pinned files from TsaiLintung/fastdid, cran/nonabsdid and cran/pampe',
        version_date='Per-record exact pre-cutoff commits; reviewed 28 October 2026',local_copy=rows[0]['local_copy'],records=rows,
        inspected_anchors=[dict(anchor='Exact per-record line ranges and excerpts',inspection='Static primary implementation review')],
        supported_claims=['Specific baseline, event-order, donor intersection, aggregation, validation, wrapper and donor-row contracts.'],
        limits=['No native execution, full dependency audit, unrestricted multiple-event proof or empirical coverage.','Upstream test claims in comments are not treated as performed project tests.']),
      dict(integrated_citation_key='exec28_panel_delegate_reference',kind='project_reference_not_external_paper',
        title='Exact panel adapter balance, date and timeline witnesses',author='Causal banking proposal project',year=2026,
        source_identity='tools/panel_delegate_reference_20261028.py',version_date='28 October 2026; authored exact Fraction reference',
        local_copy=ref(Path(exact.__file__),'Independent arithmetic and predicate transcription'),results=ref(BASE/'exact-results.json','Exact outputs'),
        evidence=[ref(RAW/'exec28_panel_stacked_identity_1.txt','Previously inspected R/Stata predicates and count formulas')],
        inspected_anchors=[dict(anchor='calculate(): balanced/unequal counts, numeric adoption predicate, donor intersection and row-clock example',inspection='Independent source-contract derivation')],
        supported_claims=['Triangular and row counts agree under common balance and differ in the stated unbalanced case.','Numeric adoption1 is an extra selected predicate case.','Stored-row and reconstructed-row diagnostics differ.'],limits=['Not executed R/Stata behavior; no unbalanced causal or uncertainty qualification.'])]
    audit=dict(sources=sources,cutoff='2026-10-07',native_execution=False);verify_bindings(audit);write(BASE/'source-audit.json',audit)
    evidence=[ref(BASE/n,'Reviewed source or authored argument') for n in ['source-audit.json','exact-results.json','development.tex','sponsor-addition.md','plan-review.json']]+[ref(Path(__file__),'Performed source audit'),ref(Path(exact.__file__),'Exact independent witness')]
    remaining=[
        'Obtain exact later paper edition named by fastdid; M>=3 and anticipation extensions are not proved by selected v3.',
        'Inspect final estimate_did, propensity/outcome, BMisc bootstrap and argument-coercion delegates plus tests and dependency versions.',
        'Check all interior event-time cells, control-option combinations, units/clusters and zero/negative weight handling on a declared profile.',
        'Inspect nonabsdid tidiers, aliases/data resolution, upstream packages and tests; preserve native intervals, options, original IDs and effective samples.',
        'Inspect leaps exact subset selector and package originals; preserve pampe row indices and test model-size/selection-aware placebo variants.',
        'Resolve stacked permissions and test actual R/Stata profile before porting; do not generalize triangular cancellation to unbalanced samples.',
        'Fresh visual, independent review and later bank acceptance remain open.']
    write(BASE/'remaining-obligations.json',dict(status='open_local_continuations',actions=remaining,canonical_gaps_closed=[],evidence=evidence))
    write(BASE/'mathematical-review.json',dict(status='pass_for_scoped_project_derivations',issues=[],evidence=evidence,
        findings=['Static target-first weight selects base period, matching Appendix17 rather than selected equation11 target period.','Intersection example: separate means change55/2; common B change5.','Common observation length cancels triangular factors; unequal example gives2/3,4/3 versus4/5,6/5.','Numeric date1 predicate witness separates intended and selected inclusion.','Pampe feasible eight-row example distinguishes5:12 from1:8; AICc example is64/3.'],
        native_execution=False,empirical_coverage=False,all_source_theorems_independently_verified=False))
    write(BASE/'copyedit-review.json',dict(status='pass_for_source_text',evidence=evidence,
        findings=['Connected banking consequence and conditional adoption decisions.','Selected source findings separated from executed behavior, proof and rights.','No inferred upstream tests are presented as performed.'],rendered_review=False))
    write(BASE/'review.json',dict(status='pass_for_bounded_delegate_addition',pinned_files=10,evidence=evidence+[ref(BASE/'mathematical-review.json','Algebra and assumptions'),ref(BASE/'remaining-obligations.json','Local remaining work')],native_execution=False,visual_acceptance=False,final_acceptance=False))
    print(json.dumps(dict(pinned_files=10,source_records=2,exact_witnesses='pass',canonical_acceptance=False)))


if __name__=='__main__':main()
