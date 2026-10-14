"""A two-state, binary-signal/reward controlled model with exogenous logging.

The numerical likelihood conditions on actions. It has a causal interpretation
only for the separately stipulated randomized-logging structural model.
"""
import numpy as np
from scipy.optimize import minimize
from scipy.special import expit, logit


def unpack(parameter):
    p = expit(np.asarray(parameter))
    return {"mu": np.array([1-p[0],p[0]]),
            "emission": np.column_stack((1-p[1:3],p[1:3])),
            "transition": np.stack((1-p[3:7],p[3:7]),axis=-1).reshape(2,2,2),
            "reward": p[7:11].reshape(2,2)}


def pack(model):
    return logit(np.r_[model["mu"][1],model["emission"][:,1],
                        model["transition"][:,:,1].ravel(),model["reward"].ravel()])


def forward_backward(data, model, counts=True):
    o,a,r = data
    n,h = o.shape
    mu,e,p,b = (model[k] for k in ("mu","emission","transition","reward"))
    emission = np.stack([e[:,o[:,t]].T * np.where(r[:,t,None],b[a[:,t]],1-b[a[:,t]]) for t in range(h)])
    alpha = np.empty((h,n,2))
    scale = np.empty((h,n))
    unnormalized = mu*emission[0]
    scale[0] = unnormalized.sum(axis=1)
    alpha[0] = unnormalized/scale[0,:,None]
    for t in range(1,h):
        unnormalized = np.einsum("ni,nij->nj",alpha[t-1],p[a[:,t-1]])*emission[t]
        scale[t] = unnormalized.sum(axis=1)
        alpha[t] = unnormalized/scale[t,:,None]
    loglik = np.log(scale).sum(axis=0)
    if not counts:
        return loglik
    gamma = np.empty_like(alpha)
    gamma[-1] = alpha[-1]
    beta = np.ones((n,2))
    transition = np.zeros((n,2,2,2))
    for t in range(h-2,-1,-1):
        end = emission[t+1]*beta
        xi = alpha[t,:,:,None]*p[a[:,t]]*end[:,None,:]/scale[t+1,:,None,None]
        gamma[t] = xi.sum(axis=2)
        for action in range(2):
            transition[:,action] += xi*(a[:,t]==action)[:,None,None]
        beta = np.einsum("nij,nj->ni",p[a[:,t]],end)/scale[t+1,:,None]
    ec = np.zeros((n,2,2))
    rc = np.zeros((n,2,2,2))  # trajectory, action, state, reward value
    for t in range(h):
        for value in range(2):
            ec[:,:,value] += gamma[t]*(o[:,t]==value)[:,None]
            for action in range(2):
                rc[:,action,:,value] += gamma[t]*((a[:,t]==action)&(r[:,t]==value))[:,None]
    return loglik, gamma[0], ec, transition, rc


def score(parameter, data):
    model = unpack(parameter)
    ll,mc,ec,tc,rc = forward_backward(data,model)
    gradient = np.column_stack((mc[:,1]-model["mu"][1],
                               ec[:,:,1]-ec.sum(axis=-1)*model["emission"][:,1],
                               (tc[:,:,:,1]-tc.sum(axis=-1)*model["transition"][:,:,1]).reshape(len(mc),4),
                               (rc[:,:,:,1]-rc.sum(axis=-1)*model["reward"]).reshape(len(mc),4)))
    return ll,gradient


def fit(data, seed, starts=3, em_iterations=70, optimizer_iterations=180):
    rng = np.random.default_rng(seed)
    diagnostics, candidates = [], []
    for start in range(starts):
        model = {"mu":np.array([.6,.4]),
                 "emission":np.array([[.8,.2],[.25,.75]]),
                 "transition":np.array([[[.8,.2],[.3,.7]],[[.8,.2],[.5,.5]]]),
                 "reward":np.array([[.8,.3],[.85,.55]])}
        parameter = pack(model) + rng.normal(scale=.6,size=11)
        history = []
        for iteration in range(em_iterations):
            model = unpack(parameter)
            ll,mc,ec,tc,rc = forward_backward(data,model)
            history.append(float(ll.sum()))
            if len(history)>1 and abs(history[-1]-history[-2])<1e-7*len(data[0]):
                break
            # Box-constrained Bernoulli complete-data maximizers.
            counts = [mc.sum(axis=0),ec.sum(axis=0),tc.sum(axis=0),rc.sum(axis=0)]
            new = np.r_[counts[0][1]/counts[0].sum(),
                        counts[1][:,1]/counts[1].sum(axis=-1),
                        (counts[2][:,:,1]/counts[2].sum(axis=-1)).ravel(),
                        (counts[3][:,:,1]/counts[3].sum(axis=-1)).ravel()]
            parameter = logit(np.clip(new,.002,.998))
        em_ll = float(forward_backward(data,unpack(parameter),False).sum())
        candidates.append((em_ll,parameter.copy()))
        diagnostics.append({"start":start,"em_iterations":iteration+1,
                            "em_cap":iteration+1==em_iterations,
                            "em_loglik":em_ll,"minimum_increment":float(min(np.diff(history+[em_ll])))})
    best = max(candidates,key=lambda x:x[0])
    def objective(parameter):
        ll,g = score(parameter,data)
        return -ll.mean(),-g.mean(axis=0)
    optimum = minimize(objective,best[1],jac=True,method="L-BFGS-B",
                       bounds=[(logit(.002),logit(.998))]*11,
                       options={"maxiter":optimizer_iterations,"ftol":1e-12,"gtol":1e-7,"maxls":30})
    optimized_ll = float(-optimum.fun*len(data[0]))
    parameter = optimum.x if optimized_ll >= best[0]-1e-8 else best[1]
    ll,g = score(parameter,data)
    return parameter, {"starts":diagnostics,"em_best_loglik":best[0],
                       "optimized_loglik":optimized_ll,"loglik":float(ll.sum()),
                       "optimizer_success":bool(optimum.success),"optimizer_message":str(optimum.message),
                       "optimizer_iterations":int(optimum.nit),
                       "score_mean_max":float(abs(g.mean(axis=0)).max()),
                       "on_boundary":bool(np.any(abs(parameter)>logit(.998)-1e-4))}


def value(parameter, policy=(0,1), horizon=8, discount=.99):
    """Fixed signal-to-action map; fitting never changes this mapping."""
    model = unpack(parameter)
    mu,e,p,b = (model[k] for k in ("mu","emission","transition","reward"))
    transition, reward = np.zeros((2,2)), np.zeros(2)
    for observation,action in enumerate(policy):
        transition += e[:,observation,None]*p[action]
        reward += e[:,observation]*(100*b[action]-12*action)
    v = np.zeros(2)
    for _ in range(horizon):
        v = reward+discount*transition@v
    return float(mu@v)


def contrast(parameter,horizon=8):
    return value(parameter,(0,1),horizon=horizon)-value(parameter,(0,0),horizon=horizon)


def information_interval(parameter, data, horizon=8):
    """Observed-information delta interval under regular identified iid trajectories."""
    step = 1e-4
    identity = np.eye(len(parameter))
    information = np.column_stack([-(score(parameter+step*v,data)[1].mean(axis=0)-
                                    score(parameter-step*v,data)[1].mean(axis=0))/(2*step) for v in identity])
    information = (information+information.T)/2
    eigen = np.linalg.eigvalsh(information)
    gradient = np.array([(contrast(parameter+step*v,horizon)-contrast(parameter-step*v,horizon))/(2*step) for v in identity])
    if eigen.min()<=1e-7:
        return {"status":"singular_or_indefinite","minimum_eigenvalue":float(eigen.min()),"se":None}
    variance = float(gradient@np.linalg.solve(information,gradient)/len(data[0]))
    return {"status":"regular_local","minimum_eigenvalue":float(eigen.min()),
            "condition_number":float(eigen.max()/eigen.min()),"se":float(np.sqrt(variance))}


def simulate(model, trajectories, horizon, rng, private_logger=False):
    mu,e,p,b = (model[k] for k in ("mu","emission","transition","reward"))
    o,a,r = (np.empty((trajectories,horizon),dtype=int) for _ in range(3))
    state = (rng.random(trajectories)<mu[1]).astype(int)
    for t in range(horizon):
        o[:,t] = rng.random(trajectories)<e[state,1]
        logging = np.where(state==1,.9,.1) if private_logger else .5
        a[:,t] = rng.random(trajectories)<logging
        r[:,t] = rng.random(trajectories)<b[a[:,t],state]
        state = (rng.random(trajectories)<p[a[:,t],state,1]).astype(int)
    return o,a,r
