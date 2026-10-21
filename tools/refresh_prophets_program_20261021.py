#!/usr/bin/env python3
"""Refresh the authoritative master from reviewed releases and current receipts."""
from collections import Counter
import json
from pathlib import Path
import subprocess
import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run=extension.base
ROOT=run.core.ROOT
WORK=ROOT/'docs/program/execution/2026-10-21/prophets-repository-v1/publication-v2'
PAPER=ROOT/'docs/program/execution/2026-10-21/census-prophets-v2'
SPONSOR=ROOT/'docs/program/execution/2026-10-21/sponsor-prophets-repository-v1'
BASE=ROOT/'docs/program/execution/2026-10-21/program-refresh-prophets-v1'
read=lambda p:json.loads(p.read_text())


def main():
    assert not BASE.exists()
    state=run.core.read(ROOT,run.core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path']=='docs/causal_proposal_prophets_repository_reviewed_v2_2026-10-21.pdf'
    sponsor=read(SPONSOR/'working-release.json');verify_bindings(sponsor)
    assert run.same_reader(state['reader'],sponsor['paired_monograph'])
    view=run.status(ROOT,state);graph,merged,stages=run.combined(ROOT,state)
    assert {q['id']:q['status'] for q in view['proposal_gaps']}==dict(Q1='open',Q2='pass',Q3='pass',Q4='pass',Q5='open')
    groups={};results=merged['execution_program']['results'];obligations=[]
    for node in graph['nodes']:
        identifier=node['id'];result=results.get(identifier)
        if stages[identifier]!='proposal_now' or result and result['outcome']=='pass':continue
        progress=merged['execution_program']['progress'].get(identifier,[])
        action=read(ROOT/progress[-1]['path'])['next_action'] if progress else node['action']
        obligations.append(dict(id=identifier,lane=node['lane'],title=node['title'],
            status=result['outcome'] if result else 'open',action=action,
            prerequisites=run.ledger.blockers(merged,node),outputs=node['outputs'],
            evidence=result,requires_inputs=node['requires_inputs']))
    for name,prefix,total in [('software','SW.CELL.',102),('reuse','SW.DECISION.',115),('chapters','TEXT.REVIEW.',22)]:
        selected={k:v for k,v in results.items() if k.startswith(prefix)}
        groups[name]=dict(Counter(v['outcome'] for v in selected.values()),open=total-len(selected),total=total)
    counts=Counter(x['disposition'] for x in read(PAPER/'census-register.json')['items'])
    assert counts['inspected_primary_retained_with_limits']==57 and counts['open_original_not_inspected']==56
    records=len(read(WORK/'reader/source-audit.json')['sources'])
    papers=read(WORK/'traceability-review.json')['scholarly_pdfs']
    sponsor_records=len(read(SPONSOR/'source-audit.json')['sources'])
    physical=read(WORK/'release-source-review.json')['checks']['physical_pages']
    BASE.mkdir()
    write(BASE/'state-snapshot.json',state);write(BASE/'status-snapshot.json',view)
    write(BASE/'remaining-operations.json',dict(reader=state['reader'],coverage=groups,
        recorded=view['recorded_proposal_operations'],proposal_operations=view['proposal_operations'],
        ready=view['ready_proposal_operations'],operations=obligations,
        census=ref(PAPER/'census-register.json','57 inspected/56 unread; four crosscutting obligations'),proposal_accepted=False))
    evidence=[ref(WORK/n,'Pinned repository and paired-result review') for n in
        ['source-audit.json','review.json','exact-results.json','omissions-register.json','conversion-contract.json',
         'working-release.json','release-source-review.json']]
    evidence+=[ref(PAPER/n,'Primary article and census preservation') for n in
        ['review.json','census-register.json','task-map.json','working-release.json']]
    write(BASE/'continuation-checkpoint.json',dict(date='2026-10-21',
        status='continued_and_integrated',prior_git_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True,cwd=ROOT).strip(),
        state=ref(BASE/'state-snapshot.json','Canonical snapshot'),reader=state['reader'],
        sponsor=ref(SPONSOR/'working-release.json','Exact paired sponsor'),
        completed=['Committed and pushed gsynth integration and recovered literature work.',
          'Preserved both source-review construction failures and completed a separate successor.',
          'Inspected candidate167 and preserved all116 other census records;57/56 across113 originals.',
          'Recovered pinned public repository; authenticated12 files and reproduced24 saved subset accuracy averages.',
          'Reconciled ETT138 versus printed137 and question2883 numeric target; preserved remaining semantic and record gaps.',
          'Integrated paper and repository discussion, exact counterexample and reference-only reuse limits into paired PDFs.',
          'Renewed Q2-Q4 for exact reader bytes; kept visual and final acceptance open.'],
        evidence=evidence,remaining=ref(BASE/'remaining-operations.json','Every nonpassing proposal obligation'),
        next_operation=view['next'],next_action=view['next_action'],global_blocker=None,
        background_worker_running=False,visual_acceptance=False,proposal_accepted=False))
    current=ROOT/'docs/program/execution/current-program.md'
    (BASE/'prior-current-program.md').write_bytes(current.read_bytes())
    current.write_text(f'''# Current executable proposal program

Updated 21 October 2026 after the formal causal-reasoning paper and repository
reviews. This is a research and product proposal. Prototype qualification,
independent acceptance, bank validation and adoption remain separate.

Use `python3 tools/run_program_reviews_v2.py status`, `next` and `check`.
The canonical ledger is [state.json](../state.json); the
[proposal scope](../master-program-proposal.md) governs the work. Earlier
numbered masters are historical snapshots. Continue eligible operations across
checkpoints and phase boundaries; one local blocker does not block another lane.

## Current integrated documents

Read the [{state['reader']['pages']:,}-page monograph](../../causal_proposal_prophets_repository_reviewed_v2_2026-10-21.pdf)
and its [{sponsor['pages']}-page sponsor proposal](../../sponsor_proposal_prophets_repository_reviewed_2026-10-21.pdf).
The monograph contains {records} audited citation records and {papers} genuine
scholarly PDFs. The sponsor contains {sponsor_records} audited citations and is
paired to the exact reader bytes. Q2-Q4 pass for these bytes. Q1/Q5, the three
mandatory repair rollups, rendered visual review and final acceptance remain open.

There are **{view['recorded_proposal_operations']} recorded outcomes of {view['proposal_operations']} proposal operations**
and **{view['ready_proposal_operations']} ready operations**. A recorded
inconclusive outcome preserves its unresolved obligations.

| Area | Pass | Inconclusive | Open | Total |
|---|---:|---:|---:|---:|
| Software coverage | {groups['software'].get('pass',0)} | {groups['software'].get('inconclusive',0)} | {groups['software']['open']} | 102 |
| Reuse decisions | {groups['reuse'].get('pass',0)} | {groups['reuse'].get('inconclusive',0)} | {groups['reuse']['open']} | 115 |
| Chapter reviews | {groups['chapters'].get('pass',0)} | {groups['chapters'].get('inconclusive',0)} | {groups['chapters']['open']} | 22 |

The frontier census has **57 inspected and 56 unread originals out of 113**,
plus four crosscutting obligations. Fourteen task reviews and twelve integration
requirements have scoped proposal outcomes; they do not establish runtime adoption.

## New findings and the limits they resolve

Candidate 167, *From Causal Parrots to Causal Prophets?*, now has an inspected
genuine publisher PDF, source audit, exact examples and integrated discussion.
All 116 other census records survive unchanged. Its reported overall GPT-4o
accuracies are 82.0%, 86.4% and 90.8% for baseline, tree and program reasoning.
These formal synthetic tasks do not establish business translation, graph truth
or effect identification from bank records.

The repository follow-up on physical PDF pages {physical[0]}-{physical[1]} authenticates
12 files at commit 2f7835a00a62545259ce4a6757d7659fc07358fe. Three aligned tables
reproduce all 24 published subset averages. ETT count 138 resolves the printed
137. Question 2883's unrounded probabilities reproduce its negative numerical
target, while death/survival coding and notation remain unresolved. Empty chain
histories and absent error annotations do not resolve the other appendix totals.

The selected self-consistency caller/helper and client plumbing disagree.
The README's pip instruction points to a Conda export. The prompt's illustrated
generator omits a common parent from its displayed graph: under its independent
noises the causal effect is zero while the association is 6/793. These are static
findings and exact authored calculations, not executed upstream or model trials.
Retain the material as a reference; unchanged executable adoption is rejected.
The paper and repository sections preserve earlier sources and financial examples.

## Standard and remaining work

Each claimed banking use must connect pre-action information to the causal model,
assumptions, identification or justified limits, estimation, uncertainty,
diagnostics, alternatives and monetary consequences. Sources need identity,
version/date, genuine local bytes, SHA-256, inspected anchors and supported
claims. Scholarly citations need real PDFs. Cutoff: 7 October 2026. FinMarketing
supplies the scholarly standard; total length does not prove quality or coverage.

MR01 requires 17 areas across six dimensions and 100-150 substantive software pages.
MR02 requires eight developed chapters, 14 tasks and about 100 pages (96-112).
MR03 requires four integration chapters and 12 requirements (indicative 40-60 pages).
Coverage and exclusive substantive depth remain the acceptance criteria.

Known routes are primary-source recovery and inspection, complementary searches,
reasoned reuse decisions, connected manuscript development, reproducible public
examples and matched prototype designs. The repository follow-up demonstrates
that public records can resolve meaningful gaps before costly bank trials.
Remaining source-specific work includes original-generator/coding review,
per-chain/error records, exact runner/model identity, inherited rights and a
supported prototype environment. These have independent next actions in the
[omissions register](2026-10-21/prophets-repository-v1/omissions-register.json).

General hidden-confounder identification, arbitrary dependence, private-state
policy inference and universal calibration remain research questions. Authentic
bank truth, platform acceptance, independent review and real economics require
later external evidence and do not block current proposal research.

## Continuation rules and exact actions

Controller next: **{view['next']}**. {view['next_action']}

Continue the 56 unread originals and complementary searches. Preserve candidate167's
paper/repository inspection and avoid repeating it. Review original CLADDER
generation and polarity before relabeling question2883; recover chain and error
annotations if available. Independently continue software survey and reuse
decisions, including untouched longitudinal/panel and integration candidates.
Choose the next ready lane after a substantive result; source-specific missing
records are local obligations, not a global checkpoint.

[Every nonpassing operation](2026-10-21/program-refresh-prophets-v1/remaining-operations.json)
and the [continuation checkpoint](2026-10-21/program-refresh-prophets-v1/continuation-checkpoint.json)
give exact actions and dependencies. The
[previous master](2026-10-21/program-refresh-prophets-v1/prior-current-program.md)
preserves earlier status. All failed construction attempts and the repaired equation overflow remain preserved.
Use short asynchronous commands, redirected logs and bounded text output.
No unattended research worker is running. The inherited image allowance is
exhausted under `/home/ubuntu/AGENTS.md`; a fresh visual session is needed for
rendered acceptance. Source work and other independent branches remain eligible.
''')
    run.render(ROOT,state)
    print(json.dumps(dict(reader=state['reader'],sponsor_pages=sponsor['pages'],
        records=records,papers=papers,recorded=view['recorded_proposal_operations'],ready=view['ready_proposal_operations'],
        census='57/56',proposal_accepted=False)))


if __name__=='__main__':main()
