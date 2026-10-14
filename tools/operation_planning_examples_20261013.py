#!/usr/bin/env python3
"""Exact operational planning counterexamples, not live reliability measurements."""
from fractions import Fraction as F
import json


def calculate():
    costs = {'easy_success': {'mass': F(7, 10), 'gross_increment': 10, 'extra_recovery_cost': 0},
             'hard_success': {'mass': F(3, 20), 'gross_increment': -30, 'extra_recovery_cost': 0},
             'hard_failure_fallback': {'mass': F(3, 20), 'gross_increment': 0, 'extra_recovery_cost': 20}}
    assert sum(row['mass'] for row in costs.values()) == 1
    gross = sum(row['mass']*row['gross_increment'] for row in costs.values())
    recovery = sum(row['mass']*row['extra_recovery_cost'] for row in costs.values())
    success_mass = F(17, 20)
    all_net = gross-2-recovery
    success_only = gross/success_mass-2
    assert gross == F(5, 2) and all_net == F(-5, 2) and success_only == F(16, 17)
    # At most three attempts. The independence case and persistent-failure
    # mixture are two different stipulated laws, not measured retry rates.
    transient_failure = F(1, 5)
    independent_success = 1-transient_failure**3
    independent_attempts = sum(transient_failure**i for i in range(3))
    persistent_mass, good_failure = F(1, 10), F(1, 10)
    mixture_success = (1-persistent_mass)*(1-good_failure**3)
    mixture_attempts = 3*persistent_mass+(1-persistent_mass)*sum(good_failure**i for i in range(3))
    marginal_failure = persistent_mass+(1-persistent_mass)*good_failure
    false_iid_success = 1-marginal_failure**3
    assert independent_success == F(124, 125) and independent_attempts == F(31, 25)
    assert mixture_success == F(8991, 10000) and mixture_attempts == F(1299, 1000)
    assert false_iid_success == F(993141, 1000000)
    # Pure keyed contributions: a crash after a durable contribution may
    # replay its calculation, but must not add it again to the public total.
    items = [('a', 100), ('b', -40), ('c', 70)]
    trace = [items[0], items[1], items[1], items[2]]
    naive = sum(value for _, value in trace)
    keyed = {}
    for key, value in trace:
        if key in keyed: assert keyed[key] == value
        keyed[key] = value
    assert sum(value for _, value in items) == sum(keyed.values()) == 130
    assert naive == 90
    selected_significance = 1-F(19, 20)**3
    assert selected_significance == F(1141, 8000)
    return {'kind': 'exact_project_operational_planning_examples', 'random_draws': 0,
        'new_live_fault_trials': 0, 'bank_actions': 0,
        'selection_cost': {'currency': 'stipulated USD per attempted request', 'law': costs,
            'cost_every_attempt': 2, 'gross_all_attempts': gross, 'extra_recovery_all_attempts': recovery,
            'success_fraction': success_mass, 'all_attempt_net': all_net,
            'success_only_net_excluding_recovery': success_only},
        'retry': {'max_attempts': 3, 'iid_transient_failure': transient_failure,
            'iid_success': independent_success, 'iid_expected_attempts': independent_attempts,
            'persistent_mass': persistent_mass, 'good_conditional_failure': good_failure,
            'mixture_success': mixture_success, 'mixture_expected_attempts': mixture_attempts,
            'incorrect_marginal_iid_success': false_iid_success},
        'keyed_recovery': {'intended': items, 'crash_replay_trace': trace,
            'naive_total': naive, 'keyed_total': sum(keyed.values()),
            'scope': 'Pure finite construction; no distributed exactly-once or external-action guarantee'},
        'selective_redraw': {'independent_null_pvalues': 3, 'per_draw_level': F(1, 20),
            'probability_any_significant': selected_significance,
            'scope': 'Assumed independent uniform null p-values, not behavior measured in the runtime'},
        'limits': ['All probabilities, payoffs and costs are stipulated.',
                   'No new runtime, platform, bank or production experiment.',
                   'Exact examples establish their finite laws only.']}


def serialize(value):
    if isinstance(value, F): return {'exact': str(value), 'decimal': float(value)}
    if isinstance(value, dict): return {k: serialize(v) for k,v in value.items()}
    if isinstance(value, (tuple, list)): return [serialize(v) for v in value]
    return value


if __name__ == '__main__':
    print(json.dumps(serialize(calculate()), indent=2))
