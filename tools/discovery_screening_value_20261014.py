#!/usr/bin/env python3
"""Exact finite decision arithmetic and analytic Gaussian-moment reference."""
from fractions import Fraction as F
import json
import math
from discovery_design_oracles_20261014 import serializable


def entropy(p):
    p = float(p)
    return -p * math.log2(p) - (1 - p) * math.log2(1 - p)


def calculate():
    q = F(1, 10)
    rows = []
    for error in [F(1, 5), F(1, 20)]:
        outcomes = []
        value = F(0)
        for z in [0, 1]:
            ph = 1 - error if z else error
            pl = error if z else 1 - error
            mass = q * ph + (1 - q) * pl
            posterior = q * ph / mass
            gain = mass * max(F(0), 8 * posterior - 3)
            value += gain
            outcomes.append({'z': z, 'mass': mass, 'posterior_high': posterior, 'gain': gain})
        mi = entropy(outcomes[1]['mass']) - entropy(error)
        rows.append({'error': error, 'outcomes': outcomes, 'decision_value': value, 'mutual_information_bits': mi})
    assert [r['decision_value'] for r in rows] == [0, F(17, 50)]
    assert [r['outcomes'][1]['posterior_high'] for r in rows] == [F(4, 13), F(19, 28)]
    assert [r['outcomes'][0]['posterior_high'] for r in rows] == [F(1, 37), F(1, 172)]
    assert rows[0]['mutual_information_bits'] > 0
    return serializable({'kind': 'exact_project_derivations_with_analytic_normal_moments',
        'random_draws': 0, 'external_engine_runs': 0, 'live_model_calls': 0,
        'nonlinear_screen': {'normal_moments_0_to_4': [1, 0, 1, 0, 3],
            'mean_Y': 0, 'variance_Y': 3, 'covariance_X_Y': 0, 'variance_H': 2, 'covariance_H_Y': 2,
            'spearman_argument': 'Sign symmetry of (X,Y) reverses Phi(X)-1/2 and preserves F_Y(Y)-1/2.',
            'effect_0_to_1': 1, 'effect_minus1_to_1': 0},
        'query_value': {'prior_high': q, 'offer_threshold': F(3, 8),
            'current_offer_value': 8*q-3, 'current_optimum': 0, 'perfect_R_value': F(1, 2),
            'perfect_R_bits': entropy(q), 'perfect_irrelevant_S_value': 0, 'perfect_irrelevant_S_bits': 1,
            'noisy_queries': rows, 'assumed_cost': F(1, 10), 'accurate_query_net': F(6, 25)},
        'scope': 'Stipulated likelihoods and utility, not a fitted model or performed experiment.'})


if __name__ == '__main__':
    print(json.dumps(calculate(), indent=2))
