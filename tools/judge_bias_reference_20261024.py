#!/usr/bin/env python3
"""Authored exact metric witnesses, not a replication of MLLM experiments."""
from fractions import Fraction as F
import json

def bd(pairs):
    eligible=[F(max(y-z,0),y-1) for y,z in pairs if y>1]
    return sum(eligible,F(0))/len(eligible) if eligible else None

def bc(pairs,S=10):
    return sum((1-F(abs(y-z),max(y-1,S-y)) for y,z in pairs),F(0))/len(pairs)

def calculate():
    constant=[(7,7)]*4
    assert bc(constant)==1 and bd(constant)==0
    truth=[0,0,1,1];accepted=[1]*4
    false_accepts=sum(a and not t for a,t in zip(accepted,truth));assert false_accepts==2
    floor_pairs=[(10,1),(1,1)];assert bd(floor_pairs)==1
    assert sum(y>1 for y,_ in floor_pairs)==1
    upper=F(max(10-8,0),10-1);lower=F(max(3-1,0),3-1)
    assert upper==F(2,9) and lower==1
    all_success=F(45,100);conditional_success=F(45,50)
    assert all_success==F(9,20) and conditional_success==F(9,10)
    false_accept_cost=F(2,1)*250000;review_cost=4*1000
    assert false_accept_cost==500000 and review_cost==4000
    costs=[F(15000,n) for n in [100,50,45]]
    # Three attempts on the same logical case do not add new independent cases.
    logical=list(range(100));attempts=[(i,k) for i in logical for k in range(3)]
    assert len(attempts)==300 and len({i for i,_ in attempts})==100
    return json.loads(json.dumps(dict(kind='authored_exact_metric_witnesses',constant_score_BC=bc(constant),
        constant_score_BD=bd(constant),false_accepts=false_accepts,floor_conditioned_BD=bd(floor_pairs),
        floor_eligible=1,floor_total=2,equal_raw_drop_BD=[upper,lower],
        conditional_success=conditional_success,all_request_success=all_success,
        false_accept_loss_usd=false_accept_cost,review_cost_usd=review_cost,
        cost_per_submitted_scored_qualified_usd=costs,attempts=300,logical_cases=100,native_execution=False),
        default=lambda x:str(x) if isinstance(x,F) else x))

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
