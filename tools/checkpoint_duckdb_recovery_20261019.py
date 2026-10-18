#!/usr/bin/env python3
"""Snapshot effective remaining work and refresh the human continuation entrypoint."""
from collections import Counter
import json
from pathlib import Path

import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-19/recovery-duckdb-v1'
SOURCE=ROOT/'docs/program/execution/2026-10-18/census-biomedical-reasoning-v1'
SPONSOR=ROOT/'docs/program/execution/2026-10-19/sponsor-duckdb-v1'
run=extension.base


def read(path):
    return json.loads(path.read_text())


def main():
    assert BASE.exists() and not (BASE/'state-snapshot.json').exists()
    state=run.core.read(ROOT,run.core.STATE)
    assert state['execution_runtime']['active'] is None
    view=run.status(ROOT,state)
    graph,merged,stages=run.combined(ROOT,state)
    results=merged['execution_program']['results']
    assert state['reader']['pages']==1083
    assert {r['id']:r['status'] for r in view['proposal_gaps']}==dict(Q1='open',Q2='pass',Q3='pass',Q4='pass',Q5='open')
    verify_bindings(read(SPONSOR/'working-release.json'))
    assert run.same_reader(state['reader'],read(SPONSOR/'working-release.json')['paired_monograph'])
    register=read(SOURCE/'census-register.json')
    assert register['counts']['inspected_primary_retained_with_limits']==44
    assert register['counts']['open_original_not_inspected']==69
    operations=[]
    for node in graph['nodes']:
        key=node['id']
        if stages[key]!='proposal_now':continue
        result=results.get(key)
        if result and result['outcome']=='pass':continue
        checkpoints=merged['execution_program']['progress'].get(key,[])
        action=read(ROOT/checkpoints[-1]['path'])['next_action'] if checkpoints else node['action']
        operations.append(dict(id=key,lane=node['lane'],status=result['outcome'] if result else 'open',
            title=node['title'],action=action,prerequisites=run.ledger.blockers(merged,node),
            outputs=node['outputs'],evidence=result,requires_inputs=node['requires_inputs']))
    groups={}
    for label,prefix,total in [('software','SW.CELL.',102),('reuse','SW.DECISION.',115),('chapters','TEXT.REVIEW.',22)]:
        selected={k:v for k,v in results.items() if k.startswith(prefix)}
        groups[label]=dict(Counter(v['outcome'] for v in selected.values()),open=total-len(selected),total=total)
    BASE.mkdir(exist_ok=True)
    write(BASE/'state-snapshot.json',state)
    write(BASE/'status-snapshot.json',view)
    write(BASE/'remaining-operations.json',dict(reader=state['reader'],
        recorded=view['recorded_proposal_operations'],proposal_operations=view['proposal_operations'],
        ready=view['ready_proposal_operations'],by_lane=dict(Counter(x['lane'] for x in operations)),
        coverage=groups,operations=operations,census=ref(SOURCE/'census-register.json','44inspected/69unread'),
        scope='Every nonpassing effective proposal obligation; conditional later bank/product gates excluded.',
        proposal_accepted=False))
    write(BASE/'recovery-checkpoint.json',dict(status='recovered_and_continued',
        canonical_state_snapshot=ref(BASE/'state-snapshot.json','Immutable ledger snapshot after DuckDB publication and commercial panel comparison'),
        current_reader=state['reader'],sponsor=ref(SPONSOR/'working-release.json','Paired15-page66-record sponsor'),
        remaining=ref(BASE/'remaining-operations.json','Every nonpassing proposal operation and actual prerequisites'),
        completed=['Recovered the pending DuckDB source review and authenticated23 original blobs at historical v1.4.0.',
            'Recorded a bounded preferred proposal route with executable admission deferred; no native execution or integration capability.',
            'Integrated population, missingness, joins, clocks and controls in1083-page786-record203-paper monograph.',
            'Preserved784 prior source records,239 compiled inputs and every prior citation context; source/math/text checks pass.',
            'Renewed exact-reader Q2-Q4 and published paired15-page66-citation sponsor preserving62 prior identities.',
            'Continued into six-family commercial panel comparison; recorded inconclusive edition/source/rights coverage and concrete follow-ups.'],
        failures_and_repairs=[ref(ROOT/'docs/program/execution/2026-10-19/duckdb-reuse-v1/acquisition-review.json','Preserved inherited403, missing-path404 and sandbox DNS failures'),
            ref(ROOT/'docs/program/execution/2026-10-19/duckdb-reuse-v1/reader/text-layout-review.json','Original extraction controls retained; text-bound review is not visual acceptance')],
        next_actions=[view['next']+': '+view['next_action'],
            'Continue public edition/source/rights research for six commercial panel families; unknown is not absent.',
            'Continue literature census44/69; next survey pair candidates18 and20; preserve original and citation-chain denominators.',
            'Close L1/L6 coverage, mandatory repair rollups and release reconciliation; fresh image allowance is needed only for visual acceptance.',
            'Retain institutional truth, platform qualification and adoption as later conditional work.'],
        global_blocker=None,visual_acceptance=False,proposal_accepted=False,background_worker_running=False))
    path=ROOT/'docs/program/execution/current-program.md'
    old=path.read_text()
    (BASE/'prior-current-program.md').write_text(old)
    header=f'''# Current executable proposal program

## Crash recovery continued on 19 October 2026

Use **python3 tools/run_program_reviews_v2.py status**, **next**, and **check**.
The canonical ledger is docs/program/state.json. The [proposal scope](../master-program-proposal.md)
governs this deliverable; older numbered controllers remain historical views.

The current [1,083-page monograph](../../causal_proposal_duckdb_reviewed_2026-10-19.pdf)
is paired with the [15-page sponsor brief](../../sponsor_proposal_duckdb_reviewed_2026-10-19.pdf).
It has 786 audited citation records and 203 genuine scholarly PDFs. All 784 predecessor
records, their citation contexts and 239 unchanged compiled inputs survive. Q2–Q4 pass
for these exact reader bytes. Source, arithmetic and all-page text-bound checks pass;
visual and final proposal acceptance remain open.

The recovered DuckDB review authenticates 23 selected source files at historical v1.4.0.
Its bounded proposal choice retains the original engine for typed local preparation and
defers executable admission. The new section connects missingness, join weighting,
information clocks and execution controls to exact descriptive banking examples. It
makes no native-engine, distribution-rights, causal-effect or bank-ROI claim. The next
six-family commercial panel comparison is recorded as inconclusive: selected Stata and
introductory EViews evidence cannot close every edition/source/rights obligation.

There are **{view['recorded_proposal_operations']} recorded outcomes among {view['proposal_operations']} proposal operations**,
with **{view['ready_proposal_operations']} ready**. Recorded inconclusive outcomes are not closed gaps.
Software: 2 pass, 23 inconclusive, 77 open of 102. Reuse: 17 pass, 3 inconclusive,
95 open of 115. Chapters: 20 pass, 2 inconclusive of 22; L1 and L6 are incomplete.
The original literature census remains 44 inspected and 69 unread of 113. Four
crosscutting records and three citation-chain leads keep separate denominators.
All 14 LLM task reviews and 12 integration requirements have bounded proposal outcomes,
not general runtime or bank qualification.

### Required standard and remaining gates

Retain a developed scholarly argument, explained notation and assumptions, derivations,
diagnostics, substantive alternatives, reproducible banking examples, authentic scholarly
PDFs and source identity/version/SHA-256/anchor audits. The cutoff is 7 October 2026;
page count alone earns no acceptance. MR01 covers 17 areas by 6 language/commercial
dimensions and 100–150 substantive pages. MR02 covers 8 chapters, 14 tasks and 96–112
substantive pages. MR03 covers 4 chapters, 12 requirements and indicative 40–60 pages.
All three repair rollups, Q1/Q5, release reconciliation and final acceptance remain open.
A proposal may retain bounded negative scientific findings without claiming an accepted product.

### Exact continuation

The fair queue selects **{view['next']}**. {view['next_action']}
Commercial panel follow-ups remain independently actionable: bind dated Stata edition
and StataNow options, full EViews estimator/diagnostic originals, and applicable originals
for SAS, IBM, MathWorks and commercial open-source frontends. Record actual public prices
or unavailable status; no vendor trial or purchase has occurred.

Continue LL.CENSUS with candidates 18 (evaluation survey, arXiv2307.03109) and 20
(code-generation survey, arXiv2406.00515), inspecting selected pre-cutoff primary revisions.
Unrestricted latent identification, joint dependence, hidden-state policy and arbitrary
learner guarantees remain open research; no universal successful repair is promised.

[Every nonpassing operation and prerequisite](2026-10-19/recovery-duckdb-v1/remaining-operations.json)
· [Recovery checkpoint](2026-10-19/recovery-duckdb-v1/recovery-checkpoint.json)
· [Original literature census](2026-10-18/census-biomedical-reasoning-v1/census-register.json)

Independent tasks do not wait for bank truth or paid trials. Rendered visual review alone
requires a fresh image allowance under /home/ubuntu/AGENTS.md; no images were forwarded
in this recovery. Use short commands and durable receipts. Checkpoints are not approval
gates and no unattended research worker is running.

---

## Preserved earlier continuation records

'''
    path.write_text(header+old)
    verify_bindings(read(BASE/'recovery-checkpoint.json'))
    print(json.dumps(dict(recorded=view['recorded_proposal_operations'],ready=view['ready_proposal_operations'],
        nonpassing=len(operations),coverage=groups,current_program=str(path.relative_to(ROOT)))))


if __name__=='__main__':
    main()
