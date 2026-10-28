"""Reconcile every proposal obligation after the linguistic-measurement publication."""
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
ROOT=Path(__file__).resolve().parents[1]
DAY=ROOT/'docs/program/execution/2026-10-28'
BASE=DAY/'program-refresh-causal-modeling-v1'
PRIOR=DAY/'program-refresh-linguistic-measurement-v1'
SOURCE=DAY/'causal-modeling-lead-v1'
READER=DAY/'causal-modeling-reader-v1'
SPONSOR=DAY/'sponsor-causal-modeling-v1'
read=lambda p:json.loads(p.read_text())

def main():
    assert not BASE.exists()
    run=controller.base;core=run.core;state=core.read(ROOT,core.STATE)
    assert state['execution_runtime']['active'] is None
    view=controller.status(ROOT,state);graph,merged,stages,ready,_=run.queue(ROOT,state)
    reader=read(READER/'working-release.json');sponsor=read(SPONSOR/'working-release.json')
    for d in [reader,sponsor,read(SOURCE/'review.json'),read(PRIOR/'remaining-operations.json')]:verify_bindings(d)
    assert run.same_reader(state['reader'],reader['pdf']) and run.same_reader(state['reader'],sponsor['paired_monograph'])
    assert any(run.same_reader(x,sponsor['pdf']) for x in state['deliveries'] if x.get('kind')=='working_sponsor')
    assert {x['id']:x['status'] for x in view['proposal_gaps']}==dict(Q1='open',Q2='pass',Q3='pass',Q4='pass',Q5='open')
    prior=read(PRIOR/'remaining-operations.json');remaining=deepcopy(prior);results=merged['execution_program']['results']
    actual={n['id'] for n in graph['nodes'] if stages[n['id']]=='proposal_now' and results.get(n['id'],{}).get('outcome')!='pass'}
    assert actual=={x['id'] for x in remaining['operations']} and len(actual)==150
    groups={}
    for name,prefix,total in [('software','SW.CELL.',102),('reuse','SW.DECISION.',115),('chapters','TEXT.REVIEW.',22)]:
        selected=[v for k,v in results.items() if k.startswith(prefix)]
        groups[name]=dict(Counter(v['outcome'] for v in selected),open=total-len(selected),total=total)
    assert groups==prior['coverage']
    assert view['proposal_operations']==376 and view['recorded_proposal_operations']==350
    counts=Counter(x['disposition'] for x in read(SOURCE/'census-register.json')['items'])
    assert counts['inspected_primary_retained_with_limits']==82 and counts['open_original_not_inspected']==31
    note=merged['execution_program']['progress']['LL.CENSUS'][-1];action=read(ROOT/note['path'])['next_action']
    row=next(x for x in remaining['operations'] if x['id']=='LL.CENSUS');row.update(action=action,action_checkpoint=note)
    remaining.update(reader=state['reader'],ready=len(ready),coverage=groups,census=ref(SOURCE/'census-register.json','Unchanged dispositions'),predecessor=ref(PRIOR/'remaining-operations.json','All unresolved operations preserved'))
    assert len(read(READER/'reader/source-audit.json')['sources'])==1397 and len(read(SPONSOR/'source-audit.json')['sources'])==1044
    BASE.mkdir();write(BASE/'state-snapshot.json',state);write(BASE/'remaining-operations.json',remaining);write(BASE/'status-snapshot.json',view)
    review=dict(status='pass_for_consistency_not_completion',evidence=[ref(READER/'working-release.json','Exact reader'),ref(SPONSOR/'working-release.json','Exact paired sponsor'),ref(SOURCE/'review.json','Primary source and exact mathematics'),ref(SOURCE/'census-register.json','Unchanged census'),ref(BASE/'remaining-operations.json','All150nonpassing obligations'),ref(Path(__file__),'Complete reconciliation')],findings=['All376proposal obligations accounted for;350recorded and150nonpassing.','One later search original is integrated without changing the inherited census denominator.','All1395prior source records,contexts and411content inputs retained;1397records and269scholarly PDFs.','Sponsor preserves1040records and adds4; exact current counts and reader pairing verified.','Actual census acceptance criteria and95later search rows are explicit;2rows now bind the reviewed original.'],ready_operations=[x['id'] for x in ready],global_blocker=None,phase_boundaries_are_stopping_points=False,visual_acceptance=False,final_acceptance=False,background_worker_running=False)
    verify_bindings(review);write(BASE/'program-review.json',review)
    current=ROOT/'docs/program/execution/current-program.md';(BASE/'prior-current-program.md').write_bytes(current.read_bytes());text=current.read_text()
    for name in ['program-review.json','remaining-operations.json','prior-current-program.md']:
        text=text.replace('2026-10-28/program-refresh-linguistic-measurement-v1/'+name,'2026-10-28/program-refresh-causal-modeling-v1/'+name)
    start=text.index('## Current integrated documents');end=text.index('## Remaining gaps and routes')
    block=f'''## Current integrated documents

The [monograph](../../causal_proposal_causal_modeling_reviewed_v1_2026-10-28.pdf) has {reader['pages']:,} pages,
1,397 audited citation records and 269 genuine scholarly PDFs. The exact paired
[sponsor proposal](../../sponsor_proposal_causal_modeling_reviewed_2026-10-28.pdf) has {sponsor['pages']} pages and 1,044 citations.
All 1,395 predecessor records, citation contexts and 411 compiled content inputs survive.
Source traceability, exact authored examples and all-page text/bounds checks pass; Q2-Q4 pass for exact bytes.
Q1/Q5, mandatory coverage/depth and fresh visual/final acceptance remain open. Page count is not completion.

**350 recorded outcomes of 376; {len(ready)} ready; 150 nonpassing obligations.**
Software remains three pass / 98 inconclusive / one open; reuse 109 pass / four inconclusive / two open.
Census remains 82 inspected / 31 unread plus four crosscutting tasks. Recorded findings are not capability qualification.

## Newly integrated work

The new section distinguishes business phrases, variable values, compound entities and causal interventions.
The inspected Razouk preprint reports seven models evaluated on generated data; independent bank truth is not inferred.
Exact authored examples distinguish compound wording from additive causal interaction and graph paths from nonzero total mean effects.
All source-reported scores remain tied to historical task definitions, model labels and generated-label denominators.

The [census contract audit](2026-10-28/census-acceptance-scope-v1/review.json) identifies an execution-scope problem:
LL.CENSUS requires evidence-backed dispositions, task mapping, complementary bounded searches and citation chaining.
It permits recorded source unavailability with affected claims restricted. Native installation and bank validation are separate gates.
No unread paper becomes inspected, and no coverage or final acceptance is granted by this diagnosis.

The [followup register](2026-10-28/causal-modeling-lead-v1/followup-lead-register.json) preserves 60 earlier and 35 specialist search rows.
Two rows now bind the inspected causal-modeling preprint. The remaining 93 need explicit identity/version and source-disposition reconciliation.
This queue is separate from the 113 inherited candidate census and prevents untracked later discoveries from being overlooked.

The prior linguistic intervention and component-adoption section remains intact. Its exact proxy example and LLM-CD/LLM-and-SCD/LCM limits
remain qualified. Public/generated prototype evidence, source coverage, native qualification and bank acceptance retain distinct outcomes.

'''
    text=text[:start]+block+text[end:]
    text=text.replace('2026-10-28/program-refresh-linguistic-measurement-v1/remaining-operations.json','2026-10-28/program-refresh-causal-modeling-v1/remaining-operations.json')
    start=text.index('Next: LL.CENSUS.');end=text.index('\n\nSerialize canonical mutations',start)
    text=text[:start]+'Next: LL.CENSUS. '+action+text[end:]
    current.write_text(text);controller.render(ROOT,state)
    write(BASE/'continuation-checkpoint.json',dict(reader=state['reader'],sponsor=sponsor['pdf'],remaining=ref(BASE/'remaining-operations.json','Exact continuation'),next_action=action,visual_acceptance=False,final_acceptance=False,background_worker_running=False))
    print(json.dumps(dict(recorded=350,ready=len(ready),nonpassing=150,reader_pages=reader['pages'],sponsor_pages=sponsor['pages'])))

if __name__=='__main__':main()
