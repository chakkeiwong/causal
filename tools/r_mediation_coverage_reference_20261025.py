#!/usr/bin/env python3
"""Independent finite examples; never import or execute acquired software."""
from fractions import Fraction as F
from itertools import product, permutations
import json
import math

def variance(values):
    mean = sum(values) / len(values)
    return sum((x-mean)**2 for x in values) / (len(values)-1)

def calculate():
    # Stochastic mediator draws preserve the declared conditioning variables.
    conditional = sum(F(1,2)*c*p for c,p in [(0,F(1,4)),(1,F(3,4))])
    shuffled = F(1,2)*F(1,2)
    assert conditional == F(3,8) and shuffled == F(1,4)
    # Independent column permutations destroy a joint mediator distribution.
    m=(0,0,1,1);perms=list(permutations(m))
    joint=sum(F(x*x,4) for x in m)
    permuted=sum(sum(F(x*y,4) for x,y in zip(a,b)) for a in perms for b in perms)/len(perms)**2
    assert joint==F(1,2) and permuted==F(1,4)
    # Z|A has probabilities1/4,1/2;P(M=1|Z)=1/4+Z/2;Y=ZM.
    q=[F(1,4),F(1,2)]
    theta=lambda a,b:q[a]*(F(1,4)+q[b]/2)
    natural_total=(q[1]-q[0])*F(3,4)
    random_direct=theta(1,0)-theta(0,0)
    random_indirect=theta(1,1)-theta(1,0)
    assert natural_total==F(3,16)
    assert random_direct==F(3,32) and random_indirect==F(1,16)
    assert random_direct+random_indirect==F(5,32)
    # Interaction-aware linear mediation, independent mean-zero disturbances.
    # M=1+2A+error; E[Y|A,M]=3A+4M+5AM.
    mu=lambda a,astar:3*a+4*(1+2*astar)+5*a*(1+2*astar)
    pnde=mu(1,0)-mu(0,0);tnie=mu(1,1)-mu(1,0)
    tnde=mu(1,1)-mu(0,1);pnie=mu(0,1)-mu(0,0)
    assert (pnde,tnie,tnde,pnie)==(8,18,18,8)
    # Common outcome odds ratio does not imply the same marginal risk ratio.
    risk0=F(1,2);odds_ratio=F(2);risk1=odds_ratio*risk0/(1-risk0+odds_ratio*risk0)
    risk_ratio=risk1/risk0
    evalue=lambda r:float(r)+math.sqrt(float(r*(r-1)))
    assert risk1==F(2,3) and risk_ratio==F(4,3)
    # A correctly normalized latent binary mixture and the selected source expression.
    p=F(4,5)
    weights=[F(1,5),F(4,5)]
    pm=[F(1,4),F(3,4)];py=[F(1,5),F(4,5)]
    intended={};source={}
    for m,y in product([0,1],repeat=2):
        pieces=[(pm[u] if m else 1-pm[u])*(py[u] if y else 1-py[u]) for u in [0,1]]
        intended[(m,y)]=sum(weights[u]*pieces[u] for u in [0,1])
        source[(m,y)]=(1-p)*sum(pieces)
    assert sum(intended.values())==1 and sum(source.values())==F(2,5)
    assert intended[(1,1)]==F(49,100) and source[(1,1)]==F(13,100)
    normalized=source[(1,1)]/sum(source.values())
    assert normalized==F(13,40) and normalized!=intended[(1,1)]
    # Equal components should eliminate prevalence from the likelihood.
    equal_component=F(1,4)
    source_equal=(1-p)*(equal_component+equal_component)
    assert source_equal==F(1,10)
    # medoutcon selected one-step weighted mean is scale invariant; source variance is not.
    score=[F(1),F(3)]
    v1=variance(score)/2;v2=variance([2*x for x in score])/2
    assert v1==1 and v2==4
    # Two-phase observed-data influence-function projection.
    d=F(3);prediction=F(1);inclusion=F(1,2)
    observed=d/inclusion-(1/inclusion-1)*prediction
    missing=prediction
    assert inclusion*observed+(1-inclusion)*missing==d
    # Outcome-unit sensitivity functions differ in sign and target.
    alpha=F(4);e=F(1,2)
    one=[alpha*(a-e) for a in [0,1]]
    align=[alpha*((1-e)*a+e*(1-a)) for a in [0,1]]
    assert one==[-2,2] and align==[2,2]
    return dict(conditional_mediator_target=str(conditional),global_shuffle_target=str(shuffled),joint_mediator_target=str(joint),independent_shuffle_target=str(permuted),interventional_decomposition=dict(natural_total=str(natural_total),direct=str(random_direct),indirect=str(random_indirect),randomized_total=str(random_direct+random_indirect)),linear_effects=dict(pnde=pnde,tnie=tnie,tnde=tnde,pnie=pnie,te=pnde+tnie,cde_at_zero=3,naive_product=8),risk_scale=dict(odds_ratio=str(odds_ratio),baseline_risk=str(risk0),risk_ratio=str(risk_ratio),evalue_on_or=evalue(odds_ratio),evalue_on_rr=evalue(risk_ratio)),latent_mixture=dict(intended_mass='1',source_mass=str(sum(source.values())),intended_event=str(intended[(1,1)]),source_event=str(source[(1,1)]),renormalized_source_event=str(normalized),equal_component_intended=str(equal_component),equal_component_source=str(source_equal)),survey_weight_rescaling=dict(mean=2,source_variance_unit=str(v1),source_variance_double=str(v2)),two_phase=dict(observed=str(observed),missing=str(missing),expectation=str(d)),sensitivity=dict(one_sided_adjustments=list(map(str,one)),alignment_adjustments=list(map(str,align)),adjusted_gap_from_10_one_sided=6,adjusted_gap_from_10_alignment=10),hypothetical_economics=dict(cost_usd=30000,requests=1000,returned=600,scientifically_admissible=400,usd_per_request=30,usd_per_returned=50,usd_per_admissible=75),native_execution=False)

if __name__=='__main__':
    print(json.dumps(calculate(),indent=2))
