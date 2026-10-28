"""Verify selected server originals and close only the finite review packet."""
import hashlib,json
from pathlib import Path
from run_followup_program_20261028 import ROOT,append,load
from run_followup_program_v2_20261028 import selected
from prepare_followup_program_20261028 import ref,write

def main():
    base=selected();key='L6.LOCALPROFILE';assert load(ROOT,base)['active']==key
    plan=json.loads((base/'selected-server-originals.json').read_text())
    assert plan['date']<='2026-10-07T15:59:59Z'
    spans=[
      [(1,21,'Selected server MIT notice; model and transitive component rights remain separate')],
      [(1,93,'Module, Go directive and declared dependency versions; not a resolved reproducible build')],
      [(1,3,'Version variable is a placeholder, not a verified release version')],
      [(60,112,'Generate request separates model, prompt, format and memory-residency keep_alive'),(135,163,'Chat request carries messages, format, tools and keep_alive'),(524,546,'Response distinguishes requested model, remote host/model, done and done_reason')],
      [(233,273,'Selected model and runner resolve before capabilities/options'),(743,803,'Generate forwards request context and format; parser error cancels context without establishing actual runtime cancellation'),(2524,2570,'Streaming error before output sets status; after output writes error object; EOF/write errors end stream'),(3000,3099,'Unload can return done true; remote model branch forwards requests and annotates remote host/model')],
      [(378,454,'Finished requests reduce reference count; keep-alive expiration schedules model unloading; not durable workflow state')],
      [(1,57,'Distinct local/cloud APIs; local server may use cloud models; API is not strictly versioned')],
      [(1,34,'Selected endpoints default to NDJSON; terminal done and nonstream option described')],
      [(1,36,'Midstream errors use error objects and cannot change the already-started HTTP status')],
      [(1,57,'Local API lacks authentication; direct cloud needs credentials; local endpoint can forward cloud inference')],
      [(50,120,'Model blueprint can select base weights and overrides template/parameters'),(180,192,'SYSTEM sets prompt; LICENSE declares distribution text without independently establishing rights')],
    ]
    sources=[]
    for req,anchors in zip(plan['requests'],spans,strict=True):
        p=ROOT/'docs/literature/raw'/(req['id']+'.txt');rp=p.with_suffix('.receipt.json');receipt=json.loads(rp.read_text());data=p.read_bytes()
        assert receipt['status']=='saved' and receipt['url']==req['url'] and receipt['sha256']==hashlib.sha256(data).hexdigest()
        blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest();assert blob==req['git_blob_sha1']
        lines=data.decode().splitlines();inspected=[]
        for lo,hi,claim in anchors:
            assert 0<lo<=hi<=len(lines),(p,lo,hi,len(lines))
            inspected.append(dict(lines=[lo,hi],excerpt_sha256=hashlib.sha256('\n'.join(lines[lo-1:hi]).encode()).hexdigest(),finding=claim))
        sources.append(dict(source_identity=req['url'],version_date=plan['date']+';'+plan['commit'],upstream_path=req['upstream_path'],local_copy=ref(p,'Exact inspected original'),acquisition_receipt=ref(rp,'Fixed collector receipt'),git_blob_sha1=blob,inspected_anchors=inspected,supported_claims=[a['finding'] for a in inspected],native_execution=False))
    out=base/'local-profile.json'
    write(out,dict(status='performed_selected_source_review',sources=sources,client_identity='ollama-python 8785556559ec1d045d27a1ba9d9cc7330c3d3cb1; prior source review',server_identity=plan['commit'],server_release_version='Not established by placeholder Version=0.0.0',model_identity=None,model_rights=None,findings=['Local URL is insufficient evidence of local inference; bind remote-host/model disposition.','HTTP success and partial text cannot establish terminal success; inspect complete stream and error events.','done=true alone admits unload responses; scientific admission additionally needs a recognized inference stop and validated identified result.','keep_alive governs model residency, not conversation custody or transaction completion.','Format is forwarded into a runner; universal schema conformance is not established by this path.'],reuse_decision='Conditional thin server adapter, with pinned build/model/runner and terminal-event contracts; no wholesale adoption or port now.',remaining=['Exact binary build, dependency closure, runner and platform identities.','Selected model manifest, weight hashes, tokenizer/template, quantization and separate redistribution/use terms.','Native terminal/error/cancellation and schema fixtures; authenticated deployment and routing review.','Hosted entitlement, limits and costs where a remote branch is chosen.'],evidence=[ref(base/'selected-server-originals.json','Cutoff original selection'),ref(base/'local-server-acquisition-plan.json','Bounded acquisition plan'),ref(Path(__file__),'Review and custody checks')],full_L6_coverage='inconclusive',native_execution=False))
    receipt=base/'local-profile-receipt.json'
    write(receipt,dict(task=key,awards_acceptance=False,execution='performed',outcome='pass',outputs=[ref(out,'Selected server profile and explicit model unknowns')],evidence=[ref(base/'selected-server-originals.json','Exact original identities')],criteria=[dict(index=0,verdict='pass',finding='Eleven originals match SHA256, Git blobs and cutoff; client/server/model identities remain separate.'),dict(index=1,verdict='pass',finding='Anchored routing, streaming, residency, version and rights findings recorded; runtime and model unknowns remain explicit.')],next_action='Integrate CDT and server findings in a preserving reader/sponsor publication; refresh current program and dispatch independent remaining source work.'))
    append('record',key,str(receipt.relative_to(ROOT)),ROOT,base)
    print(json.dumps(dict(originals=len(sources),packet='completed',full_L6_coverage='inconclusive',next_action='Preserving publication and next independent source packets')))

if __name__=='__main__':main()
