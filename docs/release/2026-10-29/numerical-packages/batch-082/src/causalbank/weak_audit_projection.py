"""Rank-robust funding-value set for a fixed independent streaming pilot.

The audit component uses exact binomial inversion. Four observable response
bands use a dependent-calendar normal approximation; no finite-sample or bank
coverage claim follows from the combined construction.
"""
import math

import numpy as np
from scipy.stats import beta, norm

from .funding_calibration import DECLARATIONS, LagAccumulator, pilot_data
from .linkage_sets import encode_set, pair_projection, weighted_sum
from .streaming_pilot import train_streaming_pilot


def audit_interval(successes, size, error):
    """Outward-rounded Clopper--Pearson two-sided interval."""
    if (not isinstance(successes, (int, np.integer))
            or not isinstance(size, (int, np.integer))
            or not 0 <= successes <= size or size < 1 or not 0 < error < 1):
        raise ValueError('Invalid binomial audit input')
    lower = 0.0 if successes == 0 else beta.ppf(error / 2, successes, size - successes + 1)
    upper = 1.0 if successes == size else beta.ppf(1 - error / 2, successes + 1, size - successes)
    if not np.isfinite(lower + upper):
        raise ValueError('Binomial inversion failed')
    return (0.0 if lower == 0 else float(np.nextafter(lower, -math.inf)),
            1.0 if upper == 1 else float(np.nextafter(upper, math.inf)))


def _validate(pilot_rows, rows, target, successes, sizes, penalties, chunk_size,
              declarations, response_error, audit_error):
    target.validate()
    length = 5 + 2 * (target.horizon + 1)
    if (not isinstance(chunk_size, int) or isinstance(chunk_size, bool) or chunk_size < 1
            or np.ndim(rows) != 2 or np.ndim(pilot_rows) != 2
            or rows.shape[1] != length or pilot_rows.shape[1] != length
            or len(rows) <= 2 * (target.horizon + 2)
            or len(pilot_rows) < 4 * len(rows)):
        raise ValueError('Invalid evaluation/pilot dimensions or information ratio')
    if declarations != DECLARATIONS:
        raise ValueError('Explicit compatible scientific declarations required')
    for data in (rows, pilot_rows):
        if (not np.isfinite(data).all() or not np.isin(data[:, 0], [0, 1]).all()
                or not np.all(data[:, 2] == 1)):
            raise ValueError('Invalid stratum, intercept or nonfinite history')
    counts, totals = np.asarray(successes), np.asarray(sizes)
    if (counts.shape != (2,) or totals.shape != (2,) or
            not all(isinstance(x, (int, np.integer)) for x in list(counts) + list(totals)) or
            any(n < 1 or k < 0 or k > n for k, n in zip(counts, totals))):
        raise ValueError('Two independent binomial audit counts required')
    if (not penalties or any(not np.isfinite(p) or p < 0 for p in penalties)
            or not 0 < response_error < 1 or not 0 < audit_error < 1
            or response_error + audit_error >= 1):
        raise ValueError('Invalid fixed penalties or error budget')
    return counts, totals


def _blocks(rows, size):
    for start in range(0, len(rows), size):
        yield rows[start:start + size]


def _residuals(block, coefficient, weights):
    data = pilot_data(block)
    fitted = data['x'] @ coefficient
    action = data['action'] - fitted[:, 0]
    residuals = data['outcomes'] - fitted[:, 1:]
    h = len(weights)
    reduced = np.column_stack((residuals[:, :h] @ weights,
                               residuals[:, h:] @ weights))
    return data['stratum'], action, reduced


def observable_scores(pilot_rows, rows, target, penalties, chunk_size):
    """Two passes; four observable monetary slopes and scalar score variances."""
    fit = train_streaming_pilot(pilot_rows, penalties, chunk_size)
    coefficient = fit['coefficient']
    weights = target.weights()
    qsum = np.zeros(2)
    products = np.zeros((2, 2))
    for block in _blocks(rows, chunk_size):
        stratum, action, outcome = _residuals(block, coefficient, weights)
        for group in (0, 1):
            keep = stratum == group
            qsum[group] += action[keep] @ action[keep]
            products[group] += action[keep] @ outcome[keep]
    if np.any(qsum <= 0):
        return dict(status='unavailable_action_variation')
    slopes = products / qsum[:, None]
    accumulators = [LagAccumulator(target.horizon) for _ in range(4)]
    n = len(rows)
    for block in _blocks(rows, chunk_size):
        stratum, action, outcome = _residuals(block, coefficient, weights)
        scores = np.zeros((len(block), 4))
        for group in (0, 1):
            keep = stratum == group
            scores[keep, 2 * group:2 * group + 2] = (
                n * action[keep, None] *
                (outcome[keep] - action[keep, None] * slopes[group]) / qsum[group])
        for j, accumulator in enumerate(accumulators):
            accumulator.add(scores[:, j])
    variances = np.array([accumulator.variance_of_mean() for accumulator in accumulators])
    if not np.isfinite(variances).all() or np.any(variances <= 0):
        return dict(status='unavailable_response_variance',
                    candidate_financial_means=slopes.ravel().tolist(),
                    candidate_financial_variances=variances.tolist())
    return dict(status='computed', candidate_financial_means=slopes.ravel().tolist(),
                candidate_financial_variances=variances.tolist(),
                pilot_penalty=float(fit['penalty']),
                pilot_validation_loss_gap=float(fit['validation_loss_gap']))


def fit_weak_audit_projection(pilot_rows, rows, target, successes, sizes, penalties,
                              *, chunk_size=4096, declarations=None,
                              response_error=.025, audit_error=.025):
    """Project four simultaneous response bands and two exact audit intervals."""
    counts, totals = _validate(pilot_rows, rows, target, successes, sizes,
                               penalties, chunk_size, declarations,
                               response_error, audit_error)
    observable = observable_scores(pilot_rows, rows, target, penalties, chunk_size)
    if observable['status'] != 'computed':
        return observable
    means = np.asarray(observable['candidate_financial_means']).reshape(2, 2)
    variances = np.asarray(observable['candidate_financial_variances']).reshape(2, 2)
    z = norm.ppf(1 - response_error / 8)
    bands = np.stack((means - z * np.sqrt(variances),
                      means + z * np.sqrt(variances)), axis=-1)
    audit = [audit_interval(int(k), int(m), audit_error / 2)
             for k, m in zip(counts, totals)]
    by_stratum = [pair_projection(bands[s, 0], bands[s, 1], audit[s])
                  for s in (0, 1)]
    financial = weighted_sum(by_stratum, [.5, .5], -target.direct_cost())
    status = 'computed_set' if financial else 'empty_projection'
    return dict(observable, status=status, financial_set=encode_set(financial),
                candidate_bands=bands.tolist(), audit_intervals=audit,
                stratum_sets=[encode_set(part) for part in by_stratum],
                response_error=response_error, audit_error=audit_error,
                pilot_dates=len(pilot_rows), evaluation_dates=len(rows),
                scope='Exact independent-binomial audit intervals plus asymptotic dependent-calendar response bands; set projection is rank-robust but can be unbounded. Scientific declarations are premises, not validated by this fit.')
