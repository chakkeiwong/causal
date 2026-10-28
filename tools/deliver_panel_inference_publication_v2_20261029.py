"""Scoped delivery with explicit Git/LFS hashes, no global clean-filter comparison."""
import hashlib,json,re,subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import deliver_panel_inference_publication_20261029 as prior
import recover_fixture_java_delivery_20261028 as delivery
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write

ROOT=prior.ROOT;DAY=prior.DAY;BASE=DAY/'panel-inference-delivery-v2';PARENT=prior.PARENT
rel=lambda p:str(p.relative_to(ROOT))
READ={};AUTH=set()


def bytes_cached(p):
    if p not in READ:READ[p]=(ROOT/p).read_bytes()
    return READ[p]


def bindings(value):
    if isinstance(value,dict):
        local=value.get('local_copy',value.get('local_path'));sha=value.get('sha256')
        if isinstance(local,dict):sha=local.get('sha256',sha);local=local.get('path')
        blob=value.get('verified_git_blob',value.get('git_blob',value.get('git_blob_sha1')))
        foreign=isinstance(local,str) and isinstance(blob,str) and bool(re.fullmatch('[0-9a-f]{40}',blob))
        if foreign:
            key=(local,sha,blob,json.dumps(value.get('decoded'),sort_keys=True))
            if key not in AUTH:
                assert local.startswith(('docs/','tools/','tests/')) and '..' not in Path(local).parts
                data=bytes_cached(local);assert hashlib.sha256(data).hexdigest()==sha
                decoded=value.get('decoded')
                if isinstance(decoded,dict):
                    import base64
                    target=decoded['path'];dd=bytes_cached(target);assert hashlib.sha256(dd).hexdigest()==decoded['sha256']
                    envelope=json.loads(data);assert envelope.get('encoding')=='base64' and envelope.get('sha')==blob
                    assert base64.b64decode(envelope['content'])==dd;data=dd
                assert hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()==blob
                AUTH.add(key)
            yield local
            if isinstance(value.get('decoded'),dict):yield value['decoded']['path']
        for k in ['path','log']:
            if foreign and k=='path':continue
            p=value.get(k)
            if isinstance(p,str) and p.startswith(('docs/','tools/','tests/')) and '..' not in Path(p).parts and (k=='log' or value.get('sha256')):yield p
        for v in value.values():yield from bindings(v)
    elif isinstance(value,list):
        for v in value:yield from bindings(v)


def index():
    result={}
    for row in subprocess.check_output(['git','ls-files','--stage','-z'],cwd=ROOT).decode().split(chr(0)):
        if row:
            meta,p=row.split(chr(9),1);mode,sha,stage=meta.split();assert stage=='0';result[p]=sha
    return result


def hash_pair(path):
    f=ROOT/path;size=f.stat().st_size;sha1=hashlib.sha1(b'blob '+str(size).encode()+bytes([0]));sha256=hashlib.sha256()
    with f.open('rb') as stream:
        for chunk in iter(lambda:stream.read(4*1024*1024),b''):sha1.update(chunk);sha256.update(chunk)
    digest=sha256.hexdigest()
    if f.suffix.lower() in {'.pdf','.zip','.npy','.npz','.png','.jpg','.jpeg'}:
        pointer=('version https://git-lfs.github.com/spec/v1\noid sha256:'+digest+'\nsize '+str(size)+'\n').encode()
        expected=hashlib.sha1(b'blob '+str(len(pointer)).encode()+bytes([0])+pointer).hexdigest()
    else:expected=sha1.hexdigest()
    return path,expected,digest


def prepare():
    assert not BASE.exists()
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==PARENT
    assert not subprocess.check_output(['git','diff','--cached','--name-only'],cwd=ROOT).strip()
    seeds={'docs/program/state.json','docs/program/execution/followup-current.json','docs/program/execution/continuation-current.json','docs/program/execution/current-program.md','docs/program/master-live.md','docs/mission-control.md','docs/mission-control.html','docs/literature/fetch-manifest.json',rel(Path(__file__))}
    for pattern in ['docs/program/execution/2026-10-29','tools/*panel*inference*20261029.py','tools/panel_runtime*20261029.*','docs/literature/raw/exec29_panel_*','docs/literature/raw/exec29_runtime_*','docs/literature/raw/exec29_dispatch_*','docs/literature/raw/exec29_rstats_*','docs/causal_proposal_panel_inference_reviewed_v1_2026-10-29.*','docs/sponsor_proposal_panel_inference_reviewed_v1_2026-10-29.pdf','docs/program/execution/2026-10-28/panel-estimator-delivery-v1']:
        for p in ROOT.glob(pattern):
            seeds.update(rel(f) for f in (p.rglob('*') if p.is_dir() else [p]) if f.is_file() and '__pycache__' not in f.parts)
    queue=[p for p in seeds if p.endswith(('.json','.jsonl'))];seen=set(queue);bound=set()
    while queue:
        p=queue.pop()
        try:
            content=(ROOT/p).read_text();values=[json.loads(x) for x in content.splitlines() if x.strip()] if p.endswith('.jsonl') else [json.loads(content)]
        except (ValueError,UnicodeError):continue
        for value in values:
            for q in bindings(value):
                assert (ROOT/q).is_file();bound.add(q)
                if q.endswith(('.json','.jsonl')) and q not in seen:seen.add(q);queue.append(q)
    READ.clear();idx=index();paths=sorted(seeds|bound)
    BASE.mkdir();write(BASE/'custody-paths.json',dict(paths=paths,bound_paths=len(bound),traversed_documents=len(seen)))
    print(json.dumps(dict(phase='direct_hash_comparison',paths=len(paths))),flush=True)
    hashes={};changed=set()
    with ThreadPoolExecutor(max_workers=4) as pool:
        for i,(p,h,sha256) in enumerate(pool.map(hash_pair,paths)):
            hashes[p]=sha256
            if idx.get(p)!=h:changed.add(p)
            if (i+1)%5000==0:print(json.dumps(dict(hashed=i+1,changed=len(changed))),flush=True)
    selected=seeds|changed
    write(BASE/'delivery-plan.json',dict(status='reviewed_direct_hash_custody',parent=PARENT,
        paths=[dict(path=p,sha256=hashes[p],anchor='Exact scoped delivery bytes') for p in sorted(selected)],
        bound_paths=len(bound),traversed_documents=len(seen),changed_bound_paths=len(changed&bound),
        evidence=[ref(DAY/'followup-runtime-v14/publication-receipt.json','Completed publication'),ref(DAY/'panel-inference-delivery-v1/prepare-failure.json','Preserved LFS comparison failure'),ref(BASE/'custody-paths.json','Complete traversed scope')],
        method='Direct streaming SHA1 for ordinary Git blobs; canonical LFS pointer SHA1 from full SHA256 and size; no clean filters invoked.',visual_acceptance=False,final_acceptance=False))
    print(json.dumps(dict(prepared=rel(BASE),paths=len(selected),bound_paths=len(bound))),flush=True)


def deliver():
    plan=json.loads((BASE/'delivery-plan.json').read_text());verify_bindings(plan)
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==PARENT
    assert not subprocess.check_output(['git','diff','--cached','--name-only'],cwd=ROOT).strip()
    delivery.BASE=BASE
    delivery.step('stage-publication',['git','add','-f','--',rel(BASE),*[p['path'] for p in plan['paths']]])
    delivery.step('authored-whitespace-check',['git','diff','--cached','--check','--','tools','docs/program/master-live.md','docs/program/execution/current-program.md','docs/mission-control.md'])
    staged=set(subprocess.check_output(['git','diff','--cached','--name-only','-z'],cwd=ROOT).decode().split(chr(0)))-{''}
    allowed={p['path'] for p in plan['paths']}|{rel(p) for p in BASE.iterdir() if p.is_file()}
    assert staged<=allowed
    idx=index()
    for p,expected,_ in map(hash_pair,sorted(staged)):assert idx[p]==expected,p
    write(BASE/'staged-review.json',dict(status='pass',staged_count=len(staged),exact_worktree_versions=True,evidence=[ref(BASE/'delivery-plan.json','Complete scoped custody')]))
    delivery.step('stage-delivery-records',['git','add','-f','--',rel(BASE)])
    delivery.step('git-commit',['git','-c','user.name=Codex','-c','user.email=codex@users.noreply.github.com','commit','-m','Recover panel inference reviews and preserve uncertainty and cluster target contracts'])
    delivery.step('git-push',['git','push'])
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();remote=subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT,text=True).strip();assert head==remote
    write(BASE/'push-verification.json',dict(status='pass',commit=head,origin_main=remote,visual_acceptance=False,final_acceptance=False))
    print(json.dumps(dict(pushed=head)),flush=True)


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','deliver']);globals()[p.parse_args().command]()
