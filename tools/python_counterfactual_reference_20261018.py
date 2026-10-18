#!/usr/bin/env python3
"""Exact authored coupling example; no external causal package is imported."""
from fractions import Fraction as F
from itertools import product
import json


def calculate():
    models = []
    for name, response in [('stable', lambda u: (u, u)),
                           ('switching', lambda u: (u, 1-u))]:
        observed = {(a, y): F(0) for a, y in product(range(2), repeat=2)}
        types = {(y0, y1): F(0) for y0, y1 in product(range(2), repeat=2)}
        numerator = denominator = F(0)
        for u, a in product(range(2), repeat=2):
            y0, y1 = response(u)
            y = (y0, y1)[a]
            observed[a, y] += F(1, 4)
            types[y0, y1] += F(1, 4)
            if a == 0 and y == 0:
                denominator += F(1, 4)
                numerator += F(1, 4)*y1
        marginal = [sum(p*ys[j] for ys, p in types.items()) for j in range(2)]
        conditional = numerator/denominator
        assert marginal == [F(1, 2), F(1, 2)]
        assert all(v == F(1, 4) for v in observed.values())
        models.append(dict(name=name, observed={f'{a},{y}': str(v) for (a,y),v in observed.items()},
            response_types={f'{y0},{y1}': str(v) for (y0,y1),v in types.items()},
            do_means=list(map(str, marginal)), ATE=str(marginal[1]-marginal[0]),
            factual_event_probability=str(denominator), conditional_recovery=str(conditional),
            benefit_fraction=str(types[0,1]), assumed_conditional_net_USD=str(400*conditional-50)))
    assert models[0]['observed'] == models[1]['observed']
    assert [m['conditional_recovery'] for m in models] == ['0', '1']
    assert [m['assumed_conditional_net_USD'] for m in models] == ['-50', '350']
    # With both marginals 1/2, every feasible response table has one free t.
    # (p00,p01,p10,p11)=(1/2-t,t,t,1/2-t), 0<=t<=1/2.
    for t in [F(0), F(1,8), F(1,4), F(3,8), F(1,2)]:
        table = [F(1,2)-t, t, t, F(1,2)-t]
        assert min(table)>=0 and sum(table)==1
        assert table[1]+table[3] == table[2]+table[3] == F(1,2)
    return dict(status='exact_authored_reference', upstream_execution=False, random_draws=0,
        assumption='A and U independent fair bits; Y=Y(A); no interference. Both models belong to the allowed A->Y model; faithfulness is not imposed.',
        models=models, sharp_benefit_bounds=['0','1/2'], sharp_conditional_bounds=['0','1'],
        sharp_conditional_net_USD=['-50','350'],
        construction='For every real t in [0,1/2], choose response-type probabilities (1/2-t,t,t,1/2-t) independently of randomized A. Nonnegativity proves necessity; the resulting SCM proves attainability.',
        monotonicity='Adding Y(1)>=Y(0) forces p10=t=0 when both means equal 1/2. This is an additional unverified scientific restriction, not information learned from randomization.',
        interpretation='Retrospective counterfactual for a factual untreated failure, with stipulated USD400 recovery value and USD50 intervention cost. The factual failure is not available before the original decision; no prospective policy value, sampling interval or bank ROI is established.')


if __name__ == '__main__':
    print(json.dumps(calculate(), indent=2))
