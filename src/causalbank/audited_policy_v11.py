"""Selected17 nonlinear servicing: exact audited likelihood and policy weights.

Representative truthful full-state audits and supplied logger probabilities
are additional information. Direct policy evaluation has no filter optimizer.
"""
import numpy as np
from scipy.special import ndtr
from scipy.stats import t

TRUTH = np.array([.35, .3, .4, np.log(.35), np.log(.5), -.2, 1.1, .25,
                  .1, .8, -.2, .35, np.log(.4), .1, np.log(.8), np.log(.9), .25])


def lognormal(x, mean, logvar):
    return -.5*(np.log(2*np.pi)+logvar+(x-mean)**2*np.exp(-logvar))


def logger(p, s, o, epsilon=.05):
    return epsilon+(1-2*epsilon)/(1+np.exp(-(p[5]+p[6]*s+p[7]*o)))


def complete_loglik(p, data, s, epsilon=.05):
    o, a, r = data[:, :, 0], data[:, :, 1], data[:, :, 2]
    prob = logger(p, s, o, epsilon)
    reward = p[8]+p[9]*s+p[10]*a+p[11]*s*a+p[16]*np.tanh(s)*a
    ll = lognormal(s[:, 0], p[13], p[14])+np.sum(lognormal(o, s, p[4])+a*np.log(prob)+(1-a)*np.log1p(-prob)+lognormal(r, reward, p[12]), axis=1)
    means = p[0]*s[:, :-1]+p[1]*np.tanh(s[:, :-1])+p[2]*a[:, :-1]
    variance = p[3]*(1-a[:, :-1])+p[15]*a[:, :-1]
    return ll+np.sum(lognormal(s[:, 1:], means, variance), axis=1)


def simulate(p, n, horizon, rng, *, epsilon=.05, misspecification=False):
    state = np.empty((n, horizon)); data = np.empty((n, horizon, 3))
    state[:, 0] = p[13]+np.sqrt(np.exp(p[14]))*rng.normal(size=n)
    for j in range(horizon):
        s = state[:, j]
        o = s+np.sqrt(np.exp(p[4]))*rng.normal(size=n)
        a = rng.binomial(1, logger(p, s, o, epsilon))
        reward = p[8]+p[9]*s+p[10]*a+p[11]*s*a+p[16]*np.tanh(s)*a
        r = reward+np.sqrt(np.exp(p[12]))*rng.normal(size=n)
        data[:, j] = np.column_stack((o, a, r))
        if j+1 < horizon:
            state[:, j+1] = p[0]*s+p[1]*np.tanh(s)+p[2]*a+np.sqrt(np.exp(p[3])*(1-a)+np.exp(p[15])*a)*rng.normal(size=n)
            if misspecification:
                state[:, j+1] += .35*np.sin(2*s)
    return data, state


def policy_estimate(data, supplied_probabilities, thresholds, *, alpha=.01, selection='independent'):
    if selection != 'independent':
        return dict(status='refused_policy_evaluation_leakage')
    data, q, thresholds = map(np.asarray, (data, supplied_probabilities, thresholds))
    n, h, _ = data.shape
    if (q.shape != (n, h) or thresholds.shape != (h,) or n < 3 or
        not np.isfinite(data).all() or not np.isfinite(q).all() or np.any(q <= 0) or np.any(q >= 1)):
        raise ValueError('Aligned data, independent policy and positive supplied logger required')
    action = data[:, :, 1]
    if not np.isin(action, [0, 1]).all():
        raise ValueError('Binary actions required')
    agrees = action == (data[:, :, 0] > thresholds)
    ratios = agrees/np.where(action == 1, q, 1-q)
    weights = np.cumprod(ratios, axis=1)
    contributions = np.sum(weights*data[:, :, 2]*.97**np.arange(h), axis=1)*1000
    estimate = float(contributions.mean()); se = float(contributions.std(ddof=1)/np.sqrt(n))
    if not np.isfinite(se) or se <= 0:
        return dict(status='unavailable_policy_variance')
    critical = float(t.ppf(1-alpha/2, n-1))
    final = weights[:, -1]
    return dict(status='computed_conditional', estimate=estimate, standard_error=se,
        interval=[estimate-critical*se, estimate+critical*se],
        final_weight_ess=float(final.sum()**2/(final@final)) if final@final else 0.,
        max_weight=float(weights.max()),
        scope='Fixed independently chosen observable policy; truthful representative full-state audits; known true private logger. Trajectory CLT, no uniform finite or optimal-policy claim.')


def grid_value(p, thresholds, nodes=801, limit=12., misspecification=False):
    grid = np.linspace(-limit, limit, nodes)
    width = 2*limit/(nodes-1)
    w = np.full(nodes, width); w[[0, -1]] *= .5
    mass = np.exp(lognormal(grid, p[13], p[14]))*w
    mean = p[0]*grid+p[1]*np.tanh(grid)
    if misspecification:
        mean += .35*np.sin(2*grid)
    matrices = [np.exp(lognormal(grid[None, :], mean[:, None]+p[2]*a, p[3] if a == 0 else p[15]))*w[None, :] for a in (0, 1)]
    result = 0.
    for j, threshold in enumerate(thresholds):
        prob = ndtr((grid-threshold)*np.exp(-p[4]/2))
        reward = p[8]+p[9]*grid+(p[10]+p[11]*grid+p[16]*np.tanh(grid))*prob
        result += .97**j*(mass@reward)
        mass = (mass*(1-prob))@matrices[0]+(mass*prob)@matrices[1]
    return float(1000*result)
