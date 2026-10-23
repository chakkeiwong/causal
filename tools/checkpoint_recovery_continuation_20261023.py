#!/usr/bin/env python3
"""Refresh the exact unfinished census action after preserving both publication pairs."""
import json, subprocess, sys
from pathlib import Path
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-23/session-recovery-v2'
DAY=BASE.parent
state=json.loads((ROOT/'docs/program/state.json').read_text())
assert state['execution_runtime']['active'] is None
assert state['reader']['path']=='docs/causal_proposal_medflex_reuse_reviewed_2026-10-23.pdf'
evidence=[ref(DAY/p,'Completed recovered source/publication unit') for p in [
 'census-goal-state-v1/review-v2.json','census-goal-state-v1/census-register-v2.json','census-goal-state-v1/task-map-v2.json',
 'gist-census-reader-v1/working-release.json','sponsor-gist-census-v1/working-release.json',
 'medflex-reuse-v1/operation-receipt.json','medflex-reuse-reader-v1/working-release.json','sponsor-medflex-reuse-v1/working-release.json']]
progress=dict(finding='GIST original and source audit repaired and integrated; sensitivity, GIST and medflex publication pairs preserved; medflex reference-only decision recorded. Census69/44, not closed.',
 next_action='Continue44 unread originals and four crosscutting obligations. Prioritize candidate165 on hypothesis-to-discovery or candidate206 on financing constraints using an allowed authentic-original route; preserve acquisition failures and choose another accessible original. GIST and medflex are already published: do not repeat them. Independent reuse, commercial follow-ups and chapter rollups remain eligible; native trials require their own prerequisites.',
 evidence=evidence,yield_reason='Release canonical operation after replacing the stale integrate-GIST instruction; checkpoint preserves unfinished scope, not completion or a permission gate.')
verify_bindings(progress);write(BASE/'census-integrated-progress.json',progress)
for phase,args in [('start',['start','LL.CENSUS','--reason','Replace completed publication instructions with remaining source actions']),
                   ('yield',['yield','LL.CENSUS','--receipt',str((BASE/'census-integrated-progress.json').relative_to(ROOT))])]:
 with (BASE/('census-'+phase+'.txt')).open('x') as stream:
  result=subprocess.run([sys.executable,'tools/run_program_checkpoint_v3.py']+args,cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT,timeout=600)
 assert result.returncode==0,phase
 print(json.dumps(dict(phase=phase,status='pass')),flush=True)
