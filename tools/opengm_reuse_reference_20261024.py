#!/usr/bin/env python3
"""Independent finite OpenGM contract witnesses; no acquired code execution."""
from fractions import Fraction as F
import math,json

def calculate():
    joint={(0,0):F(35,100),(0,1):F(25,100),(1,0):F(0),(1,1):F(40,100)}
    map_state=max(joint,key=joint.get)
    p0=sum(p for (x,y),p in joint.items() if x==0)
    assert map_state==(1,1) and p0==F(3,5)
    marginal_loss=1-p0;map_component_loss=p0
    assert (marginal_loss,map_component_loss)==(F(2,5),F(3,5))
    # Variable zero is the fastest enumeration axis in the selected source.
    order=[(0,0),(1,0),(0,1),(1,1)]
    energy=dict(zip(order,[5,4,3,0]))
    prefix_min=min(energy[x] for x in order[:2]);global_min=min(energy.values())
    assert (prefix_min,global_min)==(4,0)
    one=F(2,3);two=F(4,5)
    # Illustrate the selected additive update order using IEEE binary64.
    partial_update=float('inf')+0.0-float('inf')
    assert math.isnan(partial_update)
    assert min([F(7),F(0)])==0
    # Semantic axis reversal changes the queried event, even with normalized data.
    weights={(0,0):F(1),(0,1):F(2),(1,0):F(3),(1,1):F(4)}
    total=sum(weights.values())
    x1=sum(w for (x,y),w in weights.items() if x==1)/total
    swapped_x1=sum(w for (x,y),w in weights.items() if y==1)/total
    assert (x1,swapped_x1)==(F(7,10),F(3,5))
    # Confounding-only model: U fair, P(A=U)=4/5, Y=U.
    observed=F(4,5);intervened=F(1,2)
    return dict(kind='authored_exact_and_IEEE_witnesses_not_native_execution',
        marginal_vs_map=dict(joint={str(k):str(v) for k,v in joint.items()},map_state=list(map_state),p_x0=str(p0),marginal_loss=str(marginal_loss),map_component_loss=str(map_component_loss),hypothetical_10000_cases_100usd_extra_loss=str((map_component_loss-marginal_loss)*10000*100)),
        early_stop=dict(order=[list(x) for x in order],energies=[energy[x] for x in order],visited=2,incumbent=prefix_min,optimum=global_min,gap=4,source_return='NORMAL does not identify exhaustion'),
        repeated_factor=dict(one_factor_p0=str(one),two_factors_p0=str(two),change=str(two-one),function_sharing_not_factor_deduplication=True),
        infinity_update=dict(expression='positive infinity + 0 - positive infinity',binary64_result='NaN',exact_feasible_optimum=0,conditional_static_path=True,native_observed=False),
        axis_order=dict(correct_x1=str(x1),transposed_x1=str(swapped_x1)),
        causality=dict(observed_success=str(observed),interventional_success=str(intervened),effect=0),
        complexity=dict(binary_variables=40,assignments=2**40),
        economics=dict(hypothetical_usd=18000,submitted=600,completed=450,qualified=300,costs_usd=[30,40,60]),native_execution=False)

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
