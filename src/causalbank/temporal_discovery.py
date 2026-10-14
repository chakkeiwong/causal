"""A restricted lag-one structural Gaussian model with graph/response outer bands."""
import numpy as np
from scipy.stats import norm

from .discovery_sets import add,multiply


def interval_matrix_product(a,b):
    p=len(a)
    return [[sum_intervals([multiply(a[i][k],b[k][j]) for k in range(p)])
             for j in range(p)] for i in range(p)]


def sum_intervals(values):
    result=(0.,0.)
    for value in values:
        result=add(result,value)
    return result


def fit_temporal_class(x,horizon=8,alpha=.05):
    """Assumes observed stable VAR(1), independent innovations, no instant edges.

    Zero coefficients are not forced after testing. The complete coefficient
    box defines a graph class and maps to conservative impulse-response bands.
    """
    n=len(x)-1; p=x.shape[1]
    lag,current=x[:-1],x[1:]
    q=lag.T@lag/n
    inverse=np.linalg.inv(q)
    f=np.linalg.solve(q,lag.T@current/n).T
    residual=current-lag@f.T
    score=(residual[:,:,None]*(lag@inverse)[:,None,:]).reshape(n,-1)
    covariance=np.cov(score,rowvar=False,ddof=1)/n
    radius=norm.ppf(1-alpha/(2*p*p))*np.sqrt(np.diag(covariance)).reshape(p,p)
    lower,upper=f-radius,f+radius
    box=[[(float(lower[i,j]),float(upper[i,j])) for j in range(p)] for i in range(p)]
    power=[[(float(i==j),float(i==j)) for j in range(p)] for i in range(p)]
    effects=[]
    for h in range(horizon+1):
        effects.append(power)
        power=interval_matrix_product(power,box)
    return {"kind":"temporal_graph_and_response_outer_set","coefficient":f.tolist(),
            "coefficient_bounds":box,"coefficient_covariance":covariance.tolist(),
            "edge_marks":[["present" if lower[i,j]>0 or upper[i,j]<0 else "zero_or_nonzero" for j in range(p)] for i in range(p)],
            "response_bounds":effects,"alpha":alpha,
            "scope":"Asymptotic simultaneous coefficient coverage and its fixed-horizon polynomial image; supplied causal sufficiency/no-instantaneous-edge model."}
