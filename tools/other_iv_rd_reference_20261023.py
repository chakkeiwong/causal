#!/usr/bin/env python3
"""Exact IV/RD and static-expression witnesses; no upstream runtime execution."""
from fractions import Fraction as F
import json,math

def calculate():
    reduced, first = F(2),F(1,5)
    g=[1/first,-reduced/first**2]
    V=[[F(1,25),F(1,250)],[F(1,250),F(1,100)]]
    variance=sum(g[i]*V[i][j]*g[j] for i in range(2) for j in range(2))
    frozen=V[0][0]/first**2
    tail=lambda z: math.erfc(z/math.sqrt(2))/2
    p=dict(z=2,usual_two_sided=2*tail(2),naive_julia_display=tail(2),legacy_julia_display=tail(4))
    # Residual mutation witness: one mutable residual with a positive weight.
    residual,weight=F(1),F(4)
    once=residual*2;twice=once*2
    # Toy regression support: repeated score points do not increase polynomial rank.
    left=[F(-1)]*5;right=[F(1)]*5
    det=lambda x:len(x)*sum(v*v for v in x)-sum(x)**2
    result=dict(fuzzy=dict(reduced_form=str(reduced),first_stage=str(first),effect=str(reduced/first),
        gradient=list(map(str,g)),covariance=[[str(x) for x in row] for row in V],
        full_delta_variance=str(variance),frozen_denominator_variance=str(frozen),cost='6',net=str(reduced/first-6)),
        p_value=p,mutating_residual=dict(weight=str(weight),initial=str(residual),first_square=str(once**2),second_square=str(twice**2),ratio=str(twice**2/once**2)),
        discrete_support=dict(rows_per_side=5,unique_scores_per_side=1,left_design_determinant=str(det(left)),right_design_determinant=str(det(right))),
        empty_local_density=dict(left_near_count=0,right_near_count=2,source_fallback_theta=0,source_fallback_se=1,source_fallback_p=1,interpretation='Unavailable local log-density contrast, not evidence for no manipulation.'),
        limits=['Independent rational/asymptotic-formula and expression witnesses, not native outputs.',
         'Delta variance presumes a justified regular joint limit and a first stage bounded away from zero; not weak-IV-valid inference.',
         'Banking values/costs are stipulated; no bank economics or runtime calibration established.'])
    assert variance==24 and frozen==1 and reduced/first-6==4
    assert det(left)==det(right)==0 and p['usual_two_sided']==2*p['naive_julia_display']
    return result

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
