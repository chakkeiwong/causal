"""Projection inference for a calibrated two-candidate assignment model.

Binomial calibration is exact up to numerical inversion. Observable response
bands inherit their supplied normal/HAC approximation. Projection imposes no
lower bound on abs(2*p - 1) and retains disconnected and unbounded sets.
"""
from functools import lru_cache
import math
from statistics import NormalDist

import numpy as np
from .dynamic_validation import validate_target


@lru_cache(maxsize=4096)
def binomial_interval(successes, size, error):
    """Equal-tail inversion; zero observations convey no information."""
    if (not isinstance(size, (int, np.integer)) or size < 0
            or not isinstance(successes, (int, np.integer))
            or not 0 <= successes <= size or not 0 < error < 1):
        raise ValueError('invalid binomial count or error probability')
    if size == 0:
        return (0.0, 1.0)
    j = np.arange(size + 1)
    log_choose = np.array([math.lgamma(size + 1) - math.lgamma(int(k) + 1)
                           - math.lgamma(size - int(k) + 1) for k in j])

    def tail(p, upper):
        if p == 0:
            return float(successes == 0) if upper else 1.0
        if p == 1:
            return 1.0 if upper else float(successes == size)
        mass = np.exp(log_choose + j * math.log(p)
                      + (size - j) * math.log1p(-p))
        return math.fsum(mass[successes:] if upper else mass[:successes + 1])

    def invert(upper):
        lo, hi = 0.0, 1.0
        for _ in range(64):
            mid = (lo + hi) / 2
            below = tail(mid, upper) < error / 2
            if below == upper:
                lo = mid
            else:
                hi = mid
        # Round outwards, retaining the confidence region at numerical roots.
        return lo if upper else hi

    return (0.0 if successes == 0 else invert(True),
            1.0 if successes == size else invert(False))


def merge_intervals(intervals):
    """Closed extended-real intervals; no convexification of disjoint pieces."""
    result = []
    for lo, hi in sorted(intervals):
        if math.isnan(lo) or math.isnan(hi) or lo > hi:
            raise ValueError('invalid interval endpoint')
        if result and lo <= result[-1][1]:
            result[-1] = (result[-1][0], max(result[-1][1], hi))
        else:
            result.append((float(lo), float(hi)))
    return result


def pair_projection(first, second, probability):
    """Exact scalar image of two mean bands and a probability interval.

    The companion portfolio effect is unrestricted. At p=1/2, compatible
    observed means identify only its sum with the requested effect.
    """
    a, b = map(float, first)
    c, d = map(float, second)
    lo, hi = map(float, probability)
    if not all(math.isfinite(x) for x in (a, b, c, d, lo, hi)):
        raise ValueError('primitive bands must have finite endpoints')
    if a > b or c > d or not 0 <= lo <= hi <= 1:
        raise ValueError('invalid primitive confidence band')
    if lo <= .5 <= hi and max(a, c) <= min(b, d):
        return [(-math.inf, math.inf)]

    def value(p, x, y, side):
        if p != .5:
            return (p * x - (1 - p) * y) / (2 * p - 1)
        if x == y:
            return x
        return math.copysign(math.inf, (x - y) * side)

    pieces = []
    if lo < .5:
        end = min(hi, .5)
        lower = [value(p, b, c, -1) for p in (lo, end)]
        upper = [value(p, a, d, -1) for p in (lo, end)]
        pieces.append((min(lower), max(upper)))
    if hi > .5:
        start = max(lo, .5)
        lower = [value(p, a, d, 1) for p in (start, hi)]
        upper = [value(p, b, c, 1) for p in (start, hi)]
        pieces.append((min(lower), max(upper)))
    return merge_intervals(pieces)


def weighted_sum(sets, weights, offset=0.0):
    weights = np.asarray(weights, dtype=float)
    if len(weights) != len(sets) or not np.all(np.isfinite(weights)):
        raise ValueError('invalid fixed financial weights')
    result = [(float(offset), float(offset))]
    for pieces, weight in zip(sets, weights):
        if not pieces:
            return []
        if weight == 0:
            continue
        scaled = [(weight * lo, weight * hi) if weight > 0
                  else (weight * hi, weight * lo) for lo, hi in pieces]
        result = merge_intervals([(a + c, b + d) for a, b in result
                                  for c, d in scaled])
    return result


def sum_difference_projection(average, difference, probability):
    """Image of average + difference/(2p-1), preserving the rank-one case."""
    a, b = map(float, average)
    c, d = map(float, difference)
    p, q = map(float, probability)
    if (not all(math.isfinite(x) for x in (a, b, c, d, p, q))
            or a > b or c > d or not 0 <= p <= q <= 1):
        raise ValueError('invalid transformed confidence band')
    lo, hi = 2*p-1, 2*q-1
    if lo <= 0 <= hi and c <= 0 <= d:
        return [(-math.inf, math.inf)]

    def quotient(x, r, sign):
        if r:
            return x/r
        return 0.0 if x == 0 else math.copysign(math.inf, x*sign)

    pieces = []
    for left, right, sign in [(lo, min(hi, 0), -1), (max(lo, 0), hi, 1)]:
        if (sign < 0 and lo >= 0) or (sign > 0 and hi <= 0):
            continue
        corners = [quotient(x, r, sign) for x in (c, d) for r in (left, right)]
        pieces.append((a+min(corners), b+max(corners)))
    return merge_intervals(pieces)


def encode_set(intervals):
    """JSON-compatible infinities, without NaN or nonstandard Infinity tokens."""
    return [{'lower': None if lo == -math.inf else lo,
             'upper': None if hi == math.inf else hi} for lo, hi in intervals]


def decode_set(intervals):
    return [(-math.inf if row['lower'] is None else row['lower'],
             math.inf if row['upper'] is None else row['upper']) for row in intervals]


def project_funding(eta, covariance, successes, sizes, target, alpha=.05):
    """Fixed financial contrast, equal stratum weights, fixed 50/50 error split."""
    validate_target(target)
    eta = np.asarray(eta, dtype=float)
    covariance = np.asarray(covariance, dtype=float)
    successes, sizes = np.asarray(successes), np.asarray(sizes)
    d = target.horizon + 1
    if (eta.shape != (2, 2 * d) or covariance.shape != (4 * d, 4 * d)
            or not np.all(np.isfinite(eta)) or not np.all(np.isfinite(covariance))
            or not np.isfinite(alpha) or not 0 < alpha < 1):
        raise ValueError('invalid observable response summary or confidence level')
    if (successes.shape != (2,) or sizes.shape != (2,)
            or not np.all(np.isfinite(successes)) or not np.all(np.isfinite(sizes))
            or np.any(sizes < 0) or np.any(successes < 0)
            or np.any(successes > sizes) or np.any(sizes != np.floor(sizes))
            or np.any(successes != np.floor(successes))):
        raise ValueError('invalid audit counts')
    if not np.allclose(covariance, covariance.T, rtol=1e-10, atol=1e-12):
        raise ValueError('observable covariance is not symmetric')
    scale = max(1.0, float(np.max(np.abs(covariance))))
    if np.linalg.eigvalsh(covariance).min() < -1e-10 * scale:
        raise ValueError('observable covariance is not positive semidefinite')
    # No inverse map is used to construct these four primitive bands.
    reduction = np.kron(np.eye(4), target.weights()[None, :])
    means = reduction @ eta.ravel()
    vcov = reduction @ covariance @ reduction.T
    deviations = np.sqrt(np.maximum(np.diag(vcov), 0))
    z = NormalDist().inv_cdf(1 - alpha / 16)  # four bands, alpha/2 total
    candidate_bands = np.column_stack((means - z * deviations, means + z * deviations))
    transform = np.kron(np.eye(2), np.array([[.5, .5], [.5, -.5]]))
    transformed_mean = transform @ means
    transformed_covariance = transform @ vcov @ transform.T
    if (not np.all(np.isfinite(transformed_mean)) or not np.all(np.isfinite(transformed_covariance))
            or np.any(np.diag(transformed_covariance) <= 0)):
        raise ValueError('normal response bands require finite positive contrast variances')
    transformed_se = np.sqrt(np.maximum(np.diag(transformed_covariance), 0))
    bands = np.column_stack((transformed_mean-z*transformed_se, transformed_mean+z*transformed_se))
    audit_bands = [binomial_interval(int(k), int(n), alpha / 4)
                   for k, n in zip(successes, sizes)]
    stratum_sets = [sum_difference_projection(bands[2*s], bands[2*s+1], audit_bands[s])
                    for s in (0, 1)]
    challenger_sets = [pair_projection(candidate_bands[2*s], candidate_bands[2*s+1], audit_bands[s])
                       for s in (0, 1)]
    financial = weighted_sum(stratum_sets, [.5, .5], -target.direct_cost())
    return {'status': 'computed_set', 'financial_set': encode_set(financial),
            'confidence_level': 1 - alpha, 'error_allocation': {'observable': alpha/2, 'audit': alpha/2},
            'candidate_financial_means': means, 'candidate_financial_covariance': vcov,
            'candidate_bands': candidate_bands, 'audit_intervals': audit_bands,
            'transformed_means': transformed_mean, 'transformed_covariance': transformed_covariance,
            'transformed_bands': bands, 'coordinates': 'average_and_half_difference',
            'candidate_box_challenger': encode_set(weighted_sum(challenger_sets, [.5, .5], -target.direct_cost())),
            'stratum_sets': [encode_set(x) for x in stratum_sets],
            'scope': 'Projection of simultaneous normal/HAC observable bands and exact binomial audit intervals; finite-sample audit coverage, asymptotic response coverage; no lower bound on linkage rank'}
