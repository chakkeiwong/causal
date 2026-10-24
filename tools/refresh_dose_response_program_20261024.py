#!/usr/bin/env python3
"""Reconcile every proposal obligation after the paired dose-response reference release."""
from collections import Counter,defaultdict
from copy import deepcopy
from pathlib import Path
import json,subprocess
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-24/program-refresh-dose-response-v1'
PRIOR=ROOT/'docs/program/execution/2026-10-24/program-refresh-bnlearn-v1'
PUB=ROOT/'docs/program/execution/2026-10-24/dose-response-reader-v1'
SPONSOR=ROOT/'docs/program/execution/2026-10-24/sponsor-dose-response-v1'
SOURCE=ROOT/'docs/program/execution/2026-10-24/dose-response-reuse-v1'
CXX=ROOT/'docs/program/execution/2026-10-24/policies-cxx-v3'
CENSUS=ROOT/'docs/program/execution/2026-10-24/census-affordance-fuzzing-v1'
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
        if key in ['SW.CELL.longitudinal_survival.Python','SW.CELL.longitudinal_survival.Java','SW.CELL.longitudinal_survival.Cxx','SW.CELL.longitudinal_survival.other_relevant','SW.CELL.policies_offpolicy.R','SW.CELL.policies_offpolicy.Python','SW.CELL.policies_offpolicy.Java','SW.CELL.policies_offpolicy.Cxx']:
            row['action']=read(ROOT/node['outputs'][0])['next_action']
        if key=='SW.CELL.policies_offpolicy.Cxx':
            row['corrected_source_followup']=ref(CXX/'review.json','Preserving metadata and dependency-anchor successor; same inconclusive outcome')
            row['source_repair_record']=ref(CXX/'repair-record.json','Preserved source and build failures')
        remaining.append(row)
    assert len(remaining)+sum(x['pass'] for x in lanes.values())==view['proposal_operations']==376
    groups={}
    for group,prefix,total in [('software','SW.CELL.',102),('reuse','SW.DECISION.',115),('chapters','TEXT.REVIEW.',22)]:
        selected=[v for k,v in results.items() if k.startswith(prefix)];groups[group]=dict(Counter(v['outcome'] for v in selected),open=total-len(selected),total=total)
    assert groups['software']['pass']==3 and groups['software']['inconclusive']==50 and groups['software']['open']==49
    assert groups['reuse']['pass']==64 and groups['reuse']['inconclusive']==3 and groups['reuse']['open']==48
    assert view['recorded_proposal_operations']==256 and view['ready_proposal_operations']==len(ready) and len(remaining)==195
    census=read(CENSUS/'census-register.json');counts=Counter(x['disposition'] for x in census['items']);assert counts['inspected_primary_retained_with_limits']==80 and counts['open_original_not_inspected']==33
    assert len(read(PUB/'reader/source-audit.json')['sources'])==1108 and len(read(SPONSOR/'source-audit.json')['sources'])==600
    delta=read(PUB/'release-source-review.json')['checks'];by_id={x['id']:x for x in remaining};independent=[]
    for lane in ['software','commercial','reuse','llm','manuscript','release','proposal_acceptance']:
        selected=[n for n in ready if n['lane']==lane]
        if selected:
            n=selected[0];independent.append(dict(lane=lane,operation=n['id'],action=by_id[n['id']]['action'],depends=n['depends'],requires_inputs=n['requires_inputs']))
    BASE.mkdir();write(BASE/'state-snapshot.json',state);write(BASE/'status-snapshot.json',view)
    write(BASE/'remaining-operations.json',dict(reader=state['reader'],recorded=256,proposal_operations=376,ready=view['ready_proposal_operations'],coverage=groups,operations=remaining,census=ref(CENSUS/'census-register.json','80/33 preserved census'),proposal_accepted=False))
    evidence=[ref(PUB/'working-release.json','Current reader'),ref(SPONSOR/'working-release.json','Exact paired sponsor'),ref(PRIOR/'program-review.json','Previous full reconciliation'),ref(BASE/'remaining-operations.json','Every nonpassing obligation'),ref(SOURCE/'review.json','Bounded original and software review'),ref(SOURCE/'source-audit.json','Primary identities and anchors'),ref(SOURCE/'omissions-register.json','Remaining source/qualification questions'),ref(CENSUS/'census-register.json','Preserved80/33census'),ref(Path(__file__),'Complete reconciliation')]
    review=dict(status='pass_for_consistency_not_completion',reviewer=dict(name='Codex author/coordinator',kind='author'),evidence=evidence,effective_lane_counts={k:dict(v) for k,v in lanes.items()},findings=['All376 proposal obligations reconciled;256 recorded and195 nonpassing remain; Dose-response has a passing umbrella reference disposition for five named candidates,not native capability admission.',f'Exact reader{pub["pages"]}pages/1108citations/251scholarly PDFs; sponsor{sponsor["pages"]}pages/600citations.',f'All1101 predecessor records/contexts and{delta["unchanged_compiled_inputs"]}compiled inputs preserved.','Five R dose-response source profiles,genuine CausalGPS original and exact target,density,balance,inference and cost witnesses add seven records; every predecessor remains preserved.','Census remains80/33plus4crosscutting; software3pass/50inconclusive/49open;reuse64pass/3inconclusive/48open;no native capability granted.','Q2-Q4 pass for exact bytes; Q1/Q5, mandatory repairs and visual/final acceptance remain open.'],independent_next_actions=independent,global_blocker=None,phase_boundaries_are_stopping_points=False,background_worker_running=False)
    verify_bindings(review);write(BASE/'program-review.json',review)
    write(BASE/'continuation-checkpoint.json',dict(reader=state['reader'],sponsor=sponsor['pdf'],prior_git_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),remaining=ref(BASE/'remaining-operations.json','Complete actions'),independent_next_actions=independent,next_action=view['next_action'],proposal_accepted=False,visual_acceptance=False,global_blocker=None,background_worker_running=False))
    current=ROOT/'docs/program/execution/current-program.md';(BASE/'prior-current-program.md').write_bytes(current.read_bytes())
    rows='\n'.join(f"| {k} | {v.get('pass',0)} | {v.get('inconclusive',0)} | {v['open']} | {v['total']} |" for k,v in groups.items())
    current.write_text(f"""# Current executable proposal program

Updated 24 October 2026 (Asia/Shanghai). The [full reconciliation](2026-10-24/program-refresh-dose-response-v1/program-review.json)
and [remaining-operation register](2026-10-24/program-refresh-dose-response-v1/remaining-operations.json)
account for all 376 proposal obligations. Canonical state and reviewed receipts govern execution.
The [preserved predecessor](2026-10-24/program-refresh-dose-response-v1/prior-current-program.md) retains earlier findings.

This is a research/product proposal. Public/generated prototype evidence justifies later expensive bank experiments.
Proposal completion is distinct from implementation, independent acceptance, bank validation and adoption.
Use python3 tools/run_program_checkpoint_v3.py status, next and check. Continue eligible independent branches across phases.
No unattended worker, sibling edits or downloaded-code execution. The active agent performs eligible work.

## Current integrated documents

The [monograph](../../{Path(state['reader']['path']).name}) has {pub['pages']:,} pages,
1,108 audited citation records and 251 genuine scholarly PDFs. The exact paired
[sponsor proposal](../../{Path(sponsor['pdf']['path']).name}) has {sponsor['pages']} pages and 600 citations.
All 1,101 predecessor records, citation contexts and {delta['unchanged_compiled_inputs']} compiled content inputs survive.
Source traceability, exact authored examples and all-page text/bounds checks pass; Q2-Q4 pass for exact bytes.
Q1/Q5, mandatory coverage/depth and fresh visual/final acceptance remain open. Page count is not completion.

**256 recorded outcomes of 376; {view['ready_proposal_operations']} ready; 195 nonpassing obligations.**
Recorded outcomes include inconclusive findings; source review grants no native capability.

| Area | Pass | Inconclusive | Open | Total |
|---|---:|---:|---:|---:|
{rows}

## Newly reconciled work

Five selected R distributions resolve the dose-response umbrella into distinct roles:
causaldrf for transparent adjustment, CausalGPS for GPS design, WeightIt for point
and longitudinal weighting, drc for response fitting and inverse targets, and
DoseFinding for experimental contrasts and model selection. All38 selected source
files authenticate;27 have technically inspected anchors. One genuine CausalGPS
original is inspected with its assumptions, adverse examples and omitted interval detail.

Seven new records preserve every prior source identity, context and compiled input.
Exact authored witnesses distinguish confounding, density measures, transformed scores,
nonlinear balance, trimming targets, empty weights, pointwise versus simultaneous
coverage, customer dependence, shared-baseline covariance and inverse/optimal doses.
Reference dispositions grant no native capability. Public/generated qualification,
rights/dependencies, owners, failure denominators and costs are explicit future work.
An arithmetic draft and a CLI syntax failure are preserved with their corrections.
The C++ metadata/dependency successor remains correctly linked. Census remains
80 inspected and33unread originals plus four crosscutting obligations.

## Remaining gaps and routes

1. Software:49open and50inconclusive cells. Resolve aliases/search tails, inspect primary delegates and retain target-specific limits.
2. Reuse:48open and3inconclusive decisions. Complete concrete choices with source/rights, owners, costs and triggers.
3. Frontier census:33unread originals and four crosscutting obligations. Candidate163conference original remains locally inaccessible; candidate165journal original remains unavailable despite its related-preprint review; candidate217access/date and candidate27metadata limits remain local.
4. Commercial qualification: resolve named supported server/API profiles, entitlement, price and complete request/failure denominators.
5. Public prototypes: preregister justified task/version splits, semantic/refusal/fault oracles and full costs before broader native or bank claims.
6. Manuscript acceptance: finish mandatory coverage/depth, Q1/Q5 and fresh visual review; text bounds alone are not visual acceptance.

Unrestricted latent identification, arbitrary persistence and hidden-state policy uncertainty have no promised universal repair.
Additional information or justified restrictions are required. Authentic bank truth, independent review, target-platform
acceptance and actual economic value remain later external work, not global proposal blockers.

## Exact continuation

Next:{view['next']}. {view['next_action']}

Serialize canonical mutations and consume command exits. Preserve immutable sources and failed attempts.
Keep commands/output bounded. Independent obligations do not block one another; phase boundaries do not stop execution.
Commit and push completed units, then continue the next ready obligation.
""")
    controller.render(ROOT,state);print(json.dumps(dict(recorded=256,ready=view['ready_proposal_operations'],nonpassing=195,reader_pages=pub['pages'],sponsor_pages=sponsor['pages'],next=view['next'])))
if __name__=='__main__':main()
