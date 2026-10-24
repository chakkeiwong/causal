#!/usr/bin/env python3
"""Exact authored SAS comparison witnesses; no acquired code is imported."""
from fractions import Fraction as F
from itertools import product
import json

def calculate():
    # Identical Gaussian covariance, distinct intervention mechanisms.
    rho=F(1,2)
    covariance=[[F(1),rho],[rho,F(1)]]
    forward_effect=rho;reverse_effect=F(0)
    assert covariance[0][0]*covariance[1][1]-rho*rho==F(3,4)
    # Equal observed half-sample, unidentified missing half-sample.
    observed_fraction=F(1,2);observed_mean=F(1,5)
    means=[observed_fraction*observed_mean+(1-observed_fraction)*m for m in [F(0),F(1)]]
    assert means==[F(1,10),F(3,5)]
    # A covariate copied from the future event has perfect prediction only.
    outcomes=[0,0,1,1];future_covariate=outcomes[:]
    assert sum(int(y==x) for y,x in zip(outcomes,future_covariate))==4
    # Offset pagination under a specified insert between page requests.
    original=['a','b','c','d'];first=original[:2]
    changed=['x']+original;second=changed[2:4];seen=first+second
    assert seen==['a','b','b','c'] and len(set(seen))==3 and 'd' not in seen
    # A finite number of polls alone cannot upper-bound request durations.
    poll_count=60;sleep=F(1,2)
    examples=[poll_count*(sleep+d) for d in [F(1),F(60)]]
    assert examples==[F(90),F(3630)]
    costs=[F(36000,n) for n in [1200,900,600]];assert costs==[F(30),F(40),F(60)]
    result=dict(kind='authored_exact_reference_not_vendor_test',covariance=covariance,
        forward_effect=forward_effect,reverse_effect=reverse_effect,
        missing_outcome_mean_bounds=means,missing_loss_bounds_usd=[10000*1000*m for m in means],
        future_covariate_accuracy=F(1),pagination=dict(first=first,second=second,seen=seen,unique=3,missing_original=['d']),
        sixty_poll_seconds=examples,costs_usd=costs,native_execution=False)
    return json.loads(json.dumps(result,default=lambda x:str(x) if isinstance(x,F) else x))

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
