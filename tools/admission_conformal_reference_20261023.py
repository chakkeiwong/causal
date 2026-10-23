#!/usr/bin/env python3
"""Exact authored witnesses; no downloaded implementation is executed."""
from fractions import Fraction as F
from itertools import product
import json

def calculate():
    # Perfectly copied votes carry one random bit, not three independent bits.
    p=F(4,5)
    independent=sum(p**sum(z)*(1-p)**(3-sum(z)) for z in product([0,1],repeat=3) if sum(z)>=2)
    copied=p
    assert independent==F(112,125) and copied==F(4,5)
    # A policy's candidate stream is part of its outcome.
    streams={'A':dict(false_candidates=100,false_admissions=10),'B':dict(false_candidates=10,false_admissions=5)}
    # Stipulated utility per evaluated request, not fitted to CPB or bank prices.
    utility_a=F(60,100)*10-F(5,100)*100-1
    utility_b=F(30,100)*10-F(1,100)*100-1
    assert utility_a==0 and utility_b==1
    # Marginal 90% correctness on each independent request does not ensure simultaneous correctness.
    family_failure=1-F(9,10)**5
    assert family_failure==F(40951,100000)
    # Empirical quantile rank needs an infinity sentinel if k=n+1.
    n=5;alpha=F(1,10);x=(n+1)*(1-alpha);k=-(-x.numerator//x.denominator)
    assert k==6
    # Minimum domain quantile is NOT conservative for the ordinary event score <= quantile.
    # This is distinct from nested all-facts-valid filtering, whose direction must be derived.
    domain_scores=[0,1];domain_quantiles=[0,1]
    own=sum(F(s<=q) for s,q in zip(domain_scores,domain_quantiles))/2
    pooled_min=sum(F(s<=min(domain_quantiles)) for s in domain_scores)/2
    assert own==1 and pooled_min==F(1,2)
    # Bounded transition witness for Algorithm 3: all generated candidates fail.
    M=2;attempt=1;trace=[]
    for step in range(5):
        trace.append(attempt)
        if attempt<M:attempt+=1
    assert trace==[1,2,2,2,2]
    return dict(copied_vote=dict(independent_majority=str(independent),perfect_copy=str(copied)),
        policy_streams=streams,stipulated_net_usd=dict(A=str(utility_a),B=str(utility_b)),
        five_request_failure=str(family_failure),small_calibration=dict(n=n,alpha=str(alpha),rank=k,requires_infinity=True),
        ordinary_prediction_coverage=dict(own_domain=str(own),minimum_quantile=str(pooled_min),not_a_refutation_of_nested_filtering=True),
        pseudocode_attempts=trace,reported_table_checks=dict(math_accuracy_difference=str(F('48.9')-F('71.2')),
            phyx_full_minus_partial_accuracy=str(F('50.1')-F('53.1')),phyx_full_minus_partial_validity=str(F('91.7')-F('92.1'))),
        native_execution=False,bank_evidence=False)

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
