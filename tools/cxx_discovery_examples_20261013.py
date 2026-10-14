#!/usr/bin/env python3
"""Exact project examples for the C++ proposal survey, not vendor execution."""
import argparse
from fractions import Fraction as F
from itertools import permutations, product
import json
from pathlib import Path


def transpose(a):
    return [list(row) for row in zip(*a)]


def multiply(a, b):
    return [[sum((x * y for x, y in zip(row, col)), F(0))
             for col in zip(*b)] for row in a]


def inverse(a):
    n = len(a)
    aug = [list(row) + [F(i == j) for j in range(n)] for i, row in enumerate(a)]
    for k in range(n):
        pivot = next(i for i in range(k, n) if aug[i][k])
        aug[k], aug[pivot] = aug[pivot], aug[k]
        scale = aug[k][k]
        aug[k] = [v / scale for v in aug[k]]
        for i in range(n):
            if i != k:
                scale = aug[i][k]
                aug[i] = [x - scale * y for x, y in zip(aug[i], aug[k])]
    return [row[n:] for row in aug]


def effects(w):
    """w[source, target]; x = w.T x + epsilon."""
    return inverse([[F(i == j) - w[j][i] for j in range(len(w))]
                    for i in range(len(w))])


def direct_intervention(w, order, target, value):
    """Independent topological substitution in structural equations."""
    x = [F(0)] * len(w)
    for j in order:
        x[j] = value if j == target else sum((w[i][j] * x[i] for i in range(len(w))), F(0))
    return x


def covariance(w, variances):
    l = effects(w)
    return multiply(multiply(l, [[v if i == j else F(0) for j in range(len(w))]
                                for i, v in enumerate(variances)]), transpose(l))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    w = [[F(0), F(1, 2), F(-1, 10)],
         [F(0), F(0), F(2, 5)], [F(0), F(0), F(0)]]
    true_effect = effects(w)[2][0]
    direct = direct_intervention(w, [0, 1, 2], 0, F(1))[2]
    assert true_effect == direct == F(1, 10)
    wrong_effect = effects(transpose(w))[2][0]
    assert wrong_effect == 0
    checks = []
    for order in permutations(range(3)):
        permuted = [[w[i][j] for j in order] for i in order]
        a, y = order.index(0), order.index(2)
        value = effects(permuted)[y][a]
        topo = [order.index(i) for i in range(3)]
        assert value == direct_intervention(permuted, topo, a, F(1))[y] == true_effect
        checks.append({'node_order': order, 'effect': str(value)})
    # Backend bitmaps can store parents by child while the external contract
    # stores sources by row. This is a project encoding check, not OpenBNSL.
    masks = [sum(1 << i for i in range(3) if w[i][j]) for j in range(3)]
    decoded = [[bool(masks[j] & (1 << i)) for j in range(3)] for i in range(3)]
    assert decoded == [[bool(v) for v in row] for row in w]
    d = [F(1), F(10), F(1_000_000)]
    rescaled = [[w[i][j] * d[j] / d[i] for j in range(3)] for i in range(3)]
    assert effects(rescaled)[2][0] == 100_000

    chain = [[F(0), F(1, 2), F(0)], [F(0), F(0), F(2, 5)], [F(0)] * 3]
    fork = [[F(0)] * 3, [F(1, 2), F(0), F(2, 5)], [F(0)] * 3]
    reverse = [[F(0)] * 3, [F(1, 2), F(0), F(0)], [F(0), F(2, 5), F(0)]]
    covs = [covariance(chain, [F(1), F(3, 4), F(21, 25)]),
            covariance(fork, [F(3, 4), F(1), F(21, 25)]),
            covariance(reverse, [F(3, 4), F(21, 25), F(1)])]
    assert covs[0] == covs[1] == covs[2]
    effect_set = sorted({effects(model)[2][0] for model in [chain, fork, reverse]})
    assert effect_set == [F(0), F(1, 5)]

    # Same joint distribution and zero conditional entropy; different do-laws.
    directed_observations = [(u, u) for u in [0, 1]]
    common_cause_observations = [(u, u) for u in [0, 1]]
    assert directed_observations == common_cause_observations
    effect_directed = F(1)
    effect_common = sum((F(u, 2) - F(u, 2) for u in [0, 1]), F(0))
    assert effect_common == 0

    # Positive treatment probabilities, independent A and Y given risk R.
    joint = {}
    for r, a, y in product([0, 1], repeat=3):
        p = F(4, 5) if r else F(1, 5)
        joint[(r, a, y)] = F(1, 2) * (p if a else 1-p) * (p if y else 1-p)
    assert sum(joint.values()) == 1
    means = [sum(v * y for (r, aa, y), v in joint.items() if aa == a) /
             sum(v for (r, aa, y), v in joint.items() if aa == a) for a in [0, 1]]
    contrast = means[1] - means[0]
    assert contrast == F(9, 25)
    risk_contrasts = []
    for r in [0, 1]:
        conditional = [sum(v * y for (rr, aa, y), v in joint.items() if rr == r and aa == a) /
                       sum(v for (rr, aa, y), v in joint.items() if rr == r and aa == a)
                       for a in [0, 1]]
        risk_contrasts.append(conditional[1] - conditional[0])
    assert risk_contrasts == [F(0), F(0)]
    result = {
        'kind': 'exact_project_derivations', 'vendor_code_executed': False,
        'funding': {'variables': ['offer in 10bp units', 'retained deposits in USD10m units',
                                  'annual contribution in USD1m units'],
                    'matrix_convention': 'W[source,target], x=W.T*x+epsilon',
                    'W': [[str(x) for x in row] for row in w],
                    'direct_effect': '-1/10', 'mediated_effect': '1/5',
                    'total_effect': str(true_effect), 'annual_usd': 100000,
                    'transposed_annual_usd': 0, 'negative_weight_dropped_annual_usd': 200000,
                    'node_permutation_checks': checks, 'parent_bitmasks': masks,
                    'rescaled_annual_usd': 100000},
        'equivalence': {'covariance': [[str(x) for x in row] for row in covs[0]],
                        'three_models_same_covariance': True,
                        'offer_to_contribution_effects': [str(x) for x in effect_set],
                        'monetary_effects_usd': [0, 200000],
                        'uncertainty_kind': 'structural ambiguity, no sampling interval'},
        'entropy': {'observed_atoms': directed_observations, 'atom_probability': '1/2',
                    'conditional_entropy_bits': 0, 'directed_effect': str(effect_directed),
                    'common_cause_effect': str(effect_common)},
        'coarsening': {'positive_treatment_probabilities': ['1/5', '4/5'],
                       'conditional_effect': '0', 'true_do_effect': '0',
                       'coarsened_association': str(contrast),
                       'conditional_means': [str(x) for x in means]},
        'limitations': ['Synthetic accounting; no bank estimate.',
                        'Exact algebra only; no empirical discovery performance or calibration.',
                        'No third-party engine was compiled or executed.']}
    Path(args.output).write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': 'pass', 'permutations': len(checks), 'funding_usd': 100000,
                      'effect_set_usd': [0, 200000], 'coarsened_association': str(contrast)}))


if __name__ == '__main__':
    main()
