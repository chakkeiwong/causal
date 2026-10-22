#!/usr/bin/env python3
"""Exact authored laws for IV/RD semantics; no downloaded-package execution."""
from fractions import Fraction as F
from itertools import combinations
from math import erf, sqrt


def calculate():
    # (population mass, D(0), D(1), loss(0), loss(1)); Z independent of type.
    types=[(F(2,5),0,1,200,50),(F(1,5),1,1,200,150),(F(2,5),0,0,200,200)]
    mean_d=[sum(p*(d0,d1)[z] for p,d0,d1,y0,y1 in types) for z in (0,1)]
    mean_y=[sum(p*(y0,y1)[(d0,d1)[z]] for p,d0,d1,y0,y1 in types) for z in (0,1)]
    first=mean_d[1]-mean_d[0];itt=mean_y[1]-mean_y[0]
    late=itt/first;ate=sum(p*(y1-y0) for p,d0,d1,y0,y1 in types)
    assert (first,itt,late,ate)==(F(2,5),-60,-150,-70)
    assert mean_y==[190,130]
    cost=100;encouragement_cost=10
    encouragement_margin=-itt-cost*first-encouragement_cost
    assert encouragement_margin==10 and -ate-cost==-30 and -late-cost==50
    exclusion_ratio=(itt-20)/first
    assert exclusion_ratio==-200
    # Two compliance types move in opposite directions. The ratio is not a convex average.
    defier_first=F(2,5)-F(1,5)
    defier_itt=F(2,5)*(-150)-F(1,5)*(-50)
    assert defier_itt/defier_first==-250

    # Known covariance Gaussian reduced-form reference. q=4 gives coverage erf(sqrt(2)).
    def coefficients(a,b,vy,vd,cov=F(0)):
        return b*b-4*vd,-2*a*b+8*cov,a*a-4*vy
    def accepted(a,b,vy,vd,beta):
        return (a-beta*b)**2<=4*(vy+beta*beta*vd)
    disconnected=coefficients(F(2),F(0),F(3,4),F(1,4))
    bounded=coefficients(F(2),F(2),F(5,12),F(1,4))
    whole=coefficients(F(0),F(0),F(3,4),F(1,4))
    assert disconnected==(-1,0,1) and bounded==(3,-8,F(7,3))
    assert all(bounded[0]*x*x+bounded[1]*x+bounded[2]==0 for x in [F(1,3),F(7,3)])
    for x in [F(k,4) for k in range(-40,41)]:
        assert accepted(F(2),F(0),F(3,4),F(1,4),x)==(abs(x)>=1)
        assert accepted(F(2),F(2),F(5,12),F(1,4),x)==(F(1,3)<=x<=F(7,3))
        assert accepted(F(0),F(0),F(3,4),F(1,4),x)
    narrow_grid=[F(k,4) for k in range(-2,3)]
    assert not any(accepted(F(2),F(0),F(3,4),F(1,4),x) for x in narrow_grid)

    # Integer score with no support approaching zero: two continuous laws agree at observations.
    scores=[-1,1]
    model_a=[100-20*int(x>=0) for x in scores]
    model_b=[90-10*x for x in scores]
    assert model_a==model_b==[100,80]
    lipschitz=10
    # Each side's distance is one; two one-sided extrapolation errors add.
    identified=[-20-2*lipschitz,-20+2*lipschitz]
    margin=[-identified[1]-10,-identified[0]-10]
    assert identified==[-40,0] and margin==[-10,30]

    # Sharp null: six fixed observed dollar losses; exactly three assigned uniformly.
    outcomes=[0,0,0,100,100,100]
    statistics=[]
    for treated in combinations(range(6),3):
        t=set(treated)
        statistics.append(F(sum(outcomes[i] for i in t),3)-F(sum(outcomes[i] for i in range(6) if i not in t),3))
    observed=statistics[0]
    pvalue=F(sum(abs(x)>=abs(observed) for x in statistics),len(statistics))
    assert observed==-100 and len(statistics)==20 and pvalue==F(1,10)

    def norm(value):
        if isinstance(value,F):return str(value)
        if isinstance(value,dict):return {k:norm(v) for k,v in value.items()}
        if isinstance(value,(list,tuple)):return [norm(v) for v in value]
        return value
    return norm(dict(kind='project_authored_exact_reference',native_package_execution=False,
        assumptions='Declared finite population laws; independent encouragement; monetary inputs hypothetical.',
        iv=dict(types=types,mean_treatment=mean_d,mean_loss=mean_y,first_stage=first,itt_loss=itt,
            complier_loss_effect=late,population_loss_effect=ate,treatment_cost=cost,
            encouragement_cost=encouragement_cost,encouragement_margin=encouragement_margin,
            universal_treatment_margin=-ate-cost,complier_treatment_margin=-late-cost,
            direct_encouragement_loss_effect=-20,exclusion_violating_ratio=exclusion_ratio,
            defier_first_stage=defier_first,defier_itt_loss=defier_itt,defier_ratio=defier_itt/defier_first),
        gaussian_inversion=dict(known_covariance=True,critical_square=4,
            model_coverage=erf(sqrt(2)),not_default_95_percent=True,
            disconnected_coefficients=disconnected,disconnected_set=[['-inf','-1'],['1','inf']],
            bounded_coefficients=bounded,bounded_set=[['1/3','7/3']],
            whole_line_coefficients=whole,whole_line_set=[['-inf','inf']],
            narrow_grid=narrow_grid,narrow_grid_accepted=[],global_set_empty=False,
            empirical_coverage_claim=False),
        discrete_rd=dict(scores=scores,observed_losses=model_a,effect_model_a=-20,effect_model_b=0,
            lipschitz_bound=lipschitz,loss_effect_bounds=identified,treatment_cost=10,margin_bounds=margin),
        randomization=dict(fixed_losses=outcomes,assignment='uniform over exactly 3 of 6',
            assignments=len(statistics),observed_difference=observed,two_sided_p=pvalue,
            null='Fisher sharp null; no unit effect',window_selection='fixed before outcomes',
            population_average_effect_inference=False)))


if __name__=='__main__':
    import json
    print(json.dumps(calculate(),indent=2))
