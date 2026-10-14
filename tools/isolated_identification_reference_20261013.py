#!/usr/bin/env python3
"""Project source trace and exact law; does not import or execute y0."""
from fractions import Fraction as F
from itertools import product
import json


def run():
    nodes = {"A", "Y", "Z"}
    directed = {("A", "Y")}
    interventions = {"A"}
    # Trace remove_in_edges/from_edges: seed intervention vertices,
    # then add endpoints of surviving edges.
    surviving = {(u, v) for u, v in directed if v not in interventions}
    traced_nodes = interventions | {n for edge in surviving for n in edge}
    assert traced_nodes == {"A", "Y"} and nodes - traced_nodes == {"Z"}
    observed = {}
    for a, y, z in product(range(2), repeat=3):
        prob_y = F(1, 4) + F(1, 2) * a
        observed[a, y, z] = F(1, 4) * (prob_y if y else 1 - prob_y)
    assert sum(observed.values()) == 1 and min(observed.values()) > 0
    targets = {}
    for a, z in product(range(2), repeat=2):
        mass = sum(v for (aa, _, zz), v in observed.items() if aa == a and zz == z)
        conditional = observed[a, 1, z] / mass
        do_conditional = F(1, 4) + F(1, 2) * a
        assert conditional == do_conditional
        targets[f"a={a},z={z}"] = str(do_conditional)
    return {
        "kind": "project_source_trace_and_exact_law",
        "y0_executed": False,
        "random_draws": 0,
        "original_nodes": sorted(nodes),
        "directed_edges": [list(x) for x in sorted(directed)],
        "source_traced_nodes_after_remove_in_edges": sorted(traced_nodes),
        "missing_joint_outcome": "Z",
        "next_source_operation": "NetworkX ancestors request for absent Z",
        "native_exception_observed": False,
        "positive_observed_cells": {','.join(map(str, k)): str(v) for k, v in observed.items()},
        "identified_conditional_means": targets,
        "effect_in_each_condition": "1/2",
        "required_admission_cases": [
            "A->Y and isolated condition Z: retain joint query Y,Z under do(A)",
            "Isolated outcome Y under do(A): retain p(Y), not missing-node failure",
            "Condition Z with an incident edge: do not use the isolated-variable simplification",
            "Engine exception: retain query and classify unavailable, never nonidentified",
        ],
        "scope": "A source-level failure mechanism and exact reference; no installed-engine result",
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
