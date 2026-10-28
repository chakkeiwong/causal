#!/usr/bin/env python3
"""Resume the verified October25 survey publication at its interrupted yield."""
from collections import Counter
from pathlib import Path
import json,subprocess
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings,transition
from execute_agent_evaluation_surveys_publication_v2_20261025 import step
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-25/agent-evaluation-surveys-v1'
RECOVERY=ROOT/'docs/program/execution/2026-10-28/crash-recovery-v1'
SOURCE=BASE.parent/'census-observation-workflow-v1'
read=lambda p:json.loads(p.read_text())

def resume_census():
    run=controller.base;core=run.core;state=core.read(ROOT,core.STATE)
    assert state['reader']['path']=='docs/causal_proposal_agent_evaluation_surveys_reviewed_v2_2026-10-25.pdf'
    assert state['execution_runtime']['active']['operation']=='LL.CENSUS'
    assert not (BASE/'census-reconciliation.json').exists()
    assert not (BASE.parent/'sponsor-agent-evaluation-surveys-v1').exists()
    verify_bindings(read(BASE/'publication-plan-review-v2.json'))
    note=read(BASE/'integrated-progress.json');verify_bindings(note)
    issues=run.validate_state(ROOT,state);assert not issues,issues
    write(RECOVERY/'pre-resume-validation.json',dict(status='pass',issues=issues,reader=state['reader'],active=state['execution_runtime']['active'],evidence=[ref(BASE/'integrated-progress.json','Saved unconsumed census yield'),ref(BASE.parent/'agent-evaluation-surveys-reader-v2/working-release.json','Already published exact reader')]))
    transition('yield','LL.CENSUS',BASE/'integrated-progress.json')
    state=core.read(ROOT,core.STATE);_,merged,_=run.combined(ROOT,state)
    saved=merged['execution_program']['progress']['LL.CENSUS'][-1]
    assert saved['path']==str((BASE/'integrated-progress.json').relative_to(ROOT))
    verify_bindings(saved);assert state['execution_runtime']['active'] is None
    counts=Counter(x['disposition'] for x in read(SOURCE/'census-register.json')['items'])
    write(BASE/'census-reconciliation.json',dict(status='pass',counts=dict(counts),originals_closed=0,related_preprints_inspected=2,evidence=[saved,ref(SOURCE/'review.json','Reviewed source delta'),ref(RECOVERY/'pre-resume-validation.json','Crash recovery resumes pending yield')],next_action=note['next_action']))
    write(RECOVERY/'census-resume-result.json',dict(status='pass',active=None,evidence=[ref(BASE/'census-reconciliation.json','Recovered completed checkpoint')]))
    print('Recovered saved census yield without repeating reader publication.',flush=True)

def main():
    assert not RECOVERY.exists();RECOVERY.mkdir(parents=True)
    state=read(ROOT/'docs/program/state.json')
    write(RECOVERY/'captured-state.json',state)
    predecessor=read(BASE.parent/'data-workflow-wave-v1/push-verification.json')
    for revision in ['HEAD','origin/main']:
        assert subprocess.check_output(['git','rev-parse',revision],cwd=ROOT,text=True).strip()==predecessor['commit']
    write(RECOVERY/'recovery-plan.json',dict(status='reviewed_for_exact_pending_phase',client_date='2026-10-28',session=13915,session_status='unknown_after_machine_crash;no_exit_invented',git_predecessor=predecessor['commit'],completed=['Reader publication verified in canonical state and sequence receipt.'],pending=['Census yield written but not committed.','Sponsor build,exact-byte review renewal,master reconciliation,full checks,commit and push.'],evidence=[ref(BASE/'publication-plan-review-v2.json','Preserved reviewed publication plan'),ref(RECOVERY/'captured-state.json','Observed interruption state'),ref(Path(__file__),'Phase-specific recovery executor')],steps=['Validate saved state and yield existing census note.','Continue unused sponsor/review/publication phases.','Run both unchanged full controllers.','Commit and push,consume delivery,then execute prepared benchmark wave.'],old_logs_preserved=True,duplicate_publication=False))
    step('crash28-census-resume',['python3','tools/run_with_review_context_cache_20261025.py','tools/recover_survey_publication_20261028.py','resume-census'])
    for name,stem,verb in [('sponsor-prepare','build_agent_evaluation_surveys_sponsor','prepare'),('sponsor-build','build_agent_evaluation_surveys_sponsor','build'),('renew','publish_agent_evaluation_surveys_reader_v2','renew'),('sponsor-review','publish_agent_evaluation_surveys_sponsor','review'),('sponsor-publish','publish_agent_evaluation_surveys_sponsor','publish'),('program-refresh','refresh_agent_evaluation_surveys_program',None)]:
        command=['python3','tools/run_with_review_context_cache_20261025.py','tools/'+stem+'_20261025.py']
        if verb:command.append(verb)
        step(name,command)
    for name,tool,verb in [('program-status','run_program_checkpoint_v3','status'),('legacy-status','causal_program','status'),('program-check','run_program_checkpoint_v3','check'),('legacy-check','causal_program','check')]:
        step(name,['python3','tools/'+tool+'.py',verb])
    state=read(ROOT/'docs/program/state.json');remaining=read(BASE.parent/'program-refresh-agent-evaluation-surveys-v1/remaining-operations.json')
    write(BASE/'publication-checkpoint.json',dict(status='published_checked',reader=state['reader'],sponsor=ref(ROOT/'docs/sponsor_proposal_agent_evaluation_surveys_reviewed_2026-10-25.pdf','Exact paired sponsor'),recorded=remaining['recorded'],ready=remaining['ready'],nonpassing=len(remaining['operations']),census_inspected=82,census_unread=31,crosscutting=4,related_preprints_inspected=2,new_original_dispositions=0,checks=[ref(BASE/(n+'.log'),'Successful full unmodified controller check') for n in ['program-check','legacy-check']],recovery=ref(RECOVERY/'recovery-plan.json','Resumed28October2026'),next_action='Commit,push,consume recovery delivery;continue reviewed benchmark-oracle publication.',visual_acceptance=False,final_acceptance=False))
    step('crash28-stage-recovery',['git','add','-f','--',str(RECOVERY.relative_to(ROOT)),str(Path(__file__).relative_to(ROOT))])
    step('crash28-delivery',['python3','tools/deliver_agent_evaluation_surveys_publication_v2_20261025.py'])
    print('Recovered survey publication and delivery completed.',flush=True)

if __name__=='__main__':
    import sys
    if sys.argv[1:]==['resume-census']:resume_census()
    else:main()
