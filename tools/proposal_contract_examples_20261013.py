#!/usr/bin/env python3
"""Exact project examples for software/result semantics, not a fitted study."""
from fractions import Fraction as F
import json
from pathlib import Path


def mm(a, b):
    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def implied_covariance(b, variances):
    n = len(b)
    identity = [[F(i == j) for j in range(n)] for i in range(n)]
    power = identity
    total = [row[:] for row in identity]
    for _ in range(1, n):
        power = mm(power, b)
        total = [[x + y for x, y in zip(r, s)] for r, s in zip(total, power)]
    assert all(x == 0 for row in mm(power, b) for x in row), "SEM must be acyclic"
    covariance = mm([[v * x for v, x in zip(variances, r)] for r in total], list(zip(*total)))
    return covariance, total


def calculate():
    a, b = F(3, 5), F(4, 5)
    var_m, cov_my = 1 + a * a, b * (1 + a * a)
    var_y = 1 + b * b * var_m
    cov_xy = a * b
    zero = F(0)
    models = {
        "X_to_M_to_Y": ([[zero, zero, zero], [a, zero, zero], [zero, b, zero]], [F(1)] * 3),
        "X_from_M_to_Y": ([[zero, a / var_m, zero], [zero, zero, zero], [zero, b, zero]],
                            [1 - a * a / var_m, var_m, F(1)]),
        "X_from_M_from_Y": ([[zero, a / var_m, zero], [zero, zero, cov_my / var_y], [zero, zero, zero]],
                              [1 - a * a / var_m, var_m - cov_my * cov_my / var_y, var_y]),
    }
    covariances, effects = {}, {}
    for key, (weights, variances) in models.items():
        assert all(v > 0 for v in variances)
        covariance, total = implied_covariance(weights, variances)
        covariances[key] = covariance
        effects[key] = total[2][0]
    covariance = covariances["X_to_M_to_Y"]
    assert all(c == covariance for c in covariances.values())
    assert cov_xy - a * cov_my / var_m == 0  # Gaussian X independent Y given M.
    assert set(effects.values()) == {F(0), F(12, 25)}
    # W is measured before A; Y is in thousands of currency units.
    # P(W=1)=1/2, P(A=1|W)=1/5+3W/5, E[Y(a)|W]=3W+a(1+2W).
    joint = {(w, treatment): F(1, 2) * ((F(1, 5) + F(3, 5) * w) if treatment
                                     else (F(4, 5) - F(3, 5) * w))
             for w in (0, 1) for treatment in (0, 1)}
    mass = {t: sum(p for (w, a0), p in joint.items() if a0 == t) for t in (0, 1)}
    observed = {t: sum(p * (3 * w + t * (1 + 2 * w)) for (w, a0), p in joint.items()
                       if a0 == t) / mass[t] for t in (0, 1)}
    ate = sum(F(1, 2) * (1 + 2 * w) for w in (0, 1))
    att = sum(joint[w, 1] * (1 + 2 * w) for w in (0, 1)) / mass[1]
    atc = sum(joint[w, 0] * (1 + 2 * w) for w in (0, 1)) / mass[0]
    assert (ate, att, atc, observed[1] - observed[0]) == (F(2), F(13, 5), F(7, 5), F(22, 5))
    numeric = lambda x: float(x)
    return {
        "evidence_kind": "exact_project_derivations_with_rational_arithmetic",
        "engine_execution": False,
        "bank_data": False,
        "graph_example": {
            "nodes": ["X", "M", "Y"],
            "matrix_convention": "B[child,parent] is the SEM coefficient; not a package adjacency convention",
            "covariance": [[numeric(x) for x in r] for r in covariance],
            "same_observed_gaussian_law": True,
            "effects_Y_per_X": {k: numeric(v) for k, v in effects.items()},
            "distinct_effect_set": [0.0, 0.48],
            "units": {"X": "percentage_point", "M": "continuous_index", "Y": "thousand_currency_units"},
            "effect_currency_per_basis_point_forward_model": numeric(F(1000, 100) * a * b),
            "gain_currency_for_25_basis_points_forward_model": numeric(F(1000, 100) * a * b * 25),
            "conditional_gain_for_10000_eligible_units": numeric(F(1000, 100) * a * b * 25 * 10000),
            "interpretation": "Three observationally equivalent DAGs, not three independent datasets or engine outputs",
        },
        "target_example": {
            "law": "P(W=1)=.5; e(W)=.2+.6W; E[Y(a)|W]=3W+a(1+2W)",
            "units": "thousand_currency_units_per_eligible_unit",
            "ATE": numeric(ate), "ATT": numeric(att), "ATC": numeric(atc),
            "unadjusted_difference": numeric(observed[1] - observed[0]),
            "assumptions": ["consistency", "conditional_exchangeability_given_W", "positivity", "no_interference"],
        },
    }


if __name__ == "__main__":
    destination = Path(__file__).resolve().parents[1] / "docs/program/execution/2026-10-13/exact-examples.json"
    value = calculate()
    destination.write_text(json.dumps(value, indent=2) + "\n")
    print(json.dumps(value, indent=2))
