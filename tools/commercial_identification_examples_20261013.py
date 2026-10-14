#!/usr/bin/env python3
"""Exact project lending constructions, not vendor runtime or sampled evidence."""
from fractions import Fraction as F
from itertools import product
import json


def joint_world(rows):
    out = {(a, y): F(0) for a, y in product(range(2), repeat=2)}
    for a, y0, y1, weight in rows:
        out[a, y1 if a else y0] += weight
    assert sum(out.values()) == 1
    return out


def ate(rows):
    return sum((y1-y0)*weight for a, y0, y1, weight in rows)


def serialize(value):
    if isinstance(value, F):
        return {'exact': str(value), 'decimal': float(value)}
    if isinstance(value, dict):
        return {str(k): serialize(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [serialize(v) for v in value]
    return value


def main():
    # Hidden risk U affects offer A and repayment Y; offer has zero effect.
    hidden = [(u ^ v, u, u, F(1, 2) * (F(1, 4) if v else F(3, 4)))
              for u, v in product(range(2), repeat=2)]
    # A randomized offer changes repayment; exactly the same observed A,Y law.
    causal = [(a, int(w < 1), int(w < 3), F(1, 8))
              for a, w in product(range(2), range(4))]
    observed = joint_world(hidden)
    assert observed == joint_world(causal) == {(0, 0): F(3, 8), (0, 1): F(1, 8),
                                               (1, 0): F(1, 8), (1, 1): F(3, 8)}
    assert ate(hidden) == 0 and ate(causal) == F(1, 2)
    # Allocate each observed cell to either value of its missing potential outcome.
    # All admissible distributions are convex combinations of these vertices.
    bounds = []
    vertices = []
    for missing in product(range(2), repeat=4):
        rows = []
        for ((a, y), weight), unobserved in zip(observed.items(), missing):
            rows.append((a, unobserved if a else y, y if a else unobserved, weight))
        assert joint_world(rows) == observed
        bounds.append(ate(rows)); vertices.append(rows)
    lower, upper = min(bounds), max(bounds)
    # Separate missing-outcome algebra, not the vertex procedure.
    mu1 = (observed[1, 1], observed[1, 1] + sum(v for (a, y), v in observed.items() if a == 0))
    mu0 = (observed[0, 1], observed[0, 1] + sum(v for (a, y), v in observed.items() if a == 1))
    assert (lower, upper) == (mu1[0]-mu0[1], mu1[1]-mu0[0]) == (F(-1, 4), F(3, 4))
    assert min(ate(v) for v in vertices) == lower and max(ate(v) for v in vertices) == upper

    # Known front-door structure: U->A, U->Y, A->M->Y, no further arrows.
    joint = {}
    for u, a, m, y in product(range(2), repeat=4):
        pa = F(1, 4)+F(1, 2)*u
        pm = F(1, 5)+F(3, 5)*a
        py = F(1, 10)+F(2, 5)*m+F(2, 5)*u
        joint[u, a, m, y] = F(1, 2)*(pa if a else 1-pa)*(pm if m else 1-pm)*(py if y else 1-py)
    assert sum(joint.values()) == 1
    def prob(**conditions):
        indexes = {'u': 0, 'a': 1, 'm': 2, 'y': 3}
        return sum(p for key, p in joint.items() if all(key[indexes[k]] == v for k, v in conditions.items()))
    front = []
    intervention = []
    for a in range(2):
        front.append(sum(prob(m=m, a=a)/prob(a=a)
                         * sum(prob(y=1, m=m, a=b)/prob(m=m, a=b)*prob(a=b) for b in range(2))
                         for m in range(2)))
        # Independently sum the intervened structural law over U and M.
        pm = F(1, 5)+F(3, 5)*a
        intervention.append(sum(F(1, 2)*(pm if m else 1-pm)
                                *(F(1, 10)+F(2, 5)*m+F(2, 5)*u)
                                for u, m in product(range(2), repeat=2)))
    assert front == intervention == [F(19, 50), F(31, 50)]
    naive = prob(y=1, a=1)/prob(a=1)-prob(y=1, a=0)/prob(a=0)
    assert naive == F(11, 25) and front[1]-front[0] == F(6, 25)

    # Same complete interventional margins, different cross-world couplings.
    same = [(a, u, u, F(1, 4)) for a, u in product(range(2), repeat=2)]
    flip = [(a, u, 1-u, F(1, 4)) for a, u in product(range(2), repeat=2)]
    assert joint_world(same) == joint_world(flip)
    def individual(rows):
        denominator = sum(p for a, y0, y1, p in rows if a == 1 and y1 == 1)
        return sum(p for a, y0, y1, p in rows if a == 1 and y1 == 1 and y0 == 0)/denominator
    assert individual(same) == 0 and individual(flip) == 1
    for rows in [same, flip]:
        assert ate(rows) == 0
        assert sum(y0*p for a, y0, y1, p in rows) == sum(y1*p for a, y0, y1, p in rows) == F(1, 2)
    results = {
        'kind': 'project_exact_constructions', 'vendor_runtime_executed': False,
        'sampled_study': False, 'currency': 'USD hypothetical planning values',
        'observational_equivalence': {'observed_A_Y': observed, 'hidden_world_ate': ate(hidden),
                                      'causal_world_ate': ate(causal), 'all_four_observed_cells_positive': True},
        'partial_identification': {'mu1_bounds': mu1, 'mu0_bounds': mu0, 'ate_bounds': [lower, upper],
                                   'vertices_checked': len(vertices), 'bound_extremes_attained': True,
                                   'assumptions': 'Binary potential outcomes and consistency only; no exchangeability or monotonicity'},
        'frontdoor': {'interventional_means': intervention, 'observed_functional': front,
                     'identified_ate': front[1]-front[0], 'naive_difference': naive,
                     'assumptions': 'Specified structural graph, independent exogenous disturbances, positive observed law'},
        'cross_world': {'marginal_mu0': F(1, 2), 'marginal_mu1': F(1, 2), 'ate': F(0),
                        'individual_same': individual(same), 'individual_flip': individual(flip),
                        'benefit_probability_bounds': [F(0), F(1, 2)]},
        'planning_economics': {'value_per_repayment': 1000, 'cost_per_offer': 20,
                              'net_hidden_world': 1000*ate(hidden)-20,
                              'net_causal_world': 1000*ate(causal)-20,
                              'net_consistency_bounds': [1000*lower-20, 1000*upper-20],
                              'net_frontdoor_world': 1000*(front[1]-front[0])-20,
                              'measured_bank_roi': False}}
    print(json.dumps(serialize(results), indent=2))


if __name__ == '__main__':
    main()
