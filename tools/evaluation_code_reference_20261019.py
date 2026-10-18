#!/usr/bin/env python3
"""Exact authored evaluation denominators; no model, code-generation or bank trial."""
from fractions import Fraction as F
from itertools import combinations
from math import comb
import json


def calculate():
    labels=[1,1,1,0,0,0,0,0,0,0];n=len(labels);c=sum(labels);k=2
    subsets=list(combinations(range(n),k))
    oracle=F(sum(any(labels[i] for i in s) for s in subsets),len(subsets))
    formula=1-F(comb(n-c,k),comb(n,k))
    random_selector=F(sum(F(sum(labels[i] for i in s),k) for s in subsets),len(subsets))
    subset_count_misreading=sum((1-F(comb(n-sum(labels[i] for i in s),k),comb(n,k))) for s in subsets)/len(subsets)
    assert len(subsets)==45 and oracle==formula==F(8,15) and random_selector==F(3,10)
    assert subset_count_misreading==F(16,135)
    attempted=20;runnable=16;test_pass=12;target_valid=7;accepted=5
    cost=F(2)*attempted+F(1)*attempted+F(5)*test_pass
    benefit=F(30)*accepted;net=benefit-cost
    assert F(test_pass,runnable)==F(3,4) and F(accepted,attempted)==F(1,4)
    assert cost==120 and cost/accepted==24 and net==30 and net/attempted==F(3,2)
    return dict(kind='authored_exact_evaluation_reference',live_model_execution=False,
        selection=dict(n=n,total_successes=c,k=k,subsets=45,success_subsets=24,
            at_least_one_pass=str(oracle),random_candidate_selector_success=str(random_selector),
            incorrect_selected_subset_count_substitution=str(subset_count_misreading),
            meaning='Finite uniform sampling without replacement from a fixed pool; candidate success labels are stipulated. At-least-one success presumes an oracle or qualified selector for deployment.'),
        pipeline=dict(attempted=attempted,runnable=runnable,test_pass=test_pass,target_valid=target_valid,accepted=accepted,
            pass_among_runnable=str(F(test_pass,runnable)),end_to_end_accepted=str(F(accepted,attempted)),
            no_claim_of_independence=True,meaning='Nested stipulated outcomes. Clinical/causal correctness is not implied by passing unit tests; failure and abstention categories require separate records.'),
        assumed_economics=dict(generation_usd_per_attempt=2,harness_usd_per_attempt=1,review_usd_per_test_pass=5,
            benefit_usd_per_accepted=30,total_cost_usd=str(cost),cost_per_accepted_usd=str(cost/accepted),
            total_benefit_usd=str(benefit),net_usd=str(net),net_usd_per_attempt=str(net/attempted),
            invalid_net_if_tests_equal_acceptance_usd=str(30*test_pass-cost)),
        limitations=['No observed benchmark, candidate selection system, live model quality, vendor price or bank ROI.',
            'No binomial independence or population interval follows from dependent tasks or correlated generated candidates.'])


if __name__=='__main__':print(json.dumps(calculate(),indent=2))
