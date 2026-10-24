#!/usr/bin/env python3
"""Authored rational LiNGAM conversion examples; no package imports."""
from fractions import Fraction as F
import json

def mul(a,b):
    return [[sum((x*y for x,y in zip(row,col)),F(0)) for col in zip(*b)] for row in a]

def calculate():
    b=[[F(0),F(0),F(0)],[F(2),F(0),F(0)],[F(-1),F(3),F(0)]]
    b2=mul(b,b);b3=mul(b2,b)
    assert all(x==0 for row in b3 for x in row)
    total=b[2][0]+b2[2][0]
    assert total==F(5)
    impulse=F(1,5);cost=F(800)
    gross=1000*total*impulse;net=gross-cost
    assert gross==1000 and net==200
    draws=[F(0),F(1,10),F(9,10)];threshold=F(1,2)
    frequency=F(sum(abs(x)>threshold for x in draws),len(draws))
    selected=sorted(x for x in draws if abs(x)>0)
    median_nonzero=sum(selected,F(0))/2
    thresholded=[x for x in draws if abs(x)>threshold]
    assert frequency==F(1,3) and median_nonzero==F(1,2) and thresholded==[F(9,10)]
    # Distinct processes illustrate why independent rows and a shared shock
    # have different averaging uncertainty, without fitting any package.
    n=4;independent_variance=F(1,n);shared_variance=F(1)
    return dict(status='exact_authored_reference',downloaded_code_executed=False,
        matrix=dict(orientation='B[target,predictor]',B=[[str(v) for v in row] for row in b],
            B_squared=[[str(v) for v in row] for row in b2],direct=str(b[2][0]),
            indirect=str(b2[2][0]),total=str(total),impulse=str(impulse),
            gross_usd=str(gross),cost_usd=str(cost),net_usd=str(net),
            qualification='Assumed acyclic invariant linear system;not learned graph or bank value'),
        bootstrap_summary=dict(authored_draws=list(map(str,draws)),threshold=str(threshold),
            threshold_frequency=str(frequency),median_nonzero=str(median_nonzero),
            median_above_threshold='9/10',
            qualification='Replicate summary semantics;no posterior truth probability or coverage claim'),
        dependence=dict(n=n,independent_unit_variance_mean=str(independent_variance),
            shared_unit_variance_mean=str(shared_variance),
            qualification='Different stipulated laws;resampling choice cannot be inferred from API existence'),
        costs=dict(total_usd=4200,requested=210,finite=175,accepted=140,
            per_requested=str(F(4200,210)),per_finite=str(F(4200,175)),per_accepted=str(F(4200,140)),
            qualification='Authored prices and counts;not measured workflow economics'))

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
