#!/usr/bin/env python3
"""Independent feasibility, variance and symbolic checks for the project references."""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

import sympy as s
import temporal_graph_oracles_20261013 as candidate

ROOT=candidate.ROOT
BASE=candidate.BASE


def ref(p,anchor):
    return {'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'anchor':anchor}


def main():
    d=json.loads((BASE/'oracle-results.json').read_text())
    ratio_checks=0
    for case in d['ratio_cases']:
        nl,nu=map(F,case['numerator']);dl,du=map(F,case['denominator'])
        parts=[tuple(None if x is None else F(x) for x in p) for p in case['set']]
        probes={F(i,4) for i in range(-80,81)}|{F(-1000),F(1000)}
        for p in parts:
            for endpoint in p:
                if endpoint is not None:probes.update([endpoint,endpoint-F(1,10000),endpoint+F(1,10000)])
        for theta in probes:
            vals=[theta*dl,theta*du]
            feasible=max(nl,min(vals))<=min(nu,max(vals))
            assert candidate.contains(parts,theta)==feasible,(case['name'],theta)
            ratio_checks+=1
    byname={c['name']:c for c in d['ratio_cases']}
    assert byname['two_rays']['set']==[[None,'-1'],['1',None]]
    assert byname['zero_zero']['set']==[[None,None]]
    assert byname['empty']['set']==[]
    assert byname['strong']['set']==[['19/11','7/3']]
    data=d['fixture']['data'];n=len(data)-1
    variance_checks=0;perturbation_checks=0
    for p in d['variance_polynomials']:
        v=p['v'];q=list(map(F,p['coefficients']))
        for c in p['cells']:
            lo,hi=map(F,c['interval']);bl,bu=map(F,c['range']);el,eu=map(F,c['with_input_error'])
            for j in range(9):
                r=lo+(hi-lo)*F(j,8)
                residuals=[sum(F(a-r*b)*w for a,b,w in zip(cur,prev,v)) for prev,cur in zip(data[:-1],data[1:])]
                # Pairwise-difference identity is independent of centered quadratic coefficients.
                direct=sum((a-b)**2 for i,a in enumerate(residuals) for b in residuals[i+1:])/F(n*(n-1))
                assert candidate.evaluate(q,r)==direct and bl<=direct<=bu
                variance_checks+=1
                for pattern in range(3):
                    changed=[[F(value)+F(1 if (i+k+pattern)%3 else -1,1000) for k,value in enumerate(row)] for i,row in enumerate(data)]
                    e=[sum((a-r*b)*w for a,b,w in zip(cur,prev,v)) for prev,cur in zip(changed[:-1],changed[1:])]
                    pert=sum((a-b)**2 for i,a in enumerate(e) for b in e[i+1:])/F(n*(n-1))
                    assert el<=pert<=eu
                    perturbation_checks+=1
            a,b,_=q
            if a and lo<=-b/(2*a)<=hi:assert bl==candidate.evaluate(q,-b/(2*a))
    # Symbolically verify the equal law for every real tau, not only the fixtures.
    tau=s.symbols('tau',real=True)
    B=s.Matrix([[0,0,0],[1,0,0],[2-tau,tau,0]])
    noise=s.Matrix([[1,0,0],[0,1,0],[0,1-tau,1]])
    loading=s.simplify((s.eye(3)-B).inv()*noise)
    target=s.Matrix([[1,1,2],[1,2,3],[2,3,6]])
    assert s.simplify(loading*loading.T)==target and target.det()==1
    assert [target[:i,:i].det() for i in range(1,4)]==[1,1,1]
    surgery=B.copy();surgery[1,:]=s.zeros(1,3)
    assert s.simplify(((s.eye(3)-surgery).inv()*s.Matrix([0,1,0]))[2])==tau
    # The input-error square roots are all exact upward enclosures.
    for value in [F(0),F(1),F(2),F(9950,297),F(1,10**30)]:
        up=candidate.sqrt_upper(value)
        assert up*up>=value
        assert up==0 or (up-F(1,10**12))**2<value
    exp=d['experimental_planning'];q=F(exp['squared_halfwidth']);up=F(exp['halfwidth_upper'])
    assert q==F(9950,297) and up*up>=q
    assert F(exp['point_net'])==15000 and F(exp['net_interval'][0])<0
    assert F(d['relative_variance_bound']['bound_at_minimum'])==F(1,50)
    review={'status':'pass','scope':'Exact algebra, continuum enclosure and topology checks; no empirical coverage study',
        'checks':{'ratio_feasibility':ratio_checks,'sample_variance_identities':variance_checks,
                  'input_error_perturbations':perturbation_checks,'symbolic_all_real_effects':True,
                  'positive_definite_equal_law':True,'surgical_effect':True,'rational_sqrt_enclosures':True},
        'code':[ref(Path(__file__),'Independent rectangle feasibility, pairwise variance and symbolic surgery'),
                ref(ROOT/'tools/temporal_graph_oracles_20261013.py','Candidate exact enclosure/reference arithmetic')],
        'results':ref(BASE/'oracle-results.json','Executed deterministic results'),
        'limits':['Sampled polynomial/perturbation checks supplement the analytic bounds; they do not prove continuum coverage by enumeration.',
                  'No final random draws, graph inference engine or bank trial.','Input enclosures and statistical law remain prerequisites.']}
    (BASE/'reproduction-review.json').write_text(json.dumps(review,indent=2)+'\n')
    print(json.dumps({'status':'pass',**review['checks']}))


if __name__=='__main__':main()
