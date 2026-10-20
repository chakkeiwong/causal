#!/usr/bin/env python3
"""Refresh current execution pointers without rewriting bound historical plans."""
from collections import Counter
import json
from pathlib import Path

import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run = extension.base
ROOT = run.core.ROOT
BASE = ROOT/'docs/program/execution/2026-10-20/program-refresh-fixest-v1'
WORK = ROOT/'docs/program/execution/2026-10-20/fixest-reuse-v1'
SPONSOR = ROOT/'docs/program/execution/2026-10-20/sponsor-fixest-v1'
read = lambda p: json.loads(p.read_text())


def main():
    assert not BASE.exists()
    state=run.core.read(ROOT,run.core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path']=='docs/causal_proposal_fixest_reviewed_2026-10-20.pdf'
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
        census=ref(ROOT/'docs/program/execution/2026-10-20/census-population-attribution-v1/census-register.json','51 inspected and 62 unread originals'),proposal_accepted=False))
    write(BASE/'continuation-checkpoint.json',dict(date='2026-10-20',status='continued_and_integrated',
        prior_git_commit='ec82efad9d12086f4cdfc1db3997f6e7f5497d5e',prior_checkout_clean=False,
        state=ref(BASE/'state-snapshot.json','Canonical state'),reader=state['reader'],
        sponsor=ref(SPONSOR/'working-release.json','Exact paired sponsor'),
        completed=['Recovered the active fixest review without reacquiring its completed originals.',
                   'Authenticated sixteen pinned blobs and completed a scoped proposal selection with native admission deferred.',
                   'Integrated exact projection, cluster covariance and cohort aggregation examples into both documents.',
                   'Published1130-page reader and27-page sponsor; preserved822 prior citation records and contexts.',
                   'Renewed exact-reader Q2-Q4 and completed eight-family dynamic-commercial comparison as inconclusive.'],
        evidence=[ref(WORK/n,'Reviewed continuation evidence') for n in
                  ['source-audit.json','review.json','release-source-review.json','working-release.json']],
        remaining=ref(BASE/'remaining-operations.json','Every nonpassing proposal obligation'),
        next_operation=view['next'],next_action=view['next_action'],global_blocker=None,
        visual_acceptance=False,proposal_accepted=False,background_worker_running=False))
    current=ROOT/'docs/program/execution/current-program.md'
    (BASE/'prior-current-program.md').write_bytes(current.read_bytes())
    text=f'''# Current executable proposal program

Updated 20 October 2026 after continuing the recovered proposal through
a pinned fixed-effect reuse review and an eight-family commercial comparison.
This is research and a product proposal. Prototype qualification, independent
acceptance, bank validation and adoption remain distinct outcomes.

Use `python3 tools/run_program_reviews_v2.py status`, `next` and `check`.
The canonical ledger is [state.json](../state.json), governed by the
[proposal scope](../master-program-proposal.md). Bound historical plans and
evidence remain preserved. A checkpoint records continuation; it is not a stop gate.

## Current integrated documents

Read the [{state['reader']['pages']:,}-page integrated monograph](../../causal_proposal_fixest_reviewed_2026-10-20.pdf).
Its companion is the [{sponsor['pages']}-page sponsor proposal](../../sponsor_proposal_fixest_reviewed_2026-10-20.pdf).
The documents are paired by exact hashes. The reader has 824 audited citation
records and 210 genuine scholarly PDFs. Q2-Q4 pass for the exact current reader.
Q1/Q5, the three mandatory repair rollups, rendered visual review and final
proposal acceptance remain open. Page count and file integrity do not close them.

There are **{view['recorded_proposal_operations']} recorded outcomes of {view['proposal_operations']} proposal operations**,
with **{view['ready_proposal_operations']} ready**. Recorded inconclusive outcomes retain their unmet obligations.

| Area | Pass | Inconclusive | Open | Total |
|---|---:|---:|---:|---:|
| Software coverage | {groups['software'].get('pass',0)} | {groups['software'].get('inconclusive',0)} | {groups['software']['open']} | 102 |
| Reuse decisions | {groups['reuse'].get('pass',0)} | {groups['reuse'].get('inconclusive',0)} | {groups['reuse']['open']} | 115 |
| Chapter reviews | {groups['chapters'].get('pass',0)} | {groups['chapters'].get('inconclusive',0)} | {groups['chapters']['open']} | 22 |

The original frontier census is now **51 inspected and 62 unread out of 113**.
Four crosscutting obligations retain their own denominator. L1/L6 completeness,
complementary searches and citation chaining remain open. Fourteen task reviews
and twelve integration requirements have bounded proposal outcomes; these are
not evidence of runtime adoption.

## What this continuation changed

The recovered checkout was ec82efad with an active fixest review. Its source
acquisitions and all earlier publications were retained. New fixest discussion
occupies physical PDF pages258-262; all822 prior citation identities and contexts,
and all253 prior compiled content inputs, survive unchanged.

Sixteen original blobs authenticate against the selected26June2026 Git tree.
The proposal conditionally selects the original R engine with a typed request,
sample and diagnostic contract; executable admission remains deferred. Exact
authored examples reproduce a slope of4, raw cluster covariance8/9, explicit
corrections4/3 and10/3, and cohort aggregate variance51/16. At an assumed cost
USD4, changing aggregation weights changes illustrative net margin from
USD-0.50 toUSD1. These are algebraic references, not native or bank results.

The eight-family dynamic-panel/time-series commercial comparison is recorded
as inconclusive: selected primary methods are documented, while exact editions,
rights, prices and several technical originals remain unresolved. Its
[candidate-specific comparison](../comprehensive-v14/work/SW.COMM.dynamic_panel_timeseries/vendor-comparison.json)
records each follow-up without an absence or runtime claim. The already
integrated scholarly treatment remains preserved and earns no duplicate depth.

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

For LL.CENSUS, resume the [51/62 register](2026-10-20/census-population-attribution-v1/census-register.json)
and its latest controller checkpoint; do not repeat completed originals or publication.
For software, preserve pinned source identities, rights evidence, supported scope
and the decision to adopt, integrate, port, reference, defer or reject. A missing
original blocks its affected claims only. Continue other ready operations across
phase boundaries without asking again.

[Every nonpassing obligation](2026-10-20/program-refresh-fixest-v1/remaining-operations.json)
· [Continuation checkpoint](2026-10-20/program-refresh-fixest-v1/continuation-checkpoint.json)
· [Preserved previous program](2026-10-20/program-refresh-fixest-v1/prior-current-program.md)

Use short commands, redirected logs and bounded text output. No unattended worker
is running. The inherited image allowance is exhausted under `/home/ubuntu/AGENTS.md`;
rendered review remains pending and does not block source or manuscript work.
'''
    current.write_text(text); run.render(ROOT,state)
    print(json.dumps(dict(reader=state['reader'],sponsor_pages=sponsor['pages'],
                         recorded=view['recorded_proposal_operations'],ready=view['ready_proposal_operations'],next=view['next'])))


if __name__ == '__main__':
    main()
