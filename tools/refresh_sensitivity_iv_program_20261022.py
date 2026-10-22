#!/usr/bin/env python3
"""Reconcile the whole proposal queue after the sensitivity and IV continuation."""
from collections import Counter, defaultdict
import json
from pathlib import Path
import subprocess

import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run = extension.base
ROOT = run.core.ROOT
BASE = ROOT/'docs/program/execution/2026-10-22/program-refresh-sensitivity-iv-v1'
PRIOR = ROOT/'docs/program/execution/2026-10-22/program-refresh-observations-v1'
PUB = ROOT/'docs/program/execution/2026-10-22/sensitivity-iv-reader-v1'
HD = ROOT/'docs/program/execution/2026-10-22/honestdid-reuse-v1'
IV = ROOT/'docs/program/execution/2026-10-22/python-iv-kernels-v1'
SPONSOR = ROOT/'docs/program/execution/2026-10-22/sponsor-sensitivity-iv-v1'
CENSUS = ROOT/'docs/program/execution/2026-10-22/census-domain-knowledge-v1/census-register.json'
read = lambda p: json.loads(p.read_text())


def main():
    assert not BASE.exists()
    state = run.core.read(ROOT, run.core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path'] == 'docs/causal_proposal_sensitivity_iv_reviewed_2026-10-22.pdf'
    sponsor = read(SPONSOR/'working-release.json'); verify_bindings(sponsor)
    assert run.same_reader(state['reader'], sponsor['paired_monograph'])
    view = run.status(ROOT, state)
    graph, merged, stages, ready, _ = run.queue(ROOT, state)
    assert {q['id']: q['status'] for q in view['proposal_gaps']} == dict(Q1='open', Q2='pass', Q3='pass', Q4='pass', Q5='open')
    results = merged['execution_program']['results']
    obligations, groups, lanes = [], {}, defaultdict(Counter)
    previous = {r['id']: r for r in read(PRIOR/'remaining-operations.json')['operations']}
    for node in graph['nodes']:
        identifier = node['id']; result = results.get(identifier)
        if stages[identifier] != 'proposal_now': continue
        lanes[node['lane']][result['outcome'] if result else 'open'] += 1
        if result and result['outcome'] == 'pass': continue
        progress = merged['execution_program']['progress'].get(identifier, [])
        action = read(ROOT/progress[-1]['path'])['next_action'] if progress else node['action']
        item = dict(id=identifier, lane=node['lane'], title=node['title'], status=result['outcome'] if result else 'open',
            action=action, prerequisites=run.ledger.blockers(merged, node), outputs=node['outputs'], evidence=result,
            requires_inputs=node['requires_inputs'])
        if identifier in previous:
            for key in ['corrected_source_followup', 'source_followup']:
                if key in previous[identifier]: item[key] = previous[identifier][key]
            if identifier in ['LL.CENSUS', 'SW.CELL.iv_rd_design.R',
                    'SW.CELL.observations_data.commercial', 'SW.COMM.observations_data']:
                item['action'] = previous[identifier]['action']
        if identifier == 'SW.CELL.iv_rd_design.Python':
            item['corrected_source_followup'] = ref(IV/'review.json', 'Pinned fit/covariance/diagnostic kernels inspected; coverage remains open')
            item['action'] = read(IV/'review.json')['next_action']
        obligations.append(item)
    assert 'SW.DECISION.inherited_honestdid' not in {r['id'] for r in obligations}
    for name, prefix, total in [('software', 'SW.CELL.', 102), ('reuse', 'SW.DECISION.', 115), ('chapters', 'TEXT.REVIEW.', 22)]:
        selected = {k: v for k, v in results.items() if k.startswith(prefix)}
        groups[name] = dict(Counter(v['outcome'] for v in selected.values()), open=total-len(selected), total=total)
    census_counts = Counter(x['disposition'] for x in read(CENSUS)['items'])
    inspected, unread = census_counts['inspected_primary_retained_with_limits'], census_counts['open_original_not_inspected']
    assert (inspected, unread) == (59, 54)
    count = len(read(PUB/'reader/source-audit.json')['sources'])
    papers = read(PUB/'traceability-review.json')['scholarly_pdfs']
    sponsor_count = len(read(SPONSOR/'source-audit.json')['sources'])
    sections = read(PUB/'release-source-review.json')['checks']['sections']
    BASE.mkdir()
    write(BASE/'state-snapshot.json', state); write(BASE/'status-snapshot.json', view)
    write(BASE/'remaining-operations.json', dict(reader=state['reader'], coverage=groups,
        recorded=view['recorded_proposal_operations'], proposal_operations=view['proposal_operations'],
        ready=view['ready_proposal_operations'], operations=obligations,
        census=ref(CENSUS, 'Every original disposition retained'), proposal_accepted=False))
    by_id = {r['id']: r for r in obligations}
    independent = []
    for lane in ['software', 'commercial', 'reuse', 'llm', 'manuscript', 'release', 'proposal_acceptance']:
        eligible = [n for n in ready if n['lane'] == lane]
        if eligible:
            node = eligible[0]
            independent.append(dict(lane=lane, operation=node['id'], action=by_id.get(node['id'], node)['action'],
                depends=node['depends'], requires_inputs=node['requires_inputs'], output=node['outputs']))
    evidence = [ref(BASE/'state-snapshot.json', 'Canonical snapshot'), ref(BASE/'remaining-operations.json', 'All nonpassing obligations'),
        ref(PUB/'working-release.json', 'Current integrated reader'), ref(SPONSOR/'working-release.json', 'Exact paired sponsor'),
        ref(PUB/'release-source-review.json', 'Preservation and rendered-text review'),
        ref(HD/'review.json', 'Reference-only HonestDiD reuse'), ref(HD/'paper-inspection.json', 'Genuine scholarly original'),
        ref(HD/'omissions-register.json', 'Remaining sensitivity qualification'),
        ref(IV/'review.json', 'Independent Python source progress'), ref(IV/'acquisition-review.json', 'Preserved acquisition attempts')]
    review = dict(status='pass_for_program_consistency_not_completion', reviewer=dict(name='Codex author/coordinator', kind='author'),
        evidence=evidence, effective_lane_counts={k: dict(v) for k, v in lanes.items()}, independent_next_actions=independent,
        findings=[
            'All 376 proposal operations and their nonpassing obligations are reconciled; independent lanes retain actual prerequisites.',
            'HonestDiD receives one passing proposal reuse decision: reference, integration_allowed=false; no native capability follows.',
            'Pinned source, complete top-level MIT terms, genuine Rambachan-Roth paper and selected bridges support the bounded reuse choice.',
            'Python IV progress resolves weighted fits, covariance branches and first-stage distribution semantics; the full IV/RD cell remains open.',
            'The 102 software cells, 115 reuse entries, 22 chapter reviews, 113 originals and four search obligations keep their coverage contracts.',
            'Seven new reader citations preserve every earlier identity/context and compiled input; both exact references reproduce.',
            'The paired sponsor preserves earlier evidence and derives reader/reuse counts from actual artifacts and receipts.',
            'Q2-Q4 bind current reader bytes; Q1/Q5, mandatory repairs and fresh rendered review remain open.',
            'Bank data, independent institutional acceptance and native qualification are conditional later evidence, not global proposal blockers.',
            'Await each canonical mutation; checkpoints are durable recovery artifacts, not permission gates or background workers.'],
        known_routes=[
            'Recover Python RD/CausalPy IV originals and complementary candidates; inspect numerical delegates before native qualification.',
            'Continue 54 frontier originals and failed longitudinal/off-policy/negative searches with explicit saturation limits.',
            'Complete each software/commercial/reuse comparison and reconcile exclusive chapter depth without duplicate credit.',
            'Use generated known-law panels and public data for matched prototype and failure studies before expensive bank work.',
            'Complete fresh rendered review and exact sponsor/reader acceptance only after all mandatory repairs satisfy their contracts.'],
        unresolved_research=[
            'General latent identification and calibrated graph-to-effect uncertainty without additional information.',
            'Arbitrary dependence, hidden-state optimal-policy uncertainty and unrestricted learner remainder control.',
            'Universal calibration of LLM, linkage or diagnostic scores into causal truth.',
            'Actual bank assignment truth, production reliability and measured institutional economics.'],
        global_blocker=None, phase_boundaries_are_stopping_points=False, background_worker_running=False)
    write(BASE/'program-review.json', review)
    write(BASE/'continuation-checkpoint.json', dict(date='2026-10-22', status='reviewed_program_and_integrated_continuation',
        prior_git_commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        state=ref(BASE/'state-snapshot.json', 'Canonical state'), reader=state['reader'],
        sponsor=ref(SPONSOR/'working-release.json', 'Exact paired sponsor'),
        completed=[
            'Recovered saved preparation and passed both baseline recovery checks.',
            'Completed source-grounded reference-only HonestDiD decision; retained solver, environment and release-equivalence limits.',
            'Advanced independent Python IV kernels and preserved four sandbox DNS failures and successful fixed-collector retry.',
            'Reproduced all new mathematical references, compiled paired successors and preserved prior source identities and chapter inputs.',
            'Renewed exact-reader Q2-Q4 and reconciled every nonpassing obligation and independent next action.'],
        evidence=[ref(BASE/'program-review.json', 'Queue-wide review'), ref(PUB/'release-source-review.json', 'Integrated author review')],
        remaining=ref(BASE/'remaining-operations.json', 'Complete remaining register'), next_operation=view['next'],
        next_action=view['next_action'], independent_next_actions=independent, global_blocker=None,
        background_worker_running=False, visual_acceptance=False, proposal_accepted=False))
    current = ROOT/'docs/program/execution/current-program.md'
    (BASE/'prior-current-program.md').write_bytes(current.read_bytes())
    hp = sections['sensitivity']['physical_pages']; ip = sections['python_iv']['physical_pages']
    current.write_text(f'''# Current executable proposal program

Updated 22 October 2026 after the sensitivity reuse and Python IV continuation.
The [queue-wide review](2026-10-22/program-refresh-sensitivity-iv-v1/program-review.json)
binds every nonpassing obligation and independent next action. The goal is a
research and product proposal; bank qualification and adoption are later claims.

Use `python3 tools/run_program_reviews_v2.py status`, `next` and `check`.
The canonical ledger is [state.json](../state.json), governed by the
[proposal scope](../master-program-proposal.md). Earlier numbered masters and
scope execution counts are historical snapshots. Continue across phase boundaries.

## Current integrated documents

Read the [{state['reader']['pages']:,}-page monograph](../../causal_proposal_sensitivity_iv_reviewed_2026-10-22.pdf)
and its [{sponsor['pages']}-page sponsor proposal](../../sponsor_proposal_sensitivity_iv_reviewed_2026-10-22.pdf).
The reader has {count} audited citation records and {papers} genuine scholarly PDFs;
the sponsor has {sponsor_count} audited citations and binds the exact reader bytes.
Q2-Q4 pass. Q1/Q5, all mandatory repairs, rendered review and final acceptance remain open.

There are **{view['recorded_proposal_operations']} recorded outcomes of {view['proposal_operations']} proposal operations**,
with **{view['ready_proposal_operations']} ready operations**. Inconclusive outcomes
remain unfinished obligations; outcome counts do not measure native capabilities.

| Area | Pass | Inconclusive | Open | Total |
|---|---:|---:|---:|---:|
| Software coverage | {groups['software'].get('pass', 0)} | {groups['software'].get('inconclusive', 0)} | {groups['software']['open']} | 102 |
| Reuse decisions | {groups['reuse'].get('pass', 0)} | {groups['reuse'].get('inconclusive', 0)} | {groups['reuse']['open']} | 115 |
| Chapter reviews | {groups['chapters'].get('pass', 0)} | {groups['chapters'].get('inconclusive', 0)} | {groups['chapters']['open']} | 22 |

The frontier census remains **{inspected} inspected and {unread} unread originals out of 113**,
plus four crosscutting obligations. Fourteen LLM-task and twelve integration reviews
have scoped outcomes, without establishing live-model superiority or adoption.

## Integrated findings and reuse choices

Physical pages {hp[0]}-{hp[1]} develop HonestDiD trend restrictions, full-covariance
uncertainty, grid/status limitations and conversion from event-study engines.
The proposal decision is **reference** with **integration_allowed=false**; an
isolated R worker is a future candidate. The pinned source declares 0.2.8, and
the complete top-level MIT terms were inspected. Release equivalence, dependencies,
solver paths, bridges and native calibration retain their own qualification needs.

The known-Gaussian projection example gives effect bounds [-2.9233,10.9233];
a stipulated USD1 cost gives net bounds [-3.9233,9.9233]. This conservative authored
reference does not reproduce optimized package inference or measure bank returns.

Physical pages {ip[0]}-{ip[1]} compare Python IV fit, covariance and diagnostic
semantics. Separate X/Z ranks do not prove projected rank or exclusion. A selected
first-stage helper may display W/k while returning a chi-square p-value; retain
the null, restrictions, covariance, distribution and degrees of freedom through
library/CLI/MCP. An overidentification diagnostic is not coefficient-null inversion.
The Python cell remains open; no downloaded package was executed.

All 915 prior citation identities/contexts and 276 manuscript inputs survive.
Earlier commercial observation, frontier and integration findings remain included.

## Required standard and remaining gaps

Each banking use connects decision, information clock, target, assumptions,
identification or limits, estimation, uncertainty, diagnostics, alternatives and
monetary consequences. Sources need authentic local bytes, identity/version/date,
hashes and inspected anchors; scholarly citations need real PDFs. The cutoff is
7 October 2026. FinMarketing sets scholarly depth; total length is not acceptance.

MR01 requires 17 areas across six dimensions and 100-150 substantive software pages.
MR02 requires eight chapters, fourteen tasks and 96-112 substantive pages. MR03
requires four integration chapters and twelve requirements, with indicative 40-60
pages. Complete coverage and exclusive depth both matter.

Known routes are complementary source recovery, reasoned reuse, connected synthesis
and matched public known-law studies. General hidden-confounder identification,
arbitrary dependence, private-state optimal-policy uncertainty and universal score
calibration require narrower claims or additional information; no solution is promised.

## Exact continuation

Controller next: **{view['next']}**. {view['next_action']}

The [remaining register](2026-10-22/program-refresh-sensitivity-iv-v1/remaining-operations.json)
retains all {len(obligations)} nonpassing obligations and dependencies. The
[checkpoint](2026-10-22/program-refresh-sensitivity-iv-v1/continuation-checkpoint.json)
lists independent next actions. The
[Python continuation](2026-10-22/python-iv-kernels-v1/review.json)
now records inspected rank/fit/covariance/diagnostic delegates. Next recover Python
RD and CausalPy IV originals and complementary candidates; inspect core rank/solver
and remaining covariance/weight guards before any native qualification.

Wait for each canonical mutation before dependent work. Checkpoints and Git
preservation are not permission gates. No global blocker or unattended research
worker exists. The inherited six-preview allowance under `/home/ubuntu/AGENTS.md`
is exhausted; rendered acceptance needs a fresh visual session. Source research,
mathematics and manuscript work remain eligible.
''')
    run.render(ROOT, state)
    print(json.dumps(dict(reader=state['reader'], sponsor_pages=sponsor['pages'], records=count, papers=papers,
        recorded=view['recorded_proposal_operations'], ready=view['ready_proposal_operations'], remaining=len(obligations),
        next=view['next'], proposal_accepted=False)))


if __name__ == '__main__': main()
