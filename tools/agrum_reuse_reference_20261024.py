#!/usr/bin/env python3
"""Authored finite support/coupling witnesses; no acquired aGrUM code run."""
from fractions import Fraction as F
from itertools import product
import json

def calculate():
    supported=F(1,2)*F(1,2)
    low=supported;high=supported+F(1,2)
    assert (low,high)==(F(1,4),F(3,4))
    # U,V independent fair bits;profile E=1{U=V};W(a)=a XOR U XOR V.
    prior={(u,v):F(1,4) for u,v in product(range(2),repeat=2)}
    evidence=sum(p for (u,v),p in prior.items() if u==v)
    posterior={(u,v):p/evidence if u==v else F(0) for (u,v),p in prior.items()}
    marg_u={u:sum(p for (x,v),p in posterior.items() if x==u) for u in range(2)}
    marg_v={v:sum(p for (u,y),p in posterior.items() if y==v) for v in range(2)}
    joint_value=sum(p*(1^u^v) for (u,v),p in posterior.items())
    separate_value=sum(marg_u[u]*marg_v[v]*(1^u^v) for u,v in prior)
    assert (joint_value,separate_value)==(F(1),F(1,2))
    exact_net=1000*80*joint_value-30000;separate_net=1000*80*separate_value-30000
    p=[F(1,4),F(3,4)];q=[F(4,5),F(1,5)]
    shared=[a*b for a,b in zip(p,q)];shared=[v/sum(shared) for v in shared]
    distinct={(i,j):p[i]*q[j] for i,j in product(range(2),repeat=2)}
    mismatch=sum(v for (i,j),v in distinct.items() if i!=j)
    assert shared==[F(4,7),F(3,7)] and mismatch==F(13,20)
    zero=[F(0),F(0)];unchanged=zero if sum(zero)==0 else [v/sum(zero) for v in zero]
    assert sum(unchanged)==0
    return json.loads(json.dumps(dict(kind='authored_exact_witnesses_not_native_execution',
        support=dict(unsupported_mass='1/2',supported_mean='1/2',identified_set=[str(low),str(high)],zero_fill='1/4',uniform_fill='1/2',unsupported_ratio='0/0',unrestricted_fill_not_identification=True),
        coupling=dict(evidence_probability=str(evidence),joint_posterior={str(k):str(v) for k,v in posterior.items()},counterfactual_joint=str(joint_value),counterfactual_separate=str(separate_value),net_joint_usd=str(exact_net),net_separate_usd=str(separate_net)),
        identity=dict(shared_axis_normalized=[str(v) for v in shared],distinct_axes_mismatch=str(mismatch),pointer_identity_is_conditional_static_contract=True),
        zero_normalization=dict(result=[str(v) for v in unchanged],sum='0',valid_probability=False),
        economics=dict(total_hypothetical_usd=15000,submitted=500,completed=375,qualified=250,costs_usd=[30,40,60]),native_execution=False)))

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
