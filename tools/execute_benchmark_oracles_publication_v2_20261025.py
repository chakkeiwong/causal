#!/usr/bin/env python3
"""Publish one reviewed survey delta after verified predecessor delivery."""
import json,subprocess
from pathlib import Path
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-25/benchmark-oracles-v1'

def step(name,command):
    log=BASE/(name+'.log');assert not log.exists(),log
    with log.open('x') as output:
        result=subprocess.run(command,cwd=ROOT,stdout=output,stderr=subprocess.STDOUT)
    event=dict(step=name,exit_code=result.returncode,log=str(log.relative_to(ROOT)))
    with (BASE/'publication-sequence.jsonl').open('a') as output:output.write(json.dumps(event)+chr(10))
    print(json.dumps(event),flush=True)
    if result.returncode:raise SystemExit(result.returncode)

def main():
    state=json.loads((ROOT/'docs/program/state.json').read_text())
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path']=='docs/causal_proposal_agent_evaluation_surveys_reviewed_v2_2026-10-25.pdf'
    verify_bindings(json.loads((BASE/'publication-plan-review-v2.json').read_text()))
    predecessor=json.loads((BASE.parent/'agent-evaluation-surveys-v1/push-verification.json').read_text())
    consumed=json.loads((BASE/'predecessor-delivery-consumed.json').read_text())
    assert predecessor['status']=='pass' and consumed['exit_code']==0 and consumed['commit']==predecessor['commit']
    for revision in ['HEAD','origin/main']:
        assert subprocess.check_output(['git','rev-parse',revision],cwd=ROOT,text=True).strip()==predecessor['commit']
    for name,stem,verb in [
        ('reader-publish','publish_benchmark_oracles_reader','publish'),
        ('census-progress','reconcile_benchmark_oracles',None),
        ('sponsor-prepare','build_benchmark_oracles_sponsor','prepare'),
        ('sponsor-build','build_benchmark_oracles_sponsor','build'),
        ('renew','publish_benchmark_oracles_reader','renew'),
        ('sponsor-review','publish_benchmark_oracles_sponsor','review'),
        ('sponsor-publish','publish_benchmark_oracles_sponsor','publish'),
        ('program-refresh','refresh_benchmark_oracles_program',None)]:
        command=['python3','tools/run_with_review_context_cache_20261025.py','tools/'+stem+'_20261025.py']
        if verb:command.append(verb)
        step(name,command)
    for name,tool,verb in [('program-status','run_program_checkpoint_v3','status'),('legacy-status','causal_program','status'),('program-check','run_program_checkpoint_v3','check'),('legacy-check','causal_program','check')]:
        step(name,['python3','tools/'+tool+'.py',verb])
    state=json.loads((ROOT/'docs/program/state.json').read_text())
    remaining=json.loads((BASE.parent/'program-refresh-benchmark-oracles-v1/remaining-operations.json').read_text())
    write(BASE/'publication-checkpoint.json',dict(status='published_checked',reader=state['reader'],sponsor=ref(ROOT/'docs/sponsor_proposal_benchmark_oracles_reviewed_2026-10-25.pdf','Exact paired sponsor'),recorded=remaining['recorded'],ready=remaining['ready'],nonpassing=len(remaining['operations']),census_inspected=82,census_unread=31,crosscutting=4,independent_oracle_contracts=4,new_original_dispositions=0,checks=[ref(BASE/(n+'.log'),'Successful full unmodified controller check') for n in ['program-check','legacy-check']],next_action='Commit and push, consume delivery, then continue independent runtime-rights and source obligations.',visual_acceptance=False,final_acceptance=False,background_worker_running=False))
    print('Independent benchmark oracle publication and full program checks complete.',flush=True)

if __name__=='__main__':main()
