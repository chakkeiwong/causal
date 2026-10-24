#!/usr/bin/env python3
"""Finite authored MCP contract witnesses; never imports external SDK code."""
from fractions import Fraction as F
import json

def calculate():
    versions={'python':{'2024-11-05','2025-03-26','2025-06-18','2025-11-25','2026-07-28'},
              'r':{'2024-11-05','2025-03-26','2025-06-18','2025-11-25'},
              'hkr':{'2025-03-26'}}
    common=sorted(set.intersection(*versions.values()))
    assert common==['2025-03-26']
    # Each object passes the stated elementary type predicate. No SDK execution.
    a={'estimate':1,'unit':'USD'};b={'estimate':1,'unit':'USD thousands'}
    type_accept=lambda x:isinstance(x['estimate'],int) and isinstance(x['unit'],str)
    assert type_accept(a) and type_accept(b)
    normalized=[a['estimate'],1000*b['estimate']];assert normalized==[1,1000]
    # Known direction is lost if an endpoint-marked graph is converted to adjacency.
    graphs=[('X','tail','arrow','Y'),('X','circle','arrow','Y')]
    project=lambda g:(g[0],g[3])
    assert graphs[0]!=graphs[1] and project(graphs[0])==project(graphs[1])
    # Under Y(a)=U, intervention effect is 0 although the observed law has Y=A.
    u=[0,1];observed=[(x,x) for x in u]
    difference=F(observed[1][1]-observed[0][1]);effect=F(sum(x-x for x in u),len(u))
    assert difference==1 and effect==0
    # A durable side effect precedes a cancellation signal and cannot be undone by it.
    events=[(0,'submitted'),(2,'charge_committed'),(3,'cancel_requested'),(4,'local_cancel_observed')]
    cost_per_charge=500;one_cost=cost_per_charge;naive_retry_cost=2*cost_per_charge
    assert one_cost==500 and naive_retry_cost==1000
    # Missing scientific status is not upgraded from a returned protocol envelope.
    totals={'submitted':100,'returned':90,'tool_success':80,'qualified':60}
    rates=[F(totals['qualified'],totals[x]) for x in ['submitted','returned','tool_success']]
    costs=[F(18000,totals[x]) for x in ['submitted','returned','qualified']]
    assert rates==[F(3,5),F(2,3),F(3,4)] and costs==[180,200,300]
    # A typed missing value and an actual zero are distinct scientific outcomes.
    states=[{'status':'not_identified','estimate':None},{'status':'identified','estimate':0}]
    fallback=[s['estimate'] or 0 for s in states];assert fallback==[0,0] and states[0]!=states[1]
    return json.loads(json.dumps(dict(kind='authored_exact_contract_witnesses',common_declared_version=common,
        typed_money_values_usd=normalized,endpoint_graphs=graphs,projected_graphs=[project(g) for g in graphs],
        observed_difference=difference,intervention_effect=effect,cancellation_events=events,
        charge_before_cancel_usd=one_cost,naive_retry_charge_usd=naive_retry_cost,totals=totals,
        qualified_rates=rates,costs_usd=costs,scientific_states=states,lossy_zero_projection=fallback,
        native_execution=False),default=lambda x:str(x) if isinstance(x,F) else x))

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
