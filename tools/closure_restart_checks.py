#!/usr/bin/env python3
"""Failure injection against a separately computed serial Bartlett reference."""
import json
from pathlib import Path
import tempfile
import numpy as np
from closure_common import ROOT,save
from causalbank.checkpoint_scores import write_partitions,stream_lrv,materialize_calendar_feed
from causalbank.blocked_learning import blocked_covariance


def main():
    rng=np.random.default_rng(101067);scores=rng.normal(size=2401);scores[1:]+=.4*scores[:-1]
    folds=np.r_[np.zeros(1100,int),np.ones(1301,int)];bandwidth=13
    reference=blocked_covariance(scores,folds,bandwidth);checks={};details={}
    with tempfile.TemporaryDirectory(prefix='causal-closure-restart-',dir='/tmp') as temp:
        folder=Path(temp);manifest=write_partitions(folder/'source',scores,folds,chunk=97)
        serial=stream_lrv(manifest,folder/'serial.json',bandwidth)
        checks['serial_stream_equals_dense']=abs(serial['lrv']-reference)<1e-12
        for name,at,partial in [('committed_moments',7,False),('partial_moments',7,True),('committed_lags',35,False),('partial_lags',35,True)]:
            checkpoint=folder/(name+'.json')
            try:stream_lrv(manifest,checkpoint,bandwidth,interrupt_after=at,partial_write=partial);checks[name+'_interrupted']=False
            except InterruptedError:checks[name+'_interrupted']=True
            recovered=stream_lrv(manifest,checkpoint,bandwidth,retry_duplicate=True)
            checks[name+'_same_sample']=recovered['count']==len(scores) and abs(recovered['lrv']-reference)<1e-12
            details[name]=recovered
        duplicate=stream_lrv(manifest,folder/'duplicate.json',bandwidth,retry_duplicate=True)
        checks['duplicate_attempts_once']=duplicate['count']==len(scores) and abs(duplicate['lrv']-reference)<1e-12
        corrupted=folder/'corrupted.json';state=json.loads((folder/'serial.json').read_text());state['total']+=1;corrupted.write_text(json.dumps(state))
        try:stream_lrv(manifest,corrupted,bandwidth);checks['corrupt_checkpoint_rejected']=False
        except ValueError:checks['corrupt_checkpoint_rejected']=True
        try:stream_lrv(manifest,folder/'serial.json',bandwidth+1);checks['changed_procedure_rejected']=False
        except ValueError:checks['changed_procedure_rejected']=True
        path=manifest.parent/'part-00000.npy';arr=np.load(path);arr[0]+=1;np.save(path,arr,allow_pickle=False)
        try:stream_lrv(manifest,folder/'serial.json',bandwidth);checks['changed_data_rejected']=False
        except ValueError:checks['changed_data_rejected']=True
        records=[dict(origin=i,controls=[float(i),float(i*i)],outcome=float(i+1),treatment=1.,instrument=-1.,feature_available_day=i,decision_day=i,outcome_day=i+2,outcome_received_day=i+3) for i in range(10)]
        source=folder/'calendar.jsonl';source.write_text(''.join(json.dumps(r)+'\n' for r in records))
        streamed,receipt=materialize_calendar_feed(source,folder/'stream.npy',10,2,horizon=2,cutoff=20)
        dense,_=materialize_calendar_feed(source,folder/'dense.npy',10,2,horizon=2,cutoff=20,mode='dense')
        checks['stream_materialization_matches_dense']=bool(np.array_equal(streamed,dense))
        for name,change in [('late_feature',{'feature_available_day':100}),('wrong_horizon',{'outcome_day':100}),('duplicate_origin',{'origin':0}),('late_outcome',{'outcome_received_day':100})]:
            modified=[dict(r) for r in records];modified[5].update(change);source.write_text(''.join(json.dumps(r)+'\n' for r in modified))
            try:materialize_calendar_feed(source,folder/(name+'.npy'),10,2,horizon=2,cutoff=20);checks[name+'_rejected']=False
            except ValueError:checks[name+'_rejected']=True
    result=dict(status='pass' if all(checks.values()) else 'fail',checks=checks,details=details,reference_lrv=reference,
                scope='Single-host atomic restart, retries and exactly-once contributions with immutable source/procedure identity; no network service claim.')
    save('docs/reviews/closure-restart-checks.json',result,['tools/closure_restart_checks.py','tools/closure_common.py','src/causalbank/checkpoint_scores.py','src/causalbank/blocked_learning.py'])
    print(json.dumps({'status':result['status'],'checks':checks},indent=2));raise SystemExit(result['status']!='pass')


if __name__=='__main__':main()
