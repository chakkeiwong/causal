#!/usr/bin/env python3
"""Refresh the complete executable master from effective, reviewed receipts."""
from collections import Counter, defaultdict
import json
from pathlib import Path
import subprocess
import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run=extension.base
ROOT=run.core.ROOT
WORK=ROOT/'docs/program/execution/2026-10-22/r-iv-rd-v1'
SPONSOR=ROOT/'docs/program/execution/2026-10-22/sponsor-r-iv-rd-v1'
BASE=ROOT/'docs/program/execution/2026-10-22/program-refresh-r-iv-v1'
CENSUS=ROOT/'docs/program/execution/2026-10-21/census-prophets-v2/census-register.json'
PRIOR=ROOT/'docs/program/execution/2026-10-22/program-refresh-bayesian-v1'
read=lambda p:json.loads(p.read_text())


def main():
    assert not BASE.exists()
    state=run.core.read(ROOT,run.core.STATE);assert state['execution_runtime']['active'] is None
    assert state['reader']['path']=='docs/causal_proposal_r_iv_rd_reviewed_2026-10-22.pdf'
    sponsor=read(SPONSOR/'working-release.json');verify_bindings(sponsor)
    assert run.same_reader(state['reader'],sponsor['paired_monograph'])
    view=run.status(ROOT,state);graph,merged,stages,ready,_=run.queue(ROOT,state)
    assert {q['id']:q['status'] for q in view['proposal_gaps']}==dict(Q1='open',Q2='pass',Q3='pass',Q4='pass',Q5='open')
    results=merged['execution_program']['results'];groups={};obligations=[];lanes=defaultdict(Counter)
    previous={r['id']:r for r in read(PRIOR/'remaining-operations.json')['operations']}
    for node in graph['nodes']:
        identifier=node['id'];result=results.get(identifier)
        if stages[identifier]!='proposal_now':continue
        lanes[node['lane']][result['outcome'] if result else 'open']+=1
        if result and result['outcome']=='pass':continue
        progress=merged['execution_program']['progress'].get(identifier,[])
        action=read(ROOT/progress[-1]['path'])['next_action'] if progress else node['action']
        item=dict(id=identifier,lane=node['lane'],title=node['title'],status=result['outcome'] if result else 'open',
            action=action,prerequisites=run.ledger.blockers(merged,node),outputs=node['outputs'],evidence=result,requires_inputs=node['requires_inputs'])
        if identifier in previous and 'corrected_source_followup' in previous[identifier]:
            item['corrected_source_followup']=previous[identifier]['corrected_source_followup']
        if identifier=='SW.CELL.iv_rd_design.R':
            item['action']='Inspect nine complementary IV/RD leads at cutoff; complete the R census. CRAN rdrobust4.1.1 is now resolved as post-cutoff; retain4.0.0. Native trials and transitive distribution rights remain separate prototype obligations.'
            item['source_followup']=ref(WORK/'omissions-register.json','Exact scoped follow-ups and resolved CRAN version')
        obligations.append(item)
    for name,prefix,total in [('software','SW.CELL.',102),('reuse','SW.DECISION.',115),('chapters','TEXT.REVIEW.',22)]:
        selected={k:v for k,v in results.items() if k.startswith(prefix)}
        groups[name]=dict(Counter(v['outcome'] for v in selected.values()),open=total-len(selected),total=total)
    census_counts=Counter(x['disposition'] for x in read(CENSUS)['items'])
    inspected=census_counts['inspected_primary_retained_with_limits'];unread=census_counts['open_original_not_inspected']
    count=len(read(WORK/'reader/source-audit.json')['sources']);papers=read(WORK/'traceability-review.json')['scholarly_pdfs']
    sponsor_count=len(read(SPONSOR/'source-audit.json')['sources'])
    physical=read(WORK/'release-source-review.json')['checks']['physical_pages']
    BASE.mkdir();write(BASE/'state-snapshot.json',state);write(BASE/'status-snapshot.json',view)
    write(BASE/'remaining-operations.json',dict(reader=state['reader'],coverage=groups,
        recorded=view['recorded_proposal_operations'],proposal_operations=view['proposal_operations'],ready=view['ready_proposal_operations'],
        operations=obligations,census=ref(CENSUS,'Preserved original-candidate register'),proposal_accepted=False))
    independent=[]
    for lane in ['software','commercial','reuse','llm','manuscript','release','proposal_acceptance']:
        eligible=[n for n in ready if n['lane']==lane]
        if eligible:
            n=eligible[0];independent.append(dict(lane=lane,operation=n['id'],action=n['action'],depends=n['depends'],
                requires_inputs=n['requires_inputs'],output=n['outputs']))
    review=dict(status='pass_for_program_consistency_not_completion',reviewer=dict(name='Codex author/coordinator',kind='author'),
        evidence=[ref(BASE/'state-snapshot.json','Canonical snapshot'),ref(BASE/'remaining-operations.json','Every nonpassing obligation'),
            ref(WORK/'working-release.json','Integrated reader'),ref(SPONSOR/'working-release.json','Exact paired sponsor'),
            ref(WORK/'plan-review.json','Reviewed and executed continuation')],
        effective_lane_counts={k:dict(v) for k,v in lanes.items()},independent_next_actions=independent,
        findings=['Current scope and queue agree; recorded outcomes include inconclusive/negative findings and are not implementation counts.',
            'All 102 software cells, 115 reuse decisions, 22 chapter reviews and 113 frontier originals retain their obligations.',
            'Six R package profiles and five reference-only decisions advance the survey; nine discovered leads retain cutoff/technical follow-ups.',
            'CRAN 4.1.1 publication is after the client cutoff; do not keep the resolved distribution issue as an unknown global blocker.',
            'Package declared dependencies and actual rights texts improve evidence; transitive clearance and native behavior remain scoped prototype work.',
            'Prior Bayesian anchor repair remains bound; new excerpts use newline-consistent indexing and are revalidated.',
            'Q2-Q4 pass for current reader bytes; sponsor is paired after serialized renewals. Q1/Q5 and rendered acceptance stay open.',
            'Phase boundaries, local acquisition failures and Git preservation do not block independent lanes; no unattended research worker exists.'],
        known_routes=['Recover and inspect complementary primary originals with exact cutoff/version/rights records.',
            'Finish reasoned reuse decisions and concrete conversion/refusal contracts; run only separately scoped native/public prototypes.',
            'Review remaining frontier originals and integrate them into substantive chapters.',
            'Reconcile exclusive depth and full coverage against all three mandatory repairs; complete rendered and independent acceptance separately.'],
        unresolved_research=['General hidden-confounder identification and unrestricted graph-to-effect calibration.',
            'Arbitrary persistent dependence, private-state optimal-policy uncertainty and universal learner calibration.',
            'Bank assignment truth, production reliability and real economics require later decision-relevant evidence.'],
        global_blocker=None,phase_boundaries_are_stopping_points=False,background_worker_running=False)
    write(BASE/'program-review.json',review)
    write(BASE/'continuation-checkpoint.json',dict(date='2026-10-22',status='reviewed_program_and_integrated_continuation',
        prior_git_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        state=ref(BASE/'state-snapshot.json','Final canonical state of this continuation'),reader=state['reader'],
        sponsor=ref(SPONSOR/'working-release.json','Paired sponsor'),
        completed=['Recovered passing runtime/master checks and clean 2cc842bf baseline.',
            'Acquired 23 bounded public originals; preserved sandbox DNS failures and repaired pre-publication source-parser validations.',
            'Reviewed six pinned R packages, preserved inherited grf/fixest boundaries and resolved CRAN rdrobust4.1.1 timing.',
            'Executed exact authored credit-policy, weak-set, discrete-support and randomization references.',
            'Recorded inconclusive R coverage and five completed reference-only reuse decisions.',
            'Compiled preserving monograph/sponsor successors and renewed Q2-Q4 sequentially.'],
        evidence=[ref(WORK/'review.json','Substantive review'),ref(BASE/'program-review.json','Queue-wide master review'),
            ref(WORK/'next-lane-preflight.json','Located Python IV/RD inputs and exact next actions; no completed review claimed')],
        remaining=ref(BASE/'remaining-operations.json','Every nonpassing obligation'),next_operation=view['next'],next_action=view['next_action'],
        independent_next_actions=independent,global_blocker=None,background_worker_running=False,visual_acceptance=False,proposal_accepted=False))
    current=ROOT/'docs/program/execution/current-program.md';(BASE/'prior-current-program.md').write_bytes(current.read_bytes())
    current.write_text(f'''# Current executable proposal program

Updated 22 October 2026 after the R instrumental-variable and regression-discontinuity
review. The [queue-wide review](2026-10-22/program-refresh-r-iv-v1/program-review.json)
binds the current plan, evidence and independent actions. This is a research and
product proposal; native qualification, bank validation and adoption are separate.

Use `python3 tools/run_program_reviews_v2.py status`, `next` and `check`.
The canonical ledger is [state.json](../state.json); the
[proposal scope](../master-program-proposal.md) governs. Earlier numbered masters
remain historical snapshots. Continue eligible work across phase boundaries.

## Current integrated documents

Read the [{state['reader']['pages']:,}-page monograph](../../causal_proposal_r_iv_rd_reviewed_2026-10-22.pdf)
and its [{sponsor['pages']}-page sponsor proposal](../../sponsor_proposal_r_iv_rd_reviewed_2026-10-22.pdf).
The monograph contains {count} audited citation records and {papers} genuine
scholarly PDFs; the sponsor contains {sponsor_count} audited citations and binds
the exact current monograph. Q2-Q4 pass for these bytes. Q1/Q5, all three mandatory
repairs, rendered review and final acceptance remain open.

There are **{view['recorded_proposal_operations']} recorded outcomes of {view['proposal_operations']} proposal operations**,
with **{view['ready_proposal_operations']} ready operations**. Recorded outcomes include
inconclusive findings; they are not completed products or native integrations.

| Area | Pass | Inconclusive | Open | Total |
|---|---:|---:|---:|---:|
| Software coverage | {groups['software'].get('pass',0)} | {groups['software'].get('inconclusive',0)} | {groups['software']['open']} | 102 |
| Reuse decisions | {groups['reuse'].get('pass',0)} | {groups['reuse'].get('inconclusive',0)} | {groups['reuse']['open']} | 115 |
| Chapter reviews | {groups['chapters'].get('pass',0)} | {groups['chapters'].get('inconclusive',0)} | {groups['chapters']['open']} | 22 |

The frontier census remains **{inspected} inspected and {unread} unread originals out of 113**,
plus four crosscutting obligations. Fourteen LLM task and twelve integration
reviews have scoped proposal outcomes; they do not establish live-model or
cross-repository adoption claims.

## Findings integrated in this continuation

Physical reader pages {physical[0]}-{physical[1]} compare AER 1.2-17, ivreg 0.6-8,
ivmodel 1.9.1, rdrobust 4.0.0, rddensity 3.0 and rdlocrand 3.0. Five reuse decisions
are completed as reference-only choices, with integration_allowed=false.
Nine complementary leads remain uninspected, so overall R IV/RD coverage is
inconclusive. [Omissions and exact follow-ups](2026-10-22/r-iv-rd-v1/omissions-register.json)
retain the census, distribution rights, native tests and visual work separately.

The CRAN 4.1.1 publication timestamp is 7 October 23:20:02 UTC, after the exact
15:59:59 UTC cutoff; 4.0.0 remains the selected distribution. ivmodel's pinned
license file supplies an MIT alternative. Its CLR source also catches some
numerical errors and substitutes zero; native admission needs an explicit
failure-detection or reviewed-repair path. No R package was executed.

Exact authored laws show LATE -150 USD versus ATE -70 USD and ITT -60 USD, with assumed
policy margins 50, -30, 10 USD for different interventions. Gaussian inversion can
produce disconnected/unbounded sets; an empty finite grid need not mean an empty
global set. Integer-score observations admit continuous models with different
cutoff effects; declared slope bounds give margins [-10,30] USD. A fixed-window
twenty-allocation sharp-null reference gives p=.1. These are reproducible
mathematical examples, not empirical calibration or bank returns.

All previous source identities, citation contexts and chapter inputs survive.
The Bayesian source-anchor repair, commercial state comparisons and earlier
causal-reasoning repository findings remain preserved. New snippets were checked
against the actual newline-delimited originals before release.

## Required standard and remaining gaps

Every claimed banking use must connect its decision and information clock to
the causal target, assumptions, identification or limits, estimation, uncertainty,
diagnostics, alternatives and monetary consequences. Sources need genuine bytes,
identity/version/date, SHA-256, inspected anchors and supported claims. Scholarly
citations require real PDFs; the cutoff is 7 October 2026. FinMarketing sets the
scholarly standard. Total length is not acceptance.

MR01 requires 17 areas across six dimensions and 100-150 substantive software pages.
MR02 requires eight developed chapters, 14 tasks and 96-112 pages. MR03 requires
four integration chapters and 12 requirements, with indicative 40-60 pages.
Exclusive depth and systematic coverage both matter.

Known routes are primary-source recovery, complementary search, reasoned reuse
decisions, connected synthesis, exact public references and scoped prototype
studies. Expensive bank studies follow demonstrated prototype merit. Missing bank
data, vendor prices or platform access do not block independent proposal lanes.
General latent identification, arbitrary dependence, private-state optimal-policy
uncertainty and universal calibration remain research questions requiring narrower
claims or additional information. Bank truth and measured economics remain later
conditional evidence.

## Exact continuation

Controller next: **{view['next']}**. {view['next_action']}

The [remaining-operation register](2026-10-22/program-refresh-r-iv-v1/remaining-operations.json)
contains every nonpassing obligation and dependency; the
[checkpoint](2026-10-22/program-refresh-r-iv-v1/continuation-checkpoint.json)
lists exact independent next actions. No global blocker is present.

Keep tool output bounded, use newline-consistent anchors, and serialize canonical
mutations through completion. Preserve failures and earlier releases. Checkpoints
and Git preservation are not permission or phase gates. No unattended research
worker is running. The inherited six-preview allowance under `/home/ubuntu/AGENTS.md`
is exhausted; a fresh visual session is needed for rendered acceptance while
source research and proposal work remain eligible.
''')
    run.render(ROOT,state)
    print(json.dumps(dict(reader=state['reader'],sponsor_pages=sponsor['pages'],records=count,papers=papers,
        recorded=view['recorded_proposal_operations'],ready=view['ready_proposal_operations'],next=view['next'],proposal_accepted=False)))


if __name__=='__main__':main()
