#!/usr/bin/env python3
"""Reconcile live proposal guidance with exact paired releases and all obligations."""
from collections import Counter, defaultdict
import json
from pathlib import Path
import subprocess

import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run = extension.base
ROOT = run.core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-22/program-refresh-factuality-targets-v1'
PRIOR = ROOT / 'docs/program/execution/2026-10-22/program-refresh-observations-v1'
PUB = ROOT / 'docs/program/execution/2026-10-22/factuality-weighted-reader-v1/publication-v2'
SPONSOR = ROOT / 'docs/program/execution/2026-10-22/sponsor-factuality-targets-v1'
CENSUS = ROOT / 'docs/program/execution/2026-10-22/census-factuality-weighted-v1'
HD = ROOT / 'docs/program/execution/2026-10-22/honestdid-reuse-v1'
IV = ROOT / 'docs/program/execution/2026-10-22/python-iv-kernels-v1'
read = lambda p: json.loads(p.read_text())


def main():
    assert not BASE.exists(), 'Preserve completed refreshes; create a successor.'
    state = run.core.read(ROOT, run.core.STATE)
    assert state['execution_runtime']['active'] is None
    publication = read(PUB / 'working-release.json')
    sponsor = read(SPONSOR / 'working-release.json')
    for record in [publication, sponsor]:
        verify_bindings(record)
    assert run.same_reader(state['reader'], publication['pdf'])
    assert run.same_reader(state['reader'], sponsor['paired_monograph'])
    view = run.status(ROOT, state)
    graph, merged, stages, ready, _ = run.queue(ROOT, state)
    assert {q['id']: q['status'] for q in view['proposal_gaps']} == dict(
        Q1='open', Q2='pass', Q3='pass', Q4='pass', Q5='open')
    results = merged['execution_program']['results']
    previous = {r['id']: r for r in read(PRIOR / 'remaining-operations.json')['operations']}
    obligations, groups, lanes = [], {}, defaultdict(Counter)
    for node in graph['nodes']:
        identifier = node['id']
        if stages[identifier] != 'proposal_now':
            continue
        result = results.get(identifier)
        lanes[node['lane']][result['outcome'] if result else 'open'] += 1
        if result and result['outcome'] == 'pass':
            continue
        progress = merged['execution_program']['progress'].get(identifier, [])
        action = read(ROOT / progress[-1]['path'])['next_action'] if progress else node['action']
        item = dict(id=identifier, lane=node['lane'], title=node['title'],
            status=result['outcome'] if result else 'open', action=action,
            prerequisites=run.ledger.blockers(merged, node), outputs=node['outputs'],
            evidence=result, requires_inputs=node['requires_inputs'])
        if identifier in previous:
            for key in ['corrected_source_followup', 'source_followup']:
                if key in previous[identifier]:
                    item[key] = previous[identifier][key]
            # These earlier corrections still apply. Census uses its latest
            # integrated progress, never the obsolete prior refresh action.
            if identifier in ['SW.CELL.iv_rd_design.R',
                    'SW.CELL.observations_data.commercial', 'SW.COMM.observations_data']:
                item['action'] = previous[identifier]['action']
        if identifier == 'SW.CELL.iv_rd_design.Python':
            item['corrected_source_followup'] = ref(IV / 'review.json',
                'Pinned fit/covariance/diagnostic kernels inspected; remaining coverage explicit')
            item['action'] = read(IV / 'review.json')['next_action']
        obligations.append(item)
    for name, prefix, total in [('software', 'SW.CELL.', 102),
            ('reuse', 'SW.DECISION.', 115), ('chapters', 'TEXT.REVIEW.', 22)]:
        selected = {k: v for k, v in results.items() if k.startswith(prefix)}
        groups[name] = dict(Counter(v['outcome'] for v in selected.values()),
            open=total - len(selected), total=total)
        assert sum(v for k, v in groups[name].items() if k != 'total') == total
    assert 'SW.DECISION.inherited_honestdid' not in {r['id'] for r in obligations}
    assert len(obligations) + sum(
        v['pass'] for v in lanes.values()) == view['proposal_operations'] == 376
    dispositions = Counter(x['disposition'] for x in read(CENSUS / 'census-register.json')['items'])
    inspected = dispositions['inspected_primary_retained_with_limits']
    unread = dispositions['open_original_not_inspected']
    assert (inspected, unread) == (61, 52)
    count = len(read(PUB / 'reader/source-audit.json')['sources'])
    papers = read(PUB / 'traceability-review.json')['scholarly_pdfs']
    sponsor_count = len(read(SPONSOR / 'source-audit.json')['sources'])
    assert (count, papers) == (925, 221)
    sections = read(PUB / 'release-source-review.json')['checks']['sections']
    independent = []
    by_id = {r['id']: r for r in obligations}
    for lane in ['software', 'commercial', 'reuse', 'llm', 'manuscript',
            'release', 'proposal_acceptance']:
        eligible = [n for n in ready if n['lane'] == lane]
        if eligible:
            node = eligible[0]
            independent.append(dict(lane=lane, operation=node['id'],
                action=by_id.get(node['id'], node)['action'], depends=node['depends'],
                requires_inputs=node['requires_inputs'], outputs=node['outputs']))
    BASE.mkdir()
    write(BASE / 'state-snapshot.json', state)
    write(BASE / 'status-snapshot.json', view)
    write(BASE / 'remaining-operations.json', dict(reader=state['reader'], coverage=groups,
        recorded=view['recorded_proposal_operations'], proposal_operations=view['proposal_operations'],
        ready=view['ready_proposal_operations'], operations=obligations,
        census=ref(CENSUS / 'census-register.json', 'Every original disposition'),
        proposal_accepted=False))
    evidence = [ref(BASE / 'state-snapshot.json', 'Canonical snapshot'),
        ref(BASE / 'remaining-operations.json', 'Every nonpassing obligation and dependency'),
        ref(PUB / 'working-release.json', 'Current integrated reader'),
        ref(SPONSOR / 'working-release.json', 'Exact paired sponsor'),
        ref(PUB / 'release-source-review.json', '922 prior citation records and 278 inputs preserved'),
        ref(PUB / 'schema-failure.json', 'Preserved first-build schema failure')
        if (PUB / 'schema-failure.json').exists() else
        ref(PUB.parent / 'schema-failure.json', 'Preserved first-build schema failure'),
        ref(PUB / 'text-review-attempt-1.json', 'Preserved wrapped-text verifier failure'),
        ref(CENSUS / 'review.json', 'Two selected pre-cutoff primary originals inspected'),
        ref(CENSUS / 'integrated-progress.json', 'Integration complete; census remains partial'),
        ref(HD / 'review.json', 'Reference-only HonestDiD decision'),
        ref(IV / 'review.json', 'Inspected Python fit/covariance/diagnostic kernels'),
        ref(Path(__file__), 'Exact queue reconciliation')]
    known_routes = [
        'Inspect the 52 unread originals and complete four crosscutting searches, keeping edition and coverage limits.',
        'Complete each area/language commercial and open-source comparison and reasoned adoption/port/integration/rejection decision.',
        'Recover Python RD/CausalPy IV technical originals and inspect remaining numerical delegates; do not reacquire already inspected IV kernels.',
        'Use matched public data and generated known-law cases to justify prototype merit before expensive bank studies.',
        'Reconcile exclusive chapter depth with coverage and finish exact paired-document coherence and fresh rendered review.']
    unresolved = [
        'General identification with latent confounding or observationally equivalent causal explanations needs restrictions or new information.',
        'Arbitrary dependence, hidden-state optimal-policy uncertainty and unrestricted learner remainders have no established universal repair.',
        'No universal conversion of LLM, vendor or linkage scores into causal truth; attribution and identification remain different events.',
        'Bank assignment truth, target-platform reliability, independent institutional acceptance and actual economics need later external evidence.']
    findings = [
        'All 376 proposal operations and every nonpassing obligation retain actual evidence prerequisites; independent lanes remain eligible.',
        'Publication and reviewed progress are distinct from coverage closure, qualified native capabilities and accepted products.',
        'The two selected originals advance the census from 59/54 to 61/52 while preserving115 other rows.',
        'Weighted targets, exact versus feasible covariance and fixed versus simultaneous confidence events are developed in the reader.',
        'Factual attribution, external correctness, graph roles, causal identification and target preservation are separate public evaluation outcomes.',
        'All 922 prior citation identities/contexts and 278 earlier compiled inputs survive;925 citations and 221 genuine scholarly PDFs are audited.',
        'The sponsor preserves all 291 earlier citations, binds current reader bytes and retains explicit proposal-only limitations.',
        'HonestDiD remains reference-only with integration_allowed=false; Python IV kernels are inspected but full IV/RD coverage is open.',
        'Q2-Q4 bind the current reader; Q1/Q5, three mandatory repairs and visual/final acceptance remain open.',
        'Preserve failed build/verifier attempts and await every canonical mutation; checkpoints are recovery records, not permission gates.']
    write(BASE / 'program-review.json', dict(status='pass_for_program_consistency_not_completion',
        reviewer=dict(name='Codex author/coordinator', kind='author'), evidence=evidence,
        effective_lane_counts={k: dict(v) for k, v in lanes.items()},
        independent_next_actions=independent, findings=findings, known_routes=known_routes,
        unresolved_research=unresolved, global_blocker=None,
        phase_boundaries_are_stopping_points=False, background_worker_running=False))
    write(BASE / 'continuation-checkpoint.json', dict(date='2026-10-22',
        prior_git_commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        reader=state['reader'], sponsor=ref(SPONSOR / 'working-release.json', 'Exact paired sponsor'),
        completed=findings[2:9], remaining=ref(BASE / 'remaining-operations.json', 'Complete obligations'),
        next_operation=view['next'], next_action=view['next_action'],
        independent_next_actions=independent, global_blocker=None,
        background_worker_running=False, visual_acceptance=False, proposal_accepted=False))
    current = ROOT / 'docs/program/execution/current-program.md'
    (BASE / 'prior-current-program.md').write_bytes(current.read_bytes())
    target_pages = sections['weighted_targets']['physical_pages']
    factual_pages = sections['factuality']['physical_pages']
    link = '2026-10-22/program-refresh-factuality-targets-v1'
    rows = '\n'.join(f"| {label} | {groups[key].get('pass', 0)} | "
        f"{groups[key].get('inconclusive', 0)} | {groups[key]['open']} | {groups[key]['total']} |"
        for key, label in [('software', 'Software coverage'), ('reuse', 'Reuse decisions'),
            ('chapters', 'Chapter reviews')])
    lane_text = '\n'.join(f"- **{x['lane']}: {x['operation']}**. {x['action']}" for x in independent)
    current.write_text(f'''# Current executable proposal program

Updated 22 October 2026 after the factuality and weighted-target integration.
The [queue-wide review]({link}/program-review.json) reconciles every nonpassing
obligation and independent next action. The goal is a scholarly research and
product proposal, followed by public prototype evidence that can justify
costly bank experiments. Bank qualification and adoption are later claims.

Use `python3 tools/run_program_reviews_v2.py status`, `next` and `check`.
The canonical ledger is [state.json](../state.json), governed by the
[proposal scope](../master-program-proposal.md). Earlier numbered masters and
scope execution counts are historical snapshots. Continue across phase boundaries.

## Current integrated documents

Read the [{state['reader']['pages']:,}-page monograph](../../{Path(state['reader']['path']).name})
and its [{sponsor['pages']}-page sponsor proposal](../../{Path(sponsor['pdf']['path']).name}).
The reader has {count} audited citations and {papers} genuine scholarly PDFs;
the sponsor has {sponsor_count} audited citations and binds the exact reader.
Q2-Q4 pass for these reader bytes. Q1/Q5, the mandatory repairs, fresh visual
review and final acceptance remain open.

There are **{view['recorded_proposal_operations']} recorded outcomes of {view['proposal_operations']} proposal operations**,
with **{view['ready_proposal_operations']} ready operations** and **{len(obligations)} nonpassing obligations**.
An inconclusive recorded outcome remains unfinished; counts do not establish
native software capabilities or an accepted product.

| Area | Pass | Inconclusive | Open | Total |
|---|---:|---:|---:|---:|
{rows}

The frontier census has **{inspected} inspected and {unread} unread originals out of 113**,
plus four crosscutting search obligations. Fourteen LLM-task and twelve integration
reviews have scoped outcomes; live-model superiority and adoption remain unproved.

## Integrated progress

Physical pages {target_pages[0]}-{target_pages[1]} develop customer-population weights,
oracle target sensitivity, full covariance and fixed-target versus simultaneous
confidence events. Stipulated group effects USD 6/-2 and cost USD 1 produce net 3/-1
under different mixtures; worst-case net 3-6epsilon crosses zero at epsilon1/2.
These exact authored examples supply no observed bank effects. The source's
alpha=beta=.05 bounds are 90% fixed-target and 85% simultaneous two-sided;
feasible estimation and class containment retain their own conditions.

Physical pages {factual_pages[0]}-{factual_pages[1]} distinguish citation support, external
correctness, causal roles, identification and target preservation. Proposed
matched public known-law/corpus studies precede costly bank experiments.
Surveyed studies are not independently reviewed merely because the survey cites them.
All 922 prior citation identities/contexts and 278 compiled inputs survive.

The integrated sensitivity and Python IV sections remain present. HonestDiD's
proposal reuse decision is **reference**, **integration_allowed=false**. Native
dependencies/solvers, release equivalence and calibration remain open. Python IV
fit, covariance and selected diagnostic kernels are already acquired and inspected.
Full IV/RD coverage remains open; rank/exclusion, distribution semantics and
diagnostic-versus-coefficient inversion must survive library, CLI and MCP conversion.

## Required standard and remaining gaps

Each banking use must connect decision, information clock, population/target,
assumptions, identification or limits, estimation, uncertainty, diagnostics,
substantive alternatives and monetary consequences. Every source needs authentic
local bytes, identity/version/date, hash and inspected primary anchors; scholarly
citations need genuine PDFs. The cutoff is 7 October 2026. FinMarketing sets the
standard of connected scholarly depth; total document length is not acceptance.

MR01 requires 17 areas across six dimensions and 100-150 substantive software pages.
MR02 requires eight chapters, fourteen tasks and96-112 substantive pages. MR03
requires four integration chapters and twelve requirements, with indicative 40-60
pages. Complete coverage and exclusive depth both matter; adding pages alone
does not close a repair.

Known routes: finish the source census and crosscutting searches, area/language
comparisons and reasoned reuse choices; qualify matched public known-law cases;
reconcile chapter depth; then review the exact paired release. Independent software,
commercial, reuse and manuscript lanes retain only their real prerequisites.

Open research: unrestricted latent identification, arbitrary dependence,
hidden-state optimal-policy uncertainty and universal conversion of diagnostic
or LLM scores into causal truth. Narrow claims or additional information may be
necessary. Independent institutional acceptance, real bank truth, production
reliability and measured bank economics are later external-evidence claims.

## Exact continuation

Controller next: **{view['next']}**. {view['next_action']}

The [remaining register]({link}/remaining-operations.json) retains all
{len(obligations)} nonpassing obligations, dependencies and evidence. Independent eligible actions:

{lane_text}

The [Python continuation](2026-10-22/python-iv-kernels-v1/review.json) specifies
remaining RD/CausalPy IV originals and numerical guards. The integrated census
receipt preserves 61/52 and no longer asks for integration already delivered.

Wait for each canonical mutation. Checkpoints and Git preservation are recovery
tools, not permission gates. No global blocker or unattended research worker
exists. The inherited six-preview allowance under `/home/ubuntu/AGENTS.md` is
exhausted; visual acceptance needs a fresh image session. Source, mathematical
and manuscript work remain eligible.
''')
    run.render(ROOT, state)
    print(json.dumps(dict(reader=state['reader'], sponsor_pages=sponsor['pages'],
        records=count, papers=papers, sponsor_records=sponsor_count,
        recorded=view['recorded_proposal_operations'], ready=view['ready_proposal_operations'],
        remaining=len(obligations), next=view['next'], proposal_accepted=False)))


if __name__ == '__main__':
    main()
