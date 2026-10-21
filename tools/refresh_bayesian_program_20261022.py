#!/usr/bin/env python3
"""Review the full proposal queue and refresh authoritative status from receipts."""
from collections import Counter, defaultdict
import json
from pathlib import Path
import subprocess
import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run=extension.base
ROOT=run.core.ROOT
WORK=ROOT/'docs/program/execution/2026-10-22/bayesian-commercial-v2'
ORIGINAL=ROOT/'docs/program/execution/2026-10-22/bayesian-commercial-v1'
SPONSOR=ROOT/'docs/program/execution/2026-10-22/sponsor-bayesian-commercial-v1'
BASE=ROOT/'docs/program/execution/2026-10-22/program-refresh-bayesian-v1'
CENSUS=ROOT/'docs/program/execution/2026-10-21/census-prophets-v2/census-register.json'
read=lambda p:json.loads(p.read_text())


def main():
    assert not BASE.exists()
    state=run.core.read(ROOT,run.core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path']=='docs/causal_proposal_bayesian_commercial_reviewed_v2_2026-10-22.pdf'
    sponsor=read(SPONSOR/'working-release.json');verify_bindings(sponsor)
    assert run.same_reader(state['reader'],sponsor['paired_monograph'])
    view=run.status(ROOT,state);graph,merged,stages,ready,registerable=run.queue(ROOT,state)
    assert {q['id']:q['status'] for q in view['proposal_gaps']}==dict(Q1='open',Q2='pass',Q3='pass',Q4='pass',Q5='open')
    results=merged['execution_program']['results'];groups={};obligations=[];lanes=defaultdict(Counter)
    for node in graph['nodes']:
        identifier=node['id'];result=results.get(identifier)
        if stages[identifier]!='proposal_now':continue
        lanes[node['lane']][result['outcome'] if result else 'open']+=1
        if result and result['outcome']=='pass':continue
        progress=merged['execution_program']['progress'].get(identifier,[])
        action=read(ROOT/progress[-1]['path'])['next_action'] if progress else node['action']
        item=dict(id=identifier,lane=node['lane'],title=node['title'],status=result['outcome'] if result else 'open',
            action=action,prerequisites=run.ledger.blockers(merged,node),outputs=node['outputs'],
            evidence=result,requires_inputs=node['requires_inputs'])
        if identifier in ['SW.CELL.bayesian_scm_state.commercial','SW.COMM.bayesian_scm_state']:
            item['corrected_source_followup']=ref(WORK/'operation-followup.json','Use corrected saved anchors; outcome remains inconclusive')
        obligations.append(item)
    for name,prefix,total in [('software','SW.CELL.',102),('reuse','SW.DECISION.',115),('chapters','TEXT.REVIEW.',22)]:
        selected={k:v for k,v in results.items() if k.startswith(prefix)}
        groups[name]=dict(Counter(v['outcome'] for v in selected.values()),open=total-len(selected),total=total)
    census_counts=Counter(x['disposition'] for x in read(CENSUS)['items'])
    assert census_counts['inspected_primary_retained_with_limits']==57 and census_counts['open_original_not_inspected']==56
    count=len(read(WORK/'reader/source-audit.json')['sources'])
    papers=read(WORK/'traceability-review.json')['scholarly_pdfs']
    sponsor_count=len(read(SPONSOR/'source-audit.json')['sources'])
    physical=read(WORK/'release-source-review.json')['checks']['physical_pages']
    BASE.mkdir()
    write(BASE/'state-snapshot.json',state);write(BASE/'status-snapshot.json',view)
    write(BASE/'remaining-operations.json',dict(reader=state['reader'],coverage=groups,
        recorded=view['recorded_proposal_operations'],proposal_operations=view['proposal_operations'],
        ready=view['ready_proposal_operations'],operations=obligations,
        census=ref(CENSUS,'57 inspected/56 unread, plus four crosscutting obligations'),proposal_accepted=False))
    independent=[]
    for lane in ['software','commercial','reuse','llm','manuscript','release','proposal_acceptance']:
        eligible=[n for n in ready if n['lane']==lane]
        if eligible:
            n=eligible[0]
            independent.append(dict(lane=lane,operation=n['id'],action=n['action'],depends=n['depends'],
                requires_inputs=n['requires_inputs'],output=n['outputs']))
    review=dict(status='pass_for_program_consistency_not_completion',reviewer=dict(name='Codex author/coordinator',kind='author'),
        evidence=[ref(BASE/'state-snapshot.json','Canonical snapshot'),ref(BASE/'remaining-operations.json','Every nonpassing obligation'),
            ref(WORK/'working-release.json','Corrected integrated reader'),ref(SPONSOR/'working-release.json','Exact paired sponsor')],
        effective_lane_counts={k:dict(v) for k,v in lanes.items()},independent_next_actions=independent,
        findings=['Current proposal scope, unified queue and exact-reader reviews agree; earlier V11 master remains historical.',
            'Recorded outcomes include inconclusive and negative results; counts are not completion or native-capability counts.',
            'All 102 software cells, 115 reuse decisions, 22 chapter reviews and 113 frontier originals retain their coverage obligations.',
            'MR01/MR02/MR03 require substantive exclusive depth and coverage; 1209 pages alone do not close them.',
            'A local vendor failure does not block independent software, reuse or frontier work. Eligible nodes have explicit actions and outputs.',
            'Public design outcomesP1-P6 justify prototype plans; no bank dataset, trial, quote or adoption is fabricated.',
            'Exact-reader Q2-Q4 were renewed sequentially before sponsor preparation; Q1/Q5 and visual acceptance stay open.',
            'The observed formfeed audit defect is preserved and repaired in a successor; future line anchors must use the same newline convention as inspection.',
            'The controller durably schedules work; no unattended research worker exists. Phase boundaries and commit/push are preservation events.'],
        known_routes=['Recover and inspect exact primary originals, complementary candidate searches and rights.',
            'Complete reasoned adopt/integrate/port/reject decisions and matched public prototype specifications.',
            'Review remaining frontier originals and synthesize them into affected chapters.',
            'Reconcile scoped coverage, exclusive depth and sponsor claims; complete independent and rendered acceptance later.'],
        unresolved_research=['General hidden-confounder identification from insufficient observational information.',
            'Arbitrary persistent dependence, unrestricted private-state optimal-policy uncertainty and universal calibration.',
            'Real bank mechanism truth, production reliability and measured economics require later justified external evidence.'],
        global_blocker=None,phase_boundaries_are_stopping_points=False,background_worker_running=False)
    write(BASE/'program-review.json',review)
    write(BASE/'continuation-checkpoint.json',dict(date='2026-10-22',status='reviewed_program_and_integrated_continuation',
        prior_git_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        state=ref(BASE/'state-snapshot.json','Current canonical snapshot'),reader=state['reader'],
        sponsor=ref(SPONSOR/'working-release.json','Current paired sponsor'),
        completed=['Verified clean baseline and remote97597a3e; both recovered integrity checks passed.',
            'Executed commercial Bayesian/state coverage and comparison with three new and seven inherited official originals.',
            'Reproduced exact identification, prior, information-clock, observability, variance, frequency and approximation examples.',
            'Preserved failed downloads and the formfeed anchor defect; reviewed a corrected successor without changing science.',
            'Integrated the findings into preserving reader and sponsor PDFs and renewed exact-reader Q2-Q4.'],
        evidence=[ref(WORK/'anchor-repair-review.json','Failure and repair'),ref(BASE/'program-review.json','Queue-wide program review')],
        remaining=ref(BASE/'remaining-operations.json','All nonpassing proposal obligations'),
        next_operation=view['next'],next_action=view['next_action'],independent_next_actions=independent,
        global_blocker=None,background_worker_running=False,visual_acceptance=False,proposal_accepted=False))
    current=ROOT/'docs/program/execution/current-program.md'
    (BASE/'prior-current-program.md').write_bytes(current.read_bytes())
    current.write_text(f'''# Current executable proposal program

Updated 22 October 2026 after commercial Bayesian/state comparisons and a
preserving source-anchor repair. This is a research and product proposal.
Prototype qualification, independent acceptance, bank validation and adoption
remain separate. The [queue-wide review](2026-10-22/program-refresh-bayesian-v1/program-review.json)
records the plan, independent next actions and unresolved research.

Use `python3 tools/run_program_reviews_v2.py status`, `next` and `check`.
The canonical ledger is [state.json](../state.json); the
[proposal scope](../master-program-proposal.md) governs. The older numbered
masters are preserved historical snapshots. Continue eligible work across
phase boundaries. One missing source does not block another lane.

## Current integrated documents

Read the [{state['reader']['pages']:,}-page monograph](../../causal_proposal_bayesian_commercial_reviewed_v2_2026-10-22.pdf)
and its [{sponsor['pages']}-page sponsor proposal](../../sponsor_proposal_bayesian_commercial_reviewed_2026-10-22.pdf).
The monograph contains {count} audited citation records and {papers} genuine
scholarly PDFs. The sponsor contains {sponsor_count} audited citations and is
paired to the exact corrected reader bytes. Q2-Q4 pass for these bytes; Q1/Q5,
all three mandatory repairs, rendered visual review and final acceptance remain open.

There are **{view['recorded_proposal_operations']} recorded outcomes of {view['proposal_operations']} proposal operations**,
with **{view['ready_proposal_operations']} ready operations**. Inconclusive outcomes preserve
unresolved obligations; recorded is not synonymous with passed or implemented.

| Area | Pass | Inconclusive | Open | Total |
|---|---:|---:|---:|---:|
| Software coverage | {groups['software'].get('pass',0)} | {groups['software'].get('inconclusive',0)} | {groups['software']['open']} | 102 |
| Reuse decisions | {groups['reuse'].get('pass',0)} | {groups['reuse'].get('inconclusive',0)} | {groups['reuse']['open']} | 115 |
| Chapter reviews | {groups['chapters'].get('pass',0)} | {groups['chapters'].get('inconclusive',0)} | {groups['chapters']['open']} | 22 |

The frontier census remains **57 inspected and 56 unread originals out of 113**,
plus four crosscutting obligations. Fourteen LLM tasks and twelve integration
requirements have scoped proposal outcomes; they do not grant runtime adoption.

## Findings integrated in this continuation

Physical reader pages {physical[0]}-{physical[1]} distinguish supplied-model computation
from intervention identification. Three new Stata originals and seven reinspected
official sources support five vendor families; five more families retain explicit
source/edition follow-ups. Coverage and vendor comparison remain inconclusive.
SAS's partial transfer and EViews/HUGIN endpoint failures are not absence findings.

Identical observed credit laws imply default reductions 0 or 0.6 and assumed
margins USD -100 or 500; equal likelihoods leave causal-model odds at their priors.
Filtering and smoothing use different information, yielding illustrative margins
of USD 15 and -10. The text distinguishes unobservable state contrasts, parameter and
process variance, Monte Carlo error and conditional approximation bounds.
Stata prediction RMSE excludes parameter-estimation error; compressed MCMC rows
need frequency weights. The specified export example has mean 0.18 rather than 0.5.
These are exact authored laws and inspected documentation, not native or bank trials.

A final inspection found newline/formfeed disagreement in the saved source anchors.
The first audit, release and reviews remain preserved. The
[repair review](2026-10-22/bayesian-commercial-v2/anchor-repair-review.json)
binds corrected snippets to unchanged original bytes and claims. The current
reader and sponsor use the corrected source audit. Earlier citation identities,
contexts, chapter inputs and financial examples remain preserved.

The prior causal-reasoning paper/repository work also survives: 24 published
subset averages reproduce, ETT 138 resolves the printed 137, and question 2883's
negative numerical target is reproducible while its death/survival semantics
remain disputed. Reference-only reuse remains the disposition for that repository.

## Required standard and remaining gaps

Every claimed banking use must connect the information clock to a causal model,
assumptions, identification or justified limits, estimation, uncertainty,
diagnostics, alternatives and monetary consequences. Sources need identity,
version/date, genuine bytes, SHA-256, inspected anchors and supported claims.
Scholarly citations require genuine PDFs. The cutoff is 7 October 2026. FinMarketing
sets the scholarly standard; aggregate length does not establish completion.

MR01 requires 17 areas across six dimensions and 100-150 substantive software pages.
MR02 requires eight developed chapters, 14 tasks and 96-112 pages.
MR03 requires four integration chapters and 12 requirements, with indicative
depth of 40-60 pages. Exclusive depth and systematic coverage both matter.

Known routes are primary-source recovery, complementary search, explicit reuse
decisions, connected synthesis, exact public references and matched prototype
designs. The [commercial omissions](2026-10-22/bayesian-commercial-v2/omissions-register.json)
name exact next evidence. Public prototype merit should precede expensive bank
experiments. Current bank data, platform access and prices are not global blockers.

General latent-confounder identification, arbitrary dependence, private-state
optimal-policy uncertainty and universal calibration remain research questions.
They may require narrower claims or extra information. Actual bank truth,
independent acceptance and real economics require later external evidence.

## Exact continuation

Controller next: **{view['next']}**. {view['next_action']}

Continue eligible software, commercial, reuse and frontier tasks independently.
Preserve completed source work and do not restart the 57 inspected originals.
The [remaining-operation register](2026-10-22/program-refresh-bayesian-v1/remaining-operations.json)
contains every nonpassing obligation and its dependencies; the
[checkpoint](2026-10-22/program-refresh-bayesian-v1/continuation-checkpoint.json)
contains exact actions for independent lanes. No global blocker is present.

Use bounded output, newline-consistent source anchors and serialized canonical
mutations. Await every publication/review operation before the next dependent
step. Keep failures immutable. No unattended research worker is running.
The inherited image allowance is exhausted under `/home/ubuntu/AGENTS.md`;
a fresh visual session is needed for rendered acceptance, while research stays eligible.
''')
    run.render(ROOT,state)
    print(json.dumps(dict(reader=state['reader'],sponsor_pages=sponsor['pages'],records=count,papers=papers,
        recorded=view['recorded_proposal_operations'],ready=view['ready_proposal_operations'],
        next=view['next'],program_review='pass_for_consistency',proposal_accepted=False)))


if __name__=='__main__':main()
