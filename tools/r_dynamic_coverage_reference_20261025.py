#!/usr/bin/env python3
"""Project-authored exact witnesses; never executes downloaded R packages."""
from fractions import Fraction as F
import json

def calculate():
    times=[2000,2002,2003];values=[10,20,30];lookup=dict(zip(times,values))
    row=[None]+values[:-1];calendar=[lookup.get(t-1) for t in times]
    assert row==[None,10,20] and calendar==[None,None,20]
    declared_tolerance=F(1,1000);integer_surrogate=int(declared_tolerance);improvement=F(1,2000)
    assert not improvement>declared_tolerance and improvement>integer_surrogate
    h=[[F(-1),F(1,2)],[F(1,2),F(2)]]
    flipped=[[(-v if j==0 else v) for j,v in enumerate(row)] for row in h]
    assert flipped[0][1]!=flipped[1][0]
    rotation=[[F(3,5),F(-4,5)],[F(4,5),F(3,5)]]
    covariance=[[sum(rotation[i][k]*rotation[j][k] for k in range(2)) for j in range(2)] for i in range(2)]
    assert covariance==[[1,0],[0,1]]
    second=[[2*x for x in r] for r in covariance];assert second==[[2,0],[0,2]]
    dense_det=1-F(1,2)**2;assert dense_det**2==F(9,16)
    base_innovation=F(1);shock=F(2)
    replacement_difference=shock-base_innovation;addition_difference=shock
    assert (replacement_difference,addition_difference)==(1,2)
    def drift(x):return x*(F(1,2) if x<=0 else F(3,2))
    histories={}
    for initial in [F(-1),F(1)]:
        base=drift(initial);treated=base+1
        histories[str(initial)]=dict(first=str(treated-base),second=str(drift(treated)-drift(base)))
    assert histories['-1']['second']=='1' and histories['1']['second']=='3/2'
    return dict(times=times,values=values,row_lag=row,calendar_lag=calendar,
                fractional_tolerance=str(declared_tolerance),illustrative_integer_surrogate=integer_surrogate,
                improvement=str(improvement),fractional_continue=False,integer_continue=True,
                altered_inverse_hessian=[[str(x) for x in r] for r in flipped],altered_matrix_symmetric=False,
                covariance=[[str(x) for x in r] for r in covariance],second_regime_covariance=[[str(x) for x in r] for r in second],
                squared_determinant=str(dense_det**2),replacement_difference=str(replacement_difference),
                additive_difference=str(addition_difference),threshold_history_responses=histories,
                hypothetical_costs_usd={str(n):str(F(18000,n)) for n in [600,400,300]},
                native_execution=False,calibration_claim=False)

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
