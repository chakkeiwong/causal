#!/usr/bin/env python3
"""Reconcile all obligations against exact current publications and latest continuation."""
from collections import Counter,defaultdict
from copy import deepcopy
from pathlib import Path
import json,re,subprocess
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT;DAY=ROOT/'docs/program/execution/2026-10-23'
BASE=DAY/'program-refresh-controlled-writes-v1';PRIOR=DAY/'program-refresh-medflex-reuse-v1'
PUB=DAY/'controlled-writes-reader-v1';SPONSOR=DAY/'sponsor-controlled-writes-v1';SOURCE=DAY/'census-controlled-writes-v1'
read=lambda p:json.loads(p.read_text())
def main():
 assert not BASE.exists()
 state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active'] is None
 view=controller.status(ROOT,state);graph,merged,stages,ready,_=run.queue(ROOT,state)
 pub=read(PUB/'working-release.json');sponsor=read(SPONSOR/'working-release.json')
 for data in [pub,sponsor,read(PRIOR/'program-review.json'),read(SOURCE/'review.json')]:verify_bindings(data)
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
 groups={}
 for group,prefix,total in [('software','SW.CELL.',102),('reuse','SW.DECISION.',115),('chapters','TEXT.REVIEW.',22)]:
  selected=[v for k,v in results.items() if k.startswith(prefix)];groups[group]=dict(Counter(v['outcome'] for v in selected),open=total-len(selected),total=total)
 census=read(SOURCE/'census-register.json');counts=Counter(x['disposition'] for x in census['items']);assert counts['inspected_primary_retained_with_limits']==70 and counts['open_original_not_inspected']==43
 reader_audit=read(PUB/'reader/source-audit.json');sponsor_audit=read(SPONSOR/'source-audit.json');delta=read(PUB/'release-source-review.json')['checks']
 assert len(reader_audit['sources'])==992 and len(sponsor_audit['sources'])==401
 by_id={x['id']:x for x in remaining};independent=[]
 for lane in ['software','commercial','reuse','llm','manuscript','release','proposal_acceptance']:
  selected=[n for n in ready if n['lane']==lane]
  if selected:
   n=selected[0];independent.append(dict(lane=lane,operation=n['id'],action=by_id[n['id']]['action'],depends=n['depends'],requires_inputs=n['requires_inputs']))
 BASE.mkdir();write(BASE/'state-snapshot.json',state);write(BASE/'status-snapshot.json',view)
 write(BASE/'remaining-operations.json',dict(reader=state['reader'],recorded=view['recorded_proposal_operations'],proposal_operations=376,ready=view['ready_proposal_operations'],coverage=groups,operations=remaining,census=ref(SOURCE/'census-register.json','70/43 candidate dispositions'),proposal_accepted=False))
 evidence=[ref(PUB/'working-release.json','Current reader'),ref(SPONSOR/'working-release.json','Exact paired sponsor'),ref(PRIOR/'program-review.json','Preserved previous reconciliation'),ref(BASE/'remaining-operations.json','Every nonpassing obligation'),ref(SOURCE/'review.json','Scoped source review'),ref(SOURCE/'integrated-progress.json','Latest exact continuation'),ref(DAY/'census-scientific-method-v1/identity-followup.json','Actual source-specific acquisition gap'),ref(Path(__file__),'Reconciliation logic')]
 review=dict(status='pass_for_consistency_not_completion',reviewer=dict(name='Codex author/coordinator',kind='author'),evidence=evidence,effective_lane_counts={k:dict(v) for k,v in lanes.items()},findings=['All376 proposal obligations accounted for; inconclusive remains nonpassing.',f'Exact reader has{pub["pages"]}pages/992citations/232genuine scholarly PDFs; sponsor has{sponsor["pages"]}pages/401citations.',f'All{delta["preserved_citation_records"]} predecessor source records/contexts and{delta["unchanged_compiled_inputs"]} compiled content inputs preserved.','Candidate130 reviewed with conditional soundness, unmatched historical comparator and raw-provenance limits. Census70/43 plus four crosscutting obligations.','Candidate165 publisher route failed; metadata establishes identity only. This does not block other ready work.','Q2-Q4 pass for exact bytes; Q1/Q5, mandatory depth/coverage rollups and visual/final acceptance remain open.'],independent_next_actions=independent,global_blocker=None,phase_boundaries_are_stopping_points=False,background_worker_running=False)
 verify_bindings(review);write(BASE/'program-review.json',review)
 write(BASE/'continuation-checkpoint.json',dict(reader=state['reader'],sponsor=sponsor['pdf'],prior_git_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),remaining=ref(BASE/'remaining-operations.json','Current exact remaining actions'),independent_next_actions=independent,next_action=view['next_action'],visual_acceptance=False,proposal_accepted=False,global_blocker=None,background_worker_running=False))
 current=ROOT/'docs/program/execution/current-program.md';(BASE/'prior-current-program.md').write_bytes(current.read_bytes())
 rows='\n'.join(f"| {k} | {v.get('pass',0)} | {v.get('inconclusive',0)} | {v['open']} | {v['total']} |" for k,v in groups.items())
 current.write_text(f'''# Current executable proposal program

Updated23 October2026 after crash recovery and the controlled-write census review.
The [complete queue review](2026-10-23/program-refresh-controlled-writes-v1/program-review.json)
and [remaining-operation register](2026-10-23/program-refresh-controlled-writes-v1/remaining-operations.json)
account for all376 proposal obligations. Canonical state and reviewed receipts govern execution;
older numbered programs and publication pairs remain preserved evidence.

This is a research/product proposal using public/generated evidence to justify later costly experiments.
A completed proposal is distinct from implemented capability, independent acceptance, authentic bank validation and adoption.
Use python3 tools/run_program_checkpoint_v3.py status, next and check. Continue eligible branches across phase boundaries.
No unattended research worker runs; the active agent performs the work.

## Current integrated documents

The current [monograph](../../{Path(state['reader']['path']).name}) has{pub['pages']:,} pages,992 audited citations and232 genuine scholarly PDFs.
The exact paired [sponsor proposal](../../{Path(sponsor['pdf']['path']).name}) has{sponsor['pages']} pages and401 audited citations.
All{delta['preserved_citation_records']} immediate-predecessor source records and citation contexts, plus{delta['unchanged_compiled_inputs']} compiled content inputs, survive unchanged.
All-page text bounds and source traceability pass. Exact-reader Q2-Q4 pass; Q1/Q5 and visual/final acceptance remain open.

**{view['recorded_proposal_operations']} recorded outcomes of376; {view['ready_proposal_operations']} ready; {len(remaining)} nonpassing obligations.**
Recorded includes inconclusive results and scoped reference dispositions; it does not establish native capability.

| Area | Pass | Inconclusive | Open | Total |
|---|---:|---:|---:|---:|
{rows}

## Recovered work and substantive additions

The sensitivity decisions retain sensemakr/EValue as source-qualified references with covariance, conversion,
domain and dependency limits. The GIST audit repair replaces malformed unpublished metadata through a
validated successor without rewriting the failed attempt. Its goal-contract design is distinct from causal
identification; source-to-output schema discrepancies prevent direct replay claims.

Medflex0.6-11 has a recorded reference-only reuse decision from ten authenticated artifacts. Original-subject
expansion, complete bootstrap refitting and nuisance-score covariance remain requirements. Documentation
class reversals, global-environment call bindings and warning suppression are explicit native-test prerequisites.
Independent exact examples illustrate target and uncertainty differences, not observed package performance.

CPUNeSy candidate130 adds one authentic37-page original, controlled-write architecture and a prospective
banking protocol. Sound derivations remain conditional on admitted premises and sound source checking.
Restricted writes do not prevent false permitted leaves; agreement does not eliminate shared semantic error.
The main-table historical adapter rows are unmatched according to the appendix, so no matched superiority
claim is accepted. Printed selective counts and stipulated costs reproduce; raw archive/model/certificate
custody and prospective calibration remain open. The2027 conference header is unverified self-description.

The original census is70 inspected and43 unread of113, plus four crosscutting obligations. Candidate165's
publisher returned challenge/non-PDF content. Crossref confirms its identity and5 August2025 date; no alternate
original was found in returned OpenAlex locations. It remains unread, with no technical citation or global blocker.

Seventeen individual comparison reviews, four prospective language trial designs, fourteen LLM task reviews
and twelve integration requirement reviews retain their scoped outcomes. Designs and source inspections are
not native trials. The prior program review preserves complete historical unit summaries and their evidence.

## Remaining gaps and execution routes

1. Complete59 open software coverage cells and40 inconclusive cells using primary cutoff sources and explicit
   applicability limits. Commercial follow-ups include Dataiku historical bytes, SAS service delegates,
   Domino terminal-state schemas and Posit server/scheduler contracts; rights and pricing remain separate.
2. Complete70 open and three inconclusive reuse dispositions, preserving adopt/integrate/port/reference/reject
   reasoning, dependencies, costs and owners. Reference acceptance never grants adapter qualification.
3. Inspect43 unread originals and finish four crosscutting obligations. Resolve candidate165 through a genuine
   author/repository copy or select another available source; do not repeat completed publications.
4. Execute registered public/synthetic native trials only when their actual environments and evidence prerequisites
   exist. Do not replace missing trial results with additional design documents.
5. Complete manuscript depth/coverage rollups and exact-document Q1/Q5. Preserve the substantive100-150-page
   software, approximately100-page agent and developed integration contracts without duplicate-credit padding.
6. Rendered visual acceptance needs a fresh image allowance under /home/ubuntu/AGENTS.md; the inherited six
   previews are exhausted. This affects visual sign-off only, not independent research.

Universal latent identification, arbitrary persistent dependence, hidden-state policy uncertainty and arbitrary
learner remainders require justified restrictions or extra information, not promised generic solutions.
Authentic bank truth, independent institutional acceptance, target-platform reliability and real bank costs
are later external work and are distinct from proposal completion.

## Exact continuation

Next: {view['next']}. {view['next_action']}

The newest census continuation is census-controlled-writes-v1/integrated-progress.json. The source-acquisition
omission and every remaining action are durable. Serialize canonical mutations, consume running results,
keep output bounded, preserve failures and commit/push complete units. No phase boundary is a permission stop.
''')
 controller.render(ROOT,state)
 print(json.dumps(dict(recorded=view['recorded_proposal_operations'],ready=view['ready_proposal_operations'],nonpassing=len(remaining),reader_pages=pub['pages'],sponsor_pages=sponsor['pages'],census='70/43')))
if __name__=='__main__':main()
