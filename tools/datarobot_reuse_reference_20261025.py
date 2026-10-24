#!/usr/bin/env python3
"""Exact authored weighting/accounting witnesses; no upstream code or data executed."""
from fractions import Fraction
import json

def calculate():
    w=[Fraction(4),Fraction(4,3)];y=[Fraction(1),Fraction(0)];p=Fraction(1,2)
    normalized=sum(a*b for a,b in zip(w,y))/sum(w)
    stable=[p*x for x in w];normalized_stable=sum(a*b for a,b in zip(stable,y))/sum(stable)
    ess=sum(w)**2/sum(x*x for x in w);stable_ess=sum(stable)**2/sum(x*x for x in stable)
    assert normalized==normalized_stable==Fraction(3,4) and ess==stable_ess==Fraction(8,5)
    extreme=p/Fraction(1,100);clipped=p/Fraction(1,10);assert extreme==50 and clipped==5
    costs=dict(preparation=1000,all_model_attempts=2400,scientific_review=2800,maintenance=1000);assert sum(costs.values())==7200
    return dict(scope='Authored rational examples; no vendor run, real data, observed inference or price',
        treated_arm=dict(propensities=['1/4','3/4'],outcomes=['1','0'],weights=list(map(str,w)),stabilization_factor=str(p),stabilized_weights=list(map(str,stable)),normalized_mean=str(normalized),normalized_stabilized_mean=str(normalized_stable),effective_sample_size=str(ess),stabilized_effective_sample_size=str(stable_ess)),
        extreme_example=dict(propensity='1/100',stabilized_weight=str(extreme),hypothetical_clipped_propensity='1/10',changed_weight=str(clipped),clipping_not_upstream_behavior=True),
        assumptions='Within-arm normalization; positive weights; stipulated sample values; no finite-sample uncertainty theorem',
        costs_usd=costs,total_usd=7200,attempted=120,completed=90,admissible=60,
        per_attempt_usd=str(Fraction(7200,120)),per_completion_usd=str(Fraction(7200,90)),per_admissible_usd=str(Fraction(7200,60)))
if __name__=='__main__':print(json.dumps(calculate(),indent=2))
