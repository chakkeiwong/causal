#!/usr/bin/env python3
"""Finite reviewed publication sequence; consume every exit before mutation."""
import json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-24/agrum-reuse-v1'
steps=[
 ('sponsor-review',['python3','tools/publish_agrum_reuse_sponsor_20261024.py','review']),
 ('sponsor-publish',['python3','tools/publish_agrum_reuse_sponsor_20261024.py','publish']),
 ('program-refresh',['python3','tools/refresh_agrum_reuse_program_20261024.py']),
 ('program-check',['python3','tools/run_program_checkpoint_v3.py','check']),
 ('legacy-check',['python3','tools/causal_program.py','check']),
]
def main():
    state=json.loads((ROOT/'docs/program/state.json').read_text())
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path']=='docs/causal_proposal_agrum_reuse_reviewed_2026-10-24.pdf'
    for q in ['Q2','Q3','Q4']:
        result=state['execution_runtime']['results']['PROPOSAL.'+q]
        receipt=json.loads((ROOT/result['path']).read_text())
        assert receipt['outcome']=='pass' and receipt['reviewed_reader']['sha256']==state['reader']['sha256']
    progress=BASE/'publication-sequence.jsonl'
    assert not progress.exists(),'Sequence is single-run; inspect checkpoint before recovery.'
    for name,cmd in steps:
        log=BASE/(name+'.log');assert not log.exists(),str(log)
        with log.open('w') as output:
            result=subprocess.run(cmd,cwd=ROOT,stdout=output,stderr=subprocess.STDOUT)
        event=dict(step=name,command=cmd,exit_code=result.returncode,log=str(log.relative_to(ROOT)))
        with progress.open('a') as out:out.write(json.dumps(event)+'\n')
        print(json.dumps(event),flush=True)
        if result.returncode:raise SystemExit(result.returncode)
    from publish_latent_r_review_v2_20261013 import ref,write
    remaining=json.loads((ROOT/'docs/program/execution/2026-10-24/program-refresh-agrum-reuse-v1/remaining-operations.json').read_text())
    state=json.loads((ROOT/'docs/program/state.json').read_text())
    write(BASE/'publication-checkpoint.json',dict(status='published_checked',reader=state['reader'],sponsor=ref(ROOT/'docs/sponsor_proposal_agrum_reuse_reviewed_2026-10-24.pdf','Exact paired sponsor'),recorded=remaining['recorded'],ready=remaining['ready'],nonpassing=len(remaining['operations']),checks=[ref(BASE/(n+'.log'),'Successful exit and check') for n in ['program-check','legacy-check']],next_action='Commit/push completed aGrUM unit; start and record reviewed OpenGM SW.DECISION.seed_083, publish preserving reader, pair sponsor and continue shared SMILE/GeNIe decisions.',next_review=ref(ROOT/'docs/program/execution/2026-10-24/opengm-reuse-reader-v1/release-source-review.json','Reviewed next reader'),visual_acceptance=False,final_acceptance=False,background_worker_running=False))
    print('aGrUM publication complete and checked; no background research worker.',flush=True)
if __name__=='__main__':main()
