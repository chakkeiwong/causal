#!/usr/bin/env python3
"""Exact project diagnostics for a source review; does not run downloaded Java."""
import argparse
from fractions import Fraction as F
from itertools import combinations
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / 'docs/program/execution/2026-10-13/java-discovery/exact-results.json'


def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def transpose(a):
    return [list(r) for r in zip(*a)]


def multiply(a, b):
    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def inverse(a):
    n = len(a)
    aug = [list(row) + unit for row, unit in zip(a, eye(n))]
    for k in range(n):
        pivot = next(i for i in range(k, n) if aug[i][k])
        aug[k], aug[pivot] = aug[pivot], aug[k]
        scale = aug[k][k]
        aug[k] = [v / scale for v in aug[k]]
        for i in range(n):
            if i != k:
                scale = aug[i][k]
                aug[i] = [x - scale * y for x, y in zip(aug[i], aug[k])]
    out = [row[n:] for row in aug]
    assert multiply(a, out) == eye(n)
    return out


def conditional_covariance(cov, x, y, given):
    if not given:
        return cov[x][y]
    block = [[cov[i][j] for j in given] for i in given]
    left = [[cov[x][i] for i in given]]
    right = [[cov[i][y]] for i in given]
    return cov[x][y] - multiply(multiply(left, inverse(block)), right)[0][0]


def funding():
    # W[source][target]; x = W^T x + epsilon in a column-vector SEM.
    names = ['liquidity_pressure', 'rate_concession', 'balances', 'net_funding_cost']
    w = [[F(0) for _ in names] for _ in names]
    for i, j, v in [(0, 1, F(1, 2)), (0, 2, F(3, 10)),
                    (1, 2, F(4, 5)), (1, 3, F(1, 10)), (2, 3, F(-1, 5))]:
        w[i][j] = v

    def response(weights, treatment):
        # Surgical intervention removes all incoming treatment edges.
        a = transpose(weights)
        a[treatment] = [F(0)] * len(a)
        system = [[F(i == j) - a[i][j] for j in range(len(a))] for i in range(len(a))]
        shock = [[F(i == treatment)] for i in range(len(a))]
        return [row[0] for row in multiply(inverse(system), shock)]

    correct = response(w, 1)
    reversed_result = response(transpose(w), 1)
    sign_lost = response([[abs(v) for v in row] for row in w], 1)
    assert correct == [F(0), F(1), F(4, 5), F(-3, 50)]
    assert reversed_result == [F(1, 2), F(1), F(0), F(0)]
    assert sign_lost[-1] == F(13, 50)
    # Both orientations are acyclic: each has zero fourth matrix power.
    for weights in (w, transpose(w)):
        assert multiply(multiply(weights, weights), multiply(weights, weights)) == [[0]*4 for _ in range(4)]
    return {'variables': names, 'W_source_target': w,
            'intervention': 'increase rate_concession by one model unit',
            'correct_response': correct, 'transposed_response': reversed_result,
            'absolute_weight_response': sign_lost,
            'check': 'Structural substitution and exact matrix inverse agree; both orientations acyclic.',
            'limit': 'Stipulated normalized banking SEM, not a fitted effect or Java run.'}


def conditioning():
    # Independent standard Gaussian noises, ordered Z1,Z2,Z3,eX,eY,eC.
    names = ['Z1', 'Z2', 'Z3', 'X', 'Y', 'C']
    loading = [[F(v) for v in row] for row in
               [[1, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0],
                [1, 1, 1, 1, 0, 0], [1, 1, 1, 0, 1, 0], [2, 2, 2, 1, 1, 1]]]
    cov = multiply(loading, transpose(loading))
    candidates = [0, 1, 2, 5]
    small = [{'given': [names[z] for z in subset],
              'conditional_covariance': conditional_covariance(cov, 3, 4, subset)}
             for size in range(3) for subset in combinations(candidates, size)]
    assert len(small) == 11 and all(row['conditional_covariance'] != 0 for row in small)
    separated = conditional_covariance(cov, 3, 4, [0, 1, 2])
    opened = conditional_covariance(cov, 3, 4, candidates)
    vx = conditional_covariance(cov, 3, 3, candidates)
    vy = conditional_covariance(cov, 4, 4, candidates)
    assert separated == 0 and opened == F(-1, 3) and vx == vy == F(2, 3)
    # True skeleton neighbours Z1,Z2,Z3,C remain attached to X and Y;
    # Z_i-C can be separated by X,Y at depth 2 without removing those neighbours.
    assert all(conditional_covariance(cov, z, 5, [3, 4]) == 0 for z in range(3))
    return {'variables': names, 'structural_law': 'X=Z1+Z2+Z3+eX; Y=Z1+Z2+Z3+eY; C=X+Y+eC; independent N(0,1) inputs',
            'covariance': cov, 'all_size_zero_to_two_cases': small,
            'separator_Z1_Z2_Z3': separated,
            'all_neighbours_Z1_Z2_Z3_C': opened, 'conditional_variances': [vx, vy],
            'all_neighbours_partial_correlation': opened / vx,
            'check': 'All11 smaller subsets fail to separate; three baseline variables separate; adding collider reopens path.',
            'limit': 'Exact Gaussian population counterexample to a monotonicity shortcut; no compiled Aitiotita run or full implementation theorem.'}


def symmetric_moments():
    results = []
    for values in ([-3, -1, 1, 3], [-1, -1, 1, 1]):
        second = sum(F(v * v) for v in values) / len(values)
        fourth_standardized = sum(F(v**4) for v in values) / len(values) / second**2
        # With population standardization both have unit second moment;
        # the odd term cancels pair by pair, independently of scale convention.
        b1, b2 = F(1, 2), F(0)
        entropy = (math.log(2 * math.pi) / 2 + .5) - 79.047 * (float(b1) - .37457)**2
        results.append({'vector': values, 'fourth_standardized_moment': fourth_standardized,
                        'b1_population_standardization': b1, 'b2': b2, 'source_expression_value': entropy})
    assert results[0]['fourth_standardized_moment'] != results[1]['fourth_standardized_moment']
    assert results[0]['source_expression_value'] == results[1]['source_expression_value']
    return {'cases': results,
            'check': 'Second-moment and odd-moment expression cannot distinguish these equal-length symmetric inputs despite different fourth moments.',
            'limit': 'Algebraic diagnostic of the inspected helper only. Sample-variance standardization changes the common first term to(n-1)/(2n). It does not establish the ordering output, numerical parity, or failure rate of DirectLiNGAM.'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=DEFAULT)
    args = parser.parse_args()
    result = {'kind': 'exact_project_derivations', 'random_draws': 0,
              'downloaded_code_executed': False, 'funding_orientation': funding(),
              'nonmonotone_conditioning': conditioning(), 'symmetric_moment_diagnostic': symmetric_moments()}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, default=lambda v: str(v) if isinstance(v, F) else v) + '\n')
    print(json.dumps({'status': 'pass', 'output': str(args.output), 'examples': 3, 'random_draws': 0}))


if __name__ == '__main__':
    main()
