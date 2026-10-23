#!/usr/bin/env python3
"""Authored denominator and estimand checks; no benchmark/model execution."""
from fractions import Fraction as F
from itertools import product

def feasible(n,percent,decimals):
    # Strict interior of ordinary nearest-rounding interval, enough for these examples.
    p=F(str(percent));half=F(1,2*10**decimals)
    return [k for k in range(n+1) if p-half<=F(100*k,n)<p+half]

def calculate():
    human=[dict(n=n,reported_percent=p,decimals=d,possible_success_counts=feasible(n,p,d)) for n,p,d in [(200,'86.3',1),(200,'89.7',1),(200,'91.8',1),(200,'90.0',1),(200,'13.2',1),(60,'63.0',1),(10,'78',0),(10,'58',0),(10,'45',0),(10,'37',0),(20,'58.0',1)]]
    assert human[0]['possible_success_counts']==[] and human[3]['possible_success_counts']==[180]
    assert feasible(600,'86.3',1)==[518]
    # Six equiprobable options, one correct: expected score zero; strict accuracy1/6.
    score=F(1,6)*1+F(5,6)*F(-1,5);assert score==0
    # Agent A is sometimes correct; agent B abstains. Ranking can differ.
    a=(F(1,10),F(1,10)-F(9,10)*F(1,5));b=(F(0),F(0));assert a[0]>b[0] and a[1]<b[1]
    # Each case contains same-sign question contributions. Two independent cases,
    # ten perfectly correlated questions per case; mean has variance1/2, not1/20.
    v=sum((F(z1+z2,2))**2 for z1,z2 in product([-1,1],repeat=2))/4
    assert v==F(1,2)
    # Deterministic derivation provenance alone need not identify intervention.
    # U fair: world1 A=U,Y=A; world2 A=U,Y=U. Observed (A,Y) identical.
    return dict(evidence_class='authored_exact_checks_not_native_benchmark',denominator_checks=human,annotation_level_alternative=dict(n=600,reported='86.3',possible_success_counts=[518],interpretation='Possible annotation-level rate does not reconcile stated majority-over200 denominator.'),scoring=dict(random_strict_accuracy='1/6',random_score='0',abstain_accuracy='0',abstain_score='0',agent_A_accuracy=str(a[0]),agent_A_score=str(a[1]),agent_B_accuracy=str(b[0]),agent_B_score=str(b[1])),selection=dict(total=1604,removed=190,evaluated=1414,removed_fraction=str(F(190,1604)),meaning='Closed-book filter defines selected benchmark population; does not establish contamination truth.'),dependence=dict(cases=2,questions_per_case=10,true_mean_variance=str(v),incorrect_question_independence='1/20',ratio='10'),causal_worlds=dict(observed_law={'00':'1/2','11':'1/2'},world1_effect='1',world2_effect='0',interpretation='Same observed records can support a provenance trace in both worlds; intervention semantics require structural assumptions.'),native_execution=False)
if __name__=='__main__':
 import json
 print(json.dumps(calculate(),indent=2))
