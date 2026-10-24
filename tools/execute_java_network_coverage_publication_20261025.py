#!/usr/bin/env python3
"""Publish reviewed JVM network coverage after consuming its predecessor delivery."""
import json
import subprocess
from pathlib import Path
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-25/java-network-coverage-v1'

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
    assert state['reader']['path']=='docs/causal_proposal_python_network_coverage_reviewed_v2_2026-10-25.pdf'
    verify_bindings(json.loads((BASE/'publication-plan-review.json').read_text()))
    from publish_latent_r_review_v2_20261013 import transition
    predecessor=json.loads((BASE.parent/'python-network-coverage-v1/push-verification.json').read_text())
    assert predecessor['status']=='pass'
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==predecessor['commit']
    assert subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT,text=True).strip()==predecessor['commit']
    operation='SW.CELL.networks_interference.Java'
    step('ivrd-start',['python3','tools/run_program_checkpoint_v3.py','start',operation,'--reason','Record selected JVM network source comparison; coverage remains inconclusive.'])
    step('ivrd-receipt',['python3','tools/review_java_network_coverage_20261025.py','receipt'])
    transition('record',operation,BASE/'operation-receipt.json')
    for name,stem,verb in [
        ('reader-publish','publish_java_network_coverage_reader','publish'),
        ('sponsor-prepare','build_java_network_coverage_sponsor','prepare'),
        ('sponsor-build','build_java_network_coverage_sponsor','build'),
        ('renew','publish_java_network_coverage_reader','renew'),
        ('sponsor-review','publish_java_network_coverage_sponsor','review'),
        ('sponsor-publish','publish_java_network_coverage_sponsor','publish')]:
        step(name,['python3','tools/'+stem+'_20261025.py',verb])
    step('program-refresh',['python3','tools/refresh_java_network_coverage_program_20261025.py'])
    for name,tool,verb in [
        ('program-status','run_program_checkpoint_v3','status'),
        ('legacy-status','causal_program','status'),
        ('program-check','run_program_checkpoint_v3','check'),
        ('legacy-check','causal_program','check')]:
        step(name,['python3','tools/'+tool+'.py',verb])
    state=json.loads((ROOT/'docs/program/state.json').read_text())
    remaining=json.loads((BASE.parent/'program-refresh-java-network-coverage-v1/remaining-operations.json').read_text())
    write(BASE/'publication-checkpoint.json',dict(status='published_checked',reader=state['reader'],
        sponsor=ref(ROOT/'docs/sponsor_proposal_java_network_coverage_reviewed_2026-10-25.pdf','Exact paired sponsor'),
        recorded=remaining['recorded'],ready=remaining['ready'],nonpassing=len(remaining['operations']),
        census_inspected=82,census_unread=31,crosscutting=4,new_notebook_authenticated=0,source_files_authenticated=52,source_retrievals_authenticated=52,
        checks=[ref(BASE/(name+'.log'),'Successful check') for name in ['program-check','legacy-check']],
        next_action='Commit and push the complete pair, then continue independent ready software and frontier obligations.',
        visual_acceptance=False,final_acceptance=False,background_worker_running=False))
    print('JVM network source publication and program checks complete.',flush=True)

if __name__=='__main__':main()
