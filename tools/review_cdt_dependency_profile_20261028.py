"""Trace declared CDT dependency constraints and specify public admission fixtures."""
import hashlib,json
from pathlib import Path
from run_followup_program_20261028 import ROOT,append,load,bound
from run_followup_program_v2_20261028 import selected
from prepare_followup_program_20261028 import ref,write

def main():
    base=selected();key='CDT.DEPENDENCIES';assert load(ROOT,base)['next']==key
    evidence=[ref(base/'source-acquisition-plan.json','Selected pinned manifests'),ref(base/'cdt-dependency-extra-plan.json','Additional distribution and interpreter originals'),ref(base.parent/'followup-runtime-v2/cdt-delegates.json','Prior delegate trace')]
    start=base/'cdt-dependencies-start.json';write(start,dict(task=key,awards_acceptance=False,next_action='Distinguish declared constraints from a resolved dependency environment; specify public fixtures.',evidence=evidence));append('start',key,str(start.relative_to(ROOT)),ROOT,base)
    plan=json.loads((base/'source-acquisition-plan.json').read_text());records=[]
    claims=['Eleven Python names without version constraints,including torch; setup install_requires differs.','Eight R package names without version constraints; no R interpreter or resolved package versions.','Container uses mutable cdt-base:latest and unpinned installation commands; source text is not a reproducible image identity.','Environment recipe names tag1.0 and installs sparsebn from a repository without a version pin; base/image contents unresolved.']
    for req,claim in zip([r for r in plan['requests'] if 'cdt_deps' in r['id']],claims,strict=True):
        p=ROOT/'docs/literature/raw'/(req['id']+'.txt');rp=p.with_suffix('.receipt.json');r=json.loads(rp.read_text());data=p.read_bytes();assert r['status']=='saved' and r['url']==req['url'] and r['sha256']==hashlib.sha256(data).hexdigest()
        blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest();assert blob==req['git_blob_sha1']
        records.append(dict(source_identity=req['url'],version_date='2025-10-13;ff46dbca3d91f2dba30e6ae54986eea30c9b331f',upstream_path=req['upstream_path'],local_copy=ref(p,'Inspected complete manifest'),acquisition_receipt=ref(rp,'Fixed collector receipt'),git_blob_sha1=blob,inspected_anchors=[dict(lines=[1,len(data.decode().splitlines())],finding=claim)],supported_claims=[claim],native_execution=False))
    extra=json.loads((base/'cdt-dependency-extra-plan.json').read_text())
    extra_claims=['Container requirements are unpinned and omit torch,which Dockerfile installs separately.','Base recipe uses untagged ubuntu and delegates install-dependencies.sh; that script and image closure remain separate uninspected inputs.','Nvidia-named recipe uses mutable nv-cdt-base:latest while its shown torch index is CPU; no actual GPU runtime capability inferred.','Settings defaults to Rscript resolved from environment and allows override; changing rpath resets availability cache.','Availability template calls library(package) only; no version or rights query.']
    for req,claim in zip(extra['requests'],extra_claims,strict=True):
        p=ROOT/'docs/literature/raw'/(req['id']+'.txt');rp=p.with_suffix('.receipt.json');r=json.loads(rp.read_text());data=p.read_bytes();assert r['status']=='saved' and r['url']==req['url'] and r['sha256']==hashlib.sha256(data).hexdigest()
        blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest();assert blob==req['git_blob_sha1']
        spans=[70,133] if req['upstream_path'].endswith('Settings.py') else [1,len(data.decode().splitlines())]
        records.append(dict(source_identity=req['url'],version_date='2025-10-13;ff46dbca3d91f2dba30e6ae54986eea30c9b331f',upstream_path=req['upstream_path'],local_copy=ref(p,'Inspected selected distribution source'),acquisition_receipt=ref(rp,'Fixed collector receipt'),git_blob_sha1=blob,inspected_anchors=[dict(lines=spans,finding=claim)],supported_claims=[claim],native_execution=False))
    prior=json.loads((ROOT/'docs/program/execution/2026-10-13/python-discovery/source-audit.json').read_text())
    cdt=next(s for s in prior['sources'] if s['integrated_citation_key']=='exec13_pydisc_cdt')
    setup=next(r for r in cdt['records'] if r['local_copy']['path'].endswith('source_5.txt'));bound(ROOT,setup['local_copy'])
    records.append(dict(source_identity=setup['source_identity'],version_date=cdt['version_date'],local_copy=setup['local_copy'],inspected_anchors=[dict(lines=[15,30],finding='setup declares CDT0.6.0 and unpinned install_requires; skrebate appears here while torch appears in requirements; Apache2 metadata differs from selected MIT root')],supported_claims=['Neither selected dependency entrypoint locks interpreter or transitive packages.','Different selected dependency lists must be reconciled for the actual distribution route.'],native_execution=False))
    fixtures=[
      dict(id='identity',input='Selected source commit plus declared Python/R/binary/container route',expected='Record resolved versions,binary/image hashes,platform and separate terms before enablement'),
      dict(id='permutation',input='Public two/three-variable data in several column orders; apply same permutations to labels and constraints',expected='Inverse-permuted output has identical named endpoints and preserves declared ambiguous-edge encoding'),
      dict(id='score',input='Declared Gaussian versus categorical data and explicit intervention targets',expected='Reject unsupported likelihood/data combinations; bind actual score constructor and intervention row mapping'),
      dict(id='failure',input='Controlled child exits nonzero with absent,partial or stale CSV',expected='Never parse stale output as success; bind exitcode and attempt identity'),
      dict(id='stderr_cancel',input='Controlled large stderr and interrupted child',expected='Bound timeout and child cleanup; retain complete diagnostic/attempt accounting'),
      dict(id='numeric',input='Generated collinear,constant and nonfinite columns plus ambiguous graph endpoints',expected='Explicit validation/refusal or declared handling; no silent zero/imputed success'),
    ]
    out=base/'cdt-dependencies.json';write(out,dict(status='performed_declared_profile_review',source_records=records,selected_cdt_commit='ff46dbca3d91f2dba30e6ae54986eea30c9b331f',resolved_environment=None,rights='MIT root and Apache2 setup declarations remain inconsistent; selected component/dependency terms must be resolved before redistribution.',findings=claims,public_fixture_protocol=fixtures,remaining=['Actual Python/R versions and transitive dependency resolution for one distribution route','Component/license conflict and complete transitive terms','Native matrix/failure/cancellation conformance before enabling an adapter'],reuse_decision='Keep conditional thin-adapter/direct-R proposal; choose and record a new reproducible profile rather than inventing a historical environment from unpinned manifests.',evidence=evidence+[ref(Path(__file__),'Exact manifest review')],full_python_cell='inconclusive',native_execution=False))
    receipt=base/'cdt-dependencies-receipt.json';write(receipt,dict(task=key,awards_acceptance=False,execution='performed',outcome='pass',outputs=[ref(out,'Declared constraints and six public fixture classes')],evidence=evidence,criteria=[dict(index=0,verdict='pass',finding='Four exact manifests plus existing setup inspected; declared/unpinned versus unresolved environment separated.'),dict(index=1,verdict='pass',finding='Six public fixture classes have explicit expected behavior; versions,rights and native admission remain open.')],next_action='Integrate dependency profile and RL/CORL technical findings in the next preserving publication; retain exact unresolved runtime and coverage boundaries.'))
    append('record',key,str(receipt.relative_to(ROOT)),ROOT,base);print(json.dumps(dict(manifests=len(records),fixtures=len(fixtures),coverage='inconclusive')))

if __name__=='__main__':main()
