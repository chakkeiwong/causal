#!/usr/bin/env python3
"""Checkpoint completed publication without closing the census."""
import json,subprocess,sys
from pathlib import Path
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
ROOT=Path(__file__).resolve().parents[1];DAY=ROOT/'docs/program/execution/2026-10-23';BASE=DAY/'census-controlled-writes-v1'
state=json.loads((ROOT/'docs/program/state.json').read_text());assert state['execution_runtime']['active'] is None
assert state['reader']['path']=='docs/causal_proposal_controlled_writes_reviewed_2026-10-23.pdf'
evidence=[ref(DAY/p,'Completed source/publication unit') for p in ['census-controlled-writes-v1/review.json','census-controlled-writes-v1/census-register.json','census-controlled-writes-v1/task-map.json','controlled-writes-reader-v1/working-release.json','sponsor-controlled-writes-v1/working-release.json','census-scientific-method-v1/identity-followup.json']]
progress=dict(finding='Candidate130 integrated into1299-page reader and paired sponsor;992 reader citations/232 genuine PDFs. Census70/43 remains incomplete.',next_action='Continue43 unread originals and four crosscutting obligations. Candidate165 publisher route failed; seek a genuine author/repository original or select candidate261 sensitivity-uncertainty alignment, candidate252 agent memory, or candidate206 financing constraints. Inspect methods and adverse findings before citation. Controlled-write, GIST, medflex and sensitivity publications are complete. Independent software/reuse/commercial/chapter obligations remain eligible; native trials need actual environments.',evidence=evidence,yield_reason='Release operation after completed integration; census remains open and no phase-boundary approval is needed.')
verify_bindings(progress);write(BASE/'integrated-progress.json',progress)
steps=[('start',['start','LL.CENSUS','--reason','Refresh remaining-original actions']),('yield',['yield','LL.CENSUS','--receipt',str((BASE/'integrated-progress.json').relative_to(ROOT))])]
for phase,args in steps:
 with (BASE/('integrated-'+phase+'.txt')).open('x') as stream:
  result=subprocess.run([sys.executable,'tools/run_program_checkpoint_v3.py']+args,cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT,timeout=600)
 assert result.returncode==0,phase
 print(json.dumps(dict(phase=phase,status='pass')),flush=True)
