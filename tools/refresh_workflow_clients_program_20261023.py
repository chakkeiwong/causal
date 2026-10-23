#!/usr/bin/env python3
"""Preserve a complete queue reconciliation after crash recovery and publication."""
from collections import Counter, defaultdict
import json
from pathlib import Path
import subprocess
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run = controller.base
ROOT = run.core.ROOT
DAY = ROOT / 'docs/program/execution/2026-10-23'
BASE = DAY / 'program-refresh-workflow-clients-v1'
PRIOR = DAY / 'program-refresh-recovery-v1'
PUB = DAY / 'workflow-clients-reader-v2'
SPONSOR = DAY / 'sponsor-workflow-clients-v1'
read = lambda p: json.loads(p.read_text())


def main():
    assert not BASE.exists()
    state = run.core.read(ROOT, run.core.STATE)
    assert state['execution_runtime']['active'] is None
    view = controller.status(ROOT, state)
    graph, merged, stages, ready, _ = run.queue(ROOT, state)
    results = merged['execution_program']['results']
    pub, sponsor, previous = [read(p / n) for p, n in [(PUB, 'working-release.json'),
        (SPONSOR, 'working-release.json'), (PRIOR, 'remaining-operations.json')]]
    for item in [pub, sponsor, read(PRIOR / 'program-review.json')]: verify_bindings(item)
    assert run.same_reader(state['reader'], pub['pdf']) and run.same_reader(state['reader'], sponsor['paired_monograph'])
    assert {q['id']: q['status'] for q in view['proposal_gaps']} == dict(Q1='open', Q2='pass', Q3='pass', Q4='pass', Q5='open')
    prior = {n['id']: n for n in previous['operations']}
    remaining, lanes = [], defaultdict(Counter)
    for node in graph['nodes']:
        key = node['id']
        if stages[key] != 'proposal_now': continue
        result = results.get(key)
        outcome = result['outcome'] if result else 'open'
        lanes[node['lane']][outcome] += 1
        if outcome == 'pass': continue
        old = prior.get(key, {})
        item = dict(id=key, lane=node['lane'], title=node['title'], status=outcome,
            action=old.get('action', node['action']), prerequisites=run.ledger.blockers(merged, node),
            outputs=node['outputs'], evidence=result, requires_inputs=node['requires_inputs'])
        progress = merged['execution_program']['progress'].get(key, [])
        if progress:
            run.core.bound(ROOT, progress[-1])
            note = read(ROOT / progress[-1]['path'])
            run.validate_note(ROOT, note, 'progress')
            item.update(action=note['next_action'], action_checkpoint=progress[-1])
        for field in ['corrected_source_followup', 'source_followup']:
            if field in old:
                run.core.bound(ROOT, old[field])
                item[field] = old[field]
        remaining.append(item)
    assert len(remaining) + sum(v['pass'] for v in lanes.values()) == view['proposal_operations'] == 376
    groups = {}
    for group, prefix, total in [('software', 'SW.CELL.', 102), ('reuse', 'SW.DECISION.', 115), ('chapters', 'TEXT.REVIEW.', 22)]:
        selected = [v for k, v in results.items() if k.startswith(prefix)]
        groups[group] = dict(Counter(v['outcome'] for v in selected), open=total-len(selected), total=total)
    completed = sorted(k for k,v in results.items() if (k.startswith('SW.COMP.') or k.startswith('SW.DESIGN.')) and v['outcome']=='pass') + ['SW.DECISION.inherited_notears','SW.DECISION.seed_061']
    assert all(results[k]['outcome'] == 'pass' for k in completed)
    census_path = DAY / 'census-context-conflict-v1/census-register.json'
    census = Counter(x['disposition'] for x in read(census_path)['items'])
    assert census['inspected_primary_retained_with_limits'] == 63 and census['open_original_not_inspected'] == 50
    by_id = {x['id']: x for x in remaining}
    independent = []
    for lane in ['software', 'commercial', 'reuse', 'llm', 'manuscript', 'release', 'proposal_acceptance']:
        selected = [n for n in ready if n['lane'] == lane]
        if selected:
            n = selected[0]
            independent.append(dict(lane=lane, operation=n['id'], action=by_id[n['id']]['action'],
                depends=n['depends'], requires_inputs=n['requires_inputs']))
    comparison_queue = [n['id'] for n in ready if n['id'].startswith('SW.COMP.')]
    design_queue = [n['id'] for n in ready if n['id'].startswith('SW.DESIGN.')]
    assert not comparison_queue and not design_queue
    BASE.mkdir()
    write(BASE / 'state-snapshot.json', state)
    write(BASE / 'status-snapshot.json', view)
    write(BASE / 'remaining-operations.json', dict(reader=state['reader'], recorded=view['recorded_proposal_operations'],
        proposal_operations=376, ready=view['ready_proposal_operations'], coverage=groups, operations=remaining,
        census=ref(census_path, '113 candidate dispositions'), proposal_accepted=False))
    source = DAY / 'commercial-workflow-recovery-v1'
    write(BASE / 'recovery-review.json', dict(status='recovered_with_preserved_failures',
        findings=['Pending commercial start and progress yield completed; no unconsumed canonical transition remains.',
            'The saved collector manifest was restored after the completed acquisition.',
            'A failed top-level input marker preparation was preserved; the successor resolves the existing detailed-workflow input.',
            'A rendered apostrophe mismatch was corrected in the text-anchor checker, without changing the scientific argument.',
            'All source inspection is static; no downloaded client implementation or licensed server was run.'],
        evidence=[ref(source / n,'Preserved recovery record') for n in ['crash-continuation-plan.md','preparation-failure.json','review-anchor-failure.json','failed-build.log','review.json']],
        visual_acceptance=False, final_acceptance=False))
    evidence = [ref(BASE / n, 'Recovery and complete queue evidence') for n in ['state-snapshot.json', 'remaining-operations.json', 'recovery-review.json']]
    evidence += [ref(PRIOR / 'program-review.json', 'Previous complete queue review'), ref(PUB / 'working-release.json', 'Exact reader'),
        ref(SPONSOR / 'working-release.json', 'Paired sponsor'), ref(census_path, 'All 113 originals'),
        ref(DAY / 'ready-obligations-v1/plan-review-v2.json', 'Reviewed continuous plan'), ref(Path(__file__), 'Recovery reconciliation')]
    evidence += [results[k] for k in completed]
    review = dict(status='pass_for_consistency_not_completion', reviewer=dict(name='Codex author/coordinator', kind='author'),
        evidence=evidence, effective_lane_counts={k: dict(v) for k, v in lanes.items()},
        findings=['All 376 proposal operations and every nonpassing obligation are accounted for; inconclusive remains unfinished.',
            'The reader preserves 950 previous citation records and adds five; the sponsor preserves 331 and adds seven.',
            'NOTEARS remains reference-only; gfoRmula alias is reconciled without granting integration capability.',
            'All seventeen scientific comparisons and four prospective language trial designs are recorded; source coverage and native qualification remain incomplete.',
            'Technical-source follow-ups, individual reuse decisions and fifty unread census originals remain independently eligible.',
            'Q2-Q4 pass for actual reader bytes; Q1/Q5, mandatory repairs and final visual acceptance remain open.'],
        completed_operations=completed, independent_next_actions=independent,
        comparison_queue=comparison_queue, design_queue=design_queue,
        global_blocker=None, phase_boundaries_are_stopping_points=False, background_worker_running=False)
    verify_bindings(review)
    write(BASE / 'program-review.json', review)
    write(BASE / 'continuation-checkpoint.json', dict(reader=state['reader'], sponsor=sponsor['pdf'],
        prior_git_commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
        remaining=ref(BASE / 'remaining-operations.json', 'Exact remaining actions'),
        comparison_queue=comparison_queue, design_queue=design_queue, independent_next_actions=independent,
        next_action=view['next_action'],
        visual_acceptance=False, proposal_accepted=False, global_blocker=None, background_worker_running=False))
    current = ROOT / 'docs/program/execution/current-program.md'
    (BASE / 'prior-current-program.md').write_bytes(current.read_bytes())
    rows = '\n'.join(f"| {k} | {v.get('pass',0)} | {v.get('inconclusive',0)} | {v['open']} | {v['total']} |" for k,v in groups.items())
    current.write_text(f"""# Current executable proposal program

Updated 23 October 2026 after crash recovery and commercial-client integration.
The [complete queue review](2026-10-23/program-refresh-workflow-clients-v1/program-review.json)
and [remaining-operation register](2026-10-23/program-refresh-workflow-clients-v1/remaining-operations.json)
cover all 376 proposal obligations. The canonical state and controller are authoritative;
the older numbered master programs are preserved historical contracts.

This is a scholarly product proposal using public/generated evidence to justify later expensive bank experiments.
Use python3 tools/run_program_checkpoint_v3.py status, next and check.
Continue independent eligible work across phase boundaries. The controller preserves and selects work;
it is not an unattended research worker.

## Current integrated documents

The current pair is the [{pub['pages']:,}-page monograph](../../causal_proposal_workflow_clients_reviewed_2026-10-23.pdf)
and [{sponsor['pages']}-page sponsor](../../sponsor_proposal_workflow_clients_reviewed_2026-10-23.pdf).
There are 955 audited monograph citations, 223 genuine scholarly PDFs and 338 sponsor citations.
All 950 predecessor citation identities/contexts and 288 compiled content inputs are preserved.
The sponsor binds exact reader bytes. Q2-Q4 pass for this reader; Q1/Q5, mandatory repair rollups,
fresh visual review and final proposal acceptance remain open.

There are **{view['recorded_proposal_operations']} recorded outcomes of {view['proposal_operations']}**,
**{view['ready_proposal_operations']} ready operations** and **{len(remaining)} nonpassing obligations**.
Recorded outcomes include inconclusive results; they are not all completed or qualified capabilities.

| Area | Pass | Inconclusive | Open | Total |
|---|---:|---:|---:|---:|
{rows}

## Completed work recovered and continued

All seventeen individual software-family comparisons and four language-specific prospective trial designs
are recorded. The C++ IV/RD source review is recorded with its actual limits. These are not executed native trials.
Original NOTEARS has a source-grounded reference-only decision; the gfoRmula alias is reconciled.
Neither grants native integration or bank capability.

The commercial workflow continuation authenticates 23 source blobs and inspects explicit technical spans in 14.
Four profiles cover SAS sasctl, Domino Python, Posit connectapi and Posit Launcher Go SDK.
The monograph develops terminal states, original-code restart, task and job identities, clocks,
observation deadlines, state reconciliation and retry costs. Stipulated revision values are USD 10 and 20;
one useful gain with one or two charged attempts gives USD 5 and -2. These are exact authored examples.
The entire commercial cell remains open: detailed client evidence does not establish a licensed server,
whole-market coverage, accepted rights/prices or native qualification.

The frontier census remains 63 inspected and 50 unread originals of 113, plus four crosscutting searches.
Fourteen LLM task and twelve integration reviews have scoped outcomes; these do not prove live-model superiority.

## Remaining gaps and execution routes

1. Complete source coverage and individual reuse dispositions using genuine cutoff originals and explicit
   adoption/integration/port/reference/reject reasoning. Preserve source-specific negative or inaccessible findings.
2. Finish the fifty unread census originals and four searches with inspected methods, assumptions, adverse
   results and limitations. Do not treat abstracts, package function counts or marketing as qualification.
3. Complete the commercial temporal/API gaps: exact Dataiku cutoff bytes; SAS REST/service delegates;
   Domino supported terminal-state schema; Posit client/server and scheduler profiles. Keep rights/pricing separate.
4. Execute eligible registered public/synthetic adapter trials when their actual environments and prerequisites
   exist. Designs are already prepared; native trial results cannot be replaced by more design documents.
5. Complete chapter-depth/coverage rollups, exact-document Q1/Q5 and the final publication checks. The inherited
   six-image allowance is exhausted, so further rendered visual acceptance needs a fresh session; this blocks
   only visual review and final visual sign-off.

Unknown universal repairs remain open: unrestricted latent identification, arbitrary persistent dependence,
hidden-state optimal-policy uncertainty and arbitrary learner remainders need justified restrictions or extra
information. Authentic bank truth, independent institutional acceptance, target-platform reliability and actual
bank economics are later external work, separate from completing this proposal.

## Exact continuation

Next: {view['next']}. {view['next_action']}

Source-specific follow-ups, actual prerequisites and independent alternatives are preserved in the complete
remaining register. No phase boundary or one unavailable source is a global blocker. Resume the pending
operation after disconnect, consume its result before another canonical mutation, keep tool output bounded,
preserve failures and verified successors, and commit/push durable work.
""")
    print(json.dumps(dict(recorded=view['recorded_proposal_operations'], ready=view['ready_proposal_operations'],
        nonpassing=len(remaining), comparison_queue=comparison_queue, design_queue=design_queue, refreshed=str(BASE.relative_to(ROOT)))))


if __name__ == '__main__': main()
