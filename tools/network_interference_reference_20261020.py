#!/usr/bin/env python3
"""Authored exact network references; no commercial or downloaded engine executes."""
from fractions import Fraction as F
from itertools import product
import json

def serial(x):
    if isinstance(x,F): return str(x)
    if isinstance(x,dict): return {k:serial(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)): return [serial(v) for v in x]
    return x

def inverse(a):
    n=len(a); m=[[F(v) for v in row]+[F(i==j) for j in range(n)] for i,row in enumerate(a)]
    for j in range(n):
        k=next((i for i in range(j,n) if m[i][j]),None)
        if k is None: raise ValueError('singular feedback system')
        m[j],m[k]=m[k],m[j];q=m[j][j];m[j]=[v/q for v in m[j]]
        for i in range(n):
            if i!=j:
                q=m[i][j];m[i]=[x-q*y for x,y in zip(m[i],m[j])]
    return [row[n:] for row in m]

def multiply(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]

def response(w,rho,beta):
    n=len(w); a=[[F(i==j)-rho*w[i][j] for j in range(n)] for i in range(n)]
    inv=inverse(a)
    assert multiply(a,inv)==[[F(i==j) for j in range(n)] for i in range(n)]
    return [[beta*v for v in row] for row in inv]

def calculate():
    # W[i,j] receives an effect at i from j; this differs from source-row graph storage.
    w=[[F(0),F(1)],[F(1),F(0)]];rho=F(1,2);beta=F(10)
    s=response(w,rho,beta)
    direct=sum(s[i][i] for i in range(2))/2
    total=sum(map(sum,s))/2;indirect=total-direct
    assert s==[[F(40,3),F(20,3)],[F(20,3),F(40,3)]]
    assert (direct,indirect,total)==(F(40,3),F(20,3),F(20))
    cost=F(12);own_margin=direct-cost;portfolio_margin=sum(row[0] for row in s)-cost
    assert (beta-cost,own_margin,portfolio_margin)==(F(-2),F(4,3),F(8))
    missing=response([[F(0),F(1)],[F(0),F(0)]],rho,beta)
    missing_margin=sum(row[0] for row in missing)-cost
    assert missing_margin==-2
    try:response(w,F(1),beta)
    except ValueError: singular_refused=True
    else:raise AssertionError('Singular system accepted')

    # Gradient for T=beta/(1-rho) in ordering (beta,rho).
    grad=[1/(1-rho),beta/(1-rho)**2]
    covariance=[[F(1),F(1,20)],[F(1,20),F(1,100)]]
    assert covariance[0][0]*covariance[1][1]-covariance[0][1]**2>0
    full_variance=sum(grad[i]*covariance[i][j]*grad[j] for i in range(2) for j in range(2))
    diagonal_variance=sum(grad[i]**2*covariance[i][i] for i in range(2))
    assert (full_variance,diagonal_variance)==(F(28),F(20))

    star=[[F(0),F(1),F(1)],[F(1),F(0),F(0)],[F(1),F(0),F(0)]]
    normalized=[[v/sum(row) for v in row] for row in star]
    raw=response(star,F(1,4),F(10));row_norm=response(normalized,F(1,4),F(10))
    scaled=response([[v/2 for v in row] for row in star],F(1,2),F(10))
    assert raw==scaled and raw!=row_norm
    raw_target=[row[0] for row in raw];normalized_target=[row[0] for row in row_norm]

    # Two-person complete randomization of exactly one unit has no (0,0) or (1,1) exposures.
    balanced=[(0,1),(1,0)];independent=list(product([0,1],repeat=2))
    def exposure_law(assignments):
        out={}
        for z in assignments:
            e=f'{z[0]},{z[1]}'
            out[e]=out.get(e,F(0))+F(1,len(assignments))
        return out
    balanced_law=exposure_law(balanced);bernoulli_law=exposure_law(independent)
    assert balanced_law=={'0,1':F(1,2),'1,0':F(1,2)}
    assert all(v==F(1,4) for v in bernoulli_law.values())
    # Authored mean law mu(z,e)=5+2z+3e. HT point means average correctly, no variance guarantee claimed.
    def mu(z,e):return F(5+2*z+3*e)
    expected={}
    for target in independent:
        estimate_sum=F(0)
        for z in independent:
            ht=sum((mu(z[i],z[1-i])/F(1,4) if (z[i],z[1-i])==target else F(0)) for i in range(2))/2
            estimate_sum+=ht/F(4)
        expected[str(target)]=estimate_sum
        assert estimate_sum==mu(*target)
    assert mu(1,0)-mu(0,0)==2 and mu(0,1)-mu(0,0)==3
    deterministic_time_contrast=(100+2)-0
    alternating_contrast=2-4
    assert deterministic_time_contrast==102 and alternating_contrast==-2
    return serial(dict(scope='Exact authored structural and assignment examples; no native execution or bank observations',
        feedback=dict(receiver_row_weights=w,rho=rho,beta=beta,response_matrix=s,
            average_own=direct,average_spillover=indirect,average_total=total,
            coefficient_only=beta,cost=cost,coefficient_margin=beta-cost,
            own_margin=own_margin,portfolio_margin=portfolio_margin,
            missing_tie_margin=missing_margin,singular_refused=singular_refused),
        uncertainty=dict(assumed_parameter_covariance=covariance,gradient=grad,
            full_delta_variance=full_variance,diagonal_only_variance=diagonal_variance,
            boundary='Illustrative delta algebra; not a measured variance or coverage result'),
        normalization=dict(raw_weights=star,row_normalized_weights=normalized,
            raw_response=raw,row_normalized_response=row_norm,raw_target=raw_target,
            row_normalized_target=normalized_target,scalar_rescaling_preserves_response=True,
            row_rescaling_changes_response=True),
        assignment=dict(exposure='Own assignment, neighbor assignment',
            exactly_one_treated_probabilities=balanced_law,independent_half_probabilities=bernoulli_law,
            unsupported_in_exactly_one_design=['0,0','1,1'],
            authored_mean_law='5+2*z+3*e',expected_HT_means=expected,
            direct_contrast_at_neighbor_zero=2,spillover_contrast_for_untreated=3,
            boundary='Marginal exposure positivity and unbiased means do not establish a usable variance; joint exposure support and the design remain necessary'),
        switchback=dict(time_law='Y_t=100*t+2*z_t, t=0,1, z=(0,1)',
            observed_time_contrast=deterministic_time_contrast,causal_immediate_effect=2,
            carryover_law='Y_t=2*z_t+4*z_(t-1), alternating schedule',
            observed_alternating_contrast=alternating_contrast,sustained_effect=6,
            boundary='Authored laws illustrate confounding and carryover; no vendor failure or bootstrap coverage claim'))
        )

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
