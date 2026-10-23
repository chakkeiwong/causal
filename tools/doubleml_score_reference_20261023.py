#!/usr/bin/env python3
"""Independent finite-sample score algebra; never imports DoubleML."""
from fractions import Fraction as F
import json

def calculate():
    y=list(map(F,[5,3,4,2]));d=list(map(F,[1,0,1,0]))
    g0=[F(1)]*4;g1=[F(3)]*4;m=[F(1,2)]*4
    scores=[b-a+t*(out-b)/p-(1-t)*(out-a)/(1-p) for out,t,a,b,p in zip(y,d,g0,g1,m)]
    estimate=sum(scores)/4
    var=sum((x-estimate)**2 for x in scores)/16
    assert scores==list(map(F,[6,-2,4,0])) and estimate==2 and var==F(5,2)
    # A single treated residual with two declared propensities; no population identification claim.
    unprocessed=F(1)/F(1,1000);processed=F(1)/F(1,100)
    assert unprocessed==1000 and processed==100
    return dict(kind='authored_independent_score_witness',rows=4,ate_scores=[str(x) for x in scores],estimate=str(estimate),iid_score_variance_of_mean=str(var),stipulated_customer_value_per_effect_unit_usd=10,stipulated_cost_usd=15,net_usd=5,propensity_residual_comparison=dict(unprocessed=str(unprocessed),processed=str(processed)),assumptions=['Fixed external nuisance arrays; no nuisance estimation or package execution.','Variance is the stated empirical iid score formula, not finite-sample confidence coverage.','Clipping comparison changes the residual term; positivity/identification are not repaired by clipping.','Stipulated dollars are illustrative, not measured bank economics.'],native_execution=False)
if __name__=='__main__':print(json.dumps(calculate(),indent=2))
