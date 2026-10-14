#!/usr/bin/env python3
"""Exact authored examples; no R package or downloaded code is executed."""
import argparse
import hashlib
import json
import re
from fractions import Fraction as F
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def calculate():
    # World A: randomized action; Y responds with probabilities 1/5 and 4/5.
    direct = {(a, y): F(1, 2) * (F(1, 5) + F(3, 5) * a if y else F(4, 5) - F(3, 5) * a)
              for a, y in product(range(2), repeat=2)}
    # World B: hidden U sets Y; action assignment depends on U.
    hidden = {(a, y): F(0) for a, y in direct}
    for u, a in product(range(2), repeat=2):
        pa = F(1, 5) + F(3, 5) * u
        hidden[a, u] += F(1, 2) * (pa if a else 1 - pa)
    assert direct == hidden and min(direct.values()) > 0
    # Independent 20-unit enumeration reproduces the observed table.
    units = [(a, y) for (a, y), mass in direct.items() for _ in range(int(20 * mass))]
    assert len(units) == 20
    assert {cell: F(units.count(cell), 20) for cell in direct} == hidden
    # Selection alone: A,Y independent fair bits; selection odds favor equality.
    selected = {(a, y): F(1, 4) * (F(4, 5) if a == y else F(1, 5))
                for a, y in product(range(2), repeat=2)}
    selection_mass = sum(selected.values())
    selected = {cell: mass / selection_mass for cell, mass in selected.items()}
    assert selected == direct
    # Endpoints are serialized by column in amat.pag. Inspect branches, do not run R.
    source = ROOT / 'docs/literature/raw/exec13_latentr_r_pcalg2dagitty.txt'
    text = source.read_text()
    found = {(int(a), int(b)) for a, b in re.findall(r'amat\[i,j\]==([123]) & amat\[j,i\]==([123])', text)}
    expected = set(product((1, 2, 3), repeat=2))
    assert found == {(1, 1), (2, 3), (3, 2), (3, 3), (2, 2), (2, 1), (1, 2)}
    assert expected - found == {(1, 3), (3, 1)}
    # Stipulated information loss for alpha interpreted as a family confidence.
    alpha = F(1, 20); tests = 100
    # Under an explicitly authored independent true-null experiment only.
    any_false_reject = 1 - (1 - alpha) ** tests
    return {
        'kind': 'authored_exact_latent_discovery_and_source_trace',
        'observed_cells': [{'A': a, 'Y': y, 'probability': str(p)} for (a, y), p in sorted(direct.items())],
        'same_observed_law': True, 'independent_observed_count_check': 20,
        'worlds': {
            'direct_effect': {'graph': 'A -> Y', 'do_means': ['1/5', '4/5'], 'effect': '3/5'},
            'hidden_cause': {'graph': 'A <- U -> Y; U hidden', 'do_means': ['1/2', '1/2'], 'effect': '0'},
            'selected_sample': {'graph': 'A -> S <- Y; observed conditional on S=1',
                                'selection_probability': str(selection_mass), 'population_do_means': ['1/2', '1/2'], 'effect': '0'}},
        'banking_scenario': {'value_per_recovery_USD': 100, 'action_cost_USD': 20,
                            'net_values_by_world_USD': ['40', '-20', '-20'],
                            'limit': 'Authored laws and prices; selected-sample transport is not identified by this table.'},
        'endpoint_source_trace': {'source': str(source.relative_to(ROOT)),
            'sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
            'explicit_nonzero_pair_branches': sorted([list(x) for x in found]),
            'unhandled_tail_circle_pairs': [[1, 3], [3, 1]],
            'counterexample': {'labels': ['A', 'Y'], 'amat': [[0, 1], [3, 0]],
                              'documented_edge': 'A --o Y', 'source_traced_string': 'pag{}',
                              'limit': 'String construction trace only; parser response and native runtime not executed.'}},
        'individual_test_alpha_example': {'tests': tests, 'alpha': str(alpha),
            'independent_any_false_rejection': float(any_false_reject),
            'arbitrary_dependence_union_bound': str(min(F(1), tests * alpha)),
            'limit': 'Stipulated independent true-null tests; not the error rate of FCI, adaptive test families or a particular PAG.'},
        'upstream_package_executed': False, 'live_calls': 0, 'random_draws': 0}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = calculate()
    if args.output.exists():
        raise SystemExit('Refusing to overwrite preserved output')
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': 'pass', 'observed_cells': 4, 'worlds': 3, 'unhandled_endpoint_pairs': 2, 'upstream_execution': False}))

if __name__ == '__main__':
    main()
