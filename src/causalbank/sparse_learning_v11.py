"""Prespecified sparse cross-fitted nuisance learner under blocked mixing."""
import numpy as np


def _standardize(x):
    mean=x.mean(axis=0); scale=x.std(axis=0); scale=np.where(scale>1e-8,scale,1.)
    return (x-mean)/scale, mean, scale


def lasso_fit(x,y,lam,steps=1200):
    x=np.asarray(x,float); y=np.asarray(y,float); z=np.sum(x*x,axis=0)/len(x); b=np.zeros(x.shape[1])
    for _ in range(steps):
        old=b.copy()
        for j in range(len(b)):
            partial=(x[:,j]@(y-x@b)+z[j]*len(x)*b[j])/len(x)
            b[j]=np.sign(partial)*max(abs(partial)-lam,0.)/max(z[j],1e-12)
        if np.max(abs(b-old))<1e-9: break
    return b


def _design(x): return np.column_stack((np.ones(len(x)),x))


def fit_sparse(x, targets, *, gap, penalties, bandwidth=None):
    x=np.asarray(x,float); y=np.asarray(targets,float); n,p=x.shape
    if y.shape!=(n,3) or n<80 or gap<1 or gap>=n//2: raise ValueError('sparse learner dimensions/gap invalid')
    xn,_,_=_standardize(x); d=_design(xn); middle=n//2; left=middle-gap//2; right=left+gap; spans=[(0,left),(right,n)]
    residuals=[]; folds=[]; selected=[]
    for fold,(e0,e1) in enumerate(spans):
        t0,t1=spans[1-fold]; tr=d[t0:t1]; val=d[e0:e1]; yy=y[t0:t1]; yv=y[e0:e1]; losses=[]
        for lam in penalties:
            co=np.column_stack([lasso_fit(tr[:,1:],yy[:,j],lam) for j in range(3)])
            losses.append(float(np.mean((yv-val[:,1:]@co)**2)))
        lam=float(penalties[int(np.argmin(losses))]); co=np.column_stack([lasso_fit(tr[:,1:],yy[:,j],lam) for j in range(3)])
        residuals.append(yv-val[:,1:]@co); folds.extend([fold]*(e1-e0)); selected.append(dict(penalty=lam,losses=losses,nonzero=int(np.count_nonzero(co))))
    r=np.vstack(residuals); folds=np.asarray(folds); z=r[:,2]; den=float(z@r[:,1]/len(r))
    if abs(den)<1e-8: return dict(status='unavailable_weak_instrument',selected=selected)
    est=float(z@r[:,0]/(z@r[:,1])); scores=z*(r[:,0]-est*r[:,1]); bw=int(bandwidth or len(r)**.2); center=scores-scores.mean(); var=float(center@center)
    for k in range(1,min(bw,len(center)-1)+1): var+=2*float(center[k:]@center[:-k])
    var/=len(r)**2*den**2
    if var<=0 or not np.isfinite(var): return dict(status='unavailable_score_variance',selected=selected)
    se=float(np.sqrt(var)); return dict(status='computed',estimate=est,standard_error=se,interval=[est-1.96*se,est+1.96*se],denominator=den,bandwidth=bw,selected=selected,nonzero=sum(s['nonzero'] for s in selected),residual_rows=len(r),inference=dict(method='blocked_cross_fitted_sparse_lasso_iv',confidence_level=.95,sampling_unit='separated calendar blocks under geometric mixing',coverage_claim='conditional asymptotic with sparse approximation/product and score covariance rates',limitations='fixed sparse linear family; no arbitrary learner or finite universal guarantee'))


def fit_dense(x, targets, *, gap, bandwidth=None):
    x=np.asarray(x,float); y=np.asarray(targets,float); n=len(x); xn,_,_=_standardize(x); d=_design(xn); middle=n//2; left=middle-gap//2; right=left+gap; spans=[(0,left),(right,n)]; residuals=[]
    for fold,(e0,e1) in enumerate(spans):
        t0,t1=spans[1-fold]; co=np.linalg.lstsq(d[t0:t1,1:],y[t0:t1],rcond=None)[0]; residuals.append(y[e0:e1]-d[e0:e1,1:]@co)
    r=np.vstack(residuals); z=r[:,2]; den=float(z@r[:,1]/len(r)); est=float(z@r[:,0]/(z@r[:,1])); scores=z*(r[:,0]-est*r[:,1]); center=scores-scores.mean(); bw=int(bandwidth or len(r)**.2); v=float(center@center)+sum(2*float(center[k:]@center[:-k]) for k in range(1,min(bw,len(center)-1)+1)); se=float(np.sqrt(v/len(r)**2/den**2)); return dict(status='computed',estimate=est,standard_error=se,interval=[est-1.96*se,est+1.96*se],denominator=den,bandwidth=bw,residual_rows=len(r))
