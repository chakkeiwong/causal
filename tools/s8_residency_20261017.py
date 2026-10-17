#!/usr/bin/env python3
"""Exact loaded-model scheduling: finite hypothetical batch, no vendor trial."""
from functools import lru_cache
from itertools import combinations, product
from fractions import Fraction as F
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-17/s8/residency-extension'
REQUESTS=('A','B','C','A','B','C')


def oracle(capacity,requests=REQUESTS):
    @lru_cache(None)
    def solve(i,loaded):
        if i==len(requests): return (0,())
        needed=requests[i]; current=set(loaded)
        if needed in current:
            value,trace=solve(i+1,loaded)
            return value,((needed,False,loaded),)+trace
        choices=[current] if len(current)<capacity else [current-{x} for x in current]
        out=[]
        for keep in choices:
            next_loaded=tuple(sorted(keep|{needed}))
            value,trace=solve(i+1,next_loaded)
            out.append((1+value,((needed,True,next_loaded),)+trace))
        return min(out)
    return solve(0,())


def lru(capacity,requests=REQUESTS):
    ordered=[];misses=0;trace=[]
    for needed in requests:
        miss=needed not in ordered
        if miss:
            misses+=1
            if len(ordered)==capacity:ordered.pop(0)
        else:ordered.remove(needed)
        ordered.append(needed)
        trace.append((needed,miss,tuple(ordered)))
    return misses,trace


def calculate():
    out={}
    for m in (1,2,3):
        misses,trace=oracle(m);online,online_trace=lru(m)
        out[str(m)]=dict(oracle_loads=misses,oracle_time=5*misses+6,oracle_trace=trace,
                        lru_loads=online,lru_time=5*online+6,lru_trace=online_trace)
    all_requests=list(product(('A','B','C'),repeat=6))
    uniform={}
    license_fees={1:0,2:120,3:300}
    for m in (1,2,3):
        loads=[lru(m,r)[0] for r in all_requests]
        mean=F(sum(loads),len(loads))
        uniform[str(m)]=dict(mean_loads=str(mean),worst_loads=max(loads),
            mean_time=str(6+5*mean),mean_cost=str(license_fees[m]+20*(6+5*mean)),
            worst_time=6+5*max(loads),worst_cost=license_fees[m]+20*(6+5*max(loads)),
            deadline30_failures=sum(6+5*x>30 for x in loads),total_requests_sequences=len(loads))
    return json.loads(json.dumps(dict(requests=REQUESTS,load_duration=5,inference_duration=1,
        units='Abstract time units',capacity=out,assumptions=[
            'Empty initial cache; fixed known request order; sequential processing; no prefetch, overlapping load or inference.',
            'Every newly resident model costs5 time units; each inference costs1; eviction is instantaneous.',
            'Capacity counts every retained loaded model; oracle knows the whole batch; LRU sees past requests only.',
            'No commercial engine timing, rights or support is inferred.'],
        uniform_workload=uniform,hypothetical_capacity_charges=license_fees,time_charge=20,
        known_batch_costs={str(m):license_fees[m]+20*out[str(m)]['oracle_time'] for m in (1,2,3)})))


def separate(value):
    # Enumerate resident sets after each request directly. Unlike the recurrence,
    # this allows all valid subsets of the prior residents plus current model.
    names={'A','B','C'}
    for m in (1,2,3):
        states=[set(c) for k in range(1,m+1) for c in combinations(sorted(names),k)]
        valid=[s for s in product(states,repeat=6)
               if all(REQUESTS[i] in s[i] and s[i] <= (s[i-1] if i else set())|{REQUESTS[i]}
                      for i in range(6))]
        score=lambda s:sum(REQUESTS[i] not in (s[i-1] if i else set()) for i in range(6))
        optimum=min(map(score,valid))
        assert optimum==value['capacity'][str(m)]['oracle_loads']
    assert [value['capacity'][str(m)]['oracle_loads'] for m in (1,2,3)]==[6,4,3]
    assert [value['capacity'][str(m)]['lru_loads'] for m in (1,2,3)]==[6,6,3]
    assert [value['capacity'][str(m)]['oracle_time'] for m in (1,2,3)]==[36,26,21]
    # Marginal probability calculation independent of whole-path enumeration.
    means={1:1+5*F(2,3),2:1+sum(F(1,3)+F(1,3)*F(1,3)**(t-2) for t in range(2,7)),
           3:3*(1-F(2,3)**6)}
    assert means=={1:F(13,3),2:F(769,243),3:F(665,243)}
    for m in (1,2,3):
        assert F(value['uniform_workload'][str(m)]['mean_loads'])==means[m]
    assert value['known_batch_costs']=={'1':720,'2':640,'3':720}
    assert min(value['uniform_workload'],key=lambda m:F(value['uniform_workload'][m]['mean_cost']))=='1'
    assert [value['uniform_workload'][str(m)]['worst_time'] for m in (1,2,3)]==[36,36,21]
    return dict(status='pass',scope='Same-author independent exhaustive resident-set path enumeration',
                findings=['Known-batch optimum loads6/4/3 for capacity1/2/3.',
                          'LRU loads6/6/3, so two licensed slots alone do not ensure the offline26-unit schedule.',
                          'All729 equally likely sequences match independently derived mean load counts13/3,769/243,665/243.',
                          'Known-batch cost chooses two slots; expected IID cost chooses one; a worst-sequence30-unit deadline needs three.',
                          'No empirical workload or vendor runtime claim.'])


if __name__=='__main__':
    result=calculate();print(json.dumps(dict(result=result,review=separate(result)),indent=2))
