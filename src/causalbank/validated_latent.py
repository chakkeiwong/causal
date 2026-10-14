"""Controlled finite-state likelihood with private logging and validation data.

The validation sample supplies labelled emission observations under a declared
invariant measurement model. Its likelihood is fitted jointly. This is a
specific sufficient identification route, not latent ignorability by default.
"""
from dataclasses import dataclass
import numpy as np
from scipy.optimize import minimize
from scipy.special import softmax, expit, logit


@dataclass
class ModelShape:
    states: int = 3
    signals: int = 4
    actions: int = 2
    reward_sd: float = 12.
    include_logger: bool = True


def unpack(theta, shape):
    k,m,a=shape.states,shape.signals,shape.actions
    pos=0
    def probability(rows, columns):
        nonlocal pos
        n=rows*(columns-1)
        raw=np.asarray(theta[pos:pos+n]).reshape(rows,columns-1); pos+=n
        return softmax(np.column_stack((raw,np.zeros(rows))),axis=1)
    mu=probability(1,k)[0]; emission=probability(k,m)
    logger=probability(k,a) if shape.include_logger else np.full((k,a),1/a)
    transition=probability(a*k,k).reshape(a,k,k)
    reward=shape.reward_sd*np.asarray(theta[pos:]).reshape(a,k)
    return mu,emission,logger,transition,reward


def pack(mu,emission,logger,transition,reward,shape):
    def logits(p):
        p=np.clip(np.asarray(p),1e-6,1); return np.log(p[...,:-1]/p[...,-1:]).ravel()
    pieces=[logits(mu),logits(emission)]
    if shape.include_logger: pieces.append(logits(logger))
    return np.concatenate(pieces+[logits(transition),np.asarray(reward).ravel()/shape.reward_sd])


def likelihood_score(theta, observed, calibration, shape, individual=False):
    """Scaled forward/backward likelihood and Fisher-identity analytic score."""
    o,a,r=observed; labels,cal_o=calibration
    n,h=o.shape; k=shape.states
    mu,e,q,t,means=unpack(theta,shape)
    log_reward=-.5*((r[:,:,None]-means[a])/shape.reward_sd)**2-np.log(shape.reward_sd*np.sqrt(2*np.pi))
    # Subtract a data/parameter-dependent maximum, adding it back to log L;
    # derivatives below refer to the original density, not the scaled factors.
    offset=log_reward.max(axis=2)
    factor=e[:,o].transpose(1,2,0)*np.exp(log_reward-offset[:,:,None])
    if shape.include_logger: factor*=q[:,a].transpose(1,2,0)
    forward=np.empty((n,h,k)); scale=np.empty((n,h))
    forward[:,0]=mu*factor[:,0]; scale[:,0]=forward[:,0].sum(axis=1); forward[:,0]/=scale[:,0,None]
    for j in range(1,h):
        forward[:,j]=np.einsum('ni,nij->nj',forward[:,j-1],t[a[:,j-1]])*factor[:,j]
        scale[:,j]=forward[:,j].sum(axis=1); forward[:,j]/=scale[:,j,None]
    backward=np.ones_like(forward)
    for j in range(h-2,-1,-1):
        backward[:,j]=np.einsum('nij,nj->ni',t[a[:,j]],factor[:,j+1]*backward[:,j+1])/scale[:,j+1,None]
    posterior=forward*backward
    posterior/=posterior.sum(axis=2,keepdims=True)
    joint=forward[:,:-1,:,None]*t[a[:,:-1]]*(factor[:,1:]*backward[:,1:])[:,:,None,:]/scale[:,1:,None,None]
    emission_counts=np.einsum('nhk,nhm->nkm',posterior,np.eye(shape.signals)[o])
    action_counts=np.einsum('nhk,nha->nka',posterior,np.eye(shape.actions)[a])
    transition_counts=np.einsum('nhij,nha->naij',joint,np.eye(shape.actions)[a[:,:-1]])
    reward_score=np.einsum('nhk,nha,nhk->nak',posterior,np.eye(shape.actions)[a],(r[:,:,None]-means[a])/shape.reward_sd**2)
    components=[posterior[:,0,:-1]-mu[:-1],(emission_counts-emission_counts.sum(axis=2,keepdims=True)*e)[...,:-1].reshape(n,-1)]
    if shape.include_logger:
        components.append((action_counts-action_counts.sum(axis=2,keepdims=True)*q)[...,:-1].reshape(n,-1))
    components += [(transition_counts-transition_counts.sum(axis=3,keepdims=True)*t)[...,:-1].reshape(n,-1),shape.reward_sd*reward_score.reshape(n,-1)]
    trajectory_score=np.column_stack(components)
    trajectory_ll=np.sum(np.log(scale)+offset,axis=1)
    calibration_score=np.zeros((len(labels),len(theta)))
    if len(labels):
        ec=np.zeros((len(labels),k,shape.signals))
        ec[np.arange(len(labels)),labels]=-e[labels]
        ec[np.arange(len(labels)),labels,cal_o]+=1
        calibration_score[:,k-1:k-1+k*(shape.signals-1)]=ec[...,:-1].reshape(len(labels),-1)
    calibration_ll=np.log(e[labels,cal_o])
    total_ll=trajectory_ll.sum()+calibration_ll.sum()
    total_score=trajectory_score.sum(axis=0)+calibration_score.sum(axis=0)
    if individual:
        return total_ll,total_score,trajectory_score,calibration_score
    return total_ll,total_score


def initial_parameter(observed,calibration,shape,rng):
    o,a,r=observed; labels,cal_o=calibration; k,m=shape.states,shape.signals
    counts=np.ones((k,m))*.5
    np.add.at(counts,(labels,cal_o),1)
    e=counts/counts.sum(axis=1,keepdims=True)
    weights=e[:,o].transpose(1,2,0); weights/=weights.sum(axis=2,keepdims=True)
    q=np.empty((k,shape.actions)); reward=np.empty((shape.actions,k))
    for action in range(shape.actions):
        mass=(weights*(a==action)[:,:,None]).sum(axis=(0,1))
        q[:,action]=mass+1
        reward[action]=(weights*(a==action)[:,:,None]*r[:,:,None]).sum(axis=(0,1))/np.maximum(mass,1)
    q/=q.sum(axis=1,keepdims=True)
    transition=np.stack([.55*np.eye(k)+.45*rng.dirichlet(np.ones(k)*3,size=k) for _ in range(shape.actions)])
    mu=weights[:,0].mean(axis=0)
    return pack(mu,e,q,transition,reward,shape)


def fit(observed,calibration,shape,seed=73,starts=2,maxiter=450):
    n=len(observed[0]); rng=np.random.default_rng(seed); candidates=[]
    def objective(theta):
        ll,score=likelihood_score(theta,observed,calibration,shape)
        return -ll/n,-score/n
    for j in range(starts):
        start=initial_parameter(observed,calibration,shape,rng)
        rewards=shape.actions*shape.states
        bounds=[(-8,8)]*(len(start)-rewards)+[(-250/shape.reward_sd,250/shape.reward_sd)]*rewards
        opt=minimize(objective,start,jac=True,method='L-BFGS-B',bounds=bounds,
                     options={'maxiter':maxiter,'ftol':1e-12,'gtol':1e-6,'maxls':35})
        candidates.append(opt)
    best=min(candidates,key=lambda c:c.fun)
    diagnostics={'optimizer_success':bool(best.success),'message':str(best.message),'iterations':int(best.nit),
        'average_score_max':float(abs(best.jac).max()),'objectives':[float(c.fun) for c in candidates],
        'statuses':[str(c.message) for c in candidates],
        'on_boundary':bool(np.any(abs(best.x[:-(shape.states*shape.actions)])>=7.999)),
        'trajectories':n,'calibration_rows':len(calibration[0])}
    return best.x,diagnostics


def policy_value(theta,shape,signal_policy,horizon=8,discount=.99):
    mu,e,_,t,reward=unpack(theta,shape)
    policy=np.asarray(signal_policy,float)
    if policy.shape!=(shape.signals,shape.actions) or np.any(policy<0) or not np.allclose(policy.sum(axis=1),1):
        raise ValueError('policy must be a fixed signal-to-action probability kernel')
    state_policy=e@policy
    transition=np.einsum('sa,ask->sk',state_policy,t)
    immediate=np.einsum('sa,as->s',state_policy,reward)
    value=np.zeros(shape.states)
    for _ in range(horizon): value=immediate+discount*transition@value
    return float(mu@value)


def contrast(theta,shape,horizon=8):
    never=np.column_stack((np.ones(shape.signals),np.zeros(shape.signals)))
    assist=never.copy(); assist[-2:]=[0,1]
    return policy_value(theta,shape,assist,horizon)-policy_value(theta,shape,never,horizon)


def uncertainty(theta,observed,calibration,shape,horizon=8,step=1e-4):
    p=len(theta); information=np.empty((p,p)); gradient=np.empty(p)
    for j in range(p):
        move=np.zeros(p); move[j]=step
        information[:,j]=-(likelihood_score(theta+move,observed,calibration,shape)[1]-likelihood_score(theta-move,observed,calibration,shape)[1])/(2*step)
        gradient[j]=(contrast(theta+move,shape,horizon)-contrast(theta-move,shape,horizon))/(2*step)
    asymmetry=float(np.max(abs(information-information.T)))
    information=(information+information.T)/2
    eigen=np.linalg.eigvalsh(information)
    if eigen.min()<=0: return {'available':False,'minimum_eigenvalue':float(eigen.min()),'hessian_asymmetry':asymmetry}
    inverse=np.linalg.inv(information)
    _,_,trajectory_scores,calibration_scores=likelihood_score(theta,observed,calibration,shape,individual=True)
    # Independent samples: retain separate means, rather than pooling scores.
    centered=[a-a.mean(axis=0) for a in [trajectory_scores,calibration_scores] if len(a)]
    meat=sum(a.T@a for a in centered)
    sandwich=inverse@meat@inverse
    excluded=np.arange(shape.states-1,shape.states-1+shape.states*(shape.signals-1))
    keep=np.setdiff1d(np.arange(p),excluded)
    return {'available':True,'model_se':float(np.sqrt(gradient@inverse@gradient)),
        'sandwich_se':float(np.sqrt(gradient@sandwich@gradient)),
        'treat_emissions_fixed_se':float(np.sqrt(gradient[keep]@np.linalg.solve(information[np.ix_(keep,keep)],gradient[keep]))),
        'minimum_eigenvalue':float(eigen.min()),'information_condition':float(eigen.max()/eigen.min()),
        'hessian_asymmetry':asymmetry,'derivative_step':step}


def recover_marked_model(emission,joint,marked_reward):
    """Population algebra: unnormalised P(O_t,A_t,O_next), not P(.|A)."""
    e=np.asarray(emission).T
    left=np.linalg.solve(e.T@e,e.T)
    latent=np.array([left@ja@left.T for ja in joint])
    mass=latent.sum(axis=2)
    mu=mass.sum(axis=0)
    logger=(mass/mu).T
    transitions=latent/mass[:,:,None]
    reward=np.array([left@ka for ka in marked_reward])/mass
    return mu,logger,transitions,reward
