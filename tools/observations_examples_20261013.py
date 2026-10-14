#!/usr/bin/env python3
"""Exact authored observation laws and decision scenarios, independent of the service."""
import argparse
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


def calculate():
    laws = {
        'independent': {(a, b): F(1, 4) for a, b in product(range(2), repeat=2)},
        'shared': {(0, 0): F(1, 2), (1, 1): F(1, 2)}}
    selection = {}
    for name, law in laws.items():
        values = {r: 20*r[0]+80*r[1] for r in law}
        mean = sum(law[r]*values[r] for r in law)
        variance = sum(law[r]*(values[r]-mean)**2 for r in law)
        assert mean == 50
        assert [sum(m*r[i] for r, m in law.items()) for i in range(2)] == [F(1, 2)]*2
        selection[name] = {'mean': str(mean), 'variance': str(variance),
                           'joint_inclusion': str(sum(m*r[0]*r[1] for r, m in law.items()))}
    assert selection['independent']['variance'] == '1700'
    assert selection['shared']['variance'] == '2500'
    worlds = [(F(9, 10), F(1, 10), F(3, 10)), (F(1, 2), F(1, 10), F(3, 5))]
    noisy = []
    for s, f, p in worlds:
        joint = {(z, b): (p if z else 1-p) *
                 ((s if z else f) if b else 1-(s if z else f))
                 for z, b in product(range(2), repeat=2)}
        q = sum(v for (z, b), v in joint.items() if b)
        assert q == F(17, 50) and min(joint.values()) > 0
        assert (q-f)/(s-f) == p
        noisy.append({'sensitivity': str(s), 'false_positive': str(f), 'prevalence': str(p),
                      'reported_positive': str(q), 'stipulated_action_value_USD': str(500*p-200)})
    p = F(3, 10); d = F(4, 5)
    # Independent unit-variance X,Y; psi_q=X, psi_s=-X+Y, psi_f=0.
    joint_variance = ((1+p)**2 + p**2)/d**2
    fixed_nuisance = 1/d**2
    assert joint_variance == F(89, 32) and fixed_nuisance == F(25, 16)
    roots = [F(1, 4), F(7, 20)]
    assert all(80*x*x-48*x+7 == 0 for x in roots)
    for p in [F(k, 100) for k in range(-20, 121)]:
        assert (80*p*p-48*p+7 <= 0) == (roots[0] <= p <= roots[1])
        assert (F(3, 10) <= F(1, 10)+F(4, 5)*p <= F(19, 50)) == (roots[0] <= p <= roots[1])
    return {'kind': 'authored_exact_observation_laws_and_conditional_decision_scenarios',
            'selection': selection,
            'zero_inclusion': {'observed_value': 20, 'unobserved_alternatives': [80, 120], 'population_means': [50, 70], 'observed_laws_equal': True},
            'link_maps': {'observed_records': [20, 80], 'bijective_contrasts': [60, -60], 'total_under_both': 100,
                          'limit': 'Two stipulated maps, not a probabilistic linkage model or causal effect.'},
            'noisy_label_worlds': noisy,
            'score': {'formula': '(psi_q-p*psi_s-(1-p)*psi_f)/(s-f)',
                      'illustration': 'Unit-variance independent X,Y with psi_q=X, psi_s=-X+Y, psi_f=0; separate from any asserted label sampling law.',
                      'joint_variance': str(joint_variance), 'fixed_nuisance_variance': str(fixed_nuisance)},
            'sensitivity': {'q_range': ['3/10', '19/50'], 'fixed_s': '9/10', 'fixed_f': '1/10',
                            'polynomial': [80, -48, 7], 'prevalence_interval': [str(x) for x in roots],
                            'value_interval_USD': [str(500*x-200) for x in roots], 'coverage': None,
                            'no_signal_prevalence_interval': ['0', '1'], 'no_signal_value_USD': [-200, 300]},
            'causal_efficacy': 'One-half prevention probability conditional on the event risk is a stipulated causal model, not identified by label prevalence.',
            'service_executed': False, 'random_draws': 0, 'bank_data': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    assert not args.output.exists(), 'Preserve exact references'
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(calculate(), indent=2)+'\n')
    print(json.dumps({'exact_examples': 'pass', 'service_executed': False}))
