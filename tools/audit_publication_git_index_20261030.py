from pathlib import Path
import hashlib,json,subprocess,sys
R=Path(__file__).resolve().parents[1]
D=R/'docs/program/execution/2026-10-30/publication-git-delivery-001'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
plan=json.loads((D/'delivery-plan.json').read_text());separation=json.loads((D/'concurrent-work-separation.json').read_text())
expected={x['path']:x['sha256'] for x in plan['files'] if x['path'] not in separation['excluded_concurrent_paths']}
for row in separation['index_overrides']:expected[row['path']]=row['sha256']
for p in D.rglob('*'):
    if p.is_file() and p.name not in ['staged-verification.json','commit-output.txt','push-output.txt','push-verification.json']:expected[str(p.relative_to(R))]=sha(p)
expected[str(Path(__file__).relative_to(R))]=sha(Path(__file__))
index={}
for row in git('ls-files','--stage','-z').split(bytes([0])):
    if not row:continue
    meta,name=row.decode().split(chr(9),1);mode,oid,stage=meta.split();assert stage=='0';index[name]=oid
staged={p.decode() for p in git('diff','--cached','--name-only','-z').split(bytes([0])) if p}
missing=sorted(set(expected)-set(index));unexpected=sorted(staged-set(expected));issues=[]
if missing:issues.append({'missing_from_index':missing[:20],'count':len(missing)})
if unexpected:issues.append({'unexpected_staged':unexpected[:20],'count':len(unexpected)})
groups={}
for name,h in expected.items():
    if name in index:groups.setdefault(index[name],[]).append((name,h))
proc=subprocess.Popen(['git','cat-file','--batch'],cwd=R,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
lfs_count=0;checked=0
for oid,rows in groups.items():
    proc.stdin.write((oid+chr(10)).encode());proc.stdin.flush();header=proc.stdout.readline().decode().split();assert header[1]=='blob';size=int(header[2]);data=proc.stdout.read(size);assert len(data)==size;assert proc.stdout.read(1)==b'\n'
    digest=hashlib.sha256(data).hexdigest()
    if data.startswith(b'version https://git-lfs.github.com/spec/v1\n'):
        lines=data.decode().splitlines();digest=next(x.split(':',1)[1] for x in lines if x.startswith('oid sha256:'));lfs_count+=len(rows)
    for name,want in rows:
        checked+=1
        if digest!=want:issues.append({'path':name,'expected_sha256':want,'index_sha256':digest})
    if checked%20000<10:print(json.dumps({'phase':'verify_index','checked':checked,'expected':len(expected)}),flush=True)
proc.stdin.close();proc.wait();assert proc.returncode==0
report={'status':'fail' if issues else 'pass','scope':'Every selected indexed file matches its planned SHA-256 or explicit accepted-publication snapshot; LFS pointers match source SHA-256. Concurrent worktree continuation excluded without modification.','parent_commit':plan['parent_commit'],'actual_parent_commit':git('rev-parse','HEAD').decode().strip(),'selected_index_files':checked,'unique_blobs':len(groups),'lfs_files':lfs_count,'staged_paths':len(staged),'issues':issues,'concurrent_snapshot_overrides':separation['index_overrides'],'excluded_geometry':len(plan['excluded_regenerable_geometry']),'excluded_historical_logs':len(plan['excluded_unrelated_historical_delivery_logs'])}
if report['actual_parent_commit']!=report['parent_commit']:report['status']='fail';report['issues'].append('Parent commit changed during staging')
(D/'staged-verification.json').write_text(json.dumps(report,indent=2)+chr(10));print(json.dumps({k:v for k,v in report.items() if k not in ['concurrent_snapshot_overrides','issues']}));print(json.dumps({'issues':issues[:20]}));raise SystemExit(0 if report['status']=='pass' else 1)
