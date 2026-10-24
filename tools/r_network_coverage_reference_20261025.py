#!/usr/bin/env python3
"""Project-authored exact network witnesses; never import acquired code."""
from fractions import Fraction as F
from itertools import product

def calculate():
    A = [[0, 1], [1, 0]]
    z = [1, 0]
    closed_counts = [sum(z[j] for j in range(2) if i == j or A[i][j]) for i in range(2)]
    selected_control = [x < 2 for x in closed_counts]
    true_all_control = [x == 0 for x in closed_counts]
    assert selected_control == [True, True] and true_all_control == [False, False]
    smoothed = [F(2, 5)] * 4
    assert sum(smoothed) == F(8, 5)
    p_i, p_j = F(1, 5), F(4, 5)
    own_zero_neighbor_one = (1-p_i)*p_j
    selected_marginal = (1-p_i)*p_i
    assert own_zero_neighbor_one == F(16, 25) and selected_marginal == F(4, 25)
    assignments = list(product([0, 1], repeat=2))
    exact_joint = sum(F(1, 4) for a in assignments if a[0] and a[1])
    selected_joint = F(1, 2)**4
    assert exact_joint == F(1, 4) and selected_joint == F(1, 16)
    asymmetric = [[0, 1], [0, 0]]
    symmetry_guard = sum(asymmetric[i][j] != asymmetric[j][i] for i in range(2) for j in range(2))
    assert symmetry_guard == 2 and asymmetric[0][1] != asymmetric[1][0]
    K = [[1, 1, 0], [1, 1, 1], [0, 1, 1]]
    v = [F(1), F(-2), F(1)]
    hac = sum(v[i]*K[i][j]*v[j] for i in range(3) for j in range(3))/9
    assert sum(v)==0 and hac == F(-2, 9)
    tol, eps, u = F(1, 10**14), F(1, 10**15), F(3, 4)
    draws = [eps, eps, F(1)]
    tied = sum(abs(t) < tol for t in draws)
    larger = sum(t > 0 for t in draws)
    pvalue = (larger + u*(1+tied))/(len(draws)+1)
    two_sided = 2*min(pvalue, 1-pvalue)
    assert sum(abs(t) for t in draws)/4 > tol
    assert pvalue == F(21, 16) and two_sided == F(-5, 8)
    # Compare a one-edge candidate against an isolated-node candidate.
    common_exposure = []
    for a in assignments:
        edge_map = (a[0], int(a[1] > 0))
        isolated_map = (a[0], 0)
        if edge_map == isolated_map == (0, 1):
            common_exposure.append(a)
    assert not common_exposure
    group_contributions = [F(2), None, F(8)]
    observed = [x for x in group_contributions if x is not None]
    available_mean = sum(observed)/len(observed)
    fixed_denominator_value = sum(observed)/len(group_contributions)
    assert available_mean == 5 and fixed_denominator_value == F(10, 3)
    support = 6
    expected_draws_full_collection = support*sum(F(1, j) for j in range(1, support+1))
    assert expected_draws_full_collection == F(147, 10)
    costs = [F(30000, n) for n in [1000, 600, 400]]
    assert costs == [30, 50, 75]
    return dict(evidence_kind='project_authored_exact_arithmetic_not_native_execution',
      closed_neighborhood=dict(treatment=z,selected_all_control=selected_control,actual_all_control=true_all_control),
      smoothed_probabilities=dict(exhaustive_draws=4,counts=[1]*4,marginals=[str(x) for x in smoothed],sum=str(sum(smoothed)),exact_marginal='1/4'),
      heterogeneous_assignment=dict(probabilities=['1/5','4/5'],exact_exposure=str(own_zero_neighbor_one),selected_expression=str(selected_marginal)),
      adjacent_joint=dict(exact=str(exact_joint),selected_expression=str(selected_joint),shared_neighbors=0),
      asymmetric_guard=dict(matrix=asymmetric,unequal_transpose_entries=symmetry_guard,actually_symmetric=False),
      graph_hac=dict(kernel=K,centered_score=[str(x) for x in v],quadratic_divided_by_n_squared=str(hac)),
      randomized_tail=dict(tolerance=str(tol),draws=[str(x) for x in draws],u=str(u),ties=tied,strictly_larger=larger,degenerate_branch=False,pvalue=str(pvalue),two_sided=str(two_sided)),
      common_graph_exposure=dict(exact_probability='0',smoothing_at_R9='1/10',admissible=False),
      group_denominator=dict(contributions=['2',None,'8'],available_mean=str(available_mean),fixed_denominator_arithmetic=str(fixed_denominator_value),missing_group_truth='unknown'),
      full_assignment_sampling=dict(distinct_vectors=6,expected_uniform_draws=str(expected_draws_full_collection),deterministic_iteration_bound=False),
      hypothetical_costs=dict(total_usd=30000,denominators=[1000,600,400],per_request=[str(x) for x in costs]),native_execution=False)

if __name__ == '__main__':
    import json
    print(json.dumps(calculate(), indent=2))
