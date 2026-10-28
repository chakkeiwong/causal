#!/usr/bin/env python3
"""Finite authored evaluation examples; no model or downloaded code executes."""
from fractions import Fraction as F
import json

def calculate():
    q=F(1,10)
    independent_majority=3*q*q*(1-q)+q**3
    gross=F(70)
    cost=F(80)
    fixed_targets=[dict(action='A',proxy=F(9,10),utility=-10),
                   dict(action='B',proxy=F(4,5),utility=20)]
    proxy_choice=max(fixed_targets,key=lambda x:x['proxy'])
    utility_choice=max(fixed_targets,key=lambda x:x['utility'])
    labels=[0,1,0,1]
    predictions=[0,1,0,1]
    truth=[1,0,1,0]
    benchmark=sum(x==y for x,y in zip(labels,predictions))
    actual=sum(x==y for x,y in zip(truth,predictions))
    assert independent_majority==F(7,250)
    assert gross-cost==-10 and utility_choice['utility']-proxy_choice['utility']==30
    assert benchmark==4 and actual==0
    return dict(kind='authored_finite_laws_not_empirical_performance',
        semantic_target=dict(hypothetical_gross_recovery_usd=str(gross),
            action_cost_usd=str(cost),net_increment_usd=str(gross-cost),
            gross_only_action='act',net_value_action='decline'),
        proxy=dict(actions=[{**x,'proxy':str(x['proxy'])} for x in fixed_targets],
            proxy_selected_action='A',utility_selected_action='B',regret_usd=30),
        correlated_judges=dict(marginal_error=str(q),independent_three_majority_error=str(independent_majority),
            shared_error_three_majority_error=str(q)),
        noisy_labels=dict(reference_labels=labels,predictions=predictions,true_labels=truth,
            agreement_with_reference='1',agreement_with_truth='0'),
        partial_tests=dict(input_domain=[0,1],tested_input=[0],
            intended_function_values=[0,1],constant_zero_patch_values=[0,0],
            passes_observed_test=True,meets_full_specification=False),
        public_acceptance=dict(requested=100,completed=80,scientifically_accepted=60,
            completion_rate='4/5',accepted_per_request='3/5',accepted_per_completion='3/4',
            fixed_total_cost_usd=200,cost_per_accepted_usd='10/3',
            cost_per_completion_usd='5/2'),
        native_execution=False,bank_observations=False)

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
