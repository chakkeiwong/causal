#!/usr/bin/env python3
"""Exact authored calendar, rotation, alignment and state-law witnesses."""
from fractions import Fraction as F
import json

def calculate():
    times=[2000,2002,2003];values=[10,20,30];calendar=dict(zip(times,values))
    positional_lag=[None]+values[:-1]
    calendar_lag=[calendar.get(t-1) for t in times]
    assert positional_lag==[None,10,20] and calendar_lag==[None,None,20]
    rotation=[[F(3,5),F(-4,5)],[F(4,5),F(3,5)]]
    covariance=[[sum(rotation[i][k]*rotation[j][k] for k in range(2)) for j in range(2)] for i in range(2)]
    assert covariance==[[1,0],[0,1]]
    dense_det=1-F(1,2)**2
    squared_det=dense_det**2
    det_elementwise_square=1-F(1,2)**4
    assert squared_det==F(9,16) and det_elementwise_square==F(15,16)
    matched_dot=1*10+2*30;suffix_dot=1*20+2*30
    assert matched_dot==70 and suffix_dot==80
    # Project-authored reset trace, not a native call.
    matrix=[[0,0],[0,0]]
    for j in range(2):
        matrix=[[0,0],[0,0]];matrix[j][j]=1
    assert matrix==[[0,0],[0,1]]
    impact=F(1);diagonal=F(2);shock_sd=impact/diagonal
    initial_variance=F(1);discount=F(1,2)
    first_missing_variance=initial_variance/discount
    second_no_new_innovation=first_missing_variance
    second_fixed_innovation=first_missing_variance+1
    assert (second_no_new_innovation,second_fixed_innovation)==(2,3)
    costs={str(n):str(F(24000,n)) for n in [600,400,300]}
    return dict(times=times,values=values,positional_lag=positional_lag,calendar_lag=calendar_lag,
                orthogonal_rotation=[[str(x) for x in row] for row in rotation],
                covariance=[[str(x) for x in row] for row in covariance],
                squared_determinant=str(squared_det),determinant_elementwise_square=str(det_elementwise_square),
                determinant_ratio=str(det_elementwise_square/squared_det),matched_instrument_dot=matched_dot,
                suffix_instrument_dot=suffix_dot,two_column_reset_result=matrix,
                own_variable_impact=str(impact),structural_shock_amplitude=str(shock_sd),
                first_missing_variance=str(first_missing_variance),second_no_new_innovation=str(second_no_new_innovation),
                second_fixed_innovation=str(second_fixed_innovation),hypothetical_costs_usd=costs,
                native_execution=False,calibration_claim=False)

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
