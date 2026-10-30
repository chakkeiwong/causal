#!/usr/bin/env python3
"""Authored exact references; no Java, Tetrad, estimator or downloaded code."""
from fractions import Fraction as F
from itertools import product
import json


def calculate():
    observed=[]; risks=[]
    for model in [1,2]:
        law={(a,y):F(0) for a,y in product([0,1],repeat=2)}
        do=[F(0),F(0)]
        for u,n,e in product([0,1],repeat=3):
            w=F(1,2)*(F(1,4) if n else F(3,4))*(F(1,4) if e else F(3,4))
            a=u^n; y=u if model==1 else a^e
            law[a,y]+=w
            for fixed in [0,1]:do[fixed]+=w*(u if model==1 else fixed^e)
        observed.append(law);risks.append(do)
    assert observed[0]==observed[1]=={(0,0):F(3,8),(0,1):F(1,8),(1,0):F(1,8),(1,1):F(3,8)}
    assert risks==[[F(1,2),F(1,2)],[F(1,4),F(3,4)]]
    effects=[r[1]-r[0] for r in risks];money=[200*d-20 for d in effects]
    assert effects==[0,F(1,2)] and money==[-20,80]
    coupling=[]
    for opposite in [False,True]:
        obs={(a,y):F(0) for a,y in product([0,1],repeat=2)}
        do=[F(0),F(0)];num=F(0);den=F(0)
        for a,u in product([0,1],repeat=2):
            potential=[u,1-u if opposite else u];w=F(1,4)
            obs[a,potential[a]]+=w
            for fixed in [0,1]:do[fixed]+=w*potential[fixed]
            if a==0 and potential[0]==0:den+=w;num+=w*potential[1]
        coupling.append(dict(observational={str(k):str(v) for k,v in obs.items()},
            interventional=list(map(str,do)),counterfactual_given_A0_Y0=str(num/den)))
    assert coupling[0]['observational']==coupling[1]['observational']
    assert coupling[0]['interventional']==coupling[1]['interventional']==['1/2','1/2']
    assert [c['counterfactual_given_A0_Y0'] for c in coupling]==['0','1']
    return dict(kind='authored_exact_reference',native_Java_execution=False,
        hidden_confounding=dict(assumptions=['U~Bernoulli(1/2), N,E independently Bernoulli(1/4)',
            'A=U xor N; model1 Y=U; model2 Y=A xor E',
            'Common allowed supergraph U->A,U->Y,A->Y; zero functional effects allowed; no faithfulness assumption'],
            observed={str(k):str(v) for k,v in observed[0].items()},
            conditional_Y1_given_A1='3/4',do_risks=[list(map(str,r)) for r in risks],effects=list(map(str,effects)),
            meaning='Two compatible positive observed laws agree while their interventions differ; these two witnesses are not a sharp identified set.',
            assumed_value_usd=200,assumed_action_cost_usd=20,incremental_net_usd=list(map(str,money))),
        cross_world=dict(assumptions='A,U independent Bernoulli(1/2); stable potentials(U,U) versus switching potentials(U,1-U)',models=coupling,
            meaning='Same observational and marginal interventional laws do not determine P(Y(1)=1|A=0,Y=0) without a coupling restriction.'),
        distance=dict(candidates=['-2','2'],target='0',finite_set_distance='2',interval_hull_distance='0',
            empty_list_source_branch_at_target_minus1='-1',interpretation='Authored source-branch check; negative empty output is not a valid distance, zero hull distance is not exact membership.'),
        limitations=['No native engine, algorithm completeness proof, calibrated uncertainty or observed bank ROI.',
            'Numeric probability -1 and nonfinite results are failure states, distinct from valid signed treatment effects.'])


if __name__=='__main__':
    print(json.dumps(calculate(),indent=2))
