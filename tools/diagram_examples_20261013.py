#!/usr/bin/env python3
"""Exact stipulated banking examples; no samples, model calls or bank data."""
from fractions import Fraction as F
from itertools import product
import json


def bernoulli(value, probability):
    return probability if value else 1 - probability


def standardize(table, treatment, outcome, controls):
    levels = sorted({tuple(row[k] for k in controls) for row, _ in table})
    means = []
    for action in (0, 1):
        total = F(0)
        for level in levels:
            stratum = [(r, p) for r, p in table
                       if tuple(r[k] for k in controls) == level]
            mass = sum(p for _, p in stratum)
            selected = [(r, p) for r, p in stratum if r[treatment] == action]
            support = sum(p for _, p in selected)
            assert support > 0
            total += mass * sum(r[outcome] * p for r, p in selected) / support
        means.append(total)
    return means[1] - means[0]


def proxy_example():
    error = F(1, 5)
    table = []
    for u, a, z, y in product((0, 1), repeat=4):
        pa = F(1, 5) + F(3, 5) * u
        py = F(1, 10) + F(1, 5) * a + F(1, 2) * u
        pz = error + (1 - 2 * error) * u
        p = F(1, 2) * bernoulli(a, pa) * bernoulli(z, pz) * bernoulli(y, py)
        table.append((dict(U=u, A=a, Z=z, Y=y), p))
    assert sum(p for _, p in table) == 1
    assert all(p > 0 for _, p in table)
    latent_adjusted = standardize(table, 'A', 'Y', ['U'])
    proxy_adjusted = standardize(table, 'A', 'Y', ['Z'])
    naive = standardize(table, 'A', 'Y', [])
    # Mechanism intervention overwrites A and averages over the unchanged U law.
    do_means = [sum(F(1, 2) * (F(1, 10) + F(1, 5) * a + F(1, 2) * u)
                    for u in (0, 1)) for a in (0, 1)]
    assert latent_adjusted == do_means[1] - do_means[0] == F(1, 5)
    assert proxy_adjusted == F(143, 340) and naive == F(1, 2)
    recovered = []
    for a, y in product((0, 1), repeat=2):
        observed = [sum(p for r, p in table if r['A'] == a and r['Y'] == y and r['Z'] == z)
                    for z in (0, 1)]
        for u in (0, 1):
            inferred = ((1 - error) * observed[u] - error * observed[1 - u]) / (1 - 2 * error)
            truth = sum(p for r, p in table if r['A'] == a and r['Y'] == y and r['U'] == u)
            assert inferred == truth
            recovered.append((dict(U=u, A=a, Y=y), inferred))
    assert standardize(recovered, 'A', 'Y', ['U']) == F(1, 5)
    return {'true_effect': F(1, 5), 'observed_difference': naive,
            'proxy_adjusted': proxy_adjusted, 'residual_bias': proxy_adjusted - F(1, 5),
            'known_error_inverse_effect': standardize(recovered, 'A', 'Y', ['U']),
            'inverse_l1_amplification': 1 / (1 - 2 * error),
            'all_joint_cells_positive': True, 'support_cells': len(table)}


def collider_example():
    table = []
    for a, u, m in product((0, 1), repeat=3):
        pm = F(1, 10) + F(2, 5) * a + F(2, 5) * u
        table.append((dict(A=a, U=u, M=m, Y=u), F(1, 4) * bernoulli(m, pm)))
    assert sum(p for _, p in table) == 1 and all(p > 0 for _, p in table)
    naive = standardize(table, 'A', 'Y', [])
    adjusted = standardize(table, 'A', 'Y', ['M'])
    assert naive == 0 and adjusted == F(-4, 21)
    return {'true_effect': F(0), 'observed_difference': naive,
            'post_action_adjusted': adjusted, 'all_observed_joint_cells_positive': True,
            'observed_support_cells': len(table)}


def decision_example():
    values = [1000 * x - 50 for x in (F(1, 50), F(2, 25))]
    assert values == [-30, 30]
    scenarios = []
    for high_probability in (F(1, 2), F(4, 5)):
        adopt_value = (1 - high_probability) * values[0] + high_probability * values[1]
        current_value = max(F(0), adopt_value)
        perfect_value = sum(w * max(F(0), v) for w, v in
                            zip((1 - high_probability, high_probability), values))
        scenarios.append({'assumed_probability_high_model': high_probability,
                          'adopt_expected_net_usd': adopt_value,
                          'current_optimal_value_usd': current_value,
                          'perfect_information_value_usd': perfect_value,
                          'evpi_per_account_usd': perfect_value - current_value,
                          'evpi_10000_accounts_usd': 10000 * (perfect_value - current_value)})
    return {'model_net_values_usd': values, 'max_regret_adopt_usd': 30,
            'max_regret_decline_usd': 30, 'planning_scenarios': scenarios}


def main():
    n, correlation = 10, F(9, 10)
    effective = n / (1 + (n - 1) * correlation)
    assert effective == F(100, 91)
    print(json.dumps({'kind': 'stipulated_exact_project_examples', 'random_draws': 0,
                      'live_model_calls': 0, 'bank_data': False,
                      'proxy': proxy_example(), 'collider': collider_example(),
                      'decision': decision_example(),
                      'correlated_answers': {'n': n, 'assumed_pair_correlation': correlation,
                                             'variance_equivalent_independent_count': effective}},
                     indent=2, default=str))


if __name__ == '__main__':
    main()
