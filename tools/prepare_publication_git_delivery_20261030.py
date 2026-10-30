from pathlib import Path
import collections, hashlib, json, re, subprocess, sys, datetime
R=Path(__file__).resolve().parents[1]
D=R/'docs/program/execution/2026-10-30/publication-git-delivery-001'
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
def paths(data):return {x.decode() for x in data.split(bytes([0])) if x}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,obj):p.write_text(json.dumps(obj,indent=2)+chr(10))
def normalized(value):
    if not isinstance(value,str):return None
    if value.startswith(str(R)+'/'):value=value[len(str(R))+1:]
    if not value.startswith(('docs/','tools/','security/')) and value not in ['CURRENT.md','README.md','.gitignore','.gitattributes']:return None
    if '..' in Path(value).parts or chr(10) in value:return None
    return value if (R/value).is_file() else None
def bound(value):
    if isinstance(value,dict):
        for key,item in value.items():
            p=normalized(key)
            if p and isinstance(item,str) and re.fullmatch('[0-9a-f]{64}',item):yield p
            if key in ['path','local_copy','local_path','log','output','retained_path','snapshot','source','extraction','preview','manifest','record','retained_original']:
                p=normalized(item)
                if p:yield p
            yield from bound(item)
    elif isinstance(value,list):
        for item in value:yield from bound(item)

assert not git('diff','--cached','--name-only').strip(),'Index already contains staged changes'
D.mkdir(parents=True,exist_ok=False)
untracked=paths(git('ls-files','--others','--exclude-standard','-z'))
tracked=paths(git('ls-files','-z'))
changed=paths(git('diff','--name-only','-z'))
ignored_names={'geometry.xml','full-geometry.xml','sponsor-geometry.xml'}
excluded_geometry={p for p in untracked if Path(p).name in ignored_names}
historical_logs={p for p in changed if p.startswith('docs/program/execution/') and Path(p).suffix in ['.log','.jsonl']}
selected=(untracked-excluded_geometry)|(changed-historical_logs)
pending=[p for p in selected if p.endswith(('.json','.jsonl'))];seen=set();referenced=set();parse_errors=[]
while pending:
    name=pending.pop()
    if name in seen:continue
    seen.add(name);p=R/name
    try:
        if p.suffix=='.jsonl':values=(json.loads(line) for line in p.read_text().splitlines() if line.strip())
        else:values=[json.loads(p.read_text())]
        for value in values:
            for target in bound(value):
                referenced.add(target)
                if target not in tracked or target in changed:
                    if target not in selected:selected.add(target)
                    if target.endswith(('.json','.jsonl')) and target not in seen:pending.append(target)
    except (UnicodeError,ValueError) as exc:parse_errors.append({'path':name,'error':str(exc)[:150]})
    if len(seen)%10000==0:print(json.dumps({'phase':'bind_evidence','documents':len(seen),'pending':len(pending),'selected':len(selected)}),flush=True)
# Every frozen package checksum entry must be present, including ignored files.
for listing in (R/'docs/release/2026-10-29/packages').glob('*/SHA256SUMS'):
    selected.add(str(listing.relative_to(R)))
    for line in listing.read_text().splitlines():
        digest,name=line.split('  ',1);p=listing.parent/name
        assert p.is_file(),str(p)
        selected.add(str(p.relative_to(R)))
for mp in (R/'docs/release/2026-10-29/numerical-packages').glob('*/manifest.json'):
    for name in json.loads(mp.read_text()).get('files',{}):
        p=mp.parent/name;assert p.is_file(),str(p);selected.add(str(p.relative_to(R)))
selected={p for p in selected if p not in tracked or p in changed}
excluded_geometry-=selected;historical_logs-=selected
rows=[];total=0
for i,name in enumerate(sorted(selected)):
    p=R/name;size=p.stat().st_size;total+=size;rows.append({'path':name,'bytes':size,'sha256':sha(p)})
    if (i+1)%25000==0:print(json.dumps({'phase':'hash_scope','files':i+1,'total':len(selected)}),flush=True)
save(D/'delivery-plan.json',{'schema_version':1,'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'parent_commit':git('rev-parse','HEAD').decode().strip(),'branch':git('branch','--show-current').decode().strip(),'status':'prepared','scope':'Commit completed rewrite/research/release/publication work and local evidence dependencies. Frozen packages retained, including ignored checksum-bound files. No deletion of local files.','files':rows,'files_count':len(rows),'bytes':total,'traversed_documents':len(seen),'referenced_paths':len(referenced),'excluded_regenerable_geometry':sorted(excluded_geometry),'excluded_unrelated_historical_delivery_logs':sorted(historical_logs),'parse_errors':parse_errors,'note':'External source originals retain their existing attribution, terms and source identity; this Git operation grants no new rights.'})
allpaths=selected|{str((D/'delivery-plan.json').relative_to(R)),str(Path(__file__).relative_to(R))}
Path('/tmp/causal-publication-stage-paths.nul').write_bytes(bytes([0]).join(p.encode() for p in sorted(allpaths))+bytes([0]))
print(json.dumps({'status':'prepared','files':len(rows),'GiB':round(total/1024**3,3),'excluded_geometry':len(excluded_geometry),'excluded_historical_logs':len(historical_logs),'parse_errors':len(parse_errors),'plan':str((D/'delivery-plan.json').relative_to(R))}),flush=True)
