"""Representative audited trajectories and a fixed observable belief policy.

State sufficiency, accurate audit labels and invariance remain assumptions.
The policy tree never consumes evaluation state labels or settled rewards.
"""
import numpy as np
from .validated_latent import pack, unpack, contrast


def categorical(prob,rng):
    return (rng.random(len(prob))[:,None]>np.cumsum(prob,axis=1)).sum(axis=1)


def generate_audit(spec,n,rng):
    mu,e,q,t,r=[np.asarray(spec[k]) for k in ('mu','emission','logger','transition','reward')]
    h=spec['horizon']; s=np.empty((n,h),int); o=np.empty_like(s); a=np.empty_like(s); reward=np.empty((n,h))
    s[:,0]=rng.choice(len(mu),n,p=mu)
    for j in range(h):
        o[:,j]=categorical(e[s[:,j]],rng); a[:,j]=categorical(q[s[:,j]],rng)
        reward[:,j]=r[a[:,j],s[:,j]]+spec['reward_sd']*rng.normal(size=n)
        if j<h-1: s[:,j+1]=categorical(t[a[:,j],s[:,j]],rng)
    return {'states':s,'signals':o,'actions':a,'rewards':reward}


def trajectory_contributions(data,shape):
    s,o,a,r=[data[k] for k in ('states','signals','actions','rewards')]
    n,h=s.shape; k,m,b=shape.states,shape.signals,shape.actions
    initial=np.eye(k)[s[:,0]]
    emission=np.einsum('nhk,nhm->nkm',np.eye(k)[s],np.eye(m)[o])
    logger=np.einsum('nhk,nha->nka',np.eye(k)[s],np.eye(b)[a])
    transition=np.einsum('nha,nhi,nhj->naij',np.eye(b)[a[:,:-1]],np.eye(k)[s[:,:-1]],np.eye(k)[s[:,1:]])
    exposures=logger.transpose(0,2,1)
    reward_sum=np.einsum('nha,nhk,nh->nak',np.eye(b)[a],np.eye(k)[s],r)
    return initial,emission,logger,transition,exposures,reward_sum


def fit_audit(data,shape):
    parts=trajectory_contributions(data,shape); n=len(data['states']); parameters=[]; influences=[]
    for count in parts[:4]:
        total=count.sum(axis=0)
        if np.any(total<=0): raise ValueError('empty audited category: interior row-frequency inference unavailable')
        parameters.append(total/total.sum(axis=-1,keepdims=True))
        logit_if=n*(count[...,:-1]/total[...,:-1]-count[...,-1:]/total[...,-1:])
        influences.append(logit_if.reshape(n,-1))
    total=parts[4].sum(axis=0); reward=parts[5].sum(axis=0)/total
    influences.append((n*(parts[5]-parts[4]*reward)/total/shape.reward_sd).reshape(n,-1))
    theta=pack(*parameters,reward,shape)
    influence=np.column_stack(influences)
    return {'theta':theta,'influence':influence,'covariance':influence.T@influence/n**2,
            'minimum_transition_count':int(parts[3].sum(axis=0).min()),'trajectories':n}


def optimal_signal_tree(theta,shape,horizon,discount=.99):
    mu,e,_,transition,reward=unpack(theta,shape)
    def solve(prior,left):
        if left==0: return 0.,None
        value=0.; choices=[]
        for o in range(shape.signals):
            mass=prior*e[:,o]; prob=mass.sum(); posterior=mass/prob
            candidates=[]
            for a in range(shape.actions):
                continuation,child=solve(posterior@transition[a],left-1)
                candidates.append((float(posterior@reward[a]+discount*continuation),child))
            chosen=int(np.argmax([c[0] for c in candidates]))
            value+=prob*candidates[chosen][0]
            choices.append({'action':chosen,'next':candidates[chosen][1]})
        return value,choices
    value,tree=solve(mu,horizon)
    return {'tree':tree,'pilot_value':value,'horizon':horizon,'discount':discount,
            'information':'signal and own-action history; no audited state or within-horizon reward'}


def tree_value(theta,shape,policy):
    mu,e,_,transition,reward=unpack(theta,shape); discount=policy['discount']
    def evaluate(mass,tree):
        if tree is None:return 0.
        value=0.
        for o,node in enumerate(tree):
            observed=mass*e[:,o]; a=node['action']
            value+=observed@reward[a]+discount*evaluate(observed@transition[a],node['next'])
        return float(value)
    return evaluate(mu,policy['tree'])


def never_value(theta,shape,horizon,discount=.99):
    mu,_,_,t,r=unpack(theta,shape); value=np.zeros(shape.states)
    for _ in range(horizon):value=r[0]+discount*t[0]@value
    return float(mu@value)


def value_inference(fit,shape,policy=None,horizon=8,step=1e-5):
    theta=fit['theta']
    def functional(p):
        if policy is None:return contrast(p,shape,horizon)
        return tree_value(p,shape,policy)-never_value(p,shape,policy['horizon'],policy['discount'])
    value=functional(theta); gradient=np.empty(len(theta))
    for j in range(len(theta)):
        shift=np.zeros(len(theta));shift[j]=step
        gradient[j]=(functional(theta+shift)-functional(theta-shift))/(2*step)
    influence=fit['influence']@gradient
    variance=float(gradient@fit['covariance']@gradient)
    return {'estimate':value,'se':float(np.sqrt(max(variance,0))),
            'interval':[value-1.95996398454*np.sqrt(variance),value+1.95996398454*np.sqrt(variance)],
            'gradient':gradient,'influence':influence,'scope':'fixed policy conditional on independent pilot; iid audited trajectories'}
