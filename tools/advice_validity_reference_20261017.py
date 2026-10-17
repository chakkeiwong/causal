#!/usr/bin/env python3
"""Independent exact examples for adviser models and published graph queries.

No upstream code, model, data set or network is imported or executed.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product
from math import comb


def serial(value):
    if isinstance(value, F):
        return dict(exact=str(value), decimal=float(value))
    if isinstance(value, dict):
        return {str(k): serial(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [serial(v) for v in value]
    return value


def subsets(values):
    values = sorted(values)
    return [frozenset(c) for size in range(len(values) + 1)
            for c in combinations(values, size)]


def paths(nodes, edges, start, end):
    adjacent = {n: set() for n in nodes}
    for a, b in edges:
        adjacent[a].add(b)
        adjacent[b].add(a)
    found = []

    def visit(path):
        if path[-1] == end:
            found.append(tuple(path))
            return
        for node in sorted(adjacent[path[-1]] - set(path)):
            visit(path + [node])

    visit([start])
    return found


def colliders(path, edges):
    return {path[i] for i in range(1, len(path) - 1)
            if (path[i-1], path[i]) in edges and (path[i+1], path[i]) in edges}


def ancestors(conditioned, edges):
    answer = set(conditioned)
    while True:
        enlarged = answer | {a for a, b in edges if b in answer}
        if enlarged == answer:
            return answer
        answer = enlarged


def active_paths(nodes, edges, start, end, conditioned):
    ancestor = ancestors(conditioned, edges)
    answer = []
    for path in paths(nodes, edges, start, end):
        collider = colliders(path, edges)
        noncollider = set(path[1:-1]) - collider
        if collider <= ancestor and not (noncollider & set(conditioned)):
            answer.append(path)
    return answer


def minimal_sets(candidates):
    return [z for z in candidates if not any(other < z for other in candidates)]


def published_hitting_sets(nodes, edges, start, end):
    """Finite specification of Algorithm 1 lines 4,9--15; not upstream code."""
    assert (start, end) not in edges and (end, start) not in edges
    free = [p for p in paths(nodes, edges, start, end) if not colliders(p, edges)]
    if not free:
        return free, [frozenset()]
    hits = [z for z in subsets(set(nodes) - {start, end})
            if all(set(p[1:-1]) & z for p in free)]
    return free, minimal_sets(hits)


def cov(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))


def posterior(graphs, advice, error):
    # Equal prior over the three legal noncollider chain DAGs.
    likelihood = [product_mass([1-error if o == e else error
                               for o, e in zip(graph, advice)]) for graph in graphs]
    normalizer = sum(likelihood, F(0))
    return [weight/normalizer for weight in likelihood]


def product_mass(masses):
    answer = F(1)
    for mass in masses:
        answer *= mass
    return answer


def calculate():
    graphs = [(1, 1), (0, 1), (0, 0)]  # A->B->C, A<-B->C, A<-B<-C.
    agreeing = posterior(graphs, (1, 1), F(1, 10))
    conflicting = posterior(graphs, (1, 0), F(1, 10))
    assert agreeing == [F(81, 91), F(9, 91), F(1, 91)]
    assert conflicting == [F(9, 19), F(1, 19), F(9, 19)]
    first = sum(p for graph, p in zip(graphs, agreeing) if graph[0] == 1)
    second = sum(p for graph, p in zip(graphs, agreeing) if graph[1] == 1)
    assert first == F(81, 91) < F(9, 10) < second == F(90, 91)
    # One latent noisy answer is repeated five times deterministically. Enumerate
    # the full graph/signal joint law rather than multiplying repeated evidence.
    joint = Counter()
    for truth, signal in product([0, 1], repeat=2):
        joint[(truth, (signal,)*5)] += F(1, 2)*(F(9, 10) if truth == signal else F(1, 10))
    event = (1,)*5
    repeated = joint[(1, event)] / sum(m for (g, e), m in joint.items() if e == event)
    spurious = F(9**5, 9**5+1)
    assert repeated == F(9, 10) and spurious == F(59049, 59050)

    # Independent standard Gaussian disturbances. These coefficient vectors give
    # exact population covariance; no Monte Carlo cancellation is involved.
    cancel = dict(X=[F(1), F(0), F(0)], A=[F(1), F(1), F(0)],
                  Y=[F(0), F(-1), F(1)])
    cancellation_cov = [[cov(cancel[a], cancel[b]) for b in cancel] for a in cancel]
    assert cancellation_cov == [[1, 1, 0], [1, 2, -1], [0, -1, 2]]
    # Lower-triangular disturbance map has determinant1, so covariance determinant1.
    assert cancellation_cov[0][0]*(4-1)-cancellation_cov[0][1]*(2-0) == 1
    assert cov(cancel['X'], cancel['Y']) == 0
    conditional_cancel = cov(cancel['X'], cancel['Y']) - (
        cov(cancel['X'], cancel['A'])*cov(cancel['A'], cancel['Y']) /
        cov(cancel['A'], cancel['A']))
    assert conditional_cancel == F(1, 2)

    nodes = {'X', 'B', 'C', 'Z', 'Y'}
    edges = {('X', 'C'), ('B', 'C'), ('C', 'Z'), ('X', 'Z'), ('Z', 'Y'), ('B', 'Y')}
    free, hitting = published_hitting_sets(nodes, edges, 'X', 'Y')
    assert hitting == [frozenset({'Z'})]
    opened = active_paths(nodes, edges, 'X', 'Y', {'Z'})
    assert set(opened) == {('X', 'C', 'B', 'Y'), ('X', 'Z', 'C', 'B', 'Y')}
    separators = [z for z in subsets(nodes-{'X', 'Y'})
                  if not active_paths(nodes, edges, 'X', 'Y', z)]
    assert minimal_sets(separators) == [frozenset({'B', 'Z'})]
    coeff = dict(X=[1, 0, 0, 0, 0], B=[0, 1, 0, 0, 0], C=[1, 1, 1, 0, 0],
                 Z=[2, 1, 1, 1, 0], Y=[2, 2, 1, 1, 1])
    sigma = {a: {b: F(cov(coeff[a], coeff[b])) for b in coeff} for a in coeff}
    conditional = sigma['X']['Y'] - sigma['X']['Z']*sigma['Z']['Y']/sigma['Z']['Z']
    assert (sigma['Z']['Z'], sigma['X']['Y'], sigma['X']['Z'], sigma['Z']['Y']) == (7, 2, 2, 8)
    assert conditional == F(-2, 7)

    # Randomized treatment X and independent flip V; Y=X xor V.
    law, means = Counter(), {0: F(0), 1: F(0)}
    for x, v in product([0, 1], repeat=2):
        mass = F(1, 2)*(F(3, 4) if v == 0 else F(1, 4))
        law[(x, x ^ v)] += mass
        means[x] += 2*mass*(x ^ v)
    assert dict(law) == {(0, 0): F(3, 8), (0, 1): F(1, 8),
                         (1, 1): F(3, 8), (1, 0): F(1, 8)}
    balanced_mass, balanced_count = F(0), 0
    for sample in product(sorted(law), repeat=4):
        if Counter(sample) == Counter({cell: 1 for cell in law}):
            balanced_mass += product_mass([law[cell] for cell in sample])
            balanced_count += 1
    assert balanced_count == 24 and balanced_mass == F(27, 512)
    null_mass = {a: F(comb(2, a)*comb(2, 2-a), comb(4, 2)) for a in range(3)}
    fisher_p = sum(m for m in null_mass.values() if m <= null_mass[1])
    assert fisher_p == 1 and means[1]-means[0] == F(1, 2)
    incremental_usd = 100*(means[1]-means[0])-30
    assert incremental_usd == 20
    answered, contradicted, total = 30, 20, 100
    answer_rate, conditional_rate = F(answered, total), F(contradicted, answered)
    full_range = [answer_rate*conditional_rate, answer_rate*conditional_rate+1-answer_rate]
    assert full_range == [F(1, 5), F(9, 10)]
    return dict(
        evidence_kind='Project-authored exact mathematical references; not upstream execution or bank data',
        three_dag_advice=dict(graph_order=graphs, error=F(1, 10),
            agreeing_posterior=agreeing, conflicting_posterior=conflicting,
            first_edge_mass=first, second_edge_mass=second),
        repeated_advice=dict(repetitions=5, correct_joint_posterior=repeated,
            falsely_factorized_posterior=spurious),
        markov_cancellation=dict(structural_equations=['X=eX', 'A=X+eA', 'Y=X-A+eY'],
            covariance=cancellation_cov, covariance_determinant=1,
            cov_XY=F(0), cov_XY_given_A=conditional_cancel),
        false_separator=dict(edges=sorted(edges), all_simple_paths=paths(nodes, edges, 'X', 'Y'),
            collider_free_paths=free, published_minimal_hitting_sets=[sorted(z) for z in hitting],
            active_paths_given_Z=opened, true_minimal_d_separators=[sorted(z) for z in minimal_sets(separators)],
            structural_equations=['X=eX', 'B=eB', 'C=X+B+eC', 'Z=X+C+eZ', 'Y=Z+B+eY'],
            covariance=sigma, cov_XY_given_Z=conditional),
        nonsignificance=dict(population_law=dict(law), conditional_means=means,
            population_randomized_effect=means[1]-means[0], sample_sequences=4**4,
            balanced_sequences=balanced_count, balanced_sample_probability=balanced_mass,
            fisher_null_mass=null_mass, balanced_fisher_two_sided_p=fisher_p,
            stipulated_incremental_usd=incremental_usd),
        selective_evidence=dict(total=total, answered=answered, contradicted=contradicted,
            answer_rate=answer_rate, conditional_inconsistency=conditional_rate,
            full_query_inconsistency_range=full_range))


if __name__ == '__main__':
    import json
    print(json.dumps(serial(calculate()), indent=2))
