#!/usr/bin/env python3
"""Exact authored laws; does not import or execute retrieved package code."""
from fractions import Fraction as F
import json

def calculate():
    graphs=[{('A','B'),('B','C')},{('B','C'),('C','A')},{('C','A'),('A','B')}]
    edges=set.union(*graphs)
    counts={a+'->'+b:sum((a,b) in g for g in graphs) for a,b in sorted(edges)}
    assert set(counts.values())=={2}
    # Every input is a directed path, but pairwise majority closes the cycle.
    assert all(len(g)==2 for g in graphs)
    data=[(1,1,None),(-1,-1,None),(1,None,1),(-1,None,-1),(None,1,-1),(None,-1,1)]
    cov=[]
    for i in range(3):
        row=[]
        for j in range(3):
            pairs=[(F(r[i]),F(r[j])) for r in data if r[i] is not None and r[j] is not None]
            n=len(pairs);mi=sum(a for a,b in pairs)/n;mj=sum(b for a,b in pairs)/n
            row.append(sum((a-mi)*(b-mj) for a,b in pairs)/(n-1))
        cov.append(row)
    v=[-1,1,1];quadratic=sum(v[i]*cov[i][j]*v[j] for i in range(3) for j in range(3))
    assert quadratic==-8
    estimates=[F(0),F(2),F(4)];mean=sum(estimates)/3;between=sum((x-mean)**2 for x in estimates)/2
    pooled=F(1)+F(4,3)*between;assert pooled==F(19,3)
    target_mean=F(1,2)*0+F(1,2)*2
    source_mean=F(9,10)*0+F(1,10)*2
    weighted=(F(1)*0+F(3)*2)/4
    conditional_variance=F(1);parameter_variance=F(1,4)
    joint_difference=F(1)+F(1)-2*F(1);diagonal_difference=F(1)+F(1)
    return dict(kind='authored_exact_witnesses_not_native_execution',
        graph_majority=dict(member_edges=[[list(e) for e in sorted(g)] for g in graphs],counts=counts,frequency=str(F(2,3)),directed_cycle=['A','B','C','A']),
        pairwise_covariance=dict(matrix=[[str(x) for x in r] for r in cov],witness_vector=v,quadratic=str(quadratic)),
        conditional_draw=dict(parameter_variance=str(parameter_variance),conditional_variance=str(conditional_variance),total_variance=str(conditional_variance+parameter_variance),fixed_parameter_variance=str(conditional_variance)),
        singular_draw=dict(covariance=[[1,1],[1,1]],difference_variance_joint=int(joint_difference),difference_variance_diagonal=int(diagonal_difference)),
        pooling=dict(mean=str(mean),within='1',between=str(between),total=str(pooled)),
        weighted_completion=dict(values=[0,2],weights=[1,3],weighted_mean=str(weighted),unweighted_mean='1'),
        transport=dict(target_mean=str(target_mean),source_mean=str(source_mean),discrepancy=str(target_mean-source_mean)),
        economics=dict(hypothetical_accounts=10000,dollars_per_unit=10,discrepancy_usd=str((target_mean-source_mean)*10000*10)),
        native_execution=False)

if __name__=='__main__':
    print(json.dumps(calculate(),indent=2))
