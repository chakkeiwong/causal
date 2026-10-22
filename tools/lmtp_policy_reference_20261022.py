#!/usr/bin/env python3
"""Exact authored two-period servicing law; never invokes an upstream estimator."""
from fractions import Fraction as F
import json


def probability(e, delta, policy):
    if policy == 'natural':
        return e
    if policy == 'risk_ratio_shift':
        return delta * e if delta <= 1 else 1 - (1 - e) / delta
    if policy == 'odds_tilt':
        return delta * e / (1 - e + delta * e)
    raise ValueError(policy)


def calculate():
    results = []
    for policy in ['natural', 'risk_ratio_shift', 'odds_tilt']:
        delta = F(2)
        q1 = probability(F(1, 5), delta, policy)
        q20 = probability(F(1, 5), delta, policy)
        q21 = probability(F(3, 5), delta, policy)
        trajectories = []
        for a1 in (0, 1):
            q2 = q21 if a1 else q20
            for a2 in (0, 1):
                mass = (q1 if a1 else 1-q1) * (q2 if a2 else 1-q2)
                gross = 20*a1 + 30*a2 - 10*a1*a2
                cost = 8*(a1+a2)
                trajectories.append(dict(actions=[a1, a2], probability=str(mass),
                    gross_dollars=gross, cost_dollars=cost, net_dollars=gross-cost))
        assert sum(F(x['probability']) for x in trajectories) == 1
        net = sum(F(x['probability'])*x['net_dollars'] for x in trajectories)
        # A separate moment calculation checks the full trajectory enumeration.
        moment = 12*q1 + 22*((1-q1)*q20 + q1*q21) - 10*q1*q21
        assert net == moment
        results.append(dict(policy=policy, delta=str(delta), q1=str(q1),
            q2_given_a1_zero=str(q20), q2_given_a1_one=str(q21),
            trajectories=trajectories, expected_net_dollars=str(net)))
    baseline = F(results[0]['expected_net_dollars'])
    for row in results:
        row['incremental_net_dollars'] = str(F(row['expected_net_dollars'])-baseline)
    return dict(evidence_kind='authored_exact_known_law_example', native_execution=False,
        units='Stipulated USD per account over two servicing decisions; no bank data or measured benefit.',
        law='At each time, draw natural binary treatment conditional on the already assigned past: e1=1/5, e2(0)=1/5, e2(1)=3/5. Independently randomize the declared modification. No censoring, competing events or latent confounding is included.',
        value='Gross 20*A1+30*A2-10*A1*A2, contact cost 8*(A1+A2).',
        results=results,
        interpretation='A shift parameter of two cannot be converted to an odds tilt of two without changing the policy and monetary target. This reference validates arithmetic, not package parity or an inferential guarantee.')


if __name__ == '__main__':
    print(json.dumps(calculate(), indent=2))
