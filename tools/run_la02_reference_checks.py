#!/usr/bin/env python3
"""Exact finite scientific counterexamples plus LA02 declaration checks."""
import json
import sys
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from causalbank.problem_contract_v12 import review_problem

WORK=ROOT/'docs/program/repair-v12/work/LA02'


def oracle():
    forward={(a,y):F(0) for a in (0,1) for y in (0,1)}
    reverse=dict(forward)
    for root in (0,1):
        for flip,prob in [(0,F(9,10)),(1,F(1,10))]:
            forward[root,root^flip]+=F(1,2)*prob
            reverse[root^flip,root]+=F(1,2)*prob
    assert forward==reverse
    # Sum the two independent exogenous mechanisms after replacing A's equation.
    forward_means=[sum(F(y==a)*F(9,10)+F(y!=a)*F(1,10) for y in [1]) for a in (0,1)]
    reverse_means=[F(1,2),F(1,2)]
    effects=[forward_means[1]-forward_means[0],reverse_means[1]-reverse_means[0]]
    assert effects==[F(4,5),F(0)]
    strata=[(F(1,2),F(1,5),F(0)),(F(1,2),F(1,2),F(10))]
    trimmed=sum(p*tau for p,e,tau in strata if F(1,10)<=e<=F(9,10))/sum(p for p,e,tau in strata if F(1,10)<=e<=F(9,10))
    overlap=sum(p*e*(1-e)*tau for p,e,tau in strata)/sum(p*e*(1-e) for p,e,tau in strata)
    assert trimmed==5 and overlap==F(250,41)
    # Independent potential-outcome table; no CLadder or CausalDS code imported.
    types=[{'p':F(1,2),'t0':0,'t1':1,'y0':0,'y1':1},
           {'p':F(1,2),'t0':0,'t1':0,'y0':0,'y1':3}]
    mean_t=[sum(x['p']*x['t'+str(z)] for x in types) for z in (0,1)]
    mean_y=[sum(x['p']*x['y'+str(x['t'+str(z)])] for x in types) for z in (0,1)]
    wald=(mean_y[1]-mean_y[0])/(mean_t[1]-mean_t[0])
    ate=sum(x['p']*(x['y1']-x['y0']) for x in types)
    assert wald==1 and ate==2
    return {'status':'pass','kind':'project exact finite counterexamples; no empirical or bank qualification',
       'equivalent_graphs':{'joint_table':{str(k):str(v) for k,v in forward.items()},'effects':[str(v) for v in effects]},
       'weighting_targets':{'trimmed_population_ate':str(trimmed),'overlap_ate':str(overlap)},
       'iv_target':{'wald_ratio':str(wald),'population_ate':str(ate)},
       'scope':'These examples expose distinct scientific targets; they do not prove behavior of unexecuted external packages.'}


if __name__=='__main__':
    results=[]
    for c in json.loads((WORK/'casebook.json').read_text())['cases']:
        out=review_problem(c['problem'],c['diagram'])
        assert out['gate']==c['expected_gate'],out
        results.append({'id':c['id'],**out})
    (WORK/'case-checks.json').write_text(json.dumps({'status':'pass','cases':results},indent=2)+'\n')
    numerical=oracle()
    (WORK/'oracles.json').write_text(json.dumps(numerical,indent=2)+'\n')
    print(json.dumps({'case_gates':{r['id']:r['gate'] for r in results},'exact_counterexamples':numerical}))
