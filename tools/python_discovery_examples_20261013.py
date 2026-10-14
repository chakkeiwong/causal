#!/usr/bin/env python3
"""Exact project examples; no sampled study and no downloaded engine execution."""
import hashlib
import json
import math
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/program/execution/2026-10-13/python-discovery/oracle-results.json'


def transpose(a):
    return [list(x) for x in zip(*a)]


def multiply(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def add(a, b):
    return [[x+y for x, y in zip(r, s)] for r, s in zip(a, b)]


def identity(n):
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def total(a):
    # For these declared DAGs A**d=0: I+A+...+A**(d-1)=(I-A)**(-1).
    n = len(a)
    power = identity(n)
    ans = power
    for _ in range(1, n):
        power = multiply(power, a)
        ans = add(ans, power)
    assert multiply(power, a) == [[0]*n for _ in range(n)]
    return ans


def encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, list):
        return [encode(x) for x in value]
    if isinstance(value, dict):
        return {k: encode(v) for k, v in value.items()}
    return value


def calculate():
    w = [[F(0), F(4), F(-1)], [F(0), F(0), F(1, 2)], [F(0), F(0), F(0)]]
    tw = total(w)
    wrong = total(transpose(w))
    assert tw[0][2] == 1 and wrong[0][2] == 0 and wrong[2][0] == 1
    funding = {'variables': ['rate_percentage_points', 'retained_USD_million', 'margin_USD_million'],
               'row_source_W': w, 'target_row_B': transpose(w), 'total_row_source': tw,
               'intervention_pp': F(1, 4), 'retained_change_USD_million': tw[0][1]/4,
               'margin_change_USD_million': tw[0][2]/4,
               'wrong_transpose_margin_change_USD_million': wrong[0][2]/4}

    w1 = [[F(0), F(3, 5)], [F(0), F(0)]]
    w2 = transpose(w1)
    d1 = [[F(1), F(0)], [F(0), F(16, 25)]]
    d2 = [[F(16, 25), F(0)], [F(0), F(1)]]
    cov1 = multiply(multiply(transpose(total(w1)), d1), total(w1))
    cov2 = multiply(multiply(transpose(total(w2)), d2), total(w2))
    assert cov1 == cov2 == [[F(1), F(3, 5)], [F(3, 5), F(1)]]
    equivalence = {'covariance_forward': cov1, 'covariance_reverse': cov2,
                   'Gaussian_independent_errors': True, 'forward_effect': F(3, 5), 'reverse_effect': F(0),
                   'effect_set_for_declared_two_models': [F(0), F(3, 5)],
                   'forward_l2_population_loss': F(41, 50), 'reverse_l2_population_loss': F(41, 50),
                   'forward_l1': F(3, 5), 'reverse_l1': F(3, 5),
                   'rescaled_Y_factor': F(10), 'rescaled_forward_weight': F(6),
                   'rescaled_reverse_weight': F(3, 50),
                   'rescaled_forward_l2_loss': F(65, 2), 'rescaled_reverse_l2_loss': F(1258, 25)}

    eps = F(1, 200)
    cycle_product = float(eps**4)
    # Stable closed forms: expm trace = 2(cosh(eps**2)-1).
    h_exp = sum(2*float(eps)**(4*k)/math.factorial(2*k) for k in range(1, 8))
    h_poly = cycle_product/2
    h_logdet = -math.log1p(-cycle_product)
    assert 0 < h_exp < 1e-8 and 0 < h_poly < 1e-8 and 0 < h_logdet < 1e-8
    cyclic = {'off_diagonal_weights': eps, 'directed_two_cycle_present': True,
              'exponential_h': h_exp, 'polynomial_h_d2': h_poly,
              'logdet_h_s1': h_logdet, 'reported_tolerance_example': 1e-8,
              'threshold_retaining_cycle': F(1, 1000),
              'default_reference_threshold_0_3_removes_both_edges': True,
              'interpretation': 'Diagnostic counterexample; not a claim an optimizer returned this matrix.'}

    selected = {'law': 'F,N independent standard Gaussian; observe only F+N>0',
                'population_covariance': 0, 'selected_covariance': -1/math.pi,
                'selected_variance_each': 1-1/math.pi,
                'selected_correlation': -1/(math.pi-1)}
    clocks = {'r': 0.1, 'independent_units': 100, 'duplicated_rows': 1000,
              'unit_Z': math.sqrt(100-3)*math.atanh(0.1),
              'naive_row_Z': math.sqrt(1000-3)*math.atanh(0.1),
              'interpretation': 'Formula comparison; replacing n alone is not a dependence correction.'}
    threshold = {'weight_equals_threshold': F(3, 10), 'reference_notears_keeps': True,
                 'gcastle_binary_keeps': False, 'causalnex_unpenalized_keeps': False,
                 'causalnex_lasso_keeps': True}
    return encode({'kind': 'exact_project_algebra_and_deterministic_diagnostics',
                   'package_execution': False, 'financial_data': 'hypothetical generated coefficients',
                   'funding': funding, 'equivalence': equivalence, 'cyclic': cyclic,
                   'selection': selected, 'duplicated_rows': clocks, 'threshold_boundary': threshold})


if __name__ == '__main__':
    result = calculate()
    result['code'] = {'path': str(Path(__file__).relative_to(ROOT)),
                      'sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                      'anchor': 'Exact rational path and covariance calculations; analytic diagnostics'}
    if OUT.exists():
        assert json.loads(OUT.read_text()) == result, 'Preserve prior result; changed derivation needs successor'
    else:
        OUT.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'status': 'pass', 'examples': 6, 'margin_USD_million': result['funding']['margin_change_USD_million'],
                      'same_Gaussian_law_different_effects': result['equivalence']['effect_set_for_declared_two_models']}))
