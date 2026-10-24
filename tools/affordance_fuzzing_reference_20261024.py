#!/usr/bin/env python3
"""Authored exact semantic-oracle witnesses; no downloaded code or model execution."""
from fractions import Fraction as F
import json

def calculate():
    candidates={"familiar_unsettled":dict(days=2,collateral=True,authorized=True),"unfamiliar_feasible":dict(days=1,collateral=True,authorized=True),"fast_ineligible":dict(days=0,collateral=False,authorized=True),"fast_unapproved":dict(days=0,collateral=True,authorized=False)}
    feasible=lambda c:c['days']<=1 and c['collateral'] and c['authorized']
    winners=[k for k,v in candidates.items() if feasible(v)]
    assert winners==['unfamiliar_feasible']
    extras={f'distractor_{i}':dict(days=2+i,collateral=False,authorized=True) for i in range(5)}
    assert [k for k,v in dict(candidates,**extras).items() if feasible(v)]==winners
    normalized4=(F(85,100)-F(1,4))/(1-F(1,4));normalized9=(F(75,100)-F(1,9))/(1-F(1,9))
    cluster_variance=(1+24*F(3,5))/500
    lhs,rhs=F(1000000),F(1005000);atol,rtol=F(1,1000),F(1,100)
    threshold=atol+rtol*abs(rhs);difference=abs(lhs-rhs)
    assert difference<=threshold and difference>1000
    assert abs(F(5,10000))<=atol and abs(F(5,100))>atol
    assert normalized4==F(4,5) and normalized9==F(23,32) and cluster_variance==F(77,2500)
    assert 6+2+2==10 and 60-20==40
    out=dict(feasible_choice=winners,distractors_do_not_change_oracle=True,chance_normalized_four=normalized4,chance_normalized_nine=normalized9,cluster_mean_variance=cluster_variance,independent_mean_variance=F(1,500),equivalent_independent_count=1/cluster_variance,backend_difference_usd=difference,numerical_threshold_usd=threshold,comparison_passes=True,stipulated_business_tolerance_usd=1000,business_tolerance_passes=False,shared_error=dict(truth=100,left=110,right=110,decision_threshold=105,backend_agreement=True,decision_correct=False),unit_sensitive_absolute_tolerance=dict(dollars_pass=True,cents_pass=False),generation=dict(attempts=100,runnable=60,duplicates=20,unique_runnable=40,candidates=10,confirmed=6,intended=2,unresolved=2),cost=dict(total_usd=600,per_attempt=F(6),per_runnable=F(10),per_unique=F(15),per_confirmed=F(100)))
    def clean(x):
        if isinstance(x,F):return dict(numerator=x.numerator,denominator=x.denominator,decimal=float(x))
        if isinstance(x,dict):return {k:clean(v) for k,v in x.items()}
        if isinstance(x,list):return [clean(v) for v in x]
        return x
    return clean(out)
if __name__=='__main__':print(json.dumps(calculate(),indent=2))
