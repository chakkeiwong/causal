#!/usr/bin/env python3
"""Exact authored IV rank/exclusion witness and diagnostic scaling example."""
from fractions import Fraction as F
from math import exp
import json


def calculate():
    z=list(map(F,[-1,-1,1,1]));u=list(map(F,[-1,1,-1,1]))
    dot=lambda a,b:sum(x*y for x,y in zip(a,b))
    assert dot(z,u)==0 and dot(z,z)==dot(u,u)==4
    rows=[]
    for epsilon in [F(0),F(1,100),F(1,1000)]:
        d=[epsilon*a+b for a,b in zip(z,u)]
        y=[2*a+F(1,100)*b for a,b in zip(d,z)]
        gram=dot(z,d)**2/dot(z,z)
        assert dot(d,d)>0 and dot(z,z)>0
        if epsilon==0:
            assert gram==0
            coefficient=None
        else:
            coefficient=dot(z,y)/dot(z,d)
            assert coefficient==2+F(1,100)/epsilon
        rows.append(dict(epsilon=str(epsilon),d_gram=str(dot(d,d)),z_gram='4',
            projected_gram=str(gram),coefficient=None if coefficient is None else str(coefficient)))
    assert [r['coefficient'] for r in rows]==[None,'3','12']
    # W=8 and two restrictions: chi-square_2 survival versus F(2,20) survival.
    w=F(8);q=2;f=w/q
    fp=(1+F(2,20)*f)**-10
    return dict(status='pass_for_authored_finite_reference',native_execution=False,
        law='Four fixed centered rows; d=epsilon*z+u; y=2*d+z/100. The z/100 term violates exclusion.',
        rank_and_exclusion=rows,diagnostic=dict(wald_quadratic=str(w),restrictions=q,
            f_scaled=str(f),chi_square_2_p=exp(-4),f_2_20_p=float(fp),f_2_20_p_exact=str(fp)),
        limits=['One-column full rank of d and z is not full rank of the projected design.',
            'This is an exact sensitivity witness, not a weak-instrument sampling experiment or upstream output.',
            'P-value comparison stipulates reference distributions; neither is automatically valid for a bank.'])


if __name__=='__main__':print(json.dumps(calculate(),indent=2))
