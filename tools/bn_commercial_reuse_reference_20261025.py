#!/usr/bin/env python3
"""Exact project-authored counterfactual and resource-accounting illustrations."""
from fractions import Fraction
import json


def calculate():
    worlds={'persistent':lambda x,u:u,'flipping':lambda x,u:x^u}
    results={}
    for name,fn in worlds.items():
        observed={f'{x},{y}':Fraction(0) for x in [0,1] for y in [0,1]}
        for x in [0,1]:
            for u in [0,1]:observed[f'{x},{fn(x,u)}']+=Fraction(1,4)
        intervention={str(x):sum((Fraction(fn(x,u),2) for u in [0,1]),Fraction(0)) for x in [0,1]}
        eligible=[u for u in [0,1] if fn(0,u)==0]
        counterfactual=sum((Fraction(fn(1,u),len(eligible)) for u in eligible),Fraction(0))
        results[name]=dict(observed={k:str(v) for k,v in observed.items()},
            intervention_means={k:str(v) for k,v in intervention.items()},
            ate=str(intervention['1']-intervention['0']),
            y1_given_x0_y0=str(counterfactual))
    assert results['persistent']['observed']==results['flipping']['observed']
    assert results['persistent']['intervention_means']==results['flipping']['intervention_means']
    assert results['persistent']['y1_given_x0_y0']=='0' and results['flipping']['y1_given_x0_y0']=='1'
    loaded=[('A',0,5),('B',3,7),('C',5,9)]
    events=sorted({v for _,a,b in loaded for v in [a,b]})
    counts=[dict(t=t,loaded=sum(a<=t<b for _,a,b in loaded)) for t in events]
    peak=max(x['loaded'] for x in counts);assert peak==2
    costs={'model_preparation':2400,'all_requests':1200,'review':3600,'maintenance_allocation':800}
    total=sum(costs.values());assert total==8000
    return dict(scope='Authored exact models and hypothetical accounting; no vendor execution, quote or bank outcome',
        worlds=results,loaded_intervals=[list(x) for x in loaded],interval_convention='Half-open [load, unload)',
        occupancy=counts,peak_loaded_models=peak,distinct_models=3,
        costs_usd=costs,total_usd=total,attempted=200,completed=160,admissible=100,
        per_attempt_usd=str(Fraction(total,200)),per_completion_usd=str(Fraction(total,160)),
        per_admissible_usd=str(Fraction(total,100)))


if __name__=='__main__':print(json.dumps(calculate(),indent=2))
