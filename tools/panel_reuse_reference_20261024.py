#!/usr/bin/env python3
"""Exact authored semantic fixtures; never import or execute upstream software."""
from fractions import Fraction as F
import json

def calculate():
    treated=[F(10),F(14)];control=[F(2),F(4)];odds=[F(1),F(999)]
    imp_all=(sum(treated)-sum(o*y for o,y in zip(odds,control)))/2
    imp_trim=(sum(treated)-control[0])/2
    trad_all=sum(treated)/2-sum(o*y for o,y in zip(odds,control))/sum(odds)
    trad_trim=sum(treated)/2-control[0]
    assert (imp_all,imp_trim,trad_all,trad_trim)==(F(-1987),F(11),F(4001,500),F(10))
    fixed=F(1,2);generated=fixed+F(1,2);assert generated==1
    intended=[F(1,4),F(1,9)];shape_branch=[F(1,2),F(1,3)]
    assert intended!=shape_branch
    # Two equal-sized cohorts, per-person gains 20 and 100 USD; sample treatment rates .8 and .2.
    ate=(F(20)+F(100))/2;att=(F(4,5)*20+F(1,5)*100);assert (ate,att)==(60,36)
    return dict(kind='authored_exact_arithmetic_not_native_output',
        clipping=dict(D=[1,1,0,0],propensity=['1/2','1/2','1/2','999/1000'],outcome_residual=['10','14','2','4'],weights=[1,1,1,1],trim_level='199/200',
          improved_all=str(imp_all),improved_trimmed=str(imp_trim),traditional_all=str(trad_all),traditional_trimmed=str(trad_trim),
          restriction='Supplied nuisance values are not claimed to be attainable fitted calibration equations. This is an adapter arithmetic fixture, not an estimator comparison or theorem counterexample.'),
        generated_baseline=dict(independent_unit_variance=True,treated_n=2,untreated_n=2,fixed_baseline_variance=str(fixed),full_variance=str(generated),ratio=str(generated/fixed)),
        rhs_shape=dict(X_diagonal=[2,3],B='2x2 identity supplied as already formed cross-product',intended_diagonal=list(map(str,intended)),ambiguous_branch_diagonal=list(map(str,shape_branch)),restriction='Algebraic dispatch witness only; reachability from an actual full-rank did2s fit remains unverified.'),
        target=dict(ATE_USD=str(ate),ATT_USD=str(att),cost_per_treated_USD='40',ATE_substitution_margin=str(ate-40),ATT_margin=str(att-40)),
        native_execution=False,measured_bank_benefit=False)
if __name__=='__main__':print(json.dumps(calculate(),indent=2))
