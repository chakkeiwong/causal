#!/usr/bin/env python3
"""Independent finite examples; no package code execution or coverage claim."""
from fractions import Fraction as F
from pathlib import Path
import json
def q7(values,p):
    x=sorted(map(F,values));h=(len(x)-1)*p;j=h.numerator//h.denominator
    return x[j] if j==len(x)-1 else x[j]+(h-j)*(x[j+1]-x[j])
def calculate():
    fit=F(100);w=(-F(5),F(5));e=(-F(10),F(10));y=F(120)
    prediction=[fit+w[0]+e[0],fit+w[1]+e[1]]
    effect=[y-prediction[1],y-prediction[0]]
    assert prediction==[85,115] and effect==[5,35]
    full=q7([0]*9+[100],F(39,40));observed=q7([0]*9,F(39,40))
    assert full==F(155,2) and observed==0
    low_given=True;high_given=False
    lower_est=not low_given;upper_est=not high_given
    forwarded=(lower_est,lower_est)
    assert (lower_est,upper_est)==(False,True) and not any(forwarded)
    return dict(provenance='Authored exact calculations; not returned package output or calibrated bank evidence',intervals=dict(fit_thousand_usd=str(fit),weight_error=list(map(str,w)),prediction_error=list(map(str,e)),counterfactual=list(map(str,prediction)),observed=str(y),effect=list(map(str,effect)),union_bound_coverage=str(1-F(1,20)-F(1,20)),scope='If both component error guarantees hold, union bound gives at least0.90; no automatic0.95combined claim'),failed_tail=dict(full_sample_upper_type7=str(full),successful_only_upper_type7=str(observed),failure_fraction='1/10',scope='The removed100is an authored hypothetical missing-tail value, not inferable from a failed solve'),asymmetric_bounds=dict(requested=[lower_est,upper_est],forwarded=list(forwarded),helper_runs=any(forwarded),scope='Static Boolean witness: supplied lower only suppresses needed upper in inspected gaussian/LS dispatch'),matrix=dict(input_diagonal=['-1','4'],svd_based_root_diagonal=['1','2'],root_square=['1','4'],scope='An indefinite input is not repaired into its own square root; require PSD validation'),economics=dict(illustrative_usd=4200,attempted=210,completed=175,usable=140,costs_usd=[str(F(4200,n)) for n in [210,175,140]]),native_execution=False)
if __name__=='__main__':
    p=Path(__file__).resolve().parents[1]/'docs/program/execution/2026-10-24/scpi-reuse-v1/exact-results.json'
    assert not p.exists();p.write_text(json.dumps(calculate(),indent=2)+chr(10));print(json.dumps(calculate()))
