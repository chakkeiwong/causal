#!/usr/bin/env python3
"""Authored finite-law witnesses, without importing downloaded package code."""
from fractions import Fraction as F
import json
def calculate():
    p,e=F(4,5),F(1,2)
    # Y=A, working response=0; selected source and treatment stabilization constants.
    transport_default=p*e/(1-p)
    generalize_default=p*e
    correct_transport=p*e*((1-p)/p)*(1/e)/(1-p)
    assert (transport_default,generalize_default,correct_transport)==(2,F(2,5),1)
    q=[F(0),F(2),F(4)];between=sum((x-2)**2 for x in q)/2
    covariance=[[1+F(4,3)*between,F(4,3)*between],[F(4,3)*between,1+F(4,3)*between]]
    diff_var=covariance[0][0]+covariance[1][1]-2*covariance[0][1]
    assert diff_var==2
    s=lambda x:str(x)
    return dict(
      zepid=dict(law='P(S=1)=4/5,P(A=1)=1/2,Y=A,working_outcome=0',true_target=1,selected_stabilized_transport=s(transport_default),selected_stabilized_generalize=s(generalize_default),unstabilized_sampling_and_treatment_reference=s(correct_transport)),
      causallib=dict(prevalence=['1/4','3/4'],propensities=['1/2','1/2'],selected_row_stabilized_matrix=[['1/2','1/2'],['3/2','3/2']],column_stabilized_reference=[['1/2','3/2'],['1/2','3/2']],observed_diagonal_agrees=True),
      clipping=dict(original=['98/100','1/100','1/100'],lower='1/10',upper='9/10',clipped=['9/10','1/10','1/10'],row_sum='11/10',simplex_preserved=False),
      imputation=dict(binary_probability='1/4',stochastic_mean='1/4',stochastic_variance='3/16',modal_completion=0,modal_variance_conditional_on_prediction=0,other_training_randomness_not_claimed_zero=True),
      pooling=dict(parameter_pairs=[[0,0],[2,2],[4,4]],within_covariance=[[1,0],[0,1]],pooled_covariance=[[s(v) for v in row] for row in covariance],contrast_variance=s(diff_var),variance_if_cross_covariance_discarded='38/3'),
      missingness_fisher=dict(unconditional_rows=3,conditioning_variables=0,z_multiplier=0,nominal_p_if_finite_correlation=1,requires_explicit_sample_size_policy=True),
      economics=dict(customers=10000,usd_per_unit=10,hypothetical_transport_discrepancy_usd=100000),
      native_execution=False,empirical_bank_evidence=False)
if __name__=='__main__':print(json.dumps(calculate(),indent=2))
