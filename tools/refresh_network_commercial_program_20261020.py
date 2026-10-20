#!/usr/bin/env python3
"""Refresh the executable master view from actual receipts and current deliveries."""
from collections import Counter
import json
from pathlib import Path
import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run=extension.base
ROOT=run.core.ROOT
WORK=ROOT/'docs/program/execution/2026-10-20/network-commercial-v1'
SPONSOR=ROOT/'docs/program/execution/2026-10-20/sponsor-network-commercial-v1'
BASE=ROOT/'docs/program/execution/2026-10-20/program-refresh-network-commercial-v1'
read=lambda p:json.loads(p.read_text())


def main():
    assert not BASE.exists()
    state=run.core.read(ROOT,run.core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path']=='docs/causal_proposal_network_commercial_reviewed_2026-10-20.pdf'
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
        census=ref(ROOT/'docs/program/execution/2026-10-20/census-expert-averaging-v1/census-register.json',
                   '53 inspected and 60 unread originals'),proposal_accepted=False))
    check=read(WORK/'release-source-review.json')['checks']
    audit=read(WORK/'reader/source-audit.json');trace=read(WORK/'traceability-review.json')
    write(BASE/'continuation-checkpoint.json',dict(date='2026-10-20',status='continued_and_integrated',
        prior_git_commit='1d046622',state=ref(BASE/'state-snapshot.json','Canonical snapshot'),reader=state['reader'],
        sponsor=ref(SPONSOR/'working-release.json','Exact paired sponsor'),
        completed=['Authenticated20 gCastle blobs and completed selected-method reference disposition.',
            'Integrated gCastle typed graph, support, numerical and public prototype contracts.',
            'Inspected9 commercial network official originals and recorded coverage and comparison outcomes as inconclusive.',
            'Integrated4 supported vendor profiles,4 unresolved candidate families and exact network/assignment/temporal witnesses.',
            'Preserved failed sequencing, obsolete chapter marker and URL-overflow attempts with repairs.',
            'Published paired reader and sponsor and renewed exact-reader Q2-Q4.'],
        evidence=[ref(WORK/n,'Reviewed continuation evidence') for n in ['source-audit.json','review.json',
            'comparison-review.json','release-source-review.json','working-release.json']],
        remaining=ref(BASE/'remaining-operations.json','Every nonpassing obligation'),
        next_operation=view['next'],next_action=view['next_action'],
        prepared_next=ref(ROOT/'docs/program/execution/2026-10-20/java-effects-v1/plan.md','Reviewed Java effects continuation'),
        visual_acceptance=False,proposal_accepted=False,global_blocker=None,background_worker_running=False))
    current=ROOT/'docs/program/execution/current-program.md'
    (BASE/'prior-current-program.md').write_bytes(current.read_bytes())
    current.write_text(f'''# Current executable proposal program

Updated 20 October 2026 after gCastle reuse and commercial network/interference
comparisons. This is research and a product proposal. Prototype qualification,
independent acceptance, bank validation and adoption are separate outcomes.

Use `python3 tools/run_program_reviews_v2.py status`, `next` and `check`.
The canonical ledger is [state.json](../state.json), governed by the
[proposal scope](../master-program-proposal.md). Bound historical plans and
evidence remain preserved. A checkpoint records continuation; it is not a stop gate.

## Current integrated documents

Read the [{state['reader']['pages']:,}-page integrated monograph](../../causal_proposal_network_commercial_reviewed_2026-10-20.pdf)
and its [{sponsor['pages']}-page sponsor proposal](../../sponsor_proposal_network_commercial_reviewed_2026-10-20.pdf).
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

The frontier census remains **53 inspected and 60 unread out of113 originals**,
plus four separate crosscutting obligations. L1/L6 completeness, complementary
searches and citation chaining remain open. Fourteen task reviews and twelve
integration requirements have scoped proposal outcomes; these do not establish
runtime adoption.

## Substantive progress

gCastle now has a bounded reference choice for selected PC and linear NOTEARS,
with 20 authenticated source blobs and explicit root-tree identity. Its integrated
contract preserves graph type, variable labels, CI support, prior restrictions,
solver diagnostics, threshold and topology. Exact examples distinguish unresolved
edges from cycles and numerical tolerance from a DAG certificate. An original
Python worker is the proposed public experiment; native admission is deferred.

The new commercial discussion occupies physical PDF pages {check['physical_pages'][0]}-{check['physical_pages'][1]}.
All {check['preserved_records']} predecessor citation identities/contexts and
{check['unchanged_compiled_inputs']} compiled content inputs survive. Nine official
originals support Stata, SAS/ETS, ArcGIS Pro 3.5 and Statsig legacy profiles. Exact
editions, complete market search, rights, prices and four further candidate
families remain unresolved. Both coverage and comparison outcomes are inconclusive.

The argument distinguishes full-feedback spatial derivatives, simple impacts,
exposure contrasts and switchback policies. Exact two-branch responses give
own 40/3, spillover 20/3, total 20. At assumed cost 12, coefficient/own/portfolio margins
are -2, 4/3, 8. Missing a tie changes portfolio margin to -2. Full delta variance 28
differs from 20 after dropping covariance. Assignment enumeration shows unsupported
exposure cells; time and carryover witnesses give observed 102 versus effect 2 and
observed -2 versus immediate 2 / sustained 6. These are authored references, not native
or bank findings.

The SAS initial route timed out and one historical PDF was incomplete; a complete
official manual was recovered elsewhere. The Optimizely route returned a general
homepage. Neither result supports product absence. Failed publication sequencing,
an obsolete chapter insertion marker and an overflowing bibliography URL were
preserved and repaired. Both PDFs are source/text checked; rendered acceptance
remains pending the session image limit.

Earlier fixed-effect, Python effects, measurement-validity and expert-guided
discovery work remains integrated. The
[previous master view](2026-10-20/program-refresh-network-commercial-v1/prior-current-program.md)
preserves those detailed findings and their remaining limits.

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

The [Java effects plan](2026-10-20/java-effects-v1/plan.md) treats the inherited
empty combined query as a search limitation. Inspect H2O-3 uplift forests and
Tetrad IDA/CStaR at authenticated revisions; an uplift ranking metric or graph
slope set cannot stand in for a calibrated causal-effect interval. Initial public
discovery/identity acquisition is prepared; substantive review is outstanding.

The independent LL.CENSUS continuation remains candidate 42 and the saved
[53/60 register](2026-10-20/census-expert-averaging-v1/census-register.json).
Continue every eligible branch across phase boundaries; record a local blocker
and its acquisition/research trigger without stopping unrelated work.

[Every nonpassing obligation](2026-10-20/program-refresh-network-commercial-v1/remaining-operations.json)
· [Continuation checkpoint](2026-10-20/program-refresh-network-commercial-v1/continuation-checkpoint.json)

Use short commands, redirected logs and bounded text output. No unattended worker
is running. The inherited image allowance is exhausted under `/home/ubuntu/AGENTS.md`;
source, manuscript and public-design work remain eligible.
''')
    run.render(ROOT,state)
    print(json.dumps(dict(reader=state['reader'],sponsor_pages=sponsor['pages'],
        recorded=view['recorded_proposal_operations'],ready=view['ready_proposal_operations'],next=view['next'])))


if __name__=='__main__':main()
