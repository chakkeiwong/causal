#!/usr/bin/env python3
"""S6 signed-donor contamination and action-cost exact extensions."""
from itertools import product
from pathlib import Path
import sympy as s
from s6_examples_20261017 import ROOT,BASE,serial,R
from publish_latent_r_review_v2_20261013 import ref,write


def calculate():
    a=s.symbols('a',real=True)
    # B=2, C=1, sigmaT²=sigma²=1; separate polynomials on all four pieces.
    intervals=[(-s.oo,0),(0,1),(1,2),(2,s.oo)]
    radii=[5-4*a,5-2*a,3,4*a-5]
    risks=[s.expand(1+(1-a)**2+a**2+b**2) for b in radii]
    pieces=[];candidates=[(s.Integer(0),s.Integer(27)),(s.Integer(1),s.Integer(11)),
                         (s.Integer(2),s.Integer(15))]
    for bounds,b,risk in zip(intervals,radii,risks):
        stationary=s.solve(s.diff(risk,a),a)[0]
        admitted=bool(bounds[0]<=stationary<=bounds[1])
        if admitted:candidates.append((stationary,risk.subs(a,stationary)))
        pieces.append(dict(interval=bounds,bias_radius=b,risk=risk,
                           stationary=stationary,stationary_in_piece=admitted))
    best=min(candidates,key=lambda x:x[1])
    assert best==(1,11)
    # Direct independent mean-square expectation across all centered errors.
    witness=[]
    for aa in [1,R(3,2),2]:
        w=[1-aa,aa]
        worst=0;worstlaw=None
        for f,c0,c1 in product([-2,2],[-1,1],[-1,1]):
            mean=(2-aa)*f-w[0]*c0-w[1]*c1
            mse=0
            for et,e0,e1 in product([-1,1],repeat=3):
                mse+=(mean+et-w[0]*e0-w[1]*e1)**2/8
            if mse>worst:worst=mse;worstlaw=[f,c0,c1]
        formula=1+(1-aa)**2+aa**2+(2*abs(2-aa)+abs(1-aa)+abs(aa))**2
        assert worst==formula
        witness.append(dict(a=aa,worst_mse=worst,witness=worstlaw))
    costs=[]
    for name,k in [('maintained',R(2,5)),('open_loop',0),('replacement',-R(1,5))]:
        prev=s.Integer(0);states=[];actions=[]
        for h in range(4):
            act=k*prev+int(h==0);prev=prev/2+act
            actions.append(act);states.append(prev)
        penalty=10*sum(x*x for x in actions)
        costs.append(dict(regime=name,actions=actions,response=states,
            squared_action_sum=sum(x*x for x in actions),action_penalty_USD=penalty,
            net_USD=100*sum(states)-200-penalty))
    assert costs[0]['net_USD']==R(406107,3125)
    return serial(dict(donor_robust=dict(pieces=pieces,global_minimizer=best[0],
                       global_minimum=best[1],endpoint_enumeration=witness),feedback_costs=costs))


if __name__=='__main__':
    data=calculate()
    if (BASE/'robust-results.json').exists():
        import json
        assert json.loads((BASE/'robust-results.json').read_text())==data
    else:
        write(BASE/'robust-results.json',data)
    write(BASE/'robust-mathematics-review.json',dict(status='pass',
        reviewer={'name':'Codex author/coordinator','kind':'author'},
        checks=['Global piecewise-quadratic optimization includes every kink and admissible stationary point.',
                'Worst MSE at three candidate weights independently enumerates all factor/contamination vertices and all centered Rademacher cell errors.',
                'Controller cost paths evaluated by structural recursion; exact monetary result independently specified as406107/3125USD.'],
        evidence=[ref(BASE/'robust-results.json','Contamination and action-cost references'),
                  ref(Path(__file__),'Exact enumeration and conditional structural arithmetic')],
        limitations=['Same-author checks of stipulated laws only; no bank prices or independent review.']))
    print('Robust donor optimum1, MSE11; action-cost paths verified.')
