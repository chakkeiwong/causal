#!/usr/bin/env python3
"""Snapshot effective proposal gaps and preserve the preceding human entrypoint."""
from collections import Counter
import json
from pathlib import Path
import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-19/recovery-retrieval-selfcorrection-v1'
WORK=ROOT/'docs/program/execution/2026-10-19/census-retrieval-selfcorrection-v1'
SPONSOR=ROOT/'docs/program/execution/2026-10-19/sponsor-retrieval-selfcorrection-v1'
CENSUS=ROOT/'docs/program/execution/2026-10-19/census-retrieval-selfcorrection-v1/census-register.json'
run=extension.base
read=lambda p:json.loads(p.read_text())


def main():
    assert not BASE.exists()
    state=run.core.read(ROOT,run.core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path']=='docs/causal_proposal_retrieval_selfcorrection_reviewed_2026-10-19.pdf'
    view=run.status(ROOT,state);graph,merged,stages=run.combined(ROOT,state)
    assert {r['id']:r['status'] for r in view['proposal_gaps']}==dict(Q1='open',Q2='pass',Q3='pass',Q4='pass',Q5='open')
    sponsor=read(SPONSOR/'working-release.json');verify_bindings(sponsor)
    assert run.same_reader(state['reader'],sponsor['paired_monograph'])
    results=merged['execution_program']['results'];operations=[];groups={}
    for node in graph['nodes']:
        key=node['id'];result=results.get(key)
        if stages[key]!='proposal_now' or result and result['outcome']=='pass':continue
        checkpoints=merged['execution_program']['progress'].get(key,[])
        action=read(ROOT/checkpoints[-1]['path'])['next_action'] if checkpoints else node['action']
        operations.append(dict(id=key,lane=node['lane'],status=result['outcome'] if result else 'open',title=node['title'],action=action,prerequisites=run.ledger.blockers(merged,node),outputs=node['outputs'],evidence=result,requires_inputs=node['requires_inputs']))
    for name,prefix,total in [('software','SW.CELL.',102),('reuse','SW.DECISION.',115),('chapters','TEXT.REVIEW.',22)]:
        rows={k:v for k,v in results.items() if k.startswith(prefix)}
        groups[name]=dict(Counter(v['outcome'] for v in rows.values()),open=total-len(rows),total=total)
    BASE.mkdir()
    write(BASE/'state-snapshot.json',state);write(BASE/'status-snapshot.json',view)
    write(BASE/'remaining-operations.json',dict(reader=state['reader'],recorded=view['recorded_proposal_operations'],proposal_operations=view['proposal_operations'],ready=view['ready_proposal_operations'],by_lane=dict(Counter(x['lane'] for x in operations)),coverage=groups,operations=operations,census=ref(CENSUS,'48 inspected/65 unread originals'),scope='All effective nonpassing proposal operations; later institutional gates kept separate.',proposal_accepted=False))
    write(BASE/'recovery-checkpoint.json',dict(status='recovered_and_continued',canonical_state_snapshot=ref(BASE/'state-snapshot.json','Exact canonical ledger'),current_reader=state['reader'],sponsor=ref(SPONSOR/'working-release.json','Matched reviewed sponsor'),remaining=ref(BASE/'remaining-operations.json','Every nonpassing proposal obligation'),completed=['Recovered interrupted commercial synthetic-control build; paired1094-page reader and18-page sponsor; both integrity controllers passed.','Pushed recovery commit84f10f6a637f467568c95b77082cdd26f3115abd to origin/main.','Continued next C++ identification operation:12authenticated native files, inherited Rcpp comparison, exact coupled-root and lending examples, bounded inconclusive review.','Integrated source findings and conformance plan in the1097-page monograph and20-page sponsor; both integrity checks passed.',
        'Continued census candidates254and32: two genuine historical PDFs, source-critical retrieval/adaptive-repair synthesis and exact23-attempt/four-acceptance accounting;48inspected/65unread.',
        'Integrated the two-paper argument and proposed public prototype protocol into preserving paired successors.'],evidence=[ref(WORK/n,'Historical source and census review evidence') for n in ['plan-review.json','source-audit.json','primary-review.json','exact-results.json','census-register.json','task-map.json','reconciliation-review.json']],next_actions=[view['next']+': '+view['next_action'],'Continue65unread originals and targeted failed-search/negative-result lanes; preserve originals, cutoff and adverse results.','Native identification: align original proofs, qualify multi-conditioning and nested kernels, joint abduction, typed statuses, numeric support and wrapper semantics; inspect remaining candidates.','Commercial synthetic control: inspect five remaining families, resolve component notices and inspect compiled rounding; preserve donor/placebo obligations.','Complete mandatory software, LLM/agent and CLI/MCP repair rollups and reconcile exact-reader depth before final acceptance.'],global_blocker=None,visual_acceptance=False,proposal_accepted=False,background_worker_running=False))
    path=ROOT/'docs/program/execution/current-program.md';old=path.read_text();(BASE/'prior-current-program.md').write_text(old)
    pages=state['reader']['pages'];brief=sponsor['pages']
    header=f'''# Current executable proposal program

## Recovery and continuation: 19 October 2026

Use python3 tools/run_program_reviews_v2.py status, next and check. The canonical
ledger is docs/program/state.json; the [proposal scope](../master-program-proposal.md)
governs the deliverable. Earlier numbered controllers are preserved historical views.

The [{pages:,}-page working monograph](../../causal_proposal_retrieval_selfcorrection_reviewed_2026-10-19.pdf)
is paired with the [{brief}-page sponsor brief](../../sponsor_proposal_retrieval_selfcorrection_reviewed_2026-10-19.pdf).
It contains800 audited citation records and207 genuine scholarly PDFs. All797 predecessor
identities and contexts survive. Q2-Q4 pass for these exact reader bytes; Q1/Q5, rendered
visual review and final acceptance remain open. This is a product proposal, not an accepted product.

Recovery finished the interrupted commercial synthetic-control publication and continued the
C++ identification review with preserving paired PDFs. Execution then inspected two genuine
historical retrieval/self-correction originals. Retrieval faithfulness, evidence truth, causal
applicability, adaptive test success and final acceptance remain distinct. CoT-SelfEvolve retains
an unresolved anonymized code link and2024arXiv/2025template distinction. Exact authored ten-request
accounting requires23attempts for six test successes and four causal acceptances; assumed costs46USD
and accepted net14USD are not bank ROI. No live model or package was run.
There are **{view['recorded_proposal_operations']} recorded outcomes of {view['proposal_operations']} proposal operations**, with **{view['ready_proposal_operations']} ready**.
Software:2pass/26inconclusive/74open of102. Reuse:18pass/3inconclusive/94open of115.
Chapters:20pass/2inconclusive of22; L1/L6 remain incomplete. Census:48inspected/65unread of113.
All14 LLM task reviews and12 integration requirements have bounded proposal outcomes,
not general implementation or bank qualification. Inconclusive outcomes retain open obligations.

### Required standard

Connect the banking decision, clocks and units to assumptions, causal identification or
limits, estimation, uncertainty, diagnostics and economics. Use genuine scholarly PDFs,
primary technical anchors, immutable source identity/version/SHA-256 and reproducible
examples. Literature cutoff:7October2026. FinMarketing supplies a scholarship standard,
not acceptance by length. MR01 covers17areas by6language/commercial dimensions and100-150
substantive pages; MR02 covers8chapters/14tasks and96-112pages; MR03 covers4chapters/12requirements
and indicative40-60pages. Coverage and developed argument must pass, not merely page count.
All three repair rollups and full release reconciliation remain open.

### Exact continuation

Next: **{view['next']}**. {view['next_action']}
Continue65unread census originals and recorded search-specificity/saturation obligations.
Resolve the actual CoT-SelfEvolve artifact, retrieval/benchmark overlap and final held-out acceptance. C++ followups require original-proof alignment,
multi-conditioning/kernel fixtures, joint abduction, support-zero and wrapper conformance,
and other native candidates. Commercial followups include five uninspected synthetic-control
families and unresolved source/host/plugin rights. General hidden-confounder identification,
joint dependence and arbitrary-learner/policy guarantees remain research uncertainties.
Independent review, real bank truth, target-platform trials and adoption remain later
conditional work; public evidence and synthetic designs continue now.

[Every nonpassing obligation](2026-10-19/recovery-retrieval-selfcorrection-v1/remaining-operations.json)
· [Recovery checkpoint](2026-10-19/recovery-retrieval-selfcorrection-v1/recovery-checkpoint.json)

Independent ready work does not wait on a blocked branch. Checkpoints are restart records,
not permission gates. Use short commands and bounded outputs. No unattended worker runs.
The inherited image allowance is exhausted; rendered visual acceptance remains pending
and does not block source/manuscript work. No images were forwarded.

---

## Preserved prior execution records

'''
    path.write_text(header+old)
    print(json.dumps(dict(reader=state['reader'],sponsor=sponsor['pdf'],recorded=view['recorded_proposal_operations'],ready=view['ready_proposal_operations'],next=view['next'],coverage=groups,proposal_accepted=False)))

if __name__=='__main__':main()
