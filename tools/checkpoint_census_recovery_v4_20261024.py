#!/usr/bin/env python3
"""Replace stale census continuation after completed integration; never close census."""
import json,subprocess,sys
from pathlib import Path
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
ROOT=Path(__file__).resolve().parents[1];DAY=ROOT/'docs/program/execution/2026-10-24';BASE=DAY/'census-continuation-repair-v4'
state=json.loads((ROOT/'docs/program/state.json').read_text());assert state['execution_runtime']['active'] is None
assert state['reader']['path']=='docs/causal_proposal_affordance_fuzzing_reviewed_2026-10-24.pdf';assert not BASE.exists();BASE.mkdir()
evidence=[ref(DAY/p,'Completed publication or remaining census evidence') for p in ['census-affordance-fuzzing-v1/progress.json','census-affordance-fuzzing-v1/census-register.json','census-affordance-fuzzing-v1/omissions-register.json','census-causal-compositional-v1/acquisition-review.json','program-refresh-css-knowledge-v1/program-review.json','affordance-fuzzing-reader-v1/working-release.json','sponsor-affordance-fuzzing-v1/working-release.json']]
progress=dict(finding='Candidate191original,pinned implementation and separately identified affordance original delivered;80inspected and33unread inherited originals plus4crosscutting. Candidate163conference original remains open.',next_action='Continue the 33 unread originals and four crosscutting tasks. Candidate163 exact conference source is outside the fixed collector allowlist; its related affordance preprint is already delivered and does not close the original gap. Resolve candidate165 journal original separately from its inspected preprint; candidate217 access/date and candidate27 metadata limits remain local. Prioritize a permitted original for causal-workflow,energy-cost or temporal-discovery evaluation; inspect methods and adverse findings before any claim. Do not repeat completed affordance/fuzzing,CSS/knowledge,scientific-method,Python/Java,Ray or Splink publication. Independent C++policy,commercial and reuse tasks remain eligible.',evidence=evidence,yield_reason='Replace completed publication instruction without closing the census; keep independent obligations eligible.')
verify_bindings(progress);write(BASE/'progress.json',progress)
for phase,args in [('start',['start','LL.CENSUS','--reason','Repair stale durable continuation after completed publications.']),('yield',['yield','LL.CENSUS','--receipt',str((BASE/'progress.json').relative_to(ROOT))])]:
 with (BASE/(phase+'.log')).open('x') as stream:
  result=subprocess.run([sys.executable,'tools/run_program_checkpoint_v3.py']+args,cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT,timeout=600)
 assert result.returncode==0,phase
 print(json.dumps(dict(phase=phase,status='pass')),flush=True)
