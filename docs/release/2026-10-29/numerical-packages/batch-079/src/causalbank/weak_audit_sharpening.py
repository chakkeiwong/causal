"""Average/difference primitive bands retain candidate shared-score information."""
import numpy as np
from scipy.stats import norm

from .funding_calibration import LagAccumulator
from .linkage_sets import encode_set, sum_difference_projection, weighted_sum
from .streaming_pilot import train_streaming_pilot
from .weak_audit_projection import _validate, _blocks, _residuals, audit_interval


def transformed_scores(pilot_rows, rows, target, penalties, chunk_size):
    coefficient = train_streaming_pilot(pilot_rows, penalties, chunk_size)['coefficient']
    weights = target.weights()
    transform = np.array([[.5, .5], [.5, -.5]])
    qsum, products = np.zeros(2), np.zeros((2, 2))
    for block in _blocks(rows, chunk_size):
        strata, action, outcome = _residuals(block, coefficient, weights)
        outcome = outcome @ transform.T
        for s in (0, 1):
            keep = strata == s
            qsum[s] += action[keep] @ action[keep]
            products[s] += action[keep] @ outcome[keep]
    if np.any(qsum <= 0):
        return dict(status='unavailable_action_variation')
    means = products / qsum[:, None]
    n = len(rows)
    accumulators = [LagAccumulator(target.horizon) for _ in range(4)]
    for block in _blocks(rows, chunk_size):
        strata, action, outcome = _residuals(block, coefficient, weights)
        outcome = outcome @ transform.T
        scores = np.zeros((len(block), 4))
        for s in (0, 1):
            keep = strata == s
            scores[keep, 2 * s:2 * s + 2] = (n * action[keep, None] *
                (outcome[keep] - action[keep, None] * means[s]) / qsum[s])
        for j, accumulator in enumerate(accumulators):
            accumulator.add(scores[:, j])
    variances = np.array([x.variance_of_mean() for x in accumulators])
    paired = variances.reshape(2, 2)
    numerical_floor = (8 * np.finfo(float).eps) ** 2
    if (not np.isfinite(variances).all() or np.any(variances <= 0)
            or np.any(paired[:, 1] <= numerical_floor * paired[:, 0])):
        return dict(status='unavailable_response_variance',
                    transformed_variances=variances.tolist(),
                    numerical_difference_variance_floor=numerical_floor)
    return dict(status='computed', transformed_means=means.ravel().tolist(),
                transformed_variances=variances.tolist())


def fit_transformed_projection(pilot_rows, rows, target, successes, sizes, penalties,
                               *, chunk_size=4096, declarations=None,
                               response_error=.025, audit_error=.025):
    counts, totals = _validate(pilot_rows, rows, target, successes, sizes, penalties,
                               chunk_size, declarations, response_error, audit_error)
    result = transformed_scores(pilot_rows, rows, target, penalties, chunk_size)
    if result['status'] != 'computed':
        return result
    mean = np.asarray(result['transformed_means']).reshape(2, 2)
    se = np.sqrt(np.asarray(result['transformed_variances']).reshape(2, 2))
    z = norm.ppf(1 - response_error / 8)
    bands = np.stack((mean - z * se, mean + z * se), axis=-1)
    audits = [audit_interval(int(k), int(n), audit_error / 2) for k, n in zip(counts, totals)]
    parts = [sum_difference_projection(bands[s, 0], bands[s, 1], audits[s]) for s in (0, 1)]
    final = weighted_sum(parts, [.5, .5], -target.direct_cost())
    return dict(result, status='computed_set' if final else 'empty_projection',
                financial_set=encode_set(final), stratum_sets=[encode_set(x) for x in parts],
                transformed_bands=bands.tolist(), audit_intervals=audits,
                response_error=response_error, audit_error=audit_error,
                scope='Four average/difference normal score bands and two exact binomial audit intervals; pointwise asymptotic under declared law, no finite-sample or bank guarantee.')
