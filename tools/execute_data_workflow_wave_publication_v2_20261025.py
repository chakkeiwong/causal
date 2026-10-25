#!/usr/bin/env python3
"""Publish reviewed Observation-data and computation-workflow coverage after consuming its predecessor delivery."""
import json, contextlib, sys
import subprocess
from pathlib import Path
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-25/data-workflow-wave-v1'

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
    assert state['reader']['path']=='docs/causal_proposal_bayesian_state_wave_reviewed_v1_2026-10-25.pdf'
    verify_bindings(json.loads((BASE/'publication-plan-review-v2.json').read_text()))
    from publish_latent_r_review_v2_20261013 import transition
    predecessor=json.loads((BASE.parent/'bayesian-state-wave-v1/push-verification.json').read_text())
    assert predecessor['status']=='pass'
    assert json.loads((BASE/'predecessor-delivery-consumed.json').read_text())['exit_code']==0
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==predecessor['commit']
    assert subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT,text=True).strip()==predecessor['commit']
    import run_program_checkpoint_v3 as controller
    import review_data_workflow_wave_v2_20261025 as reviewer
    from run_with_verified_hash_cache_20261025 import VerifiedHashCache
    import build_integrated_monograph_v12 as shared
    run=controller.base;core=run.core;cache=VerifiedHashCache()
    original_core_sha,original_shared_sha=core.sha,shared.sha
    core.sha=cache.sha;shared.sha=cache.sha
    try:
        for family in ['observations_data','computation_workflow']:
            for language in ['R','Python','Java','Cxx','other_relevant']:
                operation='SW.CELL.'+family+'.'+language
                log=BASE/(family+'-'+language+'-validated-sequence-v2.log')
                assert not log.exists()
                with log.open('x') as output,contextlib.redirect_stdout(output),contextlib.redirect_stderr(output):
                    state=core.read(ROOT,core.STATE)
                    run.require(not (issues:=run.validate_state(ROOT,state)), '; '.join(issues))
                    before=core.sha(ROOT/core.STATE)
                    event=run.apply(ROOT,state,'start',operation,reason='Record reviewed source comparison;coverage and native admission remain inconclusive.')
                    run.commit(ROOT,before,state,event)
                    reviewer.receipt(family,language)
                    transition('record',operation,BASE/family/language/'operation-receipt.json')
                event=dict(step=operation,exit_code=0,log=str(log.relative_to(ROOT)),hash_verification=cache.summary())
                with (BASE/'publication-sequence.jsonl').open('a') as output:output.write(json.dumps(event)+chr(10))
                print(json.dumps(event),flush=True)
    finally:
        core.sha=original_core_sha;shared.sha=original_shared_sha
    write(BASE/'hash-reuse-observed.json',cache.summary())
    for name,stem,verb in [
        ('reader-publish','publish_data_workflow_wave_reader_v2','publish'),
        ('sponsor-prepare','build_data_workflow_wave_sponsor','prepare'),
        ('sponsor-build','build_data_workflow_wave_sponsor','build'),
        ('renew','publish_data_workflow_wave_reader_v2','renew'),
        ('sponsor-review','publish_data_workflow_wave_sponsor','review'),
        ('sponsor-publish','publish_data_workflow_wave_sponsor','publish')]:
        step(name,['python3','tools/'+stem+'_20261025.py',verb])
    step('program-refresh',['python3','tools/refresh_data_workflow_wave_program_20261025.py'])
    for name,tool,verb in [
        ('program-status','run_program_checkpoint_v3','status'),
        ('legacy-status','causal_program','status'),
        ('program-check','run_program_checkpoint_v3','check'),
        ('legacy-check','causal_program','check')]:
        step(name,['python3','tools/'+tool+'.py',verb])
    state=json.loads((ROOT/'docs/program/state.json').read_text())
    remaining=json.loads((BASE.parent/'program-refresh-data-workflow-wave-v1/remaining-operations.json').read_text())
    write(BASE/'publication-checkpoint.json',dict(status='published_checked',reader=state['reader'],
        sponsor=ref(ROOT/'docs/sponsor_proposal_data_workflow_wave_reviewed_2026-10-25.pdf','Exact paired sponsor'),
        recorded=remaining['recorded'],ready=remaining['ready'],nonpassing=len(remaining['operations']),
        census_inspected=82,census_unread=31,crosscutting=4,new_notebook_authenticated=0,source_files_authenticated=83,source_retrievals_authenticated=83,new_scholarly_originals=0,
        checks=[ref(BASE/(name+'.log'),'Successful check') for name in ['program-check','legacy-check']],
        next_action='Commit and push the complete pair, then continue independent ready software and frontier obligations.',
        visual_acceptance=False,final_acceptance=False,background_worker_running=False))
    print('Observation-data and computation-workflow source publication and program checks complete.',flush=True)

if __name__=='__main__':main()
