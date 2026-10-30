#!/usr/bin/env python3
"""Exact authored frontdoor, adjustment-scope and typed-result references."""
from fractions import Fraction as F
from itertools import product
import json


def calculate():
    # U -> A, U -> Y, A -> M -> Y; U is unobserved, noises independent.
    joint = {}
    for u, a, m, y in product((0, 1), repeat=4):
        pa = F(1, 4)+F(u, 2)
        pm = F(1, 4)+F(a, 2)
        py = F(1, 8)+F(m, 2)+F(u, 4)
        joint[u, a, m, y] = F(1, 2)*(pa if a else 1-pa)*(pm if m else 1-pm)*(py if y else 1-py)
    assert sum(joint.values()) == 1 and min(joint.values()) > 0
    obs = {(a, m, y): sum(p for (u0, a0, m0, y0), p in joint.items()
        if (a0, m0, y0) == (a, m, y)) for a, m, y in product((0, 1), repeat=3)}

    def probability(**conditions):
        return sum(p for row, p in obs.items() if all(row['amy'.index(k)] == v for k, v in conditions.items()))

    def outcome(a, m):
        return probability(a=a, m=m, y=1)/probability(a=a, m=m)

    frontdoor = [sum(probability(m=m, a=a)/probability(a=a)*
        sum(outcome(b, m)*probability(a=b) for b in (0, 1)) for m in (0, 1)) for a in (0, 1)]
    direct_do = [sum(F(1, 2)*((F(1, 4)+F(a, 2)) if m else 1-F(1, 4)-F(a, 2))*
        (F(1, 8)+F(m, 2)+F(u, 4)) for u, m in product((0, 1), repeat=2)) for a in (0, 1)]
    naive = [probability(a=a, y=1)/probability(a=a) for a in (0, 1)]
    mediator_standardized = [sum(outcome(a, m)*probability(m=m) for m in (0, 1)) for a in (0, 1)]
    assert frontdoor == direct_do == [F(3, 8), F(5, 8)]
    assert naive == [F(5, 16), F(11, 16)]
    assert mediator_standardized == [F(7, 16), F(9, 16)]
    effects = dict(intervention=direct_do[1]-direct_do[0], observed=naive[1]-naive[0],
        mediator_adjusted=mediator_standardized[1]-mediator_standardized[0])
    net = {k: 100*v-20 for k, v in effects.items()}
    assert effects == dict(intervention=F(1, 4), observed=F(3, 8), mediator_adjusted=F(1, 8))
    assert net == dict(intervention=F(5), observed=F(35, 2), mediator_adjusted=F(-15, 2))
    return dict(kind='project_authored_exact_reference', upstream_execution=False,
        assumptions=dict(hidden='U is fair binary', assignment='P(A=1|U)=1/4+U/2',
            mediator='P(M=1|A)=1/4+A/2', outcome='P(Y=1|M,U)=1/8+M/2+U/4',
            errors='Independent structural randomization; no direct A -> Y and no hidden A -> M confounding'),
        observed_law=[dict(a=a, m=m, y=y, mass=str(p)) for (a, m, y), p in obs.items()],
        interventional_risks=list(map(str, direct_do)), frontdoor_risks=list(map(str, frontdoor)),
        observed_risks=list(map(str, naive)), mediator_standardized_risks=list(map(str, mediator_standardized)),
        effects={k: str(v) for k, v in effects.items()},
        assumed_success_payoff_USD='100', assumed_action_cost_USD='20',
        assumed_net_USD={k: str(v) for k, v in net.items()},
        adjustment_reasoning=['The empty set leaves A <- U -> Y open.',
            'The only available nonendpoint candidate M is a descendant of A and does not block that hidden backdoor.',
            'No permitted backdoor set in this graph does not imply absence of another identifying functional.',
            'The frontdoor expression equals direct intervention enumeration for this stipulated law; no general theorem or package execution is asserted.'],
        proposed_result_contract=[dict(input='[[]]', meaning='one solution: the empty adjustment set'),
            dict(input='[]', meaning='no emitted solutions; validate query and completion before interpreting'),
            dict(input='false', meaning='failed selected criterion/search, not a universal nonidentification certificate'),
            dict(input='exception', meaning='invalid or unsupported request, or implementation failure; preserve cause'),
            dict(input='capped iterator', meaning='partial enumeration with completion unknown')],
        limitations=['Authored finite law and contract examples, not Julia/JavaScript/R executions.',
            'The exact expression is checked for this law; general frontdoor and path-specific completeness require their matched original proofs.',
            'No real loan outcome, bank price, empirical calibration or implemented adapter is claimed.'])


if __name__ == '__main__':
    print(json.dumps(calculate(), indent=2))
