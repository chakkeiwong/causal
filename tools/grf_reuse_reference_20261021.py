"""Exact authored population witnesses; does not import or execute grf."""
from fractions import Fraction as F
import json


def score(y, w, m, e, tau):
    return tau + (w-e)/(e*(1-e))*(y-m-tau*(w-e))


def outcome_score(y, w, mu0, mu1, e):
    return mu1-mu0 + w/e*(y-mu1) - (1-w)/(1-e)*(y-mu0)


def calculate():
    e, mu0, mu1 = F(1, 4), F(0), F(2)
    target = mu1-mu0
    cases = [
        ("correct_m_and_tau_wrong_e", F(1, 2), F(1, 2), F(2)),
        ("correct_e_wrong_m_and_tau", F(3), e, F(0)),
        ("correct_outcome_surfaces_wrong_e", F(1), F(1, 2), F(2)),
        ("correct_m_and_e_wrong_tau", F(1, 2), e, F(0)),
    ]
    results = []
    for name, mhat, ehat, tauhat in cases:
        h0, h1 = mhat-ehat*tauhat, mhat+(1-ehat)*tauhat
        scores = [score(mu0, F(0), mhat, ehat, tauhat),
                  score(mu1, F(1), mhat, ehat, tauhat)]
        independent = [outcome_score(mu0, F(0), h0, h1, ehat),
                       outcome_score(mu1, F(1), h0, h1, ehat)]
        assert scores == independent
        mean = (1-e)*scores[0]+e*scores[1]
        bias = (ehat-e)*((h1-mu1)/ehat+(h0-mu0)/(1-ehat))
        assert mean-target == bias
        results.append(dict(case=name, mhat=str(mhat), ehat=str(ehat), tauhat=str(tauhat),
            reconstructed_mu0=str(h0), reconstructed_mu1=str(h1),
            scores=list(map(str, scores)), expected_score=str(mean), bias=str(bias)))
    assert [r["expected_score"] for r in results] == ["3/2", "2", "2", "2"]
    # Check the identity by independent enumeration across a finite rational grid.
    checks = 0
    for actual_e in [F(1, 10), F(1, 4), F(1, 2), F(3, 4)]:
        for proposed_e in [F(1, 5), F(1, 2), F(4, 5)]:
            for proposed_m in [F(-1), F(0), F(3)]:
                for proposed_tau in [F(-2), F(0), F(2)]:
                    h0 = proposed_m-proposed_e*proposed_tau
                    h1 = proposed_m+(1-proposed_e)*proposed_tau
                    actual = sum(p*score(y, w, proposed_m, proposed_e, proposed_tau)
                        for p, y, w in [(1-actual_e, mu0, F(0)), (actual_e, mu1, F(1))])
                    predicted = target+(proposed_e-actual_e)*(
                        (h1-mu1)/proposed_e+(h0-mu0)/(1-proposed_e))
                    assert actual == predicted
                    checks += 1
    proportions, propensity, effects = [F(1, 2)]*2, [F(1, 2), F(1, 10)], [F(-4), F(12)]
    weights = dict(all=[F(1)]*2, treated=propensity,
        control=[1-x for x in propensity], overlap=[x*(1-x) for x in propensity])
    targets = {}
    for name, q in weights.items():
        denominator = sum(p*w for p, w in zip(proportions, q))
        theta = sum(p*w*t for p, w, t in zip(proportions, q, effects))/denominator
        targets[name] = dict(normalizer=str(denominator), effect=str(theta))
    assert [targets[k]["effect"] for k in ["all", "treated", "control", "overlap"]] == [
        "4", "-4/3", "44/7", "4/17"]
    return dict(nuisance_cases=results, algebra_grid_checks=checks,
        true_law=dict(propensity="1/4", mu0="0", mu1="2", marginal_outcome_mean="1/2"),
        target_example=dict(group_proportions=list(map(str, proportions)),
            propensities=list(map(str, propensity)), effects=list(map(str, effects)),
            targets=targets, offer_cost="2", all_population_margin="2",
            overlap_population_margin=str(F(targets["overlap"]["effect"])-2)),
        limits=["Exact hypothetical laws with fixed nuisance values; no fitted forest or simulation.",
            "The bias identity is conditional on fixed nuisance functions and a fresh observation.",
            "Algebra does not establish finite-sample coverage or validate a data-dependent selected cohort.",
            "Dollar effects and costs are assumptions, not observed bank returns."])


if __name__ == "__main__":
    print(json.dumps(calculate(), indent=2))
