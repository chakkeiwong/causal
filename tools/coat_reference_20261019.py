#!/usr/bin/env python3
"""Exact authored references for noisy factors and dependent proposal attempts."""
from fractions import Fraction as F
from itertools import product
import json


def calculate():
    # U causes A and Y. A has no effect on Y; W is a fallible measurement of U.
    joint = {}
    for u, a, y, w in product((0, 1), repeat=4):
        p = F(1, 4)+F(u, 2)
        joint[u, a, y, w] = F(1, 2)*(p if a else 1-p)*(p if y else 1-p)*(F(3, 4) if w == u else F(1, 4))
    assert sum(joint.values()) == 1 and min(joint.values()) > 0

    def mass(**conditions):
        return sum(p for row, p in joint.items() if all(row['uayw'.index(k)] == v for k, v in conditions.items()))

    true_conditional = {(a,u): mass(a=a,u=u,y=1)/mass(a=a,u=u) for a,u in product((0,1),repeat=2)}
    assert all(true_conditional[0,u] == true_conditional[1,u] for u in (0,1))
    conditional = {(a,w): mass(a=a,w=w,y=1)/mass(a=a,w=w) for a,w in product((0,1),repeat=2)}
    standardized = [sum(conditional[a,w]*mass(w=w) for w in (0,1)) for a in (0,1)]
    assert standardized == [F(2,5),F(3,5)]
    covariance = []
    for w in (0,1):
        covariance.append(mass(a=1,y=1,w=w)/mass(w=w)-mass(a=1,w=w)*mass(y=1,w=w)/mass(w=w)**2)
    assert covariance == [F(3,64),F(3,64)]
    true_risks = [F(1,2),F(1,2)]
    effect = standardized[1]-standardized[0]
    independent_failure = F(1,2)**4
    shared_failure = F(1,2)
    return dict(kind='project_authored_exact_reference',upstream_execution=False,
        assumptions=['U fair binary; A and Y independent given U with success probability1/4+U/2.',
            'W independently flips U with probability1/4; W is75percent accurate.',
            'No A-to-Y arrow; intervention leaves marginal Y risk1/2.'],
        conditional_risks=[dict(a=a,w=w,risk=str(v)) for (a,w),v in conditional.items()],
        true_intervention_risks=list(map(str,true_risks)),proxy_standardized_risks=list(map(str,standardized)),
        true_effect='0',proxy_contrast=str(effect),residual_conditional_covariances=list(map(str,covariance)),
        assumed_success_payoff_USD=100,assumed_action_cost_USD=10,
        assumed_true_net_USD='-10',assumed_proxy_net_USD=str(100*effect-10),
        attempts=dict(rounds=4,marginal_success_probability='1/2',
            independent_no_success=str(independent_failure),shared_no_success=str(shared_failure),
            conclusion='Equal marginal proposal-success probabilities do not determine the chance of useful discovery over repeated dependent attempts.'),
        limitations=['Stipulated positive law and proposal-attempt dependence, not measured LLM errors or COAT execution.',
            'This illustrates violation of the source parsing assumption, not failure under that assumption.',
            'No finite coverage, general convergence repair or actual bank economics is claimed.'])


if __name__ == '__main__':
    print(json.dumps(calculate(),indent=2))
