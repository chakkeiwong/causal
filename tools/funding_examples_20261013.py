#!/usr/bin/env python3
"""Exact generated funding examples; no fitted bank or package experiment."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-13/funding-journey'


def calculate():
    # Independent U~N(0,1), V~N(0,2); fitted-nuisance influence U+2V.
    variance_fixed, variance_joint = F(1), F(1) + 4 * F(2)
    assert variance_joint == 9
    # At n=400 and z=2 the corresponding mean half-widths are 1/10, 3/10.
    plug_in, joint = (F(19, 10), F(21, 10)), (F(17, 10), F(23, 10))
    rate_change, new_funding_spread = F(1, 4), F(15, 1000)
    legacy_balance, setup = F(2600000), F(500)
    repricing = legacy_balance * rate_change / 100
    slope = 1000000 * rate_change * new_funding_spread
    cost = repricing + setup
    profit = lambda beta: slope * beta - cost
    assert repricing == 6500 and cost == 7000 and slope == 3750
    assert tuple(map(profit, plug_in)) == (125, 875)
    assert tuple(map(profit, joint)) == (-625, 1625)
    # Four truth-known households, four independent Bernoulli inclusion states.
    truth = [F(0), F(2), F(4), F(6)]
    pi = [F(1), F(1), F(1, 2), F(1, 2)]
    population = sum(truth) / 4
    naive, ht = F(0), F(0)
    states = []
    for bits in product([0, 1], repeat=2):
        selected = [1, 1, *bits]
        raw = sum(x*s for x, s in zip(truth, selected)) / sum(selected)
        weighted = sum(x*s/p for x, s, p in zip(truth, selected, pi)) / 4
        naive += raw/4; ht += weighted/4
        states.append({'inclusion': selected, 'sample_mean': str(raw), 'HT_mean': str(weighted), 'probability': '1/4'})
    assert population == ht == 3 and naive == F(13, 6)
    duplicated = [F(0)]*4 + truth[1:]
    raw_duplicate = sum(duplicated) / len(duplicated)
    assert raw_duplicate == F(12, 7)
    return {
        'kind': 'project_generated_exact_algebra',
        'sampling': 'No Monte Carlo draw and no observed bank sample.',
        'nuisance': {'law': 'X_i=theta-2*eta0+U_i; eta_hat=eta0+mean(V); theta_hat=mean(X)+2*eta_hat. Independent U_i~N(0,1), V_i~N(0,2), independent across i.',
                    'influence': 'U_i+2*V_i', 'variance_if_nuisance_fixed': str(variance_fixed),
                    'variance_with_estimated_nuisance': str(variance_joint), 'n': 400,
                    'normal_critical': 2, 'fixed_nuisance_interval': list(map(str, plug_in)),
                    'joint_nuisance_interval': list(map(str, joint)),
                    'boundary': 'Known Gaussian toy variance, fixed denominator one. General learned/dependent nuisance validity is not established.'},
        'economics': {'rate_change_pp': str(rate_change), 'legacy_balance_USD': str(legacy_balance),
                      'new_funding_net_spread': str(new_funding_spread), 'repricing_USD': str(repricing),
                      'workflow_cost_USD': str(setup), 'total_cost_USD': str(cost),
                      'profit_function_USD': '3750*beta-7000', 'break_even_beta': str(cost/slope),
                      'fixed_nuisance_profit_set_USD': list(map(str, map(profit, plug_in))),
                      'joint_nuisance_profit_set_USD': list(map(str, map(profit, joint))),
                      'boundary': 'Scenario costs and twelve-month average balances; spread is net of interest on incremental retained funding. No measured ROI.'},
        'identity': {'true_household_values': list(map(str, truth)), 'duplicated_record_values': list(map(str, duplicated)),
                     'record_mean': str(raw_duplicate), 'known_household_mean': str(population),
                     'boundary': 'Without the true map, these same rows admit different populations; hashes and clocks do not resolve the map.'},
        'inclusion': {'pi': list(map(str, pi)), 'states': states, 'expected_sample_mean': str(naive),
                      'expected_HT_mean': str(ht), 'population_mean': str(population),
                      'boundary': 'True N and positive inclusion probabilities are stipulated. This is arithmetic on truth-known contributions, not recovery of unobserved causal outcomes from records.'}}


if __name__ == '__main__':
    BASE.mkdir(parents=True, exist_ok=True)
    p = BASE / 'exact-examples.json'
    assert not p.exists(), 'Preserve frozen exact examples'
    p.write_text(json.dumps(calculate(), indent=2) + '\n')
    print(json.dumps({'status': 'pass', 'inclusion_states': 4, 'profit_sets_USD': [[125, 875], [-625, 1625]]}))
