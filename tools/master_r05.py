"""Sparse nuisance learner versus dense reference under blocked dependence."""
import numpy as np
from causalbank.sparse_learning_v11 import fit_sparse, fit_dense


def request(spec, cell, index):
    d=spec['designs'][cell]; rng=np.random.default_rng([spec['seed'],cell,index]); n=d.get('origins',spec['origins']); p=spec['features']; rho=d.get('rho',.45); x=np.empty((n,p)); x[0]=rng.normal(size=p)
    for t in range(1,n): x[t]=rho*x[t-1]+np.sqrt(1-rho*rho)*rng.normal(size=p)
    beta=np.zeros(p); gamma=np.zeros(p); beta[:spec['sparsity']]=np.linspace(.5,.1,spec['sparsity']); gamma[:spec['sparsity']]=np.linspace(.3,.05,spec['sparsity'])
    if d.get('misspecification'): gamma[spec['sparsity']:spec['sparsity']+2]=.08
    z=x@beta+rng.normal(size=n); a=d.get('instrument_strength',.8)*z+x@gamma+rng.normal(size=n); y=spec['truth']*a+x@gamma+rng.normal(size=n)
    targets=np.column_stack((y,a,z)); gap=d.get('gap',spec['gap'])
    sparse=fit_sparse(x,targets,gap=gap,penalties=spec['penalties']); dense=fit_dense(x,targets,gap=gap)
    return dict(truth=spec['truth'],methods=dict(sparse_lasso=sparse,dense_reference=dense),history_rows=n*p,labels=0,features=p)
