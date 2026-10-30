#!/usr/bin/env python3
"""Independent rational contract witnesses; never imports downloaded software."""
from fractions import Fraction as F
import json

def calculate():
    t=F(3,10); intervention=100; cost=20
    a=b=F(1,200); z=a*b
    lower=z*z; upper=lower/(1-z*z/12)
    assert 0<lower<upper<F(1,10**8)
    equality_z=F(1,10000)
    assert equality_z**2==F(1,10**8)
    scales=[F(10),F(1),F(100)]
    w=[[F(0),F(2),F(1)],[F(0),F(0),F(3)],[F(0),F(0),F(0)]]
    transformed=[[scales[i]*w[i][j]/scales[j] for j in range(3)] for i in range(3)]
    total=w[0][2]+w[0][1]*w[1][2]
    scaled=transformed[0][2]+transformed[0][1]*transformed[1][2]
    assert total==7 and scaled==F(7,10)
    def encode(x):
        if isinstance(x,F): return str(x)
        if isinstance(x,dict): return {k:encode(v) for k,v in x.items()}
        if isinstance(x,list): return [encode(v) for v in x]
        return x
    return encode(dict(scope='Authored exact witnesses; no engine output or empirical calibration',
        threshold=dict(weight=t,threshold=t,original_retains=True,gcastle_retains=False,
            assumed_intervention=intervention,assumed_cost_usd=cost,
            original_margin_usd=t*intervention-cost,gcastle_thresholded_margin_usd=-cost),
        cycle=dict(weights=[a,b],chosen_threshold=F(1,1000),residual_strict_lower=lower,
            residual_upper=upper,tolerance=F(1,10**8),support_is_cycle=True,
            derivation='h_exp=2(cosh(ab)-1); z^2<h_exp<=z^2/(1-z^2/12) for z=1/40000'),
        formula_comparison=dict(weights=[F(1,100),F(1,100)],
            exponential_strict_lower=equality_z**2,polynomial=equality_z**2/2,
            tolerance=F(1,10**8),exponential_exceeds_tolerance=True,polynomial_below_tolerance=True),
        units=dict(original=w,scales=scales,transformed=transformed,total_original=total,total_transformed=scaled,
            identity='Z=X D^-1, W_Z=D W_X D^-1; fixed raw thresholds are not unit invariant'),
        nonlinear=dict(functions=['4 sigmoid(2x)-2','-4 sigmoid(2x)+2'],first_layer_norm=2,
            local_derivatives=[2,-2],assumed_usd_per_outcome=100,assumed_cost_per_intensity=20,
            local_net_derivatives_usd=[180,-220],finite_intervention_claim=False)))

if __name__=='__main__': print(json.dumps(calculate(),indent=2))
