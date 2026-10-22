#!/usr/bin/env python3
"""Verify recursively bound evidence in the Git index, including PDF LFS objects."""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-22/program-refresh-observations-v1'

def main():
    seeds=[BASE/'verification.json',BASE/'program-review.json',
        ROOT/'docs/program/execution/2026-10-22/observations-commercial-v1/publication-v2/working-release.json',
        ROOT/'docs/program/execution/2026-10-22/sponsor-observations-v1/working-release.json',
        ROOT/'docs/program/execution/2026-10-22/python-iv-rd-preflight-v2/source-audit.json']
    wanted={};seen=set();pending=list(seeds);conflicts=[]
    def visit(o):
        if isinstance(o,dict):
            if 'path' in o and 'sha256' in o:
                path=o['path'];digest=o['sha256']
                if path in wanted and wanted[path]!=digest:conflicts.append(path)
                wanted[path]=digest
                if path.endswith('.json'):pending.append(ROOT/path)
            for v in o.values():visit(v)
        elif isinstance(o,list):
            for v in o:visit(v)
    while pending:
        p=pending.pop()
        if p in seen:continue
        seen.add(p)
        if p.is_file():visit(json.loads(p.read_text()))
    assert not conflicts,conflicts
    index={}
    for row in subprocess.check_output(['git','ls-files','--stage','-z'],cwd=ROOT).split(b'\0'):
        if not row:continue
        meta,path=row.split(b'\t',1);mode,sha,stage=meta.split();assert stage==b'0'
        index[path.decode()]=sha.decode()
    gitdir=Path(subprocess.check_output(['git','rev-parse','--git-common-dir'],cwd=ROOT,text=True).strip())
    if not gitdir.is_absolute():gitdir=ROOT/gitdir
    missing=[];mismatch=[];pointers={};direct=0
    for path,expected in wanted.items():
        if path not in index:missing.append(path);continue
        b=(ROOT/path).read_bytes();actual=hashlib.sha256(b).hexdigest()
        if actual!=expected:mismatch.append(dict(path=path,reason='working bytes differ from bound SHA256'));continue
        blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
        if blob==index[path]:direct+=1
        else:pointers[path]=(index[path],actual,len(b))
    unique=sorted({v[0] for v in pointers.values()})
    raw=subprocess.run(['git','cat-file','--batch'],cwd=ROOT,input=('\n'.join(unique)+'\n').encode(),stdout=subprocess.PIPE,check=True).stdout if unique else b''
    objects={};offset=0
    for sha in unique:
        end=raw.index(b'\n',offset);head=raw[offset:end].split();assert head[0].decode()==sha and head[1]==b'blob'
        size=int(head[2]);offset=end+1;objects[sha]=raw[offset:offset+size];offset+=size+1
    lfs=0
    for path,(oid,digest,size) in pointers.items():
        body=objects[oid].decode(errors='replace')
        required=['version https://git-lfs.github.com/spec/v1','oid sha256:'+digest,'size '+str(size)]
        if body.splitlines()!=required:mismatch.append(dict(path=path,reason='index differs and is not matching LFS pointer'));continue
        obj=gitdir/'lfs/objects'/digest[:2]/digest[2:4]/digest
        if not obj.exists() or obj.stat().st_size!=size or hashlib.sha256(obj.read_bytes()).hexdigest()!=digest:
            mismatch.append(dict(path=path,reason='LFS object missing or mismatched'));continue
        lfs+=1
    result=dict(status='pass' if not missing and not mismatch else 'fail',bound_paths=len(wanted),direct_git_blobs=direct,
        lfs_pointers_verified=lfs,missing=missing,mismatch=mismatch,
        method='Ordinary index Git blobs verified against exact bytes; PDF LFS pointer hashes/sizes and local objects verified.')
    target=BASE/'staged-binding-review.json';assert not target.exists();target.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result));assert result['status']=='pass'

if __name__=='__main__':main()
