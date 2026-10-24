#!/usr/bin/env python3
"""Project-authored exact witnesses; no upstream package is imported or run."""
from fractions import Fraction as F

def calculate():
    labels = [2000, 2002, 2003]
    values = [10, 20, 30]
    lookup = dict(zip(labels, values))
    calendar = [lookup.get(t - 1) for t in labels]
    positional = [None] + values[:-1]
    assert calendar == [None, None, 20] and positional == [None, 10, 20]
    keys, incoming = [1, 0, 3, 2], [20, 10, 40, 30]
    correct = [dict(zip(keys, incoming))[k] for k in range(4)]
    mask_assignment = incoming.copy()
    assert correct == [10, 20, 30, 40] and correct != mask_assignment
    old = [10, 20, 7, 8, 1]
    new_y = [11, 21]
    native_expression = new_y + old[2:]
    shifted = new_y + old[:2] + [old[-1]]
    assert native_expression == [11, 21, 7, 8, 1]
    assert shifted == [11, 21, 10, 20, 1]
    frozen, changing = F(1, 2) ** 2, F(1, 2) * F(3, 4)
    cond_mean, cond_variance = F(1, 2) * 2, 1 - F(1, 2) ** 2
    innovation, horizon_two = F(1), 1 + F(1, 2) ** 2
    initial, process, observation = F(1), F(1), F(4)
    missing = [initial + process, initial + 2 * process]
    assert frozen == F(1, 4) and changing == F(3, 8)
    assert cond_mean == 1 and cond_variance == F(3, 4)
    assert horizon_two == F(5, 4) and missing == [2, 3]
    tolerance = F(1, 10**12)
    residual, variance = F(1), tolerance / 2
    assert not variance > tolerance and residual * residual / variance == 2 * 10**12
    # J is its own Gram structure; J/4 is its Moore-Penrose inverse.
    J = [[F(1), F(1)], [F(1), F(1)]]
    Jplus = [[F(1, 4), F(1, 4)], [F(1, 4), F(1, 4)]]
    def mm(a, b):
        return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
    assert mm(mm(J, Jplus), J) == J
    assert J[0][0]*J[1][1]-J[0][1]*J[1][0] == 0
    def strings(rows):
        return [[str(v) for v in row] for row in rows]
    costs = [F(24000, n) for n in [800, 600, 400]]
    assert costs == [30, 40, 60]
    return dict(
        evidence_kind='project_authored_exact_arithmetic_not_native_execution',
        calendar=dict(labels=labels, values=values, positional_lag=positional, calendar_lag=calendar),
        panel_alignment=dict(input_keys=keys, values=incoming, mask_assignment=mask_assignment, key_aligned=correct),
        repeated_moments=dict(matrix=strings(J), pseudoinverse=strings(Jplus), rank=1, raw_columns=2),
        recursive_regressors=dict(prior=old, next_observation=new_y, selected_expression=native_expression, lag_shift=shifted),
        tvp_response=dict(frozen=str(frozen), changing=str(changing)),
        conditioning=dict(mean=str(cond_mean), variance=str(cond_variance), common_cause_intervention_mean='0', common_cause_intervention_variance='1'),
        uncertainty=dict(innovation_variance=str(innovation), horizon_two_variance=str(horizon_two), missing_step_variances=[str(v) for v in missing], state_variance='1', response_variance=str(initial+observation)),
        small_variance=dict(tolerance=str(tolerance), variance=str(variance), residual_quadratic=str(residual*residual/variance), selected_update_predicate=False),
        singular_psd=dict(matrix=strings(J), determinant='0', positive_diagonal=True, zero_diagonal_special_case=False),
        hypothetical_costs=dict(total_usd=24000, requests=[800,600,400], dollars_per_request=[str(v) for v in costs]),
        native_execution=False)

if __name__ == '__main__':
    import json
    print(json.dumps(calculate(), indent=2))
