#!/usr/bin/env python3
"""Independent finite probability examples; no libDAI code is executed."""
from fractions import Fraction as F
from itertools import product
from math import exp,log,isclose
import json

def normalize(values):
    if all(isinstance(v,(int,F)) for v in values):values=[F(v) for v in values]
    total=sum(values)
    if not total:raise ValueError('zero mass')
    return [v/total for v in values]

def calculate():
    values=list(range(1,7))
    correct=normalize([sum(values[x+2*y] for y in range(3)) for x in range(2)])
    wrong=normalize([sum(values[3*x+y] for y in range(3)) for x in range(2)])
    assert correct==[F(3,7),F(4,7)] and wrong==[F(2,7),F(5,7)]
    # U fair; A agrees with U with probability4/5;Y=U.
    joint={(u,a,y):F(1,2)*(F(4,5) if a==u else F(1,5))*int(y==u)
           for u,a,y in product(range(2),repeat=3)}
    obs=sum(v*y for (u,a,y),v in joint.items() if a==1)/sum(v for (u,a,y),v in joint.items() if a==1)
    intervened={(u,y):F(1,2)*int(y==u) for u,y in product(range(2),repeat=2)}
    do=sum(v*y for (u,y),v in intervened.items());assert obs==F(4,5) and do==F(1,2)
    # A triangle of binary variables with weight3for equal neighbors,1otherwise.
    states=list(product(range(2),repeat=3));edges=[(0,1),(1,2),(2,0)]
    weights={s:__import__('functools').reduce(lambda a,e:a*(3 if s[e[0]]==s[e[1]] else 1),edges,1) for s in states}
    z=sum(weights.values());exact_pair=sum(w for s,w in weights.items() if s[0]==s[1])/F(z)
    bp_pair=F(6,8)
    # Uniform factor-to-variable messages update to uniform under this symmetry.
    new=normalize([sum(F(3 if x==y else 1)*F(1,2) for y in range(2)) for x in range(2)])
    residual=max(abs(x-F(1,2)) for x in new)
    assert z==72 and exact_pair==F(5,6) and bp_pair==F(3,4) and residual==0
    assert exact_pair-bp_pair==F(1,12)
    tiny=F(1,10**200);rational=normalize([tiny*tiny,4*tiny*tiny]);assert rational==[F(1,5),F(4,5)]
    binary64=[float(tiny)**2,(2*float(tiny))**2];assert binary64==[0.0,0.0]
    logs=[2*log(float(tiny)),2*log(2*float(tiny))];mx=max(logs);stable=normalize([exp(x-mx) for x in logs])
    assert all(isclose(float(v),w,abs_tol=1e-13) for v,w in zip(rational,stable))
    refused=False
    try:normalize([F(0),F(0)])
    except ValueError:refused=True
    assert refused
    return json.loads(json.dumps(dict(kind='authored_finite_probability_not_native_execution',
        order=dict(values=values,correct_x=[str(v) for v in correct],wrong_x=[str(v) for v in wrong],first_variable_fast=True),
        intervention=dict(observed_success=str(obs),interventional_success=str(do),causal_effect='0',assignment_factor_replaced=True),
        loopy=dict(partition=z,uniform_message_residual=str(residual),exact_edge_agreement=str(exact_pair),bp_edge_agreement=str(bp_pair),absolute_error=str(exact_pair-bp_pair),native_run=False),
        scale=dict(exact_normalized=[str(v) for v in rational],binary64_products=binary64,log_domain_normalized=stable,zero_mass_refused=refused),
        label=dict(same_label_cardinalities=[2,3],adapter_must_refuse=True),
        boundary=dict(states=2,valid=[0,1],invalid_equal_to_states=2,caller_guard='0 <= x < states'),
        memory=dict(binary_variables=30,full_joint_entries=2**30,double_payload_bytes=8*2**30,container_overhead_excluded=True),
        economics=dict(hypothetical_action_value_usd=120000,probability_error=str(F(1,12)),value_error_usd=str(F(120000,12)),hypothetical_total_usd=12000,submitted=400,completed=300,qualified=200,costs_usd=[30,40,60]),native_execution=False)))

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
