#!/usr/bin/env python3
"""Exact authored discovery examples; no samples, external engine or live model."""
from fractions import Fraction as F
from itertools import product
from math import comb
import json


def inverse(a):
    n = len(a)
    rows = [[F(v) for v in row] + [F(i == j) for j in range(n)]
            for i, row in enumerate(a)]
    for j in range(n):
        pivot = next(i for i in range(j, n) if rows[i][j])
        rows[j], rows[pivot] = rows[pivot], rows[j]
        scale = rows[j][j]
        rows[j] = [x / scale for x in rows[j]]
        for i in range(n):
            if i != j:
                scale = rows[i][j]
                rows[i] = [x - scale * y for x, y in zip(rows[i], rows[j])]
    return [r[n:] for r in rows]


def conditional_covariance(cov, i, j, given):
    if not given:
        return F(cov[i][j])
    inv = inverse([[cov[a][b] for b in given] for a in given])
    return F(cov[i][j]) - sum(F(cov[i][a]) * inv[k][l] * F(cov[b][j])
                            for k, a in enumerate(given) for l, b in enumerate(given))


def covariance(loadings, variances):
    return [[sum(F(a) * F(b) * F(v) for a, b, v in zip(x, y, variances))
             for y in loadings] for x in loadings]


def calculate():
    # Triangle: A=eA, M=A+eM, Y=-A+M+eY. Collider: M=A+Y/2+eta.
    triangle = covariance([[1, 0, 0], [1, 1, 0], [0, 1, 1]], [1, 1, 1])
    collider = covariance([[1, 0, 0], [1, F(1, 2), 1], [0, 1, 0]], [1, 2, F(1, 2)])
    assert triangle == collider == [[1, 1, 0], [1, 2, 1], [0, 1, 2]]
    assert conditional_covariance(triangle, 0, 2, [1]) == F(-1, 2)
    near = []
    for delta in [F(-1, 10), F(0), F(1, 10)]:
        cov = covariance([[1, 0, 0], [1, 1, 0], [delta, 1, 1]], [1, 1, 1])
        assert cov[0][2] == delta
        assert conditional_covariance(cov, 0, 2, [1]) == (delta - 1) / 2
        near.append({'delta': delta, 'marginal_A_Y': cov[0][2],
                     'conditional_A_Y_given_M': (delta - 1) / 2})
    # Two parallel mediators: ordering A,M1,M2,Y.
    parallel = covariance([[1, 0, 0, 0], [1, 1, 0, 0], [1, 0, 1, 0], [2, 1, 1, 1]], [1] * 4)
    seps = [{'given': s, 'covariance': conditional_covariance(parallel, 0, 3, s)}
            for s in [[], [1], [2], [1, 2]]]
    assert [r['covariance'] for r in seps] == [2, F(1, 2), F(1, 2), 0]
    # Common-cause and direct models agree in every mean-shift environment.
    confounded = covariance([[1, 1, 0], [1, 0, 1]], [1, 1, F(1, 2)])
    direct = covariance([[1, 0], [F(1, 2), 1]], [2, 1])
    assert confounded == direct == [[2, 1], [1, F(3, 2)]]
    env = []
    for mean in [F(-2), F(0), F(3)]:
        a_mean, y_mean = mean, mean / 2
        assert y_mean - confounded[0][1] / confounded[0][0] * a_mean == 0
        assert conditional_covariance(confounded, 1, 1, [0]) == 1
        env.append({'mean_A': a_mean, 'mean_Y': y_mean, 'conditional_intercept': F(0),
                    'conditional_slope': F(1, 2), 'conditional_variance': F(1)})
    # Exact binomial integration for an intervention-only information experiment.
    q, p_high, p_low = F(1, 2), F(9, 10), F(1, 2)
    evsi = []
    for n in [0, 1, 2, 5, 10, 20, 50]:
        rows = []
        value = F(0)
        for k in range(n + 1):
            high = F(comb(n, k)) * p_high**k * (1 - p_high)**(n - k)
            low = F(comb(n, k)) * p_low**k * (1 - p_low)**(n - k)
            mass = q * high + (1 - q) * low
            posterior = q * high / mass
            gain = 5 * q * high - 3 * (1 - q) * low
            offer = posterior > F(3, 8)
            assert offer == (gain > 0)
            value += max(F(0), gain)
            rows.append({'successes': k, 'mass': mass, 'posterior_high': posterior, 'offer': offer})
        assert sum(r['mass'] for r in rows) == 1
        assert F(0) <= value - 1 <= F(3, 2)
        evsi.append({'n': n, 'expected_value': value, 'EVSI': value - 1,
                     'EVSI_decimal': float(value - 1), 'offer_counts': [r['successes'] for r in rows if r['offer']],
                     'outcomes': rows})
    assert [r['EVSI'] for r in evsi[:3]] == [F(0), F(1, 2), F(13, 20)]
    assert all(a['EVSI'] <= b['EVSI'] for a, b in zip(evsi, evsi[1:]))
    # Three individually interpretable restrictions with an empty joint intersection.
    restrictions = []
    for a, b in product([0, 1], repeat=2):
        truths = [bool(a), bool(b), bool(a ^ b)]
        failures = sum(not v for v in truths)
        restrictions.append({'model': f'{a}{b}', 'satisfied': truths, 'failures': failures,
                             'retained_k0': failures <= 0, 'retained_k1': failures <= 1})
    assert not any(r['retained_k0'] for r in restrictions)
    assert [r['model'] for r in restrictions if r['retained_k1']] == ['01', '10', '11']
    return {'kind': 'exact_project_derivations', 'random_draws': 0, 'external_engine_runs': 0,
            'live_model_calls': 0,
            'faithfulness': {'covariance': triangle, 'A_Y_given_M': F(-1, 2),
                             'effect_M_on_Y_triangle': 1, 'effect_M_on_Y_collider': 0, 'near_cancellation': near},
            'search_depth': {'covariance': parallel, 'separator_results': seps, 'effect_A_on_Y': 2},
            'environments': {'covariance': confounded, 'rows': env, 'effects': [0, F(1, 2)]},
            'finite_information': {'prior_high': q, 'high_success': p_high, 'low_success': p_low,
                                   'baseline_value': 1, 'EVPI': F(3, 2), 'rows': evsi,
                                   'scope': 'Stipulated two-world law; exhaustive sums, not a performed trial.'},
            'restriction_error': {'models': restrictions, 'three_error_bounds': [F(1, 20)] * 3,
                                  'k0_bound': F(3, 20), 'k1_bound': F(3, 40),
                                  'scope': 'Conditional on genuine marginal error bounds; no LLM error calibration supplied.'}}


def serializable(obj):
    if isinstance(obj, F):
        return str(obj)
    if isinstance(obj, dict):
        return {k: serializable(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [serializable(v) for v in obj]
    return obj


if __name__ == '__main__':
    print(json.dumps(serializable(calculate()), indent=2))
