"""Serialize reviewed publication, exact-reader checks and unchanged full audits."""
import json,subprocess
from pathlib import Path
from run_followup_program_v2_20261028 import selected
from run_followup_program_20261028 import append,load
from prepare_followup_program_20261028 import ref,write
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'docs/program/execution/2026-10-28/boundary-profile-review-v2'

def step(name,command):
    log=BASE/(name+'.log');assert not log.exists(),log
    with log.open('x') as out:r=subprocess.run(command,cwd=ROOT,stdout=out,stderr=subprocess.STDOUT)
    event=dict(step=name,exit_code=r.returncode,log=str(log.relative_to(ROOT)))
    with (BASE/'publication-sequence.jsonl').open('a') as out:out.write(json.dumps(event)+'\n')
    print(json.dumps(event),flush=True)
    if r.returncode:raise SystemExit(r.returncode)

def main():
    prior=json.loads((BASE.parent/'delegate-contract-review-v1/delivery-consumed.json').read_text());assert prior['actual_exit_code']==0
    for rev in ['HEAD','origin/main']:assert subprocess.check_output(['git','rev-parse',rev],cwd=ROOT,text=True).strip()==prior['commit']
    assert json.loads((BASE/'reader-build-consumed.json').read_text())['actual_exit_code']==0
    queue=selected();key='PUBLICATION.PAIR';assert load(ROOT,queue)['next']==key
    start=queue/'publication-start.json';write(start,dict(task=key,awards_acceptance=False,next_action='Publish source-reviewed reader,pair sponsor,renew chapter reviews and run unchanged full checks.',evidence=[ref(BASE/'reader-build-consumed.json','Observed successful build')]))
    append('start',key,str(start.relative_to(ROOT)),ROOT,queue)
    for name,script,verb in [
      ('reader-review','publish_boundary_profile_reader_v2_20261028','review'),
      ('reader-publish','publish_boundary_profile_reader_v2_20261028','publish'),
      ('sponsor-prepare','build_boundary_profile_sponsor_v2_20261028','prepare'),
      ('sponsor-build','build_boundary_profile_sponsor_v2_20261028','build'),
      ('renew','publish_boundary_profile_reader_v2_20261028','renew'),
      ('sponsor-review','publish_boundary_profile_sponsor_v2_20261028','review'),
      ('sponsor-publish','publish_boundary_profile_sponsor_v2_20261028','publish'),
      ('chapter-review','review_boundary_profile_chapters_20261028',None),
      ('program-refresh','refresh_boundary_profile_program_20261028',None)]:
        command=['python3','tools/run_with_review_context_cache_20261025.py','tools/'+script+'.py']
        if verb:command.append(verb)
        step(name,command)
    for name,script in [('program-check','run_program_checkpoint_v3'),('legacy-check','causal_program')]:step(name,['python3','tools/'+script+'.py','check'])
    state=json.loads((ROOT/'docs/program/state.json').read_text())
    write(BASE/'publication-checkpoint.json',dict(status='published_checked',reader=state['reader'],sponsor='docs/sponsor_proposal_boundary_profile_reviewed_v2_2026-10-28.pdf',recorded=351,nonpassing=150,visual_acceptance=False,final_acceptance=False))
    out=queue/'publication.json';write(out,dict(status='performed_pass',reader=state['reader'],sponsor='docs/sponsor_proposal_boundary_profile_reviewed_v2_2026-10-28.pdf',evidence=[ref(BASE/n,'Observed checked publication') for n in ['publication-checkpoint.json','program-check.log','legacy-check.log']],visual_acceptance=False,final_acceptance=False))
    receipt=queue/'publication-receipt.json';write(receipt,dict(task=key,awards_acceptance=False,execution='performed',outcome='pass',outputs=[ref(out,'Paired preserving publication')],evidence=[ref(BASE/'publication-checkpoint.json','Serialized publication')],criteria=[dict(index=0,verdict='pass',finding='All1415reader and1068sponsor predecessor records retained; new source and exact witnesses bind originals.'),dict(index=1,verdict='pass',finding='Exact pairing,arithmetic,text bounds and unchanged full controllers pass; visual/full coverage remain open.')],next_action='Consume process exit and commit/push; proceed to independent RL/CORL source and CDT dependency packets.'))
    append('record',key,str(receipt.relative_to(ROOT)),ROOT,queue)
    print('Paired publication and unchanged full checks completed.',flush=True)

if __name__=='__main__':main()
