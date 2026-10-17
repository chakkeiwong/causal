#!/usr/bin/env python3
"""Exact authored examples for question translation; no bank observations."""
from fractions import Fraction as F
import json


def calculate():
    h, days = 30, 365
    b0, b1, requirement = 100000, 110000, 150000
    r0, r1, q = F(2, 100), F(225, 10000), F(5, 100)
    k0, k1 = 4, 8
    s0, s1 = h*b0, h*b1
    value = lambda rate: ((rate-r1)*s1-(rate-r0)*s0)/days-(k1-k0)
    cost0 = (r0*s0+q*(h*requirement-s0))/days+k0
    cost1 = (r1*s1+q*(h*requirement-s1))/days+k1
    threshold = (r1*s1-r0*s0+days*(k1-k0))/(s1-s0)
    retained = (q-r0)*(s1-s0)/days
    repricing = (r1-r0)*s1/days
    assert value(q) == retained-repricing-(k1-k0) == -(cost1-cost0)
    assert value(q) == -F(142, 73) and value(threshold) == 0
    # An independent cash-ledger reconstruction sums daily costs directly.
    daily = sum((r1*b1+q*(requirement-b1)-r0*b0-q*(requirement-b0))/days
                for _ in range(h))+(k1-k0)
    assert daily == -value(q)
    early = sum(x*y for x, y in zip([F(1,10),F(1,100)], [200,0]))/days
    late = sum(x*y for x, y in zip([F(1,10),F(1,100)], [0,200]))/days
    # Same mean balance, different expected capped value.
    cap_fixed = F(min(100,100),100)
    cap_random = F(min(0,100)+min(200,100),200)
    # Positive selection probabilities with a genuine randomized zero effect.
    joint = {(a,u): F(1,4)*(F(3,4) if a==u else F(1,4))
             for a in [0,1] for u in [0,1]}
    selected = {a: sum(p*u for (aa,u),p in joint.items() if aa==a)/
                    sum(p for (aa,u),p in joint.items() if aa==a) for a in [0,1]}
    corrected = {}
    for a in [0,1]:
        weights = [(u,p/(F(3,4) if a==u else F(1,4)))
                   for (aa,u),p in joint.items() if aa==a]
        corrected[a] = sum(u*w for u,w in weights)/sum(w for _,w in weights)
    assert selected == {0:F(1,4),1:F(3,4)} and corrected == {0:F(1,2),1:F(1,2)}
    measure = lambda mu,se,sp: se*mu+(1-sp)*(1-mu)
    mu0,mu1=F(2,5),F(1,2)
    common0=measure(mu0,F(4,5),F(9,10))
    common1=measure(mu1,F(4,5),F(9,10))
    bad1=measure(mu1,F(1,2),F(19,20))
    assert common1-common0 == F(7,100) and bad1-common0 == -F(21,200)
    return dict(
        funding=dict(average_balance_change=b1-b0,balance_day_change=s1-s0,
            retained_value=retained,repricing_cost=repricing,incremental_operating_cost=k1-k0,
            net_value=value(q),net_cost=cost1-cost0,break_even_rate=threshold,
            value_at_four_percent=value(F(4,100)),value_at_six_percent=value(F(6,100))),
        timing=dict(equal_average_change=100,early_value=early,late_value=late),
        nonlinear=dict(fixed_gross=cap_fixed,random_gross=cap_random,
            fixed_net=cap_fixed-F(3,4),random_net=cap_random-F(3,4)),
        selection=dict(true_effect=0,selected_control=selected[0],selected_treated=selected[1],
            selected_contrast=selected[1]-selected[0],oracle_corrected_contrast=corrected[1]-corrected[0]),
        measurement=dict(true_contrast=mu1-mu0,common_measured_contrast=common1-common0,
            differential_measured_contrast=bad1-common0),
        checks=dict(daily_cost_identity=True,selection_enumerated=True,
            fractions_exact=True,bank_or_provider_evidence=False))


def serial(value):
    if isinstance(value,F): return str(value)
    if isinstance(value,dict): return {str(k):serial(v) for k,v in value.items()}
    if isinstance(value,list): return [serial(v) for v in value]
    return value


if __name__ == '__main__':
    print(json.dumps(serial(calculate()),indent=2))
