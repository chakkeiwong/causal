#!/usr/bin/env python3
"""Authored exact witnesses; never imports or executes acquired packages."""
from fractions import Fraction as F
import json


def calculate():
    sizes, means = [2, 8], [F(100), F(0)]
    group_mean = sum(means) / len(means)
    person_mean = sum(n * y for n, y in zip(sizes, means)) / sum(sizes)
    assert (group_mean, person_mean) == (50, 20)
    adjacency = [[0, 1, 0], [0, 0, 1], [0, 0, 0]]
    exposure = [1, 0, 0]
    outgoing = [sum(a * y for a, y in zip(row, exposure)) for row in adjacency]
    incoming = [sum(adjacency[j][i] * exposure[j] for j in range(3)) for i in range(3)]
    assert outgoing == [0, 0, 0] and incoming == [0, 1, 0]
    # A star's hub is excluded by a degree rule while leaves remain eligible:
    # keeping the hub's observed exposure differs from assigning all nodes.
    fixed_neighbor_outcome = F(10) * F(1)
    all_nodes_policy_outcome = F(10) * F(1, 4)
    # Two treated members, q=1/2, proposed independent allocation alpha=1/4.
    alpha, q, n = F(1, 4), F(1, 2), 2
    policy_mass, observed_mass = alpha ** n, q ** n
    ratio_integral = observed_mass / policy_mass
    weight = 1 / ratio_integral
    multiplied_weight = policy_mass / ratio_integral
    derivative = -n * (1 - q) * weight
    multiplied_derivative = -n * (1 - q) * multiplied_weight
    assert (weight, multiplied_weight, derivative, multiplied_derivative) == (F(1, 4), F(1, 64), -F(1, 4), -F(1, 64))
    omitted_fixed_denominator = F(10 + 30, 3)
    complete_case_mean = F(10 + 30, 2)
    stipulated_complete_mean = F(10 + 60 + 30, 3)
    assert len({omitted_fixed_denominator, complete_case_mean, stipulated_complete_mean}) == 3
    residuals = [F(1), F(-2), F(1)]
    path = [[1, 1, 0], [1, 1, 1], [0, 1, 1]]
    direct_variance = sum(z * z for z in residuals) / 9
    adjacency_quadratic = sum(path[i][j] * residuals[i] * residuals[j] for i in range(3) for j in range(3)) / 9
    assert direct_variance == F(2, 3) and adjacency_quadratic == -F(2, 9)
    cost, requests, usable = F(2400), 100, 60
    return dict(
        target=dict(equal_group=str(group_mean), equal_person=str(person_mean), unit='stipulated USD per member'),
        direction=dict(row_neighbors=outgoing, reversed_neighbors=incoming),
        degree_restriction=dict(fixed_excluded_neighbor=str(fixed_neighbor_outcome), all_nodes_policy=str(all_nodes_policy_outcome)),
        allocation=dict(policy_mass=str(policy_mass), observed_mass=str(observed_mass), ratio_integral=str(ratio_integral), correct_ratio=str(weight), duplicated_mass=str(multiplied_weight), derivative=str(derivative), duplicated_mass_derivative=str(multiplied_derivative)),
        missing_group=dict(fixed_denominator=str(omitted_fixed_denominator), conditional=str(complete_case_mean), stipulated_complete=str(stipulated_complete_mean)),
        uncertainty=dict(direct=str(direct_variance), adjacency_quadratic=str(adjacency_quadratic), interpretation='Algebraic witness only; not a claimed native run or a population-valid counterexample'),
        costs=dict(total=str(cost), submitted=requests, usable=usable, per_submitted=str(cost/requests), per_usable=str(cost/usable), currency='USD', observed_prices=False),
        native_execution=False)


if __name__ == '__main__':
    print(json.dumps(calculate(), indent=2))
