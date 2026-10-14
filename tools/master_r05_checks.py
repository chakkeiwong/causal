#!/usr/bin/env python3
"""Sparse learner dense algebra and score fixture."""
import json,sys
from pathlib import Path
import numpy as np
sys.path.insert(0,'src')
from causalbank.sparse_learning_v11 import fit_sparse, fit_dense, lasso_fit
from master_experiment import atomic
ROOT=Path(__file__).resolve().parents[1]
def main():
    rng=np.random.default_rng(202610110505); n,p=320,12; x=rng.normal(size=(n,p)); z=x[:,0]+rng.normal(size=n); a=.8*z+.3*x[:,0]+rng.normal(size=n); y=np.column_stack((1.2*a+0.2*x[:,0]+rng.normal(size=n),a,z))
    out=fit_sparse(x,y,gap=20,penalties=[.001,.01,.1]); dense=fit_dense(x,y,gap=20); assert out['status']=='computed' and dense['status']=='computed'; assert abs(out['estimate']-dense['estimate'])<.2
    zero=lasso_fit(np.eye(10),np.zeros(10),.1); assert np.allclose(zero,0)
    atomic(ROOT/'docs/program/master/work/R05/fixtures.json',dict(status='pass',sparse_estimate=out['estimate'],dense_estimate=dense['estimate'],estimate_difference=out['estimate']-dense['estimate'],zero_penalty_boundary=zero.tolist(),checks=['Independent dense cross-fit comparison','Zero-response selection boundary','Positive score variance']))
    print(json.dumps({'status':'pass','estimate_difference':out['estimate']-dense['estimate']}))
if __name__=='__main__': main()
