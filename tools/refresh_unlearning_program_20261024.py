#!/usr/bin/env python3
"""Reconcile all proposal obligations after the paired workflow-contract release."""
from collections import Counter,defaultdict
from copy import deepcopy
from pathlib import Path
import json,subprocess
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-24/program-refresh-unlearning-v1'
PRIOR=ROOT/'docs/program/execution/2026-10-24/program-refresh-workflow-contracts-v2'
PUB=ROOT/'docs/program/execution/2026-10-24/unlearning-reader-v2'
SPONSOR=ROOT/'docs/program/execution/2026-10-24/sponsor-unlearning-v1'
SOURCE=ROOT/'docs/program/execution/2026-10-24/census-agent-unlearning-v1'
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
        if key=='SW.CELL.longitudinal_survival.Python':
            row['action']=read(ROOT/node['outputs'][0])['next_action']
        remaining.append(row)
    assert len(remaining)+sum(x['pass'] for x in lanes.values())==view['proposal_operations']==376
    groups={}
    for group,prefix,total in [('software','SW.CELL.',102),('reuse','SW.DECISION.',115),('chapters','TEXT.REVIEW.',22)]:
        selected=[v for k,v in results.items() if k.startswith(prefix)];groups[group]=dict(Counter(v['outcome'] for v in selected),open=total-len(selected),total=total)
    assert groups['software']['pass']==3 and groups['software']['inconclusive']==43 and groups['software']['open']==56
    assert groups['reuse']['pass']==56 and groups['reuse']['inconclusive']==3 and groups['reuse']['open']==56
    assert view['recorded_proposal_operations']==240 and view['ready_proposal_operations']==len(ready) and len(remaining)==203
    census=read(CENSUS/'census-register.json');counts=Counter(x['disposition'] for x in census['items']);assert counts['inspected_primary_retained_with_limits']==74 and counts['open_original_not_inspected']==39
    assert len(read(PUB/'reader/source-audit.json')['sources'])==1034 and len(read(SPONSOR/'source-audit.json')['sources'])==477
    delta=read(PUB/'release-source-review.json')['checks'];by_id={x['id']:x for x in remaining};independent=[]
    for lane in ['software','commercial','reuse','llm','manuscript','release','proposal_acceptance']:
        selected=[n for n in ready if n['lane']==lane]
        if selected:
            n=selected[0];independent.append(dict(lane=lane,operation=n['id'],action=by_id[n['id']]['action'],depends=n['depends'],requires_inputs=n['requires_inputs']))
    BASE.mkdir();write(BASE/'state-snapshot.json',state);write(BASE/'status-snapshot.json',view)
    write(BASE/'remaining-operations.json',dict(reader=state['reader'],recorded=240,proposal_operations=376,ready=view['ready_proposal_operations'],coverage=groups,operations=remaining,census=ref(CENSUS/'census-register.json','74/39 preserved census'),proposal_accepted=False))
    evidence=[ref(PUB/'working-release.json','Current reader'),ref(SPONSOR/'working-release.json','Exact paired sponsor'),ref(PRIOR/'program-review.json','Previous full reconciliation'),ref(BASE/'remaining-operations.json','Every nonpassing obligation'),ref(SOURCE/'review.json','Bounded original and software review'),ref(SOURCE/'source-audit.json','Primary identities and anchors'),ref(SOURCE/'omissions-register.json','Remaining source/qualification questions'),ref(SOURCE/'census-register.json','Only candidate181 advances'),ref(Path(__file__),'Complete reconciliation')]
    review=dict(status='pass_for_consistency_not_completion',reviewer=dict(name='Codex author/coordinator',kind='author'),evidence=evidence,effective_lane_counts={k:dict(v) for k,v in lanes.items()},findings=['All376 proposal obligations reconciled;240 recorded and203 nonpassing remain; census progress is not a fabricated new operation closure.',f'Exact reader{pub["pages"]}pages/1034citations/236scholarly PDFs; sponsor{sponsor["pages"]}pages/477citations.',f'All1031 predecessor records/contexts and{delta["unchanged_compiled_inputs"]}compiled inputs preserved.','K-Bench review adds original,20inspected software source blobs and exact authored witnesses;25blobs authenticated.','Scorer, data-provenance and dependency contradictions remain explicit; no downloaded code or native model executed.','Q2-Q4 pass for exact bytes; Q1/Q5, mandatory repairs and visual/final acceptance remain open.'],independent_next_actions=independent,global_blocker=None,phase_boundaries_are_stopping_points=False,background_worker_running=False)
    verify_bindings(review);write(BASE/'program-review.json',review)
    write(BASE/'continuation-checkpoint.json',dict(reader=state['reader'],sponsor=sponsor['pdf'],prior_git_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),remaining=ref(BASE/'remaining-operations.json','Complete actions'),independent_next_actions=independent,next_action=view['next_action'],proposal_accepted=False,visual_acceptance=False,global_blocker=None,background_worker_running=False))
    current=ROOT/'docs/program/execution/current-program.md';(BASE/'prior-current-program.md').write_bytes(current.read_bytes())
    rows='\n'.join(f"| {k} | {v.get('pass',0)} | {v.get('inconclusive',0)} | {v['open']} | {v['total']} |" for k,v in groups.items())
    current.write_text(f"""# Current executable proposal program

Updated 24 October 2026 (Asia/Shanghai). The [full program review](2026-10-24/program-refresh-unlearning-v1/program-review.json)
and [remaining-operation register](2026-10-24/program-refresh-unlearning-v1/remaining-operations.json)
account for all 376 proposal obligations. Canonical state and reviewed receipts govern execution.
The [preserved previous program](2026-10-24/program-refresh-unlearning-v1/prior-current-program.md)
retains the complete longitudinal, panel, software, agent, integration and census history.

This is a research/product proposal supported by public and generated evidence before expensive bank experiments.
Proposal completion is distinct from product implementation, independent acceptance, bank validation and adoption.
Use python3 tools/run_program_checkpoint_v3.py status, next and check. Continue eligible independent branches across phases.
No unattended research worker runs; the active agent performs work.

## Current integrated documents

The [monograph](../../{Path(state['reader']['path']).name}) has {pub['pages']:,} pages,
1,034 audited citation records and236 genuine scholarly PDFs. The exact paired
[sponsor proposal](../../{Path(sponsor['pdf']['path']).name}) has{sponsor['pages']}pages and477citations.
All1,031 predecessor records/contexts and{delta['unchanged_compiled_inputs']}compiled content inputs survive.
Source traceability, exact authored examples and all-page extracted text/bounds pass. Q2-Q4 pass for exact bytes.
Q1/Q5, mandatory coverage/depth and fresh visual/final acceptance remain open.

**240 recorded outcomes of376; {view['ready_proposal_operations']} ready;203 nonpassing obligations.**
Census review advances within its existing operation; it does not inflate completed-operation counts.

| Area | Pass | Inconclusive | Open | Total |
|---|---:|---:|---:|---:|
{rows}

## Completed agent-unlearning review

Candidate181 K-Bench is inspected from its genuine52-page v2 original and cutoff repository.
Twenty of25authenticated source blobs support selected inspected claims; no downloaded code or upstream test executes.
Binary disclosure, graded severity, retention, protocol health and eligibility remain distinct.
The printed twofold reduction condition disagrees with a visible public classifier branch; the signed retain equation
differs from its absolute-value prose. Real-data wording conflicts with synthetic-only wording and converter descriptions.
Exact dataset and run identities are required; no empirical number is silently corrected and no misconduct is alleged.
The CLI enforces within-seed cohort equality and separate terminal gates, while the standalone verdict path is weaker.
Seed-pooled tests and approximate topology intervals still require a justified dependence model.

Authored finite witnesses distinguish single-channel detection from joint reconstruction, queried from corpus-wide
entities, conditional denominators, positive scalar from failed terminal eligibility, and local fingerprint from weight bytes.
A stipulated200USD wrong-action cost gives100USD expected loss from either fair XOR share and0from both;
200independent outcomes repeated three times give variance1/800, not1/2400. These are examples, not bank results.
A conditional original-Python worker with typed CLI/MCP transcripts remains prospective. Rights, complete environments,
scorer reconciliation, actual costs and registered native conformance are open.

Census is now74inspected/39unread of113, plus four crosscutting obligations.
The earlier commercial-workflow review and its SAS/Dataiku/Domino/Posit source limits remain fully integrated.
One preparation mislabeled the prior citation count before building; preserved v2 corrects it.
A publication attempt was correctly rejected while census remained active; explicit controller yield resolved it.
No invalid PDF or final acceptance was published.

## Remaining gaps and routes

1. Software:56open/43inconclusive cells; inspect cutoff primary originals and resolve each candidate's scope and source tails.
2. Reuse:56open/3inconclusive decisions; complete adopt/integrate/port/reference/reject arguments with rights, owners and costs.
3. Census:39unread originals and four crosscutting searches; preserve inaccessible sources and unresolved contradictions.
4. Public prototype evidence: preregister exact environments, truth, sampling, failure, cost and acceptance contracts before execution.
5. Manuscript: complete mandatory coverage/depth, Q1/Q5 and fresh visual review. Total pages do not prove completeness.

Unrestricted latent identification, arbitrary persistence and hidden-state policy uncertainty have no promised universal
repair. Justified restrictions or additional information are necessary. Bank truth, independent review, platform acceptance
and actual economic value remain later external work, not global blockers for the proposal.

## Exact continuation

Next: {view['next']}. {view['next_action']}

Serialize canonical mutations, consume command exits, preserve source/failure evidence and keep outputs bounded.
Independent obligations do not block one another. There is no global blocker. Commit and push completed units.
""")
    controller.render(ROOT,state);print(json.dumps(dict(recorded=240,ready=view['ready_proposal_operations'],nonpassing=203,reader_pages=pub['pages'],sponsor_pages=sponsor['pages'],next=view['next'])))
if __name__=='__main__':main()
