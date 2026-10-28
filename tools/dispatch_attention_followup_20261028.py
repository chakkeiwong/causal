"""Dispatch independent attention publication and selected delegate reviews."""
import json
from run_followup_program_20261028 import ROOT,load,view
from run_followup_program_v2_20261028 import selected,POINTER
from prepare_followup_program_20261028 import ref,write


def main():
    prior=selected();assert all(v=='completed' for v in load(ROOT,prior)['states'].values())
    base=prior.parent/'followup-runtime-v5';assert not base.exists();base.mkdir()
    specs=[
      ('ATTENTION.PUBLICATION','Publish the reviewed attention/source comparison with the exact permutation witness; pair preserving reader/sponsor and renew unchanged checks.',
       ['All1423reader and1080sponsor prior records and contexts retained; seven additions have complete source custody.','Paired publication,exact examples,text bounds and both unchanged controllers pass; full coverage and visual acceptance remain open.'],'publication.json'),
      ('TCDF.DELEGATE','Inspect the pinned TCDF depthwise source and derive an independent temporal-window oracle without executing acquired code.',
       ['Exact source identity,hash,blob and inspected causal-padding/dilation anchors recorded.','Boundary/lag fixture expectations and unsupported/native limits explicit.'],'tcdf-delegate.json'),
      ('TACD.PROTOCOL','Inspect pinned configuration,scoring,data and main delegates to determine truth access,split settings and proposed held-out protocol.',
       ['All selected original delegates verified and inspected against exact entrypoint branches.','Actual defaults separated from alternatives; complete invalid-result and graph/time split protocol specified without native execution.'],'tacd-protocol.json'),
      ('ATTENTION.ORIGINALS','Resolve finite omitted primary-paper routes and the newly discovered graph-attention preprint identity using bounded permitted acquisition.',
       ['Named original candidates have edition-specific acquired PDFs or precise local access limits.','Technical claims require inspected originals; search metadata and unmatched editions cannot close scholarly coverage.'],'attention-originals.json'),
    ]
    evidence=[ref(prior/n,'Completed recovered review') for n in ['contracts.json','attention-search.json','cdt-installer.json']]
    write(base/'contracts.json',dict(schema_version=1,awards_acceptance=False,canonical_obligations=376,
        tasks=[dict(id=k,depends=[],scope='Finite proposal author work; no original acceptance awarded',action=a,acceptance=c,outputs=[str((base/o).relative_to(ROOT))],owner='Current author/coordinator') for k,a,c,o in specs],evidence=evidence,cutoff='2026-10-07T15:59:59Z'))
    write(base/'plan-review.json',dict(status='pass',evidence=evidence+[ref(base/'contracts.json','Independent bounded contracts')],findings=['No branch has an unnecessary dependency on unavailable originals.','No native execution,bank truth or new source rights inferred.','Publication is gated only by verified prior delivery; source reviews continue independently.']))
    (base/'prior-pointer.json').write_bytes(POINTER.read_bytes())
    POINTER.write_text(json.dumps(dict(contracts=ref(base/'contracts.json','Current reviewed batch'),predecessor=ref(base/'plan-review.json','Reviewed dispatch'),awards_acceptance=False),indent=2)+'\n')
    print(json.dumps(view(load(ROOT,base))))


if __name__=='__main__':main()
