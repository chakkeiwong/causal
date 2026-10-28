"""Serialize one reviewed publication and both unchanged full integrity checks."""
import json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-28/delegate-contract-review-v1'


def step(name,command):
    log=BASE/(name+'.log');assert not log.exists(),log
    with log.open('x') as out:r=subprocess.run(command,cwd=ROOT,stdout=out,stderr=subprocess.STDOUT)
    event=dict(step=name,exit_code=r.returncode,log=str(log.relative_to(ROOT)))
    with (BASE/'publication-sequence.jsonl').open('a') as out:out.write(json.dumps(event)+chr(10))
    print(json.dumps(event),flush=True)
    if r.returncode:raise SystemExit(r.returncode)


def main():
    prior=json.loads((BASE.parent/'openai-contract-review-v1/delivery-consumed.json').read_text())
    assert prior['actual_exit_code']==0
    for rev in ['HEAD','origin/main']:assert subprocess.check_output(['git','rev-parse',rev],cwd=ROOT,text=True).strip()==prior['commit']
    assert json.loads((BASE/'reader-build-consumed.json').read_text())['actual_exit_code']==0
    for name,script,verb in [
      ('reader-publish','publish_delegate_contract_reader_20261028','publish'),
      ('sponsor-prepare','build_delegate_contract_sponsor_20261028','prepare'),
      ('sponsor-build','build_delegate_contract_sponsor_20261028','build'),
      ('renew','publish_delegate_contract_reader_20261028','renew'),
      ('sponsor-review','publish_delegate_contract_sponsor_20261028','review'),
      ('sponsor-publish','publish_delegate_contract_sponsor_20261028','publish'),
      ('chapter-review','review_delegate_program_20261028',None),
      ('program-refresh','refresh_delegate_program_20261028',None)]:
        cmd=['python3','tools/run_with_review_context_cache_20261025.py','tools/'+script+'.py']
        if verb:cmd.append(verb)
        step(name,cmd)
    for name,script in [('program-check','run_program_checkpoint_v3'),('legacy-check','causal_program')]:step(name,['python3','tools/'+script+'.py','check'])
    state=json.loads((ROOT/'docs/program/state.json').read_text())
    (BASE/'publication-checkpoint.json').write_text(json.dumps(dict(status='published_checked',reader=state['reader'],sponsor='docs/sponsor_proposal_delegate_contract_reviewed_2026-10-28.pdf',recorded=351,nonpassing=150,visual_acceptance=False,final_acceptance=False),indent=2)+chr(10))
    print('Publication and unchanged full checks completed.',flush=True)


if __name__=='__main__':main()
