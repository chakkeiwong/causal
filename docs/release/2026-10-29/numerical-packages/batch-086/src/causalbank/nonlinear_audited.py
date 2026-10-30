"""A scalar nonlinear private-logger likelihood with independent labelled audits.

The fixed model and accurate representative audits supply identification.
Quadrature, local optimization and a conditional-policy delta method supply
numerical/statistical approximations, not general POMDP qualification.
"""
import os
os.environ.setdefault('JAX_PLATFORMS','cpu')
import itertools
from functools import lru_cache
import numpy as np
from scipy.optimize import minimize
from scipy.special import expit, logsumexp, ndtr
from scipy.stats import norm
import jax
jax.config.update('jax_enable_x64',True)
import jax.numpy as jnp
from jax.scipy.special import ndtr as jndtr

NAMES=('rho','gamma','beta','log_q','log_o','lambda0','lambda_s','lambda_o',
       'eta0','eta_s','eta_a','eta_sa','log_r','mu0','log_v0')
BOUNDS=((-0.55,.55),(-.4,.4),(-1.5,1.5),(-2.3,1.5),(-2.3,2.3),
        (-4.,4.),(-3.,3.),(-3.,3.),(-2.,2.),(-2.,2.),(-2.,2.),(-1.5,1.5),
        (-2.3,1.5),(-1.,1.),(-2.,1.5))
TRUTH=np.array([.35,.3,.4,np.log(.35),np.log(.5),-.2,1.1,.25,
                .1,.8,-.2,.35,np.log(.4),.1,np.log(.8)])
EPSILON=.05


def validate(theta):
    p=np.asarray(theta,float)
    if p.shape!=(15,) or not np.all(np.isfinite(p)) or abs(p[0])+abs(p[1])>=1:
        raise ValueError('finite stable 15-parameter model required')
    return p


def simulate(theta,n,h,rng,*,misspecification=False):
    p=validate(theta);s=np.empty((n,h));data=np.empty((n,h,3))
    s[:,0]=p[13]+np.sqrt(np.exp(p[14]))*rng.normal(size=n)
    for t in range(h):
        x=s[:,t];o=x+np.sqrt(np.exp(p[4]))*rng.normal(size=n)
        prob=EPSILON+(1-2*EPSILON)*expit(p[5]+p[6]*x+p[7]*o)
        a=rng.binomial(1,prob)
        r=p[8]+p[9]*x+p[10]*a+p[11]*x*a+np.sqrt(np.exp(p[12]))*rng.normal(size=n)
        data[:,t]=np.column_stack([o,a,r])
        if t<h-1:
            s[:,t+1]=p[0]*x+p[1]*np.tanh(x)+p[2]*a+np.sqrt(np.exp(p[3]))*rng.normal(size=n)
            if misspecification:s[:,t+1]+=.35*np.sin(2*x)
    return data,s


def _lognormal(x,mean,logvar):
    return -.5*(jnp.log(2*jnp.pi)+logvar+(x-mean)**2*jnp.exp(-logvar))


@lru_cache(maxsize=12)
def engine(nodes=61,limit=7.):
    # Composite trapezoid over an explicitly inspected finite domain.
    grid=jnp.linspace(-limit,limit,nodes);w=jnp.ones(nodes)*(2*limit/(nodes-1))
    w=w.at[0].multiply(.5).at[-1].multiply(.5)

    def transition(p,a):
        mean=p[0]*grid+p[1]*jnp.tanh(grid)+p[2]*a
        return jnp.exp(_lognormal(grid[None,:],mean[:,None],p[3]))*w[None,:]

    def observed(p,data):
        pred=jnp.broadcast_to(jnp.exp(_lognormal(grid,p[13],p[14]))*w,(data.shape[0],nodes))
        ll=jnp.zeros(data.shape[0]);k0,k1=transition(p,0.),transition(p,1.)
        for t in range(data.shape[1]):
            o,a,r=[data[:,t,k,None] for k in range(3)]
            prob=EPSILON+(1-2*EPSILON)*jax.nn.sigmoid(p[5]+p[6]*grid+p[7]*o)
            emission=_lognormal(o,grid,p[4])+jnp.where(a==1,jnp.log(prob),jnp.log1p(-prob))
            emission+=_lognormal(r,p[8]+p[9]*grid+p[10]*a+p[11]*grid*a,p[12])
            shift=jnp.max(emission,axis=1,keepdims=True)
            weight=pred*jnp.exp(emission-shift);mass=jnp.sum(weight,axis=1,keepdims=True)
            ll+=jnp.log(mass[:,0])+shift[:,0];post=weight/mass
            pred=(post@k0)*(1-a)+(post@k1)*a
        return ll

    def labelled(p,data,states):
        o,a,r=data[:,:,0],data[:,:,1],data[:,:,2];s=states
        prob=EPSILON+(1-2*EPSILON)*jax.nn.sigmoid(p[5]+p[6]*s+p[7]*o)
        ll=_lognormal(s[:,0],p[13],p[14])
        ll+=jnp.sum(_lognormal(o,s,p[4])+jnp.where(a==1,jnp.log(prob),jnp.log1p(-prob))+
                    _lognormal(r,p[8]+p[9]*s+p[10]*a+p[11]*s*a,p[12]),axis=1)
        means=p[0]*s[:,:-1]+p[1]*jnp.tanh(s[:,:-1])+p[2]*a[:,:-1]
        return ll+jnp.sum(_lognormal(s[:,1:],means,p[3]),axis=1)

    def contributions(p,main,audit,states):
        return jnp.concatenate([observed(p,main),labelled(p,audit,states)])

    def objective(p,main,audit,states):
        return -jnp.sum(contributions(p,main,audit,states))

    def value(p,thresholds):
        mass=jnp.exp(_lognormal(grid,p[13],p[14]))*w
        total=0.;k0,k1=transition(p,0.),transition(p,1.)
        for t in range(thresholds.shape[0]):
            prob=jndtr((grid-thresholds[t])*jnp.exp(-p[4]/2))
            reward=p[8]+p[9]*grid+(p[10]+p[11]*grid)*prob
            total+=.97**t*jnp.sum(mass*reward)
            mass=(mass*(1-prob))@k0+(mass*prob)@k1
        return total

    return {'observed':jax.jit(observed),'labelled':jax.jit(labelled),
            'objective':jax.jit(jax.value_and_grad(objective)),
            'hessian':jax.jit(jax.hessian(objective)),
            'scores':jax.jit(jax.jacrev(contributions,argnums=0)),
            'value':jax.jit(value),'value_gradient':jax.jit(jax.grad(value)),
            'observed_gradient':jax.jit(jax.grad(lambda p,data:jnp.sum(observed(p,data))))}


def audit_start(data,states):
    s=states;o,a,r=[data[:,:,k] for k in range(3)];p=np.zeros(15)
    x=np.column_stack([s[:,:-1].ravel(),np.tanh(s[:,:-1]).ravel(),a[:,:-1].ravel()])
    p[:3]=np.linalg.lstsq(x,s[:,1:].ravel(),rcond=None)[0]
    p[3]=np.log(np.mean((s[:,1:].ravel()-x@p[:3])**2));p[4]=np.log(np.mean((o-s)**2))
    design=np.column_stack([np.ones(s.size),s.ravel(),a.ravel(),(s*a).ravel()])
    p[8:12]=np.linalg.lstsq(design,r.ravel(),rcond=None)[0]
    p[12]=np.log(np.mean((r.ravel()-design@p[8:12])**2))
    logger=np.column_stack([np.ones(s.size),s.ravel(),o.ravel()]);actions=a.ravel()
    def loss(lam):
        eta=expit(logger@lam);prob=EPSILON+(1-2*EPSILON)*eta
        value=-np.sum(actions*np.log(prob)+(1-actions)*np.log1p(-prob))
        gradient=logger.T@((prob-actions)/(prob*(1-prob))*(1-2*EPSILON)*eta*(1-eta))
        return value,gradient
    p[5:8]=minimize(loss,np.zeros(3),jac=True,method='L-BFGS-B',bounds=BOUNDS[5:8]).x
    p[13]=s[:,0].mean();p[14]=np.log(s[:,0].var())
    return np.clip(p,np.array(BOUNDS)[:,0]+1e-5,np.array(BOUNDS)[:,1]-1e-5)


def fit(main,audit,states,thresholds,*,nodes=61,limit=7.,starts=2,initial=None,uncertainty=True):
    main=np.asarray(main,float);audit=np.asarray(audit,float);states=np.asarray(states,float)
    if main.ndim!=3 or main.shape[2]!=3 or audit.ndim!=3 or audit.shape[1:]!=main.shape[1:] or states.shape!=audit.shape[:2] or min(len(main),len(audit))<3:
        raise ValueError('independent complete main/audited trajectories on the same clock required')
    if not all(np.all(np.isfinite(x)) for x in (main,audit,states)) or not all(np.all(np.isin(x[:,:,1],[0,1])) for x in (main,audit)):
        raise ValueError('finite trajectories and binary actions required')
    thresholds=np.asarray(thresholds,float)
    if thresholds.shape!=(main.shape[1],) or not np.all(np.isfinite(thresholds)):
        raise ValueError('one fixed observable-signal policy threshold per date required')
    e=engine(nodes,limit);p=audit_start(audit,states) if initial is None else validate(initial)
    records=[];fits=[]
    for i in range(starts):
        start=p.copy()
        if i:start[:3]=[.15,-.1,.1]
        def objective(theta):
            loss,grad=e['objective'](theta,main,audit,states)
            return float(loss),np.asarray(grad)
        result=minimize(objective,start,jac=True,method='L-BFGS-B',bounds=BOUNDS,
                        options={'ftol':1e-12,'gtol':2e-6,'maxiter':350,'maxls':30})
        records.append(dict(success=bool(result.success),message=str(result.message),objective=float(result.fun),iterations=int(result.nit),score_norm=float(np.linalg.norm(result.jac))))
        fits.append(result)
    best=min(fits,key=lambda f:f.fun);p=best.x;value=float(e['value'](p,thresholds))
    boundary=bool(np.min(np.minimum(p-np.array(BOUNDS)[:,0],np.array(BOUNDS)[:,1]-p))<1e-5)
    out=dict(status='computed' if best.success and not boundary else 'unqualified_fit',parameters=p,value=value,
             starts=records,boundary=boundary,local_mode_objective_spread=float(np.ptp([f.fun for f in fits])),
             policy=thresholds,nodes=nodes,domain_limit=limit,
             inference={'method':'joint_audit_observed_likelihood_delta','sampling_unit':'independent whole customer trajectory in each of two independent samples',
                        'target':'value of fixed independent-pilot observable policy, conditional on training',
                        'coverage_claim':'pointwise regular parametric asymptotic; audit sample information included',
                        'numerical_status':'local optimum and finite-domain quadrature, not a global or certified bound',
                        'empirical_qualification':'research reference; inspect numerical and repeated-sample checks',
                        'confidence_level':.95})
    if uncertainty and out['status']=='computed':
        h=np.asarray(e['hessian'](p,main,audit,states));scores=np.asarray(e['scores'](p,main,audit,states))
        eig=np.linalg.eigvalsh(h);out['information_condition']=float(eig.max()/max(eig.min(),1e-20))
        if eig.min()<=1e-7:
            out['status']='unqualified_information';return out
        # The independent sample sizes enter through sums, not a presumed
        # production-sample rate for audit-identified directions.
        centered=np.vstack([scores[:len(main)]-scores[:len(main)].mean(axis=0),scores[len(main):]-scores[len(main):].mean(axis=0)])
        inv=np.linalg.solve(h,np.eye(15));cov=inv@(centered.T@centered)@inv
        g=np.asarray(e['value_gradient'](p,thresholds));se=float(np.sqrt(max(0,g@cov@g)))
        out.update(standard_error=se,interval=[value-1.95996398454*se,value+1.95996398454*se],covariance=cov,
                   inverse_information_se=float(np.sqrt(max(0,g@inv@g))),
                   audit_score_fraction=float(np.trace(scores[len(main):].T@scores[len(main):])/np.trace(scores.T@scores)))
    return out


def choose_policy(theta,horizon,nodes=81):
    e=engine(nodes);policies=list(itertools.product([-1.,0.,1.,8.],repeat=horizon))
    values=np.array([float(e['value'](theta,np.array(p))) for p in policies]);i=int(values.argmax())
    return np.array(policies[i]),dict(library_size=len(policies),selected_value=float(values[i]),
                                    scope='exact enumeration of a finite time/signal threshold library; not full belief-policy optimality')


def gaussian_loglik(theta,data):
    """Assumed-density challenger; exact when gamma=lambda_s=0.

    State-dependent action is integrated by Gaussian-Hermite nodes, followed
    by Gaussian moment matching. Its distributional approximation is explicit.
    """
    p=validate(theta);points,weights=np.polynomial.hermite.hermgauss(31);weights/=np.sqrt(np.pi)
    m=np.full(len(data),p[13]);v=np.full(len(data),np.exp(p[14]));ll=np.zeros(len(data))
    for t in range(data.shape[1]):
        o,a,r=data[:,t].T;svar=v+np.exp(p[4]);ll+=norm.logpdf(o,m,np.sqrt(svar))
        k=v/svar;m=m+k*(o-m);v=v*(1-k)
        if p[6]==0:
            prob=EPSILON+(1-2*EPSILON)*expit(p[5]+p[7]*o)
            ll+=np.where(a==1,np.log(prob),np.log1p(-prob))
        else:
            x=m[:,None]+np.sqrt(2*v[:,None])*points;prob=EPSILON+(1-2*EPSILON)*expit(p[5]+p[6]*x+p[7]*o[:,None])
            w=weights*np.where(a[:,None]==1,prob,1-prob);z=w.sum(axis=1);ll+=np.log(z);w/=z[:,None]
            m=(w*x).sum(axis=1);v=(w*(x-m[:,None])**2).sum(axis=1)
        loading=p[9]+p[11]*a;mean=p[8]+p[10]*a+loading*m;svar=loading**2*v+np.exp(p[12])
        ll+=norm.logpdf(r,mean,np.sqrt(svar));k=v*loading/svar;m=m+k*(r-mean);v=v-k*loading*v
        x=m[:,None]+np.sqrt(2*v[:,None])*points;f=p[0]*x+p[1]*np.tanh(x)+p[2]*a[:,None]
        m=(weights*f).sum(axis=1);v=(weights*(f-m[:,None])**2).sum(axis=1)+np.exp(p[3])
    return ll


def particle_loglik(theta,data,particles,seed):
    p=validate(theta);rng=np.random.default_rng(seed);n,h,_=data.shape
    x=p[13]+np.sqrt(np.exp(p[14]))*rng.normal(size=(n,particles));ll=np.zeros(n)
    for t in range(h):
        o,a,r=[data[:,t,k,None] for k in range(3)];prob=EPSILON+(1-2*EPSILON)*expit(p[5]+p[6]*x+p[7]*o)
        logw=norm.logpdf(o,x,np.sqrt(np.exp(p[4])))+np.where(a==1,np.log(prob),np.log1p(-prob))
        logw+=norm.logpdf(r,p[8]+p[9]*x+p[10]*a+p[11]*x*a,np.sqrt(np.exp(p[12])))
        logz=logsumexp(logw,axis=1);ll+=logz-np.log(particles)
        cdf=np.cumsum(np.exp(logw-logz[:,None]),axis=1);cdf[:,-1]=1.
        u=(rng.random((n,1))+np.arange(particles))/particles
        x=np.array([x[i,np.searchsorted(cdf[i],u[i])] for i in range(n)])
        x=p[0]*x+p[1]*np.tanh(x)+p[2]*a+np.sqrt(np.exp(p[3]))*rng.normal(size=x.shape)
    return ll


def simulate_policy_value(theta,policy,n,seed,*,misspecification=False):
    p=validate(theta);rng=np.random.default_rng(seed);s=p[13]+np.sqrt(np.exp(p[14]))*rng.normal(size=n);total=np.zeros(n)
    for t,threshold in enumerate(policy):
        o=s+np.sqrt(np.exp(p[4]))*rng.normal(size=n);a=(o>threshold).astype(float)
        total+=.97**t*(p[8]+p[9]*s+p[10]*a+p[11]*s*a)
        updated=p[0]*s+p[1]*np.tanh(s)+p[2]*a+np.sqrt(np.exp(p[3]))*rng.normal(size=n)
        if misspecification:updated+=.35*np.sin(2*s)
        s=updated
    return float(total.mean()),float(total.std(ddof=1)/np.sqrt(n))


def gaussian_policy_value(theta,policy):
    """Moment-matched Gaussian challenger for the same observable policy."""
    p=validate(theta);points,w=np.polynomial.hermite.hermgauss(31);w/=np.sqrt(np.pi)
    m=p[13];v=np.exp(p[14]);total=0.
    for t,threshold in enumerate(policy):
        s=m+np.sqrt(2*v)*points;prob=ndtr((s-threshold)/np.sqrt(np.exp(p[4])))
        total+=.97**t*np.sum(w*(p[8]+p[9]*s+(p[10]+p[11]*s)*prob))
        f=p[0]*s+p[1]*np.tanh(s);nextmean=np.sum(w*(f+p[2]*prob))
        nextsecond=np.sum(w*(f*f+(2*f*p[2]+p[2]**2)*prob))+np.exp(p[3])
        m=nextmean;v=nextsecond-m*m
    return float(total)
