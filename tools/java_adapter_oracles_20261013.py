#!/usr/bin/env python3
"""Independent finite adapter references; no Java import, subprocess or server."""
import argparse
import copy
from fractions import Fraction as F
from itertools import combinations, product
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from causalbank.operation_contract_v12 import context_digest
from java_discovery_examples_20261013 import inverse, multiply, transpose, funding


def canonical_edges(nodes, edges):
    """Reference endpoint codec, deliberately not a general CPDAG recognizer."""
    if len(nodes) != len(set(nodes)):
        raise ValueError('duplicate node')
    out = []
    for a, left, right, b in edges:
        if a == b or a not in nodes or b not in nodes:
            raise ValueError('invalid endpoint node')
        if (left, right) not in [('tail', 'tail'), ('tail', 'arrow'), ('arrow', 'tail')]:
            raise ValueError('endpoint outside initial CPDAG route')
        if a > b:
            a, left, right, b = b, right, left, a
        out.append((a, left, right, b))
    if len({(a, b) for a, _, _, b in out}) != len(out):
        raise ValueError('duplicate pair')
    return {'nodes': sorted(nodes), 'edges': [list(e) for e in sorted(out)]}


def acyclic(nodes, arcs):
    remaining = set(nodes)
    while remaining:
        sources = {x for x in remaining if not any(y == x and z in remaining for z, y in arcs)}
        if not sources:
            return False
        remaining -= sources
    return True


def chain_class():
    # X-Y-Z with no unshielded collider: enumerate all2^2 orientations.
    nodes = ['X', 'Y', 'Z']
    pairs = [('X', 'Y'), ('Y', 'Z')]
    covariance = [[F(1), F(4, 5), F(2, 5)], [F(4, 5), F(1), F(1, 2)], [F(2, 5), F(1, 2), F(1)]]
    models = []
    for choices in product([False, True], repeat=2):
        arcs = [(b, a) if reverse else (a, b) for (a, b), reverse in zip(pairs, choices)]
        if not acyclic(nodes, arcs) or (('X', 'Y') in arcs and ('Z', 'Y') in arcs):
            continue
        w = [[F(0) for _ in nodes] for _ in nodes]
        residuals = []
        for j, node in enumerate(nodes):
            parents = [nodes.index(a) for a, b in arcs if b == node]
            if parents:
                block = [[covariance[a][b] for b in parents] for a in parents]
                beta = multiply(inverse(block), [[covariance[a][j]] for a in parents])
                for a, row in zip(parents, beta):
                    w[a][j] = row[0]
            residuals.append(covariance[j][j] - sum(w[a][j] * covariance[a][j] for a in parents))
        system = [[F(i == j) - transpose(w)[i][j] for j in range(3)] for i in range(3)]
        transfer = inverse(system)
        noise = [[residuals[i] if i == j else F(0) for j in range(3)] for i in range(3)]
        assert multiply(multiply(transfer, noise), transpose(transfer)) == covariance
        # Replace X equation to obtain the do-response; no correlation shortcut.
        do_system = copy.deepcopy(system);do_system[0] = [F(1), F(0), F(0)]
        effect = multiply(inverse(do_system), [[F(1)], [F(0)], [F(0)]])[2][0]
        models.append({'arcs': arcs, 'W_source_target': w, 'noise_variances': residuals, 'X_to_Z_effect': effect})
    assert len(models) == 3 and sorted(m['X_to_Z_effect'] for m in models) == [F(0), F(0), F(2, 5)]
    return {'covariance': covariance, 'models': models, 'distinct_effect_set': ['0', '2/5'],
            'unsupported_hull_point': '1/5', 'scope': 'Exact specified Gaussian laws; not Tetrad outputs or confidence sets.'}


def endpoints():
    nodes = ['balance', 'rate', 'isolated']
    cases = [
        [('rate', 'tail', 'arrow', 'balance')],
        [('balance', 'arrow', 'tail', 'rate')],
        [('balance', 'tail', 'tail', 'rate')]]
    first, reversed_pair, unoriented = [canonical_edges(nodes, e) for e in cases]
    assert first == reversed_pair and first != unoriented
    symbols = {node: f'V{i:04d}' for i, node in enumerate(sorted(nodes))}
    inv = {v: k for k, v in symbols.items()}
    encoded = [(symbols[a], l, r, symbols[b]) for a, l, r, b in cases[0]]
    decoded = [(inv[a], l, r, inv[b]) for a, l, r, b in encoded]
    assert canonical_edges(list(reversed(nodes)), decoded) == first
    invalid = [
        [('rate', 'circle', 'arrow', 'balance')],
        [('rate', 'arrow', 'arrow', 'balance')],
        [('rate', 'tail', 'arrow', 'rate')],
        cases[0] + cases[1],
        [('missing', 'tail', 'arrow', 'balance')]]
    reasons = []
    for edges in invalid:
        try:
            canonical_edges(nodes, edges)
        except ValueError as exc:
            reasons.append(str(exc))
        else:
            raise AssertionError('invalid graph accepted')
    return {'directed': first, 'unoriented': unoriented, 'symbols': symbols,
            'invalid_reasons': reasons, 'isolated_node_preserved': True,
            'limit': 'Endpoint and identity codec only; acyclicity and full CPDAG recognition are distinct.'}


def unit_transformation():
    ex = funding();w = ex['W_source_target'];scales = [F(1), F(100), F(1000), F(10)]
    wp = [[w[i][j] * scales[j] / scales[i] for j in range(4)] for i in range(4)]
    # The original one-unit rate intervention is100 new rate units.
    a = transpose(wp);a[1] = [F(0)] * 4
    sys = [[F(i == j) - a[i][j] for j in range(4)] for i in range(4)]
    delta = [row[0] for row in multiply(inverse(sys), [[F(0)], [F(100)], [F(0)], [F(0)]])]
    recovered = [v / s for v, s in zip(delta, scales)]
    assert recovered == ex['correct_response']
    threshold = F(1, 10)
    original_edges = [(i, j) for i in range(4) for j in range(4) if abs(w[i][j]) > threshold]
    rescaled_edges = [(i, j) for i in range(4) for j in range(4) if abs(wp[i][j]) > threshold]
    assert original_edges != rescaled_edges
    return {'scales': scales, 'new_W_source_target': wp, 'original_unit_response': recovered,
            'threshold': threshold, 'retained_original': original_edges, 'retained_rescaled': rescaled_edges,
            'scope': 'Algebraic coefficient conversion, not a claim that the PC route estimates coefficients.'}


def identity_mutations():
    original = {'target': {'treatment': 'rate', 'outcome': 'balance', 'contrast': [1, 0]},
                'population': 'illustrative eligible deposit accounts', 'horizon': '12 months',
                'units': ['USD'], 'sampling': {'law': 'iid', 'unit': 'account'},
                'observation_clock': {'available_before_decision': True},
                'graph': {'kind': 'CPDAG', 'edges': [['rate', 'tail', 'tail', 'balance']]}}
    mutations = []
    for label, mutate in [
        ('unit', lambda x: x.update(units=['thousand_USD'])),
        ('contrast', lambda x: x['target'].update(contrast=[0, 1])),
        ('sampling', lambda x: x['sampling'].update(law='clustered')),
        ('clock', lambda x: x['observation_clock'].update(available_before_decision=False)),
        ('orientation', lambda x: x['graph'].update(edges=[['rate', 'tail', 'arrow', 'balance']]))]:
        changed = copy.deepcopy(original);mutate(changed)
        assert context_digest(original) != context_digest(changed)
        mutations.append({'change': label, 'different_digest': True})
    encoded = json.dumps(original, sort_keys=True)
    transported = [json.loads(encoded) for _ in ['library', 'CLI', 'MCP']]
    assert len({context_digest(x) for x in transported}) == 1
    return {'original': original, 'digest': context_digest(original), 'mutations': mutations,
            'same_canonical_payload_three_transports': True,
            'limit': 'Reference serialization only; no actual CLI/MCP or transport authentication exercised.'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=ROOT / 'docs/program/execution/2026-10-13/java-integration/oracle-results.json')
    args = parser.parse_args()
    result = {'kind': 'exact_proposal_adapter_references', 'java_executed': False,
              'random_draws': 0, 'gaussian_equivalence_class': chain_class(),
              'endpoint_codec': endpoints(), 'unit_transformation': unit_transformation(),
              'scientific_identity': identity_mutations()}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, default=lambda v: str(v) if isinstance(v, F) else v) + '\n')
    print(json.dumps({'status': 'pass', 'examples': 4, 'consistent_graphs': 3, 'java_executed': False,
                      'output': str(args.output)}))


if __name__ == '__main__':
    main()
