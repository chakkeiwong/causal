#!/usr/bin/env python3
"""Exact generated policy questions for the commercial comparison; no vendor run."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-16/commercial-policy'


def encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {key: encode(child) for key, child in value.items()}
    if isinstance(value, (list, tuple)):
        return [encode(child) for child in value]
    return value


def calculate():
    trajectories = []
    for a0, a1 in product([0, 1], repeat=2):
        b1 = F(9, 10) if a0 == 0 else F(1, 10)
        mass = F(1, 2) * (b1 if a1 else 1-b1)
        reward = F(20*a0 + 100*a1 - 120*a0*a1 - 5*(a0+a1))
        weight = F(a0 == 1) / F(1, 2) * F(a1 == 1) / b1
        trajectories.append({'actions': [a0, a1], 'history_state': a0,
                             'logger_second_action_probability': b1, 'logged_mass': mass,
                             'net_reward_USD': reward, 'target_11_weight': weight})
    assert sum(row['logged_mass'] for row in trajectories) == 1
    weighted = sum(row['logged_mass']*row['target_11_weight']*row['net_reward_USD'] for row in trajectories)
    conditional_last = sum(row['logged_mass']*F(row['actions'][1] == 1)/row['logger_second_action_probability']*
                           row['net_reward_USD'] for row in trajectories)
    marginal_last = sum(row['logged_mass']*F(row['actions'][1] == 1)/F(1, 2)*row['net_reward_USD'] for row in trajectories)
    # Independent intervention recursion: replace both actions, then evaluate the structural reward.
    reference = F(20+100-120-10)
    assert weighted == reference == -10 and conditional_last == F(85, 2) and marginal_last == F(169, 2)
    assert sum(row['logged_mass']*row['target_11_weight'] for row in trajectories) == 1
    second_moment = sum(row['logged_mass']*row['target_11_weight']**2 for row in trajectories)
    assert second_moment == 20
    contexts = [{'p': F(1, 2), 'logger_action1': F(9, 10), 'reward_action1': F(10)},
                {'p': F(1, 2), 'logger_action1': F(1, 10), 'reward_action1': F(100)}]
    target = sum(row['p']*row['reward_action1'] for row in contexts)
    matched = sum(row['p']*row['logger_action1']*row['reward_action1'] for row in contexts) / sum(row['p']*row['logger_action1'] for row in contexts)
    ipw = sum(row['p']*row['logger_action1']*row['reward_action1']/row['logger_action1'] for row in contexts)
    assert target == ipw == 55 and matched == 19
    selection = []
    for m in [1, 2, 8]:
        worlds = list(product([-4, 4], repeat=m))
        optimism = sum(F(max(world)) for world in worlds)/len(worlds)
        closed = 4*(1-F(1, 2)**(m-1))
        assert optimism == closed
        # Independent fresh mean-zero validation noise, regardless of chosen index.
        heldout = sum(F(noise) for _ in worlds for noise in [-4, 4])/(2*len(worlds))
        assert heldout == 0
        selection.append({'candidates': m, 'true_values': [0]*m, 'estimated_optimum_mean': optimism,
                          'independent_validation_mean': heldout, 'world_count': len(worlds)})
    groups = [{'name': 'low_increment', 'mass': F(4, 5), 'baseline_recovery': F(9, 10), 'effect': F(1, 50)},
              {'name': 'high_increment', 'mass': F(1, 5), 'baseline_recovery': F(1, 10), 'effect': F(1, 5)}]
    for row in groups:
        row['treated_recovery'] = row['baseline_recovery'] + row['effect']
        row['incremental_net_USD'] = 100*row['effect'] - 5
    all_value = sum(row['mass']*row['incremental_net_USD'] for row in groups)
    high_value = groups[1]['mass']*groups[1]['incremental_net_USD']
    capacity = F(1, 10)
    optimal_capacity_value = capacity*groups[1]['incremental_net_USD']
    predictive_capacity_value = capacity*groups[0]['incremental_net_USD']
    assert all_value == F(3, 5) and high_value == 3
    assert optimal_capacity_value == F(3, 2) and predictive_capacity_value == -F(3, 10)
    return encode({'status': 'exact_authored_reference', 'evidence_class': 'generated laws and stipulated money; no vendor or bank results',
                   'trajectory': {'rows': trajectories, 'target_actions': [1, 1], 'target_value_USD': weighted,
                                  'conditional_last_action_only_USD': conditional_last, 'marginal_last_action_only_USD': marginal_last,
                                  'target_path_probability': F(1, 20), 'weight_second_moment': second_moment,
                                  'population_kish_fraction': F(1, 20), 'limit': 'Population weight ratio, not a finite-sample coverage guarantee'},
                   'matched_replay': {'contexts': contexts, 'target_value': target, 'matched_only_mean': matched, 'ipw_value': ipw,
                                      'limit': 'Illustration of matching alone under nonuniform logging, not a claim that Azure uses this incomplete estimator'},
                   'selection': selection,
                   'capacity': {'groups': groups, 'all_treated_incremental_value_per_customer_USD': all_value,
                                'high_group_only_incremental_value_per_customer_USD': high_value, 'capacity_fraction': capacity,
                                'effect_based_value_per_customer_USD': optimal_capacity_value, 'response_based_value_per_customer_USD': predictive_capacity_value},
                   'scope': 'Finite population arithmetic only. Hidden confounding, useful precision, vendor runtime and bank acceptance remain separate.'})


if __name__ == '__main__':
    out = BASE / 'exact-results.json'
    with out.open('x') as stream:
        json.dump(calculate(), stream, indent=2); stream.write('\n')
    print(json.dumps({'exact_reference_families': 4, 'status': 'pass', 'vendor_execution': False}))
