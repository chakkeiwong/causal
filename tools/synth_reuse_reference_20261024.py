#!/usr/bin/env python3
"""Independent exact examples; never imports upstream package code."""
from fractions import Fraction as F
import json

def calculate():
    w=F(1,2);counterfactual=w*80+(1-w)*120;gap=120-counterfactual
    contaminated=120-(w*80+(1-w)*160);assert gap==20 and contaminated==0
    supplied=[F(-1),F(2)];custom=[abs(v)/sum(supplied) for v in supplied]
    optimized=[abs(v)/sum(abs(x) for x in supplied) for v in supplied]
    assert custom==[1,2] and optimized==[F(1,3),F(2,3)]
    negative=[F(-2),F(-1)];negative_result=[abs(v)/sum(negative) for v in negative]
    assert sum(negative_result)==-1
    treated=[F(0),F(0),F(9)];donor=[F(0),F(0),F(12)]
    tmedian=sorted(treated)[1];dmean=sum(donor)/len(donor);dmedian=sorted(donor)[1]
    assert (tmedian,dmean,dmedian)==(0,4,0)
    candidate=F(3,4);loss=(candidate-F(1,2))**2;gradient=2*(candidate-F(1,2))
    assert loss==F(1,16) and gradient==F(1,2)
    return dict(kind='authored_exact_reference_not_package_output',simplex=dict(weights=['1/2','1/2'],counterfactual=str(counterfactual),gap_thousand_usd=str(gap),contaminated_gap_thousand_usd=str(contaminated),postselected_gap_thousand_usd='0'),custom_weights=dict(input=list(map(str,supplied)),custom_branch=list(map(str,custom)),optimized_branch=list(map(str,optimized)),negative_input=list(map(str,negative)),negative_normalization=list(map(str,negative_result)),zero_sum_input=['-1','1'],zero_sum_status='undefined_division'),predictor_operator=dict(requested='median',treated=str(tmedian),donor_hardcoded_mean=str(dmean),matched_donor_median=str(dmedian)),solver_witness=dict(candidate=str(candidate),feasible=True,loss=str(loss),gradient=str(gradient),stationary=False),illustrative_cost_usd={k:str(F(2400,n)) for k,n in [('requested',120),('conformant',100),('useful',80)]},native_execution=False,empirical_coverage=False)

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
