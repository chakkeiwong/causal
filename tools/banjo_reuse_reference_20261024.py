#!/usr/bin/env python3
"""Authored mathematical witnesses; never imports or runs Banjo code."""
from fractions import Fraction as F
from math import lgamma, log, isclose
import json

def rising(a,n):
    out=F(1)
    for k in range(n):out*=a+k
    return out

def marginal(rows,alpha):
    q=len(rows);r=len(rows[0]);value=F(1)
    assert alpha>0 and all(len(row)==r for row in rows)
    for row in rows:
        assert all(isinstance(n,int) and n>=0 for n in row)
        for n in row:value*=rising(alpha/(q*r),n)
        value/=rising(alpha/q,sum(row))
    numerical=sum(lgamma(float(alpha/q))-lgamma(float(alpha/q)+sum(row))+
                  sum(lgamma(float(alpha/(q*r))+n)-lgamma(float(alpha/(q*r))) for n in row)
                  for row in rows)
    assert isclose(log(float(value)),numerical,abs_tol=1e-12)
    return value

def intervals(values,k=2):
    values=sorted(set(values));lo,hi=min(values),max(values)
    if len(values)<=k:return {v:i for i,v in enumerate(values)}
    return {v:min(k-1,int((v-lo)*k/(hi-lo))) for v in values}

def compare_stub(score_a,counts_a,edges_a,score_b,counts_b,edges_b):
    if score_a!=score_b:return -1 if score_a>score_b else 1
    if sum(counts_a)!=sum(counts_b):return 1 if sum(counts_a)>sum(counts_b) else -1
    for a,b in zip(counts_a,counts_b):
        if a!=b:return 1 if a>b else -1
    return 0 if edges_a==edges_b else 1

def calculate():
    p=marginal([[2,0],[0,2]],F(2));n=marginal([[2,2]],F(2))
    pd=marginal([[4,0],[0,4]],F(2));nd=marginal([[4,4]],F(2))
    assert (p,n,p/n)==(F(9,64),F(1,30),F(135,32))
    files=[[('A',i) for i in range(4)],[('B',i) for i in range(3)]]
    safe=[(s[t-1],s[t]) for s in files for t in range(1,len(s))]
    pooled=files[0]+files[1];unsafe=list(zip(pooled,pooled[1:]))
    crossing=[pair for pair in unsafe if pair[0][0]!=pair[1][0]]
    assert len(safe)==5 and len(unsafe)==6 and len(crossing)==1
    train=intervals([0,1,2]);joint=intervals([0,1,2,100])
    assert train[1]==1 and joint[1]==0
    # Two time-respecting, one-parent graphs on X,Y,Z with equal parent counts.
    a={('X','Y',1),('X','Z',1)};b={('Z','Y',1),('Y','Z',1)}
    ab=compare_stub(F(0),[0,1,1],a,F(0),[0,1,1],b)
    ba=compare_stub(F(0),[0,1,1],b,F(0),[0,1,1],a)
    assert (ab,ba)==(1,1)
    # Category 1 occurs only in the first (lag-only) row.
    sequence=[1,0,0];current=sequence[1:];lagged=sequence[:-1]
    declared=max(current)+1;actual=max(current+lagged)+1
    assert declared==1 and actual==2 and max(lagged)>=declared
    # Equal observational law, distinct intervention responses.
    law={(0,0):F(1,2),(1,1):F(1,2)}
    effects={'hidden_common_cause':F(0),'causal_action':F(1)}
    costs=[F(9000,d) for d in [300,225,150]]
    assert costs==[F(30),F(40),F(60)]
    result=dict(kind='authored_exact_witnesses_not_native_execution',
        score=dict(parent=str(p),no_parent=str(n),bayes_factor=str(p/n),
                   duplicated_parent=str(pd),duplicated_no_parent=str(nd),duplicated_bayes_factor=str(pd/nd),
                   independent_log_gamma_check=True),
        lag=dict(valid_transitions=len(safe),pooled_transitions=len(unsafe),cross_file_false_transitions=crossing,
                 example_959_rows_lag1=958),
        discretization=dict(training_map=train,joint_map=joint,training_value_1_changed=train[1]!=joint[1]),
        cardinality=dict(current_only=declared,lag_inclusive=actual,sequence=sequence,conditional_source_boundary=True),
        comparator=dict(a_vs_b=ab,b_vs_a=ba,antisymmetry=False,native_failure_observed=False),
        identification=dict(observational_joint={str(k):str(v) for k,v in law.items()},effects={k:str(v) for k,v in effects.items()},
                            hypothetical_net_usd={k:str(1000*F(50)*v-F(10000)) for k,v in effects.items()}),
        retained_subset=dict(uniform_graphs=4,retained_graphs=2,edge_probability_all='1/2',edge_frequency_retained='1'),
        economics=dict(total_hypothetical_usd=9000,submitted=300,completed=225,qualified=150,costs_usd=[str(x) for x in costs]),
        native_execution=False)
    return json.loads(json.dumps(result))

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
