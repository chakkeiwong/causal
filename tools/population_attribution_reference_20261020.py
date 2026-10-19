#!/usr/bin/env python3
"""Exact authored witnesses; no LLM, downloaded engine, or bank data runs."""
from fractions import Fraction as F
from itertools import product
import json


def calculate():
    cells = {(x, u): F(1, 4) for x, u in product([-1, 1], repeat=2)}
    mean = lambda fn: sum(p * fn(x, u) for (x, u), p in cells.items())
    y = lambda x, u: 2*x+u
    reverse_slope = mean(lambda x, u: x*y(x, u))/mean(lambda x, u: y(x, u)**2)
    r = lambda x, u: x-reverse_slope*y(x, u)
    forward_cov = mean(lambda x, u: x*u)
    reverse_cov = mean(lambda x, u: y(x, u)*r(x, u))
    square_cov = mean(lambda x, u: y(x, u)**2*r(x, u)**2) - mean(lambda x, u: y(x, u)**2)*mean(lambda x, u: r(x, u)**2)
    assert reverse_slope == F(2, 5) and forward_cov == reverse_cov == 0
    assert square_cov == F(-16, 25)
    a11, a10, a01, a00 = F(9, 10), F(3, 5), F(2, 5), F(3, 10)
    cak, cad, mak, mad = a11-a01, a11-a10, a10-a00, a01-a00
    interaction = a11-a10-a01+a00
    assert mad-mak == cad-cak and cak+mad == cad+mak == a11-a00
    assert cak+cad-(a11-a00) == interaction == F(1, 5)
    p, q, draws = F(1, 2), F(3, 5), 10000
    bias_squared = (q-p)**2
    mc_variance = q*(1-q)/draws
    payoff, cost = F(100), F(55)
    return {
        'residuals': {'reverse_slope': str(reverse_slope), 'forward_covariance': str(forward_cov),
                      'reverse_covariance': str(reverse_cov), 'reverse_squared_covariance': str(square_cov)},
        'factorial': {'a11': str(a11), 'a10': str(a10), 'a01': str(a01), 'a00': str(a00),
                     'CAK': str(cak), 'CAD': str(cad), 'MAK': str(mak), 'MAD': str(mad),
                     'interaction': str(interaction), 'total_gain': str(a11-a00),
                     'conditional_sum': str(cak+cad)},
        'simulation': {'true_probability': str(p), 'model_probability': str(q), 'draws': draws,
                       'bias_squared': str(bias_squared), 'monte_carlo_variance': str(mc_variance),
                       'mse': str(bias_squared+mc_variance), 'predicted_margin_usd': str(payoff*q-cost),
                       'true_margin_usd': str(payoff*p-cost)},
        'repeated_prompts': {'datasets': 9, 'permutations_per_dataset': 15, 'calls': 135,
                            'effective_n_if_perfect_within_dataset_correlation': 9},
        'limitations': ['Finite authored examples with stipulated probabilities and dollar units.',
                       'No native discovery engine, LLM, model weights, bank experiment, or empirical performance estimate.',
                       'The residual witness diagnoses a correlation-only rule; it does not establish that any implementation uses that rule.',
                       'Perfect within-dataset dependence is an illustrative extreme, not an estimated property of the paper.']}


if __name__ == '__main__':
    print(json.dumps(calculate(), indent=2))
