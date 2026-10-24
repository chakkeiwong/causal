#!/usr/bin/env python3
"""Publish reviewed backend comparison without closing full L6 or native qualification."""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'docs/program/execution/2026-10-24/backend-census-v1'


def step(name, command):
    log = BASE/(name+'.log')
    assert not log.exists(), log
    with log.open('x') as output:
        result = subprocess.run(command, cwd=ROOT, stdout=output, stderr=subprocess.STDOUT)
    event = dict(step=name, command=command, exit_code=result.returncode,
                 log=str(log.relative_to(ROOT)))
    with (BASE/'publication-sequence.jsonl').open('a') as output:
        output.write(json.dumps(event)+'\n')
    print(json.dumps(event), flush=True)
    if result.returncode:
        raise SystemExit(result.returncode)


def main():
    state = json.loads((ROOT/'docs/program/state.json').read_text())
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path'] == 'docs/causal_proposal_judge_bias_reviewed_2026-10-24.pdf'
    assert (BASE.parent/'dose-alias-reconciliation-v1/publication-checkpoint.json').is_file()
    from publish_latent_r_review_v2_20261013 import transition, ref, write
    step('reader-publish',['python3','tools/publish_backend_census_reader_20261024.py','publish'])
    step('sponsor-prepare',['python3','tools/build_backend_census_sponsor_20261024.py','prepare'])
    step('sponsor-build',['python3','tools/build_backend_census_sponsor_20261024.py','build'])
    step('renew',['python3','tools/publish_backend_census_reader_20261024.py','renew'])
    step('sponsor-review',['python3','tools/publish_backend_census_sponsor_20261024.py','review'])
    step('sponsor-publish',['python3','tools/publish_backend_census_sponsor_20261024.py','publish'])
    step('program-refresh',['python3','tools/refresh_backend_census_program_20261024.py'])
    step('program-status',['python3','tools/run_program_checkpoint_v3.py','status'])
    step('legacy-status',['python3','tools/causal_program.py','status'])
    step('program-check',['python3','tools/run_program_checkpoint_v3.py','check'])
    step('legacy-check',['python3','tools/causal_program.py','check'])
    state=json.loads((ROOT/'docs/program/state.json').read_text())
    remaining=json.loads((BASE.parent/'program-refresh-backend-census-v1/remaining-operations.json').read_text())
    write(BASE/'publication-checkpoint.json',dict(
        status='published_checked',reader=state['reader'],
        sponsor=ref(ROOT/'docs/sponsor_proposal_backend_census_reviewed_2026-10-24.pdf','Exact paired sponsor'),
        recorded=remaining['recorded'],ready=remaining['ready'],nonpassing=len(remaining['operations']),
        census_inspected=81,census_unread=32,crosscutting=4,backend_profiles=5,backend_files_acquired=45,backend_files_inspected=32,
        checks=[ref(BASE/(name+'.log'),'Successful check') for name in ['program-check','legacy-check']],
        next_action='Commit and push the complete pair; continue unread originals, remaining reuse and software obligations. L6, provider/model coverage, final-edition originals and public native qualification remain open.',
        visual_acceptance=False,final_acceptance=False,background_worker_running=False))
    print('Backend census publication completed and checked.',flush=True)


if __name__ == '__main__':
    main()
