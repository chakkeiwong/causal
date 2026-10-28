"""Serial publication after verified recovery delivery; explicit logs and exits."""
import json,subprocess
from pathlib import Path
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-28/causal-modeling-lead-v1'
RECOVERY=BASE.parent/'linguistic-measurement-v1'

def step(name,command):
    log=BASE/(name+'.log');assert not log.exists(),log
    with log.open('x') as output:r=subprocess.run(command,cwd=ROOT,stdout=output,stderr=subprocess.STDOUT)
    event=dict(step=name,exit_code=r.returncode,log=str(log.relative_to(ROOT)))
    with (BASE/'publication-sequence.jsonl').open('a') as output:output.write(json.dumps(event)+chr(10))
    print(json.dumps(event),flush=True)
    if r.returncode:raise SystemExit(r.returncode)

def main():
    verify_bindings(json.loads((BASE/'publication-plan-review.json').read_text()))
    push=json.loads((RECOVERY/'push-verification.json').read_text());consumed=json.loads((RECOVERY/'delivery-consumed.json').read_text())
    assert push['status']=='pass' and consumed['exit_code']==0 and consumed['commit']==push['commit']
    for revision in ['HEAD','origin/main']:assert subprocess.check_output(['git','rev-parse',revision],cwd=ROOT,text=True).strip()==push['commit']
    for name,script,verb in [
      ('reader-publish','publish_causal_modeling_reader_20261028','publish'),
      ('census-progress','reconcile_causal_modeling_20261028',None),
      ('sponsor-prepare','build_causal_modeling_sponsor_20261028','prepare'),
      ('sponsor-build','build_causal_modeling_sponsor_20261028','build'),
      ('renew','publish_causal_modeling_reader_20261028','renew'),
      ('sponsor-review','publish_causal_modeling_sponsor_20261028','review'),
      ('sponsor-publish','publish_causal_modeling_sponsor_20261028','publish'),
      ('program-refresh','refresh_causal_modeling_program_20261028',None)]:
        command=['python3','tools/run_with_review_context_cache_20261025.py','tools/'+script+'.py']
        if verb:command.append(verb)
        step(name,command)
    for name,tool in [('program-check','run_program_checkpoint_v3'),('legacy-check','causal_program')]:step(name,['python3','tools/'+tool+'.py','check'])
    state=json.loads((ROOT/'docs/program/state.json').read_text())
    write(BASE/'publication-checkpoint.json',dict(status='published_checked',reader=state['reader'],sponsor=ref(ROOT/'docs/sponsor_proposal_causal_modeling_reviewed_2026-10-28.pdf','Exact paired sponsor'),recorded=350,nonpassing=150,census_inspected=82,census_unread=31,crosscutting=4,new_scholarly_originals=1,checks=[ref(BASE/(n+'.log'),'Successful full controller check') for n in ['program-check','legacy-check']],visual_acceptance=False,final_acceptance=False,background_worker_running=False))
    print('Publication and both full checks completed.',flush=True)

if __name__=='__main__':main()
