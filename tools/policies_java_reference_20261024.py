#!/usr/bin/env python3
"""Exact authored witnesses; imports or executes no downloaded implementation."""
from fractions import Fraction as F
import json

def calculate():
    g=F(1,2);phi=F(1);next_phi=F(101,50);B=F(100)
    denominator=1+(phi-g*next_phi)*B*phi
    assert denominator==0 and 1/B+phi*(phi-g*next_phi)==0
    old=F(4);alpha=F(1,10);reward=F(2);discount=F(7,10)
    q_target=reward+discount*8;sarsa_target=reward+discount*1
    q_update=old+alpha*(q_target-old);sarsa_update=old+alpha*(sarsa_target-old)
    terminal_update=old+alpha*(reward-old)
    actor_literal=reward+8-4;actor_discounted=reward+discount*8-4
    standard=2+F(9,10)*10;double=2+F(9,10)*1
    clamp=lambda x:min(F(5),max(F(3),x))
    reveal=-1+F(9,10)*10;wait=F(9,10)*5;qmdp_wait=F(9,10)*10
    nominal_value=F(1)/(1-F(9,10));actual_value=F(2)/(1-F(9,10))
    assert (q_update,sarsa_update,terminal_update)==(F(109,25),F(387,100),F(19,5))
    assert (standard,double,clamp(standard),clamp(double),clamp(F(2)))==(11,F(29,10),5,3,3)
    assert (reveal,wait,qmdp_wait,reveal-wait)==(8,F(9,2),9,F(7,2))
    result=dict(lspi=dict(inverse_seed=B,phi=phi,next_phi=next_phi,gamma=g,denominator=denominator,regularized_scalar_matrix=F(0)),
      td=dict(q_target=q_target,sarsa_target=sarsa_target,terminal_target=reward,q_update=q_update,sarsa_update=sarsa_update,terminal_update=terminal_update,actor_literal=actor_literal,actor_discounted=actor_discounted),
      dqn=dict(standard=standard,double=double,clamped_standard=clamp(standard),clamped_double=clamp(double),clamped_terminal=clamp(F(2))),
      information=dict(reveal=reveal,wait=wait,qmdp_wait=qmdp_wait,regret=reveal-wait),
      supplied_model=dict(nominal_value=nominal_value,nominal_residual=1+F(9,10)*nominal_value-nominal_value,actual_value=actual_value,error=actual_value-nominal_value),
      tie=dict(uniform_two_action_value=F(5),first_action_value=F(10)),
      interpretation='Authored finite counterexamples and literal equation calculations; no upstream run, statistical calibration or bank evidence.')
    return json.loads(json.dumps(result,default=lambda x:str(x)))
if __name__=='__main__':print(json.dumps(calculate(),indent=2))
