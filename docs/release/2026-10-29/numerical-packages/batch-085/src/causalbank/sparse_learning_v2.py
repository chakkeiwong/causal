"""Training-only nested selection and fold-respecting covariance."""
import numpy as np
from scipy.stats import norm

def lasso(x,y,penalty,tolerance=1e-8):
    xm=x.mean(0);xs=x.std(0);xs=np.where(xs>1e-10,xs,1.)
    ym=y.mean(0);z=(x-xm)/xs;v=y-ym;coef=np.zeros((x.shape[1],y.shape[1]));res=v.copy();energy=np.mean(z*z,0)
    for iteration in range(3000):
        old=coef.copy()
        for j in range(len(coef)):
            res+=z[:,j,None]*coef[j]
            c=z[:,j]@res/len(z)
            coef[j]=np.sign(c)*np.maximum(abs(c)-penalty,0)/max(energy[j],1e-15)
            res-=z[:,j,None]*coef[j]
        if np.max(abs(coef-old))<tolerance:break
    else:raise ValueError('Lasso convergence failed')
    gradient=z.T@res/len(z)
    kkt=np.where(abs(coef)>1e-7,abs(gradient-penalty*np.sign(coef)),np.maximum(abs(gradient)-penalty,0)).max()
    if kkt>2e-6:raise ValueError('Lasso KKT check failed')
    return dict(coefficient=coef/xs[:,None],intercept=ym-xm@(coef/xs[:,None]),kkt=float(kkt),iterations=iteration+1)

def predict(fit,x):return x@fit['coefficient']+fit['intercept']

def train(x,y,penalties,gap):
    split=len(x)//2;lo=split-gap//2;hi=lo+gap
    if min(lo,len(x)-hi)<20:raise ValueError('Insufficient nested training history')
    candidates=[lasso(x[:lo],y[:lo],penalty) for penalty in penalties]
    losses=[float(np.mean((y[hi:]-predict(f,x[hi:]))**2)) for f in candidates]
    choice=int(np.argmin(losses));fit=lasso(x,y,penalties[choice])
    fit.update(penalty=float(penalties[choice]),losses=losses)
    return fit

def estimate(x,y,gap,penalties,alpha=.01,dense=False):
    n=len(x);mid=n//2;left=mid-gap//2;right=left+gap;spans=[(0,left),(right,n)];res=[];selection=[]
    for k,(e0,e1) in enumerate(spans):
        t0,t1=spans[1-k]
        if dense:
            design=np.column_stack((np.ones(t1-t0),x[t0:t1]));co=np.linalg.lstsq(design,y[t0:t1],rcond=None)[0]
            pred=np.column_stack((np.ones(e1-e0),x[e0:e1]))@co
        else:
            fit=train(x[t0:t1],y[t0:t1],penalties,min(gap,20));pred=predict(fit,x[e0:e1])
            selection.append(dict(penalty=fit['penalty'],kkt=fit['kkt'],nonzero=int(np.count_nonzero(fit['coefficient'])),training_rows=t1-t0,validation_losses=fit['losses']))
        res.append(y[e0:e1]-pred)
    joined=np.vstack(res);den=float(np.mean(joined[:,2]*joined[:,1]))
    if abs(den)<1e-8:return dict(status='unavailable_weak_iv',denominator=den)
    theta=float(np.mean(joined[:,2]*joined[:,0])/den);bw=max(1,int(len(joined)**.25));v=0.
    for block in res:
        score=block[:,2]*(block[:,0]-theta*block[:,1]);score-=score.mean()
        v+=score@score
        for lag in range(1,min(bw,len(score)-1)+1):v+=2*(1-lag/(bw+1))*(score[lag:]@score[:-lag])
    se=float(np.sqrt(v)/len(joined)/abs(den));z=norm.ppf(1-alpha/2)
    return dict(status='computed_conditional',estimate=theta,standard_error=se,interval=[theta-z*se,theta+z*se],denominator=den,selection=selection,bandwidth=bw,features=x.shape[1],scope='Training-only nested tuning; fixed-dimension geometric mixing with independent evaluation asymptotically; sparse growing dimension needs additional restricted eigenvalue/product rates. Weak IV unqualified.')
