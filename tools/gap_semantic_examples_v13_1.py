#!/usr/bin/env python3
"""Exact project examples for source-grounded semantic comparisons.

No vendor module is imported. These are stipulated examples, not package tests,
empirical calibration, bank validation or economic evidence.
"""
import json
from fractions import Fraction as F
from math import pi, sqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'docs/program/gap-execution-v13_1/semantic-examples.json'


def main():
    if OUT.exists():
        raise ValueError('Preserve existing evidence; use a successor for changes')
    # B[target, source]; sum the direct and mediated funding-to-balance paths.
    b10, b21, b20 = F(2, 5), F(2), F(1, 10)
    total = b20 + b21*b10
    direct_intervention_response = b20 + b21*(b10*1)
    assert total == direct_intervention_response == F(9, 10)
    # Two independent clusters of two equal contributions, uncorrected meat.
    scores = [(F(1), F(1)), (F(-1), F(-1))]
    row_meat = sum(x*x for group in scores for x in group)
    cluster_meat = sum(sum(group)**2 for group in scores)
    assert (row_meat, cluster_meat) == (4, 8)
    design_effect = 1 + (10-1)*F(3, 10)
    # Competing event occurs before outcome in each stipulated discrete interval.
    event = [F(1, 10), F(1, 5)]
    competing = [F(1, 20), F(1, 10)]
    alive, risks = F(1), []
    for d, y in zip(competing, event):
        risks.append(alive*(1-d)*y)
        alive *= (1-d)*(1-y)
    risk = sum(risks)
    independent_enumeration = (1-competing[0])*event[0] + (1-competing[0])*(1-event[0])*(1-competing[1])*event[1]
    assert risk == independent_enumeration == F(2489, 10000)
    no_competing = 1-(1-event[0])*(1-event[1])
    # Change of variables f_A(a|x)=f_R((a-mu)/s|x)/s, s>0.
    phi0 = 1/sqrt(2*pi)
    densities = [phi0, phi0/2]
    assert densities[0] == 2*densities[1]
    # An observed-history IV orthogonal-score remainder identity in two strata.
    errors = [(F(1, 10), F(1, 5), F(1, 20)),
              (F(-1, 10), F(1, 10), F(-1, 20))]
    theta = F(2)
    remainder = sum(dm*(dl-theta*dr) for dm, dl, dr in errors)/2
    assert remainder == F(-1, 200)
    result = {
        'scope': 'Stipulated project derivations; no package code, random final study, bank observations or ROI',
        'orientation': {'convention': 'B[target,source]', 'total_effect': float(total), 'transposed_graph_effect': 0},
        'cluster_covariance': {'row_meat': int(row_meat), 'cluster_meat': int(cluster_meat),
            'row_mean_variance_without_correction': float(row_meat/16),
            'cluster_mean_variance_without_correction': float(cluster_meat/16),
            'stipulated_m': 10, 'stipulated_rho': .3, 'design_effect': float(design_effect),
            'equivalent_independent_n_for_1000_records': float(1000/design_effect)},
        'competing_event': {'order': 'competing event before outcome within each period',
            'period_risks': [float(x) for x in risks], 'two_period_risk': float(risk),
            'risk_without_competing_event': float(no_competing),
            'stipulated_loss_difference_cny_10000_accounts_100_per_event': float((no_competing-risk)*10000*100)},
        'density_scale': {'standardized_residual_density_at_zero': phi0,
            'original_scale_densities_s1_s2': densities,
            'under_exposure_unit_multiplier_100': [x/100 for x in densities]},
        'orthogonal_score': {'theta': float(theta), 'exact_conditional_remainder': float(remainder),
            'scope': 'Finite arithmetic for independently trained nuisances in a specified identified score, not a learner-rate proof'},
        'checks': 'Five exact identities or analytic comparisons passed'}
    OUT.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
