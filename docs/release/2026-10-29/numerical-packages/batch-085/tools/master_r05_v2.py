import numpy as np
from scipy.signal import lfilter
from causalbank.sparse_learning_v2 import estimate

def request(spec,cell,index):
    d=spec['designs'][cell];rng=np.random.default_rng([spec['seed'],cell,index]);n=d.get('origins',spec['origins']);p=d.get('features',spec['features']);s=d.get('sparsity',spec['sparsity']);rho=d.get('rho',.45)
    eps=rng.normal(size=(n,p))*np.sqrt(1-rho*rho);eps[0]/=np.sqrt(1-rho*rho);x=lfilter([1.],[1.,-rho],eps,axis=0)
    beta=np.zeros(p);gamma=np.zeros(p);beta[:s]=np.linspace(.5,.1,s);gamma[:s]=np.linspace(.3,.05,s)
    nonlinear=.6*(x[:,0]**2-1) if d.get('misspecification') else 0.
    z=x@beta+nonlinear+rng.normal(size=n);a=d.get('instrument_strength',.8)*z+x@gamma+rng.normal(size=n);y=spec['truth']*a+x@gamma+nonlinear+rng.normal(size=n)
    gap=d.get('gap',spec['gap']);targets=np.column_stack((y,a,z))
    penalties=(np.array(spec['penalty_multiples'])*np.sqrt(np.log(p+1)/((n-gap)/2))).tolist()
    return dict(truth=spec['truth'],methods=dict(nested_sparse=estimate(x,targets,gap,penalties,spec['alpha']),dense_reference=estimate(x,targets,gap,penalties,spec['alpha'],dense=True)),history_rows=n*p,labels=0,actual_features=p,actual_support=s)
