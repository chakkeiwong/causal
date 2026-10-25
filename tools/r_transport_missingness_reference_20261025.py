#!/usr/bin/env python3
"""Authored finite-law references; never imports or executes retrieved packages."""
from fractions import Fraction as F
import json

def calculate():
    p = F(4, 5)
    law = [(s, a, (p if s else 1-p)*F(1, 2))
           for s in (0, 1) for a in (0, 1)]
    correct = sum(prob*s*(1-p)/p*a/F(1, 2) for s,a,prob in law)/(1-p)
    reversed_odds = sum(prob*s*p/(1-p)*a/F(1, 2) for s,a,prob in law)/(1-p)
    assert correct == 1 and reversed_odds == 16
    q = [F(0), F(2), F(4)]
    mean = sum(q)/len(q)
    between = sum((v-mean)**2 for v in q)/(len(q)-1)
    missing_total = 1+(1+F(1,len(q)))*between
    synthetic_total = 1+between/len(q)
    assert missing_total == F(19,3) and synthetic_total == F(7,3)
    normalized_ess = 1/(F(1,4)**2+F(3,4)**2)
    raw_ess = 1/(F(1)**2+F(3)**2)
    assert normalized_ess == F(8,5) and raw_ess == F(1,10)
    posterior = (F(1,2)*F(4,5))/(F(1,2)*F(4,5)+F(1,2)*F(1,5))
    assert posterior == F(4,5)
    # Missing stratum has mass 0.3. An elicited delta of 2 moves its mean contribution.
    delta_shift = F(3,10)*2
    # Explicit finite-rejection example, not an observed package failure frequency.
    no_acceptance = F(9,10)**(24+2)
    result = {
        'transport': {'selection_probability':str(p), 'true_target_effect':str(correct),
                      'selected_reversed_odds_score':str(reversed_odds),
                      'known_propensity_misspecified_zero_outcome_model':True},
        'hajek_branch': {'n':10,'constant_treatment_probability':'1/2',
                        'selected_residual_divisor':5,'residual_factor':'1/5'},
        'binary_scale': {'risk0':'1/10','risk1':'1/5','risk_difference':'1/10','odds_ratio':'9/4'},
        'joint_support': {'source':[[0,0],[1,1]],'target':[0,1],
                          'passes_coordinate_ranges':True,'joint_support':False},
        'pooling': {'mean':str(mean),'between':str(between),
                    'missing_data_total':str(missing_total),'synthetic_data_total':str(synthetic_total)},
        'compatible_binary_imputation':{'prior':'1/2','posterior_given_outcome':str(posterior)},
        'mnar':{'missing_fraction':'3/10','elicited_delta':2,'mean_shift':str(delta_shift)},
        'pmm':{'observed_donors':[0,1],'hypothetical_missing_value':2,
               'donor_rule_can_generate_two':False},
        'rejection':{'first_stage_attempts':24,'second_stage_limit':2,
                    'constant_acceptance':'1/10','all_rejected_probability':str(no_acceptance)},
        'effective_sample_size':{'weights':[1,3],'normalized':str(normalized_ess),
                                 'unnormalized_numeric_delegate':str(raw_ess)},
        'economics':{'customers':10000,'usd_per_outcome_unit':10,
                     'hypothetical_transport_score_discrepancy_usd':int((reversed_odds-correct)*10000*10)},
        'native_execution':False,'empirical_bank_evidence':False
    }
    assert result['economics']['hypothetical_transport_score_discrepancy_usd']==1500000
    return result

if __name__=='__main__':
    print(json.dumps(calculate(),indent=2))
