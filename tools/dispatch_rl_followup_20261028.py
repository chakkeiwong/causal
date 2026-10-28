"""Continue a completed finite batch without confusing it with proposal acceptance."""
import json
from run_followup_program_20261028 import ROOT,load,view
from run_followup_program_v2_20261028 import selected,POINTER
from prepare_followup_program_20261028 import ref,write

def main():
    prior=selected();assert all(v=='completed' for v in load(ROOT,prior)['states'].values())
    base=prior.parent/'followup-runtime-v4';assert not base.exists();base.mkdir()
    specs=[
      ('RL.PUBLICATION','Integrate the reviewed RL/CORL original papers,source findings,penalty-boundary qualification and CDT dependency protocol into preserving reader/sponsor successors.',['Retain1418reader/1073sponsor records and all content; five additional records have exact source/primary-PDF custody.','Exact arithmetic,pairing,text bounds and unchanged full controllers pass; no visual,full coverage or native acceptance.'],'publication.json'),
      ('ATTENTION.SEARCH','Run a finite complementary primary-repository/metadata discovery for distinct attention-based causal-discovery methods,compare existing audit and inspect originals only after identity/cutoff selection.',['Queries,denominators,duplicate decisions and cutoff limitations are recorded; metadata supports identity only.','Distinct candidates have exact permitted primary-source routes or local access limits; gCastle attention architecture alone does not close family coverage.'],'attention-search.json'),
      ('CDT.INSTALLER','Inspect the remaining pinned CDT install-dependencies script and its immediate selected script delegates as source text; qualify dependency constraints and license intake without installation.',['Exact original identity/custody and observed package-source pins are recorded.','Residual mutable endpoints and rights/runtime limits remain explicit; no script executed.'],'cdt-installer.json'),
    ]
    evidence=[ref(prior/n,'Completed prior packet') for n in ['contracts.json','publication.json','python-rl-tail.json','cdt-dependencies.json']]
    tasks=[dict(id=k,depends=[],scope='Finite proposal author work; no original acceptance awarded',action=a,acceptance=c,outputs=[str((base/o).relative_to(ROOT))],owner='Current author/coordinator') for k,a,c,o in specs]
    write(base/'contracts.json',dict(schema_version=1,awards_acceptance=False,canonical_obligations=376,tasks=tasks,evidence=evidence,cutoff='2026-10-07T15:59:59Z'))
    write(base/'plan-review.json',dict(status='pass',evidence=evidence+[ref(base/'contracts.json','Three independent packets')],findings=['Publication,attention discovery and installer inspection are independent.','No metadata-only technical claims or downloaded code execution.','All150original nonpassing obligations remain governed by original receipts; no acceptance counts change.']))
    (base/'prior-pointer.json').write_bytes(POINTER.read_bytes());POINTER.write_text(json.dumps(dict(contracts=ref(base/'contracts.json','Current reviewed batch'),predecessor=ref(base/'plan-review.json','Reviewed independent dispatch'),awards_acceptance=False),indent=2)+'\n')
    print(json.dumps(view(load(ROOT,base))))

if __name__=='__main__':main()
