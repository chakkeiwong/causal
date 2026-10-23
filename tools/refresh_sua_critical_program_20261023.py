#!/usr/bin/env python3
"""Reconcile every proposal obligation after the longitudinal R publication pair."""
from collections import Counter,defaultdict
from copy import deepcopy
from pathlib import Path
import json,subprocess
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT;DAY=ROOT/'docs/program/execution/2026-10-23'
BASE=DAY/'program-refresh-sua-critical-v1';PRIOR=DAY/'program-refresh-longitudinal-r-v1'
PUB=DAY/'sua-critical-reader-v1';SPONSOR=DAY/'sponsor-sua-critical-v1';SOURCE=DAY/'census-sensitivity-alignment-v1'
CENSUS=DAY/'census-sensitivity-alignment-v1'
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
 assert results['SW.CELL.longitudinal_survival.R']['outcome']=='inconclusive'
 groups={}
 for group,prefix,total in [('software','SW.CELL.',102),('reuse','SW.DECISION.',115),('chapters','TEXT.REVIEW.',22)]:
  selected=[v for k,v in results.items() if k.startswith(prefix)];groups[group]=dict(Counter(v['outcome'] for v in selected),open=total-len(selected),total=total)
 assert groups['reuse']['pass']==49 and groups['reuse']['open']==63
 census=read(CENSUS/'census-register.json');counts=Counter(x['disposition'] for x in census['items']);assert counts['inspected_primary_retained_with_limits']==71 and counts['open_original_not_inspected']==42
 assert len(read(PUB/'reader/source-audit.json')['sources'])==1015 and len(read(SPONSOR/'source-audit.json')['sources'])==444
 delta=read(PUB/'release-source-review.json')['checks'];by_id={x['id']:x for x in remaining};independent=[]
 for lane in ['software','commercial','reuse','llm','manuscript','release','proposal_acceptance']:
  selected=[n for n in ready if n['lane']==lane]
  if selected:
   n=selected[0];independent.append(dict(lane=lane,operation=n['id'],action=by_id[n['id']]['action'],depends=n['depends'],requires_inputs=n['requires_inputs']))
 BASE.mkdir();write(BASE/'state-snapshot.json',state);write(BASE/'status-snapshot.json',view)
 write(BASE/'remaining-operations.json',dict(reader=state['reader'],recorded=view['recorded_proposal_operations'],proposal_operations=376,ready=view['ready_proposal_operations'],coverage=groups,operations=remaining,census=ref(CENSUS/'census-register.json','71/42 preserving successor'),proposal_accepted=False))
 evidence=[ref(PUB/'working-release.json','Current reader'),ref(SPONSOR/'working-release.json','Exact paired sponsor'),ref(PRIOR/'program-review.json','Prior full reconciliation'),ref(BASE/'remaining-operations.json','Every nonpassing obligation'),ref(SOURCE/'review.json','Critical original and counterexample review'),ref(SOURCE/'progress.json','Partial census progress; no coverage closure'),ref(SOURCE/'omissions-register.json','Native and scientific follow-ups'),ref(Path(__file__),'Reconciliation logic')]
 review=dict(status='pass_for_consistency_not_completion',reviewer=dict(name='Codex author/coordinator',kind='author'),evidence=evidence,effective_lane_counts={k:dict(v) for k,v in lanes.items()},findings=['All 376 proposal obligations accounted for; inconclusive remains nonpassing.',f'Exact reader: {pub["pages"]} pages, 1,015 citations and 233 genuine scholarly PDFs; sponsor: {sponsor["pages"]} pages, 444 citations.',f'All {delta["preserved_citation_records"]} predecessor source records/contexts and {delta["unchanged_compiled_inputs"]} compiled inputs preserved.','Six R lineages are reconciled with eighteen authenticated blobs. Targets/events, stopping/warnings and dependence remain explicit; coverage stays inconclusive with141 unreturned search records and named primary-source follow-ups.','Census advances71/42; only candidate261 changes; four crosscutting obligations remain.','Q2-Q4 pass for exact bytes; Q1/Q5, mandatory coverage/depth and visual/final acceptance remain open.'],independent_next_actions=independent,global_blocker=None,phase_boundaries_are_stopping_points=False,background_worker_running=False)
 verify_bindings(review);write(BASE/'program-review.json',review)
 write(BASE/'continuation-checkpoint.json',dict(reader=state['reader'],sponsor=sponsor['pdf'],prior_git_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),remaining=ref(BASE/'remaining-operations.json','Complete current actions'),independent_next_actions=independent,next_action=view['next_action'],proposal_accepted=False,visual_acceptance=False,global_blocker=None,background_worker_running=False))
 current=ROOT/'docs/program/execution/current-program.md';(BASE/'prior-current-program.md').write_bytes(current.read_bytes())
 rows='\n'.join(f"| {k} | {v.get('pass',0)} | {v.get('inconclusive',0)} | {v['open']} | {v['total']} |" for k,v in groups.items())
 current.write_text(f"""# Current executable proposal program

Updated 24 October 2026 (Asia/Shanghai) after crash recovery, longitudinal R reconciliation and critical SUA review; source/release artifacts retain their23OctoberUTC work directories.
The [complete queue review](2026-10-23/program-refresh-sua-critical-v1/program-review.json)
and [remaining-operation register](2026-10-23/program-refresh-sua-critical-v1/remaining-operations.json)
account for all 376 proposal obligations. Canonical state and reviewed receipts govern execution.
The [preserved previous program](2026-10-23/program-refresh-sua-critical-v1/prior-current-program.md)
retains earlier workflow, Polars, probabilistic-model, software, agent and integration findings.

This is a research/product proposal supported by public/generated evidence before expensive bank experiments.
Proposal completion is distinct from implemented capability, independent acceptance, bank validation and adoption.
Use python3 tools/run_program_checkpoint_v3.py status, next and check. Continue eligible branches across boundaries.
No unattended research worker runs; the active agent performs the work.

## Current integrated documents

The [current monograph](../../{Path(state['reader']['path']).name}) has {pub['pages']:,} pages,
1,015 audited citation records and 233 genuine scholarly PDFs. The exact paired
[sponsor proposal](../../{Path(sponsor['pdf']['path']).name}) has {sponsor['pages']} pages and 444 citations.
All {delta['preserved_citation_records']} predecessor records/contexts and
{delta['unchanged_compiled_inputs']} compiled content inputs are preserved.
Source traceability, exact arithmetic and all-page text bounds pass. Q2-Q4 pass for these exact bytes.
Q1/Q5, mandatory coverage/depth and visual/final acceptance remain open.

**{view['recorded_proposal_operations']} recorded outcomes of376; {view['ready_proposal_operations']} ready;
{len(remaining)} nonpassing obligations.** Inconclusive and reference-only outcomes are not native qualification.

| Area | Pass | Inconclusive | Open | Total |
|---|---:|---:|---:|---:|
{rows}

## Latest completed review

The genuine24-page Sensitivity Uncertainty Alignment original is inspected with adverse findings.
Explicit admissible examples refute its stated generic risk bounds: a constant fair model would have
risk1/2 bounded by1/2-log2, and a constant bounded-loss example contradicts the earlier bound.
Expected perturbation sensitivity cannot replace a supremum upper bound; selected risk must retain
its conditional denominator. Equal entropy and stability do not certify causal truth. Reported empirical
tables lack the exact experiment identities needed for independent replay. The score remains a prospective
diagnostic candidate. One paper and exact authored witnesses add two audited records; no native execution.

The R longitudinal/survival cell reconciles grf, lmtp, ltmle, gfoRmula, stremr and survtmle.
Eighteen authenticated primary blobs support stremr0.4 and survtmle1.1.1 source contracts.
Baseline and repeated actions, competing-event and elimination targets, effective weights,
inner/outer convergence, residual timing, single-column paths and dependence units remain separate.
Authored examples give default risks3/20 versus19/100, stipulated insurance margins-200 versus200USD,
and true branch variance2 versus subject1 and visit1/2 independence references. No upstream code executes.

Coverage remains inconclusive: the saved search counted151 records and returned10. The141 unreturned
records, continuous-time concrete lead, lmtp survival/ife and grf survival primary reviews remain explicit.
Native trigger cases, complete rights, locked dependencies and matched costs are later qualification work.
The source draft suffered escaped-text corruption before compilation; the failed draft and receipts are
preserved. A reviewed v2 manuscript repairs the text. No corrupted PDF was published or accepted.

Census now has71 inspected/42 unread originals plus four crosscutting obligations. Q1/Q5 and coverage
rollups cannot pass while their required evidence remains unresolved. The inherited six-image allowance
is exhausted; fresh visual acceptance is a local blocker only. Public source work remains eligible.

## Remaining gaps and routes

1. Resolve58 open and41 inconclusive software cells through cutoff primary evidence and explicit limits.
   Longitudinal follow-ups are above; commercial follow-ups retain historical Dataiku bytes, SAS server
   contracts, Domino terminal/error schemas and Posit backend/profile contracts.
2. Resolve63 open and3 inconclusive reuse decisions with exact adopt/integrate/port/reference/reject reasons,
   dependencies, owners, costs and triggers. Do not reopen passed reference choices to invent native capability.
3. Inspect42 unread originals and four crosscutting census obligations; preserve inaccessible-source omissions.
4. Register and execute public/generated native trials only when actual environments and preregistration exist.
5. Complete mandatory manuscript coverage/depth, Q1/Q5 and fresh visual review. No blanket completion claim.

Unrestricted latent identification, arbitrary persistence and hidden-state optimal-policy uncertainty have no
promised universal repair. Justified restrictions or additional information are necessary. Authentic bank truth,
independent institutional acceptance, platform reliability and real costs remain later external work.

## Exact continuation

Next: {view['next']}. {view['next_action']}

Serialize canonical mutations, consume exits, keep tool outputs bounded, preserve failed attempts and successors,
and commit/push completed units. Independent items do not block each other. There is no global blocker.
""")
 controller.render(ROOT,state)
 print(json.dumps(dict(recorded=view['recorded_proposal_operations'],ready=view['ready_proposal_operations'],nonpassing=len(remaining),reader_pages=pub['pages'],sponsor_pages=sponsor['pages'])))
if __name__=='__main__':main()
