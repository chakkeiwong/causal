#!/usr/bin/env python3
"""Record exact aliases, update the sponsor and reconcile the unchanged reader."""
import json
import subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-24/dose-alias-reconciliation-v1'


def step(name,command):
    log=BASE/(name+'.log');assert not log.exists(),log
    with log.open('x') as output:
        result=subprocess.run(command,cwd=ROOT,stdout=output,stderr=subprocess.STDOUT)
    event=dict(step=name,command=command,exit_code=result.returncode,log=str(log.relative_to(ROOT)))
    with (BASE/'publication-sequence.jsonl').open('a') as output:output.write(json.dumps(event)+'\n')
    print(json.dumps(event),flush=True)
    if result.returncode:raise SystemExit(result.returncode)


def main():
    from publish_latent_r_review_v2_20261013 import ref,write,transition
    state=json.loads((ROOT/'docs/program/state.json').read_text())
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path']=='docs/causal_proposal_judge_bias_reviewed_2026-10-24.pdf'
    assert (BASE.parent/'census-judge-bias-v1/publication-checkpoint.json').is_file()
    initial_reader=dict(state['reader'])
    for role in ['causaldrf','causalgps']:
        op='SW.DECISION.v13_'+role
        step(role+'-start',['python3','tools/run_program_checkpoint_v3.py','start',op,
             '--reason','Resolve exact catalogue alias using individually reviewed pinned component,rights,target,uncertainty,cost and conversion evidence;no new capability.'])
        step(role+'-receipt',['python3','tools/reconcile_dose_aliases_20261024.py',role])
        transition('record',op,BASE/(role+'-operation-receipt.json'))
    step('sponsor-prepare',['python3','tools/build_dose_alias_sponsor_20261024.py','prepare'])
    step('sponsor-build',['python3','tools/build_dose_alias_sponsor_20261024.py','build'])
    step('sponsor-review',['python3','tools/publish_dose_alias_sponsor_20261024.py','review'])
    step('sponsor-publish',['python3','tools/publish_dose_alias_sponsor_20261024.py','publish'])
    step('program-refresh',['python3','tools/refresh_dose_alias_program_20261024.py'])
    step('program-status',['python3','tools/run_program_checkpoint_v3.py','status'])
    step('program-check',['python3','tools/run_program_checkpoint_v3.py','check'])
    step('legacy-status',['python3','tools/causal_program.py','status'])
    step('legacy-check',['python3','tools/causal_program.py','check'])
    state=json.loads((ROOT/'docs/program/state.json').read_text());assert state['reader']==initial_reader
    remaining=json.loads((BASE.parent/'program-refresh-dose-alias-v1/remaining-operations.json').read_text())
    write(BASE/'publication-checkpoint.json',dict(status='published_checked',reader=state['reader'],
        sponsor=ref(ROOT/'docs/sponsor_proposal_dose_alias_reviewed_2026-10-24.pdf','Exact paired sponsor'),
        recorded=remaining['recorded'],ready=remaining['ready'],nonpassing=len(remaining['operations']),
        monograph_unchanged=True,incremental_native_capabilities=0,
        checks=[ref(BASE/(n+'.log'),'Successful full-byte check') for n in ['program-check','legacy-check']],
        next_action='Commit/push the reviewed alias reconciliation;continue independent remaining reuse,software and frontier original obligations.',
        visual_acceptance=False,final_acceptance=False,background_worker_running=False))
    print('Alias reconciliation published and checked;monograph unchanged.',flush=True)


if __name__=='__main__':main()
