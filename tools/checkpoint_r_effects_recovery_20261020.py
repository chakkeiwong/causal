#!/usr/bin/env python3
"""Refresh the master after crash recovery and R effects continuation."""
from collections import Counter
import json
from pathlib import Path
import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run=extension.base
ROOT=run.core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-19/recovery-r-effects-v1'
WORK=ROOT/'docs/program/execution/2026-10-19/r-effects-v1'
SPONSOR=ROOT/'docs/program/execution/2026-10-19/sponsor-r-effects-v1'
CENSUS=ROOT/'docs/program/execution/2026-10-19/census-hidden-reasoning-v1/census-register.json'
read=lambda p:json.loads(p.read_text())


def main():
    assert not BASE.exists()
    state=run.core.read(ROOT,run.core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path']=='docs/causal_proposal_r_effects_reviewed_2026-10-20.pdf'
    view=run.status(ROOT,state);graph,merged,stages=run.combined(ROOT,state)
    sponsor=read(SPONSOR/'working-release.json');verify_bindings(sponsor)
    assert run.same_reader(state['reader'],sponsor['paired_monograph'])
    assert {r['id']:r['status'] for r in view['proposal_gaps']}=={
        'Q1':'open','Q2':'pass','Q3':'pass','Q4':'pass','Q5':'open'}
    results=merged['execution_program']['results'];operations=[];groups={}
    for node in graph['nodes']:
        key=node['id'];result=results.get(key)
        if stages[key]!='proposal_now' or result and result['outcome']=='pass':continue
        progress=merged['execution_program']['progress'].get(key,[])
        action=read(ROOT/progress[-1]['path'])['next_action'] if progress else node['action']
        operations.append(dict(id=key,lane=node['lane'],status=result['outcome'] if result else 'open',
            title=node['title'],action=action,prerequisites=run.ledger.blockers(merged,node),
            outputs=node['outputs'],evidence=result,requires_inputs=node['requires_inputs']))
    for name,prefix,total in [('software','SW.CELL.',102),('reuse','SW.DECISION.',115),('chapters','TEXT.REVIEW.',22)]:
        selected={k:v for k,v in results.items() if k.startswith(prefix)}
        groups[name]=dict(Counter(v['outcome'] for v in selected.values()),open=total-len(selected),total=total)
    BASE.mkdir()
    write(BASE/'state-snapshot.json',state);write(BASE/'status-snapshot.json',view)
    write(BASE/'remaining-operations.json',dict(reader=state['reader'],coverage=groups,
        recorded=view['recorded_proposal_operations'],proposal_operations=view['proposal_operations'],
        ready=view['ready_proposal_operations'],operations=operations,
        census=ref(CENSUS,'49 inspected and64unread original candidates'),proposal_accepted=False))
    write(BASE/'recovery-checkpoint.json',dict(status='recovered_and_continued',date='2026-10-20',
        state=ref(BASE/'state-snapshot.json','Canonical state at checkpoint'),reader=state['reader'],
        sponsor=ref(SPONSOR/'working-release.json','Exact paired sponsor'),
        recovery_commit_verified_on_origin='e81ff8a8c5d8f32a451473328f5c4f796477c039',
        completed=['Recovered and published the commercial dynamic-panel reader and paired sponsor.',
            'Preserved Feast, dynamic-panel and all preceding originals and reviews.',
            'Authenticated19R-source blobs; recorded a bounded effects/heterogeneity comparison.',
            'Resolved the selected tmle missing-A guard while retaining documentation and runtime limits.',
            'Integrated exact target, missing-label and dose-unit arguments; preserved814prior citations and251compiled inputs.',
            'Preserved a timed-out TeX attempt; a nonrecursive root search built the unchanged manuscript.',
            'Renewed exact-reader Q2-Q4 and paired a preserving sponsor successor.'],
        evidence=[ref(WORK/n,'Recovered R continuation evidence') for n in
            ['source-audit.json','review.json','mathematical-review.json','working-release.json',
             'release-source-review.json','build-recovery.json','reader-attempt-01/failure.txt']],
        remaining=ref(BASE/'remaining-operations.json','Every nonpassing proposal obligation'),
        next_action=view['next']+': '+view['next_action'],global_blocker=None,
        visual_acceptance=False,proposal_accepted=False,background_worker_running=False))
    current=ROOT/'docs/program/execution/current-program.md'
    (BASE/'prior-current-program.md').write_bytes(current.read_bytes())
    audit=read(WORK/'reader/source-audit.json');papers=read(WORK/'traceability-review.json')['scholarly_pdfs']
    text=f'''# Current executable proposal program

Updated 20 October 2026 after crash recovery, publication of the commercial
dynamic-panel comparison, and continuation through the R effects comparison.
This is a research and product proposal. Prototype qualification, independent
review, bank validation and adoption remain distinct outcomes.

Use `python3 tools/run_program_reviews_v2.py status`, `next` and `check`.
The canonical ledger is [state.json](../state.json), governed by the
[proposal scope](../master-program-proposal.md). Historical numbered programs
and their bound evidence are preserved. Checkpoints are restart records.

## Current deliverables

The [{state['reader']['pages']:,}-page working monograph](../../causal_proposal_r_effects_reviewed_2026-10-20.pdf)
and [{sponsor['pages']}-page sponsor proposal](../../sponsor_proposal_r_effects_reviewed_2026-10-20.pdf)
are paired by exact hashes. The reader has {len(audit['sources'])} audited citation records
and {papers} genuine scholarly PDFs. Q2-Q4 pass for these exact reader bytes.
Q1/Q5, all three mandatory repair rollups, rendered review and final acceptance
remain open. Passing integrity and author reviews do not close those gates.

There are **{view['recorded_proposal_operations']} recorded outcomes of {view['proposal_operations']} proposal operations**,
with **{view['ready_proposal_operations']} ready**. An inconclusive result retains its unmet obligations.

| Area | Pass | Inconclusive | Open | Total |
|---|---:|---:|---:|---:|
| Software coverage | {groups['software'].get('pass',0)} | {groups['software'].get('inconclusive',0)} | {groups['software']['open']} | 102 |
| Reuse decisions | {groups['reuse'].get('pass',0)} | {groups['reuse'].get('inconclusive',0)} | {groups['reuse']['open']} | 115 |
| Chapter reviews | {groups['chapters'].get('pass',0)} | {groups['chapters'].get('inconclusive',0)} | {groups['chapters']['open']} | 22 |

The original frontier census remains49inspected and64unread of113. L1/L6
frontier and framework completeness remains open. Fourteen task reviews and
twelve integration requirements have bounded proposal outcomes, not runtime adoption.

## What recovery and continuation changed

The recovered Feast and commercial dynamic-panel publications were committed
and verified on origin/main as e81ff8a8c5d8f32a451473328f5c4f796477c039.
Feast's selected creation-time filter does not establish actual availability,
and its historical, online and state-changing MCP paths retain distinct contracts.
The commercial comparison preserves instrument validity, covariance choices,
shock targets and calendar dependence; its eight-family coverage stays partial.

The R comparison authenticates nineteen source blobs across tmle, R DoubleML,
CausalGPS and causaldrf, with inherited grf originals retained. It resolves one
specific ambiguity: the selected tmle path rejects missing treatment labels;
NULL/all-zero input chooses a mean-outcome path. This is source evidence, with
native fixtures and clarification still outstanding. R DoubleML cluster splitting
and variance do not imply supported clustered multiplier bootstrap.

The new argument distinguishes mean conditional slopes from a pooled
variance-weighted slope and finite-dose contrasts. Exact authored laws give
2 versus13/5for two slope targets and USD15versus USD35for a stipulated credit
contrast and its slope proxy. GPS density scales, counterfactual-dose scores,
zero weights and pointwise/bootstrap uncertainty receive explicit contracts.
No R engine was executed. BART/causalweight alternatives, broader aliases,
complete rights and native conformance remain open. The addition is at physical
PDF pages251-255; earlier citations, contexts and chapter inputs are preserved.

A first TeX pass timed out. Its logs and partial output remain intact; retrying
the unchanged manuscript with nonrecursive root search succeeded. This repair
does not establish rendered visual acceptance.

## Required standard and remaining routes

Connect each banking decision and information clock to assumptions,
identification or limits, estimation, uncertainty, diagnostics, alternatives
and monetary consequences. Distinguish inherited results, authored derivations,
generated examples and verified implementation. Every citation needs identity,
version/date, local bytes, SHA-256, inspected anchors and supported claims;
scholarly citations need genuine PDFs. The literature cutoff is7October2026.
FinMarketing supplies the scholarship standard; page count is not acceptance.

MR01 requires17areas across six dimensions and100-150substantive software pages.
MR02 requires eight developed chapters, fourteen tasks and approximately100pages
(the depth contract is96-112). MR03 requires four integration chapters and twelve
requirements, with indicative depth40-60pages. Coverage, argument and exclusive
depth must all pass; repeated material earns no duplicate credit.

Known public-evidence routes remain for missing originals, commercial comparisons,
justified reuse choices, frontier census, reader reconciliation and proposed public
prototype experiments. General hidden-confounder identification, arbitrary
dependence, private-state policy inference and universal calibration remain
research uncertainties. Authentic bank truth, platform trials, institutional
acceptance and observed economics are later conditional gates. They do not block
proposal work that can be supported by public or generated evidence.

## Exact continuation

Next: **{view['next']}**. {view['next_action']}

Use the latest census successor rather than restarting already inspected originals.
Acquire and inspect one original at a time, preserve identity/version and failure
evidence, map its claims to the relevant tasks, and integrate only warranted claims.
Continue independent ready software, literature and integration items when an
individual original is unavailable. No phase or checkpoint is a permission gate.

[Every nonpassing obligation](2026-10-19/recovery-r-effects-v1/remaining-operations.json)
· [Recovery checkpoint](2026-10-19/recovery-r-effects-v1/recovery-checkpoint.json)
· [Preserved prior program](2026-10-19/recovery-r-effects-v1/prior-current-program.md)

Use short commands and bounded text output. No unattended worker is running.
The inherited image allowance is exhausted under `/home/ubuntu/AGENTS.md`;
rendered review remains pending and does not block source or manuscript work.
'''
    for old,new in {'remains49inspected and64unread of113':'remains 49 inspected and 64 unread of 113',
        'versus13/5for':'versus 13/5 for','USD15versus USD35for':'USD 15 versus USD 35 for',
        'pages251-255':'pages 251-255','is7October2026':'is 7 October 2026',
        'requires17areas':'requires 17 areas','and100-150substantive':'and 100-150 substantive',
        'approximately100pages':'approximately 100 pages','is96-112':'is 96-112',
        'depth40-60pages':'depth 40-60 pages'}.items():text=text.replace(old,new)
    current.write_text(text);run.render(ROOT,state)
    print(json.dumps(dict(recorded=view['recorded_proposal_operations'],ready=view['ready_proposal_operations'],
        next=view['next'],reader_pages=state['reader']['pages'],sponsor_pages=sponsor['pages'])))


if __name__=='__main__':
    main()
