#!/usr/bin/env python3
"""Continue after preserved layout failure, then deliver the complete survey."""
from pathlib import Path
import json
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
from execute_agent_evaluation_surveys_publication_v2_20261025 import step,ROOT,BASE
RECOVERY=ROOT/'docs/program/execution/2026-10-28/crash-recovery-v1'
read=lambda p:json.loads(p.read_text())
def main():
    verify_bindings(read(RECOVERY/'sponsor-layout-repair.json'))
    state=read(ROOT/'docs/program/state.json');assert state['execution_runtime']['active'] is None
    assert state['reader']['path']=='docs/causal_proposal_agent_evaluation_surveys_reviewed_v2_2026-10-25.pdf'
    for name,tool,verb in [('crash28-sponsor-prepare-v2','build_agent_evaluation_surveys_sponsor_v2_20261028','prepare'),('crash28-sponsor-build-v2','build_agent_evaluation_surveys_sponsor_v2_20261028','build'),('renew','publish_agent_evaluation_surveys_reader_v2_20261025','renew'),('sponsor-review','publish_agent_evaluation_surveys_sponsor_v2_20261028','review'),('sponsor-publish','publish_agent_evaluation_surveys_sponsor_v2_20261028','publish'),('program-refresh','refresh_agent_evaluation_surveys_program_v2_20261028',None)]:
        cmd=['python3','tools/run_with_review_context_cache_20261025.py','tools/'+tool+'.py']
        if verb:cmd.append(verb)
        step(name,cmd)
    for name,tool,verb in [('program-status','run_program_checkpoint_v3','status'),('legacy-status','causal_program','status'),('program-check','run_program_checkpoint_v3','check'),('legacy-check','causal_program','check')]:step(name,['python3','tools/'+tool+'.py',verb])
    state=read(ROOT/'docs/program/state.json');remaining=read(BASE.parent/'program-refresh-agent-evaluation-surveys-v1/remaining-operations.json')
    write(BASE/'publication-checkpoint.json',dict(status='published_checked',reader=state['reader'],sponsor=ref(ROOT/'docs/sponsor_proposal_agent_evaluation_surveys_reviewed_2026-10-25.pdf','Exact paired whitespace-repaired sponsor'),recorded=remaining['recorded'],ready=remaining['ready'],nonpassing=len(remaining['operations']),census_inspected=82,census_unread=31,crosscutting=4,related_preprints_inspected=2,new_original_dispositions=0,checks=[ref(BASE/(n+'.log'),'Successful full unmodified controller check') for n in ['program-check','legacy-check']],recovery=ref(RECOVERY/'recovery-plan.json','Crash recovery28October2026'),layout_repair=ref(RECOVERY/'sponsor-layout-repair.json','Failed layout retained and whitespace-only successor'),next_action='Commit,push,consume delivery;continue prepared benchmark publication.',visual_acceptance=False,final_acceptance=False))
    paths=[str(RECOVERY.relative_to(ROOT))]+[str(p.relative_to(ROOT)) for p in (ROOT/'tools').glob('*survey*20261028.py')]+[str(p.relative_to(ROOT)) for p in (ROOT/'tools').glob('*agent_evaluation*20261028.py')]
    step('crash28-stage-recovery',['git','add','-f','--',*sorted(set(paths))])
    step('crash28-delivery',['python3','tools/deliver_agent_evaluation_surveys_publication_v2_20261025.py'])
    print('Recovered survey pair checked and delivered.',flush=True)
if __name__=='__main__':main()
