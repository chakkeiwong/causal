#!/usr/bin/env python3
"""Independent exact examples for mathematical interchange; no random study."""
from fractions import Fraction as F
import json
from math import sqrt


def matmul(a, b):
    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def transpose(a):
    return list(map(list, zip(*a)))


def affine_set(intervals, scale, shift):
    assert scale != 0
    result = []
    for lo, hi in intervals:
        mapped = [None if x is None else scale * F(x) + shift for x in (lo, hi)]
        if scale < 0:
            mapped.reverse()
        result.append(mapped)
    return sorted(result, key=lambda p: (p[0] is not None, p[0] or F(0)))


def main():
    masses, effects, balances = [F(3, 4), F(1, 4)], [F(20), F(-40)], [F(1), F(9)]
    customer = sum(p * t for p, t in zip(masses, effects))
    balance = sum(p * b * t for p, b, t in zip(masses, balances, effects)) / sum(
        p * b for p, b in zip(masses, balances))
    assert customer == 5 and balance == -25

    # Exact invertible coordinate conversion: dollars -> thousands, offer -> loss.
    l = [[F(1, 1000), F(0)], [F(0), F(-1)]]
    covariance = [[F(40000), F(20)], [F(20), F(1, 4)]]
    transformed = matmul(matmul(l, covariance), transpose(l))
    assert transformed == [[F(1, 25), F(-1, 50)], [F(-1, 50), F(1, 4)]]
    assert covariance[0][0] * covariance[1][1] - covariance[0][1] ** 2 == 9600

    theta = [[None, -2], [3, None]]
    value = affine_set(theta, F(100), F(-300))
    loss = affine_set(value, F(-1), F(0))
    assert value == [[None, F(-500)], [F(0), None]]
    assert loss == [[None, F(0)], [F(500), None]]
    assert affine_set(value, F(1, 100), F(3)) == theta

    # Marginal 95% coverage does not give joint 95% without construction.
    joint_if_independent = F(19, 20) ** 2
    joint_union_bound = 1 - 2 * F(1, 20)
    shared_variance = F(9, 100) + F(1, 10000)
    independent_row_variance = F(109, 100) / 10000
    assert joint_if_independent == F(361, 400)
    assert shared_variance / independent_row_variance == F(90100, 109)

    # Convex hull loss for a nonlinear monetary map: V(theta)=100(theta^2-1).
    # theta in [-3,-2] union [2,3] has V in [300,800]; the hull gives [-100,800].
    nonlinear_true = [100 * (F(2) ** 2 - 1), 100 * (F(3) ** 2 - 1)]
    nonlinear_hull = [F(-100), nonlinear_true[1]]
    assert nonlinear_true == [300, 800]

    results = {
        "kind": "exact_project_derivations", "random_draws": 0,
        "population": {"customer_effect": customer, "balance_weighted_effect": balance},
        "rate_units": {"usd_per_basis_point": F(2) * 10**6 / 10000,
                       "usd_interval_per_basis_point": [F(100), F(300)]},
        "covariance": {"original": covariance, "map": l, "transformed": transformed},
        "sets": {"theta": theta, "value": value, "loss": loss,
                 "nonlinear_value": nonlinear_true, "nonlinear_value_of_hull": nonlinear_hull},
        "coverage": {"independent_joint_from_two_95": joint_if_independent,
                     "union_bound_from_two_95": joint_union_bound,
                     "three_component_lower_bound": 1 - F(2,100) - F(2,100) - F(1,100)},
        "common_calendar": {"mean_variance": shared_variance,
                            "false_iid_variance": independent_row_variance,
                            "variance_understatement_ratio": shared_variance / independent_row_variance,
                            "sd_ratio_approx": sqrt(float(shared_variance / independent_row_variance))},
        "ratio_inversion": {"inequality": "theta^2 >= 4; from mean(Y)=2, mean(X)=0, c=2, var(Y)=0, var(X)=1/4",
                            "set": [[None, -2], [2, None]], "point_ratio_defined": False},
        "decision_margin": {"statistical_lower_usd": 30, "numerical_error_usd": 40,
                            "certified_lower_usd": -10},
    }
    print(json.dumps(results, default=lambda x: str(x) if isinstance(x, F) else x, indent=2))


if __name__ == '__main__':
    main()
