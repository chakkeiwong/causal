#!/usr/bin/env python3
"""Reconcile every proposal obligation after the SCOPE-RL publication pair."""
from collections import Counter,defaultdict
from copy import deepcopy
from pathlib import Path
import json,subprocess
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT;DAY=ROOT/'docs/program/execution/2026-10-23'
BASE=DAY/'program-refresh-scope-rl-reuse-v1';PRIOR=DAY/'program-refresh-controlled-writes-v1'
PUB=DAY/'scope-rl-reuse-reader-v1';SPONSOR=DAY/'sponsor-scope-rl-reuse-v1';SOURCE=DAY/'scope-rl-reuse-v1'
CENSUS=DAY/'census-controlled-writes-v1'
read=lambda p:json.loads(p.read_text())
def main():
 assert not BASE.exists()
 state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active'] is None
 view=controller.status(ROOT,state);graph,merged,stages,ready,_=run.queue(ROOT,state)
 pub=read(PUB/'working-release.json');sponsor=read(SPONSOR/'working-release.json')
 for d in [pub,sponsor,read(PRIOR/'program-review.json'),read(SOURCE/'review.json')]:verify_bindings(d)
 assert run.same_reader(state['reader'],pub['pdf']) and run.same_reader(state['reader'],sponsor['paired_monograph'])
 assert {q['id']:q['status'] for q in view['proposal_gaps']}==dict(Q1='open',Q2='pass',Q3='pass',Q4='pass',Q5='open')
 prior={x['id']:x for x in read(PRIOR/'remaining-operations.json')['operations']};results=merged['execution_program']['results'];lanes=defaultdict(Counter);remaining=[]
 for node in graph['nodes']:
  if stages[node['id']]!='proposal_now':continue
  key=node['id'];result=results.get(key);outcome=result['outcome'] if result else 'open';lanes[node['lane']][outcome]+=1
  if outcome=='pass':continue
  old=prior.get(key,{})
  row=dict(id=key,lane=node['lane'],title=node['title'],status=outcome,action=old.get('action',node['action']),prerequisites=run.ledger.blockers(merged,node),outputs=node['outputs'],evidence=result,requires_inputs=node['requires_inputs'])
  for field in ['source_followup','corrected_source_followup','corrected_action_checkpoint']:
   if field in old:core.bound(ROOT,old[field]);row[field]=deepcopy(old[field])
  notes=merged['execution_program']['progress'].get(key,[])
  if notes:
   core.bound(ROOT,notes[-1]);note=read(ROOT/notes[-1]['path']);run.validate_note(ROOT,note,'progress');row.update(action=note['next_action'],action_checkpoint=notes[-1])
  remaining.append(row)
 assert len(remaining)+sum(x['pass'] for x in lanes.values())==view['proposal_operations']==376
 assert results['SW.DECISION.inherited_scope_rl']['outcome']=='pass'
 groups={}
 for group,prefix,total in [('software','SW.CELL.',102),('reuse','SW.DECISION.',115),('chapters','TEXT.REVIEW.',22)]:
  selected=[v for k,v in results.items() if k.startswith(prefix)];groups[group]=dict(Counter(v['outcome'] for v in selected),open=total-len(selected),total=total)
 assert groups['reuse']['pass']==43 and groups['reuse']['open']==69
 census=read(CENSUS/'census-register.json');counts=Counter(x['disposition'] for x in census['items']);assert counts['inspected_primary_retained_with_limits']==70 and counts['open_original_not_inspected']==43
 assert len(read(PUB/'reader/source-audit.json')['sources'])==994 and len(read(SPONSOR/'source-audit.json')['sources'])==405
 delta=read(PUB/'release-source-review.json')['checks'];by_id={x['id']:x for x in remaining};independent=[]
 for lane in ['software','commercial','reuse','llm','manuscript','release','proposal_acceptance']:
  selected=[n for n in ready if n['lane']==lane]
  if selected:
   n=selected[0];independent.append(dict(lane=lane,operation=n['id'],action=by_id[n['id']]['action'],depends=n['depends'],requires_inputs=n['requires_inputs']))
 BASE.mkdir();write(BASE/'state-snapshot.json',state);write(BASE/'status-snapshot.json',view)
 write(BASE/'remaining-operations.json',dict(reader=state['reader'],recorded=view['recorded_proposal_operations'],proposal_operations=376,ready=view['ready_proposal_operations'],coverage=groups,operations=remaining,census=ref(CENSUS/'census-register.json','70/43 unchanged dispositions'),proposal_accepted=False))
 evidence=[ref(PUB/'working-release.json','Current reader'),ref(SPONSOR/'working-release.json','Exact paired sponsor'),ref(PRIOR/'program-review.json','Prior full reconciliation'),ref(BASE/'remaining-operations.json','Every nonpassing obligation'),ref(SOURCE/'review.json','SCOPE-RL source review'),ref(SOURCE/'operation-receipt.json','Reference-only closure'),ref(SOURCE/'omissions-register.json','Native and scientific follow-ups'),ref(Path(__file__),'Reconciliation logic')]
 review=dict(status='pass_for_consistency_not_completion',reviewer=dict(name='Codex author/coordinator',kind='author'),evidence=evidence,effective_lane_counts={k:dict(v) for k,v in lanes.items()},findings=['All 376 proposal obligations accounted for; inconclusive remains nonpassing.',f'Exact reader: {pub["pages"]} pages, 994 citations and 232 genuine scholarly PDFs; sponsor: {sponsor["pages"]} pages, 405 citations.',f'All {delta["preserved_citation_records"]} predecessor source records/contexts and {delta["unchanged_compiled_inputs"]} compiled inputs preserved.','SCOPE-RL is reference-only. Time/interval/selection findings require reviewed repairs and actual native qualification.','Census remains 70/43 plus four crosscutting obligations.','Q2-Q4 pass for exact bytes; Q1/Q5, mandatory coverage/depth and visual/final acceptance remain open.'],independent_next_actions=independent,global_blocker=None,phase_boundaries_are_stopping_points=False,background_worker_running=False)
 verify_bindings(review);write(BASE/'program-review.json',review)
 write(BASE/'continuation-checkpoint.json',dict(reader=state['reader'],sponsor=sponsor['pdf'],prior_git_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),remaining=ref(BASE/'remaining-operations.json','Complete current actions'),independent_next_actions=independent,next_action=view['next_action'],proposal_accepted=False,visual_acceptance=False,global_blocker=None,background_worker_running=False))
 current=ROOT/'docs/program/execution/current-program.md';(BASE/'prior-current-program.md').write_bytes(current.read_bytes())
 rows='\n'.join(f"| {k} | {v.get('pass',0)} | {v.get('inconclusive',0)} | {v['open']} | {v['total']} |" for k,v in groups.items())
 current.write_text(f'''# Current executable proposal program

Updated 23 October 2026 after crash recovery, controlled-write publication and the SCOPE-RL reuse decision.
The [complete queue review](2026-10-23/program-refresh-scope-rl-reuse-v1/program-review.json)
and [remaining-operation register](2026-10-23/program-refresh-scope-rl-reuse-v1/remaining-operations.json)
account for all 376 proposal obligations. Canonical state and reviewed receipts govern execution.
Older numbered programs and publication pairs remain historical evidence.

This is a research/product proposal using public/generated evidence to justify later costly experiments.
Proposal completion is distinct from implemented capability, independent acceptance, bank validation and adoption.
Use python3 tools/run_program_checkpoint_v3.py status, next and check. Continue eligible branches across phase boundaries.
No unattended research worker runs; the active agent performs the work.

## Current integrated documents

The [current monograph](../../{Path(state['reader']['path']).name}) has {pub['pages']:,} pages,
994 audited citations and 232 genuine scholarly PDFs. The exact paired
[sponsor proposal](../../{Path(sponsor['pdf']['path']).name}) has {sponsor['pages']} pages and 405 citations.
All {delta['preserved_citation_records']} immediate-predecessor source records/contexts and
{delta['unchanged_compiled_inputs']} compiled content inputs survive unchanged.
All-page text bounds and source traceability pass. Q2-Q4 pass for these reader bytes;
Q1/Q5, mandatory coverage/depth rollups and visual/final acceptance remain open.

**{view['recorded_proposal_operations']} recorded outcomes of 376; {view['ready_proposal_operations']} ready; {len(remaining)} nonpassing obligations.**
Recorded outcomes include inconclusive findings and scoped references; they do not establish native capability.

| Area | Pass | Inconclusive | Open | Total |
|---|---:|---:|---:|---:|
{rows}

## Recovered and completed work

Controlled-write source review, exact reader Q2-Q4 renewals and paired sponsor publication are complete.
Conditional source soundness, shared semantic error, unmatched historical baselines and selective costs remain explicit.
Census is 70 inspected / 43 unread of 113 originals, plus four crosscutting obligations. Candidate 165 has a genuine-source
acquisition gap; metadata is not technical evidence and does not block other work.

SCOPE-RL 0.2.1 has a reference-only reuse disposition from eleven authenticated immutable blobs. The selected
episode scores, zero-denominator/discount admission, same-row terminal-reward masking, fixed-score bootstrap,
interval-expression discrepancies, required on-policy benchmark arrays and lower-tail name/value pairing
are documented. Exact project witnesses give population value 5 versus sample TIS 3/PDIS 15/4;
terminal-clock margins -4/4 and bootstrap variances 9/2 versus 9/4. No downloaded code executes.
Full artifact/dependency custody, reviewed repairs, native adverse fixtures and scientific qualification remain open.

The [preserved previous program review](2026-10-23/program-refresh-controlled-writes-v1/program-review.json)
retains sensitivity, GIST, medflex and the wider software/agent/integration evidence. Seventeen comparison reviews,
four prospective language designs, fourteen LLM task reviews and twelve integration reviews remain scoped outcomes,
not executed native trials or blanket acceptance. Completed publications must not be repeated.

## Remaining gaps and routes

1. Complete 59 open and 40 inconclusive software cells with primary cutoff evidence and explicit limits.
   Commercial follow-ups include historical Dataiku bytes, SAS service delegates, Domino terminal schemas,
   Posit server/scheduler contracts, and separate rights/pricing questions.
2. Complete 69 open and three inconclusive reuse dispositions with concrete adopt/integrate/port/reference/reject
   reasoning, dependencies, costs and owners. Do not restart passed reference decisions to invent native approval.
3. Inspect 43 unread originals and four crosscutting obligations. Resolve inaccessible originals through genuine
   alternative copies or continue an available candidate; preserve omissions without absence claims.
4. Execute registered public/synthetic trials only where actual environment and evidence prerequisites exist.
   Source inspections and designs cannot stand in for native results.
5. Complete manuscript coverage/depth rollups and Q1/Q5. The inherited six-image allowance is exhausted;
   fresh visual review and final visual acceptance need a fresh allowance. This is a visual-only blocker.

No universal repair is promised for unrestricted latent identification, arbitrary persistent dependence,
hidden-state optimal-policy uncertainty or arbitrary learner remainders. Justified restrictions or extra information
are required. Bank truth, independent institutional acceptance, platform reliability and real costs remain later external work.

## Exact continuation

Next: {view['next']}. {view['next_action']}

Independent source/reuse and census work remains eligible. Serialize canonical mutations, consume running results,
keep output bounded, preserve failures and successors, and commit/push complete units. There is no global blocker.
''')
 controller.render(ROOT,state)
 print(json.dumps(dict(recorded=view['recorded_proposal_operations'],ready=view['ready_proposal_operations'],nonpassing=len(remaining),reader_pages=pub['pages'],sponsor_pages=sponsor['pages'])))
if __name__=='__main__':main()
