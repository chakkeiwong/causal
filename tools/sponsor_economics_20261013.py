#!/usr/bin/env python3
"""Exact planning arithmetic; assumed inputs, no bank ROI or vendor prices."""
from fractions import Fraction as F
import json

from proposal_economics_example import calculate as inherited


def calculate():
    previous = inherited()
    priors = [F(2, 5), F(2, 5), F(1, 5)]
    gains = [40, 20, -2]
    likelihoods = [F(4, 5), F(1, 2), F(1, 10)]
    payoffs = [10000 * (gain - 6) - 100000 for gain in gains]
    prior_value = sum(p * v for p, v in zip(priors, payoffs))
    branches = []
    for positive in (True, False):
        weights = [p * (q if positive else 1 - q)
                   for p, q in zip(priors, likelihoods)]
        mass = sum(weights)
        posterior_value = sum(w * v for w, v in zip(weights, payoffs)) / mass
        branches.append({'positive': positive, 'probability': str(mass),
                         'posterior_value': str(posterior_value),
                         'build': posterior_value > 0})
    informed = sum(F(b['probability']) * max(F(0), F(b['posterior_value']))
                   for b in branches)
    evsi = informed - max(0, prior_value)
    evpi = sum(p * max(0, v) for p, v in zip(priors, payoffs)) - max(0, prior_value)
    expected = [prior_value, evsi, evpi]
    old = [previous[k] for k in ['expected_incremental_value_without_experiment',
                                'expected_value_of_sample_information',
                                'expected_value_of_perfect_information']]
    assert all(abs(float(a) - b) < 1e-8 for a, b in zip(expected, old))
    sensitivity = []
    for count, review in [(5000, 0), (10000, 0), (20000, 0), (10000, 4)]:
        threshold = F(6 + review) + F(100000, count)
        assert count * (threshold - 6 - review) - 100000 == 0
        sensitivity.append({'attempted_tasks': count, 'extra_review_per_task': review,
                            'break_even_gross_gain_per_task': str(threshold)})
    return {'kind': 'exact_project_planning_arithmetic_with_assumed_inputs',
            'currency': 'illustrative USD', 'horizon': 'one year, no discounting',
            'new_random_draws': 0, 'empirical_prices_or_benefits': False,
            'matches_preserved_economics_example': True,
            'net_values': payoffs, 'prior_expected_value': str(prior_value),
            'signal_branches': branches, 'informed_value_before_experiment_cost': str(informed),
            'EVSI': str(evsi), 'EVPI': str(evpi),
            'net_information_value_at_8000': str(evsi - 8000),
            'net_information_value_at_3000': str(evsi - 3000),
            'sensitivities': sensitivity,
            'limits': ['All gains, prices, task counts, priors and signal likelihoods are assumed.',
                       'No real investment recommendation follows from assumed positive expected value.',
                       'Unacceptable actions remain hard constraints.']}


if __name__ == '__main__':
    print(json.dumps(calculate(), indent=2))
