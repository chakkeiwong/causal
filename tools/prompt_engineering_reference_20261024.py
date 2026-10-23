#!/usr/bin/env python3
"""Authored exact prompt-evaluation witnesses; no models or downloaded code."""
from fractions import Fraction as F
from itertools import product
from math import comb
import json

def calculate():
    n,k=4,20
    cdf=lambda m:sum(F(comb(n,j),2**n) for j in range(m+1))
    expected_best=sum(1-cdf(m-1)**k for m in range(1,n+1))/n
    perfect=1-(1-F(1,2)**n)**k
    costs={'model':F(4),'retrieval':F(2),'review':F(24)}
    authority=[]
    for trusted,allowed,matched in product([False,True],repeat=3):
        authority.append(dict(trusted_request=trusted,allowed_action=allowed,
            artifact_matches=matched,admit=trusted and allowed and matched))
    result=dict(scope='Constructed probability/decision/authorization laws; not native measurements',
        prompt_selection=dict(prompts=k,development_tasks=n,true_success='1/2',
            chance_some_perfect=str(perfect),chance_some_perfect_decimal=float(perfect),
            expected_best_development_accuracy=str(expected_best),
            expected_best_development_accuracy_decimal=float(expected_best),
            independent_heldout_expected_accuracy='1/2',
            assumptions='All development success indicators independent Bernoulli1/2 across prompts/tasks; fresh test independent of selection.'),
        missing_premises=dict(loss_usd='1000',action_cost_usd='20',
            default_reduction_lower='-1/10',default_reduction_upper='1/10',
            net_lower_usd=str(1000*F(-1,10)-20),net_upper_usd=str(1000*F(1,10)-20),
            invented_reduction='1/20',invented_net_usd=str(1000*F(1,20)-20),
            break_even_reduction=str(F(20,1000))),
        pipeline=dict(stages=5,stage_success='19/20',
            independent_all_success=str(F(19,20)**5),
            arbitrary_dependence_lower=str(1-5*F(1,20)),
            perfectly_correlated_success='19/20',
            assumptions='Each stage correctness event has marginal probability19/20; independence is an added assumption.'),
        authority=dict(truth_table=authority,admitted=sum(x['admit'] for x in authority),
            denied=sum(not x['admit'] for x in authority),
            limitation='Logical contract only; no protocol implementation, adversarial guarantee or live system test.'),
        illustrative_cost=dict(costs={x:str(y) for x,y in costs.items()},total=str(sum(costs.values())),
            attempted=10,accepted=3,cost_per_attempt=str(sum(costs.values())/10),
            cost_per_accepted=str(sum(costs.values())/3)))
    assert result['missing_premises']['net_lower_usd']=='-120'
    assert result['pipeline']['independent_all_success']=='2476099/3200000'
    assert result['authority']['admitted']==1 and result['authority']['denied']==7
    return result

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
