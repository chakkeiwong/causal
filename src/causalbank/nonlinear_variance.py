"""Audited nonlinear model with action-dependent transition innovation variance."""
from functools import lru_cache
import numpy as np
from scipy.optimize import minimize
from scipy.special import expit
import jax
import jax.numpy as jnp
from jax.scipy.special import ndtr
from .nonlinear_audited import _lognormal, EPSILON, BOUNDS as OLD_BOUNDS, TRUTH as OLD_TRUTH, audit_start as old_start

TRUTH=np.r_[OLD_TRUTH,np.log(.9)]
BOUNDS=list(OLD_BOUNDS)+[(-2.3,1.5)]
BOUNDS[:2]=[(-.9,.9),(-.9,.9)]


def validate(p):
    p=np.asarray(p,float)
    if p.shape!=(16,) or not np.all(np.isfinite(p)) or abs(p[0])+abs(p[1])>=1:
        raise ValueError('stable finite 16-parameter model required')
    return p


def simulate(p,n,h,rng,*,misspecification=False):
    p=validate(p);s=np.empty((n,h));data=np.empty((n,h,3));s[:,0]=p[13]+np.sqrt(np.exp(p[14]))*rng.normal(size=n)
    for t in range(h):
        x=s[:,t];o=x+np.sqrt(np.exp(p[4]))*rng.normal(size=n)
        prob=EPSILON+(1-2*EPSILON)*expit(p[5]+p[6]*x+p[7]*o);a=rng.binomial(1,prob,n)
        r=p[8]+p[9]*x+p[10]*a+p[11]*x*a+np.sqrt(np.exp(p[12]))*rng.normal(size=n);data[:,t]=np.column_stack([o,a,r])
        if t<h-1:
            q=np.exp(p[3])*(1-a)+np.exp(p[15])*a
            s[:,t+1]=p[0]*x+p[1]*np.tanh(x)+p[2]*a+np.sqrt(q)*rng.normal(size=n)
            if misspecification:s[:,t+1]+=.35*np.sin(2*x)
    return data,s


@lru_cache(maxsize=8)
def engine(nodes=61,limit=7.):
    grid=jnp.linspace(-limit,limit,nodes);w=jnp.ones(nodes)*(2*limit/(nodes-1));w=w.at[0].multiply(.5).at[-1].multiply(.5)
    def transition(p,a):
        mean=p[0]*grid+p[1]*jnp.tanh(grid)+p[2]*a;logq=p[3]*(1-a)+p[15]*a
        return jnp.exp(_lognormal(grid[None,:],mean[:,None],logq))*w[None,:]
    def observed(p,data):
        pred=jnp.broadcast_to(jnp.exp(_lognormal(grid,p[13],p[14]))*w,(len(data),nodes));ll=jnp.zeros(len(data));k0,k1=transition(p,0.),transition(p,1.)
        for t in range(data.shape[1]):
            o,a,r=[data[:,t,k,None] for k in range(3)];prob=EPSILON+(1-2*EPSILON)*jax.nn.sigmoid(p[5]+p[6]*grid+p[7]*o)
            emission=_lognormal(o,grid,p[4])+jnp.where(a==1,jnp.log(prob),jnp.log1p(-prob))+_lognormal(r,p[8]+p[9]*grid+p[10]*a+p[11]*grid*a,p[12])
            shift=jnp.max(emission,axis=1,keepdims=True);weight=pred*jnp.exp(emission-shift);mass=jnp.sum(weight,axis=1,keepdims=True)
            ll+=jnp.log(mass[:,0])+shift[:,0];post=weight/mass;pred=(post@k0)*(1-a)+(post@k1)*a
        return ll
    def labelled(p,data,s):
        o,a,r=data[:,:,0],data[:,:,1],data[:,:,2];prob=EPSILON+(1-2*EPSILON)*jax.nn.sigmoid(p[5]+p[6]*s+p[7]*o)
        ll=_lognormal(s[:,0],p[13],p[14])+jnp.sum(_lognormal(o,s,p[4])+jnp.where(a==1,jnp.log(prob),jnp.log1p(-prob))+_lognormal(r,p[8]+p[9]*s+p[10]*a+p[11]*s*a,p[12]),axis=1)
        means=p[0]*s[:,:-1]+p[1]*jnp.tanh(s[:,:-1])+p[2]*a[:,:-1];logq=p[3]*(1-a[:,:-1])+p[15]*a[:,:-1]
        return ll+jnp.sum(_lognormal(s[:,1:],means,logq),axis=1)
    def contributions(p,main,audit,s):return jnp.concatenate([observed(p,main),labelled(p,audit,s)])
    def objective(p,main,audit,s):return -jnp.sum(contributions(p,main,audit,s))
    def value(p,thresholds):
        mass=jnp.exp(_lognormal(grid,p[13],p[14]))*w;total=0.;k0,k1=transition(p,0.),transition(p,1.)
        for t in range(len(thresholds)):
            prob=ndtr((grid-thresholds[t])*jnp.exp(-p[4]/2));reward=p[8]+p[9]*grid+(p[10]+p[11]*grid)*prob
            total+=.97**t*jnp.sum(mass*reward);mass=(mass*(1-prob))@k0+(mass*prob)@k1
        return total
    return dict(observed=jax.jit(observed),labelled=jax.jit(labelled),objective=jax.jit(jax.value_and_grad(objective)),
                hessian=jax.jit(jax.hessian(objective)),scores=jax.jit(jax.jacrev(contributions,argnums=0)),
                value=jax.jit(value),value_gradient=jax.jit(jax.grad(value)),observed_gradient=jax.jit(jax.grad(lambda p,d:jnp.sum(observed(p,d)))))


def audit_start(data,s):
    p=np.r_[old_start(data,s),0.];a=data[:,:-1,1];res=s[:,1:]-p[0]*s[:,:-1]-p[1]*np.tanh(s[:,:-1])-p[2]*a
    if min(np.sum(a==0),np.sum(a==1))<10:raise ValueError('both audited transition action groups require at least ten transitions')
    p[3]=np.log(np.mean(res[a==0]**2));p[15]=np.log(np.mean(res[a==1]**2))
    if abs(p[0])+abs(p[1])>.9:p[:2]*=.9/(abs(p[0])+abs(p[1]))
    return np.clip(p,np.array(BOUNDS)[:,0]+1e-5,np.array(BOUNDS)[:,1]-1e-5)


def fit(main,audit,states,policy,*,nodes=61,limit=7.,refined_nodes=101,refined_limit=10.,tolerances=(1e-4,1e-3,.1)):
    main=np.asarray(main,float);audit=np.asarray(audit,float);states=np.asarray(states,float);policy=np.asarray(policy,float)
    if main.ndim!=3 or main.shape[2]!=3 or audit.ndim!=3 or audit.shape[1:]!=main.shape[1:] or states.shape!=audit.shape[:2] or policy.shape!=(main.shape[1],) or min(len(main),len(audit))<3:
        raise ValueError('aligned independent main and representative labelled trajectories; frozen observable policy required')
    if not all(np.all(np.isfinite(x)) for x in (main,audit,states,policy)) or not all(np.all(np.isin(x[:,:,1],[0,1])) for x in (main,audit)):
        raise ValueError('finite trajectories and binary actions required')
    e=engine(nodes,limit);start=audit_start(audit,states);constraint=dict(type='ineq',fun=lambda p:.95-abs(p[0])-abs(p[1]),jac=lambda p:np.r_[-np.sign(p[:2]),np.zeros(14)])
    def objective(p):
        loss,gradient=e['objective'](p,main,audit,states);return float(loss),np.asarray(gradient)
    fits=[minimize(objective,initial,jac=True,method='SLSQP',bounds=BOUNDS,constraints=constraint,options={'ftol':1e-9,'maxiter':300}) for initial in (start,np.r_[.15,-.1,.1,start[3:]])]
    best=min(fits,key=lambda f:f.fun);p=best.x;boundary=bool(np.min(np.minimum(p-np.array(BOUNDS)[:,0],np.array(BOUNDS)[:,1]-p))<1e-5 or constraint['fun'](p)<1e-5)
    value=float(e['value'](p,policy));out=dict(status='computed' if best.success and not boundary else 'unqualified_fit',parameters=p,value=value,estimate=1000*value,boundary=boundary,
        starts=[dict(success=bool(f.success),message=str(f.message),objective=float(f.fun),score_norm=float(np.linalg.norm(f.jac))) for f in fits],policy=policy,
        inference=dict(method='audited_action_variance_likelihood_delta',confidence_level=.95,sampling_unit='independent full trajectory separately sampled in main and labelled audit groups',
                       coverage_claim='pointwise interior parametric asymptotic with both sample rates; accurate representative state audits and correct model',
                       numerical_status='two local starts, finite-domain quadrature and per-fit refinement; no global numerical certificate',empirical_qualification='selected 16-parameter model and fixed signal-threshold policy only'))
    if out['status']!='computed':return out
    h=np.asarray(e['hessian'](p,main,audit,states));eig=np.linalg.eigvalsh(h)
    if eig.min()<=1e-7:out['status']='unqualified_information';return out
    scores=np.asarray(e['scores'](p,main,audit,states));nm=len(main);centered=np.vstack([scores[:nm]-scores[:nm].mean(axis=0),scores[nm:]-scores[nm:].mean(axis=0)])
    inv=np.linalg.solve(h,np.eye(16));cov=inv@centered.T@centered@inv;g=np.asarray(e['value_gradient'](p,policy));se=float(np.sqrt(g@cov@g))*1000
    ref=engine(refined_nodes,refined_limit);llerror=float(np.sum(ref['observed'](p,main))-np.sum(e['observed'](p,main)));scoreerror=float(np.max(abs(np.asarray(ref['observed_gradient'](p,main))-np.asarray(e['observed_gradient'](p,main)))))
    valueerror=1000*(float(ref['value'](p,policy))-value)
    out.update(standard_error=se,interval=[1000*value-1.96*se,1000*value+1.96*se],covariance=cov,refined_loglik_error=llerror,refined_score_error=scoreerror,refined_value_error_currency=valueerror,information_condition=float(eig.max()/eig.min()))
    if abs(llerror)>tolerances[0] or scoreerror>tolerances[1] or abs(valueerror)>tolerances[2]:out['status']='unqualified_numerics';out['withheld_interval']=out.pop('interval')
    return out


def policy_simulation(p,policy,n,seed,*,misspecification=False):
    p=validate(p);rng=np.random.default_rng(seed);s=p[13]+np.sqrt(np.exp(p[14]))*rng.normal(size=n);total=np.zeros(n)
    for t,threshold in enumerate(policy):
        o=s+np.sqrt(np.exp(p[4]))*rng.normal(size=n);a=(o>threshold).astype(int);total+=.97**t*(p[8]+p[9]*s+p[10]*a+p[11]*s*a)
        updated=p[0]*s+p[1]*np.tanh(s)+p[2]*a+np.sqrt(np.exp(p[3])*(1-a)+np.exp(p[15])*a)*rng.normal(size=n)
        if misspecification:updated+=.35*np.sin(2*s)
        s=updated
    return float(total.mean()),float(total.std(ddof=1)/np.sqrt(n))
