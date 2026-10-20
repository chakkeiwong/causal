#!/usr/bin/env python3
"""Refresh current execution pointers without rewriting bound historical plans."""
from collections import Counter
import json
from pathlib import Path

import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run = extension.base
ROOT = run.core.ROOT
BASE = ROOT/'docs/program/execution/2026-10-20/program-refresh-validity-v1'
WORK = ROOT/'docs/program/execution/2026-10-20/census-validity-v1'
SPONSOR = ROOT/'docs/program/execution/2026-10-20/sponsor-validity-v1'
read = lambda p: json.loads(p.read_text())


def main():
    assert not BASE.exists()
    state=run.core.read(ROOT,run.core.STATE)
    active=state['execution_runtime']['active']
    assert active is None or active['operation']=='LL.CENSUS'
    assert state['reader']['path']=='docs/causal_proposal_validity_measurement_reviewed_2026-10-20.pdf'
    sponsor=read(SPONSOR/'working-release.json'); verify_bindings(sponsor)
    assert run.same_reader(state['reader'],sponsor['paired_monograph'])
    view=run.status(ROOT,state); graph,merged,stages=run.combined(ROOT,state)
    assert {q['id']:q['status'] for q in view['proposal_gaps']}=={
        'Q1':'open','Q2':'pass','Q3':'pass','Q4':'pass','Q5':'open'}
    results=merged['execution_program']['results']; obligations=[]; groups={}
    for node in graph['nodes']:
        key=node['id']; result=results.get(key)
        if stages[key]!='proposal_now' or result and result['outcome']=='pass': continue
        progress=merged['execution_program']['progress'].get(key,[])
        action=read(ROOT/progress[-1]['path'])['next_action'] if progress else node['action']
        obligations.append(dict(id=key,lane=node['lane'],status=result['outcome'] if result else 'open',
            title=node['title'],action=action,prerequisites=run.ledger.blockers(merged,node),
            outputs=node['outputs'],evidence=result,requires_inputs=node['requires_inputs']))
    for name,prefix,total in [('software','SW.CELL.',102),('reuse','SW.DECISION.',115),('chapters','TEXT.REVIEW.',22)]:
        selected={k:v for k,v in results.items() if k.startswith(prefix)}
        groups[name]=dict(Counter(v['outcome'] for v in selected.values()),open=total-len(selected),total=total)
    BASE.mkdir()
    write(BASE/'state-snapshot.json',state); write(BASE/'status-snapshot.json',view)
    write(BASE/'remaining-operations.json',dict(reader=state['reader'],coverage=groups,
        recorded=view['recorded_proposal_operations'],proposal_operations=view['proposal_operations'],
        ready=view['ready_proposal_operations'],operations=obligations,
        census=ref(ROOT/'docs/program/execution/2026-10-20/census-validity-v1/census-register.json','52 inspected and 61 unread originals'),proposal_accepted=False))
    write(BASE/'continuation-checkpoint.json',dict(date='2026-10-20',status='continued_and_integrated',
        prior_git_commit='ec82efad9d12086f4cdfc1db3997f6e7f5497d5e',prior_checkout_clean=False,
        state=ref(BASE/'state-snapshot.json','Canonical state'),reader=state['reader'],
        sponsor=ref(SPONSOR/'working-release.json','Exact paired sponsor'),
        completed=['Recovered and completed the conditional fixest proposal choice with sixteen authenticated original blobs.',
                   'Integrated fixed-effect sample, rank, covariance and cohort-target examples.',
                   'Recorded the eight-family commercial dynamic-panel comparison with explicit remaining gaps.',
                   'Reviewed five Python effect routes and authenticated two statsmodels blobs against a recovered immutable tree.',
                   'Reproduced target-population, clipping and covariance identities; retained narrow historical DoubleML evidence.',
                   'Inspected Lin2026 v2 with source-critical qualifications and reconciled census to52/61.',
                   'Integrated exact grading/calibration/shared-shock witnesses and a proposed public evaluation.',
                   'Published1139-page reader and paired sponsor; renewed exact-reader Q2-Q4.'],
        evidence=[ref(WORK/n,'Reviewed continuation evidence') for n in
                  ['source-audit.json','review.json','release-source-review.json','working-release.json']],
        remaining=ref(BASE/'remaining-operations.json','Every nonpassing proposal obligation'),
        next_operation=view['next'],next_action=view['next_action'],global_blocker=None,
        visual_acceptance=False,proposal_accepted=False,background_worker_running=False))
    current=ROOT/'docs/program/execution/current-program.md'
    (BASE/'prior-current-program.md').write_bytes(current.read_bytes())
    text=f'''# Current executable proposal program

Updated 20 October 2026 after continuing the recovered proposal through
fixed-effect reuse, commercial and Python comparisons, and measurement-validity review.
This is research and a product proposal. Prototype qualification, independent
acceptance, bank validation and adoption remain distinct outcomes.

Use `python3 tools/run_program_reviews_v2.py status`, `next` and `check`.
The canonical ledger is [state.json](../state.json), governed by the
[proposal scope](../master-program-proposal.md). Bound historical plans and
evidence remain preserved. A checkpoint records continuation; it is not a stop gate.

## Current integrated documents

Read the [{state['reader']['pages']:,}-page integrated monograph](../../causal_proposal_validity_measurement_reviewed_2026-10-20.pdf).
Its companion is the [{sponsor['pages']}-page sponsor proposal](../../sponsor_proposal_validity_measurement_reviewed_2026-10-20.pdf).
The documents are paired by exact hashes. The reader has 828 audited citation
records and 211 genuine scholarly PDFs. Q2-Q4 pass for the exact current reader.
Q1/Q5, the three mandatory repair rollups, rendered visual review and final
proposal acceptance remain open. Page count and file integrity do not close them.

There are **{view['recorded_proposal_operations']} recorded outcomes of {view['proposal_operations']} proposal operations**,
with **{view['ready_proposal_operations']} ready**. Recorded inconclusive outcomes retain their unmet obligations.

| Area | Pass | Inconclusive | Open | Total |
|---|---:|---:|---:|---:|
| Software coverage | {groups['software'].get('pass',0)} | {groups['software'].get('inconclusive',0)} | {groups['software']['open']} | 102 |
| Reuse decisions | {groups['reuse'].get('pass',0)} | {groups['reuse'].get('inconclusive',0)} | {groups['reuse']['open']} | 115 |
| Chapter reviews | {groups['chapters'].get('pass',0)} | {groups['chapters'].get('inconclusive',0)} | {groups['chapters']['open']} | 22 |

The original frontier census is now **52 inspected and 61 unread out of 113**.
Four crosscutting obligations retain their own denominator. L1/L6 completeness,
complementary searches and citation chaining remain open. Fourteen task reviews
and twelve integration requirements have bounded proposal outcomes; these are
not evidence of runtime adoption.

## What this continuation changed

The recovered checkout was ec82efad with an active fixest review. Its sources
and all earlier publications were retained. Fixest and Python effect comparisons
are integrated, followed by the latest measurement-validity discussion on
physical PDF pages844-847. All826 predecessor citation identities and contexts
and255 compiled content inputs survive the latest addition.

Lin's genuine August2026 v2 methodological tutorial is retained with explicit
qualifications about calibration, sampling units and aggregation. The exact
measurement model keeps true correctness at60% while observed passing rises
52% to65%. With assumed valueUSD100 and extra costUSD8, true incremental value
isUSD-8 while the grade-based value isUSD5. A separate shared-shock model shows
why averaging repeated answers does not create independence. The new section
proposes public/generated evaluation and calibration; no model was executed.

Sixteen fixest original blobs authenticate against the selected 26 June 2026
Git tree. Its completed proposal choice conditionally selects a typed R worker
while deferring executable admission. Exact projection, sample, rank, covariance
and aggregation examples make that contract testable.

The eight-family commercial dynamic-panel comparison is recorded inconclusive.
Its [candidate-specific comparison](../comprehensive-v14/work/SW.COMM.dynamic_panel_timeseries/vendor-comparison.json)
retains edition, rights, pricing and missing-original questions without a
runtime or absence claim. These documentary gaps can be pursued independently.

The Python effects cell now reconciles EconML, DoubleML, CausalML, Delicatessen
and statsmodels. Two statsmodels source blobs authenticate against a recovered
immutable tree. All five selected point-treatment paths were traced through
target populations, weights, clipped probabilities and final joint covariance.
The cell remains inconclusive for breadth: complementary originals and the
saved search remainder remain open. Seven historical DoubleML comparisons keep
their narrow original scope; no new native package was executed.

Exact authored examples give ATE/ATT/ATU of USD 50/65/35. A deliberately wrong
outcome model with clipping gives score 69970/999 instead of 60; at assumed
cost USD 65, the implied margin changes from USD -5 to about USD 5.04. Correct
outcome functions remove that bias in the example. A separate matrix identity
isolates scalar versus column centering when moment means are nonzero.
These are reproducible proposal arguments, not native or bank findings.

## Standard and remaining routes

Each banking decision must connect its information clock to causal assumptions,
identification or limits, estimation, uncertainty, diagnostics, alternatives and
monetary consequences. Distinguish inherited results, project derivations,
generated examples and verified implementation. Every cited source needs identity,
version/date, local bytes, SHA-256, inspected anchors and supported claims;
scholarly citations require genuine PDFs. The literature cutoff is 7 October 2026.
FinMarketing supplies the scholarship standard; length is not acceptance.

MR01 requires 17 areas across six dimensions and 100-150 substantive software pages.
MR02 requires eight developed chapters, fourteen tasks and approximately 100 pages
(the depth contract is 96-112). MR03 requires four integration chapters and twelve
requirements, with indicative depth 40-60 pages. Coverage, connected argument and
exclusive depth must all pass; repeated material earns no duplicate credit.

Known routes remain for original-source inspection, commercial comparisons,
justified software reuse decisions, literature search, reader reconciliation and
proposed public experiments. General hidden-confounder identification, arbitrary
dependence, private-state policy inference and universal calibration remain
research uncertainties. Authentic bank truth, platform trials, institutional
acceptance and measured economics are later conditional gates. They do not block
independent proposal work supported by public or generated evidence.

## Exact continuation

Next controller-selected operation: **{view['next']}**. {view['next_action']}

For LL.CENSUS, resume the [52/61 register](2026-10-20/census-validity-v1/census-register.json)
and its latest controller checkpoint; do not repeat completed originals or publication.
For software, preserve pinned source identities, rights evidence, supported scope
and the decision to adopt, integrate, port, reference, defer or reject. A missing
original blocks its affected claims only. Continue other ready operations across
phase boundaries without asking again.

[Every nonpassing obligation](2026-10-20/program-refresh-validity-v1/remaining-operations.json)
· [Continuation checkpoint](2026-10-20/program-refresh-validity-v1/continuation-checkpoint.json)
· [Preserved previous program](2026-10-20/program-refresh-validity-v1/prior-current-program.md)

Use short commands, redirected logs and bounded text output. No unattended worker
is running. The inherited image allowance is exhausted under `/home/ubuntu/AGENTS.md`;
rendered review remains pending and does not block source or manuscript work.
'''
    current.write_text(text); run.render(ROOT,state)
    print(json.dumps(dict(reader=state['reader'],sponsor_pages=sponsor['pages'],
                         recorded=view['recorded_proposal_operations'],ready=view['ready_proposal_operations'],next=view['next'])))


if __name__ == '__main__':
    main()
