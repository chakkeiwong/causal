#!/usr/bin/env python3
"""Bind selected Python synthetic-control sources, comparisons and exact witnesses."""
import argparse
import json
from pathlib import Path
import synthetic_python_reference_20261025 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings

run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-25/synthetic-python-coverage-v1'
RAW=ROOT/'docs/literature/raw';OP='SW.CELL.synthetic_controls.Python'
read=lambda p:json.loads(p.read_text())
LIMITS=[
 'Bounded selected-source comparison; complementary search pages and substantive candidates remain uninspected.',
 'No downloaded package, installed R distribution or upstream test executed; source predicates are not native failures.',
 'Package notices, conflicting packaging declarations, transitive rights and resolved solver artifacts require further review.',
 'Assignment exchangeability, counterfactual stability and arbitrary serial dependence are not established by package choice.',
 'No new scholarly work admitted; visual, independent, bank and final acceptance remain open.'
]
NEXT='Inspect remaining Python synthetic-control candidates and search tails, resolve package/dependency provenance, complete inference/solver delegates and preregister target-matched public native qualification. Preserve failed-draw denominators, tie rules, donor/spillover assumptions, conditional/predictive targets and all retained source findings; no universal calibration claim.'


def prepare():
    assert not (BASE/'review.json').exists()
    validation=read(BASE/'git-byte-validation-v2.json');assert validation['status']=='pass' and validation['count']==31
    for row in validation['originals']:
        assert core.sha(ROOT/row['local_path'])==row['sha256']
    write(BASE/'exact-results.json',exact.calculate())
    groups=read(BASE/'source-spec.json')
    primary=[];sources=[]
    for key,(title,repo,version,checks) in groups.items():
        evidence=[];anchors=[];claims=[]
        for filename,lo,hi,tokens,finding in checks:
            p=(ROOT/filename if filename.startswith('docs/') else RAW/filename);lines=p.read_text().splitlines();fragment='\n'.join(lines[lo-1:hi]);assert all(t in fragment for t in tokens),(filename,lo,hi,[t for t in tokens if t not in fragment])
            binding=ref(p,f'Lines {lo}-{min(hi,len(lines))}: {finding}')
            evidence.append(binding);anchors.append(dict(path=binding['path'],line_spans=[[lo,min(hi,len(lines))]],finding=finding));claims.append(finding)
        primary.append(dict(group=key,evidence=evidence,inspected_anchors=anchors,supported_claims=claims))
        sources.append(dict(integrated_citation_key='exec25_synthpy_'+key,kind='software',title=title,author=repo+' contributors',year=int(version.split(';')[1].strip()[-4:]),source_identity='https://github.com/'+repo+'/tree/'+version.split(';')[-1].strip(),version_date=version,local_copy=evidence[0],evidence=evidence,inspected_anchors=anchors,supported_claims=claims,limitations=LIMITS,native_execution=False))
    write(BASE/'primary-review.json',dict(status='pass_for_selected_source_anchors',groups=primary,evidence=[ref(BASE/'git-byte-validation-v2.json','31 original files authenticated'),ref(ROOT/'docs/program/execution/2026-10-14/causalpy-reuse/source-audit-v2.json','Inherited CausalPy originals and reviewed limits')],native_execution=False))
    write(BASE/'mathematical-review.json',dict(status='pass_for_authored_exact_witnesses',evidence=[ref(Path(exact.__file__),'Independent rational arithmetic'),ref(BASE/'exact-results.json','Exact replay')],checks=['Cutoff partitions yield10/3,2/3and10for the exact stipulated gaps.','Observed-assignment inclusion changes0to1/3withtwo donors andzero exceedances.','Mean unitRMS differs fromRMSof average;conditional-mean andpredictive draws differ.','Row sums,duration totals,horizon masks andvarianceof sums preserve distinct targets.','Costs are hypothetical;no native result orscientific calibration claimed.']))
    write(BASE/'comparison-review.json',dict(operation=OP,status='inconclusive',registered_candidates=['CausalPy'],additional_selected=['pysyncon','SparseSC','SyntheticControlMethods'],target='Regional banking untreated revenue and explicit unit/time/exposure aggregation',comparisons=['Strict/inclusive treatment-date partitions and unmatched date encodings','Conditional expectations versus predictive outcomes and cumulative economic targets','Simplex,augmentation,retrospective SVD and penalized objectives','Solver status,interval-refit state,placebo populations and actual-assignment conventions','Cross-fit and combination targets,dependencies and packaging provenance'],limitations=LIMITS,next_action=NEXT))
    write(BASE/'dependency-license-review.json',dict(status='not_complete_clearance',evidence=[ref(BASE/'primary-review.json','Original metadata/license/provenance anchors')],rights=['CausalPy Apache2original retained;installed distribution and dependencies unresolved','pysyncon MITnotice retained;SciPy and complete environment not qualified','SparseSC MITlicense and BSDpackaging classifier discrepancy retained','SyntheticControlMethods Apache2license/source headers versus MITpackaging field retained','No legal conclusion or installed-artifact/dependency clearance granted'],integration_allowed=False))
    write(BASE/'qualification-plan.json',dict(status='proposed_not_executed',tests=['Donor identity,spillovers,treatment-date partitions and unmatched-date refusal','Matched conditional-mean,predictive,unit/time and duration-weighted targets','Solver status,zero-prefit error,interval search and repeated-estimator-state oracles','Plot filters versus inference denominators;actual-assignment and subset sampling rules','Law-specific uncertainty and complete failed-request denominators','Artifact identity,conflicting packaging declarations,dependency rights and total costs'],owners=['Scientific author','Adapter owner','Environment and rights owner','Evaluation reviewer'],native_execution=False))
    write(BASE/'omissions-register.json',dict(global_blocker=False,known_routes=['Inspect outstanding search pages and concrete leads','Complete estimator/solver delegates and conflicting packaging declarations','Pin public native environment and preregister exact law-specific qualification'],unknown_universal_repairs=['Untreated trajectory and donor-spillover truth require assumptions or new information','Arbitrary serial dependence and invalid assignment laws have no automatic package repair'],evidence=[ref(BASE/'search-screening.json','39leads with incomplete search tails')],next_action=NEXT))
    sources.append(dict(integrated_citation_key='exec25_synthpy_choice',kind='project_evidence_not_scholarly_paper',title='Authored Python synthetic-control comparison, source boundaries and public qualification witnesses',author='Causal banking proposal project',year=2026,source_identity=str(BASE.relative_to(ROOT)),version_date='25 October 2026; literature cutoff7 October2026; no native execution',local_copy=ref(BASE/'mathematical-review.json','Authored rational witnesses'),evidence=[ref(BASE/n,'Reviewed comparison evidence') for n in ['comparison-review.json','search-screening.json','dependency-license-review.json','qualification-plan.json','omissions-register.json']],inspected_anchors=[dict(anchor='Clock,target,source boundaries,placebo conventions,aggregation and costs',inspection='Author inspection')],supported_claims=['Selected comparisons and exact stipulated witnesses','Bounded search and explicit unresolved coverage'],limitations=LIMITS))
    write(BASE/'source-audit.json',dict(sources=sources,new_records=5,new_scholarly_pdfs=0,native_execution=False));verify_bindings(read(BASE/'source-audit.json'))
    write(BASE/'plan-review-v2.json',dict(status='pass_for_inconclusive_source_work',evidence=[ref(BASE/n,'Reviewed plan and actual evidence') for n in ['plan.md','plan-review.json','primary-review.json','comparison-review.json','mathematical-review.json','dependency-license-review.json','qualification-plan.json','omissions-register.json']],findings=['Inherited CausalPy and three selected additional implementations differentiated','39leads retain uninspected tails;no exhaustive-pass claim','31new original files and seven inherited CausalPy delegates authenticated','No native execution,legal clearance,scientific calibration or visual acceptance implied']))
    write(BASE/'copyedit-review.json',dict(status='pass_for_connected_argument',evidence=[ref(BASE/'development.tex','Banking target,notation,alternatives and explicit limitations'),ref(BASE/'sponsor-addition.md','Investment case implications')],findings=['Source observations,authored arithmetic and proposed tests distinguished','Tied ranks and incomplete denominators not overstated as native failures','License metadata and reused-code provenance separate'],visual_acceptance=False))
    names=['git-byte-validation-v2.json','primary-review.json','comparison-review.json','search-screening.json','mathematical-review.json','exact-results.json','source-audit.json','dependency-license-review.json','qualification-plan.json','omissions-register.json','plan-review-v2.json','copyedit-review.json','development.tex','sponsor-addition.md']
    review=dict(status='pass_for_selected_source_work',operation_outcome='inconclusive',evidence=[ref(BASE/n,'Bounded source evidence') for n in names]+[ref(Path(__file__),'Review and receipt logic')],findings=['31new originals authenticated','New comparison does not replace prior package arguments','Coverage remains inconclusive'],limitations=LIMITS,native_execution=False)
    verify_bindings(review);write(BASE/'review.json',review);print(json.dumps(dict(review='pass_for_selected_work',outcome='inconclusive',originals=31,new_records=5)))


def receipt():
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==OP;verify_bindings(read(BASE/'review.json'))
    graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP);value=read(BASE/'comparison-review.json');value['evidence']=[ref(BASE/'review.json','Selected source review')];output=ROOT/node['outputs'][0];write(output,value)
    ev=[ref(BASE/n,'Reviewed bounded coverage') for n in ['review.json','search-screening.json','source-audit.json','omissions-register.json']]
    findings=['Registered candidates and selected additions identified;search/technical tails remain incomplete','Selected claims bind authentic source/version/hash/anchors;no new scholarly claim','Alternatives,rights,native limits and next actions explicit;no absence or waiver claim']
    result=run.ledger.receipt_template(node);result.update(outcome='inconclusive',execution='performed',scope='Python synthetic-control comparison with selected delegates;coverage incomplete',reviewer=dict(name='Codex author/coordinator',kind='author'),outputs=[ref(output,'Bounded coverage')],criteria=[dict(index=i,verdict='inconclusive' if i==0 else 'pass',finding=f,evidence=ev) for i,f in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=NEXT)
    run.validate_receipt(ROOT,merged,node,result,len(state['execution_program']['turns']));verify_bindings(result);write(BASE/'operation-receipt.json',result);print('Python synthetic-control inconclusive receipt prepared.')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','receipt']);globals()[p.parse_args().command]()
