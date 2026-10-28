"""Close only reviewed source publication; retain all canonical obligations."""
import json
from pathlib import Path
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write
from run_followup_program_20261028 import ROOT,append,load
from run_followup_program_v2_20261028 import selected


def main():
    day=ROOT/'docs/program/execution/2026-10-29';q=selected()
    assert load(ROOT,q)['active']=='PANEL.INFERENCE.PUBLICATION'
    base=day/'panel-inference-publication-v1';evidence=[]
    for name in ['reader-prepare','reader-finalize','reader-review','reader-publish','reader-renew','sponsor-prepare','sponsor-build','sponsor-review','sponsor-publish','chapters','refresh','legacy-check','program-check']:
        p=base/(name+'-exit.json');d=json.loads(p.read_text());verify_bindings(d);assert d['actual_exit_code']==0
        if name.endswith('-check'):assert d['unwrapped']
        evidence.append(ref(p,'Performed zero exit'))
    failed=json.loads((base/'reader-build-exit.json').read_text());verify_bindings(failed);assert failed['actual_exit_code']==1
    evidence += [ref(base/'reader-build-exit.json','Preserved post-compilation assertion failure'),ref(day/'panel-inference-reader-v1/build-repair.json','Verified completion without recompilation')]
    reader=json.loads((day/'panel-inference-reader-v1/working-release.json').read_text())
    sponsor=json.loads((day/'sponsor-panel-inference-v1/working-release.json').read_text())
    for d in [reader,sponsor]:verify_bindings(d)
    assert reader['pdf']['sha256']==sponsor['paired_monograph']['sha256']
    evidence += [ref(day/p,'Exact reviewed result') for p in ['panel-inference-contracts-v1/review.json','panel-inference-reader-v1/release-source-review.json','sponsor-panel-inference-v1/author-review.json','program-refresh-panel-inference-v1/program-review.json','continuation-handoff-v3/author-review.json']]
    out=q/'publication.json';write(out,dict(status='performed_pass',reader=reader['pdf'],sponsor=sponsor['pdf'],evidence=evidence,native_execution=False,visual_acceptance=False,final_acceptance=False))
    receipt=q/'publication-receipt.json';write(receipt,dict(task='PANEL.INFERENCE.PUBLICATION',awards_acceptance=False,execution='performed',outcome='pass',outputs=[ref(out,'Preserving paired publication')],evidence=evidence,
        criteria=[dict(index=0,verdict='pass',finding='All1449reader and1122sponsor predecessor source records, reader contexts and compiled content inputs preserved.'),dict(index=1,verdict='pass',finding='Exact source/text checks, Q2-Q4 renewals, L1/L6 successors, refreshed handoff and both unchanged controllers pass. Label-report failure retained and repaired.')],
        next_action='Deliver exact publication; continue pinned runtime-source and independent unresolved rows. No canonical acceptance awarded.'))
    append('record','PANEL.INFERENCE.PUBLICATION',str(receipt.relative_to(ROOT)),ROOT,q)
    from run_followup_program_v3_20261028 import current
    live=current();assert live['continue_work'] and live['unresolved_obligations']==150
    write(q/'handoff-verification.json',dict(status='pass',next=live['next'],next_action=live['next_action'],unresolved=150,evidence=[ref(receipt,'Completed finite packet')],awards_acceptance=False))
    print(json.dumps(dict(completed_packet=True,continue_work=True,next=live['next'],nonpassing=150,proposal_complete=False)))


if __name__=='__main__':main()
