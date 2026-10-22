#!/usr/bin/env python3
"""Preserve a queue-wide refresh and adopt the checkpoint-aware controller."""
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import subprocess

import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run = controller.base
ROOT = run.core.ROOT
PRIOR = ROOT / 'docs/program/execution/2026-10-22/program-refresh-workflow-v1'
PUB = ROOT / 'docs/program/execution/2026-10-22/computation-workflow-reader-v1'
SPONSOR = ROOT / 'docs/program/execution/2026-10-22/sponsor-workflow-v1'
JAVA = ROOT / 'docs/program/execution/2026-10-22/java-iv-rd-preflight-v1'
LMTP = ROOT / 'docs/program/execution/2026-10-22/lmtp-reuse-v1'
read = lambda p: json.loads(p.read_text())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--edition', choices=['v1', 'v2'], default='v1')
    parser.add_argument('--census', default='docs/program/execution/2026-10-22/census-factuality-weighted-v1')
    args = parser.parse_args()
    base = ROOT / f'docs/program/execution/2026-10-23/program-refresh-policy-{args.edition}'
    census = ROOT / args.census
    assert not base.exists(), 'Completed refreshes are immutable; use a successor.'
    state = run.core.read(ROOT, run.core.STATE)
    assert state['execution_runtime']['active'] is None
    publication, sponsor = read(PUB / 'working-release.json'), read(SPONSOR / 'working-release.json')
    for record in [publication, sponsor]:
        verify_bindings(record)
    assert run.same_reader(state['reader'], publication['pdf'])
    assert run.same_reader(state['reader'], sponsor['paired_monograph'])
    view = controller.status(ROOT, state)
    graph, merged, stages, ready, _ = run.queue(ROOT, state)
    results = merged['execution_program']['results']
    previous = {x['id']: x for x in read(PRIOR / 'remaining-operations.json')['operations']}
    obligations, lanes, groups = [], defaultdict(Counter), {}
    for node in graph['nodes']:
        key = node['id']
        if stages[key] != 'proposal_now':
            continue
        result = results.get(key)
        lanes[node['lane']][result['outcome'] if result else 'open'] += 1
        if result and result['outcome'] == 'pass':
            continue
        progress = merged['execution_program']['progress'].get(key, [])
        action = node['action']
        if progress:
            run.core.bound(ROOT, progress[-1])
            note = read(ROOT / progress[-1]['path'])
            run.validate_note(ROOT, note, 'progress')
            action = note['next_action']
        item = dict(id=key, lane=node['lane'], title=node['title'],
            status=result['outcome'] if result else 'open', action=action,
            prerequisites=run.ledger.blockers(merged, node), outputs=node['outputs'],
            evidence=result, requires_inputs=node['requires_inputs'])
        old = previous.get(key, {})
        for field in ['corrected_source_followup', 'source_followup']:
            if field in old:
                run.core.bound(ROOT, old[field])
                item[field] = old[field]
        # Preserve separately reviewed source corrections unless a newer
        # checkpoint supplies the action. Never replace newer durable progress.
        if old.get('corrected_source_followup') and not progress:
            item['action'] = old['action']
        if key == 'SW.CELL.iv_rd_design.Java':
            item['corrected_source_followup'] = ref(JAVA / 'progress.json', 'Partial source review; no native IV/RD qualification')
        obligations.append(item)
    for name, prefix, total in [('software', 'SW.CELL.', 102), ('reuse', 'SW.DECISION.', 115), ('chapters', 'TEXT.REVIEW.', 22)]:
        selected = {k: v for k, v in results.items() if k.startswith(prefix)}
        groups[name] = dict(Counter(v['outcome'] for v in selected.values()), open=total-len(selected), total=total)
        assert sum(v for k, v in groups[name].items() if k != 'total') == total
    assert len(obligations) + sum(v['pass'] for v in lanes.values()) == view['proposal_operations'] == 376
    for key in ['SW.DECISION.inherited_lmtp', 'SW.DECISION.inherited_linearmodels']:
        assert results[key]['outcome'] == 'pass'
        assert key not in {x['id'] for x in obligations}
    dispositions = Counter(x['disposition'] for x in read(census / 'census-register.json')['items'])
    inspected = dispositions['inspected_primary_retained_with_limits']
    unread = dispositions['open_original_not_inspected']
    assert inspected + unread == 113
    by_id = {x['id']: x for x in obligations}
    independent = []
    for lane in ['software', 'commercial', 'reuse', 'llm', 'manuscript', 'release', 'proposal_acceptance']:
        eligible = [x for x in ready if x['lane'] == lane]
        if eligible:
            node = eligible[0]
            independent.append(dict(lane=lane, operation=node['id'],
                action=by_id.get(node['id'], node)['action'], depends=node['depends'],
                requires_inputs=node['requires_inputs'], outputs=node['outputs']))
    base.mkdir(parents=True)
    write(base / 'state-snapshot.json', state)
    write(base / 'status-snapshot.json', view)
    write(base / 'remaining-operations.json', dict(reader=state['reader'], coverage=groups,
        recorded=view['recorded_proposal_operations'], proposal_operations=376,
        ready=view['ready_proposal_operations'], operations=obligations,
        census=ref(census / 'census-register.json', 'Every candidate disposition'), proposal_accepted=False))
    findings = [
        'Every proposal operation and nonpassing obligation reconciled; inconclusive results remain obligations.',
        'Independent lanes retain actual evidence dependencies and no phase boundary is a permission gate.',
        'Checkpoint-aware status now displays the same latest durable action that start resumes; frozen predecessors preserved.',
        'The linearmodels and lmtp decisions are reference-only, integration_allowed=false, capabilities empty.',
        'Java Tetrad inspection establishes a latent measurement-model scope and source-level conversion concerns, not generic IV/RD support or an executed native failure.',
        'The lmtp source review distinguishes outer fold identity, effective bounds, risk-shift versus odds-tilt policies and uninspected downstream variance semantics.',
        'New reference/source/example findings are editorial deltas; the current 1240-page reader and exact 50-page sponsor remain the current paired release.',
        f'Census: {inspected}/113 originals inspected, {unread} unread and four crosscutting searches open.',
        'Q2-Q4 pass for the current reader; Q1/Q5, mandatory repairs, rendered visual review and final proposal acceptance remain open.',
        'No live agent superiority, bank-data validation, native adoption, production reliability or institutional acceptance follows from these reviews.']
    evidence = [ref(base / 'state-snapshot.json', 'Canonical state at refresh'),
        ref(base / 'remaining-operations.json', 'All nonpassing obligations'),
        ref(PUB / 'working-release.json', 'Current reader'), ref(SPONSOR / 'working-release.json', 'Exact paired sponsor'),
        ref(JAVA / 'review.json', 'Scoped Java source findings'), ref(JAVA / 'progress.json', 'Exact remaining Java actions'),
        ref(LMTP / 'review.json', 'Reference-only decision and source limits'),
        ref(LMTP / 'tree-identity-review.json', 'Preserved failed tree assertion and authenticated repair'),
        ref(ROOT / 'tools/run_program_checkpoint_v3.py', 'Successor controller'),
        ref(ROOT / 'tests/test_run_program_checkpoint_v3.py', 'Resume agreement and altered checkpoint rejection tests'),
        ref(census / 'census-register.json', 'Conserved candidate accounting'), ref(Path(__file__), 'Exact refresh generator')]
    write(base / 'program-review.json', dict(status='pass_for_program_consistency_not_completion',
        reviewer=dict(name='Codex author/coordinator', kind='author'), evidence=evidence,
        effective_lane_counts={k: dict(v) for k, v in lanes.items()}, findings=findings,
        independent_next_actions=independent, global_blocker=None,
        phase_boundaries_are_stopping_points=False, background_worker_running=False))
    write(base / 'continuation-checkpoint.json', dict(date='2026-10-23',
        prior_git_commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        reader=state['reader'], sponsor=ref(SPONSOR / 'working-release.json', 'Paired sponsor'),
        completed=findings[2:8], remaining=ref(base / 'remaining-operations.json', 'Exact remaining work'),
        next_operation=view['next'], next_action=view['next_action'], independent_next_actions=independent,
        visual_acceptance=False, proposal_accepted=False, global_blocker=None, background_worker_running=False))
    current = ROOT / 'docs/program/execution/current-program.md'
    (base / 'prior-current-program.md').write_bytes(current.read_bytes())
    link = str(base.relative_to(ROOT / 'docs/program/execution'))
    rows = '\n'.join(f"| {label} | {groups[key].get('pass', 0)} | {groups[key].get('inconclusive', 0)} | {groups[key]['open']} | {groups[key]['total']} |"
        for key, label in [('software', 'Software coverage'), ('reuse', 'Reuse decisions'), ('chapters', 'Chapter reviews')])
    lane_text = '\n'.join(f"- **{x['lane']}: {x['operation']}**. {x['action']}" for x in independent)
    current.write_text(f'''# Current executable proposal program

Updated 23 October 2026. The [queue-wide review]({link}/program-review.json)
reconciles all 376 proposal operations and every nonpassing obligation. The goal is
a scholarly research and product proposal supported by public/generated evidence
that can justify costly bank experiments. Bank qualification and adoption are later work.

Use `python3 tools/run_program_checkpoint_v3.py status`, `next` and `check`.
This successor repairs stale idle resume guidance and preserves prior controllers.
The [canonical ledger](../state.json) and [proposal scope](../master-program-proposal.md)
govern execution. Continue eligible work across phase boundaries.

## Current integrated documents

The current pair is the [1,240-page monograph](../../causal_proposal_workflow_reviewed_2026-10-22.pdf)
and [50-page sponsor proposal](../../sponsor_proposal_workflow_reviewed_2026-10-22.pdf).
Their audits retain 932 and 305 citations respectively; the reader includes 221
genuine scholarly PDFs. The sponsor binds the exact reader bytes. Q2-Q4 pass for
this pair. Q1/Q5, the mandatory repairs, fresh visual review and final acceptance remain open.

The paired release captured 189 recorded outcomes. The live queue now has
**{view['recorded_proposal_operations']} recorded outcomes of 376**, **{view['ready_proposal_operations']} ready operations**,
and **{len(obligations)} nonpassing obligations**. Recorded inconclusive results are unfinished.

| Area | Pass | Inconclusive | Open | Total |
|---|---:|---:|---:|---:|
{rows}

The frontier census has **{inspected} inspected and {unread} unread originals out of 113**,
plus four crosscutting searches. Fourteen LLM-task and twelve integration reviews
have scoped proposal outcomes; these do not establish live-model superiority or adoption.

## Findings awaiting substantive editorial integration

The new linearmodels and lmtp reuse decisions are reference-only with
**integration_allowed=false** and no native capability. Tetrad's inspected `Tsls`
implementation addresses supplied pure latent measurement models. Its axis,
normalization, rank and covariance concerns need concrete caller/backend checks.
The partial Java review leaves generic IV/RD coverage open.

The lmtp review authenticates seventeen source files and distinguishes intended
cluster identities from the outer-fold field mismatch. Documented and effective
bound settings differ; inspected estimators do not establish execution with the
documented erroneous default. Variance/contrast semantics delegated to `ife`
remain uninspected. The AGPL license is authentic; process separation alone does
not settle integration rights. In an exact authored two-period contact example,
natural, risk-shift and odds-tilt expected net values are 7.36, 18.24 and 107/9 USD.
These are stipulated mathematical values, not package execution or bank returns.

These findings, their conversion requirements and any new census findings are
explicit editorial deltas for the next substantive paired release. The PDFs above
do not yet integrate these deltas. Do not rebuild the full reader only for a process count.

## Required standard and remaining gaps

Each banking use must connect decision, information clock, population and target,
assumptions, identification or limits, estimation, uncertainty, diagnostics,
substantive alternatives and monetary consequences. Each cited work needs authentic
local bytes, identity, version/date, SHA-256, inspected primary anchors and supported
claims. Scholarly works need genuine PDFs. The cutoff is 7 October 2026; later
observations remain labeled. FinMarketing sets connected scholarly depth.

MR01 covers seventeen areas across six language/commercial dimensions, reasoned
reuse choices and 100-150 substantive software pages. MR02 requires eight chapters,
fourteen tasks and 96-112 substantive LLM/agent pages. MR03 requires four integration
chapters and twelve requirements, with indicative 40-60 pages. Exclusive depth and
complete coverage both matter. L1 and L6 remain inconclusive.

The [remaining register]({link}/remaining-operations.json) retains all {len(obligations)}
nonpassing obligations, evidence, actual prerequisites and exact actions. Known
routes are primary-source inspection, complementary searches, cutoff-edition
comparisons, reasoned reuse, public/generated studies and chapter/release reconciliation.
Commercial source omissions and native qualification are local obligations.

No universal repair is established for unrestricted latent identification,
arbitrary persistent dependence, hidden-state optimal-policy uncertainty or arbitrary
learner remainders. Use justified restrictions, explicit negative results or new
information. No general conversion of LLM, vendor or linkage scores into causal
truth is established. Bank assignment truth, independent institutional acceptance,
target-platform reliability and actual bank economics require later external evidence.

## Exact continuation

Controller next: **{view['next']}**. {view['next_action']}

Independent eligible lanes retain only their actual prerequisites:

{lane_text}

The [Java checkpoint](2026-10-22/java-iv-rd-preflight-v1/progress.json) and
[lmtp decision](2026-10-22/lmtp-reuse-v1/review.json) preserve source findings and
remaining work. Existing commercial and Python checkpoints identify acquired
sources; do not repeat completed source inspection or delivered integration.

Await actual completion of canonical mutations before dependent transitions.
Preserve failed attempts and exact successor repairs. Checkpoints preserve recovery
and do not create permission gates. No global blocker or unattended worker exists.
The six-preview session allowance in `/home/ubuntu/AGENTS.md` is exhausted; fresh
visual review is still required for acceptance. Source and manuscript work remain eligible.
''')
    navigation = ROOT / 'docs/README.md'
    (base / 'prior-docs-readme.md').write_bytes(navigation.read_bytes())
    navigation.write_text(navigation.read_text().replace('tools/run_program_reviews_v2.py', 'tools/run_program_checkpoint_v3.py'))
    controller.render(ROOT, state)
    verify_bindings(read(base / 'program-review.json'))
    print(json.dumps(dict(refresh=str(base.relative_to(ROOT)), recorded=view['recorded_proposal_operations'],
        ready=view['ready_proposal_operations'], remaining=len(obligations), census=[inspected, unread], next=view['next'])))


if __name__ == '__main__':
    main()
