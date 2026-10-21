#!/usr/bin/env python3
"""Refresh current continuation from outcomes and exact paired releases."""
from collections import Counter
import json
from pathlib import Path
import subprocess
import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run=extension.base
ROOT=run.core.ROOT
WORK=ROOT/'docs/program/execution/2026-10-21/gsynth-reuse-v1'
RELEASE=WORK
SPONSOR=ROOT/'docs/program/execution/2026-10-21/sponsor-gsynth-v1'
BASE=ROOT/'docs/program/execution/2026-10-21/program-refresh-gsynth-v1'
read=lambda p:json.loads(p.read_text())


def main():
    assert not BASE.exists()
    state=run.core.read(ROOT,run.core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path']=='docs/causal_proposal_gsynth_reviewed_2026-10-21.pdf'
    sponsor=read(SPONSOR/'working-release.json');verify_bindings(sponsor)
    assert run.same_reader(state['reader'],sponsor['paired_monograph'])
    view=run.status(ROOT,state);graph,merged,stages=run.combined(ROOT,state)
    assert {q['id']:q['status'] for q in view['proposal_gaps']}=={'Q1':'open','Q2':'pass','Q3':'pass','Q4':'pass','Q5':'open'}
    results=merged['execution_program']['results'];groups={};obligations=[]
    for node in graph['nodes']:
        key=node['id'];result=results.get(key)
        if stages[key]!='proposal_now' or result and result['outcome']=='pass':continue
        progress=merged['execution_program']['progress'].get(key,[])
        action=read(ROOT/progress[-1]['path'])['next_action'] if progress else node['action']
        obligations.append(dict(id=key,lane=node['lane'],status=result['outcome'] if result else 'open',
            title=node['title'],action=action,prerequisites=run.ledger.blockers(merged,node),
            outputs=node['outputs'],evidence=result,requires_inputs=node['requires_inputs']))
    for name,prefix,total in [('software','SW.CELL.',102),('reuse','SW.DECISION.',115),('chapters','TEXT.REVIEW.',22)]:
        selected={k:v for k,v in results.items() if k.startswith(prefix)}
        groups[name]=dict(Counter(v['outcome'] for v in selected.values()),open=total-len(selected),total=total)
    census=ROOT/'docs/program/execution/2026-10-21/census-ace-v1/census-register.json'
    counts=Counter(x['disposition'] for x in read(census)['items'])
    inspected=counts['inspected_primary_retained_with_limits'];unread=counts['open_original_not_inspected']
    reader_count=len(read(RELEASE/'reader/source-audit.json')['sources'])
    paper_count=read(RELEASE/'traceability-review.json')['scholarly_pdfs']
    sponsor_count=len(read(SPONSOR/'source-audit.json')['sources'])
    physical=read(RELEASE/'release-source-review.json')['checks']['physical_pages']
    BASE.mkdir()
    write(BASE/'state-snapshot.json',state);write(BASE/'status-snapshot.json',view)
    write(BASE/'remaining-operations.json',dict(reader=state['reader'],coverage=groups,
        recorded=view['recorded_proposal_operations'],proposal_operations=view['proposal_operations'],ready=view['ready_proposal_operations'],
        operations=obligations,census=ref(census,'Preserved frontier census'),proposal_accepted=False))
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    evidence=[ref(WORK/n,'Pinned panel reuse evidence') for n in ['source-audit.json','review.json','identity-review.json',
        'conversion-contract.json','exact-results.json','omissions-register.json','source-review-failure.json']]
    evidence += [ref(RELEASE/n,'Preserving integrated review') for n in ['working-release.json','release-source-review.json']]
    write(BASE/'continuation-checkpoint.json',dict(date='2026-10-21',status='continued_and_integrated',prior_git_commit=commit,
        state=ref(BASE/'state-snapshot.json','Canonical snapshot'),reader=state['reader'],sponsor=ref(SPONSOR/'working-release.json','Paired sponsor'),
        completed=['Verified and preserved the committed Julia effects reader and sponsor.',
            'Recovered pinned gsynth wrapper and selected fect engine sources; inspected options, targets and uncertainty.',
            'Recorded reference-only gsynth reuse choice; ignored-weight source finding retained with exact examples.',
            'Integrated three added citations while preserving all885 prior citation identities and contexts.',
            'Renewed Q2-Q4 and paired the sponsor; visual/final acceptance remains open.',
            'Recovered candidate167 publisher original and identity after historical allowlist and sandbox DNS failures.'],
        evidence=evidence,remaining=ref(BASE/'remaining-operations.json','Every nonpassing obligation'),
        next_operation=view['next'],next_action=view['next_action'],global_blocker=None,
        visual_acceptance=False,proposal_accepted=False,background_worker_running=False))
    current=ROOT/'docs/program/execution/current-program.md'
    (BASE/'prior-current-program.md').write_bytes(current.read_bytes())
    text=f'''# Current executable proposal program

Updated 21 October 2026 after the gsynth panel reuse review. This is a
research and product proposal; prototype qualification, independent acceptance,
bank validation and adoption remain separate.

Use `python3 tools/run_program_reviews_v2.py status`, `next` and `check`.
The canonical ledger is [state.json](../state.json); the
[proposal scope](../master-program-proposal.md) governs current work.
Checkpoints and phase boundaries are continuation points, not permission gates.

## Current integrated documents

Read the [{state['reader']['pages']:,}-page monograph](../../causal_proposal_gsynth_reviewed_2026-10-21.pdf)
and its [{sponsor['pages']}-page sponsor proposal](../../sponsor_proposal_gsynth_reviewed_2026-10-21.pdf).
The monograph has {reader_count} audited citation records and {paper_count} genuine
scholarly PDFs. The sponsor has {sponsor_count} audited citations and is paired
to the exact reader bytes. Q2-Q4 pass for those bytes. Q1/Q5, all three mandatory
repair rollups, rendered visual review and final proposal acceptance remain open.

There are **{view['recorded_proposal_operations']} recorded outcomes of {view['proposal_operations']} proposal operations**
and **{view['ready_proposal_operations']} ready operations**. Recorded inconclusive work
retains its unresolved obligations and does not close the gap.

| Area | Pass | Inconclusive | Open | Total |
|---|---:|---:|---:|---:|
| Software coverage | {groups['software'].get('pass',0)} | {groups['software'].get('inconclusive',0)} | {groups['software']['open']} | 102 |
| Reuse decisions | {groups['reuse'].get('pass',0)} | {groups['reuse'].get('inconclusive',0)} | {groups['reuse']['open']} | 115 |
| Chapter reviews | {groups['chapters'].get('pass',0)} | {groups['chapters'].get('inconclusive',0)} | {groups['chapters']['open']} | 22 |

The frontier census remains **{inspected} inspected and {unread} unread out of 113 originals**,
plus four crosscutting obligations. Fourteen task reviews and twelve integration
requirements have scoped proposal outcomes, without runtime adoption claims.

## New integrated findings

Physical PDF pages {physical[0]}-{physical[1]} develop gsynth1.4.0 and the
selected fect2.4.5 dependency. The wrapper is maintained for compatibility,
and its complete source declares a documented weight argument without forwarding
it. The engine has distinct fitting/aggregation roles, canonical weighted outputs,
method restrictions, sample removal, rank selection and uncertainty behavior.
No downloaded upstream code was executed.

Exact authored examples give equal effect2 versus weighted-22/5, with margins1
and-27/5 at assumed cost1. Unequal treatment durations give cell-average6 versus
unit-average2. Rank-two worlds share the observed panel but imply effects6 or2
because the pre-period factor rank is deficient. More rows need not add rank.
These are public mathematical examples, not native or banking measurements.

The reference-only reuse decision leaves runtime admission false. A future direct
fect worker requires full rights/environment review, native parity, explicit panel
conversion/refusal and law-specific uncertainty qualification. All885 prior citation
identities/contexts and269 compiled inputs survive. An out-of-range test-file anchor
was refused; the original failed script/log and corrected successor are preserved.

Candidate167, From Causal Parrots to Causal Prophets?, now has a recovered genuine
publisher PDF and identity page. Acquisition alone does not earn census inspection
credit; its technical review is the next independent action.

## Required standard and remaining work

Each banking use must connect information available before action to assumptions,
identification or justified limits, estimation, uncertainty, diagnostics,
alternatives and monetary consequences. Inherited results, project derivations,
synthetic examples and verified implementation remain distinct. Every source
needs identity, version/date, original bytes, SHA-256, inspected anchors and
supported claims; scholarly works need genuine PDFs. Cutoff: 7 October 2026.
FinMarketing supplies the scholarly standard, not a length target.

MR01 requires 17 areas across six dimensions and 100-150 substantive software pages.
MR02 requires eight developed chapters, 14 tasks and about 100 pages (depth 96-112).
MR03 requires four integration chapters and 12 requirements (indicative depth 40-60).
Connected argument, exclusive depth and actual coverage matter; total PDF pages
do not establish completion.

Known routes remain primary-source recovery, complementary searches, reasoned
reuse choices, public examples, matched prototype designs and editorial integration.
General hidden-confounder identification, arbitrary dependence, private-state policy
inference and universal calibration remain research questions. Bank truth,
platform acceptance and real economics are later conditional work and do not block
independent proposal research.

## Exact continuation

Controller next: **{view['next']}**. {view['next_action']}

Inspect candidate167's complete primary argument, benchmark design, prompt/tool
routes, error analysis and limits. Save its original under the required scholarly
filename, bind source identity and inspected anchors, map the 14 tasks, then
publish a preserving census/manuscript successor. The effects review retains
Rust/source/pagination/wider-language obligations; commercial transport retains
vendor/edition/rights/search duties. Independent eligible branches continue.

[Every nonpassing obligation](2026-10-21/program-refresh-gsynth-v1/remaining-operations.json)
and the [continuation checkpoint](2026-10-21/program-refresh-gsynth-v1/continuation-checkpoint.json)
record exact actions and dependencies. The [previous master](2026-10-21/program-refresh-gsynth-v1/prior-current-program.md)
preserves earlier status. Use short asynchronous commands and bounded output.
No unattended research worker is running. The inherited image allowance is
exhausted under `/home/ubuntu/AGENTS.md`; rendered visual acceptance needs a
fresh visual session. Source work and independent branches remain eligible.
'''
    current.write_text(text)
    run.render(ROOT,state)
    print(json.dumps(dict(recorded=view['recorded_proposal_operations'],ready=view['ready_proposal_operations'],
        reader=state['reader'],sponsor_pages=sponsor['pages'],next=view['next'])))


if __name__=='__main__':main()
