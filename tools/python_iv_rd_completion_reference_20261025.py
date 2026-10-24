#!/usr/bin/env python3
"""Exact authored target, numerical and reporting witnesses; no package execution."""
from fractions import Fraction as F
import json

def calculate():
    jump=F(10);left_slope=F(2);right_slope=F(6)
    contrasts={str(e):str(jump+(left_slope+right_slope)*e) for e in [F(1,2),F(1,1000)]}
    assert contrasts=={'1/2':'14','1/1000':'1251/125'}
    fuzzy={str(t):str(F(2)/t) for t in [F(1,5),F(1,50)]}
    assert fuzzy=={'1/5':'10','1/50':'100'}
    z=[F(10)/2,F(8)/2,F(8)/3]
    halfwidth=[F(49,25)*s for s in [F(2),F(2),F(3)]]
    sets={str(x): bool(1-x*x<=0) for x in [F(-2),F(-1),F(0),F(1),F(2)]}
    assert sets=={'-2':True,'-1':True,'0':False,'1':True,'2':True}
    # Rank tolerance in a one-column Gram matrix is affected by physical scaling.
    gram=F(1,10**8);tol=F(1,10**6)
    scale=F(100);scaled_gram=gram*scale*scale
    assert gram<tol and scaled_gram>=tol
    costs={str(n):str(F(18000,n)) for n in [600,450,300]}
    return dict(finite_epsilon_contrasts=contrasts,true_jump=str(jump),
                fuzzy_ratios=fuzzy,three_row_z=list(map(str,z)),
                assumed_1_96_halfwidth=list(map(str,halfwidth)),
                disconnected_quadratic_membership=sets,hull_adds_excluded_zero=True,
                gram=str(gram),scaled_gram=str(scaled_gram),absolute_rank_tolerance=str(tol),
                native_execution=False,calibration_claim=False,
                hypothetical_costs_usd=costs)

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
