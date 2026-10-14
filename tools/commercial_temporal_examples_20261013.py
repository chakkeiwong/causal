#!/usr/bin/env python3
"""Exact stipulated temporal funding examples; no vendor/runtime experiment."""
import argparse
import hashlib
import json
from pathlib import Path
import sympy as s

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / 'docs/program/execution/2026-10-13/commercial-temporal/exact-results.json'


def calculate():
    Q = s.Rational
    rho = Q(4, 5)
    conditional_covariance = 1 - rho**2 / 2
    conditional_variance = 2 - rho**2 / 2
    slope = conditional_covariance / conditional_variance
    old_mse = conditional_variance
    new_mse = old_mse - conditional_covariance**2 / conditional_variance
    # Direct covariance-system solution is separate from partialling algebra.
    predictors = s.Matrix([[2, rho], [rho, 2]])
    coefficients = predictors.inv() * s.Matrix([rho, 1])
    assert coefficients[1] == slope == Q(17, 42)
    assert new_mse == Q(59, 42)
    F = s.Matrix([[Q(1, 2), 0], [Q(1, 5), Q(1, 2)]])
    Sigma = s.Matrix([[1, Q(1, 2)], [Q(1, 2), 1]])
    first = s.Matrix([[1, 0], [-Q(1, 2), 1]])
    second = s.Matrix([[1, -Q(1, 2)], [0, 1]])
    independent1 = first * Sigma * first.T
    independent2 = second * Sigma * second.T
    assert independent1 == s.diag(1, Q(3, 4))
    assert independent2 == s.diag(Q(3, 4), 1)
    assert first.inv() * independent1 * first.inv().T == Sigma
    assert second.inv() * independent2 * second.inv().T == Sigma
    delta = Q(1, 4)
    impact1, impact2 = s.Matrix([delta, delta/2]), s.Matrix([delta, 0])
    paths1, paths2 = [], []
    recursive1, recursive2 = impact1, impact2
    for h in range(7):
        one, two = F**h * impact1, F**h * impact2
        assert one == recursive1 and two == recursive2
        paths1.append(one[1]); paths2.append(two[1])
        recursive1, recursive2 = F * recursive1, F * recursive2
    margin = Q(1, 500)  # monthly net margin per balance dollar, an assumption
    cost = s.Integer(500)
    values = [s.Integer(1000000)*margin*sum(p[:3])-cost for p in [paths1, paths2]]
    assert values == [Q(275, 2), s.Integer(-300)]
    quarter = F**3
    assert quarter[1, 0] == Q(3, 20)
    innovation_quarter = sum((F**i * Sigma * (F.T)**i for i in range(3)), s.zeros(2))
    # Joint three-shock block covariance gives the same aggregation covariance.
    transform = (F**2).row_join(F).row_join(s.eye(2))
    assert transform * s.diag(Sigma, Sigma, Sigma) * transform.T == innovation_quarter
    common_variance = Q(1, 2)
    branches = 20
    proper = common_variance + (1-common_variance)/branches
    naive = Q(1, branches)
    assert proper/naive == Q(21, 2)
    fmt = lambda x: str(x)
    matrix = lambda a: [[str(a[i,j]) for j in range(a.cols)] for i in range(a.rows)]
    return {'scope': 'Exact project-owned hypothetical mechanisms and monetary assumptions; zero random draws and zero vendor executions.',
        'predictive_common_factor': {'rho': fmt(rho), 'stationary_factor_variance': '1',
            'factor_innovation_variance': '9/25', 'measurement_noise_variances': ['1','1'],
            'conditional_covariance': fmt(conditional_covariance),
            'conditional_variance': fmt(conditional_variance), 'predictive_rate_coefficient': fmt(slope),
            'mse_without_rate': fmt(old_mse), 'mse_with_rate': fmt(new_mse),
            'mse_reduction': fmt(old_mse-new_mse), 'quarter_pp_predicted_balance_million': fmt(delta*slope),
            'surgical_rate_effect': '0'},
        'equivalent_dynamic_models': {'reduced_transition': matrix(F), 'innovation_covariance': matrix(Sigma),
            'rate_first_structural_matrix': matrix(first), 'balance_first_structural_matrix': matrix(second),
            'rate_first_structural_lags': matrix(first*F), 'balance_first_structural_lags': matrix(second*F),
            'rate_first_noise_covariance': matrix(independent1), 'balance_first_noise_covariance': matrix(independent2),
            'intervention_pp': fmt(delta), 'balance_response_million_rate_first': list(map(fmt,paths1)),
            'balance_response_million_balance_first': list(map(fmt,paths2)),
            'horizons_for_value': [0,1,2], 'monthly_margin': fmt(margin), 'assumed_total_cost_usd': fmt(cost),
            'net_values_usd': list(map(fmt,values)), 'value_difference_usd': fmt(values[0]-values[1])},
        'sampling_frequency': {'endpoint_quarterly_transition': matrix(quarter),
            'endpoint_quarterly_innovation_covariance': matrix(innovation_quarter),
            'monthly_cross_lag': '1/5', 'quarterly_cross_lag': fmt(quarter[1,0]),
            'limit': 'Quarter-end stock sampling, not within-quarter totals or an unrestricted aggregation theorem.'},
        'common_calendar': {'branches': branches, 'common_shock_variance': fmt(common_variance),
            'variance_of_branch_average': fmt(proper), 'false_independence_variance': fmt(naive),
            'variance_ratio': fmt(proper/naive), 'standard_error_ratio': fmt(s.sqrt(proper/naive)),
            'limit': 'A stipulated shared-shock law; not an estimated bank correlation or universal correction.'},
        'checks': ['Partial covariance agrees with direct regression-system algebra',
            'Both independent structural noise laws recover the same reduced innovation covariance',
            'Matrix-power and direct-recursion impulse paths agree',
            'Three-month financial values follow the stated unit conversion and costs',
            'Block covariance and innovation recursion agree for quarterly endpoints'],
        'code_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--output', type=Path, default=DEFAULT)
    args = p.parse_args(); assert not args.output.exists(), 'Preserve earlier results'
    result = calculate(); args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'status':'pass','checks':len(result['checks']),
                      'net_values_usd':result['equivalent_dynamic_models']['net_values_usd'],
                      'new_random_draws':0,'vendor_executions':0}))
