#!/usr/bin/env python3
"""Refresh the executable master view from actual receipts and current deliveries."""
from collections import Counter
import json
from pathlib import Path
import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run=extension.base
ROOT=run.core.ROOT
WORK=ROOT/'docs/program/execution/2026-10-20/cxx-effects-v1/publication-v3'
SPONSOR=ROOT/'docs/program/execution/2026-10-21/sponsor-cxx-effects-v1'
BASE=ROOT/'docs/program/execution/2026-10-21/program-refresh-cxx-effects-v1'
read=lambda p:json.loads(p.read_text())


def main():
    assert not BASE.exists()
    state=run.core.read(ROOT,run.core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path']=='docs/causal_proposal_cxx_effects_reviewed_v3_2026-10-21.pdf'
    sponsor=read(SPONSOR/'working-release.json');verify_bindings(sponsor)
    assert run.same_reader(state['reader'],sponsor['paired_monograph'])
    view=run.status(ROOT,state);graph,merged,stages=run.combined(ROOT,state)
    assert {q['id']:q['status'] for q in view['proposal_gaps']}=={
        'Q1':'open','Q2':'pass','Q3':'pass','Q4':'pass','Q5':'open'}
    results=merged['execution_program']['results'];obligations=[];groups={}
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
    BASE.mkdir()
    write(BASE/'state-snapshot.json',state);write(BASE/'status-snapshot.json',view)
    write(BASE/'remaining-operations.json',dict(reader=state['reader'],coverage=groups,
        recorded=view['recorded_proposal_operations'],proposal_operations=view['proposal_operations'],
        ready=view['ready_proposal_operations'],operations=obligations,
        census=ref(ROOT/'docs/program/execution/2026-10-20/census-hypothesis-v1/census-register.json',
                   '54 inspected and 59 unread originals'),proposal_accepted=False))
    check=read(WORK/'release-source-review.json')['checks']
    audit=read(WORK/'reader/source-audit.json');trace=read(WORK/'traceability-review.json')
    write(BASE/'continuation-checkpoint.json',dict(date='2026-10-21',status='continued_and_integrated',
        prior_git_commit='f4e5e627',state=ref(BASE/'state-snapshot.json','Canonical snapshot'),reader=state['reader'],
        sponsor=ref(SPONSOR/'working-release.json','Exact paired sponsor'),
        completed=['Preserved mediation release and recovered C++ sources in commit f4e5e627.',
            'Authenticated35 source blobs and technically inspected21 selected blobs across four native lineages.',
            'Inspected genuine BCF2019v4 including adverse historical coverage and non-double-robustness limitations.',
            'Recorded C++ coverage as inconclusive with explicit candidate,rights,caller and native-test obligations.',
            'Integrated exact slope,weight,draw,scale and shrinkage witnesses with preserved prior content.',
            'Preserved bibliography overflow and missing naming-field failures; corrected reader and sponsor are paired.'],
        evidence=[ref(WORK/n,'Reviewed continuation evidence') for n in ['source-audit.json','review.json',
            'release-source-review.json','working-release.json']],
        remaining=ref(BASE/'remaining-operations.json','Every nonpassing obligation'),
        next_operation=view['next'],next_action=view['next_action'],
        prepared_next=ref(ROOT/'docs/program/execution/2026-10-21/census-causalitycheck-v1/plan.md','Next unread original recovery'),
        visual_acceptance=False,proposal_accepted=False,global_blocker=None,background_worker_running=False))
    current=ROOT/'docs/program/execution/current-program.md'
    (BASE/'prior-current-program.md').write_bytes(current.read_bytes())
    current.write_text(f'''# Current executable proposal program

Updated 21 October 2026 after the native heterogeneous-effects comparison. This is research and a product proposal. Prototype qualification,
independent acceptance, bank validation and adoption are separate outcomes.

Use `python3 tools/run_program_reviews_v2.py status`, `next` and `check`.
The canonical ledger is [state.json](../state.json), governed by the
[proposal scope](../master-program-proposal.md). Bound historical plans and
evidence remain preserved. A checkpoint records continuation; it is not a stop gate.

## Current integrated documents

Read the [{state['reader']['pages']:,}-page integrated monograph](../../causal_proposal_cxx_effects_reviewed_v3_2026-10-21.pdf)
and its [{sponsor['pages']}-page sponsor proposal](../../sponsor_proposal_cxx_effects_reviewed_2026-10-21.pdf).
They are paired by exact hashes. The reader has {len(audit['sources'])} audited
citation records and {trace['scholarly_pdfs']} genuine scholarly PDFs.
Q2-Q4 pass for this reader. Q1/Q5, all three mandatory repair rollups, rendered
review and final proposal acceptance remain open. Length is not acceptance.

There are **{view['recorded_proposal_operations']} recorded outcomes of {view['proposal_operations']} proposal operations**,
with **{view['ready_proposal_operations']} ready**. An inconclusive outcome preserves
its unmet obligations and is not counted as substantive closure.

| Area | Pass | Inconclusive | Open | Total |
|---|---:|---:|---:|---:|
| Software coverage | {groups['software'].get('pass',0)} | {groups['software'].get('inconclusive',0)} | {groups['software']['open']} | 102 |
| Reuse decisions | {groups['reuse'].get('pass',0)} | {groups['reuse'].get('inconclusive',0)} | {groups['reuse']['open']} | 115 |
| Chapter reviews | {groups['chapters'].get('pass',0)} | {groups['chapters'].get('inconclusive',0)} | {groups['chapters']['open']} | 22 |

The frontier census remains **54 inspected and 59 unread out of113 originals**,
plus four separate crosscutting obligations. L1/L6 completeness, complementary
searches and citation chaining remain open. Fourteen task reviews and twelve
integration requirements have scoped proposal outcomes; these do not establish
runtime adoption.

## Substantive progress

The native heterogeneous-effects comparison occupies physical PDF pages
{check['physical_pages'][0]}-{check['physical_pages'][1]}. All {check['preserved_records']}
earlier citation identities and contexts and {check['unchanged_compiled_inputs']}
compiled content inputs survive. Four pinned software reviews, one genuine BCF
preprint and one exact project reference add six citations.

grf's continuous slope is distinguished from finite dose contrasts and BCF
posterior draws. bcf likelihood precision is not a target-population weight.
XBCF scale restoration and static wrapper hazards, and flexBCF distinct priors,
cohort selection and training-row conventions, lead to specific prototype tests.
No native library or live model was executed and no route was admitted.

Exact witnesses distinguish slope0 from contrast1, population effect2 from
precision-reweighted5.2, and properly restored mean22.5 from15. Assumed costs
reverse margins-1/2.20 and2.50/-5. Common posterior draws preserve portfolio
uncertainty. A positive-overlap shrinkage example has true effect0 but apparent
coefficient1. These are authored examples, not measured software defects.

The genuine BCF2019v4 paper reports82% coverage at nominal95% in its historical
ACIC comparison; this is retained as an adverse result, not reproduced or
promoted into a ranking of current implementations. The broader C++ census,
additional method originals, rights, public callers and native qualification
remain open, so the coverage outcome is inconclusive.

The sponsor preserves190 prior citations and adds8, for198. Bibliography
URL overflow and a missing explicit paper filename-title field were preserved
and repaired in immutable successors. Both PDFs pass source/text checks;
rendered visual and final acceptance remain open.

The [previous master view](2026-10-21/program-refresh-cxx-effects-v1/prior-current-program.md)
preserves the mediation and earlier findings.

## Required standard and remaining routes

Every banking use must connect its information clock to causal assumptions,
identification or a justified limit, estimation, uncertainty, diagnostics,
alternatives and monetary consequences. Separate inherited results, project
derivations, generated examples and verified implementation. Every source needs
identity, version/date, local bytes, SHA-256, inspected anchors and supported
claims; scholarly works require genuine PDFs. Literature cutoff: 7 October 2026.
FinMarketing supplies the scholarship standard, not a page-count acceptance rule.

MR01 requires 17 areas across six dimensions and 100-150 substantive software pages.
MR02 requires eight developed chapters, 14 tasks and approximately 100 pages
(depth contract 96-112). MR03 requires four integration chapters and 12 requirements,
with indicative depth 40-60 pages. Coverage, connected argument and exclusive depth
must all pass; repeated material earns no duplicate credit.

Known next steps include source acquisition, candidate-specific comparison,
reasoned reuse decisions, literature searches, exact counterexamples and public
prototype designs. General hidden-confounder identification, arbitrary dependence,
private-state policy inference and universal calibration remain research
uncertainties. Authentic bank truth, platform acceptance and measured economics
are later conditional gates; they do not block independent proposal work.

## Exact continuation

Next operation: **{view['next']}**. {view['next_action']}

The [candidate109 recovery plan](2026-10-21/census-causalitycheck-v1/plan.md)
continues the original-source census. Recover CausalityCheck's matched original,
verify title/version/cutoff and inspect causal levels,benchmark labels,provenance
and adverse results. Metadata and unavailable routes never count as technical
inspection. Candidate45's SSRN403 blocker remains preserved; other unread
originals and complementary searches remain independently eligible.
Continue every eligible branch across phase boundaries; record a local blocker
and its acquisition/research trigger without stopping unrelated work.

[Every nonpassing obligation](2026-10-21/program-refresh-cxx-effects-v1/remaining-operations.json)
· [Continuation checkpoint](2026-10-21/program-refresh-cxx-effects-v1/continuation-checkpoint.json)

Use short commands, redirected logs and bounded text output. No unattended worker
is running. The inherited image allowance is exhausted under `/home/ubuntu/AGENTS.md`;
source, manuscript and public-design work remain eligible.
''')
    run.render(ROOT,state)
    print(json.dumps(dict(reader=state['reader'],sponsor_pages=sponsor['pages'],
        recorded=view['recorded_proposal_operations'],ready=view['ready_proposal_operations'],next=view['next'])))


if __name__=='__main__':main()
