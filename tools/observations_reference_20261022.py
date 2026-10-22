#!/usr/bin/env python3
"""Exact authored observation examples; no vendor or empirical banking result."""
from fractions import Fraction as F
import json

def calculate():
    rows=[dict(event=8,available=9,value=2),dict(event=9,available=12,value=9)]
    decision=10
    event_only=max((r for r in rows if r['event']<=decision),key=lambda r:r['event'])
    admissible=max((r for r in rows if r['event']<=decision and r['available']<=decision),key=lambda r:r['event'])
    treated=[F(8),F(6)];control=[F(4),F(2)]
    delta=sum(treated)/2-sum(control)/2
    p=F(4,5);mixed=p*delta+(1-p)*(-delta)
    # Independent equiprobable +/-1/2 noise gives within-map variance 1/4.
    law=[(weight/2,mean+noise) for weight,mean in [(p,delta),(1-p,-delta)] for noise in [F(-1,2),F(1,2)]]
    expectation=sum(w*x for w,x in law)
    variance=sum(w*(x-expectation)**2 for w,x in law)
    between=p*(1-p)*(2*delta)**2
    strata=[(F(1,2),F(1),F(6)),(F(1,2),F(1,4),F(2))]
    retained=sum(m*s for m,s,_ in strata)
    population=sum(m*effect for m,s,effect in strata)
    linked=sum(m*s*effect for m,s,effect in strata)/retained
    reweighted=sum((m*s/retained)*effect/s for m,s,effect in strata)/sum((m*s/retained)/s for m,s,effect in strata)
    assert expectation==mixed==F(12,5)
    assert variance==F(1,4)+between==F(1049,100)
    assert reweighted==population==4 and linked==F(26,5)
    def encode(o):
        if isinstance(o,F):return str(o)
        if isinstance(o,dict):return {k:encode(v) for k,v in o.items()}
        if isinstance(o,list):return [encode(v) for v in o]
        return o
    return encode(dict(kind='project_authored_exact_reference_not_vendor_execution',
        clocks=dict(rows=rows,decision=decision,event_only=event_only,admissible=admissible),
        linkage=dict(correct_contrast=delta,swapped_contrast=-delta,joint_map_probability=p,
            integrated_contrast=mixed,within_variance=F(1,4),between_variance=between,total_variance=variance,
            hard_map_margin=10*delta-30,integrated_margin=10*mixed-30,profit_threshold=F(7,8)),
        selection=dict(retention=retained,population_effect=population,linked_effect=linked,reweighted_effect=reweighted),
        limitations=['Hypothetical two-map law; p is stipulated joint mapping probability, not calibrated vendor confidence.',
            'Contrast needs randomized assignment, consistency and no interference to estimate a causal effect.',
            'Selection correction requires positive inclusion and conditional transport of potential outcomes.',
            'USD10 per outcome unit and USD30 cost are stipulated; no measured return.']))

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
