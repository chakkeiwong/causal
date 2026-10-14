#!/usr/bin/env python3
"""Exact graph-class and temporal residualization fixtures."""
import json, sys
from pathlib import Path
import numpy as np
sys.path.insert(0,'src')
from causalbank.temporal_graph_v11 import simulate, residual_window, infer, exact_class
from causalbank.latent_temporal_sets import unrestricted_witness
from master_experiment import atomic

ROOT=Path(__file__).resolve().parents[1]
def main():
    g=dict(tau=.8,y_lag=.55,u_to_a=.55,u_to_y=.5)
    x=simulate(g,2000,4,202610110404)
    r=residual_window(x)
    assert r.shape==(6000,3) and np.isfinite(r).all()
    obs=infer(x,'observational_latent'); assert obs['components'][0]==(-np.inf,np.inf)
    finite=infer(x,'randomized_encouragement')
    assert finite['components'] and all(a<=exact_class(g)<=b for a,b in finite['components'])
    cov=np.array([[1.,.3,.2],[.3,1.2,.4],[.2,.4,1.4]])
    for b in (-10.,0.,10.):
        w=unrestricted_witness(cov,b); assert np.allclose(w['recovered_covariance'],cov,atol=1e-8)
    atomic(ROOT/'docs/program/master/work/R04/fixtures.json',dict(status='pass',temporal_rows=len(r),observational_effect_set=obs['effect_set'],randomized_effect_set=finite['effect_set'],exact_member=exact_class(g),retained_observational_graphs=obs['retained_graphs'],checks=['Lag residualization dimensions','Finite member inside randomized outer set','Observational unrestricted set retained','Three observationally equivalent structural witnesses recover same covariance']))
    print('R04 temporal graph fixtures pass.')
if __name__=='__main__': main()
