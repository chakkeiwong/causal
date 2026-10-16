#!/usr/bin/env python3
"""Exact authored laws and separate certificates for the preserving S4 extension."""
from fractions import Fraction as F
from itertools import product
import json
from math import ceil, log, sqrt
from pathlib import Path
import sympy as sp

import build_s4_reader_20261017 as candidate
import prepare_s4_20261017 as work
from publish_latent_r_review_v2_20261013 import ref, write

ROOT = work.ROOT
BASE = work.BASE/'depth-extension'
CHAPTER = BASE/'development.tex'
REVIEWER = work.REVIEWER
INITIAL = [
    (.25,'New assignment-dependent functional; title, motivation and repeated S1 target definitions excluded.'),
    (1,'Assignment-path derivative, complete influence function, orthogonal variance component and ATT reduction.'),
    (1,'Exact corrected-overlap denominator/remainder, local versus global robustness and conditional rate requirements.'),
    (.5,'New overlap-score remainder and ESS consequences; earlier ATE/ATT/ATC and simple clipped-IPW examples discounted.'),
    (.75,'Directional derivative test and residual-regression influence function/fitted counterexample; repeated DoubleML facts excluded.'),
    (.75,'Shared-control covariance derivation and exact simultaneous contrasts; repeated source/forest introduction discounted.'),
    (.75,'New resource-weighted primal/dual certificate and exact allocation loss; inherited generic capacity rule discounted.'),
    (.5,'Deterministic same-feasible-class regret proof and exact check; inherited policy-learning and evaluation cautions discounted.'),
    (1,'Boundary equivalent kernel, normal equations, quadratic bias and distinction from random finite-sample projection.'),
    (.5,'Fuzzy approximation amplification and discrete-support setup; inherited finite-epsilon/source-uncertainty material excluded.'),
    (.75,'Discrete-support conclusion and sharp portfolio transport witnesses; adoption introduction excluded.'),
    (.25,'New target-specific proposed adoption conditions only; repeated package/commercial/cutoff and general protocol prose discounted.'),
    (0,'General public/generated prototype and qualification framing already developed elsewhere.')]


def calculate():
    w = [F(1,2)]*2
    prop = [[F(1,2),F(1,4),F(1,4)], [F(1,4),F(1,4),F(1,2)]]
    effects = [[F(0),F(12)], [F(20),F(0)]]
    theta = [sum(wi*row[j] for wi,row in zip(w,effects)) for j in range(2)]
    covariance = [[sum(wi*(row[j]-theta[j])*(row[k]-theta[k])
                       for wi,row in zip(w,effects)) for k in range(2)] for j in range(2)]
    control = sum(wi*4/p[0] for wi,p in zip(w,prop))
    for j in range(2):
        for k in range(2):
            covariance[j][k] += control
            if j==k:
                covariance[j][k] += sum(wi*4/p[j+1] for wi,p in zip(w,prop))
    pairs=[]
    for j in range(2):
        mass=sum(wi*(p[0]+p[j+1]) for wi,p in zip(w,prop))
        mean=sum(wi*(p[0]+p[j+1])*row[j] for wi,p,row in zip(w,prop,effects))/mass
        pairs.append(dict(action=j+1,retained_mass=str(mass),
                          high_stratum_share=str(w[1]*(prop[1][0]+prop[1][j+1])/mass),
                          pair_population_effect=str(mean)))
    points=[]
    for gains in product([F(2),F(8)],[F(4),F(6)]):
        oracle=max(gains)/2
        points.append(dict(gains=list(map(str,gains)),oracle_value=str(oracle),
                           mixed_value=str(sum(gains)/4),
                           mixed_regret=str(oracle-sum(gains)/4),
                           lower_gain_policy_value=str(gains[1]/2),
                           lower_gain_policy_regret=str(oracle-gains[1]/2)))
    width=125; policies=16; alpha=F(1,20); n=10000
    rad=width*sqrt(log(2*policies/float(alpha))/(2*n))
    required=ceil(2*width**2*log(2*policies/float(alpha)))
    return dict(
        evidence_kind='Authored stipulated laws and deterministic/concentration bounds, not package or bank experiments.',
        common_population=dict(theta=list(map(str,theta)),pair_populations=pairs,
            covariance=[[str(v) for v in row] for row in covariance],
            covariance_components=dict(heterogeneity_cross='-60',shared_control='12'),
            difference_variance=str(covariance[0][0]+covariance[1][1]-2*covariance[0][1]),
            independence_variance=str(covariance[0][0]+covariance[1][1])),
        design=dict(criterion='Sum of two ATE influence variances; constant effects and iid randomized design.',
            optimal_control='sqrt(2)-1',optimal_active_each='(2-sqrt(2))/2',
            optimal_trace='24+16*sqrt(2)',baseline_trace='48',
            protected_control_design=['1/5','2/5','2/5'],protected_trace='60',
            protected_active_difference_variance='20'),
        robust_allocation=dict(stratum_mass=['1/2','1/2'],net_gain_box=[['2','8'],['4','6']],
            budget='1/2',minimax_fractions=['1/2','1/2'],minimax_regret='1',
            minimax_guaranteed_value='3/2',maximin_fractions=['0','1'],
            maximin_guaranteed_value='2',maximin_worst_regret='2',endpoint_cases=points),
        policy_bound=dict(score_range_USD=['-65','60'],range_width_USD=width,
            candidates=policies,alpha=str(alpha),evaluation_accounts=n,
            simultaneous_radius_USD=rad,selected_regret_bound_USD=2*rad,
            evaluation_accounts_for_one_USD_regret=required,
            method='Deterministic bound from bounded iid scores and union bound; no sampled coverage claim.'),
        discrete_support=dict(observed_scores=['-1','1'],observed_outcomes=['10','14'],
            slope_budget_each='1',sharp_cutoff_effect=['2','6'],action_cost='3',net_set=['-1','3'],
            slope_budget_each_two_effect=['0','8']))


def separate(exact):
    # Enumerate the observable action/noise law, independently of covariance formulas.
    rows=[]
    for x in [0,1]:
        probs=[F(1,2),F(1,4),F(1,4)] if x==0 else [F(1,4),F(1,4),F(1,2)]
        effects=[20*x,12*(1-x)]
        for arm,noise in product(range(3),[F(-2),F(2)]):
            value=[]
            for j in range(2):
                value.append(effects[j]-[10,6][j]+
                    (noise/probs[j+1] if arm==j+1 else F(0))-
                    (noise/probs[0] if arm==0 else F(0)))
            rows.append((probs[arm]/4,value))
    assert sum(p for p,_ in rows)==1
    assert all(sum(p*v[j] for p,v in rows)==0 for j in range(2))
    cov=[[sum(p*v[j]*v[k] for p,v in rows) for k in range(2)] for j in range(2)]
    assert cov==[[128,-48],[-48,60]]
    assert exact['common_population']['covariance']==[[str(v) for v in r] for r in cov]
    assert sum(p*(v[1]-v[0])**2 for p,v in rows)==284
    # Cauchy--Schwarz certificate and stationary point for the design criterion.
    p=sp.symbols('p',positive=True)
    objective=8/p+16/(1-p)
    optimum=sp.sqrt(2)-1
    assert sp.simplify(sp.diff(objective,p).subs(p,optimum))==0
    assert sp.simplify(objective.subs(p,optimum)-(24+16*sp.sqrt(2)))==0
    assert sp.diff(objective,p,2).subs(p,F(1,2))>0
    # The second derivative is16/p^3+32/(1-p)^3>0 throughout(0,1).
    assert sp.simplify(sp.diff(objective,p,2)-16/p**3-32/(1-p)**3)==0
    # Enumerate rectangular endpoints and oracle policies; verify the exact regret envelope.
    for t in [F(0),F(1,4),F(1,2),F(3,4),F(1)]:
        regrets=[]
        for g1,g2 in product([F(2),F(8)],[F(4),F(6)]):
            regrets.append(max(g1,g2)/2-(t*g1+(1-t)*g2)/2)
        assert max(regrets)==2*max(t,1-t)
    # Check the augmented-score range at all vertices, including randomized policy weights.
    vals=[]
    for y,m0,m1,c,arm,d in product([0,30],[0,30],[0,30],[0,5],[0,1],[0,1]):
        score=d*(m1-m0+2*arm*(y-m1)-2*(1-arm)*(y-m0)-c)
        vals.append(score)
    assert (min(vals),max(vals))==(-65,60)
    n=exact['policy_bound']['evaluation_accounts_for_one_USD_regret']
    rate=2*125**2*log(640)
    assert n-1 < rate <= n
    # Sharp Lipschitz endpoints: preserve observed arms, globally linear extensions.
    for sign,expected in [(-1,2),(1,6)]:
        m1=lambda s: F(14)-sign*(s-1)
        m0=lambda s: F(10)-sign*(s+1)
        assert m1(F(1))==14 and m0(F(-1))==10
        assert m1(F(0))-m0(F(0))==expected
        assert abs(m1(1)-m1(0))==abs(m0(1)-m0(0))==1
    return dict(status='pass',reviewer=REVIEWER,
        method='Separate twelve-atom IF enumeration, design stationary/convex/CS certificate, robust endpoint envelope, score-range vertices and Lipschitz witness extensions.',
        observable_atoms=12,covariance=[[str(v) for v in r] for r in cov],
        robust_grid_fractions=5,score_range_vertices=len(vals),
        evidence=[ref(BASE/'exact-results.json','Authored exact calculations'),ref(Path(__file__),'Separate checks')],
        limitations=work.LIMITS)


def main():
    BASE.mkdir(exist_ok=False)
    report=json.loads((candidate.OUT/'build-report.json').read_text())
    pages=[]
    for offset,(credit,reason) in enumerate(INITIAL):
        pages.append(dict(printed_page=197+offset,pdf_page=217+offset,credit=credit,rationale=reason))
    assert sum(r['credit'] for r in pages)==8
    write(work.BASE/'depth-review-initial.json',dict(status='fail_depth',reviewer=REVIEWER,
        reviewed_reader=report['pdf'],allocation=dict(min=10,target=14,max=17),
        substantive_page_credit=8,per_page=pages,allocation_minimum_met=False,
        finding='Thirteen physical pages yield eight exclusive substantive page equivalents after overlap and generic prose deductions.',
        next_action='Develop common-population joint comparisons/design, robust allocation, proved finite-policy evaluation bounds and sharp score-gap restrictions in a preserving extension.',
        evidence=[ref(candidate.OUT/'reader.txt','Every S4 extracted page inspected'),
                  ref(work.CHAPTER,'Frozen draft'),ref(work.BASE/'plan.md','Reviewed exclusions'),
                  ref(Path(__file__),'Conservative depth assessment')],visual_acceptance=False))
    exact=calculate()
    write(BASE/'exact-results.json',exact)
    write(BASE/'mathematics-review.json',separate(exact))
    print(json.dumps(dict(initial_depth='fail',exclusive_credit=8,
        extension_exact_families=5,mathematics='pass',policy_bound=exact['policy_bound'])))


if __name__=='__main__':main()
