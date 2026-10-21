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
WORK=ROOT/'docs/program/execution/2026-10-21/transport-commercial-v1'
RELEASE=WORK/'publication-v2'
SPONSOR=ROOT/'docs/program/execution/2026-10-21/sponsor-transport-v1'
BASE=ROOT/'docs/program/execution/2026-10-21/program-refresh-transport-v1'
read=lambda p:json.loads(p.read_text())


def main():
    assert not BASE.exists()
    state=run.core.read(ROOT,run.core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path']=='docs/causal_proposal_transport_reviewed_v2_2026-10-21.pdf'
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
    evidence=[ref(WORK/n,'Commercial missingness evidence') for n in ['source-audit.json','review.json','comparison-review.json',
        'conversion-contract.json','exact-results.json','omissions-register.json','build-failure-review.json']]
    evidence += [ref(RELEASE/n,'Preserving integrated review') for n in ['working-release.json','release-source-review.json']]
    write(BASE/'continuation-checkpoint.json',dict(date='2026-10-21',status='continued_and_integrated',prior_git_commit=commit,
        state=ref(BASE/'state-snapshot.json','Canonical snapshot'),reader=state['reader'],sponsor=ref(SPONSOR/'working-release.json','Paired sponsor'),
        completed=['Committed recovered ACE reader, sponsor and active commercial checkpoint.',
            'Inspected ten complete official originals; six-family coverage and comparison are inconclusive.',
            'Integrated missingness, imputation compatibility, pooling, transport and exact monetary examples.',
            'Preserved the failed overfull-equation build and repaired a separate successor.',
            'Renewed exact-reader Q2-Q4 and paired sponsor; final visual/proposal acceptance remains open.'],
        evidence=evidence,remaining=ref(BASE/'remaining-operations.json','Every nonpassing obligation'),
        next_operation=view['next'],next_action=view['next_action'],global_blocker=None,
        visual_acceptance=False,proposal_accepted=False,background_worker_running=False))
    current=ROOT/'docs/program/execution/current-program.md'
    (BASE/'prior-current-program.md').write_bytes(current.read_bytes())
    text=f'''# Current executable proposal program

Updated 21 October 2026 after the commercial missingness and population-transfer
review. This program governs a research and product proposal. Prototype
qualification, independent acceptance, bank validation and adoption are separate.

Use `python3 tools/run_program_reviews_v2.py status`, `next` and `check`.
The canonical ledger is [state.json](../state.json); the
[proposal scope](../master-program-proposal.md) governs current work.
Checkpoints preserve continuation and are not permission or phase gates.

## Current integrated documents

Read the [{state['reader']['pages']:,}-page monograph](../../causal_proposal_transport_reviewed_v2_2026-10-21.pdf)
and its [{sponsor['pages']}-page sponsor proposal](../../sponsor_proposal_transport_reviewed_2026-10-21.pdf).
The monograph has {reader_count} audited citation records and {paper_count} genuine
scholarly PDFs; the sponsor has {sponsor_count} audited citations and is paired to
the exact reader bytes. Q2-Q4 pass for those bytes. Q1/Q5, all three mandatory
repair rollups, rendered visual review and final proposal acceptance remain open.

There are **{view['recorded_proposal_operations']} recorded outcomes of {view['proposal_operations']} proposal operations**
and **{view['ready_proposal_operations']} ready operations**. An inconclusive outcome records work and
its unresolved obligations; it does not close the gap.

| Area | Pass | Inconclusive | Open | Total |
|---|---:|---:|---:|---:|
| Software coverage | {groups['software'].get('pass',0)} | {groups['software'].get('inconclusive',0)} | {groups['software']['open']} | 102 |
| Reuse decisions | {groups['reuse'].get('pass',0)} | {groups['reuse'].get('inconclusive',0)} | {groups['reuse']['open']} | 115 |
| Chapter reviews | {groups['chapters'].get('pass',0)} | {groups['chapters'].get('inconclusive',0)} | {groups['chapters']['open']} | 22 |

The frontier census remains **{inspected} inspected and {unread} unread out of 113 originals**,
with four crosscutting obligations. Fourteen task reviews and twelve integration
requirements have scoped proposal outcomes; they do not establish runtime adoption.

## New integrated findings

The commercial missingness argument occupies physical PDF pages {physical[0]}-{physical[1]}.
Ten complete official originals support selected Stata, SAS/STAT 14.1 and IBM
SPSS 31.0.2 profiles. The comparison distinguishes missingness assumptions,
imputation compatibility, pooled covariance, complex sampling, failed fits and
target-population support. EViews, Mplus and commercial graphical tools remain
unresolved candidates. Both coverage and competitive comparison are inconclusive;
no complete census, native adapter or vendor absence is claimed.

Exact authored examples show pilot/target effects 6 and -6, giving assumed cost-2
margins 4 and -8. Identical observed missing-data laws permit effects 0 and 10,
giving cost-4 margins -4 and 6. Three imputation estimates with within variance 1
give total variance 19/3. Incompatible binary conditionals admit stable but
different scan distributions. These are public mathematical witnesses, not bank
observations or vendor runtime results.

The initial build found one equation exceeding the text width by 15.44824 points.
Its files remain preserved. A separate successor splits the equation and passes
source, arithmetic, preservation and all-page text checks. SAS download failures,
unavailable MNAR syntax, unusable search output, edition uncertainty and extraction
limits remain recorded. No partial PDF is cited as a complete source. Prior ACE
and grf findings and all earlier citation identities and contexts remain integrated.

The [previous master](2026-10-21/program-refresh-transport-v1/prior-current-program.md)
preserves earlier findings. Commit {commit[:8]} checkpoints recovered ACE integration
and commercial acquisition. This continuation adds the reviewed commercial
argument and its paired releases.

## Required standard and remaining work

Each banking use must connect information available before action to assumptions,
identification or justified limits, estimation, uncertainty, diagnostics,
alternatives and monetary consequences. Inherited results, project derivations,
synthetic examples and verified implementation must remain distinct. Every source
needs identity, version/date, original bytes, SHA-256, inspected anchors and
supported claims; scholarly works need genuine PDFs. Literature cutoff: 7 October
2026. FinMarketing supplies the scholarship standard, not a length target.

MR01 requires 17 areas across six dimensions and 100-150 substantive software pages.
MR02 requires eight developed chapters, 14 tasks and about 100 pages (depth contract
96-112). MR03 requires four integration chapters and twelve requirements, with
indicative depth 40-60 pages. Coverage, connected argument and exclusive depth all
matter; duplication and aggregate page count do not establish completion.

Known routes include source recovery and inspection, complementary searches,
reasoned reuse decisions, public examples, matched prototype designs and editorial
integration. General hidden-confounder identification, arbitrary dependence,
private-state policy inference and universal calibration remain research questions.
Bank truth, platform acceptance and real economics are later conditional work and
do not block independent proposal research.

## Exact continuation

Controller next: **{view['next']}**. {view['next_action']}

Continue that eligible operation, then the next ready branch. Commercial
missingness needs the listed vendor originals, complementary searches, matching
editions and rights, and target-specific public comparisons before expensive bank
trials. Inspect the remaining {unread} frontier originals and record citation-chain
coverage separately. Local source failures and phase boundaries do not stop
other eligible operations.

[Every nonpassing obligation](2026-10-21/program-refresh-transport-v1/remaining-operations.json)
and [exact continuation checkpoint](2026-10-21/program-refresh-transport-v1/continuation-checkpoint.json)
retain actions and prerequisites. Use short asynchronous commands and bounded
output. No unattended research worker is running. The inherited image allowance
is exhausted under `/home/ubuntu/AGENTS.md`; a fresh visual session is required
for rendered acceptance. Source and manuscript work remain eligible.
'''
    current.write_text(text)
    run.render(ROOT,state)
    print(json.dumps(dict(recorded=view['recorded_proposal_operations'],ready=view['ready_proposal_operations'],
        reader=state['reader'],sponsor_pages=sponsor['pages'],next=view['next'])))


if __name__=='__main__':main()
