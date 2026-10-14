#!/usr/bin/env python3
"""Independent exact examples for a proposed pcalg boundary; never imports pcalg."""
import argparse
from fractions import Fraction as F
from itertools import permutations, product
import json
from pathlib import Path


def transpose(a):
    return [list(row) for row in zip(*a)]


def multiply(a, b):
    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def inverse(a):
    n = len(a)
    aug = [[F(x) for x in row] + [F(i == j) for j in range(n)] for i, row in enumerate(a)]
    for k in range(n):
        pivot = next(i for i in range(k, n) if aug[i][k])
        aug[k], aug[pivot] = aug[pivot], aug[k]
        scale = aug[k][k]
        aug[k] = [x / scale for x in aug[k]]
        for i in range(n):
            if i != k:
                scale = aug[i][k]
                aug[i] = [x - scale * y for x, y in zip(aug[i], aug[k])]
    return [row[n:] for row in aug]


def encode(names, arrows, undirected=(), encoding='amat.cpdag'):
    a = [[0 for _ in names] for _ in names]
    for start, end in arrows:
        i, j = names.index(start), names.index(end)
        if encoding == 'amat.cpdag':
            a[j][i] = 1
        elif encoding == 'graph_matrix':
            a[i][j] = 1
        elif encoding == 'amat.pag':
            a[i][j], a[j][i] = 2, 3
        else:
            raise ValueError(encoding)
    for start, end in undirected:
        i, j = names.index(start), names.index(end)
        a[i][j] = a[j][i] = 3 if encoding == 'amat.pag' else 1
    return a


def decode(names, a, encoding):
    arrows, undirected = [], []
    allowed = {'amat.cpdag': {0, 1}, 'graph_matrix': {0, 1}, 'amat.pag': {0, 1, 2, 3}}[encoding]
    if any(value not in allowed for row in a for value in row):
        raise ValueError('conflict_or_invalid_encoding')
    for i in range(len(names)):
        assert a[i][i] == 0
        for j in range(i + 1, len(names)):
            pair = a[i][j], a[j][i]
            if pair == (0, 0):
                continue
            forward = (0, 1) if encoding == 'amat.cpdag' else (1, 0) if encoding == 'graph_matrix' else (2, 3)
            backward = forward[::-1]
            symmetric = (3, 3) if encoding == 'amat.pag' else (1, 1)
            if pair == forward:
                arrows.append((names[i], names[j]))
            elif pair == backward:
                arrows.append((names[j], names[i]))
            elif pair == symmetric:
                undirected.append(tuple(sorted((names[i], names[j]))))
            else:
                raise ValueError('outside_example_decoder_scope')
    return sorted(arrows), sorted(undirected)


def run():
    names = ['X', 'M', 'Y']
    sigma = [[F(x) for x in row] for row in [
        ['1', '.6', '.48'], ['.6', '1.36', '1.088'], ['.48', '1.088', '1.8704']]]
    assert sigma[0][2] - sigma[0][1] * sigma[1][2] / sigma[1][1] == 0
    sems, global_effects, local_effects = [], [], {}
    for first, second in product([True, False], repeat=2):
        # The undirected path has exactly three acyclic orientations without a collider.
        edges = [(0, 1) if first else (1, 0), (1, 2) if second else (2, 1)]
        if (0, 1) in edges and (2, 1) in edges:
            continue
        b = [[F(0) for _ in names] for _ in names]
        noise = [[F(0) for _ in names] for _ in names]
        for target in range(3):
            parents = [x for x, y in edges if y == target]
            if parents:
                coeff = multiply(inverse([[sigma[x][y] for y in parents] for x in parents]),
                                 [[sigma[x][target]] for x in parents])
                for parent, coefficient in zip(parents, coeff):
                    b[target][parent] = coefficient[0]
            noise[target][target] = sigma[target][target] - sum(b[target][p] * sigma[p][target] for p in parents)
            assert noise[target][target] > 0
        transform = inverse([[F(i == j) - b[i][j] for j in range(3)] for i in range(3)])
        reconstructed = multiply(multiply(transform, noise), transpose(transform))
        assert reconstructed == sigma
        effect = transform[2][0]
        global_effects.append(effect)
        parents_x = tuple(names[x] for x, y in edges if y == 0)
        if parents_x in local_effects:
            assert local_effects[parents_x] == effect
        local_effects[parents_x] = effect
        sems.append({'edges': [[names[x], names[y]] for x, y in edges],
                     'coefficients': b, 'noise': noise, 'total_effect': effect,
                     'covariance_reconstruction': True})
    assert sorted(global_effects) == [0, 0, F(12, 25)]
    assert sorted(local_effects.values()) == [0, F(12, 25)]
    global_average = sum(global_effects) / len(global_effects)
    local_average = sum(local_effects.values()) / len(local_effects)
    assert global_average == F(4, 25) and local_average == F(6, 25)
    scaled = F(1000, 100) * F(12, 25)
    assert scaled == F(24, 5) and scaled * 25 == 120

    roundtrips, transposes_rejected = 0, 0
    fixtures = [([('X', 'M'), ('M', 'Y')], []),
                ([('X', 'M'), ('Y', 'M')], []),
                ([], [('X', 'M'), ('M', 'Y')])]
    for names_order in permutations(names):
        for arrows, undirected in fixtures:
            expected = sorted(arrows), sorted(tuple(sorted(e)) for e in undirected)
            for encoding in ['amat.cpdag', 'graph_matrix', 'amat.pag']:
                matrix = encode(names_order, arrows, undirected, encoding)
                assert decode(names_order, matrix, encoding) == expected
                roundtrips += 1
                if arrows:
                    assert decode(names_order, transpose(matrix), encoding) != expected
                    transposes_rejected += 1
    conflict = [[0, 2], [2, 0]]
    try:
        decode(['X', 'Y'], conflict, 'amat.cpdag')
    except ValueError as e:
        assert str(e) == 'conflict_or_invalid_encoding'
    else:
        raise AssertionError('Conflict lost')
    collapsed = [[int(value != 0) for value in row] for row in conflict]
    assert decode(['X', 'Y'], collapsed, 'amat.cpdag') == ([], [('X', 'Y')])
    return {'scope': 'Exact project model and independent encoding references; no pcalg or adapter execution',
            'sigma': sigma, 'equal_law_sems': sems,
            'global_dag_multiset': sorted(global_effects),
            'local_parent_set_multiset': sorted(local_effects.values()),
            'unjustified_global_average': global_average, 'unjustified_local_average': local_average,
            'effect_currency_per_basis_point': scaled, 'effect_25bp_currency': scaled * 25,
            'independent_encoding_roundtrips': roundtrips,
            'intentional_transpositions_detected': transposes_rejected,
            'conflict_before_binarization': conflict, 'conflict_after_binarization': collapsed,
            'status': 'pass'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    result = run()
    args.output.write_text(json.dumps(result, indent=2, default=str) + '\n')
    print(json.dumps({k: result[k] for k in ['status', 'scope', 'independent_encoding_roundtrips',
                                          'intentional_transpositions_detected']}))
