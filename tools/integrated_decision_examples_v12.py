#!/usr/bin/env python3
"""Exact stipulated decision examples; no model, bank or package trial."""
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs/program/repair-v12/work/LA07/decision-examples.json"


def compute():
    effects = {"low": F(0), "high": F(400)}
    prior = {"low": F(1, 2), "high": F(1, 2)}
    likelihood = {"low": {"positive": F(1, 10), "negative": F(9, 10)},
                  "high": {"positive": F(9, 10), "negative": F(1, 10)}}
    action_cost = F(300)
    unassisted = max(F(0), sum(prior[k] * (v - action_cost) for k, v in effects.items()))
    perfect = sum(prior[k] * max(F(0), v - action_cost) for k, v in effects.items())
    signals = {}
    gross = F(0)
    for signal in ("positive", "negative"):
        probability = sum(prior[k] * likelihood[k][signal] for k in effects)
        posterior_high = prior["high"] * likelihood["high"][signal] / probability
        net_if_act = sum(prior[k] * likelihood[k][signal] * (v - action_cost)
                         for k, v in effects.items()) / probability
        value = max(F(0), net_if_act)
        gross += probability * value
        signals[signal] = {"probability": probability, "posterior_high": posterior_high,
                           "net_if_act": net_if_act, "chosen_action": int(net_if_act > 0)}
    service_cost = F(2) + F(8)
    incremental = gross - unassisted - service_cost
    break_even = F(50000) / incremental
    direct = sum(prior[k] * likelihood[k][s] *
                 signals[s]["chosen_action"] * (v - action_cost)
                 for k, v in effects.items() for s in signals)
    assert direct == gross == 30 and perfect == 50 and unassisted == 0
    assert incremental == 20 and break_even == 2500
    assert signals["positive"]["net_if_act"] == 60
    assert signals["negative"]["net_if_act"] == -260
    # A second derivation uses false-positive loss and true-positive gain.
    assert gross == F(1, 2) * F(9, 10) * 100 - F(1, 2) * F(1, 10) * 300
    monetary_cutoffs = [100 * F(-2) - 300, 100 * F(3) - 300]
    assert monetary_cutoffs == [-500, 0]
    return {"status": "exact_checks_pass", "kind": "stipulated_project_construction",
            "live_model_calls": 0, "external_packages_executed": 0,
            "units": "CNY per stipulated decision", "prior_high": F(1, 2),
            "action_cost": action_cost, "effects": effects, "signals": signals,
            "unassisted_value": unassisted, "perfect_information_gross_value": perfect,
            "signal_gross_value": gross, "assessment_cost": service_cost,
            "incremental_net_value": incremental, "fixed_cost": F(50000),
            "break_even_decisions": break_even, "high_state_action_threshold": F(3, 4),
            "set_conversion": {"effect_components": [[None, -2], [3, None]],
                               "scale": 100, "offset": -300,
                               "value_components": [[None, -500], [0, None]],
                               "loss_components": [[None, 0], [500, None]]},
            "limits": ["All probabilities and costs are stipulated, not measured or elicited.",
                       "No claim that language confidence is a calibrated posterior.",
                       "Scale calculation assumes the same expected value and linear costs for every decision.",
                       "Perfect-information bound is for this decision and information structure only."],
            "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


def encode(value):
    if isinstance(value, F):
        return {"exact": str(value), "decimal": float(value)}
    raise TypeError(type(value))


if __name__ == "__main__":
    result = compute()
    OUT.write_text(json.dumps(result, indent=2, default=encode) + "\n")
    print(json.dumps({"status": result["status"], "gross": 30, "net": 20,
                      "break_even": 2500, "live_model_calls": 0}))
