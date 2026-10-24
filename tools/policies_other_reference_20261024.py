#!/usr/bin/env python3
"""Exact authored policy semantics; no downloaded Julia/R execution."""
from fractions import Fraction as F
from itertools import product
import json

def ratio(x):
    x=F(x)
    return dict(numerator=x.numerator,denominator=x.denominator,decimal=float(x))

def calculate():
    gamma=F(9,10);cont=F(1,2);reward=F(6)
    infinite=reward/(1-gamma*cont);finite=reward*(1+gamma*cont)
    randomized=F(5)/(1-gamma/2)
    split=[F(0),F(10),F(0),F(10)/(1-gamma)]
    ratios=[F(2),F(0),F(2),F(2)];ys=[F(1),F(2),F(3),F(4)]
    partial={}
    for k in range(3):
        weighted=[ys[t]*__import__('functools').reduce(lambda a,b:a*b,ratios[t-k:t+1],F(1)) for t in range(k,len(ys))]
        partial[str(k)]=ratio(sum(weighted)/len(weighted))
    no_memory=F(0);full_information=F(10)
    stopped=F(5);continuation=F(-100);completed=stopped+continuation
    unit_equal=F(10+0,2);visit_equal=F(10*2,2+8)
    # Bernoulli behavior=.5 and deterministic target: k+1 matching actions.
    weight=[dict(k=k,nonzero_probability=ratio(F(1,2)**(k+1)),nonzero_weight=2**(k+1),second_moment=2**(k+1)) for k in [0,3,7]]
    horizon_tail=F(10)*F(9,10)**5/(1-F(9,10))
    def paper_reward(x):
        return -3 if x<=70 else -2 if x>150 else -1 if x<=80 or x>120 else 0
    def source_reward(x):
        return (-3 if x<70 else 0)+(-2 if x>150 else 0)+(-1 if 70<x<80 else 0)+(-1 if 120<x<150 else 0)
    thresholds=[dict(x=x,paper=paper_reward(x),selected_source=source_reward(x)) for x in [70,80,120,150]]
    assert infinite==F(120,11) and finite==F(87,10)
    assert randomized==F(100,11) and sum(split)/4==F(55,2)
    assert partial['0']['numerator']==4 and partial['1']['numerator']==16 and partial['1']['denominator']==3 and partial['2']['numerator']==0
    return dict(bellman=dict(infinite=ratio(infinite),two_step=ratio(finite),entry_reward=12,terminal_continuation=0),randomized_policy=dict(true_mixture_value=ratio(randomized),independent_matrix_reward_draw_values=[ratio(x) for x in split],mean_incoherent_value=ratio(sum(split)/4)),information=dict(observation_only_value=ratio(no_memory),state_informed_value=ratio(full_information),interpretation='Information changes the policy target;not a native experiment'),truncation=dict(gamma=ratio(F(9,10)),steps=5,reward_bound=10,worst_remaining_tail=ratio(horizon_tail)),partial_history=dict(ratios=[ratio(x) for x in ratios],outcomes=[int(y) for y in ys],estimates=partial),weights=weight,population=dict(equal_unit_value=ratio(unit_equal),pooled_visit_value=ratio(visit_equal)),captured_exception=dict(observed_prefix=ratio(stopped),stipulated_complete=ratio(completed),unknown_tail='Do not impute;return incomplete status'),source_boundary_witness=thresholds,lagged_feature=dict(previous=120,current=130,threshold=125,source_lagged_action=0,current_state_action=1),economics=dict(total_usd=2400,requests=100,conformant=80,useful=60,per_request=24,per_conformant=30,per_useful=40),native_execution=False)
if __name__=='__main__':print(json.dumps(calculate(),indent=2))
