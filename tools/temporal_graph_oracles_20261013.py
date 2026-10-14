#!/usr/bin/env python3
"""Exact project references for continuous-lag outer sets; zero random draws."""
from fractions import Fraction as F
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-13/temporal-graphs'


def quadratic(data,v):
    n=len(data)-1
    if n<2:raise ValueError('Need at least two transitions')
    u=[sum(F(x)*y for x,y in zip(row,v)) for row in data[1:]]
    w=[sum(F(x)*y for x,y in zip(row,v)) for row in data[:-1]]
    mu,mw=sum(u)/n,sum(w)/n
    return (sum((x-mw)**2 for x in w)/(n-1),
            -2*sum((x-mu)*(y-mw) for x,y in zip(u,w))/(n-1),
            sum((x-mu)**2 for x in u)/(n-1))


def evaluate(q,r):return q[0]*r*r+q[1]*r+q[2]


def bounds(q,cell):
    a,b,_=q;lo,hi=cell
    if a<0 or lo>hi:raise ValueError('Invalid variance polynomial/cell')
    vals=[evaluate(q,lo),evaluate(q,hi)]
    if a and lo<=-b/(2*a)<=hi:vals.append(evaluate(q,-b/(2*a)))
    return min(vals),max(vals)


def sqrt_upper(value,digits=12):
    if value<0:raise ValueError('Negative square root')
    scale=10**digits
    k=math.isqrt(value.numerator*scale*scale//value.denominator)
    if F(k*k,scale*scale)<value:k+=1
    return F(k,scale)


def inflated_bounds(q,cell,n,vnorm,eta):
    lo,hi=bounds(q,cell)
    h=vnorm*eta*(1+max(abs(cell[0]),abs(cell[1])))
    error=4*h*sqrt_upper(F(n,n-1))*sqrt_upper(hi)+4*n*h*h/F(n-1)
    return max(F(0),lo-error),hi+error


def normalize(parts):
    # None in a lower endpoint is -infinity; in an upper endpoint +infinity.
    parts=sorted(parts,key=lambda p:(p[0] is not None,p[0] or F(0)))
    out=[]
    for lo,hi in parts:
        if not out:out.append((lo,hi));continue
        plo,phi=out[-1]
        if phi is None or lo is None or lo<=phi:
            out[-1]=(plo,None if phi is None or hi is None else max(phi,hi))
        else:out.append((lo,hi))
    return out


def ratio_set(numer,denom):
    nl,nu=numer;dl,du=denom
    if nl>nu or dl>du:raise ValueError('Reversed moment interval')
    if dl<=0<=du and nl<=0<=nu:return [(None,None)]
    parts=[]
    def positive(nlo,nhi,dlo,dhi):
        if dhi<=0:return
        if dlo>0:
            corners=[a/b for a in [nlo,nhi] for b in [dlo,dhi]]
            parts.append((min(corners),max(corners)))
        elif nlo>0:parts.append((nlo/dhi,None))
        elif nhi<0:parts.append((None,nhi/dhi))
        else:raise AssertionError('Zero numerator and denominator handled first')
    if du>0:positive(nl,nu,max(F(0),dl),du)
    if dl<0:positive(-nu,-nl,max(F(0),-du),-dl)
    return normalize(parts)


def contains(parts,value):
    return any((lo is None or lo<=value) and (hi is None or value<=hi) for lo,hi in parts)


def covariance_box(data,cell,t=F(1,4),eta=F(0)):
    if not 0<t<1:raise ValueError('Relative tolerance outside (0,1)')
    vectors=[(1,0,0),(0,1,0),(0,0,1)]
    def variance(v):
        lo,hi=inflated_bounds(quadratic(data,v),cell,len(data)-1,sum(abs(x) for x in v),eta)
        return lo/(1+t),hi/(1-t)
    result={(i,i):variance(v) for i,v in enumerate(vectors)}
    for i in range(3):
        for j in range(i+1,3):
            plus=tuple(a+b for a,b in zip(vectors[i],vectors[j]))
            minus=tuple(a-b for a,b in zip(vectors[i],vectors[j]))
            pl,pu=variance(plus);ml,mu=variance(minus)
            result[i,j]=((pl-mu)/4,(pu-ml)/4)
    return result


def encode(obj):
    if isinstance(obj,F):return str(obj)
    if isinstance(obj,dict):return {str(k):encode(v) for k,v in obj.items()}
    if isinstance(obj,(tuple,list)):return [encode(v) for v in obj]
    return obj


def main():
    BASE.mkdir(parents=True,exist_ok=True)
    data=[(0,0,0),(1,2,3),(2,-1,0),(-1,0,2),(0,1,-1),(3,2,1),(-2,-1,1)]
    edges=[F(-19,20)+j*F(19,80) for j in range(9)]
    cells=list(zip(edges,edges[1:]))
    vectors=[(1,0,0),(0,1,0),(0,0,1),(1,1,0),(1,-1,0),(1,0,1),(1,0,-1),(0,1,1),(0,1,-1)]
    polys=[{'v':v,'coefficients':quadratic(data,v),
            'cells':[{'interval':c,'range':bounds(quadratic(data,v),c),
                      'with_input_error':inflated_bounds(quadratic(data,v),c,6,sum(abs(x) for x in v),F(1,1000))} for c in cells]} for v in vectors]
    raw_cases=[('strong',(F(19,10),F(21,10)),(F(9,10),F(11,10))),
               ('two_rays',(F(1),F(2)),(F(-1),F(1))),
               ('right_ray',(F(1),F(2)),(F(0),F(1))),
               ('left_ray',(F(-2),F(-1)),(F(0),F(1))),
               ('zero_zero',(F(0),F(1)),(F(-1),F(1))),
               ('empty',(F(1),F(2)),(F(0),F(0))),
               ('singleton',(F(0),F(0)),(F(1),F(2))),
               ('negative_denominator',(F(-3),F(-2)),(F(-2),F(-1)))]
    ratios=[{'name':name,'numerator':n,'denominator':d,'set':ratio_set(n,d)} for name,n,d in raw_cases]
    boxes=[]
    for cell in cells:
        box=covariance_box(data,cell,eta=F(1,1000))
        boxes.append({'lag_cell':cell,'moment_box':box,'effect_outer_set':ratio_set(box[0,2],box[0,1])})
    # Algebraic family, expanded from structural loadings, not statistical data.
    family=[]
    for tau in map(F,[-5,-1,0,1,2,7]):
        c=2-tau
        loadings=[[F(1),F(0),F(0)],[F(1),F(1),F(0)],[tau+c,tau+(1-tau),F(1)]]
        cov=[[sum(a*b for a,b in zip(x,y)) for y in loadings] for x in loadings]
        family.append({'tau':tau,'direct_Z':c,'disturbance_variance':1+(1-tau)**2,
                       'disturbance_covariance':1-tau,'innovation_covariance':cov,
                       'stationary_covariance_rho_2_5':[[a/(1-F(2,5)**2) for a in row] for row in cov],
                       'interventional_arm_difference_delta_half':tau})
    m=200;alpha=F(3,100);delta=F(1,2);s2=F(100);estimate=F(20);nu=2*m-2
    b2=F(nu,nu-2)/alpha
    half2=b2*s2/(2*m*delta*delta);half=sqrt_upper(half2)
    experimental={'kind':'supplied_planning_summaries_not_trial_results','m_per_arm':m,'df':nu,
                  'alpha':alpha,'delta':delta,'squared_multiplier':b2,'pooled_variance':s2,
                  'estimate':estimate,'squared_halfwidth':half2,'halfwidth_upper':half,
                  'effect_interval':[estimate-half,estimate+half],
                  'cohort':3000,'cost_per_offer':15,
                  'net_interval':[3000*(estimate-half-15),3000*(estimate+half-15)],
                  'point_net':3000*(estimate-15)}
    result={'kind':'deterministic_project_algebra_not_final_study','random_draws':0,
            'relative_variance_bound':{'directions':9,'tolerance':F(1,4),'alpha':F(1,50),
                                      'minimum_df':14400,'predecessor_df':239,
                                      'bound_at_minimum':F(18,14400)/F(1,4)**2},
            'fixture':{'data':data,'not_gaussian_sample':True,'numerical_tolerance_only':F(1,4),
                       'input_error_envelope':F(1,1000),'lag_partition':cells},
            'variance_polynomials':polys,'ratio_cases':ratios,'continuum_outer_boxes':boxes,
            'equal_law_family':family,'experimental_planning':experimental,
            'limits':['Exact fixtures prove arithmetic only; confidence proof requires its declared observation law and sample size.',
                      'No graph search, optimized joint feasibility, statistical qualification or bank experiment.']}
    (BASE/'oracle-results.json').write_text(json.dumps(encode(result),indent=2)+'\n')
    print(json.dumps({'references':len(ratios),'quadratics':len(polys),'lag_cells':len(cells),
                      'random_draws':0,'planning_halfwidth':float(half),'planning_net_lower':float(experimental['net_interval'][0])}))


if __name__=='__main__':main()
