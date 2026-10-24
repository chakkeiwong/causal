#!/usr/bin/env python3
"""Publish the reviewed frontier addition without closing the full census."""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'docs/program/execution/2026-10-24/census-judge-bias-v1'


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
    assert state['reader']['path'] == 'docs/causal_proposal_mcp_reuse_reviewed_2026-10-24.pdf'
    assert (BASE.parent/'mcp-reuse-v1/publication-checkpoint.json').is_file()
    from publish_latent_r_review_v2_20261013 import transition, ref, write
    step('reader-publish',['python3','tools/publish_judge_bias_reader_20261024.py','publish'])
    step('sponsor-prepare',['python3','tools/build_judge_bias_sponsor_20261024.py','prepare'])
    step('sponsor-build',['python3','tools/build_judge_bias_sponsor_20261024.py','build'])
    step('renew',['python3','tools/publish_judge_bias_reader_20261024.py','renew'])
    step('sponsor-review',['python3','tools/publish_judge_bias_sponsor_20261024.py','review'])
    step('sponsor-publish',['python3','tools/publish_judge_bias_sponsor_20261024.py','publish'])
    write(BASE/'integrated-progress.json',dict(
        finding='Candidate225 selected arXivv3 original is integrated in the preserving reader and exact paired sponsor; 81 inspected,32 unread and4crosscutting. Final conference bytes remain a separate omission.',
        next_action='Continue32 unread originals and4crosscutting with authentic permitted sources; retain local access/date and final-version omissions. Judge-bias reader/sponsor are already paired: do not repeat their build or publication. Advance independent backend,commercial and software obligations.',
        yield_reason='Completed scoped original and integration; full census stays open while independent work continues.',
        evidence=[ref(BASE/'review.json','Primary original review'),ref(BASE/'census-register.json','81/32census'),
                  ref(BASE.parent/'judge-bias-reader-v1/working-release.json','Completed integrated reader'),
                  ref(BASE.parent/'sponsor-judge-bias-v1/working-release.json','Exact paired sponsor')]))
    step('census-start', ['python3','tools/run_program_checkpoint_v3.py','start','LL.CENSUS',
         '--reason','Record completed candidate225 integration without closing the full census or forgetting final-edition omissions.'])
    transition('yield','LL.CENSUS',BASE/'integrated-progress.json')
    step('program-refresh',['python3','tools/refresh_judge_bias_program_20261024.py'])
    step('program-check',['python3','tools/run_program_checkpoint_v3.py','check'])
    step('legacy-check',['python3','tools/causal_program.py','check'])
    state=json.loads((ROOT/'docs/program/state.json').read_text())
    remaining=json.loads((BASE.parent/'program-refresh-judge-bias-v1/remaining-operations.json').read_text())
    write(BASE/'publication-checkpoint.json',dict(
        status='published_checked',reader=state['reader'],
        sponsor=ref(ROOT/'docs/sponsor_proposal_judge_bias_reviewed_2026-10-24.pdf','Exact paired sponsor'),
        recorded=remaining['recorded'],ready=remaining['ready'],nonpassing=len(remaining['operations']),
        census_inspected=81,census_unread=32,crosscutting=4,
        checks=[ref(BASE/(name+'.log'),'Successful check') for name in ['program-check','legacy-check']],
        next_action='Commit and push the complete pair; continue unread originals and independent backend,commercial and software obligations. Final conference bytes remain a local omission.',
        visual_acceptance=False,final_acceptance=False,background_worker_running=False))
    print('Judge-bias publication completed and checked.',flush=True)


if __name__ == '__main__':
    main()
