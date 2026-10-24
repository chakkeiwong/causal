#!/usr/bin/env python3
"""Stage missing local evidence for an already controller-verified publication.

This checks Git custody, not content correctness. Controller checks retain
full-byte hashing. Upstream repository filenames are not local bindings.
"""
import argparse,json,subprocess
from pathlib import Path
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
    p=argparse.ArgumentParser();p.add_argument('unit');a=p.parse_args()
    assert '/' not in a.unit and '..' not in a.unit
    base=ROOT/'docs/program/execution/2026-10-24'/a.unit
    assert (base/'publication-checkpoint.json').is_file()
    out=base/'evidence-staging-review.json';assert not out.exists()
    def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT).decode().split('\0')
    known=set(git('ls-files','-z'));staged=git('diff','--cached','--name-only','-z')
    seen=set();queue=[p for p in staged if p.endswith(('.json','.jsonl'))];added=set();missing=set()
    while queue:
        path=queue.pop()
        if path in seen:continue
        seen.add(path);f=ROOT/path
        if not f.is_file():continue
        try:
            docs=[json.loads(x) for x in f.read_text().splitlines() if x.strip()] if f.suffix=='.jsonl' else [json.loads(f.read_text())]
        except (ValueError,UnicodeError):continue
        for d in docs:
            for q in bindings(d):
                if not (ROOT/q).is_file():missing.add(q);continue
                if q not in known:
                    added.add(q)
                    if q.endswith(('.json','.jsonl')):queue.append(q)
    added.update(str(p.relative_to(ROOT)) for p in base.glob('*.log'))
    report=dict(status='pass' if not missing else 'fail',scope='Git custody for staged local evidence;full-byte controller verification remains separate',staged_json_count=len(seen),added_evidence=sorted(added),missing=sorted(missing))
    out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='added_evidence'}))
    assert not missing,sorted(missing)[:10]
    subprocess.run(['git','add','-f','--',str(out.relative_to(ROOT)),str(Path(__file__).relative_to(ROOT)),*sorted(added)],cwd=ROOT,check=True)

if __name__=='__main__':main()
