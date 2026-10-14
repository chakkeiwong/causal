#!/usr/bin/env python3
"""Deterministic sample-size/cost illustrations, not a live study or registration."""
import argparse
from fractions import Fraction as F
import json
import math
from pathlib import Path

import numpy as np
import scipy
from scipy.stats import binom


def critical_successes(k, alpha):
    """Smallest b with Pr[Binomial(k,.5)>=b]<=alpha; k+1 means no rejection."""
    b = int(binom.isf(alpha, k, .5)) + 1
    while b <= k and binom.sf(b - 1, k, .5) > alpha:
        b += 1
    while b > 0 and binom.sf(b - 2, k, .5) <= alpha:
        b -= 1
    return b


def paired_power(n, p_plus, p_minus, alpha):
    q = p_plus + p_minus
    assert 0 < q <= 1 and 0 < alpha < 1
    k = np.arange(n + 1)
    critical = np.array([critical_successes(int(d), alpha) for d in k])
    sign_power = binom.sf(critical - 1, k, p_plus / q)
    return float(np.dot(binom.pmf(k, n, q), sign_power))


def small_exact_reference(n, p_plus, p_minus, alpha):
    result = F(0)
    for b in range(n + 1):
        for c in range(n - b + 1):
            k = b + c
            tail = sum(F(math.comb(k, j), 2**k) for j in range(b, k+1))
            if tail <= alpha:
                coefficient = math.comb(n, b) * math.comb(n-b, c)
                result += coefficient * p_plus**b * p_minus**c * (1-p_plus-p_minus)**(n-k)
    return result


def run():
    # Independent exact multinomial enumeration checks the conditional-binomial calculation.
    errors = []
    for n in [2, 6, 10, 12]:
        exact = small_exact_reference(n, F(1, 5), F(1, 10), F(1, 20))
        actual = paired_power(n, .2, .1, .05)
        error = abs(float(exact) - actual)
        assert error < 2e-14
        errors.append(error)
    alpha = .05 / 12
    grids = []
    for p_plus, p_minus in [(.15, .10), (.20, .10), (.25, .05)]:
        values = [{'n_per_family': n, 'power': paired_power(n, p_plus, p_minus, alpha)}
                  for n in [24, 48, 100, 200, 400, 800]]
        # Under the paired null, the exact rejection probability must remain below allocation.
        null = paired_power(100, (p_plus+p_minus)/2, (p_plus+p_minus)/2, alpha)
        assert null <= alpha + 1e-12
        grids.append({'p_plus': p_plus, 'p_minus': p_minus,
                      'difference': p_plus-p_minus, 'discordance_probability': p_plus+p_minus,
                      'alpha_per_test': alpha, 'powers': values,
                      'first_listed_n_reaching_80pct': next((v['n_per_family'] for v in values if v['power'] >= .8), None),
                      'null_rejection_probability_n100': null})
    error_bounds = []
    for k in [1, 6, 12]:
        allocated = .05/k
        n = math.ceil(math.log(allocated)/math.log1p(-.05))
        assert (1-.05)**n <= allocated and (1-.05)**(n-1) > allocated
        error_bounds.append({'simultaneous_bounds': k, 'alpha_per_bound': allocated,
            'zero_failure_n_for_upper_le_5pct': n,
            'upper_if_zero_in_24': -math.expm1(math.log(allocated)/24),
            'upper_if_zero_in_48': -math.expm1(math.log(allocated)/48),
            'upper_if_zero_in_100': -math.expm1(math.log(allocated)/100)})
    mechanisms_per_family, families, variants, live_arms, attempts, internal_calls = 100, 6, 2, 4, 3, 3
    calls = mechanisms_per_family*families*variants*live_arms*attempts*internal_calls
    assert calls == 43200
    return {'status': 'pass', 'scope': 'Illustrative planning calculations only; no final n, threshold, model, price, seed or study selected',
        'assumptions': ['Independent identically distributed mechanism draws within each family.',
            'One predeclared binary primary variant per mechanism for paired sign screen; variants are not independent units.',
            'Bonferroni allocation over12 illustrative claims (six improvement screens and six severe-error bounds).',
            'Hypothetical discordance/error rates and thresholds, not pilot estimates or bank requirements.'],
        'formula': 'Power=sum_k Bin(n,q)[k]*Pr(Bin(k,p_plus/q)>=critical(k)); critical uses Bin(k,1/2) upper tail.',
        'paired_power': grids, 'zero_error_bounds': error_bounds,
        'independent_exact_reference_max_error': max(errors),
        'cost_upper_scenario': {'independent_mechanisms_per_family': mechanisms_per_family, 'families': families,
            'total_independent_mechanisms': mechanisms_per_family*families, 'variants_per_mechanism': variants,
            'live_arms': live_arms, 'attempts_per_arm_variant': attempts, 'model_calls_per_attempt_cap': internal_calls,
            'max_model_calls': calls, 'input_tokens_per_call_cap': 2000, 'output_tokens_per_call_cap': 500,
            'max_input_tokens_million': calls*2000/1e6, 'max_output_tokens_million': calls*500/1e6,
            'model_cost_expression': '86.4*r_input+21.6*r_output, rates in currency per million tokens',
            'prices': None, 'budget_approved': False,
            'excluded_from_expression': ['cache price distinctions','retrieval','numerical compute','storage','reviewer time','rework'],
            'claim': 'Conservative planning envelope under stated caps, not expected spend or authorization.'},
        'environment': {'numpy': np.__version__, 'scipy': scipy.__version__},
        'final_sample_size': None, 'final_thresholds': None, 'live_calls': 0}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    result = run()
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': result['status'], 'zero_error_minimum_n': [v['zero_failure_n_for_upper_le_5pct'] for v in result['zero_error_bounds']],
                      'first_listed_80pct_n': [v['first_listed_n_reaching_80pct'] for v in result['paired_power']],
                      'live_calls': 0}))
