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
BASE = ROOT / 'docs/program/execution/2026-10-22/program-refresh-workflow-v1'
PRIOR = ROOT / 'docs/program/execution/2026-10-22/program-refresh-observations-v1'
PUB = ROOT / 'docs/program/execution/2026-10-22/computation-workflow-reader-v1'
FACTUAL = ROOT / 'docs/program/execution/2026-10-22/factuality-weighted-reader-v1/publication-v2'
WORKFLOW = ROOT / 'docs/program/execution/2026-10-22/computation-commercial-preflight-v1'
LINEAR = ROOT / 'docs/program/execution/2026-10-22/linearmodels-reuse-v1'
SPONSOR = ROOT / 'docs/program/execution/2026-10-22/sponsor-workflow-v1'
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
        if identifier in ['SW.CELL.computation_workflow.commercial', 'SW.COMM.computation_workflow']:
            item['corrected_source_followup'] = ref(PUB / 'integrated-progress.json',
                'Current comparison integrated; historical and remaining-family coverage still open')
            item['action'] = read(PUB / 'integrated-progress.json')['next_action']
        obligations.append(item)
    for name, prefix, total in [('software', 'SW.CELL.', 102),
            ('reuse', 'SW.DECISION.', 115), ('chapters', 'TEXT.REVIEW.', 22)]:
        selected = {k: v for k, v in results.items() if k.startswith(prefix)}
        groups[name] = dict(Counter(v['outcome'] for v in selected.values()),
            open=total - len(selected), total=total)
        assert sum(v for k, v in groups[name].items() if k != 'total') == total
    assert 'SW.DECISION.inherited_honestdid' not in {r['id'] for r in obligations}
    assert 'SW.DECISION.inherited_linearmodels' not in {r['id'] for r in obligations}
    assert view['recorded_proposal_operations'] == 190
    assert len(obligations) + sum(
        v['pass'] for v in lanes.values()) == view['proposal_operations'] == 376
    dispositions = Counter(x['disposition'] for x in read(CENSUS / 'census-register.json')['items'])
    inspected = dispositions['inspected_primary_retained_with_limits']
    unread = dispositions['open_original_not_inspected']
    assert (inspected, unread) == (61, 52)
    count = len(read(PUB / 'reader/source-audit.json')['sources'])
    papers = read(PUB / 'traceability-review.json')['scholarly_pdfs']
    sponsor_count = len(read(SPONSOR / 'source-audit.json')['sources'])
    assert (count, papers, sponsor_count) == (932, 221, 305)
    workflow_pages = read(PUB / 'release-source-review.json')['checks']['physical_pages']
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
        ref(PUB / 'release-source-review.json', '925 earlier citations and 280 compiled inputs preserved'),
        ref(FACTUAL.parent / 'schema-failure.json', 'Preserved earlier schema failure'),
        ref(FACTUAL / 'text-review-attempt-1.json', 'Preserved earlier wrapped-text verifier failure'),
        ref(PUB / 'transition-attempt-1.json', 'Rejected out-of-order transition preserved'),
        ref(SPONSOR / 'review-attempt-1.json', 'Preserved sponsor verifier correction'),
        ref(SPONSOR / 'publication-attempt-1.json', 'Immutable review publication repair'),
        ref(WORKFLOW / 'omissions-register.json', 'Candidate-specific commercial omissions'),
        ref(PUB / 'integrated-progress.json', 'Commercial integration complete; source gaps remain'),
        ref(LINEAR / 'review.json', 'New reference-only linearmodels decision'),
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
        'Recover commercial workflow cutoff editions; inspect Dataiku technical pages, SAS Viya, Domino and Posit, then reconcile complementary market coverage.',
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
        'All 925 earlier citation identities/contexts and 280 compiled inputs survive; 932 citations and 221 genuine scholarly PDFs are audited.',
        'The 50-page sponsor preserves all 296 earlier citations and audits 305 citations; it binds the 1240-page reader at the 189-outcome release snapshot.',
        'The subsequent linearmodels reference-only decision advances the live queue to 190 outcomes, with no adapter permission. Its editorial reconciliation remains explicit.',
        'Six current commercial workflow manuals are integrated as later observations; zero qualify historical coverage. Source-specific omissions remain open.',
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
    link = '2026-10-22/program-refresh-workflow-v1'
    rows = '\n'.join(f"| {label} | {groups[key].get('pass', 0)} | "
        f"{groups[key].get('inconclusive', 0)} | {groups[key]['open']} | {groups[key]['total']} |"
        for key, label in [('software', 'Software coverage'), ('reuse', 'Reuse decisions'),
            ('chapters', 'Chapter reviews')])
    lane_text = '\n'.join(f"- **{x['lane']}: {x['operation']}**. {x['action']}" for x in independent)
    current.write_text(f'''# Current executable proposal program

Updated 22 October 2026 after the workflow release and the linearmodels reuse decision.
The [queue-wide review]({link}/program-review.json) reconciles every nonpassing
obligation and independent action. This is a scholarly research and product proposal.
Public/generated prototype evidence should justify any expensive bank experiment.
Bank qualification, production reliability and adoption remain later claims.

Use `python3 tools/run_program_reviews_v2.py status`, `next` and `check`.
The canonical ledger is [state.json](../state.json), governed by the
[proposal scope](../master-program-proposal.md). Earlier numbered masters and scope
counts are historical snapshots. Continue eligible work across phase boundaries.

## Current integrated documents

Read the [{state['reader']['pages']:,}-page monograph](../../{Path(state['reader']['path']).name})
and its [{sponsor['pages']}-page sponsor proposal](../../{Path(sponsor['pdf']['path']).name}).
The reader audits {count} citations and {papers} genuine scholarly PDFs; the sponsor
has {sponsor_count} audited citations and binds the exact reader bytes.
Q2-Q4 pass for this working reader. Q1/Q5, the three mandatory repairs, fresh visual
review and final acceptance remain open. All-page text bounds and extracted-text
checks passed; they do not grant visual acceptance.

The paired release captures 189 recorded outcomes. The later linearmodels proposal
reference decision brings the live queue to **{view['recorded_proposal_operations']} recorded outcomes
of {view['proposal_operations']}**, **{view['ready_proposal_operations']} ready operations**, and
**{len(obligations)} nonpassing obligations**. Its native integration remains disabled.
This is an explicit editorial delta for the next substantive release; the existing
reader already develops its IV rank, covariance and diagnostic semantics. Do not
rebuild the whole reader solely to update a process count.

| Area | Pass | Inconclusive | Open | Total |
|---|---:|---:|---:|---:|
{rows}

Inconclusive outcomes remain unfinished obligations. The frontier census has
**{inspected} inspected and {unread} unread originals out of 113**, plus four
crosscutting searches. Fourteen LLM-task and twelve integration reviews have scoped
proposal outcomes; they establish neither live-model superiority nor repository adoption.

## Integrated findings and source limits

Physical PDF pages {workflow_pages[0]}-{workflow_pages[1]} (printed pages 635-639),
section 39.8, connect commercial orchestration to scientific replay. Six current
official manuals across five families describe Databricks repair and monitoring,
Snowflake task graphs, Azure ML reuse, AWS error handling and Dataiku automation.
None has an authenticated cutoff-era edition. Their current mechanisms supplement
the survey without closing historical coverage. Detailed Dataiku technical pages,
SAS Viya, Domino, Posit and complementary market discovery remain open.

In the exact authored example, three units have contrast 6 and one has -2.
The intended average is 4. Appending two partial results and then all four on retry
changes the stored-row mean to 14/3; keyed recovery returns 4 while preserving six
attempts. Changing the target can change net value from 3 to -1. These stipulated
values motivate public known-law recovery trials; they are not measured vendor
failures or bank returns. The library, CLI and MCP must preserve the target, data
vintage, assumptions, numerical settings and failure history as well as the number.
All 925 earlier citation identities/contexts and 280 compiled inputs survive.

The integrated factuality and weighted-target sections preserve the distinction
between attribution, external correctness, causal identification and target validity.
The census advanced from 59/54 to 61/52. The sensitivity/IV material distinguishes
trend restrictions, full covariance, projected rank and actual diagnostic distributions.
HonestDiD and linearmodels have reference-only proposal decisions with
**integration_allowed=false**. Native dependencies, release equivalence, conversion
behavior and calibration remain unqualified. Python IV/RD coverage remains open.

## Required standard and complete gap register

Each banking use connects decision, information clock, population/target, assumptions,
identification or limits, estimation, uncertainty, diagnostics, substantive alternatives
and monetary consequences. Every citation needs authentic local bytes, source identity,
version/date, SHA-256, inspected primary anchors and supported claims. Scholarly works
need genuine PDFs. The literature cutoff is 7 October 2026; later observations remain
labeled. FinMarketing sets connected scholarly depth, not a total-length target.

MR01 requires 17 areas across six language/commercial dimensions, reasoned reuse
choices and 100-150 substantive software pages. MR02 requires eight chapters,
fourteen tasks and 96-112 substantive LLM/agent pages. MR03 requires four integration
chapters and twelve requirements, with indicative 40-60 pages. Exclusive depth and
complete coverage both matter. L1 and L6 remain inconclusive despite their depth.

The [remaining register]({link}/remaining-operations.json) retains every one of the
{len(obligations)} nonpassing obligations with dependencies, evidence and a next action.
Known routes are primary-source recovery, complementary searches, edition-specific
comparisons, reasoned reuse, reviewed public/generated studies, and integrated
chapter/release reconciliation. Commercial source omissions and missing native
qualification are local obligations, not global blockers.

There is no established universal repair for unrestricted latent identification,
arbitrary persistent dependence, hidden-state optimal-policy uncertainty or arbitrary
learner remainders. Narrow claims, explicit negative findings or justified extra
information are valid proposal outcomes. No universal conversion of an LLM, vendor
or linkage score into causal truth is established. Bank truth, independent acceptance,
production service levels and actual bank economics require later external evidence.

## Exact continuation and execution discipline

Controller next: **{view['next']}**. {view['next_action']}

Independent eligible lanes retain only their actual prerequisites:

{lane_text}

The [commercial continuation](2026-10-22/computation-workflow-reader-v1/integrated-progress.json)
marks the integration already delivered and lists the actual source work remaining.
The [Python continuation](2026-10-22/python-iv-kernels-v1/review.json) identifies
remaining RD/CausalPy IV originals and numerical delegates; do not reacquire inspected
kernels. The [linearmodels decision](2026-10-22/linearmodels-reuse-v1/review.json)
binds its local reference role and later qualification obligations.

Await process completion, not merely a session ID, before a dependent canonical
transition. Preserve failed attempts and exact successor repairs. Independent reads
may overlap; edits and canonical state changes are sequential. Batch related source
and editorial work into substantive releases; a publication checkpoint is not a stop
or permission gate. No global blocker or unattended research worker exists.
The six-preview session allowance in `/home/ubuntu/AGENTS.md` is exhausted; a fresh
image session is required for visual acceptance. Source and manuscript work remain eligible.
''')
    run.render(ROOT, state)
    print(json.dumps(dict(reader=state['reader'], sponsor_pages=sponsor['pages'],
        records=count, papers=papers, sponsor_records=sponsor_count,
        recorded=view['recorded_proposal_operations'], ready=view['ready_proposal_operations'],
        remaining=len(obligations), next=view['next'], proposal_accepted=False)))


if __name__ == '__main__':
    main()
