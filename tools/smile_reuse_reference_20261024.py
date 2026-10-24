#!/usr/bin/env python3
"""Authored vendor-interface witnesses; no commercial engine executed."""
from fractions import Fraction as F
import json

def calculate():
    joint={(0,0):F(2,5),(0,1):F(1,10),(1,0):F(1,10),(1,1):F(2,5)}
    action_model={(a,y):F(1,2)*(F(4,5) if y==a else F(1,5)) for a,y in joint}
    reverse_model={(a,y):F(1,2)*(F(4,5) if a==y else F(1,5)) for a,y in joint}
    assert action_model==reverse_model==joint
    effect_action=F(4,5)-F(1,5);effect_reverse=F(0)
    assert effect_action==F(3,5)
    values=[2000*100*e-40000 for e in [effect_action,effect_reverse]]
    assert values==[80000,-40000]
    data=[F(4,5),F(1,5),F(3,5),F(2,5),F(3,10),F(7,10)]
    correct=[data[2*t] for t in range(3)];wrong=data[:3]
    assert correct[1]==F(3,5) and wrong[1]==F(1,5)
    temporal_difference=1000*100*(correct[1]-wrong[1]);assert temporal_difference==40000
    unseen_best=F(50);informed=F(100);voi=informed-unseen_best;assert voi==50
    return dict(kind='authored_exact_witnesses_not_vendor_execution',
        equivalent_graphs=dict(joint={str(k):str(v) for k,v in joint.items()},model_A_to_Y_effect=str(effect_action),model_Y_to_A_effect=str(effect_reverse),two_compatible_values_not_unrestricted_identified_set=True,incremental_net_usd=[str(v) for v in values]),
        initialization=dict(uniform_rows=['1/2','1/2'],not_estimated=True),
        temporal_layout=dict(slice_major=[str(v) for v in data],correct_first_outcome=[str(v) for v in correct],wrong_outcome_major=[str(v) for v in wrong],hypothetical_t1_value_difference_usd=str(temporal_difference)),
        information_clock=dict(best_without_observation_usd=str(unseen_best),with_perfect_predecision_observation_usd=str(informed),value_of_information_usd=str(voi),future_information_not_available=True),
        economics=dict(hypothetical_usd=24000,submitted=800,completed=600,qualified=400,costs_usd=[30,40,60]),native_execution=False)

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
