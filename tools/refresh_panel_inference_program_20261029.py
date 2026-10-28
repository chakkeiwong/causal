"""Refresh mutable master and reader-bound handoff, preserving all historical gates."""
import copy
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write

ROOT=Path(__file__).resolve().parents[1]
DAY=ROOT/'docs/program/execution/2026-10-29'
PRIOR_DAY=ROOT/'docs/program/execution/2026-10-28'
BASE=DAY/'program-refresh-panel-inference-v1'
read=lambda p:json.loads(p.read_text())


def main():
    assert not BASE.exists()
    run=controller.base;state=run.core.read(ROOT,run.core.STATE)
    assert state['execution_runtime']['active'] is None
    graph,merged,stages,ready,_=run.queue(ROOT,state)
    results=merged['execution_program']['results']
    reader=read(DAY/'panel-inference-reader-v1/working-release.json')
    sponsor=read(DAY/'sponsor-panel-inference-v1/working-release.json')
    for item in [reader,sponsor]:verify_bindings(item)
    assert run.same_reader(state['reader'],reader['pdf']) and run.same_reader(state['reader'],sponsor['paired_monograph'])
    nodes=[n for n in graph['nodes'] if stages[n['id']]=='proposal_now']
    unresolved={n['id'] for n in nodes if results.get(n['id'],{}).get('outcome')!='pass'}
    prior=PRIOR_DAY/'program-refresh-panel-estimators-v1/remaining-operations.json'
    remaining=copy.deepcopy(read(prior))
    assert len(nodes)==376 and len(unresolved)==150
    assert unresolved=={r['id'] for r in remaining['operations']}
    assert Counter(results.get(k,{}).get('outcome','open') for k in unresolved)==dict(inconclusive=121,open=25,negative=4)
    for row in remaining['operations']:
        if row['id'] in ('TEXT.REVIEW.L1','TEXT.REVIEW.L6'):
            binding=results[row['id']];row.update(action=read(ROOT/binding['path'])['revisit_trigger'],evidence=binding,action_basis=binding)
        if row['id']=='SW.CELL.panels_did.R':
            row.update(later_source_delta=ref(DAY/'panel-inference-contracts-v1/review.json','Selected constructor, tests and numerical delegates'),
                       corrected_continuation='Retain previous panel originals and all completed pinned reviews. New wave inspected 12 schema/delegate files and 3 DESCRIPTION metadata files; one BMisc R file remains acquired-only. Next pin R stats covariance/QR paths, Rcpp RNG law, upstream influence normalization and dplyr/tibble attribute behavior. Resolve exact upstream object editions, original-paper omissions, full dependency locks and rights before native qualification.')
    protected=[ROOT/'docs/program/master-program.md',ROOT/'docs/program/master-current.md']
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
    BASE.mkdir()
    for rel,name in [('docs/program/master-live.md','prior-master-live.md'),('docs/program/execution/current-program.md','prior-current-program.md'),('docs/mission-control.md','prior-mission-control.md')]:
        (BASE/name).write_bytes((ROOT/rel).read_bytes())
    remaining.update(reader=state['reader'],ready=len(ready),predecessor=ref(prior,'All prior unresolved statuses'))
    write(BASE/'remaining-operations.json',remaining);write(BASE/'state-snapshot.json',state)
    evidence=[ref(DAY/p,'Verified current publication') for p in ['panel-inference-reader-v1/working-release.json','sponsor-panel-inference-v1/working-release.json','panel-inference-contracts-v1/review.json','panel-inference-contracts-v1/remaining-obligations.json']]
    evidence += [ref(PRIOR_DAY/'panel-estimator-delivery-v1/push-verification.json','Verified parent commit'),ref(BASE/'remaining-operations.json','All 150unresolved obligations'),ref(Path(__file__),'Refresh logic')]
    write(BASE/'program-review.json',dict(status='pass_for_consistency_not_completion',recorded=351,proposal_operations=376,nonpassing=150,software_reuse_rows=105,evidence=evidence,protected_historical_hashes=hashes,visual_acceptance=False,final_acceptance=False))
    summary=f'''The current monograph has {reader['pages']:,} pages, 1,451 audited citation
records and 277 genuine scholarly PDFs. The paired sponsor has {sponsor['pages']}
pages and 1,126 records. All 1,449 reader and 1,122 sponsor predecessor records,
reader citation contexts and compiled content inputs remain. Q2-Q4 exact-reader
author checks pass; Q1/Q5, full coverage/depth, visual and final acceptance remain open.

351/376 original operations are recorded. All 150 nonpassing obligations remain:
121 inconclusive,25 open and four negative. Software is 3 passing,98 inconclusive
and 1 open; reuse is 109 passing,4 inconclusive and 2 open. The frontier census remains
82 inspected and 31 unread. These source additions award no canonical acceptance.

The verified predecessor commit is 760468e0ef5a9445fb3b7f48dd0a41b7c6033c2c.
The complete inventory retains 105 unresolved software/reuse rows. Four have bounded
later deltas; 101 still need semantic reconciliation. Two historical reference hash
mismatches remain explicit alongside the passing current replay.

The new addition reviews 12 selected constructor/test/delegate files and 3 package
metadata files. One acquired BMisc R file remains technically uninspected.
Exact reference results distinguish 9/8 from 5/2 variance under stated independent
signs, show equal-cluster-size agreement, and expose partial-interval replacement
and fractional-clock mismatch. Source review does not establish native calibration.
'''
    continuation='''Use python3 tools/run_followup_program_v3_20261028.py status, next and check.
Use v2 for registered start/checkpoint/record events. Finite packet completion
hands off to the remaining inventory; phase boundaries are not stopping points.

Next pin R stats covariance/QR methods and Rcpp sampling semantics; inspect the
full influence-weighting path and dplyr/tibble mixed-confidence metadata behavior.
Declare full-rank, aliased, pivot, unequal-cluster and failure fixtures. Dependency
versions selected by cutoff are candidates, not an installed lockfile. Exact
DCDH/fect/PanelMatch objects, later fastdid proof and pampe/Synth/trend originals,
transitive rights and bounded native trials remain local continuations.

Other software/reuse rows and 31 unread frontier originals remain independently
eligible. Unknown counterfactual truth and unrestricted dependence require extra
information or justified restrictions; no universal repair is promised. Bank and
independent acceptance are later external gates. The six-image allowance is
exhausted; fresh visual review remains open. No unattended research worker runs.
'''
    old=(BASE/'prior-current-program.md').read_text()
    gaps=old[old.index('## Remaining gaps and routes'):old.index('## Execution and recovery')]
    mon=Path(reader['pdf']['path']).name;sp=Path(sponsor['pdf']['path']).name
    (ROOT/'docs/program/execution/current-program.md').write_text(f'''# Current executable proposal program

Updated 29 October 2026. [Live master](../master-live.md),
[program review](2026-10-29/{BASE.name}/program-review.json),
[all unresolved obligations](2026-10-29/{BASE.name}/remaining-operations.json).

This is a scholarly product proposal. Software/reuse, LLM/agent and CLI/MCP
coverage remain mandatory. Public evidence justifies later costly experiments.

## Current integrated documents

[Monograph](../../{mon}) and [paired sponsor](../../{sp}).

{summary}
{gaps}## Execution and recovery

Frozen historical masters, source evidence and failures retain their bytes.

## Exact continuation

{continuation}''')
    (ROOT/'docs/program/master-live.md').write_text(f'''# Current master program: causal banking proposal

Updated 29 October 2026. [Executable program](execution/current-program.md).
[All unresolved obligations](execution/2026-10-29/{BASE.name}/remaining-operations.json).

The standard is a connected banking argument from information clocks through
assumptions, identification, estimation, uncertainty, diagnostics, alternatives
and monetary consequences. Genuine scholarly PDFs and exact primary identities,
hashes and inspected anchors support claims. Reproducible examples and rendered
inspection are required. FinMarketing is an exposition standard, not a length target.
Software, LLM/agent and CLI/MCP coverage remain mandatory.

[Current monograph](../{mon}) and [paired sponsor](../{sp}).

{summary}
{continuation}''')
    controller.render(ROOT,state)
    mission=ROOT/'docs/mission-control.md';text=mission.read_text()
    start,end=text.index('Current entrypoint:'),text.index('Public design outcomes:')
    text=text[:start]+'[Current master program](program/master-live.md).\n\nCurrent work: python3 tools/run_followup_program_v3_20261028.py status, next, check.\n\n**351/376 recorded;150 nonpassing.** Complete inventory retains 105 unresolved software/reuse rows.\n\n'+text[end:]
    text+=f'\n[Current paired sponsor]({sp}) — {sponsor["pages"]} pages.\n';mission.write_text(text)
    html=subprocess.run(['pandoc','--from=gfm','--to=html'],input=text,text=True,capture_output=True,check=True,timeout=20).stdout
    (ROOT/'docs/mission-control.html').write_text('<!doctype html><meta charset="utf-8"><title>Causal proposal execution</title>'+html)
    assert hashes=={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
    pointer=ROOT/'docs/program/execution/continuation-current.json';prior_pointer=read(pointer)
    handoff_base=DAY/'continuation-handoff-v3';assert not handoff_base.exists();handoff_base.mkdir()
    (handoff_base/'prior-pointer.json').write_bytes(pointer.read_bytes())
    handoff=copy.deepcopy(read(ROOT/prior_pointer['manifest']['path']))
    handoff.update(reader=state['reader'],operations=remaining['operations'],evidence=[ref(BASE/'remaining-operations.json','Current statuses'),ref(handoff_base/'prior-pointer.json','Prior handoff'),ref(BASE/'program-review.json','Reviewed refresh')])
    for row in handoff['operations']:
        if row.get('corrected_action_checkpoint'):row['resolved_action']=read(ROOT/row['corrected_action_checkpoint']['path'])['next_action']
    write(handoff_base/'manifest.json',handoff)
    write(handoff_base/'author-review.json',dict(status='pass_for_reader_refresh',evidence=[ref(handoff_base/'manifest.json','All 150obligations'),ref(PRIOR_DAY/'continuation-handoff-v1/author-review.json','Original behavior review')],awards_acceptance=False))
    pointer.write_text(json.dumps(dict(manifest=ref(handoff_base/'manifest.json','Current inventory'),review=ref(handoff_base/'author-review.json','Reviewed refresh')),indent=2)+'\n')
    from run_followup_program_v3_20261028 import current
    assert current()['unresolved_obligations']==150
    write(BASE/'continuation-checkpoint.json',dict(reader=state['reader'],sponsor=sponsor['pdf'],evidence=evidence,next_action='Consume unchanged checks, deliver preserving publication, and continue dependency/reconciliation work.',visual_acceptance=False,final_acceptance=False))
    print(json.dumps(dict(recorded=351,nonpassing=150,reader_pages=reader['pages'],sponsor_pages=sponsor['pages'],protected_master_bytes_unchanged=True)))


if __name__=='__main__':main()
