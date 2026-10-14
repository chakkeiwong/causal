"""Mergeable score means and crossed-cluster covariance; no causal identification."""
import numpy as np


class ScoreReducer:
    """Precomputed equal-row score vectors with declared integer cluster keys.

    Callers own target weighting, nuisance training and dependence assumptions.
    Intersections are retained, including repeated observations in the same cell.
    """
    def __init__(self, n_entities, n_dates, dimension=1):
        if min(n_entities,n_dates,dimension)<1: raise ValueError('POSITIVE_DIMENSIONS_REQUIRED')
        self.ne,self.nt,self.d=n_entities,n_dates,dimension
        self.n=0; self.total=np.zeros(dimension)
        self.groups=[np.zeros((n_entities,dimension)),np.zeros((n_dates,dimension)),np.zeros((n_entities*n_dates,dimension))]
        self.counts=[np.zeros(n_entities,np.int64),np.zeros(n_dates,np.int64),np.zeros(n_entities*n_dates,np.int64)]

    def add(self, scores, entities, dates):
        scores=np.asarray(scores,float); entities=np.asarray(entities); dates=np.asarray(dates)
        if scores.ndim!=2 or scores.shape[1]!=self.d or entities.ndim!=1 or dates.ndim!=1 or len(scores)!=len(entities) or len(scores)!=len(dates): raise ValueError('SCORE_SHAPE')
        if not np.isfinite(scores).all(): raise ValueError('NONFINITE_SCORE')
        if entities.dtype.kind not in 'iu' or dates.dtype.kind not in 'iu': raise ValueError('INTEGER_CLUSTERS_REQUIRED')
        if len(scores)==0: return
        if entities.min()<0 or entities.max()>=self.ne or dates.min()<0 or dates.max()>=self.nt: raise ValueError('CLUSTER_RANGE')
        self.n+=len(scores); self.total+=scores.sum(0)
        for raw,key,count in zip(self.groups,[entities,dates,entities*self.nt+dates],self.counts):
            count+=np.bincount(key,minlength=len(count))
            for k in range(self.d): raw[:,k]+=np.bincount(key,weights=scores[:,k],minlength=len(count))

    def merge(self,other):
        if (self.ne,self.nt,self.d)!=(other.ne,other.nt,other.d): raise ValueError('INCOMPATIBLE_REDUCERS')
        self.n+=other.n; self.total+=other.total
        for a,b in zip(self.groups,other.groups): a+=b
        for a,b in zip(self.counts,other.counts): a+=b
        return self

    def result(self):
        if self.n<2: raise ValueError('INSUFFICIENT_SCORES')
        mean=self.total/self.n; covs=[]; numbers=[]
        for raw,count in zip(self.groups,self.counts):
            mask=count>0; g=int(mask.sum()); numbers.append(g)
            if g<2: raise ValueError('INSUFFICIENT_CLUSTERS')
            centered=raw[mask]-count[mask,None]*mean
            covs.append((g/(g-1))*(centered.T@centered)/self.n**2)
        cov=covs[0]+covs[1]-covs[2]
        eigen=np.linalg.eigvalsh(cov)
        return {'n_scores':self.n,'mean':mean.tolist(),'covariance':cov.tolist(),
                'cluster_counts':dict(zip(['entity','date','intersection'],numbers)),
                'minimum_eigenvalue':float(eigen.min()),
                'flags':['INDEFINITE_CLUSTER_COVARIANCE'] if eigen.min() < -1e-12 else [],
                'scope':'Equal-row precomputed scores; scientific weighting and dependence assumptions supplied by caller'}
