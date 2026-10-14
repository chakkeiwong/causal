#!/usr/bin/env python3
"""Fresh-process complete equal-obligation dense/QR requests from mapped inputs."""
import argparse
import json
import os
import resource
import subprocess
import time
import numpy as np
from threadpoolctl import threadpool_limits
from reliability_common import ROOT,Journal,SPEC
from closure_common import digest,default
from reliability_learning_study import data,request
from causalbank.chunked_learning import fit_chunked

DIRECTORY=ROOT/'docs/studies/reliability-workloads'

def worker(args,s):
    start=time.perf_counter();manifest=json.loads((DIRECTORY/f'input-{args.n}.json').read_text())
    for p,h in manifest['input_sha256'].items():assert digest(p)==h
    c=np.load(DIRECTORY/f'controls-{args.n}.npy',mmap_mode='r');y=np.load(DIRECTORY/f'targets-{args.n}.npy',mmap_mode='r')
    cfg=dict(s['learning'],n=args.n);result=fit_chunked(request(cfg),c,y,chunk_rows=cfg['chunk_rows'],algorithm=args.algorithm)
    stem=f'{args.n}-{args.algorithm}-{args.repeat}';scores_path=DIRECTORY/(stem+'-scores.npz');output=DIRECTORY/(stem+'.json')
    np.savez(scores_path,scores=result.pop('scores'),folds=result.pop('folds'))
    output.write_text(json.dumps(result,default=default,allow_nan=False)+'\n');reread=json.loads(output.read_text());score=np.load(scores_path)
    assert reread['status']=='computed' and len(score['scores'])==args.n-cfg['gap'] and np.isfinite(score['scores']).all()
    print(json.dumps(dict(output=str(output.relative_to(ROOT)),scores=str(scores_path.relative_to(ROOT)),input_manifest=str((DIRECTORY/f'input-{args.n}.json').relative_to(ROOT)),
        request_seconds=time.perf_counter()-start,max_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        estimate=reread['estimate'],standard_error=reread['standard_error'],identity=reread['identity'])))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--worker',action='store_true');ap.add_argument('--n',type=int);ap.add_argument('--algorithm');ap.add_argument('--repeat',type=int);args=ap.parse_args();s=json.loads((ROOT/SPEC).read_text())
    if args.worker:
        with threadpool_limits(limits=1):worker(args,s)
        return
    DIRECTORY.mkdir(exist_ok=True);inputs=['tools/reliability_workloads.py','tools/reliability_learning_study.py','tools/study_response_extensions.py','src/causalbank/chunked_learning.py','src/causalbank/blocked_learning.py'];j=Journal('workloads',inputs);rows=[];generated=[];comparisons=[]
    for n in s['workloads']['sizes']:
        manifest=DIRECTORY/f'input-{n}.json'
        if not manifest.exists():
            with threadpool_limits(limits=1):c,y=data(dict(s['learning'],n=n),np.random.default_rng([s['pilot_seed'],80,n]))
            np.save(DIRECTORY/f'controls-{n}.npy',c);np.save(DIRECTORY/f'targets-{n}.npy',y)
            paths=[str((DIRECTORY/f'{name}-{n}.npy').relative_to(ROOT)) for name in ('controls','targets')]
            manifest.write_text(json.dumps(dict(input_sha256={p:digest(p) for p in paths}),indent=2)+'\n')
        generated.extend([str(manifest.relative_to(ROOT))]+list(json.loads(manifest.read_text())['input_sha256']))
        for rep in range(s['workloads']['repeats']):
            pair=[]
            for algorithm in ('dense_svd','chunked_qr'):
                def run():
                    environment=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1');start=time.perf_counter()
                    process=subprocess.run([str(ROOT/'.venv-scope/bin/python'),str(ROOT/'tools/reliability_workloads.py'),'--worker','--n',str(n),'--algorithm',algorithm,'--repeat',str(rep)],cwd=ROOT,env=environment,text=True,capture_output=True,timeout=300)
                    if process.returncode:raise RuntimeError(process.stderr[-2000:])
                    row=json.loads(process.stdout);row.update(n=n,algorithm=algorithm,repeat=rep,process_seconds=time.perf_counter()-start);return row
                row=j.run(f'{n}/{rep}/{algorithm}',run);pair.append(row);rows.append(row);generated.extend([row['output'],row['scores']])
            a,b=pair;ra=json.loads((ROOT/a['output']).read_text());rb=json.loads((ROOT/b['output']).read_text());sa=np.load(ROOT/a['scores']);sb=np.load(ROOT/b['scores'])
            delta=max(abs(ra['estimate']-rb['estimate']),abs(ra['standard_error']-rb['standard_error']),float(np.max(abs(sa['scores']-sb['scores']))))
            checks=dict(equivalent=delta<1e-9,identity=ra['identity']==rb['identity'],same_inference=ra['inference']==rb['inference'],same_folds=np.array_equal(sa['folds'],sb['folds']))
            assert all(checks.values()),checks
            comparisons.append(dict(n=n,repeat=rep,checks=checks,max_difference=delta,chunk_to_dense_memory_ratio=b['max_rss_kib']/a['max_rss_kib'],chunk_to_dense_process_time_ratio=b['process_seconds']/a['process_seconds']))
            print(json.dumps(comparisons[-1]),flush=True)
    j.finish(dict(runs=rows,comparisons=comparisons,artifact_sha256={p:digest(p) for p in sorted(set(generated))},
        scope='Complete local requests: fresh process/import, immutable mapped input verification, fitting, predictions, inference, output/score persistence and read-back. Input acquisition/synthetic preparation excluded equally. O(n) scores/residuals retained. No multi-host, fault-service or arbitrary learner benchmark.'))

if __name__=='__main__':main()
