#!/usr/bin/env python3
"""Authored exact references; never import or execute the acquired upstream code."""
from collections import Counter
from fractions import Fraction as F
from itertools import product
from math import comb


def serial(value):
    if isinstance(value, F):
        return dict(exact=str(value), decimal=float(value))
    if isinstance(value, dict):
        return {str(k): serial(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [serial(v) for v in value]
    return value


def outcome(world, u, v, intervention=None):
    x = u if world == 'A' else u ^ v
    if intervention is not None:
        x = intervention
    y = x ^ v if world == 'A' else u
    return x, y


def graph_metrics(truth, prediction):
    # Flattened ordered off-diagonal indicators, NOT an upstream graph object.
    tp = sum(t == p == 1 for t, p in zip(truth, prediction))
    fp = sum(t == 0 and p == 1 for t, p in zip(truth, prediction))
    fn = sum(t == 1 and p == 0 for t, p in zip(truth, prediction))
    return F(2 * tp, 2 * tp + fp + fn) if 2 * tp + fp + fn else F(0)


def deletion_reference(raw, directed, uncertain, answer):
    # Authored finite translation of the inspected recommendation/pair/guard
    # expressions. No model, parser, BackgroundKnowledge or later pruning runs.
    high = {(i, j) for i, j in product(range(2), repeat=2) if directed[i][j] >= F(9, 10)}
    low = {(i, j) for i, j in product(range(2), repeat=2) if directed[i][j] <= F(1, 10)}
    middle = low | {
        (i, j) for i, j in product(range(2), repeat=2)
        if F(1, 10) < directed[i][j] < F(9, 10)
        or uncertain[i][j] >= F(9, 10)
        or F(1, 10) < uncertain[i][j] < F(9, 10)
    }
    pairs = {tuple(sorted(pair)) for pair in middle}
    revised = [row[:] for row in raw]
    for i, j in high:
        if not raw[i][j]:
            revised[i][j], revised[j][i] = 1, 0
    for i, j in low:
        if raw[i][j]:
            revised[i][j] = revised[j][i] = 0
    fixed_pairs = []
    if (0, 1) in pairs and answer == 'C':
        j, i = 0, 1  # Accepted canonical pair maps to forbid_dict[(0,1)].
        if (revised[i][j] != 0 or revised[j][i] != 0) and (i, j) not in fixed_pairs:
            revised[i][j] = revised[j][i] = 0
    return dict(high=sorted(high), low=sorted(low), middle=sorted(middle),
                llm_pairs=sorted(pairs), after_llm=revised)


def calculate():
    noise = {0: F(9, 10), 1: F(1, 10)}
    observed, contrasts = {}, {}
    for world in ['A', 'B']:
        law = Counter()
        means = {x: F(0) for x in [0, 1]}
        for u, v in product([0, 1], repeat=2):
            mass = F(1, 2) * noise[v]
            law[outcome(world, u, v)] += mass
            for x in [0, 1]:
                means[x] += mass * outcome(world, u, v, x)[1]
        assert sum(law.values()) == 1
        observed[world] = dict(law)
        contrasts[world] = means[1] - means[0]
    assert observed['A'] == observed['B'] == {(0, 0): F(9, 20), (0, 1): F(1, 20),
                                            (1, 0): F(1, 20), (1, 1): F(9, 20)}
    assert contrasts == dict(A=F(4, 5), B=F(0))
    # Conditional bootstrap law for three copies of each concordant pair.
    positive_count = 0
    for indices in product(range(6), repeat=6):
        sample = [int(i >= 3) for i in indices]
        covariance = F(sum(sample), 6) - F(sum(sample), 6) ** 2
        positive_count += covariance > 0
    stable = F(positive_count, 6 ** 6)
    assert stable == 1 - 2 * F(1, 2) ** 6 == F(31, 32)
    # Independent exact probability of observing the stipulated unordered data.
    event = F(0)
    atoms = sorted(observed['A'])
    for sample in product(atoms, repeat=6):
        if Counter(sample) == Counter({(0, 0): 3, (1, 1): 3}):
            mass = F(1)
            for atom in sample:
                mass *= observed['A'][atom]
            event += mass
    assert event == comb(6, 3) * F(9, 20) ** 6 == F(531441, 3200000)
    value = {w: 100 * tau - 30 for w, tau in contrasts.items()}
    assert value == dict(A=F(50), B=F(-30))
    # One asymmetric undirected tag at [0,1] is legal in the inspected converter.
    # Both possible two-node orientations belong to this simple equivalence class.
    truths = [(1, 0), (0, 1)]
    assisted = [graph_metrics(t, t) for t in truths]
    fixed = [graph_metrics(t, (1, 0)) for t in truths]
    assert assisted == [1, 1] and fixed == [1, 0]
    raw = [[0, 0], [1, 0]]  # [i,j]=1 means j->i.
    # A stipulated 20-result collection: 19 forward, 1 reverse. This is
    # compatible with the default bootstrap count, not an observed run.
    directed = [[F(0), F(1, 20)], [F(19, 20), F(0)]]
    uncertain = [[F(0), F(0)], [F(0), F(0)]]
    reachability = deletion_reference(raw, directed, uncertain, 'C')
    assert (1, 0) in reachability['high'] and (0, 1) in reachability['middle']
    assert (0, 1) in reachability['llm_pairs'] and reachability['after_llm'] == [[0, 0], [0, 0]]
    # A separately stated guard using unordered protected pairs blocks the same
    # response. This is a proposed invariant, not an upstream implementation.
    protected = {tuple(sorted(pair)) for pair in reachability['high'] if pair[0] != pair[1]}
    guarded = [row[:] for row in raw]
    if (0, 1) not in protected:
        guarded = [[0, 0], [0, 0]]
    assert guarded == raw
    return dict(
        evidence_kind='Project-authored exact enumeration and conditional static witness; not upstream execution',
        observational_laws=observed, intervention_contrasts=contrasts,
        bootstrap_positive_covariance=stable, bootstrap_positive_sequences=positive_count,
        bootstrap_sequences=6 ** 6, stipulated_dataset_probability=event,
        stipulated_incremental_usd=value,
        two_world_scoring=dict(truth_assisted=assisted, fixed_truth_blind=fixed,
            truth_assisted_mean=sum(assisted)/2, fixed_truth_blind_mean=sum(fixed)/2),
        conditional_deletion=dict(raw=raw, directed_probabilities=directed, **reachability,
            stipulated_bootstrap_results=20, stipulated_forward_results=19,
            accepted_answer='C', proposed_unordered_guard_result=guarded,
            limitations=['Accepted response stipulated; no observed model response or full runtime reproduction.',
                'Witness stops after LLM mutation; later KCI/cycle behavior and external background-knowledge library not simulated.',
                'Does not attribute this2026 snapshot to the2025 paper experiments.']))


if __name__ == '__main__':
    import json
    print(json.dumps(serial(calculate()), indent=2))
