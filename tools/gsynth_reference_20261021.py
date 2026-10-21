#!/usr/bin/env python3
"""Exact project examples for wrapper semantics and panel counterfactual support."""
from fractions import Fraction as F
import json


def calculate():
    effect, weight = (F(-6), F(10)), (F(9), F(1))
    equal = sum(effect)/2
    weighted = sum(e*w for e,w in zip(effect,weight))/sum(weight)
    assert (equal,weighted)==(F(2),F(-22,5))
    cells = [(0,t,F(10)) for t in range(3)]+[(1,0,F(-6))]
    per_cell = sum(v for i,t,v in cells)/len(cells)
    per_unit = sum(sum(v for i,t,v in cells if i==u)/sum(i==u for i,t,v in cells) for u in [0,1])/2
    assert (per_cell,per_unit)==(F(6),F(2))
    factors = ((F(1),F(0)),(F(2),F(0)),(F(1),F(1)))
    dot=lambda x,y:sum(a*b for a,b in zip(x,y))
    controls=[tuple(dot(f,l) for f in factors) for l in [(F(0),F(1)),(F(1),F(1))]]
    loadings=[(F(2),F(0)),(F(2),F(4))]
    potentials=[tuple(dot(f,l) for f in factors) for l in loadings]
    observed=[list(v[:2])+[F(8)] for v in potentials]
    assert observed[0]==observed[1]
    contrasts=[F(8)-v[2] for v in potentials]
    assert contrasts==[F(6),F(2)]
    null_direction=(F(0),F(1))
    assert all(dot(f,null_direction)==0 for f in factors[:2]) and dot(factors[2],null_direction)==1
    padded_factors = factors[:2]*3 + factors[2:]
    padded_controls = [tuple(dot(f,l) for f in padded_factors)
                       for l in [(F(0),F(1)),(F(1),F(1)),(F(2),F(1))]]
    padded_potentials = [tuple(dot(f,l) for f in padded_factors) for l in loadings]
    assert padded_potentials[0][:-1] == padded_potentials[1][:-1]
    assert all(dot(f,null_direction)==0 for f in padded_factors[:-1])
    return dict(scope='Exact authored targets and deterministic rank-two models; no upstream R execution or empirical uncertainty qualification',
        weights=dict(effects=list(map(str,effect)),weights=list(map(str,weight)),equal=str(equal),weighted=str(weighted),
            cost='1',equal_margin=str(equal-1),weighted_margin=str(weighted-1)),
        aggregation=dict(treated_periods=[3,1],unit_effects=['10','-6'],treated_cell_average=str(per_cell),
            equal_unit_average=str(per_unit),cost='4',cell_margin=str(per_cell-4),unit_margin=str(per_unit-4)),
        factor_support=dict(factors=[list(map(str,v)) for v in factors],controls=[list(map(str,v)) for v in controls],
            treated_loadings=[list(map(str,v)) for v in loadings],observed_treated=[list(map(str,v)) for v in observed],
            counterfactual_post=[str(v[-1]) for v in potentials],effects=list(map(str,contrasts)),
            cost='4',margins=[str(v-4) for v in contrasts],observed_panels_equal=True,pre_factor_rank=1,full_factor_rank=2,
            padded_pre_period_count=6,padded_donor_count=len(padded_controls),
            padded_controls=[list(map(str,v)) for v in padded_controls],
            padded_pre_outcomes=list(map(str,padded_potentials[0][:-1])),
            padded_pre_factor_rank=1,
            limitation='Outside full pre-factor-rank qualification; calendar and donor counts alone do not establish rank.'))


if __name__=='__main__':print(json.dumps(calculate(),indent=2))
