#!/usr/bin/env python3
"""Exact authored graph-contract witnesses; never imports or runs gCastle."""
from fractions import Fraction as F
import json


def encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {k: encode(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [encode(v) for v in value]
    return value


def pc_edges(matrix, labels):
    assert len(set(labels)) == len(labels) == len(matrix)
    directed, undirected = [], []
    for i in range(len(labels)):
        assert len(matrix[i]) == len(labels) and matrix[i][i] == 0
        for j in range(i+1, len(labels)):
            pair = matrix[i][j], matrix[j][i]
            assert pair in [(0, 0), (1, 0), (0, 1), (1, 1)]
            if pair == (1, 1):
                undirected.append(sorted([labels[i], labels[j]]))
            elif pair == (1, 0):
                directed.append([labels[i], labels[j]])
            elif pair == (0, 1):
                directed.append([labels[j], labels[i]])
    return dict(directed=sorted(directed), undirected=sorted(undirected))


def acyclic(matrix):
    indegrees = [sum(row[j] != 0 for row in matrix) for j in range(len(matrix))]
    queue = [j for j, count in enumerate(indegrees) if count == 0]
    removed = 0
    while queue:
        node = queue.pop()
        removed += 1
        for j, present in enumerate(matrix[node]):
            if present:
                indegrees[j] -= 1
                if indegrees[j] == 0:
                    queue.append(j)
    return removed == len(matrix)


def calculate():
    # One unresolved pair plus an oriented edge. A matrix without its type is ambiguous.
    labels = ['offer', 'response', 'margin', 'cost_shock']
    raw = [[0, 1, 0, 0], [1, 0, 1, 0], [0, 0, 0, 0], [0, 0, 1, 0]]
    decoded = pc_edges(raw, labels)
    assert decoded == dict(directed=[['cost_shock', 'margin'], ['response', 'margin']],
                           undirected=[['offer', 'response']])
    order = [2, 0, 3, 1]
    permuted = [[raw[i][j] for j in order] for i in order]
    assert pc_edges(permuted, [labels[i] for i in order]) == decoded
    assert not acyclic(raw)  # Deliberately wrong interpretation: every nonzero as a directed edge.
    assert acyclic([[0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 0], [0, 0, 1, 0]])
    assert acyclic([[0, 0, 0, 0], [1, 0, 1, 0], [0, 0, 0, 0], [0, 0, 1, 0]])

    # For d=2, tr((I+W o W/2)^2)-2 = a^2 b^2/2.
    a = b = F(1, 100)
    h = a*a*b*b/2
    tolerance, threshold = F(1, 10**8), F(1, 200)
    weights = [[F(0), a], [b, F(0)]]
    binary = [[int(abs(w) > threshold) for w in row] for row in weights]
    default = [[int(abs(w) > F(3, 10)) for w in row] for row in weights]
    assert h == F(1, 200000000) and 0 < h < tolerance
    assert not acyclic(binary) and acyclic(default)

    # An assumed structural coefficient, not an estimated causal claim.
    weight = cutoff = F(3, 10)
    raw_kept, scaled_kept = abs(weight) > cutoff, abs(100*weight) > cutoff
    assert not raw_kept and scaled_kept
    direct_margin = 100*weight-20
    transposed_margin = F(0)-20
    assert direct_margin == 10 and transposed_margin == -20

    # Literal source branch implication, not a native CI experiment.
    zero_dof_p = F(1)
    alpha = F(1, 20)
    assert zero_dof_p >= alpha
    return encode(dict(
        scope='Project-authored exact references; no gCastle execution, fitted output, or bank evidence',
        pc=dict(labels=labels, raw=raw, decoded=decoded, permutation=order,
                permutation_preserves_named_edges=True, naive_directed_interpretation_is_cyclic=True,
                two_displayed_DAG_completions_are_acyclic=True,
                interpretation='Symmetric pair means one unresolved edge, not a directed cycle or latent bidirected edge'),
        polynomial=dict(a=a, b=b, h=h, tolerance=tolerance, threshold=threshold,
                thresholded=binary, thresholded_acyclic=False,
                default_threshold=F(3,10), at_default_threshold=default,
                boundary='Illustrative weights, not observed optimizer output; chosen threshold differs from default'),
        scale=dict(weight=weight, threshold=cutoff, equality_retained=raw_kept,
                predictor_scale_divisor=100, transformed_weight=100*weight,
                transformed_edge_retained=scaled_kept,
                boundary='Same assumed linear equation expressed in different predictor units'),
        economics=dict(assumed_intervention=100, assumed_cost_USD=20,
                correct_margin_USD=direct_margin, wrongly_transposed_margin_USD=transposed_margin,
                boundary='Known authored structural law only; algorithm weights need separate identification'),
        sparse_CI=dict(conditional_dof=0, source_fallback_p=zero_dof_p, alpha=alpha,
                satisfies_source_edge_removal_branch=True,
                boundary='Source branch trace; no claim that zero-support conditional tests demonstrate population independence')))


if __name__ == '__main__':
    print(json.dumps(calculate(), indent=2))
