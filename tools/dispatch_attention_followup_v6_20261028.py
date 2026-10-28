"""Dispatch the next independent research and public-fixture work packets."""
import json
from pathlib import Path
from run_followup_program_20261028 import ROOT,load,view
from run_followup_program_v2_20261028 import selected,POINTER
from prepare_followup_program_20261028 import ref,write


def main():
    prior=selected();assert all(v=='completed' for v in load(ROOT,prior)['states'].values())
    base=prior.parent/'followup-runtime-v6';assert not base.exists();base.mkdir()
    specs=[
      ('ATTENTION.PROTOCOL','Integrate exact TCDF temporal-support, TACD truth/split/device/scoring and empty-denominator findings into a preserving paired reader and sponsor successor.',
       ['All1430 prior reader and1089 sponsor records/content/contexts preserved; new source delegates and authored reference are traceable.','Exact protocol distinctions, text bounds and both unchanged controllers pass; no native or full-coverage acceptance.'],'publication.json'),
      ('ATTENTION.FIXTURE','Implement and run proposal-owned synthetic fixtures for training/validation/evaluation identity, truth withholding, empty denominators, threshold ties and lag support.',
       ['Fixture functions cannot use held-out truth during threshold selection and report zero-valid denominators as unavailable.','Known synthetic output matches exact source-free expectations; third-party/native claims remain excluded.'],'public-fixture.json'),
      ('PYTHON.DISCOVERY.DELTA','Compare the completed RL/attention family routes and all new exact originals against the historical Python IID omission register; preserve every uninspected family and candidate limit.',
       ['Each of the historical essential omission groups is reconciled with exact later source evidence, or retains its precise route.','Metadata leads are not technical evidence; the broad Python cell remains inconclusive unless its exact contract is met.'],'python-discovery-delta.json'),
      ('ATTENTION.PAPER.IDENTITY','Run a finite metadata-first identity search for the selected CausalTransformer and CAMCNs scholarly works, then acquire only version-matched originals on permitted hosts.',
       ['Exact title/author/edition routes, query counts and collector results are recorded.','No README, metadata, source-code repository or unmatched version substitutes for a scholarly primary PDF.'],'paper-identity.json'),
    ]
    evidence=[ref(prior/n,'Completed verified source and publication packet') for n in ['contracts.json','attention-originals.json','tcdf-delegate.json','tacd-protocol.json','publication.json']]
    write(base/'contracts.json',dict(schema_version=1,awards_acceptance=False,canonical_obligations=376,
       tasks=[dict(id=k,depends=[],scope='Finite proposal author work; no original acceptance awarded',action=a,acceptance=c,outputs=[str((base/o).relative_to(ROOT))],owner='Current author/coordinator') for k,a,c,o in specs],
       evidence=evidence,cutoff='2026-10-07T15:59:59Z'))
    write(base/'plan-review.json',dict(status='pass',evidence=evidence+[ref(base/'contracts.json','Reviewed independent work packets')],
       findings=['The four tasks have no mutual dependencies; a scholarly access limit cannot stop source integration or synthetic contract fixtures.','Existing publisher/rate-limit failures are preserved; no unchanged retry is included.','The new packet does not modify the original 376-operation acceptance ledger.']))
    (base/'prior-pointer.json').write_bytes(POINTER.read_bytes())
    POINTER.write_text(json.dumps(dict(contracts=ref(base/'contracts.json','Current reviewed batch'),predecessor=ref(base/'plan-review.json','Independent continuation plan'),awards_acceptance=False),indent=2)+'\n')
    print(json.dumps(view(load(ROOT,base))))


if __name__=='__main__':main()
