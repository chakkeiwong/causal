#!/usr/bin/env python3
"""Authored finite measurement and mechanism examples; no model execution."""
from fractions import Fraction as F
from itertools import product
import json

def calculate():
    prevalence=F(1,5)
    treated=dict(sensitivity=F(9,10),specificity=F(9,10))
    control=dict(sensitivity=F(7,10),specificity=F(19,20))
    observed=[];accuracy=[]
    for arm in [treated,control]:
        observed.append(arm['sensitivity']*prevalence+(1-arm['specificity'])*(1-prevalence))
        accuracy.append(arm['sensitivity']*prevalence+arm['specificity']*(1-prevalence))
    assert observed==[F(13,50),F(9,50)] and accuracy==[F(9,10)]*2
    apparent_contrast=observed[0]-observed[1];loss_bias=1000*apparent_contrast
    assert apparent_contrast==F(2,25) and loss_bias==80
    n=5;rho=F(4,5);variance=(1+(n-1)*rho)/n;effective=n/(1+(n-1)*rho)
    assert variance==F(21,25) and effective==F(25,21)
    joint_one={};joint_zero={}
    for u in [0,1]:
        x=u;joint_one[(x,x)]=F(1,2);joint_zero[(x,u)]=F(1,2)
    assert joint_one==joint_zero
    do_one=sum(F(1,2)*((1)-(0)) for u in [0,1])
    do_zero=sum(F(1,2)*(u-u) for u in [0,1])
    assert (do_one,do_zero)==(1,0)
    clean,corrupt,restore=F(9,10),F(1,5),F(4,5)
    restoration=(restore-corrupt)/(clean-corrupt)
    assert restoration==F(6,7)
    answered=90;correct=81;requests=100
    answered_accuracy=F(correct,answered);coverage=F(answered,requests);correct_per_request=F(correct,requests)
    assert (answered_accuracy,coverage,correct_per_request)==(F(9,10),F(9,10),F(81,100))
    cost=F(240);assert cost/requests==F(12,5) and cost/answered==F(8,3) and cost/correct==F(80,27)
    return dict(scope='Exact authored finite examples; no model, benchmark reproduction, validated bank causal effect or real price.',measurement=dict(prevalence=str(prevalence),treated_observed=str(observed[0]),control_observed=str(observed[1]),both_accuracy=str(accuracy[0]),true_contrast='0',apparent_contrast=str(apparent_contrast),stipulated_1000usd_loss_bias=str(loss_bias)),prompt_dependence=dict(prompts=n,correlation=str(rho),independent_mean_variance='1/5',correlated_mean_variance=str(variance),effective_independent_equivalents=str(effective)),observational_equivalence=dict(observed_pairs={str(k):str(v) for k,v in joint_one.items()},effect_world_one=str(do_one),effect_world_zero=str(do_zero),model_activation_restoration=str(restoration),activation_restoration_does_not_resolve_world=True),refusal=dict(requests=requests,answered=answered,correct=correct,answered_accuracy=str(answered_accuracy),coverage=str(coverage),correct_per_request=str(correct_per_request)),stipulated_cost_usd=dict(total=str(cost),per_request=str(cost/requests),per_answer=str(cost/answered),per_correct_artifact=str(cost/correct)))

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
