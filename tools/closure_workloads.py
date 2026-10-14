#!/usr/bin/env python3
"""Matched complete local work in fresh processes, separately from simulations."""
import argparse
import json
from pathlib import Path
import resource
import subprocess
import sys
import tempfile
import time
import platform
import numpy as np
from threadpoolctl import threadpool_limits,threadpool_info
from closure_common import ROOT,save,default
from causalbank.blocked_learning import BlockedIVRequest,fit_blocked,blocked_covariance
from causalbank.checkpoint_scores import write_partitions,stream_lrv,materialize_calendar_feed
from causalbank.closure_journeys import JourneyRequest,run_journey,compose_result,treasury_consumer,application_consumer
from causalbank.persistent_audits import audited_pair_effect
from causalbank.latent_temporal_sets import effect_set
from causalbank.nonlinear_stability import fit_stable
from causalbank.nonlinear_audited import TRUTH,simulate
from closure_linkage_study import pair_sample
from closure_discovery_study import sample
from study_response_extensions import learning_sample


def worker(kind,size,mode,repeat):
    spec=json.loads((ROOT/'docs/studies/closure-spec.json').read_text());rng=np.random.default_rng([101090,size,repeat]);stages={}
    with tempfile.TemporaryDirectory(prefix='causal-workload-',dir='/tmp') as tmp,threadpool_limits(limits=1):
        folder=Path(tmp);source=folder/'source.npz'
        if kind=='funding':
            a,y,r,l,q,_=pair_sample(dict(spec['persistent'],pairs=size),rng,.3);payload=dict(action=a,candidates=y,audited=r,labels=l,inclusion_probability=q)
            request=JourneyRequest('persistent_funding','independent_pairs','eligible_deposit_customers','pair','action_then_outcome','audited_pair_CLT',1000.)
        elif kind=='nonlinear':
            main,_=simulate(TRUTH,80,3,rng);audit,s=simulate(TRUTH,size,3,rng);payload=dict(main=main,audit=audit,states=s,policy=np.array([-1.,-1.,0.]))
            request=JourneyRequest('nonlinear_servicing','independent_trajectories','eligible_servicing_customers','customer','signal_action_reward_transition','audited_nonlinear_delta',1000.)
        elif kind=='discovery':
            payload=dict(episodes=sample(rng,size),information=np.array('randomized_encouragement'))
            request=JourneyRequest('discovery_decision','independent_gaussian_episodes','eligible_credit_episodes','episode','Z_then_A_then_Y','outer_graph_union',1000.)
        else:
            config=dict(spec['learning'],dates=size);c,y,d,z,_=learning_sample(config,rng);payload=dict(controls=c,outcome=y,treatment=d,instrument=z)
            request=BlockedIVRequest('sparse_lasso',90,.4)
        np.savez(source,**payload)
        if kind=='learning':
            source=folder/'source.jsonl'
            with source.open('w') as output:
                for i in range(size):
                    output.write(json.dumps(dict(origin=i,controls=c[i].tolist(),outcome=float(y[i]),treatment=float(d[i]),instrument=float(z[i]),feature_available_day=i,decision_day=i,outcome_day=i,outcome_received_day=i+1))+'\n')
        start=time.perf_counter();tick=start
        if kind=='learning':
            columns,materialization=materialize_calendar_feed(source,folder/'materialized.npy',size,c.shape[1],cutoff=size+1,mode='stream' if mode=='managed' else 'dense')
            payload=dict(controls=columns[:,:-3],outcome=columns[:,-3],treatment=columns[:,-2],instrument=columns[:,-1])
        else:
            with np.load(source,allow_pickle=False) as arrays:payload={k:arrays[k] for k in arrays.files}
        if kind=='discovery':payload['information']=str(payload['information'])
        stages['source_read']=time.perf_counter()-tick;tick=time.perf_counter()
        if kind=='learning':
            fitted=fit_blocked(request,**payload);stages['fit_and_uncertainty']=time.perf_counter()-tick;tick=time.perf_counter()
            if mode=='managed':
                manifest=write_partitions(folder/'scores',fitted['scores'],fitted['folds'],257)
                streamed=stream_lrv(manifest,folder/'checkpoint.json',fitted['bandwidth'])
                numerical_error=abs(streamed['lrv']-blocked_covariance(fitted['scores'],fitted['folds'],fitted['bandwidth']))
                io=streamed['bytes_read_including_hash_pass']+streamed['checkpoint_bytes_written']
            else:numerical_error=0.;io=0
            stages['score_execution']=time.perf_counter()-tick;tick=time.perf_counter()
            public={k:fitted[k] for k in ('status','estimate','standard_error','interval','identity','inference')}
            reports={'treasury':public,'application':dict(public,estimate_per_fixed_account=fitted['estimate']/2000)}
        else:
            if mode=='managed':
                result=run_journey(request,payload)
            elif kind=='funding':
                result=compose_result(request,payload,audited_pair_effect(**payload,monetary_scale=1000.))
            elif kind=='nonlinear':
                result=compose_result(request,payload,fit_stable(**payload))
            else:
                result=compose_result(request,payload,effect_set(payload['episodes'],information=payload['information']))
            reports={'treasury':treasury_consumer(result),'application':application_consumer(result,2000)}
            stages['fit_uncertainty_consumers']=time.perf_counter()-tick;tick=time.perf_counter();io=0;numerical_error=0.
        output=folder/'reports.json';output.write_text(json.dumps(reports,default=default,allow_nan=False));stages['serialize']=time.perf_counter()-tick
        elapsed=time.perf_counter()-start
        import hashlib
        return dict(kind=kind,size=size,mode=mode,repeat=repeat,elapsed=elapsed,stages=stages,
                    peak_rss_mb=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,
                    source_bytes=source.stat().st_size,output_bytes=output.stat().st_size,additional_score_io_bytes=io,
                    numeric_covariance_difference=numerical_error,threads=threadpool_info(),
                    output_status=reports['treasury']['status'],
                    output_sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
                    scope='Cold process; imports precede timing, JIT first compilation included where applicable. Synthetic source generation excluded; source read through serialization included.')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--worker',choices=['funding','nonlinear','discovery','learning']);ap.add_argument('--size',type=int);ap.add_argument('--mode',choices=['managed','direct']);ap.add_argument('--repeat',type=int,default=0);args=ap.parse_args()
    if args.worker:
        print(json.dumps(worker(args.worker,args.size,args.mode,args.repeat),default=default,allow_nan=False));return
    rows=[]
    for kind,sizes in [('funding',[8000,32000]),('learning',[3000,12000]),('nonlinear',[160,640]),('discovery',[600,2400])]:
        for size in sizes:
            for repeat in range(2):
                for mode in ('direct','managed'):
                    command=[sys.executable,str(Path(__file__).resolve()),'--worker',kind,'--size',str(size),'--mode',mode,'--repeat',str(repeat)]
                    result=subprocess.run(command,text=True,capture_output=True,timeout=180)
                    if result.returncode:raise RuntimeError(result.stderr[-3000:])
                    row=json.loads(result.stdout);rows.append(row);print(json.dumps({k:row[k] for k in ('kind','size','mode','elapsed','peak_rss_mb','output_status')}),flush=True)
                    save('docs/studies/closure-workload-progress.json',dict(status='in_progress',runs=rows),['tools/closure_workloads.py'])
    for kind,size,repeat in {(r['kind'],r['size'],r['repeat']) for r in rows}:
        pair=[r for r in rows if (r['kind'],r['size'],r['repeat'])==(kind,size,repeat)]
        if pair[0]['output_sha256']!=pair[1]['output_sha256']:
            raise RuntimeError('Matched work emitted different public results: '+str((kind,size,repeat)))
    save('docs/studies/closure-workload-results.json',dict(status='executed',host=dict(platform=platform.platform(),processor=platform.processor()),runs=rows,
         comparison='Same synthetic sources, targets, inference obligations and fixed consumers. Direct expert composition uses the same qualified kernels; these timings measure local wrapper/restart costs, not analyst savings.',
         limitations='Single host; inference fitting matrices materialize. Score passes stream and restart. No multi-host or enterprise speedup claim.'),
         ['tools/closure_workloads.py','tools/closure_common.py','src/causalbank/closure_journeys.py','src/causalbank/blocked_learning.py','src/causalbank/checkpoint_scores.py','src/causalbank/nonlinear_stability.py','src/causalbank/nonlinear_audited.py','src/causalbank/persistent_audits.py','src/causalbank/latent_temporal_sets.py'])


if __name__=='__main__':main()
