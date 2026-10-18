#!/usr/bin/env python3
"""Snapshot effective remaining work and refresh the human continuation entrypoint."""
from collections import Counter
import json
from pathlib import Path

import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-18/recovery-agent-reasoning-v1'
SOURCE=ROOT/'docs/program/execution/2026-10-18/census-biomedical-reasoning-v1'
SPONSOR=ROOT/'docs/program/execution/2026-10-18/sponsor-agent-reasoning-v1'
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
    assert state['reader']['pages']==1080
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
    BASE.mkdir()
    write(BASE/'state-snapshot.json',state)
    write(BASE/'status-snapshot.json',view)
    write(BASE/'remaining-operations.json',dict(reader=state['reader'],
        recorded=view['recorded_proposal_operations'],proposal_operations=view['proposal_operations'],
        ready=view['ready_proposal_operations'],by_lane=dict(Counter(x['lane'] for x in operations)),
        coverage=groups,operations=operations,census=ref(SOURCE/'census-register.json','44inspected/69unread'),
        scope='Every nonpassing effective proposal obligation; conditional later bank/product gates excluded.',
        proposal_accepted=False))
    write(BASE/'recovery-checkpoint.json',dict(status='recovered_and_continued',
        canonical_state_snapshot=ref(BASE/'state-snapshot.json','Immutable ledger snapshot after both new publication pairs'),
        current_reader=state['reader'],sponsor=ref(SPONSOR/'working-release.json','Paired14-page62-record sponsor'),
        remaining=ref(BASE/'remaining-operations.json','Every nonpassing proposal operation and actual prerequisites'),
        completed=['Recovered pending Python reader publication without repeating it; renewed Q2-Q4 and published14-page56-record sponsor.',
            'Inspected two authentic pre-cutoff originals; preserved source errors and changed only candidates46/115 in the original census.',
            'Integrated source-critical causal-agent discussion and exact structural servicing example in1080-page784-record203-paper successor.',
            'Preserved all781 predecessor records,238 unchanged compiled inputs and all prior citation contexts; source/math/text checks passed.',
            'Renewed Q2-Q4 and published exact-reader14-page62-record sponsor, preserving56 prior records and prior substantive sections.'],
        failures_and_repairs=[ref(SOURCE/'prepare-attempt-1/failure-review.json','Manifest activation failure preserved and repaired'),
            ref(SOURCE/'sandbox-failures/exec18_census_biomedical_v1.receipt.json','Sandbox DNS failure preserved before approved public collector retry'),
            ref(ROOT/'docs/program/execution/2026-10-18/python-identification-reader-v1/review-attempt-1/failure-review.json','Prior extracted-text hyphenation check repaired without manuscript change')],
        next_actions=['Inspect remaining69 original candidates and search-specificity/citation-chain limits; next concrete survey pair is candidates18 and20.',
            'Continue independent77open/23inconclusive software cells and96open/3inconclusive reuse decisions with genuine technical sources and explicit decisions.',
            'Complete L1/L6 coverage successors, reconcile all mandatory repair contracts, and obtain fresh-session rendered review before Q1/Q5/final acceptance.',
            'Retain later bank/platform/adoption needs as conditional evidence, not proposal blockers.'],
        global_blocker=None,visual_acceptance=False,proposal_accepted=False,background_worker_running=False))
    path=ROOT/'docs/program/execution/current-program.md'
    old=path.read_text()
    (BASE/'prior-current-program.md').write_text(old)
    header=f'''# Current executable proposal program

## Crash recovery continued on 18 October 2026

Use **python3 tools/run_program_reviews_v2.py status**, **next**, and **check**.
The canonical ledger is docs/program/state.json. Earlier numbered programs,
controllers and the continuation history below are preserved historical views.
The [proposal scope](../master-program-proposal.md) governs the current deliverable.

The current [1,080-page monograph](../../causal_proposal_agent_reasoning_reviewed_2026-10-18.pdf)
is paired with the [14-page sponsor brief](../../sponsor_proposal_agent_reasoning_reviewed_2026-10-18.pdf).
It contains784 audited citation records and203 genuine scholarly PDFs. All781
predecessor citation records, their prior contexts and238 unchanged compiled inputs
survive. Q2–Q4 pass for these exact reader bytes. Source, exact arithmetic and
all-page text-bound checks pass; visual and final proposal acceptance remain open.

Recovery completed the Python identification comparison and its preserving reader
and sponsor. New causal-agent material distinguishes a biomedical research agenda
from validated integration and a philosophical attribution test from statistical
identification. It preserves observed source citation/transcription defects. An exact
authored servicing example distinguishes a single intervention from a compound
intervention and derives hypothetical incremental value160-190pUSD. It is not a
live model result, DEF-1 implementation or observed bank benefit.

There are **{view['recorded_proposal_operations']} recorded outcomes among{view['proposal_operations']} proposal operations**,
with **{view['ready_proposal_operations']} ready**. A recorded inconclusive outcome is not a closed gap.
Software coverage:2pass,23inconclusive,77open of102. Reuse decisions:
16pass,3inconclusive,96open of115. Chapter reviews:20pass and2inconclusive
of22; L1 and L6 remain incomplete. The original census is now44inspected and
69unread of113; four crosscutting records and three citation-chain leads retain
separate denominators. All14LLM task reviews and12integration requirements have
bounded proposal outcomes, not general runtime or bank qualification.

### Standard and remaining gates

Retain developed scholarly argument, explained notation, assumptions, alternatives,
derivations, diagnostics, banking examples, authentic PDFs and source identity/version/
SHA-256/anchor audits. The cutoff is7October2026; length alone earns no acceptance.
MR01 retains17areas by6language/commercial dimensions and100–150substantive pages.
MR02 retains8chapters,14tasks and96–112substantive pages. MR03 retains4chapters,
12requirements and indicative40–60pages. Duplicate material earns no duplicate credit.
All three repair rollups, Q1, Q5, full release reconciliation and final acceptance
remain open. A complete proposal may retain bounded negative scientific findings;
it must not claim an implemented, independently accepted bank product.

### Executable continuation

Continue LL.CENSUS from the44/69 successor. The next concrete pair is candidate18
(evaluation survey, arXiv2307.03109) and candidate20(code-generation survey,
arXiv2406.00515): verify selected revisions and cutoff, inspect technical and adverse
anchors, update only actual original dispositions, and preserve the14-task mapping.
Continue software/reuse lanes independently when a source is blocked. Known routes
are primary-source inspection, explicit adoption/integration/port/rejection decisions,
controlled references and preserving manuscript integration. Unrestricted latent
identification, joint dependence, hidden-state policy and arbitrary-learner guarantees
remain open research; no general successful repair is promised.

[Every nonpassing operation and prerequisite](2026-10-18/recovery-agent-reasoning-v1/remaining-operations.json)
· [Recovery checkpoint](2026-10-18/recovery-agent-reasoning-v1/recovery-checkpoint.json)
· [Latest source census](2026-10-18/census-biomedical-reasoning-v1/census-register.json)

Source acquisition, public/synthetic prototype design and literature work do not
require bank truth, institutional approval or paid production trials. Rendered visual
acceptance requires a fresh image allowance under /home/ubuntu/AGENTS.md; it blocks
only that review. Continue other eligible work. Commands stay short and their outputs
bounded; durable receipts identify exact restart actions. No unattended worker runs.

---

## Preserved earlier continuation records

'''.replace('It contains784','It contains 784').replace('and203','and 203').replace('All781','All 781').replace('and238','and 238')
    path.write_text(header+old)
    verify_bindings(read(BASE/'recovery-checkpoint.json'))
    print(json.dumps(dict(recorded=view['recorded_proposal_operations'],ready=view['ready_proposal_operations'],
        nonpassing=len(operations),coverage=groups,current_program=str(path.relative_to(ROOT)))))


if __name__=='__main__':
    main()
