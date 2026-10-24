#!/usr/bin/env python3
"""Publish reviewed panel-language coverage and preserve two local source-access blockers."""
import json
import subprocess
from pathlib import Path
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-25/panels-other-v1'

def step(name, command):
    log=BASE/(name+'.log')
    assert not log.exists(),log
    with log.open('x') as output:
        result=subprocess.run(command,cwd=ROOT,stdout=output,stderr=subprocess.STDOUT)
    event=dict(step=name,exit_code=result.returncode,log=str(log.relative_to(ROOT)))
    with (BASE/'publication-sequence.jsonl').open('a') as out:
        out.write(json.dumps(event)+'\n')
    print(json.dumps(event),flush=True)
    if result.returncode:raise SystemExit(result.returncode)

def main():
    state=json.loads((ROOT/'docs/program/state.json').read_text())
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path']=='docs/causal_proposal_agena_reuse_reviewed_2026-10-25.pdf'
    verify_bindings(json.loads((BASE/'publication-plan-review.json').read_text()))
    from publish_latent_r_review_v2_20261013 import transition
    predecessor=json.loads((BASE.parent/'graph-reuse-wave-v1/push-verification.json').read_text())
    assert predecessor['status']=='pass'
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==predecessor['commit']
    assert subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT,text=True).strip()==predecessor['commit']
    for seed in ['088','092']:
        receipt=BASE.parent/'commercial-tail-v1'/('seed_'+seed+'-local-block.json')
        verify_bindings(json.loads(receipt.read_text()))
        transition('block','SW.DECISION.seed_'+seed,receipt)
    operation='SW.CELL.panels_did.other_relevant'
    step('panel-start',['python3','tools/run_program_checkpoint_v3.py','start',operation,'--reason','Record selected Julia/MATLAB panel source comparison;coverage remains inconclusive.'])
    step('panel-receipt',['python3','tools/review_panels_other_20261025.py','receipt'])
    transition('record',operation,BASE/'operation-receipt.json')
    for name,stem,verb in [
        ('reader-publish','publish_panels_other_reader','publish'),
        ('sponsor-prepare','build_panels_other_sponsor','prepare'),
        ('sponsor-build','build_panels_other_sponsor','build'),
        ('renew','publish_panels_other_reader','renew'),
        ('sponsor-review','publish_panels_other_sponsor','review'),
        ('sponsor-publish','publish_panels_other_sponsor','publish')]:
        step(name,['python3','tools/'+stem+'_20261025.py',verb])
    step('program-refresh',['python3','tools/refresh_panels_other_program_20261025.py'])
    for name,tool,verb in [
        ('program-status','run_program_checkpoint_v3','status'),
        ('legacy-status','causal_program','status'),
        ('program-check','run_program_checkpoint_v3','check'),
        ('legacy-check','causal_program','check')]:
        step(name,['python3','tools/'+tool+'.py',verb])
    state=json.loads((ROOT/'docs/program/state.json').read_text())
    remaining=json.loads((BASE.parent/'program-refresh-panels-other-v1/remaining-operations.json').read_text())
    write(BASE/'publication-checkpoint.json',dict(status='published_checked',reader=state['reader'],
        sponsor=ref(ROOT/'docs/sponsor_proposal_panels_other_reviewed_2026-10-25.pdf','Exact paired sponsor'),
        recorded=remaining['recorded'],ready=remaining['ready'],nonpassing=len(remaining['operations']),
        census_inspected=82,census_unread=31,crosscutting=4,new_notebook_authenticated=0,source_files_authenticated=40,
        checks=[ref(BASE/(name+'.log'),'Successful check') for name in ['program-check','legacy-check']],
        next_action='Commit and push the complete pair, then continue independent ready software and frontier obligations.',
        visual_acceptance=False,final_acceptance=False,background_worker_running=False))
    print('Panel-language source publication and program checks complete.',flush=True)

if __name__=='__main__':main()
