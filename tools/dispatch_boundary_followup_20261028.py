"""Install independent next work without rewriting completed batch contracts."""
import json
from run_followup_program_20261028 import ROOT,load,view
from run_followup_program_v2_20261028 import selected,POINTER
from prepare_followup_program_20261028 import ref,write

def main():
    prior=selected();state=load(ROOT,prior);assert all(s=='completed' for s in state['states'].values())
    base=prior.parent/'followup-runtime-v3';assert not base.exists();base.mkdir()
    specs=[
      ('PUBLICATION.PAIR','Compile and source-review the prepared CDT/server additions,preserve all prior citations,pair sponsor,renew exact-reader reviews and run unchanged full controllers.',['All prior reader/sponsor source records and compiled content are preserved; new claims bind inspected originals.','Exact reader pairing,arithmetic,text bounds and unchanged full integrity checks pass; visual/full coverage remain open.'],'publication.json'),
      ('PYTHON.RLTAIL','Use the pinned gCastle catalog/tree to identify RL and CORL originals and available associated papers; inspect bounded technical source paths or record precise source-access limits.',['Existing gCastle PC/NOTEARS review and ENCO paper are preserved without duplication.','Selected RL/CORL identity,source/paper availability and next technical route are explicit; no exhaustive attention-family coverage inferred.'],'python-rl-tail.json'),
      ('CDT.DEPENDENCIES','Trace exact available CDT dependency declarations against the reviewed R launcher and separate pcalg source; record declared constraints versus unresolved installation and rights.',['Inspect actual manifests and identify which interpreter/packages are constrained or merely availability-probed.','Specify a concrete public conversion/failure fixture and remaining dependency/rights intake; do not invent installed versions.'],'cdt-dependencies.json'),
    ]
    evidence=[ref(prior/n,'Completed predecessor packet') for n in ['contracts.json','python-delta.json','cdt-delegates.json','local-profile.json','l1-successor.json']]
    tasks=[dict(id=key,depends=[],scope='Finite author proposal work,not product acceptance',action=action,acceptance=criteria,outputs=[str((base/name).relative_to(ROOT))],owner='Current author/coordinator') for key,action,criteria,name in specs]
    write(base/'contracts.json',dict(schema_version=1,awards_acceptance=False,canonical_obligations=376,tasks=tasks,evidence=evidence,cutoff='2026-10-07T15:59:59Z'))
    write(base/'plan-review.json',dict(status='pass',findings=['Three independent packets; a source access limit cannot prevent publication or dependency inspection.','Publication preserves both current deliverables and unchanged validators.','Finite source review does not close full Python or L6 coverage.','The active agent continues across completed packets; no unattended worker is asserted.'],evidence=evidence+[ref(base/'contracts.json','Exact work contracts')]))
    (base/'prior-pointer.json').write_bytes(POINTER.read_bytes())
    POINTER.write_text(json.dumps(dict(contracts=ref(base/'contracts.json','Current reviewed followup batch'),predecessor=ref(base/'plan-review.json','Reviewed dispatch'),awards_acceptance=False),indent=2)+'\n')
    print(json.dumps(view(load(ROOT,base))))

if __name__=='__main__':main()
