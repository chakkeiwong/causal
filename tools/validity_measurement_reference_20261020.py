#!/usr/bin/env python3
"""Authored exact measurement model for a proposed causal-assistant evaluation."""
from fractions import Fraction as F
import json


def reported(p,s,c):return s*p+(1-c)*(1-p)


def invert(q,s,c):
    if s+c==1:return None
    return (q+c-1)/(s+c-1)


def calculate():
    p=F(3,5)
    s0,c0=F(4,5),F(9,10);s1,c1=F(19,20),F(4,5)
    q0,q1=reported(p,s0,c0),reported(p,s1,c1)
    assert (q0,q1)==(F(13,25),F(13,20)) and q1-q0==F(13,100)
    assert invert(q0,s0,c0)==invert(q1,s1,c1)==p
    invariant=[reported(x,s0,c0) for x in [F(1,2),F(7,10)]]
    assert invariant[1]-invariant[0]==F(7,50)
    assert (invariant[1]-invariant[0])/(s0+c0-1)==F(1,5)
    assert invert(F(1,2),F(1,2),F(1,2)) is None
    assert reported(F(1,10),F(1,2),F(1,2))==reported(F(9,10),F(1,2),F(1,2))
    # Generated correctness law; grades are one noisy measurement of that law.
    value=F(100);extra=F(8)
    true_increment=value*(p-p)-extra;apparent=value*(q1-q0)-extra
    assert true_increment==-8 and apparent==5
    # Z_jr = U + V_j + e_jr: independent zero-mean components, with shared U.
    # Averaging repeats removes neither U nor covariance between cluster means.
    shared_var, cluster_var, noise_var, repeats = F(1,4), F(1,2), F(1), 20
    mean_var = shared_var+cluster_var+noise_var/repeats
    assert mean_var==F(4,5) and shared_var/mean_var==F(5,16)
    return dict(kind='project_authored_exact_measurement_reference',model_executed=False,bank_data=False,
        varying_measurement=dict(true_success_probability=str(p),
            arm0=dict(sensitivity=str(s0),specificity=str(c0),pass_rate=str(q0)),
            arm1=dict(sensitivity=str(s1),specificity=str(c1),pass_rate=str(q1)),
            observed_difference=str(q1-q0),true_difference='0',corrected_probabilities=['3/5','3/5']),
        invariant_measurement=dict(sensitivity=str(s0),specificity=str(c0),true_probabilities=['1/2','7/10'],
            observed_difference='7/50',corrected_difference='1/5',slope='7/10'),
        uninformative_grader=dict(sensitivity='1/2',specificity='1/2',identified=False),
        shared_shock=dict(model='Z_jr=U+V_j+e_jr; all distinct components independent',
            shared_variance=str(shared_var),cluster_variance=str(cluster_var),noise_variance=str(noise_var),
            repeats=repeats,cluster_mean_variance=str(mean_var),
            cross_cluster_mean_covariance=str(shared_var),cross_cluster_mean_correlation='5/16'),
        illustrative_economics=dict(value_per_correct_result_usd=str(value),incremental_workflow_cost_usd=str(extra),
            actual_expected_increment_usd=str(true_increment),grade_based_increment_usd=str(apparent)),
        limitations=['Imposed binary correctness and grading law; not a live assistant study or observed bank value.',
            'Known sensitivity/specificity are assumptions here; real calibration requires held-out adjudication and its uncertainty.',
            'The model assumes calibration transports within each declared arm and population; subgroup drift requires richer strata.',
            'Repeated outputs or aggregate scores alone cannot supply missing independent units or identify an uninformative grader.'])


if __name__=='__main__':print(json.dumps(calculate(),indent=2))
