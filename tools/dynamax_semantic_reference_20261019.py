#!/usr/bin/env python3
"""Authored exact private-logger and information-clock examples; no Dynamax run."""
from fractions import Fraction as F
from itertools import product
import json


def calculate():
    # Z is persistent latent repayment propensity. A is an informative observed action,
    # Y depends only on Z; intervening on A cannot change Y in this stipulated model.
    joint={}
    for z,a,y in product([0,1],repeat=3):
        joint[z,a,y]=F(1,2)*(F(9,10) if a==z else F(1,10))*(F(4,5) if y==z else F(1,5))
    assert sum(joint.values())==1
    p_a=lambda a:sum(v for (z,b,y),v in joint.items() if b==a)
    y_given_a=[sum(v for (z,b,y),v in joint.items() if b==a and y==1)/p_a(a) for a in [0,1]]
    observed=y_given_a[1]-y_given_a[0]
    intervention=F(0)
    joint_a1y1=sum(v for (z,a,y),v in joint.items() if a==1 and y==1)
    posterior=joint[1,1,1]/joint_a1y1
    assert y_given_a==[F(13,50),F(37,50)] and observed==F(12,25)
    assert posterior==F(36,37) and joint_a1y1==F(37,100)
    # Separate persistent-state example: two conditionally independent 80%-accurate
    # emissions, Y1=0 followed by Y2=1. A decision between them cannot use Y2.
    weights={z:F(1,2)*(F(4,5) if z==0 else F(1,5)) for z in [0,1]}
    filtered=weights[1]/sum(weights.values())
    smoothed_weights={z:weights[z]*(F(4,5) if z==1 else F(1,5)) for z in [0,1]}
    smoothed=smoothed_weights[1]/sum(smoothed_weights.values())
    assert filtered==F(1,5) and smoothed==F(1,2)
    return dict(kind='authored_exact_reference',upstream_execution=False,
        logger=dict(action_one_probability=str(p_a(1)),joint_action1_outcome1=str(joint_a1y1),
            outcome_given_action0=str(y_given_a[0]),outcome_given_action1=str(y_given_a[1]),
            posterior_state1_with_logger=str(posterior),posterior_omitting_logger='4/5',
            observational_contrast=str(observed),interventional_contrast=str(intervention),
            assumed_value_observational_usd=str(200*observed-20),assumed_value_causal_usd=str(200*intervention-20)),
        clocks=dict(filtered_state1=str(filtered),smoothed_state1=str(smoothed),
            assumed_online_net_usd=str(100*filtered-30),invalid_future_informed_net_usd=str(100*smoothed-30),
            assumed_rule='Contact earns100USD if latent Z=1 and costs30USD; known response rule is stipulated, not inferred.'),
        limitations=['Finite authored SCM and persistent-state examples; no package, numerical backend or bank trial.',
                    'Omitting an informative latent-state logger gives a different conditional law; externally fixed inputs are a distinct regime.',
                    'All currency values are assumptions. Parameter fitting and uncertainty coverage are not evaluated.'])


if __name__=='__main__':print(json.dumps(calculate(),indent=2))
