"""Explicit persistent-pair Gaussian random-effects experiment.

The scalar covariance corrects double-counted cell interactions. It remains
first-order inference with independent symmetric gold-label validation.
"""
import numpy as np
from scipy.stats import norm
from .joint_audited import bartlett
from .linkage_sets import binomial_interval


def effect(action, candidates, audited, labels, inclusion, gold, bandwidth, *, alpha=.01,
           independent_pairs=True, exogenous_maps=True, known_inclusion=True):
    if not (independent_pairs and exogenous_maps and known_inclusion):
        return dict(status='refused_unsupported_sampling_or_map')
    a, y = np.asarray(action, float), np.asarray(candidates, float)
    r, label, q, gold = map(np.asarray, (audited, labels, inclusion, gold))
    n, t = a.shape
    if (y.shape != (n, 2, t) or n < 3 or t < 3 or len(gold) < 30 or
        any(z.shape != (n,) for z in (r, label, q)) or
        not np.isin(a, [-1, 1]).all() or not np.isin(r, [0, 1]).all() or
        not np.isin(label[r == 1], [0, 1]).all() or
        not np.isnan(label[r == 0]).all() or not np.isin(gold, [0, 1]).all() or
        not np.isfinite(y).all() or not np.isfinite(q).all() or np.any(q <= 0) or np.any(q > 1)):
        raise ValueError('Aligned finite histories and truthful observed audit schema required')
    e = float(gold.mean())
    ci = binomial_interval(int(gold.sum()), len(gold), .05)
    if ci[1] >= .5:
        return dict(status='unqualified_label_rank', gold_interval=ci)
    observed_label = np.where(r == 1, label, 0.)
    scores = a[:, None, :]*y
    avg, diff = scores.mean(axis=1), scores[:, 0]-scores[:, 1]
    term = (r/q)*(2*observed_label-1)
    z = avg + term[:, None]*diff/(2*(1-2*e))
    row, col = z.mean(axis=1), z.mean(axis=0)
    residual = z-row[:, None]-col[None, :]+z.mean()
    interaction = float(np.sum(residual**2)/((n-1)*(t-1))/(n*t))
    pair = float(row.var(ddof=1)/n)
    calendar = float(bartlett(col, bandwidth)/t)
    derivative = float(np.mean(term[:, None]*diff/(1-2*e)**2))
    validation = derivative**2*e*(1-e)/len(gold)
    variance = pair+calendar-interaction+validation
    if not np.isfinite(variance) or variance <= 0:
        return dict(status='unavailable_variance', variance_components=dict(pair=pair, calendar=calendar, interaction=interaction, gold=validation))
    value, se = float(1000*z.mean()), float(1000*np.sqrt(variance))
    critical = float(norm.ppf(1-alpha/2))
    return dict(status='computed_conditional', estimate=value, standard_error=se,
        interval=[value-critical*se, value+critical*se], gold_interval=ci,
        variance_components=dict(pair=pair, calendar=calendar, interaction_subtracted=interaction, gold=validation),
        scope='Joint iid-pair, mixing-calendar, independent-gold first-order limit; fixed error below one half and comparable growth.')


def variance_reference(n, t, m, q, e, rho, pair_sd, calendar_sd, cell_sd, beta, decoy):
    second = 1/(q*(1-2*e)**2)
    d = (beta-decoy)/2
    pair = (pair_sd**2*(1+second)/2+d*d*(second-1))/n
    calendar = calendar_sd**2*(t+2*sum((t-k)*rho**k for k in range(1, t)))/t**2
    cell = cell_sd**2*(1+second)/(2*n*t)
    gold = ((beta-decoy)/(1-2*e))**2*e*(1-e)/m
    return dict(pair=pair, calendar=calendar, cell=cell, gold=gold)
