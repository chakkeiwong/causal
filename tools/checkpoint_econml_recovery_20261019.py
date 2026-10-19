#!/usr/bin/env python3
"""Preserve current proposal state and publish a concise crash-recovery entrypoint."""
from collections import Counter
import json
from pathlib import Path

import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run = extension.base
ROOT = run.core.ROOT
BASE = ROOT/'docs/program/execution/2026-10-19/recovery-econml-v1'
WORK = ROOT/'docs/program/execution/2026-10-19/econml-reuse-v1'
SPONSOR = ROOT/'docs/program/execution/2026-10-19/sponsor-econml-v1'
COMMERCIAL = ROOT/'docs/program/execution/2026-10-19/commercial-synthetic-comparison-v1'
CENSUS = ROOT/'docs/program/execution/2026-10-19/census-retrieval-selfcorrection-v1/census-register.json'
read = lambda p: json.loads(p.read_text())


def main():
    assert not BASE.exists()
    state = run.core.read(ROOT, run.core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path'] == 'docs/causal_proposal_econml_reviewed_2026-10-19.pdf'
    view = run.status(ROOT, state)
    graph, merged, stages = run.combined(ROOT, state)
    assert {r['id']: r['status'] for r in view['proposal_gaps']} == dict(Q1='open', Q2='pass', Q3='pass', Q4='pass', Q5='open')
    sponsor = read(SPONSOR/'working-release.json')
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
        action = read(ROOT/checkpoints[-1]['path'])['next_action'] if checkpoints else node['action']
        operations.append(dict(id=key, lane=node['lane'], status=result['outcome'] if result else 'open',
            title=node['title'], action=action, prerequisites=run.ledger.blockers(merged, node),
            outputs=node['outputs'], evidence=result, requires_inputs=node['requires_inputs']))
    for name, prefix, total in [('software', 'SW.CELL.', 102), ('reuse', 'SW.DECISION.', 115), ('chapters', 'TEXT.REVIEW.', 22)]:
        selected = {k: v for k, v in results.items() if k.startswith(prefix)}
        groups[name] = dict(Counter(v['outcome'] for v in selected.values()), open=total-len(selected), total=total)
    BASE.mkdir()
    write(BASE/'state-snapshot.json', state)
    write(BASE/'status-snapshot.json', view)
    write(BASE/'remaining-operations.json', dict(reader=state['reader'], recorded=view['recorded_proposal_operations'],
        proposal_operations=view['proposal_operations'], ready=view['ready_proposal_operations'],
        by_lane=dict(Counter(r['lane'] for r in operations)), coverage=groups, operations=operations,
        census=ref(CENSUS, '48 inspected/65 unread of 113'), proposal_accepted=False))
    write(BASE/'recovery-checkpoint.json', dict(status='recovered_and_continued',
        state_snapshot=ref(BASE/'state-snapshot.json', 'Exact canonical state'), current_reader=state['reader'],
        sponsor=ref(SPONSOR/'working-release.json', 'Exact matched sponsor'),
        remaining=ref(BASE/'remaining-operations.json', 'Every effective nonpassing proposal obligation'),
        completed=['Verified the saved 41de9461 baseline, both published PDFs and all seventeen acquired EconML sources.',
            'Completed EconML proposal reference decision, with no executable integration capability.',
            'Integrated exact target, panel-history and sampling examples in preserving paired PDFs; renewed Q2-Q4.',
            'Recorded six-family commercial synthetic-control comparison as inconclusive, with one actual local unsupported request and separate evidence routes.',
            'Continued independent Julia/JavaScript source inspection and exact frontdoor reference preparation.'],
        evidence=[ref(WORK/n, 'Recovery and scientific evidence') for n in ['crash-recovery-checkpoint.json',
            'source-audit.json', 'review.json', 'exact-results.json', 'conversion-contract.json',
            'omissions-register.json', 'working-release.json', 'extracted-page-inspection.json']]+
            [ref(COMMERCIAL/'review.json', 'Commercial criterion findings')],
        next_actions=[view['next']+': '+view['next_action'],
            'Continue prepared Julia/JavaScript source review; distinguish graphical manipulation, adjustment, frontdoor, general identification and path-specific scope.',
            'Keep five missing synthetic-control vendor families open; use authentic permitted originals and never infer absence from rejected acquisition.',
            'Finish the remaining software/reuse and 65 unread census originals, then reconcile all mandatory repair contracts and full-reader acceptance.'],
        global_blocker=None, visual_acceptance=False, proposal_accepted=False, background_worker_running=False))
    path = ROOT/'docs/program/execution/current-program.md'
    (BASE/'prior-current-program.md').write_bytes(path.read_bytes())
    audit = read(WORK/'reader/source-audit.json')
    papers = read(WORK/'traceability-review.json')['scholarly_pdfs']
    text = f'''# Current executable proposal program

Updated 19 October 2026 after machine-crash recovery. The current deliverable is a
research and product proposal. A completed proposal, working prototype, independent
acceptance, bank validation and adoption are separate outcomes.

Use `python3 tools/run_program_reviews_v2.py status`, `next` and `check`.
The canonical ledger is [state.json](../state.json); the [proposal scope](../master-program-proposal.md)
governs this work. Earlier numbered programs are preserved historical records.

## Current deliverables and completion

The [{state['reader']['pages']:,}-page working monograph](../../causal_proposal_econml_reviewed_2026-10-19.pdf)
and [{sponsor['pages']}-page sponsor proposal](../../sponsor_proposal_econml_reviewed_2026-10-19.pdf)
are paired by exact hashes. The reader contains {len(audit['sources'])} audited citation records
and {papers} genuine scholarly PDFs. Q2-Q4 pass for these exact reader bytes.
Q1/Q5, the three mandatory repair rollups, rendered visual review and final acceptance remain open.

There are **{view['recorded_proposal_operations']} recorded outcomes of {view['proposal_operations']} proposal operations**,
with **{view['ready_proposal_operations']} ready**. Recorded inconclusive outcomes retain unmet obligations.

| Area | Pass | Inconclusive | Open | Total |
|---|---:|---:|---:|---:|
| Software coverage | {groups['software'].get('pass',0)} | {groups['software'].get('inconclusive',0)} | {groups['software']['open']} | 102 |
| Reuse decisions | {groups['reuse'].get('pass',0)} | {groups['reuse'].get('inconclusive',0)} | {groups['reuse']['open']} | 115 |
| Chapter reviews | {groups['chapters'].get('pass',0)} | {groups['chapters'].get('inconclusive',0)} | {groups['chapters']['open']} | 22 |

The original-candidate census remains 48 inspected and 65 unread out of 113.
L1/L6 coverage remains incomplete. Fourteen LLM task reviews and twelve integration
requirements have bounded proposal outcomes; they do not establish runtime or adoption.

## Recovery findings and completed work

The saved baseline and published PDFs survived the crash. EconML's seventeen selected
originals authenticate to the pre-cutoff commit. Its proposal reference decision passes
without executable integration permission. The added argument separates the residual
projection from population effect, panel chronology from row order, and fold grouping
from the covariance and resampling experiment. Exact assumed-money examples reproduce.
The inspected dynamic bootstrap composition samples rows inside fixed units; native
conformance remains proposed, and no measured coverage defect is claimed.

The six-family commercial synthetic-control comparison is inconclusive. Only selected
community code inside Stata has matching technical originals; five other families remain
unresolved. One actual dependent-panel request to the local common dispatcher returned
unsupported. Prices, exact entitlements and source/plugin rights remain unknown. Each
family has its own public-evidence route; these gaps do not stop other eligible work.

## Required standard and remaining work

Connect every banking decision and information clock to assumptions, identification or
limits, estimation, uncertainty, diagnostics and monetary consequences. Distinguish inherited
results, authored derivations, synthetic examples and verified implementation. Bind cited
originals to identity, version/date, local bytes, SHA-256, inspected anchors and supported
claims. Every scholarly citation needs a genuine PDF. The literature cutoff is 7 October 2026.
FinMarketing supplies the scholarship standard; aggregate page count does not establish quality.

MR01 requires 17 areas across six language/commercial dimensions and 100-150 substantive
software pages. MR02 requires eight developed chapters, fourteen tasks and approximately
100 pages (the current depth contract is 96-112). MR03 requires four developed integration
chapters and twelve requirements, with indicative depth 40-60 pages. Coverage and argument
must pass alongside depth, with no duplicate page credit.

Known next steps are the remaining primary-source reviews, vendor comparisons, justified
reuse choices, frontier census and full-reader reconciliation. General hidden-confounder
identification, arbitrary dependence, private-state policy inference and universal calibration
remain research uncertainties. Authentic bank truth, target-platform trials, independent
institutional acceptance and observed economics are later conditional gates. Public and
generated evidence can justify whether those expensive trials are worthwhile.

## Exact continuation

Next: **{view['next']}**. {view['next_action']}

Seven pinned Julia files and inherited DAGitty originals are already acquired. Inspection
and an exact frontdoor example have begun. Complete their source/target/status review,
then integrate a connected successor and continue the queue. Native EconML admission later
requires exact environment/notices, target and keyed-history checks, weight refusal,
resampling conformance and declared-law evaluation; the proposal choice itself is complete.

[Every nonpassing obligation](2026-10-19/recovery-econml-v1/remaining-operations.json)
· [Recovery evidence](2026-10-19/recovery-econml-v1/recovery-checkpoint.json)
· [Preserved preceding program](2026-10-19/recovery-econml-v1/prior-current-program.md)

Independent ready work continues across phase boundaries. Checkpoints are restart records,
not permission gates. Use short commands and bounded output. No unattended worker runs.
The inherited image allowance is exhausted under `/home/ubuntu/AGENTS.md`; rendered
review remains pending and does not stop source, mathematical or manuscript work.
'''
    path.write_text(text)
    print(json.dumps(dict(reader=state['reader'], sponsor=sponsor['pdf'],
        recorded=view['recorded_proposal_operations'], ready=view['ready_proposal_operations'],
        next=view['next'], coverage=groups, proposal_accepted=False)))


if __name__ == '__main__':
    main()
