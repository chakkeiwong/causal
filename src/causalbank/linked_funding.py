"""Outcome-linked audits for the selected independent-pilot funding calendar.

Audit probabilities and exact labels are supplied scientific premises. This
construction has no inverse identity-mixing matrix or estimated label-error law.
"""
import numpy as np
from scipy.stats import norm

from .funding_calibration import LagAccumulator, pilot_data, simulate_rows
from .linkage_sets import encode_set
from .streaming_pilot import train_streaming_pilot

LINKED_DECLARATIONS = {
    'correct_fixed_action_mean': True,
    'exogenous_structural_innovation': True,
    'finite_innovation_response_horizon': True,
    'independent_invariant_pilot': True,
    'stationary_common_calendar': True,
    'known_positive_audit_inclusion': True,
    'conditionally_independent_audits_across_origins': True,
    'truthful_linked_outcome_labels': True,
}


def pseudo_rows(rows, audited, labels, inclusion, horizon, *, augmentation=True):
    """Only sampled labels are available; each audit resolves a full origin vector."""
    rows = np.asarray(rows, float)
    r, label, q = np.asarray(audited), np.asarray(labels, float), np.asarray(inclusion, float)
    h = horizon + 1
    if rows.ndim != 2 or rows.shape[1] != 5 + 2*h or not np.isfinite(rows).all():
        raise ValueError('Invalid candidate histories')
    n = len(rows)
    if (not np.isin(rows[:, 0], [0, 1]).all() or not np.all(rows[:, 2] == 1)
            or r.shape != (n,) or label.shape != (n,) or q.shape != (n,)
            or not np.isin(r, [0, 1]).all()):
        raise ValueError('Invalid stratum, audit dimensions or indicator')
    if not np.isfinite(q).all() or np.any(q <= 0) or np.any(q > 1):
        raise ValueError('Known positive inclusion probabilities required')
    keep = r.astype(bool)
    if not np.isin(label[keep], [0, 1]).all() or not np.isnan(label[~keep]).all():
        raise ValueError('Binary sampled labels and absent unsampled labels required')
    first, second = rows[:, 5:5+h], rows[:, 5+h:]
    baseline = (first + second)/2 if augmentation else np.zeros_like(first)
    outcome = baseline.copy()
    focal = np.where(label[keep, None] == 1, first[keep], second[keep])
    outcome[keep] += (focal - baseline[keep])/q[keep, None]
    if not np.isfinite(outcome).all():
        raise ValueError('Nonfinite audit-adjusted outcomes')
    return np.column_stack((rows[:, :5], outcome))


def fit_linked_funding(pilot_rows, rows, target, pilot_audit, audit, penalties,
                       *, augmentation=True, chunk_size=4096, alpha=.05,
                       declarations=None):
    target.validate()
    if declarations != LINKED_DECLARATIONS:
        raise ValueError('Explicit linked-outcome scientific declarations required')
    if (len(rows) <= 2*(target.horizon+2) or len(pilot_rows) < 4*len(rows)
            or not isinstance(chunk_size, int) or isinstance(chunk_size, bool)
            or chunk_size < 1 or not 0 < alpha < 1):
        raise ValueError('Invalid information ratio, history size, chunk or confidence')
    pilot = pseudo_rows(pilot_rows, *pilot_audit, target.horizon, augmentation=augmentation)
    data_rows = pseudo_rows(rows, *audit, target.horizon, augmentation=augmentation)
    for source, info in ((pilot_rows, pilot_audit), (rows, audit)):
        for s in (0, 1):
            if np.sum((source[:, 0] == s) & np.asarray(info[0], bool)) < 2:
                return dict(status='unavailable_outcome_audit')
    fit = train_streaming_pilot(pilot, penalties, chunk_size)
    coefficient = fit['coefficient']
    n, weights = len(rows), target.weights()
    qsum, products = np.zeros(2), np.zeros(2)
    for start in range(0, n, chunk_size):
        block = pilot_data(data_rows[start:start+chunk_size])
        fitted = block['x'] @ coefficient
        v = block['action'] - fitted[:, 0]
        outcome = (block['outcomes'] - fitted[:, 1:]) @ weights
        for s in (0, 1):
            keep = block['stratum'] == s
            qsum[s] += v[keep] @ v[keep]
            products[s] += v[keep] @ outcome[keep]
    if not np.isfinite(qsum).all() or np.any(qsum <= 0):
        return dict(status='unavailable_action_variation')
    slopes = products/qsum
    accumulator = LagAccumulator(target.horizon)
    raw_score_energy = 0.
    for start in range(0, n, chunk_size):
        block = pilot_data(data_rows[start:start+chunk_size])
        fitted = block['x'] @ coefficient
        v = block['action'] - fitted[:, 0]
        outcome = (block['outcomes'] - fitted[:, 1:]) @ weights
        scores = np.empty(len(v))
        for s in (0, 1):
            keep = block['stratum'] == s
            scores[keep] = .5*n*v[keep]*(outcome[keep]-v[keep]*slopes[s])/qsum[s]
            raw_score = .5*n*v[keep]*outcome[keep]/qsum[s]
            raw_score_energy += float(raw_score @ raw_score)
        accumulator.add(scores)
    value = float(.5*slopes.sum()-target.direct_cost())
    variance = accumulator.variance_of_mean()
    numerical_floor = (8*np.finfo(float).eps)**2*raw_score_energy/n**2
    if not np.isfinite(variance) or variance <= max(0., numerical_floor):
        return dict(status='unavailable_response_variance', estimate=value)
    se = float(np.sqrt(variance))
    bounds = [float(value-norm.ppf(1-alpha/2)*se), float(value+norm.ppf(1-alpha/2)*se)]
    return dict(status='computed_set', estimate=value, standard_error=se,
                financial_set=encode_set([bounds]), interval=bounds, calendar_variance=variance,
                stratum_slopes=slopes.tolist(), action_sums=qsum.tolist(),
                evaluation_dates=n, pilot_dates=len(pilot_rows),
                evaluation_labels=int(np.sum(audit[0])), pilot_labels=int(np.sum(pilot_audit[0])),
                pilot_penalty=float(fit['penalty']), augmentation=bool(augmentation), alpha=alpha,
                scope='Pointwise dependent-calendar normal interval under truthful linked-outcome audits, known inclusion and exogeneity; premises are not verified by fitting.')


def simulate_linked(base, observation, dates, data_seed, audit_seed, *,
                    inclusion=.25, actual_inclusion=None, label_error=0., correlation=0.):
    """Synthetic truth is used only to supply sampled audit labels and check maps."""
    rows = simulate_rows(base, observation, dates, data_seed, correlation)
    true_rows = simulate_rows(base, dict(observation, correct_pair_probability=[1., 1.]),
                              dates, data_seed, correlation)
    h = base['horizon'] + 1
    correct = np.all(rows[:, 5:5+h] == true_rows[:, 5:5+h], axis=1)
    focal = np.where(correct[:, None], rows[:, 5:5+h], rows[:, 5+h:])
    if not np.array_equal(focal, true_rows[:, 5:5+h]):
        raise ValueError('Simulator identity witness failed')
    rng = np.random.default_rng(audit_seed)
    actual = inclusion if actual_inclusion is None else actual_inclusion
    sampled = rng.random(dates) < actual
    flips = rng.random(dates) < label_error
    labels = np.full(dates, np.nan)
    labels[sampled] = (correct ^ flips)[sampled].astype(float)
    return rows, (sampled, labels, np.full(dates, inclusion))
