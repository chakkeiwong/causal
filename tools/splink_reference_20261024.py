#!/usr/bin/env python3
"""Authored finite linkage witnesses; never imports or executes Splink."""
from fractions import Fraction as F
from itertools import permutations
import json


def posterior(prior, likelihood_ratio):
    odds = prior / (1 - prior) * likelihood_ratio
    return odds / (1 + odds)


def components(nodes, edges, threshold):
    parent = {n: n for n in nodes}
    def find(n):
        while parent[n] != n:
            n = parent[n]
        return n
    for a, b, score in edges:
        if score >= threshold:
            a, b = find(a), find(b)
            parent[max(a, b)] = min(a, b)
    return sorted(sorted(n for n in nodes if find(n) == p)
                  for p in sorted({find(n) for n in nodes}))


def calculate():
    p1 = posterior(F(1, 100), 100)
    p2 = posterior(F(1, 1000), 100)
    correlated_true = posterior(F(1, 100), 10)
    correlated_double = posterior(F(1, 100), 100)
    assert (p1, p2) == (F(100, 199), F(100, 1099))
    assert correlated_true == F(10, 109)
    prior_recall_half = F(40) / F(1, 2) / 10000
    prior_recall_four_fifths = F(40) / F(4, 5) / 10000
    assert (prior_recall_half, prior_recall_four_fifths) == (F(1, 125), F(1, 200))
    nodes = ['A', 'B', 'C']
    edges = [('A', 'B', F(96, 100)), ('B', 'C', F(96, 100)), ('A', 'C', F(1, 10))]
    outcomes = [components(nodes, es, F(95, 100)) for es in permutations(edges)]
    assert all(x == [['A', 'B', 'C']] for x in outcomes)
    joint_lower_bound = F(96, 100) * 2 - 1
    assert joint_lower_bound == F(23, 25) and F(1, 10) < joint_lower_bound
    candidate_recall, full_recall, precision = F(54, 60), F(54, 100), F(54, 60)
    assert (candidate_recall, full_recall, precision) == (F(9, 10), F(27, 50), F(9, 10))
    true_arm_means = [F(100 + 0, 2), F(100 + 0, 2)]
    selected_arm_means = [F(100), F(0)]
    assert true_arm_means[0] - true_arm_means[1] == 0
    assert selected_arm_means[0] - selected_arm_means[1] == 100
    values, weights = [F(20), F(-20)], [F(3, 4), F(1, 4)]
    mean = sum(p * x for p, x in zip(weights, values))
    between = sum(p * (x - mean)**2 for p, x in zip(weights, values))
    total = F(4) + between
    assert (mean, between, total) == (10, 300, 304)
    mutual_best_sum = F(9, 10) + F(1, 10)
    alternate_sum = F(8, 10) + F(85, 100)
    assert (mutual_best_sum, alternate_sum) == (1, F(33, 20))
    parameter_changes = [F(1, 10), F(1, 20), F(1, 25)]
    tolerance = F(1, 100)
    assert not any(x < tolerance for x in parameter_changes)
    costs = dict(compute=F(40), annotation=F(160), engineering=F(200), storage_review=F(80))
    cost = sum(costs.values())
    assert (cost, cost / 6, cost / 4, cost / 3) == (480, 80, 120, 160)
    return {
        'scope': 'Exact authored examples; no Splink runtime, empirical probability calibration, causal identification or bank price claim.',
        'posterior_prior_sensitivity': {'prior_001': str(p1), 'prior_0001': str(p2)},
        'duplicated_correlated_field': {'one_information_source': str(correlated_true), 'incorrect_independence': str(correlated_double)},
        'recall_assumption_prior': {'recall_half': str(prior_recall_half), 'recall_four_fifths': str(prior_recall_four_fifths)},
        'blocking': {'candidate_recall': str(candidate_recall), 'full_recall': str(full_recall), 'precision': str(precision)},
        'graph': {'components': outcomes[0], 'event_orders': len(outcomes), 'joint_AC_lower_bound': str(joint_lower_bound), 'incoherent_AC_score': '1/10'},
        'selection': {'complete_contrast_usd': 0, 'selected_contrast_usd': 100},
        'joint_map_mixture': {'mean_usd': str(mean), 'between_variance_usd_squared': str(between), 'within_variance_usd_squared': '4', 'total_variance_usd_squared': str(total)},
        'matching_objectives': {'local_mutual_sum': str(mutual_best_sum), 'alternative_sum': str(alternate_sum)},
        'iteration_cap': {'changes': list(map(str, parameter_changes)), 'tolerance': str(tolerance), 'criterion_met': False},
        'stipulated_cost_usd': {'components': {k: str(v) for k, v in costs.items()}, 'total': str(cost), 'per_attempt': str(cost / 6), 'per_request': str(cost / 4), 'per_accepted': str(cost / 3)},
    }


if __name__ == '__main__':
    print(json.dumps(calculate(), indent=2))
