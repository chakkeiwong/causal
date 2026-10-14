#!/usr/bin/env python3
"""Reproduce a declared illustrative investment/experiment calculation; no bank ROI."""
import json
from pathlib import Path


def calculate():
    rows = [
        {'scenario': 'high', 'prior': .4, 'gross_gain_per_task': 40, 'p_positive_signal': .8},
        {'scenario': 'moderate', 'prior': .4, 'gross_gain_per_task': 20, 'p_positive_signal': .5},
        {'scenario': 'adverse', 'prior': .2, 'gross_gain_per_task': -2, 'p_positive_signal': .1}]
    n, fixed, variable = 10000, 100000, 6
    for row in rows:
        row['incremental_net_value'] = n * (row['gross_gain_per_task'] - variable) - fixed
    prior_value = sum(r['prior'] * r['incremental_net_value'] for r in rows)
    signal_results = []
    for positive in (True, False):
        joint = [r['prior'] * (r['p_positive_signal'] if positive else 1-r['p_positive_signal']) for r in rows]
        probability = sum(joint)
        conditional_value = sum(w*r['incremental_net_value'] for w, r in zip(joint, rows)) / probability
        signal_results.append({'positive': positive, 'probability': probability,
                               'posterior_net_value': conditional_value, 'choose_build': conditional_value > 0})
    informed_value = sum(r['probability'] * max(0, r['posterior_net_value']) for r in signal_results)
    evsi = informed_value - max(0, prior_value)
    evpi = sum(r['prior'] * max(0, r['incremental_net_value']) for r in rows) - max(0, prior_value)
    assert abs(prior_value-76000) < 1e-8 and abs(evsi-5200) < 1e-8 and abs(evpi-36000) < 1e-8
    return {'kind': 'project_assumed_scenario_not_empirical_ROI', 'currency': 'illustrative USD',
            'horizon': 'one year, no discounting', 'tasks': n, 'fixed_incremental_cost': fixed,
            'variable_incremental_cost_per_attempted_task': variable, 'regimes': rows,
            'expected_incremental_value_without_experiment': prior_value, 'signal_results': signal_results,
            'expected_value_of_sample_information': evsi, 'expected_value_of_perfect_information': evpi,
            'net_information_value_at_cost_8000': evsi-8000, 'net_information_value_at_cost_3000': evsi-3000,
            'limits': ['Every payoff, prior, signal likelihood, task volume and price is assumed',
                       'No empirical bank benefit, calibration, transport or willingness to adopt is established',
                       'Nonmonetary unacceptable risk remains a separate constraint, not a bought-off loss']}


if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    target = root / 'docs/program/comprehensive-v14/work/ECON.DESIGN/illustration.json'
    target.parent.mkdir(parents=True, exist_ok=True)
    value = calculate()
    target.write_text(json.dumps(value, indent=2) + '\n')
    print(json.dumps({k: value[k] for k in ['expected_incremental_value_without_experiment',
        'expected_value_of_sample_information', 'net_information_value_at_cost_8000']}))
