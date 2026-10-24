#!/usr/bin/env python3
"""Independent exact semantic and accounting examples; no upstream code."""
from fractions import Fraction
import json

def calculate():
    edges={('A','B'),('B','C')}
    reachable=set(edges)
    while True:
        updated=reachable|{(a,d) for a,b in reachable for c,d in reachable if b==c}
        if updated==reachable:break
        reachable=updated
    assert ('A','C') in reachable and ('A','C') not in edges
    alpha=Fraction(1,20);legacy_missing=Fraction(0)
    assert legacy_missing<alpha
    # Two equally weighted strata, with specified overlap probabilities/effects.
    propensity=[Fraction(1,2),Fraction(1,10)];effects=[Fraction(0),Fraction(10)]
    uniform=sum(effects)/2
    weights=[e*(1-e) for e in propensity]
    overlap=sum(w*t for w,t in zip(weights,effects))/sum(weights)
    assert uniform==5 and overlap==Fraction(45,17)
    costs={'preparation':900,'all_attempts':1100,'review':2500,'maintenance_allocation':500}
    total=sum(costs.values());assert total==5000
    return dict(scope='Exact authored examples; no observed package behavior or benchmark result',
        direct_edges=[list(x) for x in sorted(edges)],ancestry=[list(x) for x in sorted(reachable)],
        ancestry_is_not_adjacency=True,
        zero_as_missing_below_alpha=legacy_missing<alpha,alpha=str(alpha),
        missing_status='unavailable; not a numerical test result',
        estimands=dict(equal_stratum_effect=str(uniform),overlap_weighted_effect=str(overlap),
            propensities=[str(x) for x in propensity],effects=[str(x) for x in effects],
            unnormalized_overlap_weights=[str(x) for x in weights],
            assumptions='Two equal population strata; both retained by a stipulated trimming interval[0.05,0.95]; effects and propensities given'),
        costs_usd=costs,total_usd=total,attempted=100,completed=80,admissible=50,
        per_attempt_usd=str(Fraction(total,100)),per_completion_usd=str(Fraction(total,80)),
        per_admissible_usd=str(Fraction(total,50)))

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
