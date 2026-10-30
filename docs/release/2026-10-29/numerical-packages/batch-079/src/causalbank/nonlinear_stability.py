"""Explicit broader stable-domain challenger for the audited nonlinear model."""
import numpy as np
from scipy.optimize import minimize
from .nonlinear_audited import engine,audit_start,BOUNDS


def fit_stable(main,audit,states,policy,*,nodes=61):
    main=np.asarray(main,float);audit=np.asarray(audit,float);states=np.asarray(states,float);policy=np.asarray(policy,float)
    if main.ndim!=3 or main.shape[2]!=3 or audit.shape[1:]!=main.shape[1:] or states.shape!=audit.shape[:2] or policy.shape!=(main.shape[1],):
        raise ValueError('aligned independent complete trajectories and frozen policy required')
    if min(len(main),len(audit))<3 or not all(np.all(np.isfinite(x)) for x in (main,audit,states,policy)) or not all(np.all(np.isin(x[:,:,1],[0,1])) for x in (main,audit)):
        raise ValueError('finite trajectories and binary actions required')
    e=engine(nodes,7.);bounds=list(BOUNDS);bounds[:2]=[(-.9,.9),(-.9,.9)];start=audit_start(audit,states)
    constraint={'type':'ineq','fun':lambda p:.95-abs(p[0])-abs(p[1]),
                'jac':lambda p:np.r_[-np.sign(p[:2]),np.zeros(13)]}
    def objective(p):
        value,gradient=e['objective'](p,main,audit,states)
        return float(value),np.asarray(gradient)
    fits=[]
    for initial in (start,np.r_[.15,-.1,.1,start[3:]]):
        fits.append(minimize(objective,initial,jac=True,method='SLSQP',bounds=bounds,constraints=constraint,
                             options={'ftol':1e-9,'maxiter':250}))
    best=min(fits,key=lambda f:f.fun);p=best.x
    boundary=bool(np.min(np.minimum(p-np.array(bounds)[:,0],np.array(bounds)[:,1]-p))<1e-5 or constraint['fun'](p)<1e-5)
    out=dict(status='computed' if best.success and not boundary else 'unqualified_fit',parameters=p,value=float(e['value'](p,policy)),
             boundary=boundary,starts=[dict(success=bool(f.success),objective=float(f.fun),message=str(f.message),score_norm=float(np.linalg.norm(f.jac))) for f in fits],
             local_mode_objective_spread=float(np.ptp([f.fun for f in fits])),policy=policy,
             inference={'method':'joint_audit_likelihood_stable_diamond','confidence_level':.95,
                        'sampling_unit':'independent complete trajectory, separately sampled main and labelled-audit populations',
                        'target':'frozen pilot policy value conditional on training',
                        'coverage_claim':'pointwise interior regular parametric asymptotic with both sample information rates',
                        'numerical_status':'two local constrained starts and inspected quadrature; no global optimum certificate',
                        'empirical_qualification':'research reference with explicit availability and calibration evidence'})
    if out['status']!='computed':return out
    h=np.asarray(e['hessian'](p,main,audit,states));eigen=np.linalg.eigvalsh(h)
    if eigen.min()<=1e-7:out['status']='unqualified_information';return out
    scores=np.asarray(e['scores'](p,main,audit,states));nm=len(main)
    centered=np.vstack([scores[:nm]-scores[:nm].mean(axis=0),scores[nm:]-scores[nm:].mean(axis=0)])
    inv=np.linalg.solve(h,np.eye(15));cov=inv@centered.T@centered@inv;gradient=np.asarray(e['value_gradient'](p,policy))
    se=float(np.sqrt(gradient@cov@gradient));ref=engine(81,9.)
    score_error=float(np.max(abs(np.asarray(ref['observed_gradient'](p,main))-np.asarray(e['observed_gradient'](p,main)))))
    llerror=float(np.sum(ref['observed'](p,main))-np.sum(e['observed'](p,main)))
    value_error=1000*(float(ref['value'](p,policy))-out['value'])
    out.update(standard_error=se,interval=[out['value']-1.96*se,out['value']+1.96*se],covariance=cov,
               refined_score_error=score_error,refined_loglik_error=llerror,refined_value_error_currency=value_error,
               information_condition=float(eigen.max()/eigen.min()))
    if score_error>1e-3 or abs(llerror)>1e-4 or abs(value_error)>.1:
        out['status']='unqualified_numerics';out['withheld_interval']=out.pop('interval')
    return out
