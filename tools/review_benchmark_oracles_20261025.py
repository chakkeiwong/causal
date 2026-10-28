#!/usr/bin/env python3
"""Audit retained originals and independently authored oracle fixtures."""
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
import benchmark_oracle_reference_20261025 as exact
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-25/benchmark-oracles-v1'
PRIOR=BASE.parent/'agent-evaluation-surveys-reader-v2/reader/source-audit.json'
OLD=ROOT/'docs/program/execution/2026-10-14/evaluation-cost/primary-review.json'
read=lambda p:json.loads(p.read_text())
LIMITS=['Static pinned-source inspection and independent finite project witnesses; no downloaded code executed.','Graph-level counterexample is not a measured failure rate or proof that every generated benchmark item is wrong.','Full generator,visible-information,parser,dependency and native conformance paths remain unqualified.','No complete rights,calibration,independent,visual,bank or final acceptance.']

def main():
    assert not (BASE/'review.json').exists()
    prior=read(PRIOR);verify_bindings(prior)
    packages=read(OLD)['packages'];verify_bindings(packages)
    bypath={r['path']:r for p in packages for r in p['originals']}
    specs=[
        ('v12_la_cladder_source_1.txt',[(15,58,'IV known-estimand terms and ratio metadata'),(103,144,'Question generation separately calls treatment-effect bounds')]),
        ('v12_la_cladder_source_2.txt',[(293,301,'Unobserved V1; independent-root instrument and treatment/outcome parents')]),
        ('v12_la_causalds_source_1.txt',[(186,239,'Backend failure and unavailable states retain identifiable null'),(303,329,'IV-only method filtered from nonparametric population-ATE result')]),
        ('v12_la_causalds_source_2.txt',[(152,174,'Missing/null ATE and exact-false counterfactual grading helpers'),(294,370,'Intentional abstention versus malformed-answer handling'),(1507,1568,'Local interval conversion,ordering and scoring branch'),(3529,3555,'Both uncapped and capped aggregate losses and separate coverage/width')])]
    inspected=[]
    for filename,anchors in specs:
        path=ROOT/'docs/literature/raw'/filename;binding=bypath[str(path.relative_to(ROOT))];verify_bindings(binding)
        lines=path.read_text().splitlines()
        for lo,hi,finding in anchors:
            inspected.append(dict(source_identity=binding['source_identity'],original=ref(path,f'Lines {lo}-{hi}'),lines=[lo,hi],finding=finding,excerpt=chr(10).join(lines[lo-1:hi])))
    write(BASE/'inspected-source-anchors.json',dict(cutoff='2026-10-07T15:59:59Z',anchors=inspected,packages=[dict(id=p['id'],commit=p['commit'],commit_date=p['commit_date'],source_identity=p['source_identity']) for p in packages],native_execution=False))
    result=exact.calculate();write(BASE/'exact-results.json',result)
    write(BASE/'mathematical-review.json',dict(status='pass_for_independent_finite_witnesses',evidence=[ref(Path(exact.__file__),'Independent standard-library implementation'),ref(BASE/'exact-results.json','Exact enumeration and numeric-contract cases'),ref(BASE/'development.tex','Explained assumptions and connected banking interpretation')],findings=['Four exact observed support probabilities agree across both IV worlds; population effects have opposite signs.','Instrument exogeneity,exclusion,monotonicity and relevance hold by construction.','Financial translation is -500000 versus250000USD under stipulated scale and no costs.','Explicit identification-state and refusal matrix preserves unknown reference truth.','Finite interval losses2and41 reproduce; nonfinite,invalid and overflowing cases rejected.','Clipping at10 reverses aggregate ranking10versus1to0.1versus1.'],limitations=LIMITS))
    selected={s['integrated_citation_key']:s for s in prior['sources']}
    reused=[deepcopy(selected[k]) for k in ['v12_la_2312_04350','v12_la_2607_08093']]
    source=dict(integrated_citation_key='exec25_bor_sources',kind='software_primary_sources',title='Pinned CLadder and CausalDS causal-oracle and grading branch inspection',author='causalNLP and andleb contributors',year=2026,source_identity='https://github.com/causalNLP/cladder ; https://github.com/andleb/causalds',version_date='CLadder 3d2d1169b4b939a09048a6a75956c8972a93cc38 (29 May 2024); CausalDS c74671d0a0924efc5bb021fc8966f856d5b80a4f (17 July 2026)',local_copy=ref(BASE/'inspected-source-anchors.json','Exact original bytes,URLs,line excerpts and source identities'),records=packages,inspected_anchors=[dict(anchor=x['finding'],source=x['original']) for x in inspected],supported_claims=[x['finding'] for x in inspected],limitations=LIMITS)
    project=dict(integrated_citation_key='exec25_bor_reference',kind='project_derivation_and_exact_reference',title='Independent finite IV identification and scoring-contract witnesses',author='Causal banking proposal project',year=2026,source_identity='tools/benchmark_oracle_reference_20261025.py',version_date='25 October 2026; exact finite project constructions',local_copy=ref(Path(exact.__file__),'Authored independent enumerator and validation reference'),inspected_anchors=[ref(BASE/'exact-results.json','Complete exact outputs'),ref(BASE/'mathematical-review.json','Premises,calculations and limitations')],supported_claims=read(BASE/'mathematical-review.json')['findings'],limitations=LIMITS)
    write(BASE/'source-audit.json',dict(sources=reused+[source,project],cutoff='2026-10-07T15:59:59Z',prior_audit=ref(PRIOR,'1390 preserved citation identities'),native_execution=False))
    qualification=dict(status='preregistered_proposal_design_not_native_execution',task='LA01-benchmark-oracles',source=ref(BASE/'inspected-source-anchors.json','Pinned source scope'),fixtures=ref(BASE/'exact-results.json','Independent expected outputs'),requirements=['Bind generated task,visible information,target,source,dependencies and oracle identity.','Separate graph-level compatible-world witness from per-item native label correctness.','Test zero first stage and restricted-effect alternatives in addition to current finite witnesses.','Preserve true,false,null,missing,error and malformed metadata distinctly.','Test complete parser and caller paths; isolate unknown oracle from model refusal and invalid response.','Validate endpoints,truth,confidence level and arithmetic results for finiteness.','Report raw and capped losses,coverage,width,tail loss and every request/refusal/failure/quarantine count.','Record exact environment,artifacts,rights,full attempt cost and reviewer before adoption.'],native_runs=0,bank_runs=0,completion_criterion='Each admitted task/version passes independent semantic,identification,finite-arithmetic and complete-denominator conformance under its declared regime.',next_action='Implement and run the bounded native fixture harness in a separately admitted environment;retain failures and unknown targets without inventing oracle truth.')
    write(BASE/'qualification-design.json',qualification)
    census=read(BASE.parent/'census-observation-workflow-v1/census-register.json');verify_bindings(census);reg=deepcopy(census)
    row=next(x for x in reg['items'] if x['id']=='LA01-benchmark-oracles');assert row['disposition']=='open_benchmark_qualification'
    row.update(effect_on_claims='Independent finite witnesses resolve the graph-level IV and local scoring-contract pitfalls;full native item/generator/scorer qualification remains open.',source_followup=ref(BASE/'source-audit.json','Reinspected pinned originals and exact project references'),qualification_design=ref(BASE/'qualification-design.json','Bounded public prototype admission contract'),next_action=qualification['next_action'])
    assert Counter(x['disposition'] for x in census['items'])==Counter(x['disposition'] for x in reg['items'])
    reg.update(supersedes=ref(BASE.parent/'census-observation-workflow-v1/census-register.json','Unchanged original dispositions'),changes=['Independent finite oracle witnesses and public qualification design added; no original or crosscutting obligation closed.'],closure=False)
    write(BASE/'census-register.json',reg)
    write(BASE/'copyedit-review.json',dict(status='pass_for_connected_argument',evidence=[ref(BASE/'development.tex','Target,proof,scoring and bounded trial argument'),ref(BASE/'sponsor-addition.md','Concrete investment consequence')],findings=['Sources and independent examples remain distinct.','Native and full-generator uncertainty retained.','Existing uncapped score and abstention protections acknowledged.','Financial examples reproduce and are explicitly stipulated.'],visual_acceptance=False))
    evidence=[ref(BASE/n,'Reviewed evidence') for n in ['plan.md','inspected-source-anchors.json','source-audit.json','exact-results.json','mathematical-review.json','qualification-design.json','census-register.json','copyedit-review.json','development.tex','sponsor-addition.md']]+[ref(Path(__file__),'Scoped review')]
    write(BASE/'plan-review.json',dict(status='pass_for_bounded_independent_oracle_review',evidence=evidence,steps=['Inspect retained pinned originals.','Independently derive graph and scoring witnesses.','Keep full native qualification open.','Integrate preserving reader and exact sponsor after consumed predecessor.'],coverage_acceptance=False,native_execution=False,visual_acceptance=False))
    evidence.append(ref(BASE/'plan-review.json','Reviewed execution plan'));verify_bindings(dict(evidence=evidence))
    write(BASE/'review.json',dict(status='pass_for_scoped_source_and_project_review',evidence=evidence,new_citation_records=2,reused_papers=2,new_scholarly_papers=0,census_inspected=82,census_unread=31,crosscutting=4,limitations=LIMITS,coverage_acceptance=False,native_execution=False,visual_acceptance=False))
    print(json.dumps(dict(review='pass',new_records=2,original_dispositions_changed=0,native_execution=False)))

if __name__=='__main__':main()
