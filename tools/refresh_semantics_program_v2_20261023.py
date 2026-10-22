#!/usr/bin/env python3
"""Reconcile the full proposal queue and exact paired release without rewriting history."""
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import re
import subprocess

import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run = controller.base
ROOT = run.core.ROOT
DAY = ROOT / 'docs/program/execution/2026-10-23'
PRIOR = DAY / 'program-refresh-policy-v2'
PUB = DAY / 'semantics-reader-v4'
SPONSOR = DAY / 'sponsor-semantics-v1'
CENSUS = DAY / 'census-context-conflict-v1'
read = lambda path: json.loads(path.read_text())
CORRECTED = {'SW.CELL.iv_rd_design.R', 'SW.CELL.observations_data.commercial',
    'SW.COMM.observations_data'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--edition', choices=['v2', 'v3'], default='v2')
    args = parser.parse_args()
    base = DAY / ('program-refresh-semantics-' + args.edition)
    assert not base.exists(), 'Preserve completed refreshes; use an unused successor edition.'
    state = run.core.read(ROOT, run.core.STATE)
    assert state['execution_runtime']['active'] is None
    publication, sponsor = read(PUB / 'working-release.json'), read(SPONSOR / 'working-release.json')
    for record in [publication, sponsor, read(PRIOR / 'program-review.json')]:
        verify_bindings(record)
    assert run.same_reader(state['reader'], publication['pdf'])
    assert run.same_reader(state['reader'], sponsor['paired_monograph'])
    assert not publication['final_acceptance'] and not sponsor['final_acceptance']
    view = controller.status(ROOT, state)
    assert {q['id']: q['status'] for q in view['proposal_gaps']} == dict(
        Q1='open', Q2='pass', Q3='pass', Q4='pass', Q5='open')
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
        old = previous.get(key, {})
        if not progress and key in CORRECTED:
            action = old['action']
        item = dict(id=key, lane=node['lane'], title=node['title'],
            status=result['outcome'] if result else 'open', action=action,
            prerequisites=run.ledger.blockers(merged, node), outputs=node['outputs'],
            evidence=result, requires_inputs=node['requires_inputs'])
        if progress:
            item['action_checkpoint'] = progress[-1]
        for field in ['corrected_source_followup', 'source_followup']:
            if field in old:
                run.core.bound(ROOT, old[field])
                item[field] = old[field]
        obligations.append(item)
    for name, prefix, total in [('software', 'SW.CELL.', 102), ('reuse', 'SW.DECISION.', 115),
            ('chapters', 'TEXT.REVIEW.', 22)]:
        selected = {k: v for k, v in results.items() if k.startswith(prefix)}
        groups[name] = dict(Counter(v['outcome'] for v in selected.values()),
            open=total-len(selected), total=total)
        assert sum(v for k, v in groups[name].items() if k != 'total') == total
    assert len(obligations) + sum(v['pass'] for v in lanes.values()) == view['proposal_operations'] == 376
    by_id = {x['id']: x for x in obligations}
    for key in CORRECTED:
        if key in by_id and not by_id[key].get('action_checkpoint'):
            assert by_id[key]['action'] == previous[key]['action']
    for key in ['SW.DECISION.inherited_lmtp', 'SW.DECISION.inherited_linearmodels']:
        assert results[key]['outcome'] == 'pass' and key not in by_id
    dispositions = Counter(x['disposition'] for x in read(CENSUS / 'census-register.json')['items'])
    inspected, unread = (dispositions[k] for k in
        ['inspected_primary_retained_with_limits', 'open_original_not_inspected'])
    assert inspected + unread == 113
    independent = []
    for lane in ['software', 'commercial', 'reuse', 'llm', 'manuscript', 'release', 'proposal_acceptance']:
        eligible = [x for x in ready if x['lane'] == lane]
        if eligible:
            node = eligible[0]
            independent.append(dict(lane=lane, operation=node['id'],
                action=by_id.get(node['id'], node)['action'], depends=node['depends'],
                requires_inputs=node['requires_inputs'], outputs=node['outputs']))
    sources = len(read(PUB / 'reader/source-audit.json')['sources'])
    papers = read(PUB / 'traceability-review.json')['scholarly_pdfs']
    sponsor_sources = len(read(SPONSOR / 'source-audit.json')['sources'])
    pages, sponsor_pages = state['reader']['pages'], sponsor['pages']
    assert (pages, sources, papers, sponsor_pages, sponsor_sources) == (1245, 939, 223, 52, 314)
    base.mkdir(parents=True)
    write(base / 'state-snapshot.json', state)
    write(base / 'status-snapshot.json', view)
    write(base / 'remaining-operations.json', dict(reader=state['reader'], coverage=groups,
        recorded=view['recorded_proposal_operations'], proposal_operations=376,
        ready=view['ready_proposal_operations'], operations=obligations,
        census=ref(CENSUS / 'census-register.json', 'All 113 candidate dispositions'), proposal_accepted=False))
    findings = [
        'All 376 proposal operations and every nonpassing obligation are reconciled; inconclusive is unfinished.',
        'Independent lanes retain only real prerequisites; checkpoints and phase boundaries are not stopping points.',
        f'The exact {pages}-page reader and {sponsor_pages}-page sponsor are paired and source/text reviewed, without visual or final acceptance.',
        f'The reader conserves 932 prior source identities and adds seven; {sources} audited citations and {papers} scholarly PDFs are retained.',
        f'The sponsor conserves 305 prior source identities; all {sponsor_sources} current citations are audited.',
        'Four connected additions integrate reference-only software choices, lmtp policy semantics, observational twins and the qualified multimodal-conflict critique.',
        f'The census has {inspected} inspected and {unread} unread originals of 113, plus four crosscutting searches.',
        'Layout, source-schema and preparation failures are preserved with exact successful successors; the earlier refresh regression also remains recorded.',
        'The three source-specific follow-up actions are retained unless superseded by newer authenticated progress.',
        'Q2-Q4 pass for exact current reader bytes; Q1/Q5, MR01-MR03, L1/L6 and rendered visual acceptance remain open.',
        'Reference decisions grant no integration capability; authored mathematics, documentation and benchmark reports do not establish bank returns or native adoption.']
    evidence = [ref(base / 'state-snapshot.json', 'Canonical state at refresh'),
        ref(base / 'remaining-operations.json', 'All nonpassing obligations'),
        ref(PRIOR / 'program-review.json', 'Preserved successful predecessor'),
        ref(PUB / 'working-release.json', 'Exact integrated working reader'),
        ref(SPONSOR / 'working-release.json', 'Exact paired working sponsor'),
        ref(PUB / 'release-source-review.json', 'Reader preservation and source review'),
        ref(SPONSOR / 'author-review.json', 'Sponsor preservation and review'),
        ref(CENSUS / 'census-register.json', 'Candidate accounting'),
        ref(DAY / 'refresh-preservation-v1/correction-review.json', 'Earlier refresh failure and verified successor')]
    evidence.append(ref(DAY / 'program-refresh-semantics-v1/navigation-failure.json',
        'Preserved failed fragment-link insertion; successor verifies all navigation'))
    for name in ['layout-correction.json', 'source-schema-correction.json', 'prepare-correction.json',
            'failure-carryforward.json', 'layout-carryforward.json']:
        evidence.append(ref(PUB / name, 'Preserved failure and successor evidence'))
    for name in ['run_program_checkpoint_v3.py', 'build_semantics_reader_v4_20261023.py',
            'review_publish_semantics_20261023.py', 'review_publish_semantics_v4_20261023.py',
            'build_semantics_sponsor_20261023.py', 'review_publish_semantics_sponsor_20261023.py']:
        evidence.append(ref(ROOT / 'tools' / name, 'Exact used controller or publication implementation'))
    evidence += [ref(ROOT / 'tests/test_run_program_checkpoint_v3.py', 'Controller resume and tamper checks'),
        ref(Path(__file__), 'Immutable refresh successor')]
    review = dict(status='pass_for_program_consistency_not_completion',
        reviewer=dict(name='Codex author/coordinator', kind='author'), evidence=evidence,
        effective_lane_counts={k: dict(v) for k, v in lanes.items()}, findings=findings,
        independent_next_actions=independent, global_blocker=None,
        phase_boundaries_are_stopping_points=False, background_worker_running=False)
    verify_bindings(review)
    write(base / 'program-review.json', review)
    write(base / 'continuation-checkpoint.json', dict(date='2026-10-23',
        prior_git_commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        reader=state['reader'], sponsor=ref(SPONSOR / 'working-release.json', 'Exact paired sponsor'),
        completed=findings[2:9], remaining=ref(base / 'remaining-operations.json', 'All exact remaining actions'),
        next_operation=view['next'], next_action=view['next_action'], independent_next_actions=independent,
        visual_acceptance=False, proposal_accepted=False, global_blocker=None, background_worker_running=False))
    current = ROOT / 'docs/program/execution/current-program.md'
    (base / 'prior-current-program.md').write_bytes(current.read_bytes())
    link = str(base.relative_to(ROOT / 'docs/program/execution'))
    rows = '\n'.join(f"| {label} | {groups[key].get('pass', 0)} | {groups[key].get('inconclusive', 0)} | {groups[key]['open']} | {groups[key]['total']} |"
        for key, label in [('software', 'Software coverage'), ('reuse', 'Reuse decisions'), ('chapters', 'Chapter reviews')])
    lane_text = '\n'.join(f"- **{x['lane']}: {x['operation']}**. {x['action']}" for x in independent)
    reader_path, sponsor_path = publication['pdf']['path'].removeprefix('docs/'), sponsor['pdf']['path'].removeprefix('docs/')
    current.write_text(f'''# Current executable proposal program

Updated 23 October 2026. The [queue-wide review]({link}/program-review.json)
reconciles all 376 proposal operations and every nonpassing obligation. The goal is
a scholarly research and product proposal using public/generated evidence to justify
expensive bank experiments. Bank qualification and adoption are later work.

Use `python3 tools/run_program_checkpoint_v3.py status`, `next` and `check`.
The [canonical ledger](../state.json), [proposal scope](../master-program-proposal.md)
and actual evidence dependencies govern execution. Continue eligible work across phase boundaries.

## Current integrated documents

The current pair is the [{pages:,}-page monograph](../../{reader_path}) and
[{sponsor_pages}-page sponsor proposal](../../{sponsor_path}). Their audits retain
{sources} and {sponsor_sources} citations respectively; the reader includes {papers} genuine scholarly
PDFs. The sponsor binds exact reader bytes. Q2-Q4 pass for this reader. Q1/Q5,
mandatory repairs, fresh visual review and final proposal acceptance remain open.

The live queue has **{view['recorded_proposal_operations']} recorded outcomes of 376**,
**{view['ready_proposal_operations']} ready operations**, and **{len(obligations)} nonpassing obligations**.
Recorded inconclusive outcomes are unfinished.

| Area | Pass | Inconclusive | Open | Total |
|---|---:|---:|---:|---:|
{rows}

The frontier census has **{inspected} inspected and {unread} unread originals of 113**,
plus four crosscutting searches. Fourteen LLM-task and twelve integration reviews have
scoped proposal outcomes; these do not establish live-model superiority or adoption.

## Substantive findings now integrated

The reader and sponsor integrate all four reviewed developments. The linearmodels
and lmtp reuse choices remain reference-only, **integration_allowed=false**, with
no native capability. The Tetrad source addresses supplied pure latent measurement
models; it does not establish generic IV/RD coverage. Conversion, rank and covariance
concerns remain source-level questions requiring caller/backend checks.

For lmtp, seventeen authenticated originals distinguish intended cluster identity
from an outer-fold field mismatch, and documented bounds from effective call paths.
Downstream `ife` uncertainty semantics remain uninspected. AGPL rights need a specific
integration assessment. Exact authored two-period policy values are 7.36, 18.24 and
107/9 USD for natural, risk-shift and odds-tilt laws. These are stipulated mathematical
values, not package executions or bank returns.

The contextual-causality discussion distinguishes textual interventions from changes
to a data-generating process. Two observationally identical models imply net contact
values of USD 90 and USD -10. The multimodal-conflict discussion derives a precise
disagreement/correctness identity, checks the reported DCD gains, retains conflicting
tables and leaves code/data/rights unqualified. Survey citations do not qualify unread
cited originals. Neither example turns LLM output into causal truth.

Earlier source records, citation contexts and compiled content survive. Original layout,
source-schema, preparation and program-refresh failures remain preserved with successful
successors. Text bounds and source/arithmetic reviews passed; visual acceptance is open.

## Required standard and remaining gaps

Each banking use must connect decision, information clock, population and target,
assumptions, identification or limits, estimation, uncertainty, diagnostics, substantive
alternatives and monetary consequences. Each source needs authentic local bytes,
identity, version/date, SHA-256, inspected primary anchors and supported claims.
Scholarly works need genuine PDFs. The cutoff is 7 October 2026; later observations
remain labeled. FinMarketing sets connected scholarly depth.

MR01 covers seventeen areas across six language/commercial dimensions, reasoned reuse
choices and 100-150 substantive software pages. MR02 requires eight chapters, fourteen
tasks and 96-112 substantive LLM/agent pages. MR03 requires four integration chapters
and twelve requirements, with indicative 40-60 pages. Exclusive depth and complete
coverage both matter. L1 and L6 remain inconclusive.

The [remaining register]({link}/remaining-operations.json) retains all {len(obligations)}
nonpassing obligations, evidence, actual prerequisites and exact actions. Known routes
are primary-source inspection, complementary searches, cutoff-edition comparisons,
reasoned reuse, public/generated studies and substantive chapter/release reconciliation.
Commercial temporal omissions and native qualification remain separate obligations.

No universal repair is established for unrestricted latent identification, arbitrary
persistent dependence, hidden-state optimal-policy uncertainty or arbitrary learner
remainders. Use justified restrictions, explicit negative results or new information.
No general conversion of LLM, vendor or linkage scores into causal truth is established.
Bank truth, independent institutional acceptance, target-platform reliability and actual
bank economics require later external evidence; they do not block independent proposal work.

## Exact continuation

Controller next: **{view['next']}**. {view['next_action']}

Independent eligible lanes retain only their actual prerequisites:

{lane_text}

Use the latest authenticated checkpoint for each operation. Preserve the specific
R IV/RD and commercial observation follow-ups. Do not repeat already acquired and
inspected Python IV kernels, completed source reviews or delivered integration.
Await actual canonical mutation completion before dependent transitions.

Checkpoints preserve recovery and create no permission gates. There is no global
blocker or unattended worker. The six-preview allowance in `/home/ubuntu/AGENTS.md`
is exhausted; a fresh session is needed for further visual acceptance. This affects
visual review only. Source, manuscript and other independent work remain eligible.
''')
    master = ROOT / 'docs/program/master-program.md'
    prior_master = base / 'prior-master-program.md'
    prior_master.write_bytes(master.read_bytes())
    master_text = master.read_text()
    master_text = master_text.replace('Version 11.0 · 11 October 2026 · Literature cutoff: 7 October 2026',
        'Version 15.0 · 23 October 2026 · Literature cutoff: 7 October 2026', 1)
    status_block = f'''## Current execution status

This master now governs the proposal and public-evidence program. The executable
scope and queue are in the [current program](execution/current-program.md), the
[proposal scope](master-program-proposal.md), and [canonical state](state.json).
The current working pair is the [{pages:,}-page monograph](../{reader_path}) and
[{sponsor_pages}-page sponsor proposal](../{sponsor_path}); the sponsor binds the
exact monograph bytes. The reader has {sources} audited citation records and
{papers} genuine cited scholarly PDFs; the sponsor has {sponsor_sources} audited
records. Q2-Q4 pass for this exact reader. Q1/Q5, MR01-MR03, L1/L6, fresh visual
acceptance and final proposal acceptance remain open.

The live queue records {view['recorded_proposal_operations']} of 376 proposal
operations, with {view['ready_proposal_operations']} ready and {len(obligations)}
nonpassing obligations. The frontier census has {inspected} inspected and {unread}
unread originals of 113. See the [complete queue reconciliation](execution/{link}/program-review.json)
and its [remaining-operation register](execution/{link}/remaining-operations.json).

Recent integration adds bounded treatment of reference-only linearmodels/lmtp
decisions, exact longitudinal policy semantics, observationally identical
business worlds, and qualified multimodal-conflict results. These are reviewed
proposal findings, not native capability, independent validation, or bank returns.
Earlier compilation and refresh failures remain in the execution archive with
their successful successors. The six-preview allowance is exhausted for this
session; only visual acceptance awaits a fresh image allowance.

'''
    heading = '## What the required standard means'
    assert master_text.count(heading) == 1
    if '## Current execution status\n' in master_text:
        master_text, count = re.subn(
            r'(?ms)^## Current execution status\n.*?(?=^## What the required standard means\n)',
            status_block, master_text)
        assert count == 1
    else:
        master_text = master_text.replace(heading, status_block + heading, 1)
    baseline = f'''## Reconciled baseline

The current canonical reader is the [{pages:,}-page working monograph](../{reader_path}),
with {sources} audited citation records and {papers} genuine scholarly PDFs. The
exact paired [working sponsor proposal](../{sponsor_path}) has {sponsor_pages} pages
and {sponsor_sources} audited citations. Both are compiled working deliverables;
they have not passed visual or final proposal acceptance. The sponsor release binds
the reader SHA-256, so these are the current integrated documents rather than an
older monograph and a separately updated proposal.

The reader integrates four reviewed developments: reuse boundaries for linearmodels
and Tetrad; lmtp policy-law, rights and uncertainty limits with exact authored
values; an observational-twins contact example that preserves causal ambiguity; and
a source-qualified multimodal-conflict analysis retaining table discrepancies.
None claims a working package adapter, bank validation, or causal truth from a
language-model response. Existing source records and compiled content were conserved.

The sponsor carries forward its prior substantive argument and audit identities,
then adds the new source-grounded findings and current queue/census figures. The
public-data survey and existing generated examples remain proposals or stipulated
demonstrations according to their own evidence; neither implies authentic bank
performance. Q2-Q4 pass for the exact current reader; Q1/Q5 and the mandatory
repair, coverage, visual, and final acceptance obligations remain open.

'''
    pattern = r'(?ms)^## Reconciled baseline\n.*?(?=^## Remaining gaps and whether we know a route\n)'
    master_text, count = re.subn(pattern, baseline, master_text)
    assert count == 1
    graph_note = '''## One execution graph

The package-level graph below retains the scientific and later qualification
dependencies. Current proposal operations, mandatory repairs, public-study
designs, source omissions and eligible lanes are reconciled by the [executable
queue](execution/current-program.md). Its 376-operation proposal scope takes
precedence over historical product-oriented completion counts. Later bank inputs
do not become proposal blockers; negative and inconclusive research outcomes
remain legitimate scoped proposal findings and unresolved capability claims.
'''
    if 'The package-level graph below retains' not in master_text:
        assert master_text.count('## One execution graph\n') == 1
        master_text = master_text.replace('## One execution graph\n', graph_note, 1)
    start = '## Executing and resuming\n\nRun from the repository root:'
    if start in master_text:
        master_text = master_text.replace(start, '''## Executing and resuming

Use `python3 tools/run_program_checkpoint_v3.py status`, `next`, and `check`
for the current proposal queue. Its durable checkpoints select actual unfinished
work. `start`, `progress`, `record`, `yield`, `block`, `resume` and `reopen`
preserve evidence and prior reviews; a checkpoint is not a permission gate.

The package-level dependency and historical-integrity views remain available
from the repository root:''', 1)
    release_pattern = r'(?ms)^## Release and review policy\n.*?(?=^Historical controls are available under\n)'
    release = '''## Release and review policy

The current integrated working pair carries preserved source identities,
substantive mathematics and explicit negative findings. Source, arithmetic and
text review do not establish visual, independent, bank or final proposal
acceptance. Q2-Q4 currently pass for exact reader bytes; Q1 and Q5 still require
complete repair coverage/depth and the remaining integrated/rendered review.
The [current queue review](execution/current-program.md) governs the next work.

Integrate material findings into connected existing chapters and the exact
paired sponsor, preserving prior failed attempts. Do not rebuild solely to
advance process counters. Changes to reader bytes require applicable exact-reader
reviews. A new scientific attempt identifies its gap, preserves prior results
and meets the common source, argument, study and failure criteria. Independent
eligible lanes continue after local omissions or checkpoints. Public/generated
evidence justifies later costly bank work; it does not pretend to be that work.

'''
    master_text, count = re.subn(release_pattern, release, master_text)
    assert count == 1
    master.write_text(master_text)
    master_review = dict(status='refreshed_current_baseline_and_execution_pointer',
        evidence=[ref(master, 'Current master and current exact-reader baseline'),
            ref(current, 'Executable queue and unresolved gaps'),
            ref(base / 'remaining-operations.json', 'All nonpassing obligations'),
            ref(SPONSOR / 'working-release.json', 'Exact paired sponsor')],
        reader=publication['pdf'], sponsor=sponsor['pdf'], proposal_accepted=False)
    write(base / 'master-program-review.json', master_review)
    navigation = ROOT / 'docs/README.md'
    (base / 'prior-docs-readme.md').write_bytes(navigation.read_bytes())
    navigation.write_text(f'''# Current causal banking proposal

This workspace develops a scholarly monograph and product/investment proposal.
It is unfinished and does not establish an accepted bank product.

- [Current master program and execution rules](program/execution/current-program.md)
- [Proposal scope and public-data portfolio](program/master-program-proposal.md)
- [Mission Control](mission-control.md) · [HTML dashboard](mission-control.html)
- [Canonical machine state](program/state.json)
- [Working monograph — {pages:,} pages]({reader_path})
- [Paired working sponsor proposal — {sponsor_pages} pages]({sponsor_path})
- [Public-data survey](program/public-data-v15/public-data-survey.pdf)

Run `python3 tools/run_program_checkpoint_v3.py status`, `check`, and `next` from the repository root.

The pair passed preservation, source, arithmetic and extracted-text reviews. Coverage,
mandatory repairs, fresh visual review and final proposal acceptance remain open.
The current program records further live progress separately from the paired release.
''')
    controller.render(ROOT, state)
    mission = ROOT / 'docs/mission-control.md'
    mission.write_text(mission.read_text().replace('[Public-data survey]',
        f'[Paired working sponsor proposal]({sponsor_path}) — {sponsor_pages} pages. [Public-data survey]', 1))
    html = ROOT / 'docs/mission-control.html'
    html.write_text(html.read_text() +
        f'<p><a href="{sponsor_path}">Paired working sponsor proposal</a> — {sponsor_pages} pages.</p>\n')
    for path in [current, master, navigation, mission, html]:
        assert reader_path in path.read_text() and sponsor_path in path.read_text(), str(path)
    assert 'Version 15.0' in master.read_text() and '1,240-page' not in master.read_text()
    write(base / 'navigation-review.json', dict(status='pass', evidence=[ref(path, 'Exact current program/navigation')
        for path in [current, master, navigation, mission, html]], reader=publication['pdf'], sponsor=sponsor['pdf']))
    verify_bindings(read(base / 'program-review.json'))
    print(json.dumps(dict(refresh=str(base.relative_to(ROOT)), recorded=view['recorded_proposal_operations'],
        ready=view['ready_proposal_operations'], remaining=len(obligations), census=[inspected, unread],
        reader_pages=pages, sponsor_pages=sponsor_pages, next=view['next'])))


if __name__ == '__main__':
    main()
