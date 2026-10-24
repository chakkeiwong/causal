#!/usr/bin/env python3
"""Exact authored panel witnesses; acquired libraries are never imported."""
from fractions import Fraction as F
from itertools import product
import json

def calculate():
    treatment=[[F(0),F(1),F(1)],[F(0),F(0),F(1)]]
    outcomes=[[F(0),F(1),F(10)],[F(0),F(0),F(1)]]
    def within(a):
        row=[sum(v)/3 for v in a]
        col=[sum(a[g][t] for g in range(2))/2 for t in range(3)]
        grand=sum(map(sum,a))/6
        return [[a[g][t]-row[g]-col[t]+grand for t in range(3)] for g in range(2)]
    d,y=within(treatment),within(outcomes)
    denominator=sum(v*v for row in d for v in row)
    numerator=sum(d[g][t]*y[g][t] for g in range(2) for t in range(3))
    beta=numerator/denominator
    weights=[d[0][1]/denominator,d[0][2]/denominator,d[1][2]/denominator]
    assert weights==[F(1),F(-1,2),F(1,2)] and beta==F(-7,2)
    att=F(1+10+1,3);assert att==4
    cluster_means=[F(z1+z2,2) for z1,z2 in product([-1,1],repeat=2)]
    iid_means=[F(sum(z),4) for z in product([-1,1],repeat=4)]
    cluster_var=sum(v*v for v in cluster_means)/len(cluster_means)
    iid_var=sum(v*v for v in iid_means)/len(iid_means)
    assert cluster_var==F(1,2) and iid_var==F(1,4)
    x2,sigma2=F(2),F(9)
    inverse=1/x2;cov=sigma2*inverse
    assert inverse==F(1,2) and cov==F(9,2)
    did=(F(15)-10)-(F(12)-10)
    assert did==3
    return dict(twfe=dict(treatment=[[int(v) for v in r] for r in treatment],outcomes=[[int(v) for v in r] for r in outcomes],residualized_treatment=[[str(v) for v in r] for r in d],denominator=str(denominator),treated_cell_weights=[str(v) for v in weights],coefficient=str(beta),equal_treated_cell_effect=str(att),untreated_controls_available_at_last_period=False),
        sampling=dict(two_cluster_four_row_variance=str(cluster_var),four_independent_rows_variance=str(iid_var),empirical_package_coverage=False),
        covariance=dict(inverse_gram=str(inverse),residual_variance=str(sigma2),scaled_covariance=str(cov),unscaled_is_covariance=False),
        trend=dict(observed_did=str(did),world_a=dict(untreated_treated_post=12,effect=3),world_b=dict(untreated_treated_post=15,effect=0),observed_cells_identical=True),
        cost=dict(illustrative_usd=2400,submitted=100,usable=60,per_submission='24',per_usable='40',observed_price=False),native_execution=False)

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
