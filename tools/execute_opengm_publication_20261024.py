#!/usr/bin/env python3
"""Publish already reviewed OpenGM work; each subprocess exit is consumed."""
import argparse,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-24/opengm-reuse-v1'
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
    assert state['reader']['path']=='docs/causal_proposal_agrum_reuse_reviewed_2026-10-24.pdf'
    assert (ROOT/'docs/program/execution/2026-10-24/agrum-reuse-v1/publication-checkpoint.json').exists()
    step('start',['python3','tools/run_program_checkpoint_v3.py','start','SW.DECISION.seed_083','--reason','Reviewed historical OpenGM source,paper,exact semantic witnesses and preserving reader ready.'])
    step('receipt',['python3','tools/decide_opengm_reuse_20261024.py','receipt'])
    from publish_latent_r_review_v2_20261013 import transition
    transition('record','SW.DECISION.seed_083',BASE/'operation-receipt.json')
    step('reader-publish',['python3','tools/publish_opengm_reuse_reader_20261024.py','publish'])
    step('sponsor-prepare',['python3','tools/build_opengm_reuse_sponsor_20261024.py','prepare'])
    step('sponsor-build',['python3','tools/build_opengm_reuse_sponsor_20261024.py','build'])
    step('renew',['python3','tools/publish_opengm_reuse_reader_20261024.py','renew'])
    step('sponsor-review',['python3','tools/publish_opengm_reuse_sponsor_20261024.py','review'])
    step('sponsor-publish',['python3','tools/publish_opengm_reuse_sponsor_20261024.py','publish'])
    step('program-refresh',['python3','tools/refresh_opengm_reuse_program_20261024.py'])
    step('program-check',['python3','tools/run_program_checkpoint_v3.py','check'])
    step('legacy-check',['python3','tools/causal_program.py','check'])
    from publish_latent_r_review_v2_20261013 import ref,write
    remaining=json.loads((ROOT/'docs/program/execution/2026-10-24/program-refresh-opengm-reuse-v1/remaining-operations.json').read_text())
    state=json.loads((ROOT/'docs/program/state.json').read_text())
    write(BASE/'publication-checkpoint.json',dict(status='published_checked',reader=state['reader'],sponsor=ref(ROOT/'docs/sponsor_proposal_opengm_reuse_reviewed_2026-10-24.pdf','Exact paired sponsor'),recorded=remaining['recorded'],ready=remaining['ready'],nonpassing=len(remaining['operations']),checks=[ref(BASE/(n+'.log'),'Successful check') for n in ['program-check','legacy-check']],next_action='Commit/push completed OpenGM unit; finish preserving SMILE/GeNIe reader and two distinct engine/offering reference decisions,then continue independent obligations.',next_review=ref(ROOT/'docs/program/execution/2026-10-24/smile-reuse-v1/review.json','Reviewed next comparison'),visual_acceptance=False,final_acceptance=False,background_worker_running=False))
    print('OpenGM publication completed and checked.',flush=True)
if __name__=='__main__':publish()
