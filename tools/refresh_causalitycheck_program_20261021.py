#!/usr/bin/env python3
"""Refresh the executable master view from actual receipts and current deliveries."""
from collections import Counter
import json
from pathlib import Path
import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run=extension.base
ROOT=run.core.ROOT
WORK=ROOT/'docs/program/execution/2026-10-21/census-causalitycheck-v1'
SPONSOR=ROOT/'docs/program/execution/2026-10-21/sponsor-causalitycheck-v1'
BASE=ROOT/'docs/program/execution/2026-10-21/program-refresh-causalitycheck-v1'
read=lambda p:json.loads(p.read_text())


def main():
    assert not BASE.exists()
    state=run.core.read(ROOT,run.core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path']=='docs/causal_proposal_causalitycheck_reviewed_2026-10-21.pdf'
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
        census=ref(ROOT/'docs/program/execution/2026-10-21/census-causalitycheck-v1/census-register.json',
                   '55 inspected and 58 unread originals'),proposal_accepted=False))
    check=read(WORK/'release-source-review.json')['checks']
    audit=read(WORK/'reader/source-audit.json');trace=read(WORK/'traceability-review.json')
    write(BASE/'continuation-checkpoint.json',dict(date='2026-10-21',status='continued_and_integrated',
        prior_git_commit='f4e5e627',state=ref(BASE/'state-snapshot.json','Canonical snapshot'),reader=state['reader'],
        sponsor=ref(SPONSOR/'working-release.json','Exact paired sponsor'),
        completed=['Recovered prior work and committed mediation/source evidence as f4e5e627.',
            'Completed bounded native heterogeneous-effects review and integrated1172-page reader/36-page sponsor.',
            'Recovered and inspected genuine27-page CausalityCheck original,retaining annotation,selection and score-difference limits.',
            'Reconciled candidate109 only;116 other entries and14 tasks preserved; census55/58.',
            'Integrated exact paired-error and selection-economics witnesses; all862 prior citation identities/contexts survive.',
            'Published paired reader/sponsor and renewed exact-reader Q2-Q4; no final acceptance.'],
        evidence=[ref(WORK/n,'Reviewed continuation evidence') for n in ['source-audit.json','review.json',
            'release-source-review.json','working-release.json','census-register.json','task-map.json']],
        remaining=ref(BASE/'remaining-operations.json','Every nonpassing obligation'),
        next_operation=view['next'],next_action=view['next_action'],
        prepared_next=ref(ROOT/'docs/program/execution/2026-10-21/census-ace-v1/plan.md','Next unread original recovery'),
        visual_acceptance=False,proposal_accepted=False,global_blocker=None,background_worker_running=False))
    current=ROOT/'docs/program/execution/current-program.md'
    (BASE/'prior-current-program.md').write_bytes(current.read_bytes())
    current.write_text(f'''# Current executable proposal program

Updated 21 October 2026 after native heterogeneous-effects and CausalityCheck reviews. This is research and a product proposal. Prototype qualification,
independent acceptance, bank validation and adoption are separate outcomes.

Use `python3 tools/run_program_reviews_v2.py status`, `next` and `check`.
The canonical ledger is [state.json](../state.json), governed by the
[proposal scope](../master-program-proposal.md). Bound historical plans and
evidence remain preserved. A checkpoint records continuation; it is not a stop gate.

## Current integrated documents

Read the [{state['reader']['pages']:,}-page integrated monograph](../../causal_proposal_causalitycheck_reviewed_2026-10-21.pdf)
and its [{sponsor['pages']}-page sponsor proposal](../../sponsor_proposal_causalitycheck_reviewed_2026-10-21.pdf).
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

The frontier census remains **55 inspected and 58 unread out of113 originals**,
plus four separate crosscutting obligations. L1/L6 completeness, complementary
searches and citation chaining remain open. Fourteen task reviews and twelve
integration requirements have scoped proposal outcomes; these do not establish
runtime adoption.

## Substantive progress

The CausalityCheck discussion occupies physical PDF pages
{check['physical_pages'][0]}-{check['physical_pages'][1]}. All {check['preserved_records']}
earlier citation identities and contexts and {check['unchanged_compiled_inputs']}
compiled content inputs survive. A genuine ACL original and an authored exact
reference add two citation records and one scholarly PDF.

The paper proposes a four-by-four textual reasoning checklist. Reported data
flow1200 seeds/43200 generated/10800 selected/8920 retained is distinguished
from runtime reproduction. Printed task counts and1880 exclusions reconcile.
Annotation agreement varies,including AJ.72/.78 and CVA.59-.65. The paper's
limited structural/counterfactual scope remains explicit.

An accuracy difference is net discordance,not the rate of correct answers with
wrong chains. Under an explicitly paired population,the same82.27%/59.46%
marginals allow22.81%-40.54% discordance. A negative difference-5.12points
permits0%-23.2%. These are authored illustrations,not bounds on the actual
unmatched task outputs. Filtering50 of100 requests with45 correct gives90%
selected accuracy but full45%-95%; assumed10/-30/1 economics gives margins
-13..7 rather than the selected5.

The C++ comparison remains integrated at physical pages283-287. Its distinct
slope/contrast,precision/target weights,priors,draw alignment and static hazards
remain source-grounded proposal findings. BCF historical82% coverage at95%
nominal is retained without claiming a current native ranking or reproduction.

The sponsor preserves198 prior citations and adds4,for202. Both PDFs pass
source,exact arithmetic,preservation and extracted text-bounds checks.
Rendered visual acceptance,complete repair rollups,Q1/Q5 and independent
acceptance remain open. No live models or upstream code were executed.

The [previous master view](2026-10-21/program-refresh-causalitycheck-v1/prior-current-program.md)
preserves the C++ and earlier findings.

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

Candidate109 is technically inspected and integrated. Do not repeat its
acquisition or publication. Continue58 unread originals,starting candidate26
(ACE bowtie extraction) or another accessible original. Inspect authentic
methods and negative evidence,verify cutoff identity,and update the census
without granting runtime adoption. Candidate45's SSRN403 blocker remains local.

Recover CausalityCheck pinned code/data and raw paired judgments before any
runtime reuse. Its source-generation/filtering and model-policy alternatives
remain unresolved. Complete complementary longitudinal/off-policy and negative
searches,citation chaining and software candidate reviews independently.
Continue every eligible branch across phase boundaries; record a local blocker
and its acquisition/research trigger without stopping unrelated work.

[Every nonpassing obligation](2026-10-21/program-refresh-causalitycheck-v1/remaining-operations.json)
· [Continuation checkpoint](2026-10-21/program-refresh-causalitycheck-v1/continuation-checkpoint.json)

Use short commands, redirected logs and bounded text output. No unattended worker
is running. The inherited image allowance is exhausted under `/home/ubuntu/AGENTS.md`;
source, manuscript and public-design work remain eligible.
''')
    run.render(ROOT,state)
    print(json.dumps(dict(reader=state['reader'],sponsor_pages=sponsor['pages'],
        recorded=view['recorded_proposal_operations'],ready=view['ready_proposal_operations'],next=view['next'])))


if __name__=='__main__':main()
