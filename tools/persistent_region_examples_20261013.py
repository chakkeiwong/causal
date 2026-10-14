#!/usr/bin/env python3
"""Deterministic references for the R02S information argument, without final draws."""
from fractions import Fraction as F
import json
from math import erf, sqrt
from pathlib import Path


def calendar_factor(t, rho):
    return (t + 2 * sum((t - k) * rho**k for k in range(1, t))) / t**2


def multiply(left, right):
    return [[sum(a*b for a, b in zip(row, col)) for col in zip(*right)] for row in left]


def calculate():
    # Direct covariance sum versus lag count, and exact inverse AR(1) information.
    references = []
    for t in (3, 5, 8):
        rho = F(3, 5)
        covariance = [[rho**abs(i-j) for j in range(t)] for i in range(t)]
        precision = [[F(0) for _ in range(t)] for _ in range(t)]
        for i in range(t):
            precision[i][i] = (1 if i in (0, t-1) else 1+rho*rho)/(1-rho*rho)
            if i < t-1:
                precision[i][i+1] = precision[i+1][i] = -rho/(1-rho*rho)
        assert multiply(covariance, precision) == [[F(i == j) for j in range(t)] for i in range(t)]
        direct = sum(map(sum, covariance))/t**2
        information = sum(map(sum, precision))
        assert direct == calendar_factor(t, rho)
        assert information == (t*(1-rho)+2*rho)/(1+rho)
        references.append({'dates': t, 'calendar_factor': str(direct), 'mean_information': str(information)})

    # Persistent audit multiplier before division by unknown r.
    q, e, d = F(2, 5), F(2, 25), F(7, 10)
    r = 1-2*e
    weights = [(F(0), 1-q), (1/q, q*(1-e)), (-1/q, q*e)]
    mean = sum(w*p for w, p in weights)
    second = sum(w*w*p for w, p in weights)
    assert mean == r and second == 1/q
    pair_variance, cell_variance, t, n = F(16, 25), F(1), 160, 100
    conditional = pair_variance/2+cell_variance/(2*t)
    direct_variance = sum(p*(w*w*conditional+(w*d-r*d)**2) for w, p in weights)/n
    formula = (conditional/q+(1/q-r*r)*d*d)/n
    assert direct_variance == formula

    finite = []
    for t in (40, 160, 320):
        k = calendar_factor(t, F(19, 20))
        finite.append({'dates': t, 'rho': .95, 'calendar_factor': float(k),
                       'calendar_mean_sd_at_sigma_point6': .6*sqrt(float(k)),
                       'unit_variance_mean_information': float((t*F(1,20)+F(19,10))/F(39,20))})
    tails = []
    alpha_m = F(1, 50)
    for n, q in ((100,F(2,5)), (32,F(2,5)), (320,F(2,5)), (100,F(1,10))):
        leading = r*r*(alpha_m+F(1,n))-1/(q*n)
        tails.append({'pairs': n, 'inclusion': float(q), 'rank': float(r),
                      'numerator_error_budget': float(alpha_m),
                      'quadratic_leading_coefficient': str(leading),
                      'bounded_set_possible_at_this_rank': leading > 0,
                      'strict_rank_squared_threshold': float(1/(q*(n*alpha_m+1)))})
    information_limit = []
    for t in (10,100,1000):
        rho = 1-F(1,t*t)
        information = (t*(1-rho)+2*rho)/(1+rho)
        # TV between equally covariant Gaussian laws with standardized shift 1.
        tv = erf(sqrt(float(information))/(2*sqrt(2)))
        information_limit.append({'dates':t,'rho':float(rho),'unit_variance_information':float(information),
                                  'total_variation_for_unit_shift':tv,
                                  'diameter_at_least_one_probability_lower_bound_at_95pct':.9-tv})
    return {'kind':'project_derivation_deterministic_references','random_draws':0,
            'final_study':False,'package_qualification':False,
            'matrix_references':references,
            'multiplier_reference':{'mean':str(mean),'second_moment':str(second),
                                    'numerator_variance':str(formula)},
            'persistent_calendar_references':finite,'chebyshev_projection_tail_examples':tails,
            'local_to_unity_information':information_limit,
            'limits':['Variance bounds are proposed inputs, not supplied by this arithmetic.',
                      'Unbounded Chebyshev regions are a property of this construction, not proof all methods fail.',
                      'The local-to-unity lower bound concerns an unrestricted persistence sequence; the fixed-rho asymptotic claim is separate.']}


if __name__ == '__main__':
    out = Path(__file__).resolve().parents[1] / 'docs/program/execution/2026-10-13/research/persistent-region-examples.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    value = calculate()
    out.write_text(json.dumps(value, indent=2) + '\n')
    print(json.dumps({'exact_references':'pass','random_draws':0,'tail_examples':value['chebyshev_projection_tail_examples']}))
