#!/usr/bin/env python3
"""Exact authored witnesses; does not import or execute vendor code."""
from fractions import Fraction as F
import json

def calculate():
    rows=[]
    for u in [0,1]:
        for a in [0,1]:
            rows.append((u,a,F(1,2)*(F(4,5) if a==u else F(1,5))))
    conditional={a:sum(p*u for u,t,p in rows if t==a)/sum(p for u,t,p in rows if t==a) for a in [0,1]}
    intervention={a:sum(F(1,2)*u for u in [0,1]) for a in [0,1]}
    assert sum(p for _,_,p in rows)==1
    assert conditional=={0:F(1,5),1:F(4,5)} and intervention=={0:F(1,2),1:F(1,2)}
    old={'id':'branch_17','model':'m1','data':'d1','engine':'e1','query':'q1'}
    new=dict(old,model='m2',data='d2')
    assert old['id']==new['id'] and tuple(old.items())!=tuple(new.items())
    total=1200+1800+4000+1000
    return dict(kind='exact_authored_examples_not_vendor_results',confounding=dict(observed_means={str(a):str(v) for a,v in conditional.items()},intervention_means={str(a):str(v) for a,v in intervention.items()},observed_contrast=str(conditional[1]-conditional[0]),intervention_contrast=str(intervention[1]-intervention[0])),cache=dict(old=old,new=new,id_only_skip=True,full_identity_match=False,stipulated_old_result='1/5',stipulated_new_result='4/5',stale_error='3/5'),cost=dict(currency='USD',measured=False,total=total,attempts=200,completions=160,admissible=100,per_attempt=str(F(total,200)),per_completion=str(F(total,160)),per_admissible=str(F(total,100))),native_execution=False)

if __name__=='__main__':
    print(json.dumps(calculate(),indent=2))
