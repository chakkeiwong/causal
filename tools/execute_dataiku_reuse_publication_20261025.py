#!/usr/bin/env python3
"""Serially publish Dataiku reference choice and reconcile the program."""
import json
import subprocess
from pathlib import Path
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-25/dataiku-reuse-v1'

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
    assert state['reader']['path']=='docs/causal_proposal_agents_reuse_reviewed_2026-10-25.pdf'
    verify_bindings(json.loads((BASE/'publication-plan-review.json').read_text()))
    from publish_latent_r_review_v2_20261013 import transition
    operation='SW.DECISION.seed_095'
    step('dataiku-start',['python3','tools/run_program_checkpoint_v3.py','start',operation,'--reason','Record separate Dataiku client/server reference choice without native admission.'])
    step('dataiku-receipt',['python3','tools/decide_dataiku_reuse_20261025.py','receipt'])
    transition('record',operation,BASE/'operation-receipt.json')
    for name,stem,verb in [
        ('reader-publish','publish_dataiku_reuse_reader','publish'),
        ('sponsor-prepare','build_dataiku_reuse_sponsor','prepare'),
        ('sponsor-build','build_dataiku_reuse_sponsor','build'),
        ('renew','publish_dataiku_reuse_reader','renew'),
        ('sponsor-review','publish_dataiku_reuse_sponsor','review'),
        ('sponsor-publish','publish_dataiku_reuse_sponsor','publish')]:
        step(name,['python3','tools/'+stem+'_20261025.py',verb])
    step('program-refresh',['python3','tools/refresh_dataiku_reuse_program_20261025.py'])
    for name,tool,verb in [
        ('program-status','run_program_checkpoint_v3','status'),
        ('legacy-status','causal_program','status'),
        ('program-check','run_program_checkpoint_v3','check'),
        ('legacy-check','causal_program','check')]:
        step(name,['python3','tools/'+tool+'.py',verb])
    state=json.loads((ROOT/'docs/program/state.json').read_text())
    remaining=json.loads((BASE.parent/'program-refresh-dataiku-reuse-v1/remaining-operations.json').read_text())
    write(BASE/'publication-checkpoint.json',dict(status='published_checked',reader=state['reader'],
        sponsor=ref(ROOT/'docs/sponsor_proposal_dataiku_reuse_reviewed_2026-10-25.pdf','Exact paired sponsor'),
        recorded=remaining['recorded'],ready=remaining['ready'],nonpassing=len(remaining['operations']),
        census_inspected=82,census_unread=31,crosscutting=4,original_files_authenticated=5,
        checks=[ref(BASE/(name+'.log'),'Successful check') for name in ['program-check','legacy-check']],
        next_action='Commit and push the complete pair, then continue independent ready software and frontier obligations.',
        visual_acceptance=False,final_acceptance=False,background_worker_running=False))
    print('Dataiku reference publication and program checks complete.',flush=True)

if __name__=='__main__':main()
