#!/usr/bin/env python3
"""Preserve a crash-resumable checkpoint for the paired Feast proposal."""
from collections import Counter
import json
from pathlib import Path

import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run = extension.base
ROOT = run.core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-19/recovery-feast-v1'
WORK = ROOT / 'docs/program/execution/2026-10-19/feast-reuse-v1'
SPONSOR = ROOT / 'docs/program/execution/2026-10-19/sponsor-feast-v1'
CENSUS = ROOT / 'docs/program/execution/2026-10-19/census-hidden-reasoning-v1/census-register.json'
read = lambda p: json.loads(p.read_text())


def main():
    assert not BASE.exists()
    state = run.core.read(ROOT, run.core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path'] == 'docs/causal_proposal_feast_reviewed_2026-10-19.pdf'
    view = run.status(ROOT, state)
    graph, merged, stages = run.combined(ROOT, state)
    assert {r['id']: r['status'] for r in view['proposal_gaps']} == dict(Q1='open', Q2='pass', Q3='pass', Q4='pass', Q5='open')
    sponsor = read(SPONSOR / 'working-release.json')
    verify_bindings(sponsor)
    assert run.same_reader(state['reader'], sponsor['paired_monograph'])
    results = merged['execution_program']['results']
    operations, groups = [], {}
    for node in graph['nodes']:
        key = node['id']
        result = results.get(key)
        if stages[key] != 'proposal_now' or result and result['outcome'] == 'pass':
            continue
        checkpoints = merged['execution_program']['progress'].get(key, [])
        action = read(ROOT / checkpoints[-1]['path'])['next_action'] if checkpoints else node['action']
        operations.append(dict(id=key, lane=node['lane'], status=result['outcome'] if result else 'open',
            title=node['title'], action=action, prerequisites=run.ledger.blockers(merged, node),
            outputs=node['outputs'], evidence=result, requires_inputs=node['requires_inputs']))
    for name, prefix, total in [('software', 'SW.CELL.', 102), ('reuse', 'SW.DECISION.', 115), ('chapters', 'TEXT.REVIEW.', 22)]:
        selected = {k: v for k, v in results.items() if k.startswith(prefix)}
        groups[name] = dict(Counter(v['outcome'] for v in selected.values()), open=total-len(selected), total=total)
    BASE.mkdir()
    write(BASE / 'state-snapshot.json', state)
    write(BASE / 'status-snapshot.json', view)
    write(BASE / 'remaining-operations.json', dict(reader=state['reader'], recorded=view['recorded_proposal_operations'],
        proposal_operations=view['proposal_operations'], ready=view['ready_proposal_operations'],
        by_lane=dict(Counter(r['lane'] for r in operations)), coverage=groups, operations=operations,
        census=ref(CENSUS, '49 inspected / 64 unread of 113'), proposal_accepted=False))
    evidence = [ref(WORK / n, 'Reviewed Feast proposal evidence') for n in
        ['source-audit.json', 'review.json', 'exact-results.json', 'identity-review.json',
         'conversion-contract.json', 'working-release.json', 'release-source-review.json']]
    write(BASE / 'recovery-checkpoint.json', dict(status='recovered_and_continued',
        state_snapshot=ref(BASE / 'state-snapshot.json', 'Exact canonical state'), current_reader=state['reader'],
        sponsor=ref(SPONSOR / 'working-release.json', 'Exact matched sponsor'),
        remaining=ref(BASE / 'remaining-operations.json', 'Every effective nonpassing proposal obligation'),
        completed=['Verified recovery commit 3cff35f8dd4960841b6fc74c8c7bc7c8d148ed10 on origin/main.',
            'Authenticated 20 Feast source blobs to the selected cutoff commit and complete tree.',
            'Recorded a conditional reuse choice with executable admission deferred.',
            'Integrated exact availability-clock examples and distinct historical/online/MCP contracts.',
            'Preserved 807 prior citation records and 249 compiled inputs; renewed exact-reader Q2-Q4.'],
        evidence=evidence, next_actions=[view['next'] + ': ' + view['next_action'],
            'Continue independently eligible software and frontier-original reviews; preserve unresolved acquisition routes.',
            'Keep mandatory repair rollups and rendered visual/final acceptance open.'],
        global_blocker=None, visual_acceptance=False, proposal_accepted=False, background_worker_running=False))
    path = ROOT / 'docs/program/execution/current-program.md'
    (BASE / 'prior-current-program.md').write_bytes(path.read_bytes())
    audit = read(WORK / 'reader/source-audit.json')
    papers = read(WORK / 'traceability-review.json')['scholarly_pdfs']
    text = f'''# Current executable proposal program

Updated 19 October 2026 after crash recovery and the Feast proposal review. This
is a research and product proposal; prototype qualification, independent review,
bank validation and adoption are distinct outcomes.

Use `python3 tools/run_program_reviews_v2.py status`, `next` and `check`.
The canonical ledger is [state.json](../state.json), governed by the
[proposal scope](../master-program-proposal.md). Earlier numbered programs are
preserved historical records. Checkpoints are restart records, not permission gates.

## Current deliverables and status

The [{state['reader']['pages']:,}-page working monograph](../../causal_proposal_feast_reviewed_2026-10-19.pdf)
and [{sponsor['pages']}-page sponsor proposal](../../sponsor_proposal_feast_reviewed_2026-10-19.pdf)
are paired by exact hashes. The reader contains {len(audit['sources'])} audited
citation records and {papers} genuine scholarly PDFs. Q2-Q4 pass for these exact
reader bytes. Q1/Q5, mandatory repair rollups, visual review and final acceptance
remain open.

There are **{view['recorded_proposal_operations']} recorded outcomes of {view['proposal_operations']} proposal operations**,
with **{view['ready_proposal_operations']} ready**. An inconclusive outcome preserves
its unmet obligations; a recorded outcome is not automatically a closed gap.

| Area | Pass | Inconclusive | Open | Total |
|---|---:|---:|---:|---:|
| Software coverage | {groups['software'].get('pass',0)} | {groups['software'].get('inconclusive',0)} | {groups['software']['open']} | 102 |
| Reuse decisions | {groups['reuse'].get('pass',0)} | {groups['reuse'].get('inconclusive',0)} | {groups['reuse']['open']} | 115 |
| Chapter reviews | {groups['chapters'].get('pass',0)} | {groups['chapters'].get('inconclusive',0)} | {groups['chapters']['open']} | 22 |

The original census remains 49 inspected and 64 unread out of 113. L1/L6 frontier
and framework coverage remains incomplete. Fourteen task reviews and twelve
integration requirements have bounded proposal outcomes, not runtime adoption.

## Recovery and completed continuation

The recovered identification and COAT publications are committed and verified
on origin/main as 3cff35f8dd4960841b6fc74c8c7bc7c8d148ed10. This continuation
authenticates twenty Feast source blobs at a selected 7 October revision.
Creation filtering exists and is provider-dependent; its field must represent
actual availability before it can reconstruct decision information. The exact
finite example gives USD 15 for an unavailable type-dependent rule and USD 0
for every feasible rule under the stipulated information. Historical retrieval,
latest online access and state-changing MCP tools have distinct contracts.
No native Feast runtime, complete distribution rights or executable admission
is claimed. The new argument is at physical PDF pages 571-574.

The earlier Julia/JavaScript identification and COAT source-critical arguments
remain intact. Their proof, native-conformance and census limits remain open.
Candidate 167's ACL route was rejected by the fixed collector; the preserved
failure is not evidence that the original does not exist. Six-family commercial
synthetic-control comparison remains inconclusive; only selected community code
inside one host has matched technical originals, and exact entitlements, prices
and source/plugin rights remain unresolved.

## Required standard and unresolved work

Connect each banking decision and information clock to assumptions, identification
or limits, estimation, uncertainty, diagnostics, alternatives and monetary
consequences. Distinguish inherited results, authored derivations, generated
examples and verified implementation. Bind cited originals to identity, date or
version, local bytes, SHA-256, inspected anchors and supported claims. Scholarly
citations require genuine PDFs. The client literature cutoff is 7 October 2026.
FinMarketing supplies the scholarship standard; page count is not acceptance.

MR01 requires 17 areas across six dimensions and 100-150 substantive software
pages. MR02 requires eight developed chapters, fourteen tasks and approximately
100 pages (the depth contract is 96-112). MR03 requires four integration chapters
and twelve requirements, with indicative depth 40-60 pages. Coverage and argument
must pass alongside depth, with no duplicate page credit.

We know the public-evidence routes for remaining original reviews, commercial
comparisons, justified reuse choices, the frontier census and reader reconciliation.
General hidden-confounder identification, arbitrary dependence, private-state
policy inference and universal calibration remain research uncertainties.
Authentic bank truth, platform trials, independent institutional acceptance and
observed economics are later conditional gates. Public/generated evidence can
justify whether those expensive trials are worthwhile.

## Exact continuation

Next: **{view['next']}**. {view['next_action']}

Continue the commercial dynamic-panel/time-series cell using existing authentic
originals and narrowly selected additional technical manuals. Independent ready
items continue across phase boundaries; one missing source does not stop others.

[Every nonpassing obligation](2026-10-19/recovery-feast-v1/remaining-operations.json)
· [Recovery checkpoint](2026-10-19/recovery-feast-v1/recovery-checkpoint.json)
· [Preserved prior program](2026-10-19/recovery-feast-v1/prior-current-program.md)

Use short commands and bounded text output. No unattended worker is running.
The inherited image allowance is exhausted under `/home/ubuntu/AGENTS.md`;
rendered review remains pending and does not stop source or manuscript work.
'''
    path.write_text(text)
    run.render(ROOT, state)
    print(json.dumps(dict(recorded=view['recorded_proposal_operations'], ready=view['ready_proposal_operations'],
        next=view['next'], reader_pages=state['reader']['pages'], sponsor_pages=sponsor['pages'])))


if __name__ == '__main__':
    main()
