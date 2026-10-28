"""Close only the bounded estimator review after exact publication checks."""
import json
from pathlib import Path
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write
from run_followup_program_20261028 import ROOT,append,load
from run_followup_program_v2_20261028 import selected

def main():
 day=ROOT/'docs/program/execution/2026-10-28';queue=selected();assert load(ROOT,queue)['active']=='PANEL.ESTIMATOR.CONTRACTS';base=day/'panel-estimator-publication-v1';evidence=[]
 for name in ['reader-prepare','reader-build','reader-review','reader-publish','reader-renew','sponsor-prepare','sponsor-build','sponsor-review','sponsor-publish','chapters','refresh','legacy-check','program-check']:
  p=base/(name+'-exit.json');d=json.loads(p.read_text());verify_bindings(d);assert d['actual_exit_code']==0
  if name.endswith('-check'):assert d['unwrapped']
  evidence.append(ref(p,'Actual performed step'))
 reader=json.loads((day/'panel-estimators-reader-v1/working-release.json').read_text());sponsor=json.loads((day/'sponsor-panel-estimators-v1/working-release.json').read_text())
 for d in [reader,sponsor]:verify_bindings(d)
 assert reader['pdf']['sha256']==sponsor['paired_monograph']['sha256']
 evidence += [ref(day/p,'Reviewed source or delivery') for p in ['panel-estimator-contracts-v1/review.json','panel-estimators-reader-v1/release-source-review.json','sponsor-panel-estimators-v1/author-review.json','program-refresh-panel-estimators-v1/program-review.json','continuation-handoff-v2/author-review.json']]
 out=queue/'estimator-contracts.json';write(out,dict(status='performed_pass',reader=reader['pdf'],sponsor=sponsor['pdf'],evidence=evidence,native_execution=False,visual_acceptance=False,final_acceptance=False))
 receipt=queue/'estimator-contracts-receipt.json';write(receipt,dict(task='PANEL.ESTIMATOR.CONTRACTS',awards_acceptance=False,execution='performed',outcome='pass',outputs=[ref(out,'Exact source and paired publication')],evidence=evidence,criteria=[dict(index=0,verdict='pass',finding='Nine pinned originals have SHA256, Git blob, cutoff identity and inspected anchors; all1447reader and1118sponsor prior citations preserved.'),dict(index=1,verdict='pass',finding='Exact arithmetic/translation witnesses and current paired PDFs pass source/text checks; native, upstream, rights, visual and broad coverage limits remain.')],next_action='Continue BMisc/parglm, common constructor and upstream editions through the persistent master handoff; this packet grants no canonical acceptance.'))
 append('record','PANEL.ESTIMATOR.CONTRACTS',str(receipt.relative_to(ROOT)),ROOT,queue)
 from run_followup_program_v3_20261028 import current
 live=current();assert live['packet_exhausted'] and live['continue_work'] and live['unresolved_obligations']==150
 write(queue/'handoff-verification.json',dict(status='pass',next=live['next'],next_action=live['next_action'],unresolved=150,evidence=[ref(receipt,'Finished bounded packet')],awards_acceptance=False))
 print(json.dumps(dict(completed_packet=True,continue_work=True,next=live['next'],nonpassing=150,proposal_complete=False)))

if __name__=='__main__':main()
