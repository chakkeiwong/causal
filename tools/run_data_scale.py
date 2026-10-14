#!/usr/bin/env python3
"""Temporal adversarial fixture and isolated streaming-component measurements."""
from pathlib import Path
import argparse
import hashlib
import platform
import json
import resource
import statistics
import subprocess
import sys
import time
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from causalbank import Event,Decision,compile_snapshot,ScoreReducer


def temporal_fixture():
    events=[Event('credit','H1','2026-01-02T00:00:00Z','2026-01-03T00:00:00Z',1,100,'USD'),
            Event('credit','H1','2026-01-02T00:00:00Z','2026-01-10T00:00:00Z',2,60,'USD'),
            Event('late','H1','2026-01-04T00:00:00Z','2026-01-12T00:00:00Z',1,30,'USD'),
            Event('moved','H1','2026-01-05T00:00:00Z','2026-01-05T00:00:00Z',1,20,'USD'),
            Event('moved','H1','2026-02-01T00:00:00Z','2026-01-10T00:00:00Z',2,20,'USD'),
            Event('voided','H1','2026-01-06T00:00:00Z','2026-01-06T00:00:00Z',1,40,'USD'),
            Event('voided','H1','2026-01-06T00:00:00Z','2026-01-10T00:00:00Z',2,40,'USD',True)]
    decisions=[Decision('early','H1','2026-01-08T00:00:00Z'),Decision('later','H1','2026-01-13T00:00:00Z')]
    result=compile_snapshot(events,decisions,lookback_days=30,currency='USD',feed_complete=True)
    assert [x['amount'] for x in result['rows']]==[160,90]
    assert result==compile_snapshot(list(reversed(events)),decisions,lookback_days=30,currency='USD',feed_complete=True)
    # Deliberately incorrect alternatives, computed directly for comparison.
    latest={}
    for e in events:
        if e.event_id not in latest or e.revision>latest[e.event_id].revision: latest[e.event_id]=e
    result['wrong_event_time_only_early']=sum(e.amount for e in latest.values() if e.occurred_at<=decisions[0].decision_at and not e.void)
    wrong_latest={}
    for e in events:
        if e.occurred_at<=decisions[1].decision_at and e.available_at<=decisions[1].decision_at:
            if e.event_id not in wrong_latest or e.revision>wrong_latest[e.event_id].revision: wrong_latest[e.event_id]=e
    result['wrong_filter_time_before_revision_later']=sum(e.amount for e in wrong_latest.values() if not e.void)
    result['checks']=['late availability excluded','historical revision retained','void respected','moved economic date does not resurrect old version','input ordering invariant']
    negatives=[]
    cases=[('duplicate',events+[events[0]],decisions,'USD'),('currency',events,decisions,'GBP'),('naive time',events,[Decision('bad','H1','2026-01-08T00:00:00')],'USD'),
           ('empty decision identity',events,[Decision('','H1','2026-01-08T00:00:00Z')],'USD'),
           ('missing entity identity',events,[Decision('bad',None,'2026-01-08T00:00:00Z')],'USD'),
           ('blank entity identity',events,[Decision('bad',' ','2026-01-08T00:00:00Z')],'USD')]
    for name,ee,dd,cc in cases:
        try: compile_snapshot(ee,dd,lookback_days=30,currency=cc,feed_complete=True)
        except ValueError as e: negatives.append({'case':name,'error':str(e)})
        else: raise AssertionError(name)
    try: compile_snapshot(events,decisions,lookback_days=30,currency='USD',feed_complete=False)
    except ValueError as e: negatives.append({'case':'unverified feed completeness','error':str(e)})
    else: raise AssertionError('unverified feed completeness')
    result['rejections']=negatives
    return result


def benchmark(n):
    ne,nt,dim=10000,120,2
    begin=time.perf_counter(); acc=ScoreReducer(ne,nt,dim); reduce_seconds=0.
    for first in range(0,n,100000):
        ix=np.arange(first,min(n,first+100000)); scores=np.c_[np.sin(ix*.17)+.2*np.cos(ix*.009),np.cos(ix*.11)-.15*np.sin(ix*.017)]
        entity=ix%ne; date=(ix//ne)%nt
        stamp=time.perf_counter(); acc.add(scores,entity,date); reduce_seconds+=time.perf_counter()-stamp
    stamp=time.perf_counter(); answer=acc.result(); finalize=time.perf_counter()-stamp
    return {'rows':n,'chunk_rows':100000,'score_dimensions':dim,'declared_entities':ne,'declared_dates':nt,'elapsed_seconds':time.perf_counter()-begin,'reduction_seconds':reduce_seconds,'finalize_seconds':finalize,'peak_rss_mib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,'mean':answer['mean'],'flags':answer['flags'],'scope':'Generated precomputed score reduction; includes generation/finalization, excludes all nuisance fitting and data I/O'}


def verify_reducer():
    rng=np.random.default_rng(701); ns,nt=9,7
    ent=np.repeat(np.arange(ns),nt); date=np.tile(np.arange(nt),ns); x=rng.normal(size=(ns*nt,2)); x+=rng.normal(size=(ns,2))[ent]+rng.normal(size=(nt,2))[date]
    all_rows=ScoreReducer(ns,nt,2); all_rows.add(x,ent,date); got=all_rows.result()
    parts=[ScoreReducer(ns,nt,2) for _ in range(3)]
    for k,part in enumerate(parts): part.add(x[k::3],ent[k::3],date[k::3])
    parts[0].merge(parts[1]).merge(parts[2]); merged=parts[0].result()
    centered=x-x.mean(0); e=centered.reshape(ns,nt,2).sum(1); t=centered.reshape(ns,nt,2).sum(0)
    reference=(ns/(ns-1)*(e.T@e)+nt/(nt-1)*(t.T@t)-(ns*nt)/(ns*nt-1)*(centered.T@centered))/(ns*nt)**2
    np.testing.assert_allclose(reference,got['covariance'],atol=1e-14)
    np.testing.assert_allclose(reference,merged['covariance'],atol=1e-14)
    # A rejected group-key shape must not partially accumulate scores.
    for bad_entity,bad_date in [(ent[:,None],date),(ent,date[:,None])]:
        try: all_rows.add(x,bad_entity,bad_date)
        except ValueError as exc: assert str(exc)=='SCORE_SHAPE'
        else: raise AssertionError('invalid group-key shape accepted')
        assert all_rows.result()==got
    return {'batch_reference_max_error':float(np.max(np.abs(reference-got['covariance']))),'partition_merge_max_error':float(np.max(np.abs(reference-merged['covariance']))),'rejected_shape_preserves_state':True,'rows':len(x),'scope':'Independent centered batch formula and partition merge comparison'}


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--rows',type=int); args=ap.parse_args()
    if args.rows:
        print(json.dumps(benchmark(args.rows))); return
    temporal=temporal_fixture(); verify=verify_reducer(); runs=[]
    for n in [100000,1000000,10000000]:
        for rep in range(3):
            out=subprocess.run([sys.executable,str(Path(__file__).resolve()),'--rows',str(n)],check=True,text=True,capture_output=True)
            row=json.loads(out.stdout); row['replicate']=rep; runs.append(row)
    med=[]
    for n in [100000,1000000,10000000]:
        rr=[x for x in runs if x['rows']==n]
        med.append({'rows':n,**{key:statistics.median(x[key] for x in rr) for key in ['elapsed_seconds','reduction_seconds','finalize_seconds','peak_rss_mib']}})
    result={'temporal':temporal,'reducer_verification':verify,'runs':runs,'medians':med,'python':sys.version,'numpy':np.__version__,'platform':platform.platform(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'component_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'src/causalbank').glob('*.py')},'measurement':'Fresh child process per run; Linux peak RSS includes interpreter and libraries; no extrapolation to estimator training'}
    (ROOT/'docs/derivations/data-scale.json').write_text(json.dumps(result,indent=2)+'\n')
    rows=[r'\begin{tabular}{@{}rrrr@{}}',r'\toprule Rows & Total seconds & Reduce seconds & Peak RSS (MiB)\\\midrule']
    rows += [f'{v["rows"]:,} & {v["elapsed_seconds"]:.3f} & {v["reduction_seconds"]:.3f} & {v["peak_rss_mib"]:.1f}'+r'\\' for v in med]
    rows += [r'\bottomrule\end{tabular}']; (ROOT/'docs/derivations/scale_results.tex').write_text('\n'.join(rows)+'\n')
    print(json.dumps({'temporal_values':[x['amount'] for x in temporal['rows']],'verification':verify,'medians':med}))


if __name__=='__main__': main()
