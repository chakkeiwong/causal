#!/usr/bin/env python3
"""Exact project-authored binary potential-outcome reference for R survey."""
from fractions import Fraction as F
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs/program/execution/2026-10-18/r-identification/exact-results.json"


def calculate():
    # q[y0,y1], with randomized-arm risks fixed at 1/4 and 3/4.
    rows = []
    for t in (F(0), F(1, 8), F(1, 4)):
        q = {(1, 1): t, (0, 1): F(3, 4)-t,
             (1, 0): F(1, 4)-t, (0, 0): t}
        assert sum(q.values()) == 1
        assert q[1, 0] >= 0 and q[0, 1] >= 0
        p_y0 = q[1, 0] + q[1, 1]
        p_y1 = q[0, 1] + q[1, 1]
        ate = p_y1 - p_y0
        pn = q[0, 1] / p_y1
        rows.append({"t_q11": str(t), "q00": str(q[0, 0]),
                     "q01": str(q[0, 1]), "q10": str(q[1, 0]),
                     "q11": str(q[1, 1]), "p_y0": str(p_y0),
                     "p_y1": str(p_y1), "ate": str(ate), "pn": str(pn)})

    # Equal randomized-arm binomial likelihood on every member of the fiber.
    sequence_likelihood = F(1, 4)**2 * F(3, 4)**6
    aggregate_likelihood = 16 * sequence_likelihood
    prior_a = [F(1, 3)] * 3
    prior_b = [F(1, 6), F(1, 3), F(1, 2)]
    pn = [F(1), F(5, 6), F(2, 3)]

    def posterior_mean(weights):
        weighted = [w * sequence_likelihood for w in weights]
        normalizer = sum(weighted)
        posterior = [w / normalizer for w in weighted]
        return {"posterior_weights": [str(x) for x in posterior],
                "mean_pn": str(sum(w*x for w, x in zip(posterior, pn)))}

    assert [r["ate"] for r in rows] == ["1/2"] * 3
    assert [r["pn"] for r in rows] == ["1", "5/6", "2/3"]
    assert sequence_likelihood == F(729, 65536)
    assert aggregate_likelihood == F(729, 4096)
    assert posterior_mean(prior_a)["mean_pn"] == "5/6"
    assert posterior_mean(prior_b)["mean_pn"] == "7/9"
    net = [1000*x - 800 for x in pn]
    assert net == [F(200), F(F(1000)*F(5, 6)-800), F(-400, 3)]
    hidden = []
    for name, outcome in [('causal', lambda a, u: a),
                          ('confounded', lambda a, u: u)]:
        observed = {(a, y): F(0) for a in (0, 1) for y in (0, 1)}
        risks = []
        for u in (0, 1):
            observed[u, outcome(u, u)] += F(1, 2)
        for a in (0, 1):
            risks.append(sum(F(outcome(a, u), 2) for u in (0, 1)))
        hidden.append(dict(model=name,
                           observed={str(k): str(v) for k, v in observed.items()},
                           do_risks=[str(x) for x in risks],
                           ate=str(risks[1]-risks[0])))
    assert hidden[0]['observed'] == hidden[1]['observed']
    assert [x['ate'] for x in hidden] == ['1', '0']
    return {
        "status": "pass",
        "kind": "project_authored_exact_reference",
        "assumptions": ["binary potential outcomes", "consistency",
                        "positive randomized offer assignment",
                        "known randomized-arm population risks P(Y0=1)=1/4 and P(Y1=1)=3/4"],
        "fiber_order": ["t=0", "t=1/8", "t=1/4"],
        "fiber": rows,
        "hidden_confounding_counterexample": hidden,
        "sharp_population_set": {"ate": ["1/2", "1/2"],
                                  "pn": ["2/3", "1"],
                                  "monotonicity_y1_ge_y0": {"t": "1/4", "pn": "2/3"}},
        "finite_arm_counts": {"design": "four randomized units per arm; 1/4 and 3/4 successes",
                              "ordered_sequence_likelihood_each_fiber_world": str(sequence_likelihood),
                              "aggregate_binomial_likelihood_each_fiber_world": str(aggregate_likelihood)},
        "stipulated_discrete_priors": {
            "support": ["t=0", "t=1/8", "t=1/4"],
            "prior_a": [str(x) for x in prior_a],
            "posterior_a": posterior_mean(prior_a),
            "prior_b": [str(x) for x in prior_b],
            "posterior_b": posterior_mean(prior_b),
        },
        "hypothetical_retrospective_value_contract": {
            "formula": "1000 USD * PN - 800 USD per treated responder",
            "sharp_net_value_set_usd": [str(min(net)), str(max(net))],
            "prior_a_mean_net_usd": str(1000*F(5, 6)-800),
            "prior_b_mean_net_usd": str(1000*F(7, 9)-800),
            "limitation": "Illustrative retrospective attribution accounting, not prospective selection on a future outcome or an observed bank ROI."
        },
        "limitations": ["Finite exact construction; not upstream package execution or empirical coverage.",
                        "Point identification, the sharp population set, sampling uncertainty and posterior summaries are different objects.",
                        "The posterior summaries are prior-sensitive because the stipulated randomized likelihood is constant along the fiber."]
    }


if __name__ == "__main__":
    value = calculate()
    OUT.write_text(json.dumps(value, indent=2) + "\n")
    print(json.dumps({"status": value["status"], "fiber_worlds": len(value["fiber"]),
                      "ate": value["sharp_population_set"]["ate"],
                      "pn": value["sharp_population_set"]["pn"],
                      "posterior_means": [value["stipulated_discrete_priors"]["posterior_a"]["mean_pn"],
                                          value["stipulated_discrete_priors"]["posterior_b"]["mean_pn"]]}))
