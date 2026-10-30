"""Frozen joint-law comparisons, including declared-law violations."""
import numpy as np
from scipy.signal import lfilter
from scipy.stats import norm
from causalbank.joint_audited import joint_effect
from causalbank.joint_projection_v11 import effect, variance_reference


def request(spec, cell, index):
    d = spec['designs'][cell]
    rng = np.random.default_rng([spec['seed'], cell, index])
    n, t, m = d.get('pairs', 100), d.get('dates', 160), d.get('gold', 400)
    q, e, rho = d.get('q', .4), d.get('error', .08), d.get('rho', .5)
    beta, decoy = 1., -.4
    u, v = rng.normal(size=(2, n))*.8
    innovations = rng.normal(size=t)*.6*np.sqrt(1-rho*rho)
    innovations[0] = rng.normal()*.6
    calendar = lfilter([1], [1, -rho], innovations)
    focal = beta+u[:, None]+calendar+rng.normal(size=(n, t))
    companion = decoy+v[:, None]+calendar+rng.normal(size=(n, t))
    correct = rng.random(n) < d.get('identity_p', .6)
    a = rng.choice([-1., 1.], size=(n, t))
    candidates = a[:, None, :]*np.stack((np.where(correct[:, None], focal, companion), np.where(correct[:, None], companion, focal)), axis=1)
    actual_q = d.get('actual_q', q)
    if d.get('shared_audit'):
        r = np.repeat(rng.random((n+9)//10) < actual_q, 10)[:n]
    else:
        r = rng.random(n) < actual_q
    flips = rng.random(n) < e
    if d.get('endogenous_error'):
        flips = u > np.quantile(u, 1-e)
    full_labels = (correct ^ flips).astype(float)
    labels = np.where(r, full_labels, np.nan)
    gold = (rng.random(m) < e).astype(int)
    bandwidth = d.get('bandwidth', max(1, int(t**(1/3))))
    primary = effect(a, candidates, r, labels, np.full(n, q), gold, bandwidth, alpha=spec['alpha'])
    old = joint_effect(a, candidates, r, np.where(r, full_labels, 0), np.full(n, q), bandwidth=bandwidth,
                       gold_errors=gold, alpha=.05)
    reference = variance_reference(n, t, m, q, e, rho, .8, .6, 1., beta, decoy)
    if 'estimate' in primary:
        se = float(1000*np.sqrt(sum(reference.values())))
        z = norm.ppf(1-spec['alpha']/2)
        oracle = dict(status='oracle_diagnostic', estimate=primary['estimate'], standard_error=se,
                      interval=[primary['estimate']-z*se, primary['estimate']+z*se])
    else:
        oracle = dict(status='unavailable_primary_estimate')
    return dict(truth=1000*beta, methods=dict(interaction_adjusted=primary, inherited_double_count=old, oracle_first_order=oracle),
                labels=int(r.sum()+m), history_rows=2*n*t, analytical_components=reference,
                gold_errors=int(gold.sum()), bandwidth=bandwidth)
