"""Outer effect confidence over a finite Gaussian episode structural class.

Three ordered nodes Z,A,Y; one possible latent root; no arbitrary coefficient
bounds. Necessary covariance restrictions conservatively retain parameters.
"""
from itertools import product
import numpy as np
from scipy.stats import chi2
from .linkage_sets import merge_intervals,encode_set


def covariance_region(data,alpha=.05):
    x=np.asarray(data,float)
    if x.ndim!=2 or x.shape[1]!=3 or len(x)<5 or not np.all(np.isfinite(x)) or not 0<alpha<1:
        raise ValueError('finite independent Gaussian episodes for Z,A,Y required')
    # 3 coordinate variances and both signs of each of the 3 pairs: 9 regions.
    df=len(x)-1;error=alpha/9
    lowq,highq=chi2.ppf([error/2,1-error/2],df)
    def band(v):
        ss=df*np.var(v,ddof=1)
        return np.array([ss/highq,ss/lowq])
    region=np.empty((3,3,2))
    for j in range(3):region[j,j]=band(x[:,j])
    for j in range(3):
        for k in range(j):
            plus,minus=band(x[:,j]+x[:,k]),band(x[:,j]-x[:,k])
            region[j,k]=region[k,j]=[(plus[0]-minus[1])/4,(plus[1]-minus[0])/4]
    return region


def ratio_region(numerator,denominator):
    a,b=map(float,numerator);c,d=map(float,denominator)
    if c<=0<=d and a<=0<=b:return [(-np.inf,np.inf)]
    pieces=[]
    if c<0:
        end=min(d,0.)
        vals=[n/q for n in (a,b) for q in (c,end) if q]
        if end==0:
            vals += [-np.inf if n>0 else np.inf for n in (a,b) if n]
        pieces.append((min(vals),max(vals)))
    if d>0:
        start=max(c,0.)
        vals=[n/q for n in (a,b) for q in (start,d) if q]
        if start==0:
            vals += [np.inf if n>0 else -np.inf for n in (a,b) if n]
        pieces.append((min(vals),max(vals)))
    return merge_intervals(pieces)


def multiply(a,b):
    corners=[x*y for x in a for y in b];return np.array([min(corners),max(corners)])


def subtract(a,b):return np.array([a[0]-b[1],a[1]-b[0]])


def graph_class(information):
    if information not in ('observational_latent','randomized_encouragement','observed_sufficiency'):
        raise ValueError('unsupported graph/information class')
    roots=[(),(1,2)] if information=='randomized_encouragement' else ([()] if information=='observed_sufficiency' else [(),(0,1),(0,2),(1,2),(0,1,2)])
    return [dict(edges=[name for name,yes in zip(('Z_to_A','Z_to_Y','A_to_Y'),bits) if yes],latent_support=list(root))
            for bits,root in product(product([0,1],repeat=3),roots)
            if information!='randomized_encouragement' or not bits[1]]


def effect_set(data,*,information='observational_latent',sampling='independent_gaussian_episodes',alpha=.05):
    if sampling!='independent_gaussian_episodes':
        raise ValueError('this covariance region is not a dependent-calendar or infinite-history guarantee')
    region=covariance_region(data,alpha);graphs=graph_class(information);rows=[];union=[]
    for graph in graphs:
        edges=graph['edges'];reason='retained by conservative necessary restrictions'
        if information=='randomized_encouragement':
            numerator=region[0,2];denominator=region[0,1]
            if 'Z_to_A' not in edges:
                pieces=[(-np.inf,np.inf)] if denominator[0]<=0<=denominator[1] and numerator[0]<=0<=numerator[1] else []
            else:pieces=ratio_region(numerator,denominator)
            if 'A_to_Y' not in edges:
                pieces=[(0.,0.)] if numerator[0]<=0<=numerator[1] and pieces else []
        elif information=='observed_sufficiency' or not graph['latent_support']:
            numerator=subtract(multiply(region[1,2],region[0,0]),multiply(region[0,1],region[0,2]))
            denominator=subtract(multiply(region[1,1],region[0,0]),multiply(region[0,1],region[0,1]))
            pieces=ratio_region(numerator,denominator) if denominator[0]>0 else [(-np.inf,np.inf)]
            if 'A_to_Y' not in edges:pieces=[(0.,0.)] if any(a<=0<=b for a,b in pieces) else []
        else:
            pieces=[(-np.inf,np.inf)] if 'A_to_Y' in edges else [(0.,0.)]
            reason='outer relaxation retains latent parameter space; no unsupported optimizer exclusion'
        rows.append(dict(graph=graph,effect_set=encode_set(pieces),reason=reason));union+=pieces
    return dict(status='computed_set',effect_set=encode_set(merge_intervals(union)),covariance_region=region,
                enumerated_graphs=len(graphs),graphs=rows,
                inference={'method':'simultaneous_covariance_region_outer_structural_projection','confidence_level':1-alpha,
                           'sampling_unit':'independent Gaussian episode with finite Z,A,Y window',
                           'coverage_claim':'finite-sample covariance inclusion via 9 chi-square pivots and Bonferroni, conditional on declared structural class',
                           'information':information,'numerical_status':'analytic interval outer relaxation, not sharp identification',
                           'empirical_qualification':'synthetic model-class construction; exclusions supplied, not discovered'},
                next_information='Validate randomized encouragement and exclusion, or measure sufficient confounders' if information=='observational_latent' else None)


def unrestricted_witness(covariance,effect):
    """Same SPD observed covariance for any finite effect in the broad class."""
    s=np.asarray(covariance,float);b=float(effect)
    if s.shape!=(3,3) or not np.allclose(s,s.T) or np.linalg.eigvalsh(s).min()<=0:
        raise ValueError('positive definite covariance required')
    a=s[0,1]/s[0,0];c=s[0,2]/s[0,0]-b*a
    va=s[1,1]-s[0,1]**2/s[0,0]
    cov=s[1,2]-s[0,1]*s[0,2]/s[0,0]
    vy=s[2,2]-s[0,2]**2/s[0,0]
    w=cov-b*va;v=vy-2*b*cov+b*b*va
    la=np.sqrt((va+w*w/v)/2);ly=w/la
    B=np.array([[0.,0.,0.],[a,0.,0.],[c,b,0.]])
    loading=np.array([0.,la,ly]);D=np.diag([s[0,0],va-la*la,v-ly*ly])
    inverse=np.linalg.solve(np.eye(3)-B,np.eye(3));recovered=inverse@(np.outer(loading,loading)+D)@inverse.T
    return dict(B=B,loading=loading,noise_variances=np.diag(D),recovered_covariance=recovered,effect=inverse[2,1])
