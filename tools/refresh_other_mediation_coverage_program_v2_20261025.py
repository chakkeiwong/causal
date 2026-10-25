#!/usr/bin/env python3
"""Reconcile every proposal obligation after remaining-language mediation comparison."""
from collections import Counter,defaultdict
from copy import deepcopy
from pathlib import Path
import json,subprocess
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-25/program-refresh-other-mediation-coverage-v1'
PRIOR=ROOT/'docs/program/execution/2026-10-25/program-refresh-cxx-mediation-coverage-v1'
PUB=ROOT/'docs/program/execution/2026-10-25/other-mediation-coverage-reader-v1'
READER=ROOT/'docs/program/execution/2026-10-25/other-mediation-coverage-reader-v1'
SPONSOR=ROOT/'docs/program/execution/2026-10-25/sponsor-other-mediation-coverage-v1'
SOURCE=ROOT/'docs/program/execution/2026-10-25/other-mediation-coverage-v1'
PANEL=ROOT/'docs/program/execution/2026-10-24/linearmodels-panel-v1'
CXX=ROOT/'docs/program/execution/2026-10-24/policies-cxx-v3'
CENSUS=ROOT/'docs/program/execution/2026-10-25/census-route-followup-v1'
read=lambda p:json.loads(p.read_text())

def main():
    assert not BASE.exists();state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active'] is None
    view=controller.status(ROOT,state);graph,merged,stages,ready,_=run.queue(ROOT,state)
    pub,sponsor=read(PUB/'working-release.json'),read(SPONSOR/'working-release.json')
    for d in [pub,sponsor,read(PRIOR/'program-review.json'),read(SOURCE/'plan-review-v2.json'),read(ROOT/'docs/program/execution/2026-10-24/fect-reuse-v1/review.json')]:verify_bindings(d)
    assert run.same_reader(state['reader'],pub['pdf']) and run.same_reader(state['reader'],sponsor['paired_monograph'])
    assert any(run.same_reader(d,sponsor['pdf']) and run.same_reader(d.get('paired_monograph',{}),state['reader']) for d in state['deliveries'] if d.get('kind')=='working_sponsor'), 'Sponsor manifest is not yet canonically delivered'
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
        if result:
            receipt=read(ROOT/result['path']);core.bound(ROOT,result)
            trigger=receipt.get('revisit_trigger','').strip()
            output_notes=[]
            for path in node['outputs']:
                target=ROOT/path
                if target.is_file() and target.suffix=='.json':
                    output=read(target)
                    for field in ['revisit_trigger','next_action']:
                        value=output.get(field)
                        if isinstance(value,str) and value.strip():output_notes.append(value.strip())
            if trigger or output_notes:
                row['action']=trigger or output_notes[0]
            else:
                row['action']='Create a reviewed successor for these recorded unresolved limits: '+'; '.join(receipt.get('limitations',[]))
            row['action_basis']=result
            if notes:row['superseded_pre_result_checkpoint']=notes[-1]
        elif key in merged['execution_program'].get('blocks', {}):
            block=merged['execution_program']['blocks'][key];core.bound(ROOT,block['receipt'])
            row.update(action=block['revisit_trigger'],action_basis=block['receipt'],continuation_status='blocked_local')
            row.pop('action_checkpoint',None)
            if notes:row['superseded_pre_block_checkpoint']=notes[-1]
        elif notes:
            core.bound(ROOT,notes[-1]);note=read(ROOT/notes[-1]['path']);run.validate_note(ROOT,note,'progress');row.update(action=note['next_action'],action_checkpoint=notes[-1])
        if key=='SW.CELL.computation_workflow.commercial':
            row['action']=read(ROOT/node['outputs'][0])['next_action'];row.pop('action_checkpoint',None)
        if key in ['SW.CELL.longitudinal_survival.Python','SW.CELL.longitudinal_survival.Java','SW.CELL.longitudinal_survival.Cxx','SW.CELL.longitudinal_survival.other_relevant','SW.CELL.policies_offpolicy.R','SW.CELL.policies_offpolicy.Python','SW.CELL.policies_offpolicy.Java','SW.CELL.policies_offpolicy.Cxx']:
            row['action']=read(ROOT/node['outputs'][0])['next_action']
        if key=='SW.CELL.policies_offpolicy.Cxx':
            row['corrected_source_followup']=ref(CXX/'review.json','Preserving metadata and dependency-anchor successor; same inconclusive outcome')
            row['source_repair_record']=ref(CXX/'repair-record.json','Preserved source and build failures')
        if key=='SW.CELL.panels_did.Python':
            follow=read(PANEL/'review.json');verify_bindings(follow)
            assert result and result['outcome']=='inconclusive' and follow['outcome_remains']=='inconclusive'
            row['action']=follow['next_action']
            row['corrected_source_followup']=ref(PANEL/'review.json','Panel-specific source followup; original inconclusive receipt preserved')
            row['action_basis']=row['corrected_source_followup']
            row.pop('action_checkpoint',None)
        if key=='TEXT.REVIEW.L6':
            follow=read(ROOT/'docs/program/execution/2026-10-24/backend-census-v1/remaining-l6-gap.json');verify_bindings(follow)
            assert result and result['outcome']=='inconclusive'
            row.update(action=follow['next_action'],corrected_source_followup=ref(ROOT/'docs/program/execution/2026-10-24/backend-census-v1/remaining-l6-gap.json','Named backend progress; incomplete L6 coverage'),action_basis=ref(ROOT/'docs/program/execution/2026-10-24/backend-census-v1/remaining-l6-gap.json','Current source followup'))
            row.pop('action_checkpoint',None)
        remaining.append(row)
    assert len(remaining)+sum(x['pass'] for x in lanes.values())==view['proposal_operations']==376
    groups={}
    for group,prefix,total in [('software','SW.CELL.',102),('reuse','SW.DECISION.',115),('chapters','TEXT.REVIEW.',22)]:
        selected=[v for k,v in results.items() if k.startswith(prefix)];groups[group]=dict(Counter(v['outcome'] for v in selected),open=total-len(selected),total=total)
    assert groups['software']['pass']==3 and groups['software']['inconclusive']==78 and groups['software']['open']==21
    assert groups['reuse']['pass']==109 and groups['reuse']['inconclusive']==4 and groups['reuse']['open']==2
    assert view['recorded_proposal_operations']==330 and view['ready_proposal_operations']==len(ready) and len(remaining)==150
    census=read(CENSUS/'census-register.json');counts=Counter(x['disposition'] for x in census['items']);assert counts['inspected_primary_retained_with_limits']==82 and counts['open_original_not_inspected']==31
    assert len(read(READER/'reader/source-audit.json')['sources'])==1346 and len(read(SPONSOR/'source-audit.json')['sources'])==975
    delta=read(PUB/'release-source-review-v2.json')['checks'];by_id={x['id']:x for x in remaining};independent=[]
    for lane in ['software','commercial','reuse','llm','manuscript','release','proposal_acceptance']:
        selected=[n for n in ready if n['lane']==lane]
        if selected:
            n=selected[0];independent.append(dict(lane=lane,operation=n['id'],action=by_id[n['id']]['action'],depends=n['depends'],requires_inputs=n['requires_inputs']))
    BASE.mkdir();write(BASE/'state-snapshot.json',state);write(BASE/'status-snapshot.json',view)
    write(BASE/'remaining-operations.json',dict(reader=state['reader'],recorded=330,proposal_operations=376,ready=view['ready_proposal_operations'],coverage=groups,operations=remaining,census=ref(CENSUS/'census-register.json','82/31 preserved census'),proposal_accepted=False))
    evidence=[ref(PUB/'working-release.json','Current reader'),ref(SPONSOR/'working-release.json','Exact paired sponsor'),ref(PRIOR/'program-review.json','Previous full reconciliation'),ref(BASE/'remaining-operations.json','Every nonpassing obligation'),ref(SOURCE/'review.json','remaining-language mediation source comparison'),ref(ROOT/'docs/program/execution/2026-10-25/dara-reuse-v1/review.json','Dara bounded inconclusive commercial resolution'),ref(ROOT/'docs/program/execution/2026-10-25/commercial-tail-v1/acquisition-result.json','Six unavailable commercial acquisition routes'),ref(SOURCE/'plan-review.json','Reviewed preserving integration plan'),ref(ROOT/'docs/program/execution/2026-10-24/backend-census-v1/remaining-l6-gap.json','Remaining L6 gap and exact continuation'),ref(ROOT/'docs/program/execution/2026-10-24/backend-census-v1/blocked-continuation-review.json','Block receipt supersedes pre-block progress without unblocking'),ref(CENSUS/'census-register.json','Preserved82/31census'),ref(ROOT/'docs/program/execution/2026-10-24/census-clinical-evaluation-v1/acquisition-review.json','Three original-source client challenges'),ref(ROOT/'docs/program/execution/2026-10-24/census-energy-workflow-v1/acquisition-review.json','Workflow and energy original-access limits'),ref(ROOT/'docs/program/execution/2026-10-24/execution-action-repair-v1/verification.json','15verifiedcorrectedcontinuations'),ref(ROOT/'docs/program/execution/2026-10-24/navigation-repair-v1/review.json','Formattedcountrepair'),ref(ROOT/'docs/program/execution/2026-10-24/fect-reuse-v1/review.json','Preserved fect reference decision'),ref(Path(__file__),'Complete reconciliation')]
    review=dict(status='pass_for_consistency_not_completion',reviewer=dict(name='Codex author/coordinator',kind='author'),evidence=evidence,effective_lane_counts={k:dict(v) for k,v in lanes.items()},findings=['All376 proposal obligations reconciled;330 recorded and150 nonpassing remain; The remaining-language mediation cell records an inconclusive outcome;no native capability admitted.',f'Exact reader{pub["pages"]}pages/1346citations/265scholarly PDFs; sponsor{sponsor["pages"]}pages/975citations.',f'All1339 predecessor records/contexts and{delta["unchanged_compiled_inputs"]}compiled inputs preserved.','Fifty-five authentic originals and40technical anchors cover MATLAB resampling and intervals,Julia covariance/index and mediator-law contracts,and Stata estimator/rights boundaries.','Census remains82/31plus4crosscutting; software3pass/78inconclusive/21open;reuse109pass/4inconclusive/2open; twelve recorded source/identity limits retained without changing dispositions.','Q2-Q4 pass for exact bytes; Q1/Q5, mandatory repairs and visual/final acceptance remain open.','Completed-inconclusive operations use final receipt/output revisit actions; older pre-result checkpoints no longer instruct repeated builds or recordings.'],independent_next_actions=independent,global_blocker=None,phase_boundaries_are_stopping_points=False,background_worker_running=False)
    verify_bindings(review);write(BASE/'program-review.json',review)
    write(BASE/'continuation-checkpoint.json',dict(reader=state['reader'],sponsor=sponsor['pdf'],prior_git_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),remaining=ref(BASE/'remaining-operations.json','Complete actions'),independent_next_actions=independent,next_action=view['next_action'],proposal_accepted=False,visual_acceptance=False,global_blocker=None,background_worker_running=False))
    current=ROOT/'docs/program/execution/current-program.md';(BASE/'prior-current-program.md').write_bytes(current.read_bytes())
    rows='\n'.join(f"| {k} | {v.get('pass',0)} | {v.get('inconclusive',0)} | {v['open']} | {v['total']} |" for k,v in groups.items())
    current.write_text(f"""# Current executable proposal program

Updated 25 October 2026 (Asia/Shanghai). The [full reconciliation](2026-10-25/program-refresh-other-mediation-coverage-v1/program-review.json)
and [remaining-operation register](2026-10-25/program-refresh-other-mediation-coverage-v1/remaining-operations.json)
account for all 376 proposal obligations. Canonical state and reviewed receipts govern execution.
The [preserved predecessor](2026-10-25/program-refresh-other-mediation-coverage-v1/prior-current-program.md) retains earlier findings.

This is a research/product proposal. Public/generated prototype evidence justifies later expensive bank experiments.
Proposal completion is distinct from implementation, independent acceptance, bank validation and adoption.
Use python3 tools/run_program_checkpoint_v3.py status, next and check. Continue eligible independent branches across phases.
No unattended worker, sibling edits or downloaded-code execution. The active agent performs eligible work.

## Current integrated documents

The [monograph](../../{Path(state['reader']['path']).name}) has {pub['pages']:,} pages,
{len(read(READER/'reader/source-audit.json')['sources']):,} audited citation records and 265 genuine scholarly PDFs. The exact paired
[sponsor proposal](../../{Path(sponsor['pdf']['path']).name}) has {sponsor['pages']} pages and 975 citations.
All {delta['preserved_citation_records']:,} predecessor records, citation contexts and {delta['unchanged_compiled_inputs']} compiled content inputs survive.
Source traceability, exact authored examples and all-page text/bounds checks pass; Q2-Q4 pass for exact bytes.
Q1/Q5, mandatory coverage/depth and fresh visual/final acceptance remain open. Page count is not completion.

**330 recorded outcomes of 376; {view['ready_proposal_operations']} ready; 150 nonpassing obligations.**
Recorded outcomes include inconclusive findings; source review grants no native capability.

| Area | Pass | Inconclusive | Open | Total |
|---|---:|---:|---:|---:|
{rows}

## Newly reconciled work

The preserving successor compares CANlab,Paramed.jl,Mediation.jl,CausalMediation.jl,CausalTargeted.jl and Stata cmed. Fifty-five authentic originals ground resampling,covariance,interval probabilities,joint mediator-law and runtime/rights contracts. Exact authored examples reproduce; static findings are not native failure-rate measurements. Coverage remains inconclusive;no native admission is inferred.

All 1,339 predecessor records, contexts and content inputs survive; the reader has 1,346 records and 265 scholarly PDFs, with 975 in the paired sponsor. Coverage is inconclusive: four successful bounded queries retain explicit irrelevant,uninspected and unreturned candidates;package/code-comment scholarly references are not admitted as technical papers; complete delegates, installed artifact/dependency rights and native law-specific qualification remain open. MATLAB and HUGIN are locally blocked on authentic named-edition sources; other ready work remains eligible.

There are 330 recorded outcomes of 376 and 150 nonpassing obligations. Software is three pass / 78 inconclusive / 21 open; reuse is 109 pass / four inconclusive / two open; census remains 82 inspected / 31 unread plus four crosscutting tasks. Recorded work is not final acceptance.

## Remaining gaps and routes

1. Software: 21 open and 78 inconclusive cells. Complete explicit search tails,
   inspect remaining primary delegates, and qualify narrowly matched public trials.
2. Reuse: two open and four inconclusive decisions. Resolve concrete candidates,
   rights, targets, owners, costs and revisit conditions without umbrella approval.
3. Frontier census: 31 unread originals and four crosscutting tasks. Candidate
   163 original access, 165 final-original access, 217 access/date and 27 metadata
   limits remain local. Clinical 125/207/277 client challenges and workflow 136
   and energy 218 original access limits are preserved; candidate225 final conference
   bytes remain a separate omission after the selected preprint review. Candidate 214 final
   publisher layout, supplementary text and native reproduction remain separate from
   the inspected author original. Candidates157/199/202/206 have additional recorded
   permitted-route/identity limits; no substitute original is admitted. Independent work continues.
4. Commercial qualification: resolve named supported server/API profiles,
   entitlement, price and complete request/failure denominators.
5. Public prototypes: preregister task/version splits, scientific and refusal
   oracles, native environment, fault tests and full costs before expensive bank work.
6. Manuscript acceptance: complete mandatory coverage/depth, Q1/Q5 and a fresh
   visual review. Text bounds alone do not establish visual or final acceptance.

Known routes exist for bounded source acquisition, explicit comparisons,
conversion contracts, native public fixtures and manuscript integration. Unknown
assignment truth, unrestricted hidden-state identification, arbitrary persistence
and universal dependent-data uncertainty have no promised universal repair.
They need additional information or justified restrictions. Independent review,
authentic bank truth, platform acceptance and actual economic value remain later
external gates, not global proposal blockers.

## Execution repair

Earlier refreshes preferred progress checkpoints even after an operation had a
recorded outcome. This could repeat instructions to finish a build or record a
receipt that already existed. Recorded outcomes now derive continuation from
the final receipt or output revisit trigger. Recorded local blocks take precedence over earlier progress checkpoints.
Pre-result and pre-block checkpoints remain history; other open operations use
their latest durable progress. The L6 source followup preserves its inconclusive outcome. The census successor records current 82/31 counts and binds local access failures to the affected candidate actions. Yield verification checks the saved operation checkpoint independently of the next scheduler choice, so normal lane rotation does not falsely stop publication.

## Exact continuation

Next: {view['next']}. {view['next_action']}

Serialize canonical mutations and consume command exits. Preserve immutable sources and failed attempts.
Keep commands/output bounded. Independent obligations do not block one another; phase boundaries do not stop execution.
Publish reviewed independent deltas in bounded waves to avoid repeated full-book reviews; record each decision separately. Commit and push completed waves, then continue ready obligations.
""")
    controller.render(ROOT,state);print(json.dumps(dict(recorded=330,ready=view['ready_proposal_operations'],nonpassing=150,reader_pages=pub['pages'],sponsor_pages=sponsor['pages'],next=view['next'])))
if __name__=='__main__':main()
