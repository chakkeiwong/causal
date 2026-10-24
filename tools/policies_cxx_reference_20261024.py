#!/usr/bin/env python3
"""Exact authored policy-contract witnesses; no imported third-party implementation."""
from fractions import Fraction as F
import json

def calculate():
    h=[F(4,5),F(1,5)];pi=[F(1,5),F(4,5)];cost=[F(20),F(100)];pred=[F(10),F(80)]
    truth=sum(p*c for p,c in zip(pi,cost));ips=sum(hh*pp/ hh*c for hh,pp,c in zip(h,pi,cost))
    clip=F(2,5);clipped=sum(hh*pp/max(hh,clip)*c for hh,pp,c in zip(h,pi,cost))
    dr=sum(pp*q for pp,q in zip(pi,pred))+sum(hh*pp/hh*(c-q) for hh,pp,c,q in zip(h,pi,cost,pred))
    clipped_dr=sum(pp*q for pp,q in zip(pi,pred))+sum(hh*pp/max(hh,clip)*(c-q) for hh,pp,c,q in zip(h,pi,cost,pred))
    assert truth==ips==dr==84 and clipped==44 and clipped_dr==76
    gamma=F(9,10);reward=F(10);v=reward;limit=reward/(1-gamma);assert limit==100 and limit-v==90
    residual=abs(reward+gamma*v-v);assert residual/(1-gamma)==90
    # Literal zero-tolerance reporting convention is not a measured Bellman residual.
    terminal=reward;wrong_terminal=reward+gamma*50;assert wrong_terminal==55
    # Policy evaluation is distinct from maximizing next-action continuation.
    eval_next=F(1,4)*20+F(3,4)*4;control_next=max(20,4);assert eval_next==8 and control_next==20
    ordinary=3+gamma**3*10;single_discount=3+gamma*10;assert ordinary==F(1029,100) and single_discount==12
    # Categorical projection coefficients at an exact atom are both zero unless separately repaired.
    b=F(1);lo=hi=1;mass=F(1);literal_mass=mass*(hi-b)+mass*(b-lo);assert literal_mass==0
    # Explicit finite unsupported-action worlds share observations but disagree off support.
    unsupported_values=[F(0),F(100)];assert unsupported_values[0]!=unsupported_values[1]
    # Two equally likely future states: stale next-state greedy action differs from current-state greedy action.
    q_current=[F(10),F(0)];q_next=[F(0),F(10)];epsilon=F(1,10);behavior=F(1,2)
    selected_next=1;ratio_literal=(epsilon/2+(1-epsilon)*int(0==selected_next))/behavior
    ratio_current=(epsilon/2+(1-epsilon)*int(0==0))/behavior
    assert ratio_literal==F(1,10) and ratio_current==F(19,10)
    # Gross payoff versus normalized monetary costs must keep bounds and sign conventions.
    drift=[F(1,5),F(4,5)];assert sum(drift)/2==F(1,2)
    def clean(x):
        if isinstance(x,F):return dict(numerator=x.numerator,denominator=x.denominator,decimal=float(x))
        if isinstance(x,dict):return {k:clean(v) for k,v in x.items()}
        if isinstance(x,list):return [clean(v) for v in x]
        return x
    return clean(dict(bandit_cost=dict(true=truth,ips=ips,dr=dr,clipped_ips=clipped,clipped_dr=clipped_dr,reported_cost_100_over_zero_replaced_by_point001=100000),finite_model=dict(one_iteration=v,infinite_horizon=limit,error=limit-v,bellman_residual=residual,returned_variation_when_tolerance_disabled=0),terminal=dict(correct=terminal,unabsorbed_next_value=wrong_terminal),policy_target=dict(fixed_policy_continuation=eval_next,maximum_continuation=control_next),categorical=dict(three_step_target=ordinary,single_discount_target=single_discount,exact_atom_literal_mass=literal_mass,correct_preserved_mass=1),control_trace=dict(next_state_selected_action=selected_next,source_expression_ratio=ratio_literal,current_state_epsilon_greedy_ratio=ratio_current),unsupported_world_values=unsupported_values,time_varying=dict(average=F(1,2),latest=F(4,5)),cost=dict(total_usd=900,requests=100,conformant=75,useful=45,per_request=9,per_conformant=12,per_useful=20)))
if __name__=='__main__':print(json.dumps(calculate(),indent=2))
