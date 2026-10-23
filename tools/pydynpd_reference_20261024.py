#!/usr/bin/env python3
"""Exact authored dynamic-panel witnesses; no package or downloaded code execution."""
from fractions import Fraction as F

def calculate():
    original = [(2, 30), (0, 10), (1, 20)]
    occupied = sorted(k for k, _ in original)
    positional = list(zip(occupied, [v for _, v in original]))
    keyed = sorted(original)
    assert positional != keyed
    # Invalid moment: y=beta*x+epsilon with beta=1, x=z=epsilon=U.
    u = [-1, 1]
    moment_true = sum(F(z*(2*z-z), 2) for z in u)
    moment_root = sum(F(z*(2*z-2*z), 2) for z in u)
    assert moment_true == 1 and moment_root == 0
    # Repeated regressor columns identify a sum, never its decomposition.
    solutions = [[F(0), F(1)], [F(1), F(0)], [F(1,2), F(1,2)]]
    assert all(a+b == 1 for a,b in solutions)
    selected_probability = 1-F(9,10)**20
    assert F(10)/(1-F(4,5))==50 and F(10)/(1-F(19,20))==200
    return dict(
        provenance='Authored finite laws and abstract matrix/index operations; not native tests',
        positional_alignment=dict(input=[list(x) for x in original], positional=[list(x) for x in positional], keyed=[list(x) for x in keyed]),
        time_grid=dict(observed_periods=[1,3,4], categorical_steps=[0,1,2], calendar_gaps=[2,1], equal_step_claim=False),
        invalid_moment=dict(true_beta=1, moment_at_true=str(moment_true), moment_root_beta=2, moment_at_root=str(moment_root), reason='z=x=epsilon=U, y=2U; orthogonality false'),
        rank=dict(regressors='x1=x2=z', identified_sum=1, observationally_equivalent_coefficients=[[str(a),str(b)] for a,b in solutions], unique_coefficients=False),
        instruments=dict(periods=6, lag2plus_per_equation=[1,2,3,4], uncollapsed_count=10, collapsed_lag_count=4, scope='One complete series, difference equations t3..6, no other instruments; count is not rank'),
        selection=dict(attempts=20, stipulated_invalid_candidate_pass_probability='1/10', independent_pass_events=True, any_pass_probability=str(selected_probability), any_pass_decimal=float(selected_probability), actual_test_power_claim=False),
        common_shock=dict(units=100, law='g_i=U for all i; U is a fair +/-1 shock', true_mean_variance=1, diagonal_only_expectation='1/100', ratio=100),
        long_run=dict(short_run_usd=10, persistence=['4/5','19/20'], long_run_usd=[50,200], requires='Stable scalar linear response with invariant beta; no generic policy value', interval_crossing_one='No bounded continuous plug-in image across pole at alpha=1'),
        cost=dict(attempts=20, stipulated_usd=100, diagnostic_survivors=8, accepted_artifacts=2, correct_refusals=4, usd_per_attempt='5', usd_per_survivor='25/2', usd_per_accepted='50', measured_prices=False),
    )

if __name__=='__main__':
    import json
    print(json.dumps(calculate(),indent=2))
