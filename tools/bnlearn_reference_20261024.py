#!/usr/bin/env python3
"""Exact authored semantic witnesses; never imports or executes bnlearn."""
from fractions import Fraction as F
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def rational(x):
    x=F(x);return dict(numerator=x.numerator,denominator=x.denominator,decimal=float(x))
def calculate():
    beta=F(1,2);noise=F(3,4);assert beta**2+noise==1
    joint1={(a,y):F(0) for a in [0,1] for y in [0,1]};joint2=dict(joint1)
    for a in [0,1]:
        for u in [0,1]:joint1[a,u]+=F(1,4);joint2[a,u^a]+=F(1,4)
    assert joint1==joint2 and all(v==F(1,4) for v in joint1.values())
    sample=[2,2,3,1];literal=[sample.index(2)+1];desired=[i+1 for i,v in enumerate(sample) if v==2]
    assert literal==[1] and desired==[1,2]
    # Forty undirected appearances count half in each orientation.
    forward=(F(20)+F(40,2))/100;backward=F(40,2)/100
    strength=forward+backward;direction=forward/strength
    # Two workers have unequal evidence acceptance; mean of ratios differs.
    worker_mean=(F(1,1)+F(0,9))/2;pooled=F(1,10)
    weights=[F(1,10),F(9,10)];outcomes=[0,1]
    weighted=sum(w*y for w,y in zip(weights,outcomes))/sum(weights)
    # Duplicated visits are not independent customers.
    customers,visits,rho=20,25,F(3,5)
    naive=F(1,customers*visits);correct=naive*(1+(visits-1)*rho)
    assert correct==F(77,2500)
    return dict(gaussian_equivalence=dict(covariance=[[1,rational(beta)],[rational(beta),1]],residual_variance=rational(noise),dose_shift=1,response_forward=rational(beta),response_reverse=0,dollars_per_response_unit=100,action_cost_usd=20,net_forward_usd=30,net_reverse_usd=-20),counterfactual_coupling=dict(observed_joint_uniform=True,both_interventional_probabilities=rational(F(1,2)),observed_A=0,observed_Y=0,counterfactual_Y_A1_world1=0,counterfactual_Y_A1_world2=1),manipulated_resampling=dict(original_manipulated_rows=[2],resampled_rows=sample,literal_match_positions=literal,correct_replicate_positions=desired),bootstrap_strength=dict(forward_count=rational(forward),reverse_count=rational(backward),adjacency_strength=rational(strength),conditional_direction=rational(direction),directed_frequency=rational(F(1,5))),query_denominators=dict(worker_mean=rational(worker_mean),pooled_ratio=rational(pooled),zero_acceptance_literal_result=0,zero_acceptance_scientific_result='unresolved_no_accepted_samples'),weight_retention=dict(weighted_mean=rational(weighted),unweighted_mean=rational(F(1,2))),intervention_distribution=dict(two_selected_levels_uniform_mean=50,requested_90_10_mixture_mean=10),gaussian_metadata=dict(original_fitted_values=[1,2],requested_fixed_value=5,expected_fitted_values=[5,5],literal_retained_fitted_values=[1,2],literal_residuals=[0,0],status='static field-assignment witness, not native output'),dependent_sampling=dict(naive_variance=rational(naive),cluster_variance=rational(correct)),economics=dict(total_usd=1200,requests=100,conformant=80,useful=50,per_request=12,per_conformant=15,per_useful=24),native_execution=False)
if __name__=='__main__':
    path=ROOT/'docs/program/execution/2026-10-24/bnlearn-reuse-v1/exact-results.json'
    assert not path.exists();path.write_text(json.dumps(calculate(),indent=2)+'\n');print('Exact bnlearn semantic witnesses pass; no native execution.')
