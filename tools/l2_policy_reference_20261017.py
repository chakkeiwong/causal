#!/usr/bin/env python3
"""Finite authored decision laws, independent of any fitted causal model."""
from fractions import Fraction as F
import json


def calculate():
    reward=lambda a,l,b:F(100)+20*a-40*l+30*b*l-10*b
    value=lambda a,rule:sum((F(3,4) if a else F(1,4))**l *
        (F(1,4) if a else F(3,4))**(1-l)*reward(a,l,rule(l)) for l in [0,1])
    adaptive=[value(a,lambda l:l) for a in [0,1]]
    nofollow=[value(a,lambda l:0) for a in [0,1]]
    always=[value(a,lambda l:1) for a in [0,1]]
    assert adaptive==[95,105] and nofollow==[90,90] and always==[F(175,2),F(205,2)]
    conditional=[reward(1,l,l)-reward(0,l,l) for l in [0,1]]
    assert conditional==[20,20]
    logger=[]
    for a in [0,1]:
        for l in [0,1]:
            pl=(F(3,4) if a else F(1,4)) if l else (F(1,4) if a else F(3,4))
            for b in [0,1]:logger.append((a,l,b,F(1,4)*pl,reward(a,l,b)))
    replay=[sum(p*y*4 for a,l,b,p,y in logger if a==target and b==l) for target in [0,1]]
    assert replay==adaptive and sum(row[3] for row in logger)==1
    old_mass,new_mass=F(1,5),F(1,10)
    old_value=old_mass*F(100)
    favorable_value=old_value+new_mass*F(50)
    adverse_value=old_value-new_mass*F(50)
    lower,upper=new_mass*(-F(200)),new_mass*F(100)
    return dict(sequential=dict(adaptive_values=adaptive,no_followup_values=nofollow,
        always_followup_values=always,adaptive_first_offer_contrast=adaptive[1]-adaptive[0],
        controlled_state_contrasts=conditional,static_first_offer_contrast=nofollow[1]-nofollow[0],
        adaptive_vs_never=adaptive[1]-nofollow[0],logger_reweighted_values=replay),
        threshold=dict(old_value_per_applicant=old_value,new_approved_mass=old_mass+new_mass,
          favorable_total_value=favorable_value,adverse_total_value=adverse_value,
          favorable_increment=favorable_value-old_value,adverse_increment=adverse_value-old_value,
          favorable_mean_approved=favorable_value/(old_mass+new_mass),
          adverse_mean_approved=adverse_value/(old_mass+new_mass),
          bounded_increment=[lower,upper]),bank_evidence=False)


def serial(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {k:serial(v) for k,v in x.items()}
    if isinstance(x,list):return [serial(v) for v in x]
    return x


if __name__=='__main__':print(json.dumps(serial(calculate()),indent=2))
