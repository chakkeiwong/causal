#!/usr/bin/env python3
"""Serially publish two graph-interface/runtime reference decisions in one wave and reconcile the program."""
import json
import subprocess
from pathlib import Path
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-25/graph-reuse-wave-v1'

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
    verify_bindings(json.loads((BASE/'sponsor-check-repair-review.json').read_text()))
    from publish_graph_reuse_wave_20261025 import controller
    view=controller.status(ROOT,state)
    assert {q['id']:q['status'] for q in view['proposal_gaps']}==dict(Q1='open',Q2='pass',Q3='pass',Q4='pass',Q5='open')
    for name,stem,verb in [
        ('sponsor-review-v2','publish_graph_reuse_wave_sponsor_v2','review'),
        ('sponsor-publish','publish_graph_reuse_wave_sponsor_v2','publish')]:
        step(name,['python3','tools/'+stem+'_20261025.py',verb])
    step('program-refresh',['python3','tools/refresh_graph_reuse_wave_program_20261025.py'])
    for name,tool,verb in [
        ('program-status','run_program_checkpoint_v3','status'),
        ('legacy-status','causal_program','status'),
        ('program-check','run_program_checkpoint_v3','check'),
        ('legacy-check','causal_program','check')]:
        step(name,['python3','tools/'+tool+'.py',verb])
    state=json.loads((ROOT/'docs/program/state.json').read_text())
    remaining=json.loads((BASE.parent/'program-refresh-graph-reuse-wave-v1/remaining-operations.json').read_text())
    write(BASE/'publication-checkpoint.json',dict(status='published_checked',reader=state['reader'],
        sponsor=ref(ROOT/'docs/sponsor_proposal_graph_reuse_wave_reviewed_2026-10-25.pdf','Exact paired sponsor'),
        recorded=remaining['recorded'],ready=remaining['ready'],nonpassing=len(remaining['operations']),
        census_inspected=82,census_unread=31,crosscutting=4,new_notebook_authenticated=0,source_files_authenticated=35,
        checks=[ref(BASE/(name+'.log'),'Successful check') for name in ['program-check','legacy-check']],
        next_action='Commit and push the complete pair, then continue independent ready software and frontier obligations.',
        visual_acceptance=False,final_acceptance=False,background_worker_running=False))
    print('Grouped graph/runtime reference publication and program checks complete.',flush=True)

if __name__=='__main__':main()
