"""Bind selected inspected source ranges and preserve explicit omissions."""
import hashlib
import json
from pathlib import Path
import panel_inference_reference_20261029 as exact
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT=Path(__file__).resolve().parents[1]
DAY=ROOT/'docs/program/execution/2026-10-29'
BASE=DAY/'panel-inference-contracts-v1'
RAW=ROOT/'docs/literature/raw'
read=lambda p:json.loads(p.read_text())
ANCHORS={
 'schema_0':[(18,20,'Native bounds and confidence metadata'),(79,85,'Already-tidied result ignores new confidence request'),(91,136,'Length, missing-bound derivation, integer clock and window'),(140,171,'First-row labels and delegated row binding')],
 'schema_1':[(1,11,'Per-object list conversion and row binding')],
 'schema_2':[(1,47,'Selected asserted ordinary schema and confidence cases; not executed')],
 'schema_3':[(19,42,'Length checks and separate integerish helper tests'),(61,69,'Unknown fect label expected to become IFE')],
 'schema_4':[(1,99,'Selected alias tests; no fractional alias fixture in this file')],
 'schema_5':[(1,112,'Selected haven-conditional DTA tests; no truncation collision fixture in this file')],
 'bmisc_kernel_0':[],
 'bmisc_kernel_1':[(1,52,'Mean normalization and inconsistent square-root comment'),(57,84,'Packed-bit multiplier generation; exact Rcpp semantics unqualified'),(102,119,'Multiplier signed dot products divided by input row count')],
 'bmisc_kernel_2':[(43,46,'Direct compiled bootstrap wrapper with no extra scaling')],
 'parglm_kernel_0':[(132,180,'Solver defaults, method choices, dimensions and initial-value warnings'),(250,261,'Compiled solver call'),(285,353,'Rank/convergence status and pivot-aware summary/covariance methods')],
 'parglm_kernel_1':[(390,536,'Selected rank/pivot, Cholesky and convergence branches; helpers uninspected')],
 'leaps_kernel_0':[(89,200,'Setup, weights, rank and forced-in handling'),(212,258,'Exhaustive search size guard'),(420,500,'Information criteria, variable order and default search dispatch'),(525,554,'Formula model frame and matrix route')],
 'leaps_kernel_1':[(836,944,'XHAUST bounds and search traversal'),(1106,1171,'Selected singularity handling'),(1205,1255,'Selected tolerance calculation')],
}


def record(planned, candidate, version, ranges):
    stem=planned['id'];p=RAW/(stem+'.txt');rp=RAW/(stem+'.receipt.json')
    data=p.read_bytes();receipt=read(rp)
    blob=hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()
    assert blob==planned['git_blob_sha1']
    assert hashlib.sha256(data).hexdigest()==receipt['sha256']
    identity=planned.get('url',planned.get('source_identity'))
    assert identity==receipt['url']
    lines=data.decode().splitlines(); anchors=[]
    for a,b,finding in ranges:
        assert 1<=a<=b<=len(lines),(stem,a,b,len(lines))
        anchors.append(dict(lines=[a,b],finding=finding,excerpt_sha256=hashlib.sha256('\n'.join(lines[a-1:b]).encode()).hexdigest()))
    return dict(candidate=candidate,source_identity=identity,version_date=version,
                local_copy=ref(p,'Exact acquired bytes'),acquisition_receipt=ref(rp,'Observed public acquisition'),
                git_blob_sha1=blob,inspected_anchors=anchors,supported_claims=[x['finding'] for x in anchors],
                inspection_status='selected_ranges_inspected' if anchors else 'acquired_only_no_technical_claim',
                native_execution=False)


def main():
    assert not (BASE/'review.json').exists()
    rows=[]
    for p in read(BASE/'source-plan.json')['sources']:
        rows.append(record(p,'nonabsdid','2026-06-23T08:50:08Z; '+p['commit'],ANCHORS[p['id'].removeprefix('exec29_panel_')]))
    for p in read(BASE/'kernel-source-plan.json')['sources']:
        rows.append(record(p,p['candidate'],p['date']+'; '+p['commit'],ANCHORS[p['id'].removeprefix('exec29_panel_')]))
    metadata=[]
    for identity in read(BASE/'dependency-identities.json')['repositories']:
        stem='exec29_panel_'+identity['candidate'].lower();tree=read(RAW/(stem+'_tree.json'))
        assert not tree['truncated']
        entry=next(t for t in tree['tree'] if t['path']=='DESCRIPTION')
        p=dict(id=stem+'_description',git_blob_sha1=entry['sha'],url='https://raw.githubusercontent.com/'+identity['repository']+'/'+identity['commit']+'/DESCRIPTION')
        count=len((RAW/(stem+'_description.txt')).read_text().splitlines())
        item=record(p,identity['candidate'],identity['date']+'; '+identity['commit'],[(1,count,'Declared package version, dependencies, compilation and licence; not complete rights clearance')])
        item['identity_navigation']=[ref(RAW/(stem+s),'Cutoff candidate identity; not technical evidence') for s in ('_cutoff.json','_tree.json')]
        metadata.append(item)
    assert len(rows)==13 and len(metadata)==3
    write(BASE/'exact-results.json',exact.calculate())
    sources=[dict(integrated_citation_key='exec29_panel_inference_sources',kind='software_primary_sources',
        title='Pinned panel schemas and bootstrap, numerical and subset-selection delegates',author='Selected panel package contributors',year=2026,
        source_identity='Selected nonabsdid, BMisc, parglm and leaps repository bytes',version_date='Pre-cutoff candidates; inspected 29 October 2026',
        local_copy=rows[0]['local_copy'],records=rows,metadata=metadata,
        inspected_anchors=[dict(anchor='Per-file ranges and excerpt hashes',inspection='Bounded primary text inspection')],
        supported_claims=['Selected constructor, uncertainty, normalization, dispatch and selection contracts.'],
        limits=['One acquired BMisc R file is not technically reviewed. Remaining file tails and dependency helpers are uninspected.',
                'Selected dependency candidates are not an observed installed lockfile. No native execution or rights acceptance.']),
        dict(integrated_citation_key='exec29_panel_inference_reference',kind='project_reference_not_external_paper',
        title='Exact branch-weighting and panel-schema boundary witnesses',author='Causal banking proposal project',year=2026,
        source_identity='tools/panel_inference_reference_20261029.py',version_date='29 October 2026; independent project reference',
        local_copy=ref(Path(exact.__file__),'Performed reference'),results=ref(BASE/'exact-results.json','Exact and numerical results'),
        inspected_anchors=[dict(anchor='cluster_laws, interval and calculate',inspection='Exact algebra and branch witnesses')],
        supported_claims=['Reference variances 9/8 and 5/2, equal-size agreement, partial interval replacement and fractional-clock mismatch.'],
        limits=['Independent signs are an assumption, not a proved native RNG law. No native calibration.'])]
    audit=dict(sources=sources,cutoff='2026-10-07',native_execution=False);verify_bindings(audit);write(BASE/'source-audit.json',audit)
    evidence=[ref(BASE/n,'Reviewed source or argument') for n in ('source-audit.json','exact-results.json','development.tex','sponsor-addition.md','plan-review.json','fetch-exit.json','dependency-fetch-exit.json','kernel-fetch-exit.json')]
    evidence += [ref(Path(__file__),'Source reviewer'),ref(Path(exact.__file__),'Independent witness')]
    write(BASE/'mathematical-review.json',dict(status='pass_for_scoped_project_derivations',issues=[],evidence=evidence,
        findings=['Four sign assignments establish the exact variance distinction conditional on a unit-average influence target.',
                  'Equal-size and reordered-cluster invariants pass; complete and partial interval cases remain distinct.',
                  'Reported native IQR scale and empirical coverage are not inferred from the variance reference.'],native_execution=False,empirical_coverage=False))
    write(BASE/'copyedit-review.json',dict(status='pass_for_source_text',evidence=evidence,rendered_review=False,
        findings=['Connected banking target, uncertainty and CLI/MCP argument; no process history in manuscript.',
                  'Dispatch risk is not called a proved covariance defect; selected tests are not called executed.']))
    remaining=[
        dict(id='INFERENCE.R.STATS',action='Pin R stats summary.glm/vcov.glm and QR paths; construct full-rank, aliased and pivot fixtures.',known_route=True),
        dict(id='INFERENCE.RNG',action='Pin Rcpp sampling implementation and full upstream influence normalization; qualify packed multiplier law and complete draw denominator.',known_route=True),
        dict(id='INFERENCE.BIND',action='Pin dplyr/tibble attribute semantics and exact DCDH/fect/PanelMatch object editions; test mixed confidence provenance.',known_route=True),
        dict(id='INFERENCE.ORIGINALS',action='Resolve genuine pampe/Synth/trend-weighting originals and later fastdid proof edition; unavailable originals remain omitted.',known_route='permitted acquisition attempts; access not guaranteed'),
        dict(id='INFERENCE.NATIVE',action='Fix complete dependency lock and rights profile, then execute bounded public native fixtures with all failures and costs.',known_route=True),
        dict(id='INFERENCE.SCIENCE',action='Obtain justified restrictions or extra information for unknown counterfactual trends and unrestricted dependence; no universal repair promised.',known_route=False),
        dict(id='INFERENCE.ACCEPTANCE',action='Complete independent coverage/depth work and fresh visual review; canonical and final gates remain open.',known_route=True)]
    write(BASE/'remaining-obligations.json',dict(status='open_local_continuations',actions=remaining,canonical_gaps_closed=[],evidence=evidence))
    write(BASE/'review.json',dict(status='pass_for_bounded_source_addition',acquired_source_files=13,inspected_source_files=12,metadata_files=3,
        evidence=evidence+[ref(BASE/'mathematical-review.json','Derivation review'),ref(BASE/'remaining-obligations.json','Local omissions and routes')],
        native_execution=False,visual_acceptance=False,final_acceptance=False))
    print(json.dumps(dict(source_records=2,acquired_source_files=13,inspected_source_files=12,metadata_files=3,exact_witnesses='pass',canonical_acceptance=False)))


if __name__=='__main__':main()
