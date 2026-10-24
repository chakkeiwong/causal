#!/usr/bin/env python3
"""Authored finite examples; no vendor package,model or downloaded code runs."""
from fractions import Fraction as F
import json


def calculate():
    # A conventional edge-list schema checks types and enum labels,not acyclicity.
    nodes={'A','B','C'}
    edges=[('A','B'),('B','C'),('C','A')]
    structurally_typed=all(a in nodes and b in nodes and a!=b for a,b in edges)
    def has_cycle():
        incoming={n:0 for n in nodes};children={n:[] for n in nodes}
        for a,b in edges:incoming[b]+=1;children[a].append(b)
        ready=[n for n,k in incoming.items() if k==0];seen=0
        while ready:
            n=ready.pop();seen+=1
            for child in children[n]:
                incoming[child]-=1
                if incoming[child]==0:ready.append(child)
        return seen!=len(nodes)
    assert structurally_typed and has_cycle()
    # Two remote model responses can surround several local tool invocations.
    calls_per_response=[3,2]
    remote_limit=2
    executed_calls=sum(calls_per_response[:remote_limit-1])
    assert executed_calls==3
    costs=[F(1,5),F(3,10)];tool_costs=[F(2),F(5),F(3)]
    total=sum(costs)+sum(tool_costs)
    assert total==F(21,2)
    # A stipulated read-timeout profile does not include queue/prefill/tool delays.
    queue,prefill,first_newline=F(5),F(3),F(8)
    generation_limit=F(2)
    observed_end=queue+prefill+first_newline
    assert observed_end==16 and observed_end>generation_limit
    # Retry counters and request counters have different origins.
    original,retries=1,2
    attempts=original+retries
    retry_after=[F(12),F(12)];request_elapsed=[F(4)]*attempts
    elapsed=sum(retry_after)+sum(request_elapsed)
    assert elapsed==36
    # Conditional accuracy can reverse all-request coverage and cost rankings.
    providers={'A':dict(submitted=100,complete=50,correct=45,cost=F(150)),
               'B':dict(submitted=100,complete=90,correct=72,cost=F(180))}
    results={k:dict(conditional_agreement=str(F(v['correct'],v['complete'])),
                   correct_per_submission=str(F(v['correct'],v['submitted'])),
                   cost_per_correct_usd=str(v['cost']/v['correct'])) for k,v in providers.items()}
    assert F(45,50)>F(72,90) and F(45,100)<F(72,100)
    assert F(150,45)>F(180,72)
    # Paired logical cases,not repeated attempts,define the target comparison.
    paired=[(1,1),(1,0),(0,1),(0,0)]
    differences=[b-a for a,b in paired]
    assert sum(differences)==0
    return dict(schema_example=dict(nodes=sorted(nodes),edges=[list(e) for e in edges],typed=True,acyclic=False,
                    conclusion='Request structure alone does not qualify the DAG or causal premises.'),
        automatic_tools=dict(remote_limit=remote_limit,tool_calls_in_first_response=3,
                    executed_local_functions=executed_calls,unexecuted_last_response_calls=2,
                    model_cost_usd=str(sum(costs)),tool_cost_usd=str(sum(tool_costs)),total_usd=str(total)),
        deadline=dict(queue_seconds=str(queue),prefill_seconds=str(prefill),configured_generation_seconds=str(generation_limit),
                    next_newline_seconds=str(first_newline),end_to_end_seconds=str(observed_end),
                    assumption='No earlier EOS/token/other stop;time branch checked when newline arrives.'),
        retry=dict(max_retries=retries,request_attempts=attempts,request_seconds=str(sum(request_elapsed)),
                    retry_wait_seconds=str(sum(retry_after)),elapsed_seconds=str(elapsed)),
        ranking=results,paired_case_example=dict(logical_cases=len(paired),paired_mean_difference=str(F(sum(differences),len(paired))),
                    repeated_attempts_do_not_add_logical_cases=True),
        native_execution=False,prices='All amounts stipulated for mathematical illustration,not provider prices.')


if __name__=='__main__':print(json.dumps(calculate(),indent=2))
