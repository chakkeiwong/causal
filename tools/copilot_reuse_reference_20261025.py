#!/usr/bin/env python3
"""Project-authored exact interface examples; never imports upstream code."""
from fractions import Fraction
import json


def calculate():
    # Each set contains the possible directed-edge worlds represented by a result.
    unresolved = frozenset(['X_to_Y', 'Y_to_X'])
    oriented = frozenset(['X_to_Y'])
    absent = frozenset(['no_edge'])
    assert unresolved != oriented and unresolved != absent
    # Protection is symmetric in the identifiers, unlike a directed matrix slot.
    protected = {frozenset(['X', 'Y'])}
    blocked = [frozenset(pair) in protected for pair in [('X', 'Y'), ('Y', 'X')]]
    assert blocked == [True, True]
    costs = {'preparation': 1200, 'all_attempts': 1800, 'review': 2400, 'maintenance_allocation': 600}
    total = sum(costs.values())
    attempts, completed, admissible = 120, 100, 80
    assert 0 < admissible <= completed <= attempts
    return {
        'scope': 'Exact authored illustrations; no native execution or estimated bank value',
        'graph_sets': {'unresolved': sorted(unresolved), 'oriented': sorted(oriented), 'absent': sorted(absent)},
        'same_skeleton_does_not_mean_same_admissible_worlds': True,
        'both_orderings_protected': blocked,
        'costs_usd': costs, 'total_usd': total,
        'requests': {'attempted': attempts, 'completed': completed, 'scientifically_admissible': admissible},
        'usd_per_attempt': str(Fraction(total, attempts)),
        'usd_per_completion': str(Fraction(total, completed)),
        'usd_per_admissible_result': str(Fraction(total, admissible)),
        'completion_fraction': str(Fraction(completed, attempts)),
        'admissible_fraction': str(Fraction(admissible, attempts)),
    }


if __name__ == '__main__':
    print(json.dumps(calculate(), indent=2))
