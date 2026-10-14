#!/usr/bin/env python3
"""Exact proposal references. Does not import or execute y0 or draw random data."""
from fractions import Fraction as F
from itertools import product
import json


def binary(p, x):
    return p if x else 1 - p


def frontdoor():
    # U is hidden from the observational table supplied to identification.
    observed = {(a, m, y): F(0) for a, m, y in product(range(2), repeat=3)}
    for u, a, m, y in product(range(2), repeat=4):
        observed[a, m, y] += (F(1, 2) * binary(F(1, 5) + F(3, 5) * u, a)
                              * binary(F(1, 4) + F(1, 2) * a, m)
                              * binary(F(1, 10) + F(1, 2) * m + F(1, 5) * u, y))
    assert sum(observed.values()) == 1 and min(observed.values()) > 0

    def mass(a=None, m=None, y=None):
        return sum(p for (aa, mm, yy), p in observed.items()
                   if (a is None or a == aa) and (m is None or m == mm)
                   and (y is None or y == yy))

    # Evaluate the observational front-door functional independently of do-law.
    identified = [sum(mass(a=a, m=m) / mass(a=a)
                      * sum(mass(a=aa, m=m, y=1) / mass(a=aa, m=m) * mass(a=aa)
                            for aa in range(2)) for m in range(2)) for a in range(2)]
    intervention = [sum(F(1, 2) * binary(F(1, 4) + F(1, 2) * a, m)
                        * (F(1, 10) + F(1, 2) * m + F(1, 5) * u)
                        for u, m in product(range(2), repeat=2)) for a in range(2)]
    naive = [mass(a=a, y=1) / mass(a=a) for a in range(2)]
    assert identified == intervention == [F(13, 40), F(23, 40)]
    assert naive[1] - naive[0] == F(37, 100)
    return {"graph": {"directed": [["A", "M"], ["M", "Y"]], "bidirected": [["A", "Y"]]},
            "observed_positive_cells": {','.join(map(str, k)): str(v) for k, v in observed.items()},
            "do_means": list(map(str, intervention)), "functional_means": list(map(str, identified)),
            "causal_difference": str(identified[1] - identified[0]),
            "naive_difference": str(naive[1] - naive[0]),
            "assumed_value_per_success_usd": 1000, "hypothetical_gross_difference_usd": 250,
            "scope": "Exact generated population, not fitted data or y0 execution"}


def bow():
    # Both SCMs are members of the model allowing A -> Y and A <-> Y.
    # A=U; first SCM uses Y=A xor E, second uses Y=U xor E, E~Bernoulli(.2).
    models = [lambda a, u, e: a ^ e, lambda a, u, e: u ^ e]
    joints, means = [], []
    for model in models:
        joint = {(a, y): F(0) for a, y in product(range(2), repeat=2)}
        for u, e in product(range(2), repeat=2):
            joint[u, model(u, u, e)] += F(1, 2) * binary(F(1, 5), e)
        joints.append(joint)
        means.append([sum(F(1, 2) * binary(F(1, 5), e) * model(a, u, e)
                          for u, e in product(range(2), repeat=2)) for a in range(2)])
    assert joints[0] == joints[1]
    assert means == [[F(1, 5), F(4, 5)], [F(1, 2), F(1, 2)]]
    effects = [m[1] - m[0] for m in means]
    joint = joints[0]
    assert sum(joint.values()) == 1 and min(joint.values()) > 0
    return {"observed_law_in_both_models": {','.join(map(str, k)): str(v) for k, v in joint.items()},
            "first_do_means": list(map(str, means[0])), "second_do_means": list(map(str, means[1])),
            "different_effects": list(map(str, effects)),
            "scope": "Nonidentification reference under an allowed-edge graph; no faithfulness requirement"}


def collider():
    # Latents U,V are independent fair bits. Y=U, Z=V; B reports U=V
    # with error .1. Observed graph is Y <-> B <-> Z, with isolated X.
    observed = {(y, b, z): F(0) for y, b, z in product(range(2), repeat=3)}
    for u, v, b in product(range(2), repeat=3):
        observed[u, b, v] += F(1, 4) * binary(F(9, 10) if u == v else F(1, 10), b)
    conditional = observed[1, 1, 1] / sum(observed[y, 1, 1] for y in range(2))
    # do(Z=1) overwrites Z, leaving independent U,V and B's mechanism intact.
    numerator = sum(F(1, 4) * (F(9, 10) if u == v else F(1, 10))
                    for u, v in product(range(2), repeat=2) if u == 1)
    denominator = sum(F(1, 4) * (F(9, 10) if u == v else F(1, 10))
                      for u, v in product(range(2), repeat=2))
    interventional = numerator / denominator
    assert conditional == F(9, 10) and interventional == F(1, 2)
    assert min(observed.values()) > 0
    return {"graph": {"nodes": ["X", "Y", "B", "Z"], "directed": [],
                      "bidirected": [["Y", "B"], ["B", "Z"]]},
            "rule2_query": "Y independent of Z given X,B in G_bar(X)_under(Z)",
            "m_separated": False,
            "source_traced_prediction_of_inspected_routine": "separated: no directed moral links, remove B disconnects Y and Z",
            "conditional_Y1_given_B1_Z1": str(conditional),
            "Y1_given_B1_after_do_Z1": str(interventional),
            "observed_positive_cells": {','.join(map(str, k)): str(v) for k, v in observed.items()},
            "qualification": "Source-level counterexample plus independent arithmetic; package was not run"}


def main():
    print(json.dumps({"kind": "independent_exact_proposal_references", "random_draws": 0,
                      "y0_executed": False, "frontdoor": frontdoor(), "bow": bow(),
                      "bidirected_collider": collider()}, indent=2))


if __name__ == '__main__':
    main()
