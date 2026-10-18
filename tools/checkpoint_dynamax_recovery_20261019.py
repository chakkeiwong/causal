#!/usr/bin/env python3
"""Snapshot effective remaining work and refresh the human continuation entrypoint."""
from collections import Counter
import json
from pathlib import Path

import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-19/recovery-dynamax-v1'
SOURCE=ROOT/'docs/program/execution/2026-10-19/census-evaluation-code-v1'
SPONSOR=ROOT/'docs/program/execution/2026-10-19/sponsor-dynamax-v2'
run=extension.base


def read(path):
    return json.loads(path.read_text())


def main():
    assert not BASE.exists()
    state=run.core.read(ROOT,run.core.STATE)
    assert state['execution_runtime']['active'] is None
    view=run.status(ROOT,state)
    graph,merged,stages=run.combined(ROOT,state)
    results=merged['execution_program']['results']
    assert state['reader']['path']=='docs/causal_proposal_dynamax_reviewed_v2_2026-10-19.pdf'
    assert {r['id']:r['status'] for r in view['proposal_gaps']}==dict(Q1='open',Q2='pass',Q3='pass',Q4='pass',Q5='open')
    verify_bindings(read(SPONSOR/'working-release.json'))
    assert run.same_reader(state['reader'],read(SPONSOR/'working-release.json')['paired_monograph'])
    register=read(SOURCE/'census-register.json')
    assert register['counts']['inspected_primary_retained_with_limits']==46
    assert register['counts']['open_original_not_inspected']==67
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
        coverage=groups,operations=operations,census=ref(SOURCE/'census-register.json','46inspected/67unread'),
        scope='Every nonpassing effective proposal obligation; conditional later bank/product gates excluded.',
        proposal_accepted=False))
    write(BASE/'recovery-checkpoint.json',dict(status='recovered_and_continued',
        canonical_state_snapshot=ref(BASE/'state-snapshot.json','Immutable ledger snapshot after Dynamax reader and sponsor publication'),
        current_reader=state['reader'],sponsor=ref(SPONSOR/'working-release.json','Paired current Dynamax sponsor'),
        remaining=ref(BASE/'remaining-operations.json','Every nonpassing proposal operation and actual prerequisites'),
        completed=['Recovered the pushed Java/DuckDB baseline and completed the interrupted historical-survey tranche.',
            'Published the1089-page evaluation/code reader and17-page paired sponsor with791 citations and205 genuine scholarly PDFs.',
            'Reconciled original census46inspected/67unread; preserved all prior citation identities and contexts.',
            'Continued the independent Dynamax lane with12authenticated pinned source blobs, exact private-logger/clock examples and a bounded proposal selection deferring executable admission.',
            'Integrated the Dynamax argument into another preserving reader/sponsor pair and renewed Q2-Q4.'],
        failures_and_repairs=[ref(SOURCE/'review-attempt-1/failure-review.json','Preserved initial source-review generation failure'),
            ref(SOURCE/'recovery-transport-review.json','Corrected bounded transport/generator failures'),
            ref(ROOT/'docs/program/execution/2026-10-19/dynamax-reuse-v1/tree-identity-failure.json','Preserved tree-identity mismatch; resolved by exact tree/commit acquisition'),
            ref(ROOT/'docs/program/execution/2026-10-19/dynamax-reuse-v1/identity-review.json','Authenticated exact tree and12source blobs'),
            ref(ROOT/'docs/program/execution/2026-10-19/dynamax-reuse-v1/reader-build-failure-review.json','Preserved equation overflow and versioned repair'),
            ref(ROOT/'docs/program/execution/2026-10-19/dynamax-reuse-v1/publication-v2/revision-review.json','Equation-only revision'),
            ref(ROOT/'docs/program/execution/2026-10-19/dynamax-reuse-v1/recovery-followup-errors.json','Transport and exploratory errors corrected before admission'),
            ref(ROOT/'docs/program/execution/2026-10-19/sponsor-dynamax-v1/date-review.json','Inherited running date corrected in preserving sponsor v2')],
        next_actions=[view['next']+': '+view['next_action'],
            'Continue67unread census originals and search-specificity/saturation review; candidate254 retrieval survey and32 self-correcting code study are concrete leads.',
            'Dynamax executable admission remains deferred pending resolved dependencies/notices, native conformance, logger/clock contracts and parameter uncertainty.',
            'Retain unresolved Java proof/helpers, commercial source/edition/rights and reuse coverage.',
            'Reconcile mandatory repairs and rendered visual acceptance without imposing later bank-data gates.'],
        global_blocker=None,visual_acceptance=False,proposal_accepted=False,background_worker_running=False))
    path=ROOT/'docs/program/execution/current-program.md'
    old=path.read_text()
    (BASE/'prior-current-program.md').write_text(old)
    pages=state['reader']['pages']
    sponsor_pages=read(SPONSOR/'working-release.json')['pages']
    header=f'''# Current executable proposal program

## Crash recovery continued on 19 October 2026: Dynamax reuse and paired publication

Use **python3 tools/run_program_reviews_v2.py status**, **next**, and **check**.
The canonical ledger is docs/program/state.json. The [proposal scope](../master-program-proposal.md)
governs this deliverable; older numbered controllers and entries below are historical views.

The current [{pages:,}-page monograph](../../causal_proposal_dynamax_reviewed_v2_2026-10-19.pdf)
is paired with the [{sponsor_pages}-page sponsor brief](../../sponsor_proposal_dynamax_reviewed_v2_2026-10-19.pdf).
It contains 793 audited citation records and 205 genuine scholarly PDFs. All 791 predecessor
identities and citation contexts survive. Q2–Q4 pass for the exact current reader. Source,
exact arithmetic and all-page text-bound checks pass. Visual and final acceptance remain open.

Recovery completed the two historical evaluation/code surveys and advanced the original census
to46 inspected/67 unread. It then continued the independent Dynamax reuse lane. Twelve pinned
originals establish bounded conditional-likelihood, private-logger, input-clock, numerical,
parameter and dependency distinctions. Exact authored examples demonstrate an observed
contrast12/25 with zero intervention effect, and filtering1/5 versus future-informed smoothing1/2.
The proposal retains the original engine as a conditional comparator and defers executable
admission. These are source and synthetic findings, not native qualification or bank ROI.

There are **{view['recorded_proposal_operations']} recorded outcomes among {view['proposal_operations']} proposal operations**,
with **{view['ready_proposal_operations']} ready**. Inconclusive does not mean closed.
Software coverage: 2 pass, 24 inconclusive, 76 open of 102. Reuse: 18 pass,
3 inconclusive, 94 open of 115. Chapters: 20 pass and 2 inconclusive of 22;
L1 and L6 are incomplete. The original census remains 46 inspected and 67 unread
of 113; four crosscutting records and three citation-chain leads retain separate
denominators. All 14 LLM task reviews and 12 integration requirements have bounded
proposal outcomes, not general runtime or bank qualification.

### Required standard

A developed scholarly argument must connect banking question, clocks and units to causal
assumptions, identification or its limits, estimation, uncertainty, diagnostics and economic
consequences. Retain genuine scholarly PDFs and audited primary identity/version/SHA-256/
anchors, substantive alternatives and reproducible examples. The cutoff is 7 October 2026.
MR01 spans 17 areas by 6 language/commercial dimensions and 100–150 substantive pages.
MR02 spans 8 chapters, 14 tasks and 96–112 substantive pages. MR03 spans 4 chapters,
12 requirements and indicative 40–60 pages. Length and repeated text do not close coverage.
All three repair rollups, Q1/Q5, full reconciliation and final acceptance remain open.

### Executable continuation and remaining uncertainty

The fair queue selects **{view['next']}**: {view['next_action']}
The new census preserves46 inspected and67 unread originals. Candidate254 retrieval-augmented
generation survey and candidate32 self-correcting data-science code study remain concrete
acquisition/inspection leads. Record original version and adverse results before using them.
The Dynamax proposal decision is recorded. Native conformance, a resolved dependency/right
inventory and regime-specific scientific qualification remain separate executable-admission work.

Java follow-ups: acquire and inspect the algorithm proof named by the source, graph/legal
and probability-storage helpers, and other Java candidates. No general ID/IDC, cross-world
or partial-identification capability follows from the selected interfaces. Keep failed
candidate, sentinel, subtype and nonfinite paths in a future native conformance protocol.
Commercial panel follow-ups: dated edition/options, full EViews technical originals,
applicable SAS/IBM/MathWorks/commercial-hosting paths, rights and authentic price evidence.
Unrestricted hidden-confounder identification, joint dependence, hidden-state policy and
arbitrary-learner guarantees remain open scientific questions with no promised universal repair.

[Every nonpassing operation](2026-10-19/recovery-dynamax-v1/remaining-operations.json)
· [Recovery checkpoint](2026-10-19/recovery-dynamax-v1/recovery-checkpoint.json)
· [Original literature census](2026-10-19/census-evaluation-code-v1/census-register.json)

Independent public research and synthetic prototype design continue without bank truth
or paid production trials. The inherited image allowance is exhausted, affecting only
rendered visual review; no images were forwarded. Checkpoints are durable restart records,
not permission gates. Use short commands and bounded outputs; no unattended worker runs.

---

## Preserved earlier continuation records

'''
    path.write_text(header+old)
    verify_bindings(read(BASE/'recovery-checkpoint.json'))
    print(json.dumps(dict(recorded=view['recorded_proposal_operations'],ready=view['ready_proposal_operations'],
        nonpassing=len(operations),coverage=groups,current_program=str(path.relative_to(ROOT)))))


if __name__=='__main__':
    main()
