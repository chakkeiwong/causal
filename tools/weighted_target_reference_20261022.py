#!/usr/bin/env python3
"""Exact authored banking geometry and analytic wrong-target normal coverage."""
from fractions import Fraction as F
from math import sqrt
from statistics import NormalDist


def calculate():
    theta = (F(6), F(-2))
    baseline, alternative, cost = (F(3, 4), F(1, 4)), (F(1, 4), F(3, 4)), F(1)
    dot = lambda x, y: sum(a*b for a, b in zip(x, y))
    effect, other = dot(baseline, theta), dot(alternative, theta)
    mean = sum(theta)/2
    h2 = sum((t-mean)**2 for t in theta)
    distance2 = sum((a-b)**2 for a, b in zip(alternative, baseline))
    assert (effect, other, h2, distance2) == (4, 0, 32, F(1, 2))
    assert h2*distance2 == (other-effect)**2 == 16
    epsilon = F(2, 3)
    left, right = (1-epsilon)*baseline[0], (1-epsilon)*baseline[0]+epsilon
    center = (left+right)/2
    center_effect = -2+8*center
    effect_radius = 8*(right-left)/2
    assert (left, right, center, center_effect, effect_radius) == (F(1,4), F(11,12), F(7,12), F(8,3), F(8,3))
    variance = dot(baseline, baseline)  # stipulated known Sigma=I
    sd = sqrt(variance)
    normal = NormalDist()
    z = normal.inv_cdf(.975)
    shift = float(effect-other)/sd
    coverage = normal.cdf(z-shift)-normal.cdf(-z-shift)
    assert abs((normal.cdf(z)-normal.cdf(-z))-.95) < 1e-12
    assert 0 < coverage < .002
    default_alpha, default_beta = F(1,20), F(1,20)
    alpha, beta = F(1,80), F(1,40)
    assert 1-2*alpha-beta == F(19,20)
    return dict(
        status='authored_exact_reference_not_native_or_bank_evidence',
        theta=list(map(str,theta)), baseline_weights=list(map(str,baseline)),
        alternative_weights=list(map(str,alternative)), contribution_units='stipulated USD per customer',
        baseline_effect=str(effect), alternative_effect=str(other), cost=str(cost),
        baseline_net=str(effect-cost), alternative_net=str(other-cost),
        ambiguity=dict(class_definition='Lambda_e=(1-e)w+e Delta_2, 0<=e<=1',
            effect_bounds=['4-6e','4+2e'], net_bounds=['3-6e','3+2e'],
            strictly_positive_worst_case_net='e<1/2', alternative_first_included_at='2/3',
            at_two_thirds=dict(first_coordinate_bounds=list(map(str,[left,right])),
                minimax_center=str(center), center_effect=str(center_effect), effect_radius=str(effect_radius))),
        known_covariance_geometry=dict(Sigma=[[1,0],[0,1]], H_squared=str(h2), distance_squared=str(distance2),
            squared_product=str(h2*distance2), squared_effect_difference=str((other-effect)**2)),
        wrong_target_interval=dict(model='theta_hat~N(theta,I); fixed w and lambda; baseline equal-tail 95% interval',
            baseline_variance=str(variance), baseline_sd=sd, z=z, standardized_target_shift=shift,
            coverage_formula='Phi(z-shift)-Phi(-z-shift)', wrong_target_coverage=coverage,
            percent=100*coverage, baseline_coverage=.95,
            qualification='Analytic normal probability; not Monte Carlo, causal identification or a replication of robust CI'),
        source_coverage_budgets=dict(default_alpha=str(default_alpha),default_beta=str(default_beta),
            uniform_fixed_target=str(1-default_alpha-default_beta),
            simultaneous_two_sided=str(1-2*default_alpha-default_beta),
            example_alpha=str(alpha),example_beta=str(beta),example_simultaneous_two_sided=str(1-2*alpha-beta)),
        limitations=['Group effects and covariance are stipulated; no observed bank population or estimated covariance.',
            'Geometry is oracle sensitivity, not a feasible heterogeneity upper bound or folded-normal interval implementation.',
            'The source theorem assumptions, fixed targets/classes and actual coverage type must be checked separately.'])


if __name__ == '__main__':
    import json
    print(json.dumps(calculate(),indent=2))
