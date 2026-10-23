#!/usr/bin/env python3
"""Reconcile all proposal obligations after the paired workflow-contract release."""
from collections import Counter,defaultdict
from copy import deepcopy
from pathlib import Path
import json,subprocess
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-24/program-refresh-workflow-contracts-v1'
PRIOR=ROOT/'docs/program/execution/2026-10-24/program-refresh-longitudinal-python-v1'
PUB=ROOT/'docs/program/execution/2026-10-24/workflow-contracts-reader-v3'
SPONSOR=ROOT/'docs/program/execution/2026-10-24/sponsor-workflow-contracts-v1'
SOURCE=ROOT/'docs/program/execution/2026-10-24/workflow-contracts-v3'
CENSUS=ROOT/'docs/program/execution/2026-10-24/census-language-collaboration-v1'
read=lambda p:json.loads(p.read_text())

def main():
    assert not BASE.exists();state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active'] is None
    view=controller.status(ROOT,state);graph,merged,stages,ready,_=run.queue(ROOT,state)
    pub,sponsor=read(PUB/'working-release.json'),read(SPONSOR/'working-release.json')
    for d in [pub,sponsor,read(PRIOR/'program-review.json'),read(SOURCE/'review-v2.json')]:verify_bindings(d)
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
            row['action']=read(ROOT/node['outputs'][0])['next_action'];row['source_followup']=ref(SOURCE/'omissions-register.json','Current vendor-specific follow-ups');row.pop('action_checkpoint',None)
        if key=='SW.CELL.longitudinal_survival.Python':
            row['action']=read(ROOT/node['outputs'][0])['next_action']
        remaining.append(row)
    assert len(remaining)+sum(x['pass'] for x in lanes.values())==view['proposal_operations']==376
    groups={}
    for group,prefix,total in [('software','SW.CELL.',102),('reuse','SW.DECISION.',115),('chapters','TEXT.REVIEW.',22)]:
        selected=[v for k,v in results.items() if k.startswith(prefix)];groups[group]=dict(Counter(v['outcome'] for v in selected),open=total-len(selected),total=total)
    assert groups['software']['pass']==3 and groups['software']['inconclusive']==43 and groups['software']['open']==56
    assert groups['reuse']['pass']==56 and groups['reuse']['inconclusive']==3 and groups['reuse']['open']==56
    assert view['recorded_proposal_operations']==240 and view['ready_proposal_operations']==112 and len(remaining)==203
    census=read(CENSUS/'census-register.json');counts=Counter(x['disposition'] for x in census['items']);assert counts['inspected_primary_retained_with_limits']==73 and counts['open_original_not_inspected']==40
    assert len(read(PUB/'reader/source-audit.json')['sources'])==1031 and len(read(SPONSOR/'source-audit.json')['sources'])==472
    delta=read(PUB/'release-source-review.json')['checks'];by_id={x['id']:x for x in remaining};independent=[]
    for lane in ['software','commercial','reuse','llm','manuscript','release','proposal_acceptance']:
        selected=[n for n in ready if n['lane']==lane]
        if selected:
            n=selected[0];independent.append(dict(lane=lane,operation=n['id'],action=by_id[n['id']]['action'],depends=n['depends'],requires_inputs=n['requires_inputs']))
    BASE.mkdir();write(BASE/'state-snapshot.json',state);write(BASE/'status-snapshot.json',view)
    write(BASE/'remaining-operations.json',dict(reader=state['reader'],recorded=240,proposal_operations=376,ready=112,coverage=groups,operations=remaining,census=ref(CENSUS/'census-register.json','73/40 preserved census'),proposal_accepted=False))
    evidence=[ref(PUB/'working-release.json','Current reader'),ref(SPONSOR/'working-release.json','Exact paired sponsor'),ref(PRIOR/'program-review.json','Previous full reconciliation'),ref(BASE/'remaining-operations.json','Every nonpassing obligation'),ref(SOURCE/'review-v2.json','Bounded vendor review'),ref(SOURCE/'operation-receipt.json','Inconclusive coverage'),ref(SOURCE/'source-audit-qualified.json','Primary identities and anchors'),ref(SOURCE/'omissions-register.json','Remaining vendor contracts'),ref(ROOT/'docs/program/execution/2026-10-24/workflow-contracts-v5/review-v2.json','Preserved layout repairs'),ref(Path(__file__),'Complete reconciliation')]
    review=dict(status='pass_for_consistency_not_completion',reviewer=dict(name='Codex author/coordinator',kind='author'),evidence=evidence,effective_lane_counts={k:dict(v) for k,v in lanes.items()},findings=['All376 proposal obligations reconciled; recorded inconclusive remains nonpassing.',f'Exact reader{pub["pages"]}pages/1031citations/235scholarly PDFs; sponsor{sponsor["pages"]}pages/472citations.',f'All1026 predecessor records/contexts and{delta["unchanged_compiled_inputs"]}compiled content inputs preserved.','Commercial coverage now recorded inconclusive; scoped source review narrows client/dependency/backend questions without manufacturing server schemas or native acceptance.','Historical Dataiku14.7.3 is distinct from unresolved DSS15.0.2; SAS preview2019 is not a support matrix; Domino api-docs is redirect only; Posit Finished retains exit code.','Q2-Q4 pass for exact bytes. Q1/Q5, mandatory coverage/depth and visual/final acceptance remain open.'],independent_next_actions=independent,global_blocker=None,phase_boundaries_are_stopping_points=False,background_worker_running=False)
    verify_bindings(review);write(BASE/'program-review.json',review)
    write(BASE/'continuation-checkpoint.json',dict(reader=state['reader'],sponsor=sponsor['pdf'],prior_git_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),remaining=ref(BASE/'remaining-operations.json','Complete actions'),independent_next_actions=independent,next_action=view['next_action'],proposal_accepted=False,visual_acceptance=False,global_blocker=None,background_worker_running=False))
    current=ROOT/'docs/program/execution/current-program.md';(BASE/'prior-current-program.md').write_bytes(current.read_bytes())
    rows='\n'.join(f"| {k} | {v.get('pass',0)} | {v.get('inconclusive',0)} | {v['open']} | {v['total']} |" for k,v in groups.items())
    current.write_text(f"""# Current executable proposal program

Updated 24 October 2026 (Asia/Shanghai). The [full program review](2026-10-24/program-refresh-workflow-contracts-v1/program-review.json)
and [remaining-operation register](2026-10-24/program-refresh-workflow-contracts-v1/remaining-operations.json)
account for all 376 proposal obligations. Canonical state and reviewed receipts govern execution.
The [preserved previous program](2026-10-24/program-refresh-workflow-contracts-v1/prior-current-program.md)
retains the complete longitudinal, panel, software, agent, integration and census history.

This is a research/product proposal supported by public and generated evidence before expensive bank experiments.
Proposal completion is distinct from product implementation, independent acceptance, bank validation and adoption.
Use python3 tools/run_program_checkpoint_v3.py status, next and check. Continue eligible independent branches across phases.
No unattended research worker runs; the active agent performs work.

## Current integrated documents

The [monograph](../../{Path(state['reader']['path']).name}) has {pub['pages']:,} pages,
1,031 audited citation records and 235 genuine scholarly PDFs. The exact paired
[sponsor proposal](../../{Path(sponsor['pdf']['path']).name}) has {sponsor['pages']} pages and 472 citations.
All 1,026 predecessor source records/contexts and {delta['unchanged_compiled_inputs']} content inputs survive.
Source traceability, exact authored calculations and all-page extracted text/bounds pass. Q2-Q4 pass for exact bytes.
Q1/Q5, mandatory coverage/depth and fresh visual/final acceptance remain open.

**240 recorded outcomes of 376; 112 ready; 203 nonpassing obligations.**
Recorded outcomes include inconclusive findings. Reference-only choices grant no native capability.

| Area | Pass | Inconclusive | Open | Total |
|---|---:|---:|---:|---:|
{rows}

## Completed commercial-workflow review

Thirty-eight primary blobs authenticate against cutoff trees. Only inspected spans support claims.
Dataiku14.7.3 distinguishes trigger and run identities, strict SUCCESS and warning/failure/abort outcomes.
A documented cancelled-trigger condition exposes an unguarded None path in the convenience composition;
it is a static finding, not an observed deployment failure. Historical DSS15.0.2 server originals remain unresolved.
SAS preview REST examples identify asynchronous job/state/provider-result/cleanup routes. Their document date/version
does not establish a supported server version; Visual Investigator BPMN is a distinct workflow product.
Domino's declared-range Requests2.31.0/urllib3 1.26.20 profile separates method/status/read retries from connection errors.
No solved lock or exactly-once server contract is inferred. The pinned api-docs original is only a mutable-guide redirect.
Posit's concrete C++ Local backend records nonzero ExitCode separately from Finished and explicitly lacks Cancel.
Historical prerequisites, current build declarations and smoke tests do not substitute for a supported product profile.

Exact authored four-request accounting yields three starts and one accepted artifact:1/4 per request versus1/3 per start.
Stipulated USD12 total is USD4 per start versus USD12 per accepted artifact. These are examples, not prices or bank value.
The first two builds caught unbreakable method-name overflow. Both failed attempts are preserved and unpublished;
reader-v3 uses readable method wording and passes all-page text/bounds checks. No visual acceptance is asserted.

## Remaining gaps and known routes

1. Software:56 open and43 inconclusive cells. Inspect cutoff primary evidence, reconcile source tails and state candidate-specific limits.
   Commercial follow-ups are immutable Dataiku/SAS server contracts, Domino v4/jobs schema and lock, supported Posit profiles and broader market coverage.
2. Reuse:56 open and3 inconclusive decisions. Complete explicit adopt/integrate/port/reference/reject arguments, dependency rights, owners, costs and triggers.
3. Frontier census:40 unread originals and four crosscutting obligations. Inspect originals; preserve inaccessible candidates and conflicting evidence.
4. Native prototype qualification:register public/generated trials after exact environments and experiment contracts exist; no source review counts as a run.
5. Manuscript:finish mandatory coverage/depth, Q1/Q5 and fresh visual review. Aggregate page count does not establish completeness.

Unrestricted latent identification, arbitrary persistence and hidden-state policy uncertainty have no promised universal repair.
Justified restrictions or extra information are necessary. Authentic bank truth, independent acceptance, platform reliability
and actual costs remain later external work, rather than blanket blockers for this proposal.

## Exact continuation

Next: {view['next']}. {view['next_action']}

Serialize canonical mutations, consume command exits, preserve source/failure evidence and keep outputs bounded.
Independent obligations do not block one another. There is no global blocker. Commit and push completed units.
""")
    controller.render(ROOT,state);print(json.dumps(dict(recorded=240,ready=112,nonpassing=203,reader_pages=pub['pages'],sponsor_pages=sponsor['pages'],next=view['next'])))
if __name__=='__main__':main()
