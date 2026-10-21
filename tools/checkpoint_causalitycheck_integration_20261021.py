import json
from pathlib import Path
from publish_latent_r_review_v2_20261013 import ref,transition,write
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-21/census-causalitycheck-v1'
SPONSOR=ROOT/'docs/program/execution/2026-10-21/sponsor-causalitycheck-v1'
write(BASE/'integrated-progress.json',dict(
 finding='Candidate109 integrated into1175-page reader and37-page sponsor;864 audited records,215 genuine papers; exact-reader Q2-Q4 renewed; census55/58.',
 next_action='Continue58 unread originals,starting candidate26 ACE bowtie extraction or another accessible original. Preserve source-specific blockers. Complete complementary longitudinal/off-policy and negative-result searches and citation chaining. Recover CausalityCheck pinned code/data and raw paired seed judgments before reuse. Do not repeat completed candidate109 acquisition/publication.',
 evidence=[ref(BASE/n,'Integrated census evidence') for n in ['working-release.json','census-register.json','task-map.json','release-source-review.json']]+[ref(SPONSOR/'working-release.json','Exact paired sponsor')],
 yield_reason='Preserve completed integration and release controller for integrity/Git checks; independent eligible work continues at the recorded next action.'))
transition('yield','LL.CENSUS',BASE/'integrated-progress.json')
