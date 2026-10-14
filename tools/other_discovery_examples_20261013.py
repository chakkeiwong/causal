#!/usr/bin/env python3
"""Finite graph-contract examples; no execution of surveyed packages."""
from fractions import Fraction as F
from statistics import NormalDist
import json


def transpose(a):
    return [list(row) for row in zip(*a)]


def multiply(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def inverse(a):
    n = len(a)
    m = [[F(x) for x in row]+[F(i == j) for j in range(n)] for i, row in enumerate(a)]
    for i in range(n):
        pivot = next(j for j in range(i, n) if m[j][i])
        m[i], m[pivot] = m[pivot], m[i]
        scale = m[i][i]
        m[i] = [x/scale for x in m[i]]
        for j in range(n):
            if j != i:
                scale = m[j][i]
                m[j] = [x-scale*y for x, y in zip(m[j], m[i])]
    return [row[n:] for row in m]


def structural_covariance(b, noise):
    n = len(b)
    transfer = inverse([[F(i == j)-b[i][j] for j in range(n)] for i in range(n)])
    variance = [[noise[i] if i == j else F(0) for j in range(n)] for i in range(n)]
    return multiply(multiply(transfer, variance), transpose(transfer))


def response(b, treatment, delta):
    # Replace treatment equation. Effects concern do(Q), not a noise shock.
    changed = [list(row) for row in b]
    changed[treatment] = [F(0)]*len(b)
    transfer = inverse([[F(i == j)-changed[i][j] for j in range(len(b))] for i in range(len(b))])
    return [row[treatment]*delta for row in transfer]


def calculate():
    models = {
        'risk_quote_funding': {'B': [[0, 0, 0], [F(1, 2), 0, 0], [0, 2, 0]], 'noise': [1, F(3, 4), 1]},
        'quote_root': {'B': [[0, F(1, 2), 0], [0, 0, 0], [0, 2, 0]], 'noise': [F(3, 4), 1, 1]},
        'funding_quote_risk': {'B': [[0, F(1, 2), 0], [0, 0, F(2, 5)], [0, 0, 0]], 'noise': [F(3, 4), F(1, 5), 5]},
    }
    expected = [[1, F(1, 2), 1], [F(1, 2), 1, 2], [1, 2, 5]]
    for row in models.values():
        row['covariance'] = structural_covariance(row['B'], row['noise'])
        assert row['covariance'] == expected
        row['do_quote_quarter_response'] = response(row['B'], 1, F(1, 4))
    assert [r['do_quote_quarter_response'][2] for r in models.values()] == [F(1, 2), F(1, 2), 0]
    forward = models['risk_quote_funding']['B']
    wrong = response(transpose(forward), 1, F(1, 4))
    assert wrong[2] == 0
    # Three equivalent Gaussian constructions share U independent of F | Q.
    conditional_covariance = expected[0][2]-expected[0][1]*expected[1][2]/expected[1][1]
    assert conditional_covariance == 0
    cpdag_pairs = {'julia_reciprocal_arcs': [1, 1], 'flop': [2, 2],
                   'generalized_ges': [-1, -1], 'bnt_pc': [1, 1]}
    directed_pairs = {'julia_reciprocal_arcs': [1, 0], 'flop': [1, 0],
                      'generalized_ges': [1, 0], 'bnt_pc': [-1, 0]}
    # Pure adapter contract demonstration. The same numerical value has
    # different meaning in different declared graph representations.
    for family, pair in cpdag_pairs.items():
        assert pair[0] == pair[1] and pair[0] != 0
        assert directed_pairs[family][1] == 0
    alpha = 0.02
    nominal = NormalDist().inv_cdf(1-alpha/2)
    inspected_fallback = 1.960
    statistic = 2.2
    assert statistic < nominal and statistic > inspected_fallback
    return {'kind': 'exact_project_graph_contract_examples', 'random_draws': 0,
        'surveyed_package_executions': 0, 'models': models,
        'variable_order': ['risk_index', 'quote_percentage_points', 'funding_USD_million'],
        'disturbance_law': 'Centered independent Gaussian within each of the three stipulated models',
        'conditional_covariance_risk_funding_given_quote': conditional_covariance,
        'effect_set_quote_slope': [0, 2], 'quarter_point_funding_effect_set': [0, F(1, 2)],
        'transpose_error_response': wrong, 'undirected_pair_contracts': cpdag_pairs,
        'directed_pair_contracts': directed_pairs,
        'threshold_formula_example': {'requested_alpha': alpha, 'nominal_normal_critical': nominal,
            'inspected_fallback_critical': inspected_fallback, 'statistic': statistic,
            'nominal_rejects': statistic > nominal, 'fallback_rejects': statistic > inspected_fallback,
            'normal_reference_size_at_fallback': 2*(1-NormalDist().cdf(inspected_fallback)),
            'scope': 'Scalar reference-rule calculation; not an empirical rejection rate or a Rust runtime test'},
        'limits': ['Exactly three stipulated linear Gaussian worlds; no fitted bank coefficient.',
                   'The finite effect set is not a confidence interval or all causal models.',
                   'Encodings require a named method/version and cannot identify graph type by values alone.',
                   'No new engine benchmark, package installation, live model call or external action.']}


def serialize(x):
    if isinstance(x, F):
        return {'exact': str(x), 'decimal': float(x)}
    if isinstance(x, dict):
        return {k: serialize(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [serialize(v) for v in x]
    return x


if __name__ == '__main__':
    print(json.dumps(serialize(calculate()), indent=2))
