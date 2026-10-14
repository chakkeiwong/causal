#!/usr/bin/env python3
"""Standard-library supervisor: no input preparation contaminates child RSS."""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import resource
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
FOLDER=ROOT/'docs/studies/precision-workload-runs'
SPEC='docs/studies/precision-streaming-spec.json'


def digest(path):
    with (ROOT/path).open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()


def difference(left,right):
    if isinstance(left,dict):
        excluded={'algorithm','pilot_validation_losses','pilot_validation_loss_gap'}
        assert set(left)-excluded==set(right)-excluded
        return max((difference(left[k],right[k]) for k in left if k not in excluded),default=0.)
    if isinstance(left,list):
        assert len(left)==len(right)
        return max((difference(a,b) for a,b in zip(left,right)),default=0.)
    if isinstance(left,(float,int)):
        return abs(left-right)/max(1.,abs(left),abs(right))
    assert left==right
    return 0.


def child(n,algorithm,repeat):
    status=Path('/proc/self/status').read_text().splitlines()
    rss=int(next(line for line in status if line.startswith('VmRSS:')).split()[1])*1024
    command=[sys.executable,str(ROOT/'tools/precision_workloads.py'),'--n',str(n),'--algorithm',algorithm,'--repeat',str(repeat)]
    started=time.perf_counter()
    process=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=600)
    elapsed=time.perf_counter()-started
    assert process.returncode==0,process.stderr
    print(json.dumps(dict(launcher_rss_bytes=rss,child_peak_rss_bytes=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss*1024,worker_seconds=elapsed)))


def main():
    spec=json.loads((ROOT/SPEC).read_text())
    names=[SPEC,'tools/precision_workload_launcher.py','tools/precision_workloads.py']
    for n in spec['workloads']['dates']:
        names.append(str((FOLDER/f'input-{n}.json').relative_to(ROOT)))
        names.extend(json.loads((FOLDER/f'input-{n}.json').read_text())['files'])
    identities={p:digest(p) for p in names}
    journal=ROOT/'docs/studies/precision-workloads.jsonl'
    rows={}
    if journal.exists():
        lines=journal.read_text().splitlines()
        assert json.loads(lines[0])['input_sha256']==identities
        for line in lines[1:]:
            row=json.loads(line);assert row['key'] not in rows
            rows[row['key']]=row['result']
    else:journal.write_text(json.dumps(dict(input_sha256=identities))+'\n')
    comparisons=[]
    for n in spec['workloads']['dates']:
        for repeat in range(spec['workloads']['repeats']):
            for algorithm in (['dense','streaming'] if repeat==0 else ['streaming','dense']):
                key=f'{n}/{repeat}/{algorithm}'
                if key not in rows:
                    command=[sys.executable,str(Path(__file__).resolve()),'--child','--n',str(n),'--algorithm',algorithm,'--repeat',str(repeat)]
                    started=time.perf_counter()
                    process=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=660)
                    elapsed=time.perf_counter()-started
                    assert process.returncode==0,process.stderr
                    launch=json.loads(process.stdout)
                    assert launch['launcher_rss_bytes']<40*1024**2
                    output=str((FOLDER/f'{algorithm}-{n}-{repeat}.json').relative_to(ROOT))
                    value=json.loads((ROOT/output).read_text())
                    assert abs(launch['child_peak_rss_bytes']-value['peak_rss_bytes'])<2*1024**2
                    value.update(algorithm=algorithm,dates=n,repeat=repeat,complete_seconds=elapsed,launcher=launch,output_path=output,output_sha256=digest(output))
                    rows[key]=value
                    with journal.open('a') as stream:stream.write(json.dumps(dict(key=key,result=value))+'\n');stream.flush()
            dense,streamed=[rows[f'{n}/{repeat}/{a}'] for a in ('dense','streaming')]
            error=difference(dense['result'],streamed['result']);assert error<1e-9
            comparison=dict(dates=n,pilot_dates=4*n,repeat=repeat,maximum_scaled_difference=error,memory_ratio=streamed['peak_rss_bytes']/dense['peak_rss_bytes'],time_ratio=streamed['complete_seconds']/dense['complete_seconds'])
            comparisons.append(comparison);print(json.dumps(comparison),flush=True)
    inputs=set(names+[str(journal.relative_to(ROOT))])
    for row in rows.values():inputs.add(row['output_path'])
    for n in spec['workloads']['dates']:
        inputs.update(json.loads((FOLDER/f'input-{n}.json').read_text())['input_sha256'])
    output=dict(status='pass',comparisons=comparisons,runs=list(rows.values()),platform=dict(system=platform.system(),machine=platform.machine(),python=platform.python_version()),input_sha256={p:digest(p) for p in sorted(inputs)},scope='Complete local pilot-tuning/refit plus inference, imports, input hashes, output persistence/read-back. Input acquisition excluded equally; resident mapped pages included. No target-platform service-level or partial-fit recovery claim.')
    (ROOT/'docs/studies/precision-workloads-results.json').write_text(json.dumps(output,indent=2)+'\n')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--child',action='store_true')
    parser.add_argument('--n',type=int);parser.add_argument('--algorithm',choices=['dense','streaming'])
    parser.add_argument('--repeat',type=int,default=0);args=parser.parse_args()
    child(args.n,args.algorithm,args.repeat) if args.child else main()
