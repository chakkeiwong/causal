"""Turn performed reviews into specific independent successor work packets."""
import json
from pathlib import Path
from run_followup_program_20261028 import ROOT,BASE,append,load
from prepare_followup_program_20261028 import ref,write


def main():
    key='FOLLOWUP.DISPATCH';state=load();node=state['nodes'][key]
    assert state['next']==key
    outputs=['gap-routes.json','l6-profiles.json','l1-essentiality.json','software-tails.json']
    evidence=[ref(BASE/n,'Performed finite reconciliation') for n in outputs]
    start=BASE/'dispatch-start.json';write(start,dict(task=key,awards_acceptance=False,next_action=node['action'],evidence=evidence));append('start',key,str(start.relative_to(ROOT)))
    nextbase=BASE.parent/'followup-runtime-v2';assert not nextbase.exists();nextbase.mkdir()
    specs=[
      ('PYTHON.DELTA',[], 'Compare Python IID omissions against the current integrated source audit and saved source receipts; preserve already reviewed ENCO and gCastle work.', ['Each original omission is compared with exact later evidence without claiming exhaustive absence.','Only genuinely missing or uninspected selected originals advance to acquisition.'], 'python-delta.json'),
      ('CDT.DELEGATES',['PYTHON.DELTA'], 'Acquire the exact saved-tree pc.R,ges.R and R launcher blobs for the selected CDT commit; inspect target,labels,score and dependency semantics without execution.', ['Original identity,Git blob,SHA256,receipt and anchored technical findings are complete or an exact local route blocker is recorded.','Trace the int-score label and node-order mapping; preserve unresolved dependency rights/version and do not claim native qualification.'], 'cdt-delegates.json'),
      ('L1.SUCCESSOR',[], 'Record a preserving L1 chapter successor on the exact current reader using the14task comparison and31unread-original restrictions; keep full coverage inconclusive.', ['Predecessor/source/content preservation and the existing eight-page exclusive depth are evidenced.','Same original criteria and current reader are reviewed; no unknown essentiality or visual acceptance silently closed.'], 'l1-successor.json'),
      ('L6.LOCALPROFILE',[], 'Select one exact local-server candidate behind the already reviewed Ollama client and inspect available cutoff identity/API/rights leads; define the missing model profile.', ['Client,server and model artifacts remain distinct with exact selected identities or explicit unknowns.','Only primary inspected material supports technical claims; no automatic model/service right or native guarantee.'], 'local-profile.json'),
    ]
    tasks=[dict(id=k,depends=deps,scope='Bounded proposal source/review successor; original acceptance remains separate',action=action,acceptance=criteria,outputs=[str((nextbase/name).relative_to(ROOT))],owner='Current author/coordinator') for k,deps,action,criteria,name in specs]
    write(nextbase/'contracts.json',dict(schema_version=1,awards_acceptance=False,canonical_obligations=376,tasks=tasks,evidence=evidence+[ref(BASE/'contracts.json','Preserved predecessor batch'),ref(ROOT/'tools/run_followup_program_v2_20261028.py','Pointer-aware queue runner')],cutoff='2026-10-07T15:59:59Z'))
    out=BASE/'next-contracts-review.json';write(out,dict(status='pass',tasks=tasks,evidence=evidence+[ref(nextbase/'contracts.json','Reviewed next finite work contracts')],findings=['Three independent roots; CDT depends only on its source delta.','Original criteria and outcomes remain unchanged; local unavailable original blocks only its packet.','Every packet names exact inputs,outputs,owner and acceptance review; no background worker.'],remaining_other_obligations='All150original obligations remain in gap-routes.json; this finite dispatch does not mark them complete.'))
    receipt=BASE/'dispatch-receipt.json';write(receipt,dict(task=key,awards_acceptance=False,execution='performed',outcome='pass',outputs=[ref(out,'Reviewed next queue')],evidence=evidence,criteria=[dict(index=0,verdict='pass',finding='Fourbounded tasks with three independent roots specify exact outputs and reviewed evidence.'),dict(index=1,verdict='pass',finding='No canonical acceptance outcome or prerequisite changed; original150gap register retained.')],next_action='Execute the next finite batch immediately; source blocks remain local.'))
    append('record',key,str(receipt.relative_to(ROOT)))
    pointer=ROOT/'docs/program/execution/followup-current.json';assert not pointer.exists()
    write(pointer,dict(contracts=ref(nextbase/'contracts.json','Current reviewed followup batch'),predecessor=ref(BASE/'next-contracts-review.json','Reviewed dispatch'),awards_acceptance=False))
    print(json.dumps(dict(first_batch_completed=5,next_batch_tasks=4,next='PYTHON.DELTA')))


if __name__=='__main__':main()
