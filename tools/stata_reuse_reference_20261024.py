#!/usr/bin/env python3
"""Authored command-interface mathematics; no Stata binary or package executed."""
from fractions import Fraction as F
import json

def calculate():
    effects=[F(10),F(-5)]
    weights_a=[F(4,5),F(1,5)];weights_b=list(reversed(weights_a))
    aggregate_a=sum(w*x for w,x in zip(weights_a,effects));aggregate_b=sum(w*x for w,x in zip(weights_b,effects))
    assert (aggregate_a,aggregate_b)==(7,-2)
    groups=10;members=100
    actual_variance=F(1,groups);iid_variance=F(1,groups*members)
    assert actual_variance/iid_variance==100
    estimates=[F(0),F(2)];within=[F(1),F(1)];m=len(estimates)
    pooled=sum(estimates)/m;w=sum(within)/m;b=sum((x-pooled)**2 for x in estimates)/(m-1)
    total=w+(1+F(1,m))*b;assert (pooled,w,b,total)==(1,1,2,4)
    # Static Gaussian state S~N(0,1); later Y=S+noise, noise~N(0,1), observed Y=2.
    prior_mean=F(0);gain=F(1,2);later_y=F(2)
    smoothed_mean=gain*later_y;smoothed_var=1-gain
    assert (smoothed_mean,smoothed_var)==(1,F(1,2))
    # With iid unit innovations, first differences have variance2 and lag1cov-1.
    diff_var=F(2);lag1_cov=F(-1);lag1_corr=lag1_cov/diff_var
    assert lag1_corr==F(-1,2)
    return dict(kind='authored_exact_witnesses_not_Stata_execution',
        aggregation=dict(effects=[str(x) for x in effects],weights_a=[str(x) for x in weights_a],weights_b=[str(x) for x in weights_b],effect_a=str(aggregate_a),effect_b=str(aggregate_b),hypothetical_10000_accounts_usd=[str(10000*aggregate_a),str(10000*aggregate_b)],different_targets_not_estimator_defect=True),
        dependence=dict(groups=groups,members=members,within_group_correlation=1,actual_mean_variance=str(actual_variance),iid_mean_variance=str(iid_variance),variance_ratio=100,se_ratio=10,known_covariance_toy_not_finite_cluster_calibration=True),
        imputation=dict(estimates=[str(x) for x in estimates],pooled=str(pooled),within=str(w),between=str(b),total_variance=str(total),within_only_variance=str(w),standard_error=2,within_only_standard_error=1),
        state_clock=dict(prior_mean=str(prior_mean),later_observation=str(later_y),smoothed_mean=str(smoothed_mean),smoothed_variance=str(smoothed_var),future_observation_unavailable_at_initial_decision=True),
        dynamic_panel=dict(iid_level_innovation_variance=1,difference_variance=str(diff_var),lag1_covariance=str(lag1_cov),lag1_correlation=str(lag1_corr),lag2_covariance=0,not_a_native_test=True),
        economics=dict(hypothetical_usd=30000,submitted=1000,completed=750,qualified=500,costs_usd=[30,40,60]),native_execution=False)

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
