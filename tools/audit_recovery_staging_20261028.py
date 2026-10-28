"""Ensure staged evidence includes transitive local bindings and exact worktree bytes."""
import argparse
import json
from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parents[1]


def bindings(value):
    if isinstance(value,dict):
        for key in ['path','log']:
            p=value.get(key)
            if isinstance(p,str) and p.startswith(('docs/','tools/')) and '..' not in Path(p).parts and (key=='log' or value.get('sha256')):
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
    queue=[p for p in staged if p.endswith(('.json','.jsonl'))];seen=set();bound=set();missing=set()
    while queue:
        p=queue.pop()
        if p in seen:continue
        seen.add(p);f=ROOT/p
        if not f.is_file():continue
        try:
            values=[json.loads(x) for x in f.read_text().splitlines() if x.strip()] if f.suffix=='.jsonl' else [json.loads(f.read_text())]
        except (ValueError,UnicodeError):continue
        for v in values:
            for q in bindings(v):
                if not (ROOT/q).is_file():missing.add(q);continue
                bound.add(q)
                if q.endswith(('.json','.jsonl')) and q not in seen:queue.append(q)
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
                historical_logs_not_selected_without_evidence_binding=True)
    out.write_text(json.dumps(report,indent=2)+chr(10))
    subprocess.run(['git','add','-f','--',str(out.relative_to(ROOT)),str(Path(__file__).relative_to(ROOT)),*added],cwd=ROOT,check=True)
    print(json.dumps(dict(status='pass',traversed_json=len(seen),bound_paths=len(paths),added=len(added))))


if __name__=='__main__':main()
