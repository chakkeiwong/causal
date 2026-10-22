#!/usr/bin/env python3
"""Refresh every remaining proposal obligation after domain-knowledge review."""
from collections import Counter, defaultdict
import json
from pathlib import Path
import subprocess
import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run=extension.base
ROOT=run.core.ROOT
WORK=ROOT/'docs/program/execution/2026-10-22/census-domain-knowledge-v1'
SPONSOR=ROOT/'docs/program/execution/2026-10-22/sponsor-domain-knowledge-v1'
BASE=ROOT/'docs/program/execution/2026-10-22/program-refresh-domain-v1'
PRIOR=ROOT/'docs/program/execution/2026-10-22/program-refresh-r-iv-v1'
CENSUS=WORK/'census-register.json'
read=lambda p:json.loads(p.read_text())


def main():
    assert not BASE.exists()
    state=run.core.read(ROOT,run.core.STATE);assert state['execution_runtime']['active'] is None
    assert state['reader']['path']=='docs/causal_proposal_domain_knowledge_reviewed_2026-10-22.pdf'
    sponsor=read(SPONSOR/'working-release.json');verify_bindings(sponsor)
    assert run.same_reader(state['reader'],sponsor['paired_monograph'])
    view=run.status(ROOT,state);graph,merged,stages,ready,_=run.queue(ROOT,state)
    assert {q['id']:q['status'] for q in view['proposal_gaps']}==dict(Q1='open',Q2='pass',Q3='pass',Q4='pass',Q5='open')
    results=merged['execution_program']['results'];groups={};obligations=[];lanes=defaultdict(Counter)
    previous={r['id']:r for r in read(PRIOR/'remaining-operations.json')['operations']}
    for node in graph['nodes']:
        identifier=node['id'];result=results.get(identifier)
        if stages[identifier]!='proposal_now':continue
        lanes[node['lane']][result['outcome'] if result else 'open']+=1
        if result and result['outcome']=='pass':continue
        progress=merged['execution_program']['progress'].get(identifier,[])
        action=read(ROOT/progress[-1]['path'])['next_action'] if progress else node['action']
        item=dict(id=identifier,lane=node['lane'],title=node['title'],status=result['outcome'] if result else 'open',
            action=action,prerequisites=run.ledger.blockers(merged,node),outputs=node['outputs'],evidence=result,requires_inputs=node['requires_inputs'])
        if identifier in previous:
            for key in ['corrected_source_followup','source_followup']:
                if key in previous[identifier]:item[key]=previous[identifier][key]
            if identifier=='SW.CELL.iv_rd_design.R':item['action']=previous[identifier]['action']
        if identifier=='LL.CENSUS':
            item['action']='Inspect 54 remaining originals including ontology candidate 176 when a legitimate copy is available; continue independent candidates and four complementary-search/task-coverage obligations. Newly integrated 53/182 do not close census.'
            item['source_followup']=ref(WORK/'omissions-register.json','Exact candidate/raw-evidence/visual follow-ups')
        if identifier=='SW.CELL.iv_rd_design.Python':
            item['corrected_source_followup']=ref(WORK/'next-lane-review.json','CausalPy inheritance is sharp RD only with equal-tail plotting quantiles; inspect IV separately')
        obligations.append(item)
    for name,prefix,total in [('software','SW.CELL.',102),('reuse','SW.DECISION.', 115),('chapters','TEXT.REVIEW.', 22)]:
        selected={k:v for k,v in results.items() if k.startswith(prefix)}
        groups[name]=dict(Counter(v['outcome'] for v in selected.values()),open=total-len(selected),total=total)
    census_counts=Counter(x['disposition'] for x in read(CENSUS)['items'])
    inspected=census_counts['inspected_primary_retained_with_limits'];unread=census_counts['open_original_not_inspected']
    assert (inspected,unread)==(59,54)
    count=len(read(WORK/'reader/source-audit.json')['sources']);papers=read(WORK/'traceability-review.json')['scholarly_pdfs']
    sponsor_count=len(read(SPONSOR/'source-audit.json')['sources'])
    physical=read(WORK/'release-source-review.json')['checks']['physical_pages']
    BASE.mkdir();write(BASE/'state-snapshot.json',state);write(BASE/'status-snapshot.json',view)
    write(BASE/'remaining-operations.json',dict(reader=state['reader'],coverage=groups,
        recorded=view['recorded_proposal_operations'],proposal_operations=view['proposal_operations'],ready=view['ready_proposal_operations'],
        operations=obligations,census=ref(CENSUS,'Every original disposition conserved'),proposal_accepted=False))
    independent=[]
    for lane in ['software','commercial','reuse','llm','manuscript','release','proposal_acceptance']:
        eligible=[n for n in ready if n['lane']==lane]
        if eligible:
            n=eligible[0];independent.append(dict(lane=lane,operation=n['id'],action=n['action'],depends=n['depends'],
                requires_inputs=n['requires_inputs'],output=n['outputs']))
    review=dict(status='pass_for_program_consistency_not_completion',reviewer=dict(name='Codex author/coordinator',kind='author'),
        evidence=[ref(BASE/'state-snapshot.json','Canonical snapshot'),ref(BASE/'remaining-operations.json','All nonpassing obligations'),
            ref(WORK/'working-release.json','Integrated reader'),ref(SPONSOR/'working-release.json','Exact paired sponsor'),
            ref(WORK/'plan-review.json','Reviewed execution'),ref(WORK/'reconciliation-review.json','Census and task-map conservation'),
            ref(WORK/'acquisition-review.json','Preserved public reads and failures'),
            ref(WORK/'next-lane-review.json','Independent Python pinning and inference preflight'),
            ref(WORK/'integrated-progress.json','Completed integration and exact continuation')],
        effective_lane_counts={k:dict(v) for k,v in lanes.items()},independent_next_actions=independent,
        findings=['Proposal scope and effective receipts agree; recorded outcomes are not native or product completion counts.',
            'All 102 software cells, 115 reuse decisions, 22 chapter reviews, 113 originals and four search obligations retain their coverage requirements.',
            'Two originals now support domain-knowledge synthesis; metadata-only ontology evidence remains unread and cannot support technical claims.',
            'Local acquisition failure does not block other papers, independent software/commercial/reuse work or manuscript synthesis.',
            'Independent preflight corrected the inherited CausalPy scope: sharp RD only, not IV; equal-tail plotting quantiles are not generically HDIs.',
            'Public known-law tests distinguish expert reconstruction, edge semantics, causal identification and decision value before costly bank studies.',
            'Q2-Q4 bind the new reader; sponsor pairing follows their completed renewals. Q1/Q5, all repairs and rendered acceptance remain open.',
            'No unattended worker exists; canonical mutations remain sequential and bounded tool output preserves recoverability.'],
        known_routes=['Inspect original bytes at cutoff, pin source versions and finish candidate-specific decisions.',
            'Resolve ontology source access through authorized copies while pursuing other 54 originals and complementary searches.',
            'Acquire raw outputs, independent reference/corpus splits and licenses; run separately scoped public prototypes only after design review.',
            'Reconcile exclusive chapter depth and full coverage for all three repairs; complete rendered review in a fresh image allowance.'],
        unresolved_research=['General hidden-confounder identification and unrestricted graph-to-effect calibration.',
            'Arbitrary persistent dependence and private-state optimal-policy uncertainty.',
            'Universal learner calibration or conversion of LLM confidence to intervention truth.',
            'Bank assignment truth, production reliability and measured economics require later decision-relevant evidence.'],
        global_blocker=None,phase_boundaries_are_stopping_points=False,background_worker_running=False)
    write(BASE/'program-review.json',review)
    write(BASE/'continuation-checkpoint.json',dict(date='2026-10-22',status='reviewed_program_and_integrated_continuation',
        prior_git_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        state=ref(BASE/'state-snapshot.json','Canonical state after integrated continuation'),reader=state['reader'],
        sponsor=ref(SPONSOR/'working-release.json','Paired sponsor'),
        completed=['Recovered clean b5f04843 baseline and passing runtime/master checks.',
            'Executed reviewed three-candidate plan; preserved seven sandbox DNS failures and publisher 403.',
            'Inspected two originals across 56 extracted pages; retained figure-pixel limits and authentic PDF identities.',
            'Reconciled all 117 census rows and fourteen task families;59 inspected/54 unread.',
            'Derived exact graph/observational-equivalence and conditional financial examples.',
            'Integrated connected synthesis, compiled both successors, renewed Q2-Q4 and refreshed every nonpassing obligation.'],
        evidence=[ref(WORK/'review.json','Substantive review'),ref(BASE/'program-review.json','Queue-wide program review'),
            ref(WORK/'next-lane-review.json','Independent Python IV/RD inputs rechecked; actual source pins remain required')],
        remaining=ref(BASE/'remaining-operations.json','Complete nonpassing register'),next_operation=view['next'],next_action=view['next_action'],
        independent_next_actions=independent,global_blocker=None,background_worker_running=False,visual_acceptance=False,proposal_accepted=False))
    current=ROOT/'docs/program/execution/current-program.md';(BASE/'prior-current-program.md').write_bytes(current.read_bytes())
    current.write_text(f'''# Current executable proposal program

Updated 22 October 2026 after the domain-knowledge and causal-graph literature review.
The [queue-wide review](2026-10-22/program-refresh-domain-v1/program-review.json)
binds the current plan, evidence and independent next actions. This is a research
and product proposal; native qualification, bank validation and adoption are later.

Use `python3 tools/run_program_reviews_v2.py status`, `next` and `check`.
The canonical ledger is [state.json](../state.json); the
[proposal scope](../master-program-proposal.md) governs. Earlier numbered masters
remain historical snapshots. Continue eligible work across phase boundaries.

## Current integrated documents

Read the [{state['reader']['pages']:,}-page monograph](../../causal_proposal_domain_knowledge_reviewed_2026-10-22.pdf)
and its [{sponsor['pages']}-page sponsor proposal](../../sponsor_proposal_domain_knowledge_reviewed_2026-10-22.pdf).
The monograph contains {count} audited citation records and {papers} genuine
scholarly PDFs; the sponsor contains {sponsor_count} audited citations and binds
the exact current monograph. Q2-Q4 pass for these bytes. Q1/Q5, all three mandatory
repairs, rendered review and final acceptance remain open.

There are **{view['recorded_proposal_operations']} recorded outcomes of {view['proposal_operations']} proposal operations**,
with **{view['ready_proposal_operations']} ready operations**. Outcomes include
inconclusive findings; they are not completed products or native integrations.

| Area | Pass | Inconclusive | Open | Total |
|---|---:|---:|---:|---:|
| Software coverage | {groups['software'].get('pass',0)} | {groups['software'].get('inconclusive',0)} | {groups['software']['open']} | 102 |
| Reuse decisions | {groups['reuse'].get('pass',0)} | {groups['reuse'].get('inconclusive',0)} | {groups['reuse']['open']} | 115 |
| Chapter reviews | {groups['chapters'].get('pass',0)} | {groups['chapters'].get('inconclusive',0)} | {groups['chapters']['open']} | 22 |

The frontier census is **{inspected} inspected and {unread} unread originals out of 113**,
plus four crosscutting obligations. Fourteen LLM task and twelve integration
reviews have scoped proposal outcomes; they do not establish live-model results
or cross-repository adoption.

## Findings integrated in this continuation

Physical monograph pages {physical[0]}-{physical[1]}, section 45.30, compare Aziz and
Brookhart's statin graph-elicitation study with Lin and colleagues' chronic-pain
knowledge-retrieval preprint. The former's completeness proxy is predictor recall,
not causal-edge truth. The latter uses a cyclic expert reference and the same
document corpus used to build it. Its strongest F1 is 0.745 versus 0.714 for ordinary
retrieval and 0.737 for graph retrieval alone; rankings depend on the query.

Exact authored examples distinguish direct edges from ancestry and show that union
can lower F1 and create a three-cycle. Two Gaussian models have identical observed
laws but intervention effects -1/2 and 0; stipulated costs imply margins USD 30 and -20.
These are mathematical examples, not measured bank effects. The public evaluation
design separates evidence entailment, graph semantics, identification and value.

The ontology article remains unread after publisher 403 and an alternate-location
check. Its failure is local. [Exact omissions and follow-ups](2026-10-22/census-domain-knowledge-v1/omissions-register.json)
retain supplemental outputs, raw code/data, rights, held-out evaluation and visual
review separately. All earlier sources, citation contexts and chapter inputs survive.

## Required standard and remaining gaps

Each banking use must connect the decision and information clock to its target,
assumptions, identification or limits, estimation, uncertainty, diagnostics,
alternatives and monetary consequences. Sources require authentic bytes, identity,
version/date, hash and inspected supporting anchors. Scholarly citations require
real PDFs; the cutoff is 7 October 2026. FinMarketing sets the scholarly standard.
Total length is not acceptance.

MR01 requires 17 areas across six dimensions and 100-150 substantive software pages.
MR02 requires eight developed chapters, fourteen tasks and 96-112 pages. MR03
requires four integration chapters and twelve requirements, with indicative 40-60
pages. Exclusive depth and systematic coverage both matter.

Known routes are primary-source recovery, complementary searches, reasoned reuse,
connected synthesis and public known-law studies. Expensive bank studies follow
demonstrated prototype merit. General latent identification, arbitrary dependence,
private-state optimal-policy uncertainty and universal calibration require narrower
claims or additional information; there is no promised general solution.

## Exact continuation

Controller next: **{view['next']}**. {view['next_action']}

The [remaining-operation register](2026-10-22/program-refresh-domain-v1/remaining-operations.json)
contains every nonpassing obligation and dependency; the
[checkpoint](2026-10-22/program-refresh-domain-v1/continuation-checkpoint.json)
lists independent next actions. Python IV/RD sources have a saved preflight;
commercial observation software and open reuse decisions remain eligible.
The [rechecked Python preflight](2026-10-22/census-domain-knowledge-v1/next-lane-review.json)
corrects an earlier scope ambiguity: CausalPy's inherited review covers sharp RD
only, with equal-tail plotting quantiles; its IV path needs a separate review.

Keep tool output bounded and serialize canonical mutations through completion.
Preserve failures and earlier releases. Checkpoints and Git preservation are not
permission gates. No global blocker or unattended research worker is present.
The inherited six-preview allowance under `/home/ubuntu/AGENTS.md` is exhausted;
rendered acceptance requires a fresh visual session, while research continues.
''')
    run.render(ROOT,state)
    print(json.dumps(dict(reader=state['reader'],sponsor_pages=sponsor['pages'],records=count,papers=papers,
        recorded=view['recorded_proposal_operations'],ready=view['ready_proposal_operations'],remaining=len(obligations),next=view['next'],proposal_accepted=False)))

if __name__=='__main__':main()
