"""Exactly Gaussian privately logged scalar state model with analytic score.

Known measurement scale/noise and process noise identify the reference's
scientific scale. This is not an unknown-sensor or nonlinear POMDP solver.
"""
import numpy as np
from scipy.optimize import minimize


def likelihood_score(theta,data,noises,include_logger=True):
    f,b,k,c,d=np.asarray(theta);o,a,r=data;n,h=o.shape
    process,signal,action,reward=noises
    channels=[0,1,2] if include_logger else [0,2]
    C=np.array([1.,k,c])[channels];vnoise=np.diag(np.array([signal,action,reward])[channels])
    dC=np.zeros((5,len(channels)))
    if include_logger:dC[2,1]=1
    dC[3,-1]=1
    m=np.zeros(n);dm=np.zeros((n,5));P=1.;dP=np.zeros(5);ll=0.;score=np.zeros(5)
    for t in range(h):
        z=np.column_stack((o[:,t],a[:,t],r[:,t]-d*a[:,t]))[:,channels]
        innovation=z-m[:,None]*C
        covariance=P*np.outer(C,C)+vnoise;inverse=np.linalg.solve(covariance,np.eye(len(C)))
        sign,logdet=np.linalg.slogdet(covariance)
        if sign!=1:raise ValueError('nonpositive innovation covariance')
        solved=innovation@inverse
        ll+=-.5*(n*(len(C)*np.log(2*np.pi)+logdet)+np.sum(solved*innovation))
        gain=P*C@inverse
        dcov=np.array([dP[j]*np.outer(C,C)+P*(np.outer(dC[j],C)+np.outer(C,dC[j])) for j in range(5)])
        dinnovation=-dm[:,:,None]*C-m[:,None,None]*dC
        dinnovation[:,4,-1]-=a[:,t]
        score+=-.5*n*np.einsum('ab,jba->j',inverse,dcov)+.5*np.einsum('na,jab,nb->j',solved,dcov,solved)-np.einsum('nja,na->j',dinnovation,solved)
        dgain=np.array([(dP[j]*C+P*dC[j]-gain@dcov[j])@inverse for j in range(5)])
        filtered=m+innovation@gain
        dfiltered=dm+innovation@dgain.T+np.einsum('nja,a->nj',dinnovation,gain)
        filteredP=P-gain@C*P
        dfilteredP=dP-(dgain@C+ dC@gain)*P-(gain@C)*dP
        m=f*filtered+b*a[:,t]
        dm=f*dfiltered;dm[:,0]+=filtered;dm[:,1]+=a[:,t]
        P=f*f*filteredP+process
        dP=f*f*dfilteredP;dP[0]+=2*f*filteredP
    return float(ll),score


def fit(data,noises,include_logger=True):
    n=len(data[0])
    def objective(theta):
        ll,s=likelihood_score(theta,data,noises,include_logger)
        return -ll/n,-s/n
    opt=minimize(objective,[.3,.2,.2,.7,.1],jac=True,method='BFGS',options={'gtol':1e-6,'maxiter':300})
    # The omitted logger leaves k unused; it is a diagnostic fit with singular
    # full information, so only its point estimate is used.
    return opt.x,{'success':bool(opt.success),'message':str(opt.message),'iterations':int(opt.nit),'average_score':float(abs(opt.jac).max())}


def value(theta,horizon=12,discount=.97,intercept=.4,slope=-.2):
    f,b,k,c,d=theta;m=0.;total=0.
    for t in range(horizon):
        action=intercept+slope*m
        total+=discount**t*(c*m+d*action)
        m=f*m+b*action
    return float(total)


def information(theta,data,noises,horizon=12,step=1e-5):
    p=len(theta);I=np.empty((p,p));gradient=np.empty(p)
    for j in range(p):
        delta=np.zeros(p);delta[j]=step
        I[:,j]=-(likelihood_score(theta+delta,data,noises)[1]-likelihood_score(theta-delta,data,noises)[1])/(2*step)
        gradient[j]=(value(theta+delta,horizon)-value(theta-delta,horizon))/(2*step)
    asym=float(abs(I-I.T).max());I=(I+I.T)/2
    eig=np.linalg.eigvalsh(I)
    if eig[0]<=0:return {'available':False,'minimum_eigenvalue':float(eig[0])}
    return {'available':True,'se':float(np.sqrt(gradient@np.linalg.solve(I,gradient))),'condition':float(eig[-1]/eig[0]),'asymmetry':asym}
