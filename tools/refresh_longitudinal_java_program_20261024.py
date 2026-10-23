#!/usr/bin/env python3
"""Reconcile every proposal obligation after the paired Java survival release."""
from collections import Counter,defaultdict
from copy import deepcopy
from pathlib import Path
import json,subprocess
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-24/program-refresh-longitudinal-java-v1'
PRIOR=ROOT/'docs/program/execution/2026-10-24/program-refresh-unlearning-v1'
PUB=ROOT/'docs/program/execution/2026-10-24/longitudinal-java-reader-v1'
SPONSOR=ROOT/'docs/program/execution/2026-10-24/sponsor-longitudinal-java-v1'
SOURCE=ROOT/'docs/program/execution/2026-10-24/longitudinal-java-v1'
CENSUS=ROOT/'docs/program/execution/2026-10-24/census-agent-unlearning-v1'
read=lambda p:json.loads(p.read_text())

def main():
    assert not BASE.exists();state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active'] is None
    view=controller.status(ROOT,state);graph,merged,stages,ready,_=run.queue(ROOT,state)
    pub,sponsor=read(PUB/'working-release.json'),read(SPONSOR/'working-release.json')
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
        if key=='SW.CELL.computation_workflow.commercial':
            row['action']=read(ROOT/node['outputs'][0])['next_action'];row.pop('action_checkpoint',None)
        if key in ['SW.CELL.longitudinal_survival.Python','SW.CELL.longitudinal_survival.Java']:
            row['action']=read(ROOT/node['outputs'][0])['next_action']
        remaining.append(row)
    assert len(remaining)+sum(x['pass'] for x in lanes.values())==view['proposal_operations']==376
    groups={}
    for group,prefix,total in [('software','SW.CELL.',102),('reuse','SW.DECISION.',115),('chapters','TEXT.REVIEW.',22)]:
        selected=[v for k,v in results.items() if k.startswith(prefix)];groups[group]=dict(Counter(v['outcome'] for v in selected),open=total-len(selected),total=total)
    assert groups['software']['pass']==3 and groups['software']['inconclusive']==44 and groups['software']['open']==55
    assert groups['reuse']['pass']==56 and groups['reuse']['inconclusive']==3 and groups['reuse']['open']==56
    assert view['recorded_proposal_operations']==241 and view['ready_proposal_operations']==len(ready) and len(remaining)==203
    census=read(CENSUS/'census-register.json');counts=Counter(x['disposition'] for x in census['items']);assert counts['inspected_primary_retained_with_limits']==74 and counts['open_original_not_inspected']==39
    assert len(read(PUB/'reader/source-audit.json')['sources'])==1039 and len(read(SPONSOR/'source-audit.json')['sources'])==484
    delta=read(PUB/'release-source-review.json')['checks'];by_id={x['id']:x for x in remaining};independent=[]
    for lane in ['software','commercial','reuse','llm','manuscript','release','proposal_acceptance']:
        selected=[n for n in ready if n['lane']==lane]
        if selected:
            n=selected[0];independent.append(dict(lane=lane,operation=n['id'],action=by_id[n['id']]['action'],depends=n['depends'],requires_inputs=n['requires_inputs']))
    BASE.mkdir();write(BASE/'state-snapshot.json',state);write(BASE/'status-snapshot.json',view)
    write(BASE/'remaining-operations.json',dict(reader=state['reader'],recorded=241,proposal_operations=376,ready=view['ready_proposal_operations'],coverage=groups,operations=remaining,census=ref(CENSUS/'census-register.json','74/39 preserved census'),proposal_accepted=False))
    evidence=[ref(PUB/'working-release.json','Current reader'),ref(SPONSOR/'working-release.json','Exact paired sponsor'),ref(PRIOR/'program-review.json','Previous full reconciliation'),ref(BASE/'remaining-operations.json','Every nonpassing obligation'),ref(SOURCE/'review.json','Bounded original and software review'),ref(SOURCE/'source-audit.json','Primary identities and anchors'),ref(SOURCE/'omissions-register.json','Remaining source/qualification questions'),ref(CENSUS/'census-register.json','Preserved74/39census'),ref(Path(__file__),'Complete reconciliation')]
    review=dict(status='pass_for_consistency_not_completion',reviewer=dict(name='Codex author/coordinator',kind='author'),evidence=evidence,effective_lane_counts={k:dict(v) for k,v in lanes.items()},findings=['All376 proposal obligations reconciled;241 recorded and203 nonpassing remain; census progress is not a fabricated new operation closure.',f'Exact reader{pub["pages"]}pages/1039citations/236scholarly PDFs; sponsor{sponsor["pages"]}pages/484citations.',f'All1034 predecessor records/contexts and{delta["unchanged_compiled_inputs"]}compiled inputs preserved.','Four Java survival profiles add39inspected source blobs and exact authored witnesses;42newblobs authenticated.','Weight, baseline, event, covariance, cleanup and secure-disclosure limits explicit; no upstream code executed.','Q2-Q4 pass for exact bytes; Q1/Q5, mandatory repairs and visual/final acceptance remain open.'],independent_next_actions=independent,global_blocker=None,phase_boundaries_are_stopping_points=False,background_worker_running=False)
    verify_bindings(review);write(BASE/'program-review.json',review)
    write(BASE/'continuation-checkpoint.json',dict(reader=state['reader'],sponsor=sponsor['pdf'],prior_git_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),remaining=ref(BASE/'remaining-operations.json','Complete actions'),independent_next_actions=independent,next_action=view['next_action'],proposal_accepted=False,visual_acceptance=False,global_blocker=None,background_worker_running=False))
    current=ROOT/'docs/program/execution/current-program.md';(BASE/'prior-current-program.md').write_bytes(current.read_bytes())
    rows='\n'.join(f"| {k} | {v.get('pass',0)} | {v.get('inconclusive',0)} | {v['open']} | {v['total']} |" for k,v in groups.items())
    current.write_text(f"""# Current executable proposal program

Updated 24 October 2026 (Asia/Shanghai). The [complete reconciliation](2026-10-24/program-refresh-longitudinal-java-v1/program-review.json)
and [remaining-operation register](2026-10-24/program-refresh-longitudinal-java-v1/remaining-operations.json)
account for all 376 proposal obligations. Canonical state and reviewed receipts govern execution.
The [preserved predecessor](2026-10-24/program-refresh-longitudinal-java-v1/prior-current-program.md)
retains earlier source, software, agent, integration and census findings.

This is a research/product proposal using public and authored evidence before expensive bank experiments.
Proposal completion is distinct from implementation, independent acceptance, bank validation and adoption.
Use python3 tools/run_program_checkpoint_v3.py status, next and check. Continue eligible independent branches across phases.
No unattended worker is running; the active agent performs the work.

## Current integrated documents

The [monograph](../../{Path(state['reader']['path']).name}) has {pub['pages']:,} pages,
1,039 audited citation records and 236 genuine scholarly PDFs. The exact paired
[sponsor proposal](../../{Path(sponsor['pdf']['path']).name}) has {sponsor['pages']} pages and 484 citations.
All 1,034 predecessor records, citation contexts and {delta['unchanged_compiled_inputs']} compiled content inputs survive.
Source traceability, exact authored examples and all-page text/bounds checks pass; Q2-Q4 pass for exact bytes.
Q1/Q5, mandatory coverage/depth and fresh visual/final acceptance remain open.

**241 recorded outcomes of 376; {view['ready_proposal_operations']} ready; 203 nonpassing obligations.**
Recorded outcomes include inconclusive findings, not fabricated capability closures.

| Area | Pass | Inconclusive | Open | Total |
|---|---:|---:|---:|---:|
{rows}

## Completed Java survival comparison

H2O-3, BioJava, FRESCO-stat and the distinct robbyjo/JLinAlg repository have pinned primary-source comparisons.
Thirty-nine source blobs support inspected claims; 42 new blobs authenticate against complete cutoff trees.
H2O's log score, named baseline paths, weighted likelihood and event mapping remain distinct contracts.
BioJava's strata conversion, exception-to-null helper and selected state-restoration/cluster-guard branches need qualification.
FRESCO's fixed-iteration optimizer and public tie partition require explicit numerical and disclosure contracts.
JLinAlg's robust diagnostics are separate from ordinary fit errors; its CLI is narrower than its Java APIs.
No upstream implementation, test, secure protocol or native backend was executed.

Authored exact witnesses distinguish delayed-entry increments 1/2 versus 1/3, Efron 5/6 versus Breslow 2/3,
weighted likelihood 1/4 versus 1/16, and row versus cluster variance 1/4 versus 1/2.
With relative score two, baseline survival 1/2 or 3/4 implies risks 3/4 or 7/16.
Stipulated USD 1,000 loss and USD 600 premium give margins -150 and 162.50 dollars; these are not bank results.
Conditional original workers, R/Python sequential-policy alternatives, owners, failures, rights and cost categories are explicit.
The Java cell records an inconclusive coverage outcome; bounded source review does not establish exhaustive coverage.

The preceding K-Bench and commercial workflow findings remain fully integrated.
Census remains 74 inspected and 39 unread originals of 113, plus four crosscutting obligations.
The recovered unlearning pair was committed and pushed through 141917b7 before this continuation.

## Remaining gaps and routes

1. Software: 55 open and 44 inconclusive cells. Resolve aliases and search tails, inspect primary delegates, and preserve candidate-specific target limits.
2. Reuse: 56 open and three inconclusive decisions. Complete explicit adopt/integrate/port/reference/reject choices with rights, owners, costs and triggers.
3. Frontier census: 39 unread originals and four crosscutting obligations. Candidate217 needs a permitted original route and cutoff-date verification; that is local.
4. Prototype qualification: justify and preregister generated/public-data trials with exact environments, truth, failure denominators, uncertainty and full costs.
5. Manuscript acceptance: reconcile all mandatory coverage/depth, Q1/Q5 and fresh visual review. Page count is not completion.

Unrestricted latent identification, arbitrary persistence and hidden-state policy uncertainty have no promised universal repair.
Additional information or justified restrictions are necessary. Authentic bank truth, independent review, platform acceptance
and actual economic value remain later external work, not global proposal blockers.

## Exact continuation

Next: {view['next']}. {view['next_action']}

Serialize canonical mutations and consume command exits. Preserve failures and exact source bytes.
Keep commands/output bounded. Independent obligations do not block one another. Commit and push completed units.
""")
    controller.render(ROOT,state);print(json.dumps(dict(recorded=241,ready=view['ready_proposal_operations'],nonpassing=203,reader_pages=pub['pages'],sponsor_pages=sponsor['pages'],next=view['next'])))
if __name__=='__main__':main()
