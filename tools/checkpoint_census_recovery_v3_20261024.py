#!/usr/bin/env python3
"""Replace stale census continuation after completed integration; never close census."""
import json,subprocess,sys
from pathlib import Path
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
ROOT=Path(__file__).resolve().parents[1];DAY=ROOT/'docs/program/execution/2026-10-24';BASE=DAY/'census-continuation-repair-v3'
state=json.loads((ROOT/'docs/program/state.json').read_text());assert state['execution_runtime']['active'] is None
assert state['reader']['path']=='docs/causal_proposal_css_knowledge_reviewed_2026-10-24.pdf';assert not BASE.exists();BASE.mkdir()
evidence=[ref(DAY/p,'Completed publication or remaining census evidence') for p in ['census-css-knowledge-v1/progress.json','census-css-knowledge-v1/census-register.json','census-css-knowledge-v1/omissions-register.json','program-refresh-splink-v1/program-review.json','css-knowledge-reader-v1/working-release.json','sponsor-css-knowledge-v1/working-release.json']]
progress=dict(finding='CSS/knowledge author-original reviews and paired integration delivered; census now 79 inspected and 34 unread originals plus four crosscutting obligations.',next_action='Continue the 34 unread originals and four crosscutting tasks. Prioritize candidate163 causal/compositional reasoning using genuine cutoff-eligible originals. Resolve candidate165 journal original separately from its inspected preprint; candidate217 access/date and candidate27 metadata limits remain local. Inspect methods, assumptions and adverse findings, update task map and preserve current citations. Do not repeat completed CSS/knowledge, scientific-method, Python/Java, Ray or Splink publication. Independent software, reuse and commercial tasks remain eligible.',evidence=evidence,yield_reason='Replace completed publication instruction without closing the census; keep independent obligations eligible.')
verify_bindings(progress);write(BASE/'progress.json',progress)
for phase,args in [('start',['start','LL.CENSUS','--reason','Repair stale durable continuation after completed publications.']),('yield',['yield','LL.CENSUS','--receipt',str((BASE/'progress.json').relative_to(ROOT))])]:
 with (BASE/(phase+'.log')).open('x') as stream:
  result=subprocess.run([sys.executable,'tools/run_program_checkpoint_v3.py']+args,cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT,timeout=600)
 assert result.returncode==0,phase
 print(json.dumps(dict(phase=phase,status='pass')),flush=True)
