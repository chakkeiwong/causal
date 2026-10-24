#!/usr/bin/env python3
"""Authored distributed-accounting oracles; never import or start Ray."""
from fractions import Fraction as F
import hashlib,json,itertools,math

def logical_reduce(events):
    accepted={}
    for identity,value in events:
        if identity in accepted and accepted[identity]!=value:raise ValueError('conflicting duplicate')
        accepted[identity]=value
    return sum(accepted.values(),F(0))/len(accepted)

def calculate():
    events=[('A',F(2)),('B',F(4)),('C',F(-1)),('D',F(3))];retries=events+[events[1]]
    logical=logical_reduce(retries);assert logical==2
    assert all(logical_reduce(list(p))==2 for p in itertools.permutations(retries))
    conflicting=False
    try:logical_reduce(events+[('B',F(5))])
    except ValueError:conflicting=True
    assert conflicting
    naive_attempt_mean=sum(v for _,v in retries)/len(retries);fixed_denominator=sum(v for _,v in retries)/len(events)
    rows=[F(1),F(1),F(-1),F(-1)];clusters=[sum(rows[:2]),sum(rows[2:])]
    cluster_meat=sum(x*x for x in clusters)/len(rows)**2;row_meat=sum(x*x for x in rows)/len(rows)**2
    a,b,c=1e16,-1e16,1.;left=(a+b)+c;right=a+(b+c);accurate=math.fsum([a,b,c]);assert (left,right,accurate)==(1.,0.,1.)
    def fold(unit):return int(hashlib.sha256(('fixed-study|'+unit).encode()).hexdigest(),16)%2
    units=['householdA','householdA','householdB','householdB'];stable=[fold(x) for x in units];assert stable[0]==stable[1] and stable[2]==stable[3]
    speedup=1/(F(1,5)+F(4,5)/4);with_overhead=1/(F(1,5)+F(4,5)/4+F(3,10))
    assert speedup==F(5,2) and with_overhead==F(10,7)
    # All money and timings below are stipulated, never vendor quotes.
    total=F(180)+F(120)+F(60);accepted=3;attempts=6;logical_requests=4
    r=dict(retry=dict(logical=logical,attempt_mean=naive_attempt_mean,fixed_denominator_with_duplicate=fixed_denominator,permutations_checked=120,conflicting_duplicate_refused=conflicting),
      covariance=dict(cluster_meat=cluster_meat,row_meat=row_meat,interpretation='Same four rows and denominator16;cluster sums preserve within-cluster cross terms;neither is a calibrated CI'),
      reduction=dict(left=left,right=right,accurate=accurate),folds=dict(stable_unit_folds=stable,row_parity=[0,1,0,1],unit_preserved=True),
      speed=dict(serial_fraction=F(1,5),workers=4,ideal=speedup,extra_overhead=F(3,10),with_overhead=with_overhead),
      cost=dict(total=total,per_attempt=total/attempts,per_logical_request=total/logical_requests,per_accepted=total/accepted),
      interpretation='Exact finite accounting and stipulated cost/scaling laws;no Ray execution,benchmark or bank qualification.')
    return json.loads(json.dumps(r,default=lambda x:str(x)))
if __name__=='__main__':print(json.dumps(calculate(),indent=2))
