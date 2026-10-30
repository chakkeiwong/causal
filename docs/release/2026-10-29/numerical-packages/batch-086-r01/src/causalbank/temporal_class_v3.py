"""Stationary Gaussian scalar-lag union over finite scientific graph classes."""
import numpy as np
from scipy.signal import lfilter
from .latent_temporal_sets import effect_set
from .gaussian_effect_pivots import effect_confidence
from .linkage_sets import decode_set,encode_set,merge_intervals

def innovation(rng,n,law):
    z,u,ea,ey=rng.normal(size=(4,n))
    a=law.get('strength',.8)*z+law.get('ua',.6)*u+ea
    y=law.get('tau',.8)*a+law.get('direct',0.)*z+law.get('uy',.7)*u+ey
    return np.column_stack((z,a,y))

def simulate(n,rng,law):
    rho=law.get('rho',.4)
    eps=innovation(rng,n+1,law)
    eps[0]/=np.sqrt(1-rho*rho)
    x=lfilter([1.],[1.,-rho],eps,axis=0)
    if law.get('hidden_history'):
        # Added independent stationary latent history: scalar AR class is false.
        latent=rng.normal(size=n+1);latent[0]/=np.sqrt(1-.96**2)
        latent=lfilter([1.],[1.,-.96],latent)
        x[:,1]+=latent;x[:,2]+=.9*latent
    if law.get('selection'):
        # Outcome-dependent selection destroys the Gaussian innovation experiment.
        keep=x[:,1]+x[:,2]>0
        x=x[keep]
    return x

def infer(x,rhos,information,alpha=.01):
    if x.ndim!=2 or x.shape[1]!=3 or len(x)<10 or not np.isfinite(x).all():
        raise ValueError('Finite stationary three-variable calendar required')
    if not rhos or any(abs(r)>=1 for r in rhos):raise ValueError('Finite stable candidate lag set required')
    pieces=[]; rows=[]
    for rho in rhos:
        eps=x[1:]-rho*x[:-1]
        out=effect_set(eps,information=information,alpha=alpha)
        graphs=[g for g in out['graphs'] if g['effect_set']]
        pieces.extend(decode_set(out['effect_set']))
        rows.append(dict(rho=rho,graphs=graphs,effect_set=out['effect_set']))
    return dict(status='computed_set',effect_set=encode_set(merge_intervals(pieces)),
        candidates=rows,retained_graphs=sum(len(r['graphs']) for r in rows),
        scope='Exact Gaussian innovation covariance bands at the true candidate lag; union retains all finite lag candidates and compatible graphs. True lag and scientific graph restrictions must belong to the declared class.')

def selected_challenger(x,rhos,information):
    rho=min(rhos,key=lambda r:np.mean((x[1:]-r*x[:-1])**2))
    out=effect_confidence(x[1:]-rho*x[:-1],information=information)
    return dict(status=out['status'],effect_set=out.get('effect_set',[]),selected_rho=rho,
        scope='Selected-lag 95% Gaussian pivot challenger; selection is not accounted for and is not qualified.')
