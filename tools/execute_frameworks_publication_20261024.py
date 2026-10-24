#!/usr/bin/env python3
"""Publish already reviewed Framework work; each subprocess exit is consumed."""
import argparse,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-24/framework-census-v1'
def step(name,cmd):
    log=BASE/(name+'.log');assert not log.exists(),str(log)
    with log.open('w') as out:r=subprocess.run(cmd,cwd=ROOT,stdout=out,stderr=subprocess.STDOUT)
    event=dict(step=name,command=cmd,exit_code=r.returncode,log=str(log.relative_to(ROOT)))
    with (BASE/'publication-sequence.jsonl').open('a') as out:out.write(json.dumps(event)+'\n')
    print(json.dumps(event),flush=True)
    if r.returncode:raise SystemExit(r.returncode)
def publish():
    state=json.loads((ROOT/'docs/program/state.json').read_text())
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path']=='docs/causal_proposal_sas_reuse_reviewed_2026-10-24.pdf'
    assert (ROOT/'docs/program/execution/2026-10-24/sas-reuse-v1/publication-checkpoint.json').exists()
    from publish_latent_r_review_v2_20261013 import transition
    for role,operation in [('langchain','SW.DECISION.seed_097'),('autogen','SW.DECISION.seed_098'),('semantic_kernel','SW.DECISION.seed_099'),('dspy','SW.DECISION.seed_100'),('llama_index','SW.DECISION.seed_101'),('haystack','SW.DECISION.seed_102')]:
        step(role+'-start',['python3','tools/run_program_checkpoint_v3.py','start',operation,'--reason','Reviewed distinct Framework command-specific reference choice;official scope and exact witnesses;no native admission.'])
        step(role+'-receipt',['python3','tools/review_framework_census_20261024.py',role])
        transition('record',operation,BASE/(role+'-operation-receipt.json'))
    step('reader-publish',['python3','tools/publish_frameworks_reuse_reader_v2_20261024.py','publish'])
    step('sponsor-prepare',['python3','tools/build_frameworks_reuse_sponsor_20261024.py','prepare'])
    step('sponsor-build',['python3','tools/build_frameworks_reuse_sponsor_20261024.py','build'])
    step('renew',['python3','tools/publish_frameworks_reuse_reader_v2_20261024.py','renew'])
    step('sponsor-review',['python3','tools/publish_frameworks_reuse_sponsor_20261024.py','review'])
    step('sponsor-publish',['python3','tools/publish_frameworks_reuse_sponsor_20261024.py','publish'])
    step('program-refresh',['python3','tools/refresh_frameworks_reuse_program_20261024.py'])
    step('program-check',['python3','tools/run_program_checkpoint_v3.py','check'])
    step('legacy-check',['python3','tools/causal_program.py','check'])
    from publish_latent_r_review_v2_20261013 import ref,write
    remaining=json.loads((ROOT/'docs/program/execution/2026-10-24/program-refresh-frameworks-reuse-v1/remaining-operations.json').read_text())
    state=json.loads((ROOT/'docs/program/state.json').read_text())
    write(BASE/'publication-checkpoint.json',dict(status='published_checked',reader=state['reader'],sponsor=ref(ROOT/'docs/sponsor_proposal_frameworks_reuse_reviewed_2026-10-24.pdf','Exact paired sponsor'),recorded=remaining['recorded'],ready=remaining['ready'],nonpassing=len(remaining['operations']),checks=[ref(BASE/(n+'.log'),'Successful check') for n in ['program-check','legacy-check']],next_action='Commit/push completed Framework unit; advance exact hosted/local backend and remaining framework delegates,then frontier originals;do not close L6 or mandatory coverage prematurely.',visual_acceptance=False,final_acceptance=False,background_worker_running=False))
    print('Framework publication completed and checked.',flush=True)
if __name__=='__main__':publish()
