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
BASE = DAY / 'program-refresh-recovery-v1'
PRIOR = DAY / 'program-refresh-detailed-workflow-v2'
PUB = DAY / 'ltmle-reader-v2'
SPONSOR = DAY / 'sponsor-ltmle-v1'
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
    completed = ['SW.COMP.iv_rd_design', 'SW.COMP.computation_workflow', 'SW.COMP.networks_interference',
        'SW.COMP.longitudinal_survival', 'SW.COMP.policies_offpolicy', 'SW.DECISION.inherited_ltmle']
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
    assert len(comparison_queue) == 12 and len(design_queue) == 4
    BASE.mkdir()
    write(BASE / 'state-snapshot.json', state)
    write(BASE / 'status-snapshot.json', view)
    write(BASE / 'remaining-operations.json', dict(reader=state['reader'], recorded=view['recorded_proposal_operations'],
        proposal_operations=376, ready=view['ready_proposal_operations'], coverage=groups, operations=remaining,
        census=ref(census_path, '113 candidate dispositions'), proposal_accepted=False))
    failed = DAY / 'sponsor-ltmle-failed-prepare-1'
    write(BASE / 'recovery-review.json', dict(status='recovered_with_preserved_failures',
        findings=['Reader publication and Q2-Q4 renewal finished; no orphan canonical process remains.',
            'Initial sponsor preparation compared a release-manifest identity with the PDF identity; repaired before output creation.',
            'Second preparation failed prior-citation preservation; its three draft artifacts are retained unchanged.',
            'The sponsor successor preserves all 323 earlier identities, adds four, and binds the actual 1251-page reader.',
            'Prepublication source review corrected fallback-variance wording and supplied the example probability/cost definitions.',
            'Sandbox git status attempted an LFS temporary write under read-only .git; elevated authorized inspection was requested.'],
        evidence=[ref(p, 'Preserved unsuccessful sponsor preparation') for p in sorted(failed.glob('*.json'))] +
            [ref(failed / 'proposal.md', 'Preserved unsuccessful draft'), ref(SPONSOR / 'author-review.json', 'Successful corrected review')],
        visual_acceptance=False, final_acceptance=False))
    evidence = [ref(BASE / n, 'Recovery and complete queue evidence') for n in ['state-snapshot.json', 'remaining-operations.json', 'recovery-review.json']]
    evidence += [ref(PRIOR / 'program-review.json', 'Previous complete queue review'), ref(PUB / 'working-release.json', 'Exact reader'),
        ref(SPONSOR / 'working-release.json', 'Paired sponsor'), ref(census_path, 'All 113 originals'),
        ref(DAY / 'ready-obligations-v1/plan-review-v2.json', 'Reviewed continuous plan'), ref(Path(__file__), 'Recovery reconciliation')]
    evidence += [results[k] for k in completed]
    review = dict(status='pass_for_consistency_not_completion', reviewer=dict(name='Codex author/coordinator', kind='author'),
        evidence=evidence, effective_lane_counts={k: dict(v) for k, v in lanes.items()},
        findings=['All 376 proposal operations and every nonpassing obligation are accounted for; inconclusive remains unfinished.',
            'The reader preserves 946 previous citation records and adds two; the sponsor preserves 323 and adds four.',
            'Ltmle is a justified reference-only decision, with integration_allowed=false and no admitted capability.',
            'Five individual scientific comparisons have passing source/arithmetic receipts; software source coverage remains incomplete.',
            'Independent comparisons, language designs, technical-source acquisition and census work remain eligible.',
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
        next_action='Continue individual ready scientific comparisons, then language designs; source acquisition and census remain independent.',
        visual_acceptance=False, proposal_accepted=False, global_blocker=None, background_worker_running=False))
    current = ROOT / 'docs/program/execution/current-program.md'
    (BASE / 'prior-current-program.md').write_bytes(current.read_bytes())
    rows = '\n'.join(f"| {k} | {v.get('pass',0)} | {v.get('inconclusive',0)} | {v['open']} | {v['total']} |" for k,v in groups.items())
    current.write_text(f'''# Current executable proposal program

Updated 23 October 2026 after crash recovery. The [complete queue review](2026-10-23/program-refresh-recovery-v1/program-review.json)
and [continuous execution plan](2026-10-23/ready-obligations-v1/plan.md) govern the remaining work.
This is a scholarly product proposal using public/generated evidence to justify later expensive bank experiments.

Use `python3 tools/run_program_checkpoint_v3.py status`, `next` and `check`.
The [canonical ledger](../state.json) preserves outcomes and actual evidence dependencies.
Independent obligations continue across checkpoints and phase boundaries.

## Current integrated documents

The current pair is the [1,251-page monograph](../../causal_proposal_longitudinal_regimes_reviewed_v2_2026-10-23.pdf)
and [54-page sponsor proposal](../../sponsor_proposal_longitudinal_regimes_reviewed_2026-10-23.pdf).
Their audits retain 948 and 327 citations; the reader includes 223 genuine scholarly PDFs.
The sponsor binds exact reader bytes. Q2-Q4 pass; Q1/Q5, the three mandatory repairs,
fresh rendered visual review and final proposal acceptance remain open.

There are **{view['recorded_proposal_operations']} recorded outcomes of 376**, **{view['ready_proposal_operations']} ready operations**,
and **{len(remaining)} nonpassing obligations**. Inconclusive outcomes remain unfinished.

| Area | Pass | Inconclusive | Open | Total |
|---|---:|---:|---:|---:|
{rows}

The frontier census retains 63 inspected and 50 unread originals of 113, plus four crosscutting searches.
Fourteen LLM task and twelve integration reviews have scoped proposal outcomes; those do not establish live-model superiority or adoption.

## Recovered scientific work

The ltmle review authenticates 11 originals and 27 inspected anchors at the pinned 1.3-0 source revision.
It retains a reference-only choice, with `integration_allowed=false`. The source distinguishes effective IC variance,
household aggregation, cumulative probability floors, warnings and paired covariance from requested options.
Exact risks 13/60,17/100,7/75 and net values 0,130/3,340/3 USD are stipulated mathematical references.
Their censoring and covariance checks are integrated with all previous source records and content preserved.

Five scientific comparisons are now recorded: IV/RD, computation/workflow, networks/interference,
longitudinal/survival and policies/off-policy. Each uses inspected source behavior and individual exact examples.
These syntheses reconcile arguments already developed in the monograph; they do not close wider source coverage or native trials.

The earlier Dataiku, lmtp, linearmodels, contextual-causality and multimodal findings remain preserved.
The new [recovery review](2026-10-23/program-refresh-recovery-v1/recovery-review.json) records failed preparations and repairs.
Frozen historical master files, research chapters and previous PDFs remain unchanged.

## Exact continuation

Complete the 12 remaining individual comparisons: {', '.join(x.removeprefix('SW.COMP.') for x in comparison_queue)}.
Then complete the four language-specific trial designs with independent oracles, adverse regimes,
threshold rationale, exact sample-size/screen power and fixed stopping. A design is not an executed qualification result.

The C++ IV/RD lane has authenticated rddsigma and academic system-identification candidate identities and trees;
technical source and license inspection remain. Do not reacquire completed metadata/tree requests.
The commercial lane still needs authentic cutoff technical bytes and SAS Viya/Domino/Posit comparison.
Continue individual reuse reviews and the 50 unread census originals/four searches independently.
All source-specific follow-ups and actual prerequisites appear in the [remaining register](2026-10-23/program-refresh-recovery-v1/remaining-operations.json).

Unknown universal repairs remain open: unrestricted latent identification, arbitrary persistent dependence,
hidden-state optimal-policy uncertainty and arbitrary learner remainders need justified restrictions or new information.
Bank truth, independent institutional review, platform reliability and actual bank economics are later external obligations.

The six-image allowance in `/home/ubuntu/AGENTS.md` is exhausted in this session; this blocks only further visual acceptance.
There is no global blocker and no unattended research worker. Continue eligible work, preserve/check/commit changes,
and resume from the exact checkpoint after a disconnect.
''')
    print(json.dumps(dict(recorded=view['recorded_proposal_operations'], ready=view['ready_proposal_operations'],
        nonpassing=len(remaining), comparison_queue=comparison_queue, design_queue=design_queue, refreshed=str(BASE.relative_to(ROOT)))))


if __name__ == '__main__': main()
