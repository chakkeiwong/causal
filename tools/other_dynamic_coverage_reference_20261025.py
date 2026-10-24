#!/usr/bin/env python3
"""Exact project-authored comparisons; no fetched source or package runs."""
from fractions import Fraction as F

def calculate():
    dates, y = [1, 3, 4], [10, 30, 40]
    positional_lag = [None, 10, 30]
    lag_difference_at_four = positional_lag[2] - positional_lag[1]
    calendar_second_lag = dict(zip(dates, y)).get(2)
    assert lag_difference_at_four == 20 and calendar_second_lag is None
    all_origins = list(range(3, 13))
    h0 = [t for t in all_origins if t != 5]
    h2 = [t for t in range(3, 11) if t+2 != 5]
    assert len(h0)==9 and len(h2)==7 and 3 in h0 and 3 not in h2
    diagonal = [F(1), F(1,10**10)]
    scaled = [10**4*x for x in diagonal]
    absolute = lambda v: sum(x >= F(1,10**8) for x in v)
    relative = lambda v: sum(x > F(1,10**9)*max(v) for x in v)
    assert [absolute(diagonal),absolute(scaled)] == [1,2]
    assert [relative(diagonal),relative(scaled)] == [1,1]
    # Unit-effect proxy column is not necessarily unit-shock covariance scale.
    sigma = [[F(1,4),F(0)],[F(0),F(1)]]
    unit_column = [F(1),F(0)]
    residual = [[sigma[i][j]-unit_column[i]*unit_column[j] for j in range(2)] for i in range(2)]
    assert residual[1][1]==1 and residual[0][1]==0
    # Selected completion has sqrt(1) in the remaining coordinate and zero cross term.
    impact = [[unit_column[0],F(0)],[unit_column[1],F(1)]]
    reconstructed = [[sum(impact[i][k]*impact[j][k] for k in range(2)) for j in range(2)] for i in range(2)]
    assert reconstructed[0][0]-sigma[0][0] == F(3,4)
    # Conditional update using one observed coordinate of a two-coordinate system.
    prior_variance, measurement_variance, observation = F(1),F(1),F(2)
    gain = prior_variance/(prior_variance+measurement_variance)
    posterior_mean, posterior_variance = gain*observation,(1-gain)*prior_variance
    assert posterior_mean==1 and posterior_variance==F(1,2)
    F_array=[F(7),F(11),F(17)]
    expected=F_array[1:]; offset=F_array[:2]
    assert expected==[11,17] and offset==[7,11]
    state_variance=F(1); missing_variances=[]
    for _ in range(2):
        state_variance=state_variance+F(1)
        missing_variances.append(state_variance)
    assert missing_variances==[2,3]
    cost=[F(27000,n) for n in [900,600,450]]
    assert cost==[30,45,60]
    def mat(a):return [[str(x) for x in row] for row in a]
    return dict(evidence_kind='project_authored_exact_arithmetic_not_native_execution',
      calendar=dict(dates=dates,values=y,positional_lag=positional_lag,adjacent_current_dates=[3,4],positional_lag_difference=20,calendar_second_lag=None,index_selected_second_lag=10),
      projection_samples=dict(horizon0_origins=h0,horizon2_origins=h2,counts=[len(h0),len(h2)],missing_outcome_date=5),
      rank_scaling=dict(diagonal=[str(x) for x in diagonal],scaled=[str(x) for x in scaled],absolute_counts=[absolute(diagonal),absolute(scaled)],relative_counts=[relative(diagonal),relative(scaled)]),
      proxy_scale=dict(reduced_covariance=mat(sigma),unit_effect_column=[str(x) for x in unit_column],selected_completion_covariance=mat(reconstructed),first_diagonal_mismatch='3/4'),
      partial_observation=dict(prior_mean='0',prior_variance='1',observed_coordinate=2,posterior_mean=str(posterior_mean),posterior_variance=str(posterior_variance),whole_row_skip_mean='0',whole_row_skip_variance='1'),
      forecast_indices=dict(last_observed_and_two_future_F=[str(x) for x in F_array],future_F=[str(x) for x in expected],one_step_earlier_F=[str(x) for x in offset]),
      missing_state=dict(initial_variance='1',process_variance='1',predicted_variances=[str(x) for x in missing_variances]),
      hypothetical_costs=dict(total_usd=27000,requests=[900,600,450],dollars_per_request=[str(x) for x in cost]),native_execution=False)

if __name__=='__main__':
    import json
    print(json.dumps(calculate(),indent=2))
