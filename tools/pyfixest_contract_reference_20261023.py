#!/usr/bin/env python3
"""Exact authored panel and conversion examples, without executing PyFixest."""
from fractions import Fraction as F
import json

def calculate():
    D=[[F(v)for v in row]for row in [[0,1,1],[0,0,1]]]
    Y=[[F(v)for v in row]for row in [[0,1,10],[0,0,1]]]
    n,t=2,3
    gm=sum(map(sum,D))/(n*t)
    residual=[[D[i][j]-sum(D[i])/t-sum(D[k][j]for k in range(n))/n+gm for j in range(t)]for i in range(n)]
    denominator=sum(v*v for row in residual for v in row)
    beta=sum(residual[i][j]*Y[i][j]for i in range(n)for j in range(t))/denominator
    att=sum(Y[i][j]for i in range(n)for j in range(t)if D[i][j]) / sum(map(sum,D))
    w=[F(1,4),F(3,4)];tau=[F(10),F(-2)];cov=[[F(4),F(1)],[F(1),F(9)]]
    aggregate=sum(a*b for a,b in zip(w,tau));var=sum(w[i]*cov[i][j]*w[j]for i in range(2)for j in range(2))
    diagonal=sum(w[i]**2*cov[i][i]for i in range(2))
    out=dict(twfe=dict(treatment=[[int(v)for v in row]for row in D],outcome=[[int(v)for v in row]for row in Y],
      residualized_treatment=[[str(v)for v in row]for row in residual],denominator=str(denominator),
      coefficient=str(beta),treated_cell_average=str(att),cost='2',projection_net=str(beta-2),target_net=str(att-2)),
      aggregation=dict(weights=list(map(str,w)),effects=list(map(str,tau)),weighted_effect=str(aggregate),
        equal_cohort_effect=str(sum(tau)/2),full_variance=str(var),diagonal_only_variance=str(diagonal)),
      conversion=dict(coded_month_difference=202601-202512,month_index_difference=1,
        two_nonzero_numeric_codes=[2,3],boolean_images=[bool(x)for x in [2,3]],
        adoption_period=2,observed_post_period=3,declared_relative=1,first_observed_relative=0),
      limits=['Independent exact toy panel, stipulated effect population and selected expression witnesses.',
       'Not a native PyFixest output, finite-sample coverage result, timing measurement or bank return.'])
    assert beta==F(-7,2) and att==4 and aggregate==1 and var==F(91,16) and diagonal==F(85,16)
    assert all(sum(residual[i])==0 for i in range(n))
    assert all(sum(residual[i][j]for i in range(n))==0 for j in range(t))
    return out
if __name__=='__main__':print(json.dumps(calculate(),indent=2))
