"""Refresh the current master from recorded grf results and exact paired releases."""
from collections import Counter
import json
from pathlib import Path
import subprocess
import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run = extension.base
ROOT = run.core.ROOT
WORK = ROOT/'docs/program/execution/2026-10-21/census-ace-v1'
SPONSOR = ROOT/'docs/program/execution/2026-10-21/sponsor-ace-v1'
BASE = ROOT/'docs/program/execution/2026-10-21/program-refresh-ace-v1'
read = lambda p: json.loads(p.read_text())


def main():
    assert not BASE.exists()
    state = run.core.read(ROOT, run.core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path'] == 'docs/causal_proposal_ace_reviewed_2026-10-21.pdf'
    sponsor = read(SPONSOR/'working-release.json')
    verify_bindings(sponsor)
    assert run.same_reader(state['reader'], sponsor['paired_monograph'])
    view = run.status(ROOT, state)
    graph, merged, stages = run.combined(ROOT, state)
    assert {q['id']:q['status'] for q in view['proposal_gaps']} == {
        'Q1':'open','Q2':'pass','Q3':'pass','Q4':'pass','Q5':'open'}
    results = merged['execution_program']['results']
    obligations, groups = [], {}
    for node in graph['nodes']:
        key, result = node['id'], results.get(node['id'])
        if stages[key] != 'proposal_now' or result and result['outcome']=='pass':
            continue
        progress = merged['execution_program']['progress'].get(key, [])
        action = read(ROOT/progress[-1]['path'])['next_action'] if progress else node['action']
        obligations.append(dict(id=key,lane=node['lane'],status=result['outcome'] if result else 'open',
            title=node['title'],action=action,prerequisites=run.ledger.blockers(merged,node),
            outputs=node['outputs'],evidence=result,requires_inputs=node['requires_inputs']))
    for name,prefix,total in [('software','SW.CELL.',102),('reuse','SW.DECISION.',115),('chapters','TEXT.REVIEW.',22)]:
        selected={k:v for k,v in results.items() if k.startswith(prefix)}
        groups[name]=dict(Counter(v['outcome'] for v in selected.values()),open=total-len(selected),total=total)
    BASE.mkdir()
    write(BASE/'state-snapshot.json',state)
    write(BASE/'status-snapshot.json',view)
    write(BASE/'remaining-operations.json',dict(reader=state['reader'],coverage=groups,
        recorded=view['recorded_proposal_operations'],proposal_operations=view['proposal_operations'],
        ready=view['ready_proposal_operations'],operations=obligations,
        census=ref(ROOT/'docs/program/execution/2026-10-21/census-ace-v1/census-register.json',
            '56 inspected and 57 unread originals; one genuine primary review added'),
        proposal_accepted=False))
    prior_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    write(BASE/'continuation-checkpoint.json',dict(date='2026-10-21',status='continued_and_integrated',
        prior_git_commit=prior_commit,state=ref(BASE/'state-snapshot.json','Canonical snapshot'),
        reader=state['reader'],sponsor=ref(SPONSOR/'working-release.json','Exact paired sponsor'),
        completed=['Inspected all ten pages of genuine July2026 ACE publisher original and preserved acquisition failures.',
            'Reconciled candidate26 only; 116 other census records and 14 task families preserved, census56/57.',
            'Integrated source-critical pipeline, matching, metric, interaction, stability and intervention discussion on physical pages884-887.',
            'Preserved all866 prior citation identities and contexts; added genuine paper and exact reference, totals868/216.',
            'Published paired1181-page reader and37-page sponsor with210 audited records and exact-reader Q2-Q4.',
            'Continued commercial transport/missingness acquisition; preserved HTTP404, timeouts and incomplete PDF bodies without admitting partial text.'],
        evidence=[ref(WORK/n,'Reviewed ACE continuation') for n in ['source-audit.json','primary-review.json',
            'release-source-review.json','working-release.json','census-register.json','task-map.json','integrated-progress.json',
            'checkpoint-control-repair.json']],
        remaining=ref(BASE/'remaining-operations.json','Every nonpassing obligation'),
        next_operation=view['next'],next_action=view['next_action'],
        independent_continuation=ref(ROOT/'docs/program/execution/2026-10-21/transport-commercial-v1/plan.md','Next commercial survey plan'),
        visual_acceptance=False,proposal_accepted=False,global_blocker=None,background_worker_running=False))
    current=ROOT/'docs/program/execution/current-program.md'
    (BASE/'prior-current-program.md').write_bytes(current.read_bytes())
    current.write_text(f'''# Current executable proposal program

Updated21October2026 after grf reuse and ACE extraction reviews. This is a research
and product proposal. Prototype qualification, independent acceptance, bank
validation and adoption remain separate outcomes.

Use python3 tools/run_program_reviews_v2.py status, next and check. The canonical
ledger is [state.json](../state.json), governed by the
[proposal scope](../master-program-proposal.md). Historical plans and evidence
remain preserved. Checkpoints record continuation and are not permission gates.

## Current integrated documents

Read the [{state['reader']['pages']:,}-page monograph](../../causal_proposal_ace_reviewed_2026-10-21.pdf)
and its [{sponsor['pages']}-page sponsor proposal](../../sponsor_proposal_ace_reviewed_2026-10-21.pdf).
The reader has868 audited citation records and216 genuine scholarly PDFs.
The sponsor has210 audited citations and is paired to the exact reader bytes.
Q2-Q4 pass. Q1/Q5, all three mandatory repair rollups, rendered review and final
proposal acceptance remain open. Length is not acceptance.

There are **{view['recorded_proposal_operations']} recorded outcomes of {view['proposal_operations']} proposal operations**,
with **{view['ready_proposal_operations']} ready**. Inconclusive outcomes retain unmet obligations.

| Area | Pass | Inconclusive | Open | Total |
|---|---:|---:|---:|---:|
| Software coverage | {groups['software'].get('pass',0)} | {groups['software'].get('inconclusive',0)} | {groups['software']['open']} | 102 |
| Reuse decisions | {groups['reuse'].get('pass',0)} | {groups['reuse'].get('inconclusive',0)} | {groups['reuse']['open']} | 115 |
| Chapter reviews | {groups['chapters'].get('pass',0)} | {groups['chapters'].get('inconclusive',0)} | {groups['chapters']['open']} | 22 |

The frontier census is **56 inspected and57 unread out of113 originals**, plus
four crosscutting obligations. Fourteen task reviews and twelve integration
requirements have scoped proposal outcomes, not executable adoption.

## Integrated findings

ACE occupies physical PDF pages884-887. Its genuine July2026 paper reports three
bowtie extraction pipelines using retrieval, OCR or vision followed by another
model. Three tabular component references and dynamic-seal narratives support a
bounded extraction comparison. Narrative accuracy ratings1.2-3.0, missing roles,
implicit expert additions and hallucinated barriers remain explicit. Article
attribution rights do not qualify code, model, handbook or dependency reuse.

Printed response categories21/10/49 and9/11/60 each sum80; hallucinations decrease
15points while unclear outputs increase one. A12/32 JSON failure rate uses a
separate denominator. Exact authored examples show that a zero first-order context
index can coexist with total-order index one; edge F1 of198/199 can lose the entire
critical path; and the same unsigned graph with opposite mechanisms gives assumed
margins-12 and8. These examples do not reproduce ACE's models or identify its actual
sensitivity interactions. Ten repeated identical outputs do not identify quantization
as their cause or establish scientific truth.

All866 prior citation identities/contexts and266 compiled content inputs survive.
One genuine primary paper and one authored exact reference add two records. Source,
arithmetic, preservation and all-page text bounds pass. A checkpoint submission while
the controller was idle was rejected and repaired by starting the operation; the
failure and exact correction are preserved. No live model or upstream engine ran.

The grf reference disposition remains integrated on physical pages287-290 with one
R/native lineage. Correct marginal-outcome and conditional-effect inputs can still
produce score expectation1.5 versus2 with wrong propensity in the stipulated law.
All-customer effect4 and overlap effect4/17 give different-population assumed margins2
and-30/17 at cost2. Prior C++ and CausalityCheck findings remain preserved.

The [previous master](2026-10-21/program-refresh-ace-v1/prior-current-program.md)
retains earlier results and exact limitations. Commitf0a3bde4 preserves the completed
grf review and has been pushed. The current continuation adds ACE and commercial
source acquisition without claiming final proposal acceptance.

## Required standard and remaining gaps

Every banking use connects its information clock to assumptions, identification or
a justified limit, estimation, uncertainty, diagnostics, alternatives and monetary
consequences. Distinguish inherited results, project derivations, hypothetical
examples and verified implementation. Every source needs identity, version/date,
original local bytes, SHA-256, inspected anchors and supported claims. Scholarly
works need genuine PDFs. Literature cutoff:7October2026. FinMarketing sets the
scholarship standard, not a page-count acceptance rule.

MR01 requires17areas across six dimensions and100-150substantive software pages.
MR02 requires eight developed chapters,14tasks and approximately100pages
(depth contract96-112). MR03 requires four integration chapters and12requirements,
with indicative depth40-60pages. Coverage, connected argument and exclusive depth
must all pass; duplication earns no additional credit.

Known routes include authentic source inspection, method-specific comparisons,
reasoned reuse decisions, complementary searches, exact counterexamples and public
prototype designs. General hidden-confounder identification, arbitrary dependence,
private-state policy inference and universal calibration remain research questions.
Authentic bank truth, platform acceptance and measured economics are later conditional
gates and do not block independent proposal work.

## Exact continuation

Controller next: **{view['next']}**. {view['next_action']}

Follow the [commercial transport/missingness plan](2026-10-21/transport-commercial-v1/plan.md).
The inherited coverage row has no reviewed candidates; a registered unfetched query
is not an absence finding. Build explicit Stata/SAS/SPSS and additional-commercial
candidate records. Inspect missingness assumptions, imputation and analysis compatibility,
pooling, selection support and target-population transport separately. Preserve failed
search tooling,404responses,timeouts and partial PDFs. Retrying official sources is a
local acquisition step, not a global program blocker. Do not treat incomplete files as
authentic complete manuals or infer that imputation supplies transport identification.

Continue57 unread originals, complementary searches and citation chaining. Recover
ACE exact prompts/model/code/raw evaluation and rights before native reuse. Recover
CausalityCheck raw paired judgments before runtime claims. Candidate45's SSRN403
blocker remains local. Continue eligible branches across phase boundaries.

[Every nonpassing obligation](2026-10-21/program-refresh-ace-v1/remaining-operations.json)
and [continuation checkpoint](2026-10-21/program-refresh-ace-v1/continuation-checkpoint.json).

Use short commands, redirected logs and bounded text output. No unattended worker is
running. The inherited image allowance is exhausted under /home/ubuntu/AGENTS.md;
rendered acceptance needs a fresh visual session. Source/manuscript work remains eligible.
''')
    run.render(ROOT,state)
    print(json.dumps(dict(recorded=view['recorded_proposal_operations'],ready=view['ready_proposal_operations'],
        reader=state['reader'],sponsor_pages=sponsor['pages'],next=view['next'])))


if __name__=='__main__':
    main()
