"""Ensure staged evidence includes transitive local bindings and exact worktree bytes."""
import argparse
import base64
import hashlib
import re
import json
from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parents[1]


def bindings(value):
    if isinstance(value,dict):
        foreign=False
        local=value.get('local_copy',value.get('local_path'))
        local_sha=value.get('sha256')
        if isinstance(local,dict):
            local_sha=local.get('sha256',local_sha)
            local=local.get('path')
        blob=value.get('verified_git_blob',value.get('git_blob',value.get('git_blob_sha1')))
        if isinstance(local,str) and isinstance(blob,str) and re.fullmatch(r'[0-9a-f]{40}',blob):
            assert local.startswith(('docs/','tools/','tests/')) and '..' not in Path(local).parts
            data=(ROOT/local).read_bytes()
            assert hashlib.sha256(data).hexdigest()==local_sha, ('Local SHA-256 mismatch',local,local_sha)
            decoded=value.get('decoded')
            if isinstance(decoded,dict):
                decoded_path=decoded['path']
                assert decoded_path.startswith(('docs/','tools/','tests/')) and '..' not in Path(decoded_path).parts
                decoded_data=(ROOT/decoded_path).read_bytes()
                assert hashlib.sha256(decoded_data).hexdigest()==decoded['sha256'], ('Decoded SHA-256 mismatch',decoded_path)
                envelope=json.loads(data)
                assert envelope.get('encoding')=='base64' and envelope.get('sha')==blob
                assert base64.b64decode(envelope['content'])==decoded_data, ('Decoded API bytes mismatch',local,decoded_path)
                data=decoded_data
                yield decoded_path
            assert hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()==blob, ('Git blob mismatch',local,value.get('path'),blob,hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest())
            foreign=True
            yield local
        for key in ['path','log']:
            if foreign and key=='path':continue
            p=value.get(key)
            if isinstance(p,str) and p.startswith(('docs/','tools/','tests/')) and '..' not in Path(p).parts and (key=='log' or value.get('sha256')):
                yield p
        for v in value.values():yield from bindings(v)
    elif isinstance(value,list):
        for v in value:yield from bindings(v)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('directory');a=parser.parse_args()
    base=ROOT/a.directory
    assert base.is_relative_to(ROOT/'docs/program/execution') and base.is_dir()
    out=base/'evidence-staging-review.json';assert not out.exists()
    staged=subprocess.check_output(['git','diff','--cached','--name-only','-z'],cwd=ROOT).decode().split(chr(0))
    queue=list(dict.fromkeys(p for p in staged if p.endswith(('.json','.jsonl'))));queued=set(queue);seen=set();bound=set();missing=set()
    while queue:
        p=queue.pop()
        if p in seen:continue
        seen.add(p);f=ROOT/p
        if len(seen)%500==0:
            print(json.dumps(dict(progress='custody_scan',traversed=len(seen),pending=len(queue),bound_paths=len(bound))),flush=True)
        if not f.is_file():continue
        try:
            values=[json.loads(x) for x in f.read_text().splitlines() if x.strip()] if f.suffix=='.jsonl' else [json.loads(f.read_text())]
        except (ValueError,UnicodeError):continue
        for v in values:
            for q in bindings(v):
                if not (ROOT/q).is_file():missing.add(q);continue
                bound.add(q)
                if q.endswith(('.json','.jsonl')) and q not in queued:
                    queue.append(q);queued.add(q)
    assert not missing,sorted(missing)[:10]
    index={}
    for row in subprocess.check_output(['git','ls-files','--stage','-z'],cwd=ROOT).decode().split(chr(0)):
        if row:
            meta,p=row.split(chr(9),1);mode,sha,stage=meta.split();assert stage=='0';index[p]=sha
    paths=sorted(bound)
    hashes=subprocess.check_output(['git','hash-object','--stdin-paths'],cwd=ROOT,input=(chr(10).join(paths)+chr(10)).encode()).decode().splitlines() if paths else []
    assert len(hashes)==len(paths)
    added=[p for p,h in zip(paths,hashes) if index.get(p)!=h]
    report=dict(status='pass',scope='Transitive staged evidence custody; content and full-byte bindings validated separately by both controllers',
                traversed_json=len(seen),bound_paths=len(paths),added_exact_worktree_versions=added,missing=[],
                historical_logs_not_selected_without_evidence_binding=True,
                upstream_path_policy='A foreign path is excluded only after explicit local-copy SHA-256 and Git-blob verification.')
    out.write_text(json.dumps(report,indent=2)+chr(10))
    subprocess.run(['git','add','-f','--',str(out.relative_to(ROOT)),str(Path(__file__).relative_to(ROOT)),*added],cwd=ROOT,check=True)
    print(json.dumps(dict(status='pass',traversed_json=len(seen),bound_paths=len(paths),added=len(added))))


if __name__=='__main__':main()
