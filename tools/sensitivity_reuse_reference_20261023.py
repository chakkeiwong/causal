#!/usr/bin/env python3
"""Independent rational witnesses; no upstream code is imported or executed."""
from fractions import Fraction as F
from math import isqrt

def sqrt_exact(value):
    a,b=isqrt(value.numerator),isqrt(value.denominator)
    assert a*a==value.numerator and b*b==value.denominator
    return F(a,b)

def risk_ratio_threshold(rr):
    if rr <= 0: raise ValueError('Strictly positive risk ratio required by this proposed profile')
    oriented=max(rr,1/rr)
    return oriented+sqrt_exact(oriented*(oriented-1))

def calculate():
    estimate,se,dof,a,b=F(3),F(1),F(8),F(1,5),F(1,2)
    bias=se*sqrt_exact(dof*a*b/(1-a))
    adjusted=estimate-bias
    variance=se*se*(1-b)/(1-a)*dof/(dof-1)
    assert bias==1 and adjusted==2 and variance==F(5,7)
    assert risk_ratio_threshold(F(9,5))==risk_ratio_threshold(F(5,9))==3
    assert risk_ratio_threshold(F(1))==1
    or_value=F(81,25); baseline=F(1,5)
    converted=sqrt_exact(or_value)
    exact_rr=or_value/(1-baseline+baseline*or_value)
    assert converted==F(9,5) and exact_rr==F(405,181) and converted!=exact_rr
    net_before=10*estimate-25;net_after=10*adjusted-25
    assert net_before==5 and net_after==-5
    return dict(kind='project_owned_exact_arithmetic',native_execution=False,
        regression=dict(estimate=str(estimate),se=str(se),residual_dof=str(dof),partial_r2_treatment=str(a),partial_r2_outcome=str(b),bias=str(bias),adjusted_estimate=str(adjusted),adjusted_variance=str(variance),stipulated_net_before=str(net_before),stipulated_net_after=str(net_after)),
        risk_ratio=dict(harmful='9/5',protective='5/9',threshold='3',null_threshold='1',interval_crosses_null_threshold='1'),
        odds_ratio=dict(odds_ratio=str(or_value),nonrare_source_conversion=str(converted),stipulated_baseline_risk=str(baseline),exact_rr_under_that_baseline=str(exact_rr)),
        domain_requirements=['Strictly positive finite RR and target, ordered compatible interval bounds.','For this proposed regular regression profile require finite se>0, dof>1 and 0<=a<1, 0<=b<1; degenerate boundaries require explicit refusal.'],
        limitations=['Specified algebra, not native outputs or observed package failures.','No confidence coverage, confounder truth, external acceptance or measured economics is established.'])
if __name__=='__main__':
    import json
    print(json.dumps(calculate(),indent=2))
