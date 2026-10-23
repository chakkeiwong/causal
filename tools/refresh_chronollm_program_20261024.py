#!/usr/bin/env python3
"""Reconcile every proposal obligation after the paired ChronoLLM release."""
from collections import Counter,defaultdict
from copy import deepcopy
from pathlib import Path
import json,subprocess
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-24/program-refresh-chronollm-v1'
PRIOR=ROOT/'docs/program/execution/2026-10-24/program-refresh-openlineage-v1'
PUB=ROOT/'docs/program/execution/2026-10-24/chronollm-reader-v1'
SPONSOR=ROOT/'docs/program/execution/2026-10-24/sponsor-chronollm-v1'
SOURCE=ROOT/'docs/program/execution/2026-10-24/census-chronollm-v1'
CENSUS=SOURCE
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
    assert groups['reuse']['pass']==57 and groups['reuse']['inconclusive']==3 and groups['reuse']['open']==55
    assert view['recorded_proposal_operations']==243 and view['ready_proposal_operations']==len(ready) and len(remaining)==202
    census=read(CENSUS/'census-register.json');counts=Counter(x['disposition'] for x in census['items']);assert counts['inspected_primary_retained_with_limits']==75 and counts['open_original_not_inspected']==38
    assert len(read(PUB/'reader/source-audit.json')['sources'])==1043 and len(read(SPONSOR/'source-audit.json')['sources'])==493
    delta=read(PUB/'release-source-review.json')['checks'];by_id={x['id']:x for x in remaining};independent=[]
    for lane in ['software','commercial','reuse','llm','manuscript','release','proposal_acceptance']:
        selected=[n for n in ready if n['lane']==lane]
        if selected:
            n=selected[0];independent.append(dict(lane=lane,operation=n['id'],action=by_id[n['id']]['action'],depends=n['depends'],requires_inputs=n['requires_inputs']))
    BASE.mkdir();write(BASE/'state-snapshot.json',state);write(BASE/'status-snapshot.json',view)
    write(BASE/'remaining-operations.json',dict(reader=state['reader'],recorded=243,proposal_operations=376,ready=view['ready_proposal_operations'],coverage=groups,operations=remaining,census=ref(CENSUS/'census-register.json','75/38 preserved census'),proposal_accepted=False))
    evidence=[ref(PUB/'working-release.json','Current reader'),ref(SPONSOR/'working-release.json','Exact paired sponsor'),ref(PRIOR/'program-review.json','Previous full reconciliation'),ref(BASE/'remaining-operations.json','Every nonpassing obligation'),ref(SOURCE/'review.json','Bounded original and software review'),ref(SOURCE/'source-audit.json','Primary identities and anchors'),ref(SOURCE/'omissions-register.json','Remaining source/qualification questions'),ref(CENSUS/'census-register.json','Preserved75/38census'),ref(Path(__file__),'Complete reconciliation')]
    review=dict(status='pass_for_consistency_not_completion',reviewer=dict(name='Codex author/coordinator',kind='author'),evidence=evidence,effective_lane_counts={k:dict(v) for k,v in lanes.items()},findings=['All376 proposal obligations reconciled;243 recorded and202 nonpassing remain; census progress is not a fabricated new operation closure.',f'Exact reader{pub["pages"]}pages/1043citations/237scholarly PDFs; sponsor{sponsor["pages"]}pages/493citations.',f'All1041 predecessor records/contexts and{delta["unchanged_compiled_inputs"]}compiled inputs preserved.','ChronoLLM2025original and exact authored metric/causal/cost witnesses add2records and1genuine paper.','Code quality and execution remain distinct from causal identification; eight-family commercial outcome remains inconclusive; no upstream code executed.','Q2-Q4 pass for exact bytes; Q1/Q5, mandatory repairs and visual/final acceptance remain open.'],independent_next_actions=independent,global_blocker=None,phase_boundaries_are_stopping_points=False,background_worker_running=False)
    verify_bindings(review);write(BASE/'program-review.json',review)
    write(BASE/'continuation-checkpoint.json',dict(reader=state['reader'],sponsor=sponsor['pdf'],prior_git_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),remaining=ref(BASE/'remaining-operations.json','Complete actions'),independent_next_actions=independent,next_action=view['next_action'],proposal_accepted=False,visual_acceptance=False,global_blocker=None,background_worker_running=False))
    current=ROOT/'docs/program/execution/current-program.md';(BASE/'prior-current-program.md').write_bytes(current.read_bytes())
    rows='\n'.join(f"| {k} | {v.get('pass',0)} | {v.get('inconclusive',0)} | {v['open']} | {v['total']} |" for k,v in groups.items())
    current.write_text(f"""# Current executable proposal program

Updated 24 October 2026 (Asia/Shanghai). The [full reconciliation](2026-10-24/program-refresh-chronollm-v1/program-review.json)
and [remaining-operation register](2026-10-24/program-refresh-chronollm-v1/remaining-operations.json)
account for all 376 proposal obligations. Canonical state and reviewed receipts govern execution.
The [preserved predecessor](2026-10-24/program-refresh-chronollm-v1/prior-current-program.md) retains earlier findings.

This is a research/product proposal. Public/generated prototype evidence justifies later expensive bank experiments.
Proposal completion is distinct from implementation, independent acceptance, bank validation and adoption.
Use python3 tools/run_program_checkpoint_v3.py status, next and check. Continue eligible independent branches across phases.
No unattended worker, sibling edits or downloaded-code execution. The active agent performs eligible work.

## Current integrated documents

The [monograph](../../{Path(state['reader']['path']).name}) has {pub['pages']:,} pages,
1,043 audited citation records and 237 genuine scholarly PDFs. The exact paired
[sponsor proposal](../../{Path(sponsor['pdf']['path']).name}) has {sponsor['pages']} pages and 493 citations.
All 1,041 predecessor records, citation contexts and {delta['unchanged_compiled_inputs']} compiled content inputs survive.
Source traceability, exact authored examples and all-page text/bounds checks pass; Q2-Q4 pass for exact bytes.
Q1/Q5, mandatory coverage/depth and fresh visual/final acceptance remain open. Page count is not completion.

**243 recorded outcomes of 376; {view['ready_proposal_operations']} ready; 202 nonpassing obligations.**
Recorded outcomes include inconclusive findings; source review grants no native capability.

| Area | Pass | Inconclusive | Open | Total |
|---|---:|---:|---:|---:|
{rows}

## Newly reconciled work

The eight-family commercial workflow comparison now records an inconclusive outcome.
Databricks, Snowflake, Azure Machine Learning, AWS Step Functions, Dataiku, SAS, Domino and Posit
have explicit source/use-case comparisons against the narrow local reference runtime and proposed workers.
Supported cutoff server editions, complete failure semantics, deployment entitlements, actual prices and
matched native trials remain incomplete. Their existing manuscript treatment is preserved; the register
adds no fabricated depth or commercial acceptance. Missing evidence is not absent capability.

ChronoLLM adds a genuine52-page19August2025preprint and exact authored references.
Its domain-specific curation, version-bound API knowledge and metric-specific evaluation inform public prototype design.
Reported combined judge improvement26.23 coexists with documentation-only decline5.19; source metrics are not acceptance probabilities.
Two authored structural worlds have identical observed data but intervention effects10and0USD and stipulated net5and-5USD.
Compiling or running a program cannot select the scientifically correct world. An authored full-cost example
includes expert preparation:33USDtotal,5.50percompiled and16.50peraccepted output; no measured price or ROI.
Companion originals, task/split/scorer artifacts, exact rights and matched held-out trials remain explicit follow-ups.

Census now has75inspected and38unread originals of113, plus four crosscutting obligations.
Onlycandidate120advances in the successor; all other candidate dispositions are preserved.
OpenLineage's reference-only decision, Java survival, K-Bench and all preceding content remain integrated.
The OpenLineage paired release and full reconciliation were committed and pushed as48bda947.

## Remaining gaps and routes

1. Software:55open and44inconclusive cells. Resolve aliases/search tails, inspect primary delegates and retain target-specific limits.
2. Reuse:55open and3inconclusive decisions. Complete concrete choices with source/rights, owners, costs and triggers.
3. Frontier census:38unread originals and four crosscutting obligations. Candidate217 original access/date remains local; candidate27 metadata supplies no original.
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
    controller.render(ROOT,state);print(json.dumps(dict(recorded=243,ready=view['ready_proposal_operations'],nonpassing=202,reader_pages=pub['pages'],sponsor_pages=sponsor['pages'],next=view['next'])))
if __name__=='__main__':main()
