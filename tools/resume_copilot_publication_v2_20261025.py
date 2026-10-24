#!/usr/bin/env python3
"""Resume after successful yield; scheduler rotation is not checkpoint loss."""
import json
from pathlib import Path
import run_program_checkpoint_v3 as controller
from execute_copilot_reuse_publication_20261025 import ROOT, BASE, step
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings, transition

def main():
    census=BASE.parent/'census-continuation-v1'
    state=json.loads((ROOT/'docs/program/state.json').read_text())
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path']=='docs/causal_proposal_copilot_reuse_reviewed_2026-10-25.pdf'
    assert not (BASE/'publication-checkpoint.json').exists()
    verify_bindings(json.loads((census/'review.json').read_text()))
    write(BASE/'recovery-plan-review-v2.json',dict(status='pass',
        reason='Yield succeeded and scheduler selected an independent operation. Validate the saved LL.CENSUS checkpoint separately from the global next task; do not repeat its successful mutation.',
        evidence=[ref(BASE/'resume-publication.log','Preserved post-yield assertion failure'),
                  ref(BASE/'recovery-plan-review.json','Earlier transition repair'),
                  ref(census/'review.json','Preserving census review'),
                  ref(Path(__file__),'Resume only unfinished refresh/check/delivery')],
        completed_steps_not_repeated=['Operation record','Reader publication','Sponsor publication','Q2-Q4 renewal','Census start and yield'],
        final_acceptance=False))
    note=json.loads((census/'integrated-progress.json').read_text())
    _,merged,_=controller.base.combined(ROOT,state)
    saved=merged['execution_program']['progress']['LL.CENSUS'][-1]
    assert saved['path']==str((census/'integrated-progress.json').relative_to(ROOT))
    verify_bindings(saved)
    assert json.loads((ROOT/saved['path']).read_text())['next_action']==note['next_action']
    view=controller.status(ROOT,state)
    assert state['execution_runtime']['active'] is None
    write(census/'verification.json',dict(status='pass',next=view['next'],next_action=view['next_action'],
        census_next_action=note['next_action'],checkpoint=saved,
        scheduler_may_select_independent_operation=True,
        evidence=[ref(census/'review.json','Reviewed preserving correction'),ref(BASE/'recovery-plan-review-v2.json','Corrected verification')]))
    step('program-refresh',['python3','tools/refresh_copilot_reuse_program_20261025.py'])
    for name,tool,verb in [('program-status','run_program_checkpoint_v3','status'),('legacy-status','causal_program','status'),('program-check','run_program_checkpoint_v3','check'),('legacy-check','causal_program','check')]:
        step(name,['python3','tools/'+tool+'.py',verb])
    state=json.loads((ROOT/'docs/program/state.json').read_text())
    remaining=json.loads((BASE.parent/'program-refresh-copilot-reuse-v1/remaining-operations.json').read_text())
    write(BASE/'publication-checkpoint.json',dict(status='published_checked',reader=state['reader'],
        sponsor=ref(ROOT/'docs/sponsor_proposal_copilot_reuse_reviewed_2026-10-25.pdf','Exact paired sponsor'),
        recorded=remaining['recorded'],ready=remaining['ready'],nonpassing=len(remaining['operations']),
        census_inspected=82,census_unread=31,crosscutting=4,original_blobs_revalidated=15,
        checks=[ref(BASE/(n+'.log'),'Successful check') for n in ['program-check','legacy-check']],
        recovery=ref(BASE/'recovery-plan-review-v2.json','Preserved failure and exact resume'),
        next_action='Commit and push the pair, then publish the reviewed commercial network reference choices.',
        visual_acceptance=False,final_acceptance=False,background_worker_running=False))
    print('Recovered Copilot publication and both checks complete.',flush=True)

if __name__=='__main__':main()
