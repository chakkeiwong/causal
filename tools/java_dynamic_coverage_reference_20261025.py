#!/usr/bin/env python3
"""Authored exact JVM temporal contracts; no upstream code execution."""
from fractions import Fraction as F
import json

def calculate():
    times=[2000,2002,2003];values=[10,20,30]
    lag_rows=[[values[r+1],values[r]] for r in range(len(values)-1)]
    assert lag_rows==[[20,10],[30,20]]
    names=['funding','funding:1'];dot_indices=[n.find('.') for n in names]
    assert dot_indices==[-1,-1]
    # Widths under the explicitly stated one-exogenous-column fixture.
    n,p,m,q,spec=2,2,1,3,0
    input_width=spec+n*p+m*q;forged_width=spec+n*p
    assert input_width==7 and forged_width==4
    phi=F(1,2);variance1=F(1);variance2=1+phi**2
    assert variance2==F(5,4)
    levels=[10,13,17];last_difference=levels[-1]-levels[-2]
    acceleration=[F(1),F(1)]
    differences=[];v=F(last_difference)
    for a in acceleration:v+=a;differences.append(v)
    reconstructed=[];v=F(levels[-1])
    for d in differences:v+=d;reconstructed.append(v)
    assert reconstructed==[22,28]
    state_variance=F(1);missing=[]
    for _ in range(2):state_variance+=1;missing.append(state_variance)
    assert missing==[2,3]
    coefficient_variance=F(1,4);dx=F(2);base_variance=F(1)
    adjusted=base_variance+dx*coefficient_variance*dx;assert adjusted==2
    return dict(times=times,values=values,positional_lag_rows=lag_rows,
                generated_names=names,dot_parser_indices=dot_indices,
                constructed_varx_width=input_width,forged_varx_width=forged_width,
                ar1_forecast_variances=[str(variance1),str(variance2)],
                second_difference_forecast_levels=[str(x) for x in reconstructed],
                missing_state_variances=[str(x) for x in missing],
                conditional_variance_with_regression_uncertainty=str(adjusted),
                hypothetical_costs_usd={str(n):str(F(21000,n)) for n in [700,500,350]},
                native_execution=False,causal_calibration_claim=False)

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
