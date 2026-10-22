#!/usr/bin/env python3
"""Review every nonpassing obligation after commercial observation integration."""
from collections import Counter,defaultdict
import json
from pathlib import Path
import subprocess
import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write

run=extension.base;ROOT=run.core.ROOT
WORK=ROOT/'docs/program/execution/2026-10-22/observations-commercial-v1'
PUB=WORK/'publication-v2'
SPONSOR=ROOT/'docs/program/execution/2026-10-22/sponsor-observations-v1'
BASE=ROOT/'docs/program/execution/2026-10-22/program-refresh-observations-v1'
PRIOR=ROOT/'docs/program/execution/2026-10-22/program-refresh-domain-v1'
CENSUS=ROOT/'docs/program/execution/2026-10-22/census-domain-knowledge-v1/census-register.json'
read=lambda p:json.loads(p.read_text())

def main():
    assert not BASE.exists()
    state=run.core.read(ROOT,run.core.STATE);assert state['execution_runtime']['active'] is None
    assert state['reader']['path']=='docs/causal_proposal_observations_reviewed_v2_2026-10-22.pdf'
    sponsor=read(SPONSOR/'working-release.json');verify_bindings(sponsor)
    assert run.same_reader(state['reader'],sponsor['paired_monograph'])
    view=run.status(ROOT,state);graph,merged,stages,ready,_=run.queue(ROOT,state)
    assert {q['id']:q['status'] for q in view['proposal_gaps']}==dict(Q1='open',Q2='pass',Q3='pass',Q4='pass',Q5='open')
    results=merged['execution_program']['results'];obligations=[];groups={};lanes=defaultdict(Counter)
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
        if identifier in previous:
            for k in ['corrected_source_followup','source_followup']:
                if k in previous[identifier]:item[k]=previous[identifier][k]
            if identifier in ['LL.CENSUS','SW.CELL.iv_rd_design.R']:item['action']=previous[identifier]['action']
        if identifier=='SW.CELL.iv_rd_design.Python':
            item['corrected_source_followup']=ref(ROOT/'docs/program/execution/2026-10-22/python-iv-rd-preflight-v2/review.json','Two cutoff commits and eight blobs acquired; diagnostic semantics inspected; coverage remains open')
            item['action']=read(ROOT/'docs/program/execution/2026-10-22/python-iv-rd-preflight-v2/review.json')['next_action']
        if identifier in ['SW.CELL.observations_data.commercial','SW.COMM.observations_data']:
            item['action']='Complete complementary market discovery, four unread candidate families, detailed IBM scoring, exact cutoff editions and deployment rights; qualify generated identity/clock/inclusion cases before bank studies.'
            item['source_followup']=ref(WORK/'omissions-register.json','Candidate-specific evidence and acquisition follow-ups')
        obligations.append(item)
    for name,prefix,total in [('software','SW.CELL.',102),('reuse','SW.DECISION.',115),('chapters','TEXT.REVIEW.',22)]:
        selected={k:v for k,v in results.items() if k.startswith(prefix)}
        groups[name]=dict(Counter(v['outcome'] for v in selected.values()),open=total-len(selected),total=total)
    census_counts=Counter(x['disposition'] for x in read(CENSUS)['items'])
    inspected=census_counts['inspected_primary_retained_with_limits'];unread=census_counts['open_original_not_inspected']
    assert (inspected,unread)==(59,54)
    count=len(read(PUB/'reader/source-audit.json')['sources']);papers=read(PUB/'traceability-review.json')['scholarly_pdfs']
    sponsor_count=len(read(SPONSOR/'source-audit.json')['sources'])
    physical=read(PUB/'release-source-review.json')['checks']['physical_pages']
    BASE.mkdir();write(BASE/'state-snapshot.json',state);write(BASE/'status-snapshot.json',view)
    write(BASE/'remaining-operations.json',dict(reader=state['reader'],coverage=groups,
        recorded=view['recorded_proposal_operations'],proposal_operations=view['proposal_operations'],ready=view['ready_proposal_operations'],
        operations=obligations,census=ref(CENSUS,'Every original disposition retained'),proposal_accepted=False))
    independent=[]
    for lane in ['software','commercial','reuse','llm','manuscript','release','proposal_acceptance']:
        eligible=[n for n in ready if n['lane']==lane]
        if eligible:
            n=eligible[0];independent.append(dict(lane=lane,operation=n['id'],action=n['action'],depends=n['depends'],requires_inputs=n['requires_inputs'],output=n['outputs']))
    evidence=[ref(BASE/'state-snapshot.json','Canonical snapshot'),ref(BASE/'remaining-operations.json','All nonpassing obligations'),
        ref(PUB/'working-release.json','Current integrated reader'),ref(SPONSOR/'working-release.json','Paired sponsor'),
        ref(WORK/'plan-review.json','Reviewed execution'),ref(WORK/'review.json','Six-original observation review'),
        ref(WORK/'comparison-review.json','Eight candidate dispositions'),ref(WORK/'acquisition-review.json','Preserved source recovery'),
        ref(WORK/'transition-recovery.json','Rejected early receipt and successful sequential recovery'),
        ref(PUB/'copyedit-repair.json','Preserved v1 and citation-spacing successor'),
        ref(ROOT/'docs/program/execution/2026-10-22/python-iv-rd-preflight-v2/review.json','Independent next-operation source progress')]
    review=dict(status='pass_for_program_consistency_not_completion',reviewer=dict(name='Codex author/coordinator',kind='author'),
        evidence=evidence,effective_lane_counts={k:dict(v) for k,v in lanes.items()},independent_next_actions=independent,
        findings=['Proposal scope and receipts agree; recorded outcomes include inconclusive work and are not completed products.',
            'All 102 software cells, 115 reuse decisions, 22 chapter reviews, 113 originals and four census obligations retain their contracts.',
            'Commercial observation coverage and comparison advanced together; four documented families do not close the eight-family frame or market search.',
            'Source404 and index-only response were recovered locally; all failed attempts survive without blocking independent lanes.',
            'Exact examples distinguish map uncertainty, information clocks, inclusion and stipulated value from native implementation and measured returns.',
            'Native or bank qualification is not a proposal prerequisite; public tests must first demonstrate merit.',
            'Q2-Q4 bind current reader bytes; exact paired sponsor, all previous citation identities and manuscript inputs are preserved.',
            'Python continuation recovered two cutoff revisions and eight Git-verified originals. linearmodels anderson_rubin is an overidentification property, not coefficient-null confidence-set inversion; selected first-stage statistics require distribution/covariance metadata. CausalPy sharp-RD-only inheritance remains.',
            'A premature dependent receipt was rejected, preserved and repaired after the controller start completed; await every canonical mutation.',
            'Q1/Q5, three mandatory repairs and rendered acceptance remain open; no unattended worker or global blocker.'],
        known_routes=['Recover complementary technical originals and exact revisions, then complete candidate-specific use/rejection decisions.',
            'Inspect 54 unread frontier originals and four search/task obligations without blocking software or integration work.',
            'Use known-identity, late-arrival and inclusion generators, with held-out calibration and matched baselines, before paid qualification.',
            'Reconcile exclusive chapter depth and full coverage for all repairs; finish rendered review in a fresh image session.'],
        unresolved_research=['Unrestricted hidden-confounder identification and graph-to-effect calibration.',
            'General persistent dependence, private-state optimal-policy uncertainty and arbitrary-learner calibration.',
            'No universal conversion of vendor or LLM scores into causal/linkage truth; missing information may require narrower targets.',
            'Bank assignment truth, production reliability and measured economics remain later evidence-dependent claims.'],
        global_blocker=None,phase_boundaries_are_stopping_points=False,background_worker_running=False)
    write(BASE/'program-review.json',review)
    write(BASE/'continuation-checkpoint.json',dict(date='2026-10-22',status='reviewed_program_and_integrated_continuation',
        prior_git_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        state=ref(BASE/'state-snapshot.json','Canonical state'),reader=state['reader'],sponsor=ref(SPONSOR/'working-release.json','Paired sponsor'),
        completed=['Verified clean b38b96b0 baseline and remote equality; both recovery checks passed.',
            'Executed reviewed commercial observation coverage and comparison with six originals, four documented families and eight candidates.',
            'Preserved nine sandbox DNS failures, AWS404, IBM index and successful official-link recovery.',
            'Reproduced exact clock, linkage, uncertainty, selection and monetary examples.',
            'Advanced the independent Python IV/RD lane with two cutoff repository pins, eight verified source blobs and selected diagnostic review; no coverage outcome claimed.',
            'Integrated and compiled corrected monograph/sponsor successors, preserved earlier content, renewed Q2-Q4 and refreshed every nonpassing obligation.'],
        evidence=[ref(BASE/'program-review.json','Queue-wide review'),ref(PUB/'release-source-review.json','Integrated source and exact-argument review')],
        remaining=ref(BASE/'remaining-operations.json','Complete remaining register'),next_operation=view['next'],next_action=view['next_action'],
        independent_next_actions=independent,global_blocker=None,background_worker_running=False,visual_acceptance=False,proposal_accepted=False))
    current=ROOT/'docs/program/execution/current-program.md';(BASE/'prior-current-program.md').write_bytes(current.read_bytes())
    current.write_text(f'''# Current executable proposal program

Updated 22 October 2026 after commercial observation coverage and comparison.
The [queue-wide review](2026-10-22/program-refresh-observations-v1/program-review.json)
binds every nonpassing obligation and independent next action. This is a research
and product proposal. Native qualification, bank validation and adoption are later.

Use `python3 tools/run_program_reviews_v2.py status`, `next` and `check`.
The canonical ledger is [state.json](../state.json); the
[proposal scope](../master-program-proposal.md) governs. Earlier numbered masters
remain historical snapshots. Continue eligible work across phase boundaries.

## Current integrated documents

Read the [{state['reader']['pages']:,}-page monograph](../../causal_proposal_observations_reviewed_v2_2026-10-22.pdf)
and its [{sponsor['pages']}-page sponsor proposal](../../sponsor_proposal_observations_reviewed_2026-10-22.pdf).
The reader has {count} audited citation records and {papers} genuine scholarly PDFs;
the sponsor has {sponsor_count} audited citations and binds the exact reader.
Q2-Q4 pass. Q1/Q5, all mandatory repairs, rendered review and final acceptance remain open.

There are **{view['recorded_proposal_operations']} recorded outcomes of {view['proposal_operations']} proposal operations**,
with **{view['ready_proposal_operations']} ready operations**. Inconclusive outcomes
are retained as unfinished obligations; these counts are not native capabilities.

| Area | Pass | Inconclusive | Open | Total |
|---|---:|---:|---:|---:|
| Software coverage | {groups['software'].get('pass',0)} | {groups['software'].get('inconclusive',0)} | {groups['software']['open']} | 102 |
| Reuse decisions | {groups['reuse'].get('pass',0)} | {groups['reuse'].get('inconclusive',0)} | {groups['reuse']['open']} | 115 |
| Chapter reviews | {groups['chapters'].get('pass',0)} | {groups['chapters'].get('inconclusive',0)} | {groups['chapters']['open']} | 22 |

The frontier census remains **{inspected} inspected and {unread} unread originals out of 113**,
plus four crosscutting obligations. Fourteen LLM-task and twelve integration reviews
have scoped outcomes, without live-model superiority or cross-repository adoption.

## Integrated findings

Physical pages {physical[0]}-{physical[1]}, section 24.13, compare AWS Entity Resolution,
IBM QualityStage, Databricks feature lookup and Snowflake historical storage.
Six official originals support separate contracts for matching scores, availability
clocks, training/serving behavior, inclusion, schema and replay. Four other families,
exact cutoff revisions, detailed IBM scoring and commercial rights remain unresolved.

Exact authored examples show event-only lookup returning 9 when only 2 was available;
two map contrasts +4/-4 become 2.4 at stipulated probability 0.8, changing hypothetical
margin from USD 10 to USD -6. Selection changes population effect 4 to 5.2. These are
reproducible mathematical examples, not vendor measurements or bank returns.
The [omissions](2026-10-22/observations-commercial-v1/omissions-register.json)
give candidate-specific next actions. All prior sources and chapter inputs survive.

## Required standard and remaining gaps

Each banking use connects decision, information clock, target, assumptions,
identification or limits, estimation, uncertainty, diagnostics, alternatives and
monetary consequences. Sources need authentic bytes, identity/version/date, hashes
and inspected anchors; scholarly citations need real PDFs. Cutoff: 7 October 2026.
FinMarketing sets the scholarly standard; total length does not establish acceptance.

MR01 requires 17 areas across six dimensions and 100-150 substantive software pages.
MR02 requires eight developed chapters, fourteen tasks and 96-112 pages. MR03
requires four integration chapters and twelve requirements, with indicative 40-60
pages. Exclusive depth and complete systematic coverage both matter.

Known routes are source recovery, complementary searches, reasoned reuse, connected
synthesis and public known-law studies. General latent identification, arbitrary
dependence, private-state optimal-policy uncertainty and universal score calibration
need narrower claims or additional information; no general solution is promised.

## Exact continuation

Controller next: **{view['next']}**. {view['next_action']}

The [remaining register](2026-10-22/program-refresh-observations-v1/remaining-operations.json)
retains all {len(obligations)} nonpassing obligations and dependencies. The
[checkpoint](2026-10-22/program-refresh-observations-v1/continuation-checkpoint.json)
lists independent next actions. The
[Python source continuation](2026-10-22/python-iv-rd-preflight-v2/review.json)
records two cutoff commits and eight verified originals. Next inspect delegated
rank/covariance/diagnostic kernels and separate overidentification tests from
weak-IV coefficient confidence sets. Python RD and CausalPy IV still need review;
inherited CausalPy evidence covers sharp RD with equal-tail quantiles only.

Wait for every canonical mutation to finish before a dependent transition.
Checkpoints and Git preservation are not permission gates. No global blocker or
unattended research worker exists. The inherited six-preview allowance under
`/home/ubuntu/AGENTS.md` is exhausted; rendered acceptance needs a fresh visual
session, while source research and manuscript work remain eligible.
''')
    run.render(ROOT,state)
    print(json.dumps(dict(reader=state['reader'],sponsor_pages=sponsor['pages'],records=count,papers=papers,
        recorded=view['recorded_proposal_operations'],ready=view['ready_proposal_operations'],remaining=len(obligations),next=view['next'],proposal_accepted=False)))

if __name__=='__main__':main()
