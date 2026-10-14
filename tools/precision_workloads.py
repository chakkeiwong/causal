#!/usr/bin/env python3
"""Prepare or execute complete dense/streaming pilot requests on saved histories."""
import argparse
import json
import resource
from pathlib import Path
import numpy as np
from threadpoolctl import threadpool_limits, threadpool_info
from precision_common import ROOT, SPEC, SCIENCE_INPUTS, digest
from causalbank.dynamic_funding import FundingTarget
from causalbank.funding_calibration import simulate_rows, DECLARATIONS
from causalbank.funding_pilot_rates import fit_growing_pilot
from causalbank.streaming_pilot import fit_streaming_pilot

FOLDER=ROOT/'docs/studies/precision-workload-runs'
INPUTS=SCIENCE_INPUTS+['tools/precision_workloads.py']


def prepare(n):
    FOLDER.mkdir(exist_ok=True)
    spec=json.loads((ROOT/SPEC).read_text())
    base=json.loads((ROOT/spec['base']).read_text())
    obs=json.loads((ROOT/spec['observation']).read_text())
    obs['correct_pair_probability']=[.9,.85]
    metadata=FOLDER/f'input-{n}.json'
    expected={p:digest(p) for p in INPUTS}
    if metadata.exists():
        prior=json.loads(metadata.read_text())
        assert prior['input_sha256']==expected
        assert all(digest(p)==h for p,h in prior['files'].items())
        return
    files={}
    for kind,multiple,tag in (('evaluation',1,1),('pilot',spec['workloads']['pilot_multiple'],2)):
        path=FOLDER/f'{kind}-{n}.npy'
        rows=simulate_rows(base,obs,n*multiple,[spec['workloads']['seed'],n,tag])
        with path.open('xb') as stream: np.save(stream,rows)
        files[str(path.relative_to(ROOT))]=digest(path)
        del rows
    metadata.write_text(json.dumps(dict(files=files,dates=n,pilot_dates=4*n,input_sha256=expected),indent=2)+'\n')
    print(json.dumps(dict(prepared_dates=n,files=files)),flush=True)


def worker(n,algorithm,repeat):
    spec=json.loads((ROOT/SPEC).read_text())
    base=json.loads((ROOT/spec['base']).read_text())
    metadata=json.loads((FOLDER/f'input-{n}.json').read_text())
    assert all(digest(p)==h for p,h in metadata['input_sha256'].items())
    assert all(digest(p)==h for p,h in metadata['files'].items())
    arrays=[np.load(FOLDER/f'{kind}-{n}.npy',mmap_mode='r' if algorithm=='streaming' else None) for kind in ('pilot','evaluation')]
    for array in arrays:array.flags.writeable=False
    target=FundingTarget(horizon=base['horizon'],branches=base['branches'])
    with threadpool_limits(limits=1):
        pools=threadpool_info()
        assert all(p['num_threads']==1 for p in pools)
        operation=fit_streaming_pilot if algorithm=='streaming' else fit_growing_pilot
        kwargs=dict(declarations=DECLARATIONS)
        if algorithm=='streaming':kwargs['chunk_size']=spec['workloads']['chunk_size']
        result=operation(*arrays,target,[9000,8500],[10000,10000],base['penalties'],**kwargs)
    output=FOLDER/f'{algorithm}-{n}-{repeat}.json'
    receipt=dict(result=result,input_files=metadata['files'],numeric_threadpools=pools,
        peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
        cpu_seconds=resource.getrusage(resource.RUSAGE_SELF).ru_utime+resource.getrusage(resource.RUSAGE_SELF).ru_stime)
    temporary=output.with_suffix('.json.tmp')
    temporary.write_text(json.dumps(receipt,indent=2,allow_nan=False)+'\n')
    temporary.replace(output)
    assert json.loads(output.read_text())==receipt
    assert all(digest(p)==h for p,h in metadata['files'].items())


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--prepare',action='store_true')
    parser.add_argument('--n',type=int,required=True)
    parser.add_argument('--algorithm',choices=['dense','streaming'])
    parser.add_argument('--repeat',type=int,default=0)
    args=parser.parse_args()
    prepare(args.n) if args.prepare else worker(args.n,args.algorithm,args.repeat)
