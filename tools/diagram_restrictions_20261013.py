#!/usr/bin/env python3
"""Three positive observed laws, clocks and exact model-class restrictions."""
from fractions import Fraction as F
from itertools import product
import json


def main():
    tables = {}
    for model in ('F', 'R', 'C'):
        table = {(a, y): F(0) for a, y in product((0, 1), repeat=2)}
        for base, error in product((0, 1), repeat=2):
            mass = F(1, 2) * (F(1, 10) if error else F(9, 10))
            if model == 'F':
                a, y = base, base ^ error
            else:
                # R: base is Y; C: base is pre-action U and Y=U.
                a, y = base ^ error, base
            table[a, y] += mass
        assert sum(table.values()) == 1 and all(p > 0 for p in table.values())
        tables[model] = table
    assert tables['F'] == tables['R'] == tables['C']
    # Intervention replaces only the A equation. In R and C, Y remains fair.
    do_means = {}
    for model in tables:
        do_means[model] = []
        for action in (0, 1):
            mean = F(0)
            for base, error in product((0, 1), repeat=2):
                mass = F(1, 2) * (F(1, 10) if error else F(9, 10))
                outcome = action ^ error if model == 'F' else base
                mean += mass * outcome
            do_means[model].append(mean)
    effects = {m: means[1] - means[0] for m, means in do_means.items()}
    assert effects == {'F': F(4, 5), 'R': F(0), 'C': F(0)}
    rows = []
    for name, models in [('initial', ['F', 'R', 'C']),
                         ('valid_time_order', ['F', 'C']),
                         ('time_order_and_valid_exogeneity', ['F'])]:
        rows.append({'restriction': name, 'models': models,
                     'effect_candidates': sorted({effects[m] for m in models})})
    # Three direct-edge restrictions on the SAME variable instances.
    edges = [(0, 1), (1, 2), (2, 0)]
    def acyclic(chosen):
        reach = {(a, b) for a, b in chosen}
        for k in range(3):
            reach |= {(a, b) for a in range(3) for b in range(3)
                      if (a, k) in reach and (k, b) in reach}
        return not any((i, i) in reach for i in range(3))
    assert not acyclic(edges)
    assert all(acyclic(edges[:i] + edges[i+1:]) for i in range(3))
    print(json.dumps({'kind': 'stipulated_exact_model_class_examples',
                      'random_draws': 0, 'bank_data': False, 'live_model_calls': 0,
                      'observed_joint': {str(k): v for k, v in tables['F'].items()},
                      'all_observed_cells_positive': True,
                      'do_means': do_means, 'effects': effects, 'restrictions': rows,
                      'confounded_assignment_given_u': ['1/10', '9/10'],
                      'cycle_restrictions': edges, 'inclusion_minimal_conflict': True,
                      'scope': 'Finite candidate list, not all compatible causal models'},
                     indent=2, default=str))


if __name__ == '__main__':
    main()
