#!/usr/bin/env python3
"""Exact project arithmetic for software-survey examples, not package trials."""
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs/program/repair-v12/work/SW01/software-contract-examples.json"


def number(x):
    return {"exact": str(x), "decimal": float(x)}


def main():
    # A binary baseline stratum H has probability 1/2. Treatment propensities
    # are 4/5 in H and 1/5 outside H. Effects are fixed within strata, CNY/account.
    p_high, p_a_high, p_a_low = F(1, 2), F(4, 5), F(1, 5)
    p_a = p_high * p_a_high + (1 - p_high) * p_a_low
    p_high_a = p_high * p_a_high / p_a
    ate = p_high * 400 + (1 - p_high) * 100
    att = p_high_a * 400 + (1 - p_high_a) * 100
    assert ate == 250 and att == 340 and ate - 300 < 0 < att - 300

    # Project SCM mean, CNY account cost over the same finite horizon:
    # E[Y|do(a0),L1=l,do(a1)] = 100*l - 50*a1*l +20*a0+10*a1.
    def mean(a0, l, a1):
        return F(100 * l - 50 * a1 * l + 20 * a0 + 10 * a1)

    def policy_value(a0, rule):
        p_l = F(4, 5) if a0 == 0 else F(2, 5)
        return (1 - p_l) * mean(a0, 0, rule(0)) + p_l * mean(a0, 1, rule(1))

    never = policy_value(0, lambda l: 0)
    adaptive = policy_value(1, lambda l: l)
    always = policy_value(1, lambda l: 1)
    assert (never, adaptive, always) == (80, 44, 50)

    # At A0=0 the observed logger acts with probability .9 if L1=1 and .1
    # otherwise; no unmeasured confounding is posited in this project example.
    p_l, logger_l1, logger_l0 = F(4, 5), F(9, 10), F(1, 10)
    p_second = p_l * logger_l1 + (1 - p_l) * logger_l0
    observed_treated = (p_l * logger_l1 * mean(0, 1, 1) + (1 - p_l) * logger_l0 * mean(0, 0, 1)) / p_second
    observed_untreated = (p_l * (1 - logger_l1) * mean(0, 1, 0) + (1 - p_l) * (1 - logger_l0) * mean(0, 0, 0)) / (1 - p_second)
    marginal_contrast = policy_value(0, lambda l: 1) - never
    assert observed_treated - observed_untreated > 0 and marginal_contrast == -30

    # Two linear Gaussian SCMs share covariance [[1,rho],[rho,1]], with
    # independent unit/1-rho^2 exogenous noises, but different intervention slopes.
    rho = F(2, 5)
    residual_variance = 1 - rho * rho
    assert rho * rho + residual_variance == 1

    # Hypothetical reported candidate set and independent pointwise intervals.
    candidates, target = [F(0), F(4, 5)], F(2, 5)
    candidate_distance = min(abs(x - target) for x in candidates)
    hull_distance = max(min(candidates) - target, F(0), target - max(candidates))
    assert candidate_distance == F(2, 5) and hull_distance == 0
    all_ten = F(95, 100) ** 10
    assert F(59, 100) < all_ten < F(60, 100)

    report = {
        "schema_version": "causalbank.project-software-examples/1",
        "kind": "exact_project_arithmetic_not_bank_data_or_external_software_execution",
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "target_population": {"units": "CNY gross incremental contribution per account over one declared horizon",
                              "high_stratum_population": number(p_high), "high_stratum_treated": number(p_high_a),
                              "ate": number(ate), "att": number(att), "hypothetical_cost": 300,
                              "net_population": number(ate - 300), "net_treated_target": number(att - 300)},
        "sequential_servicing": {"units": "CNY cost per account over one declared horizon; smaller is preferable",
                                 "never": number(never), "initial_then_adaptive": number(adaptive), "always": number(always),
                                 "observed_second_treated": number(observed_treated), "observed_second_untreated": number(observed_untreated),
                                 "observational_difference": number(observed_treated - observed_untreated),
                                 "causal_second_action_contrast_at_initial_zero": number(marginal_contrast)},
        "graph_equivalence": {"covariance": [[1, float(rho)], [float(rho), 1]],
                              "forward_effect_per_unit": number(rho), "reverse_effect_of_X_on_Y": 0,
                              "residual_variance": number(residual_variance)},
        "candidate_set": {"candidate_values": [float(x) for x in candidates], "hypothetical_truth": float(target),
                          "nearest_candidate_distance": number(candidate_distance), "hull_distance": number(hull_distance),
                          "empty_result_disposition": "unavailable; cannot replace with zero effect or scalar distance"},
        "pointwise_intervals": {"pointwise_coverage_assumed": .95, "independent_queries_assumed": 10,
                                "simultaneous_coverage_under_these_assumptions": number(all_ten),
                                "limitation": "No independence or coverage rate is asserted for an actual event-study package."},
        "status": "exact_checks_pass", "external_packages_run": 0,
    }
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"status": report["status"], "example_families": 5,
                      "observational_difference": float(observed_treated - observed_untreated),
                      "causal_difference": float(marginal_contrast), "external_packages_run": 0}))


if __name__ == "__main__":
    main()
