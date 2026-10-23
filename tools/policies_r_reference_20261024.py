#!/usr/bin/env python3
"""Exact authored policy-learning examples; execute no upstream packages."""
from fractions import Fraction as F
from itertools import product
import json

def calculate():
    def q(x):return dict(exact=str(x),decimal=float(x))
    selected=sum(F(max(a,b),4) for a,b in product([-1,1],repeat=2))
    assert selected==F(1,2)
    mu,mhat,e,ehat=F(10),F(8),F(1,4),F(1,2)
    score=mhat+e/ehat*(mu-mhat)
    bias=(1-e/ehat)*(mhat-mu);assert score==9 and bias==-1
    correct_e=mhat+e/e*(mu-mhat);correct_m=mu+e/ehat*(mu-mu)
    assert correct_e==correct_m==mu
    path_probability=F(1,10)**4;true_weight=1/path_probability
    capped_weight=F(100);capped_expectation=path_probability*capped_weight
    assert true_weight==10000 and capped_expectation==F(1,100)
    full_history=sum(F(int(a==h),2) for h in [0,1] for a in [h])
    state_only=max(sum(F(int(a==h),2) for h in [0,1]) for a in [0,1])
    assert full_history==1 and state_only==F(1,2)
    utility=lambda a:8*a-2*a*a
    assert utility(2)==8 and utility(1)==6
    groups,repeats=2,100
    actual_variance=F(1,4*groups);independent_row_variance=F(1,4*groups*repeats)
    assert actual_variance/independent_row_variance==100
    return dict(scope='Independent exact finite-law and stipulated banking examples; not native package results',
        selection=dict(true_values=[0,0],independent_estimation_errors=[-1,1],expected_selected_training_value=q(selected),fresh_expected_value=0),
        doubly_robust_score=dict(true_mean=q(mu),outcome_fit=q(mhat),true_propensity=q(e),propensity_fit=q(ehat),expected_score=q(score),bias=q(bias),correct_propensity=q(correct_e),correct_outcome=q(correct_m),positivity_required=True),
        unsupported_action=dict(observed_action=0,observed_reward=0,indistinguishable_action1_rewards=[-10,10],identified_optimum=False),
        sequential_support=dict(stages=4,each_probability=q(F(1,10)),path_probability=q(path_probability),weight=q(true_weight),cap=q(capped_weight),unit_reward_true_value=1,capped_ipw_expectation=q(capped_expectation)),
        history=dict(full_history_value=q(full_history),constant_state_value=q(state_only)),
        continuous_action=dict(stipulated_quadratic='8a-2a^2',unrestricted_maximizer=2,unrestricted_value=8,observed_support=[0,1],restricted_maximizer=1,restricted_value=6,alternative_beyond_one='6-100(a-1)',alternative_optimum_on_nonnegative_domain=1,extrapolated_optimum_identified=False),
        clusters=dict(clusters=groups,copies_per_cluster=repeats,actual_mean_variance=q(actual_variance),false_independent_rows_variance=q(independent_row_variance),variance_ratio=100),
        costs=dict(initiated=20,accepted_numeric=5,correct_refusals=4,total_usd=100,cost_per_attempt=5,cost_per_accepted_numeric=20),native_execution=False)

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
