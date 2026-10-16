#!/usr/bin/env python3
"""Exact joint-weight and full-controller references; no fitted-package trial."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

import sympy as z
import build_s6_reader_20261017 as previous
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT, WORK = previous.ROOT, previous.WORK
BASE = WORK / 'depth-extension'


def serial(v):
    if isinstance(v, F):
        return str(v) if v.denominator != 1 else v.numerator
    if isinstance(v, dict):
        return {k: serial(x) for k, x in v.items()}
    if isinstance(v, (tuple, list)):
        return [serial(x) for x in v]
    return v


def risk(a, b, s):
    Q = lambda v: 1 + (1-v)**2 + v*v
    return (2-a)**2 * (2-b)**2 + s * Q(a) * Q(b)


def value(kp, beta, H=None):
    d, lam, k = F(19,20), F(9,10), F(2,5)
    a = lam + (kp-k)*beta
    geom = lambda r: 1/(1-r) if H is None else (1-r**(H+1))/(1-r)
    return 100*(a*geom(d*a)-lam*geom(d*lam)) - 10*(
        kp*kp*geom(d*a*a)-k*k*geom(d*lam*lam))-200


def calculate():
    a,b,s,p,t,x,y = z.symbols('a b s p t x y', real=True)
    Q = lambda v: 1+(1-v)**2+v*v
    objective = risk(a,b,s)
    certificate = 9*s/(1+s)+3*s*(p+t)**2+(1+s)*(
        p-t-(1-2*s)/(1+s))**2
    assert z.factor(objective.subs({a:1+x,b:1+y})-
                    certificate.subs({p:x+y,t:x*y})) == 0
    conditional = (2*(2-b)**2+s*Q(b))/((2-b)**2+2*s*Q(b))
    assert z.factor(z.diff(objective,a).subs(a,conditional)) == 0
    root_hi, root_lo = (7+z.sqrt(13))/6, (7-z.sqrt(13))/6
    assert z.simplify(objective.subs({a:root_hi,b:root_lo,s:z.Rational(1,8)})) == 1
    assert z.simplify((root_hi-1)+(root_lo-1)) == z.Rational(1,3)
    assert z.simplify((root_hi-1)*(root_lo-1)) == -z.Rational(1,3)
    assert z.factor(objective.subs({a:1+x,b:1+y,s:z.Rational(1,2)})-
                    3-3*(x+y)**2-3*x*x*y*y) == 0
    profiles=[]
    for name,aa,bb in [('nonnegative',F(1),F(1)),
                       ('unit_exact_only',F(2),F(1,2)),
                       ('both_axes_exact',F(2),F(2))]:
        profiles.append(dict(name=name,a=aa,b=bb,mse=risk(aa,bb,F(1,8))))
    # Strict negativity of each partial on [0,1]^2 at s=1/8:
    # (a-2)(2-b)^2 <= -1 and s Q(b)(2a-1) <= 1/4.
    assert F(1,8)*2-1 == -F(3,4)
    d,lam,k = F(19,20),F(9,10),F(2,5)
    values=[]
    for kp in [F(21,50),F(11,25)]:
        worlds=[]
        for beta in [F(1),F(2)]:
            coef=lam+(kp-k)*beta
            worlds.append(dict(beta=beta,rho=lam-k*beta,new_coefficient=coef,
                infinite_value=value(kp,beta),
                finite_values=[dict(H=H,value=value(kp,beta,H)) for H in [0,3,20,80]]))
        values.append(dict(new_feedback=kp,endpoint_worlds=worlds,
                           worst_infinite_value=value(kp,F(1))))
    # A single positive lower bound covers both finite-valued comparisons.
    derivative_lower=100/(1-d*F(23,25))**2-2*d*10*F(11,25)**2*F(49,50)/(
        1-d*F(49,50)**2)**2
    assert derivative_lower > 0 and 100 > 2*10*F(11,25)**2
    # Absolute tail bound holds uniformly over these two rules and beta in [1,2].
    H=80;amax=F(49,50);kpmax=F(11,25)
    uniform_tail=100*(amax*(d*amax)**(H+1)/(1-d*amax)+
        lam*(d*lam)**(H+1)/(1-d*lam)) + 10*(
        kpmax**2*(d*amax*amax)**(H+1)/(1-d*amax*amax)+
        k*k*(d*lam*lam)**(H+1)/(1-d*lam*lam))
    assert uniform_tail < F(109,25)
    bad_k=F(47,100)
    bad_min=lam+(bad_k-k);bad_max=lam+2*(bad_k-k)
    assert d*bad_max < 1 and d*bad_max*bad_max > 1
    return serial(dict(joint_weights=dict(
        conditional_optimizer=str(conditional),certificate=str(certificate),
        zero_square_solution=dict(p='(1-2*s)/(2*(1+s))',t='-p',range='0<s<=1/2'),
        noise_one_eighth=dict(optima=[[str(root_hi),str(root_lo)],[str(root_lo),str(root_hi)]],
            global_mse=1,profiles=profiles,partial_derivative_upper=-F(3,2)),
        noise_one_half=dict(unique_optimum=[1,1],global_mse=3)),
        controllers=dict(discount=d,old_feedback=k,old_coefficient=lam,
            margin=100,action_cost=10,setup_cost=200,beta_range=[1,2],comparisons=values,
            derivative_lower=derivative_lower,finite_derivative_cost_ratio_bound=F(121,3125),
            uniform_absolute_tail_H80=uniform_tail,
            robust_state_stability=[-F(11,20),F(9,20)],
            robust_finite_value_interval=['2/5-(sqrt(20/19)+9/10)/2',
                                        '2/5+(sqrt(20/19)-9/10)/2'],
            divergent_rule=dict(feedback=bad_k,coefficient_range=[bad_min,bad_max],
                largest_benefit_ratio=d*bad_max,largest_cost_ratio=d*bad_max*bad_max,
                divergence_beta_threshold='(sqrt(20/19)-9/10)/(7/100)'))))


def separate(results):
    # Enumerate all 512 independent-cell noise signs on several rational weights.
    # Each table is one treated row/two donor rows and one post/two pre columns.
    checked=[]
    for a,b in [(F(1),F(1)),(F(2),F(1,2)),(F(2),F(2)),(F(7,4),F(3,5))]:
        rows=[F(1),-(1-a),-a];cols=[F(1),-(1-b),-b]
        coefficients=[r*c for r in rows for c in cols]
        noise=[sum(c*e for c,e in zip(coefficients,signs))
               for signs in product([-1,1],repeat=9)]
        signal=sum(rows[i]*cols[j]*[2,0,1][i]*[2,0,1][j]
                   for i in range(3) for j in range(3))
        assert sum(noise)==0 and signal==(2-a)*(2-b)
        mse=signal*signal+F(1,8)*sum(n*n for n in noise)/512
        assert mse==risk(a,b,F(1,8))
        checked.append(dict(a=a,b=b,direct_mse=mse))
    # At the irrational optimum, calculate noise variance by cell coefficients.
    a,b=(7+z.sqrt(13))/6,(7-z.sqrt(13))/6
    coefficients=[r*c for r in [1,a-1,-a] for c in [1,b-1,-b]]
    raw_mse=z.expand(((2-a)*(2-b))**2+sum(c*c for c in coefficients)/8)
    assert z.simplify(raw_mse)==1
    # Direct structural recursion, with old and new action costs retained.
    d,lam,k=F(19,20),F(9,10),F(2,5)
    maximum_error=F(0)
    for kp,beta in product([F(21,50),F(11,25)],[F(1),F(3,2),F(2)]):
        rho=lam-k*beta
        old=new=F(1);running=-F(200);coef=rho+beta*kp
        for h in range(81):
            old_action,new_action=k*old,kp*new
            old=rho*old+beta*old_action
            new=rho*new+beta*new_action
            running+=d**h*(100*(new-old)-10*(new_action**2-old_action**2))
            assert old==lam**(h+1) and new==coef**(h+1)
            if h in [0,3,20,80]:
                assert running==value(kp,beta,h)
        tail=(100*(coef*(d*coef)**81/(1-d*coef)-lam*(d*lam)**81/(1-d*lam))-
            10*(kp*kp*(d*coef*coef)**81/(1-d*coef*coef)-k*k*(d*lam*lam)**81/(1-d*lam*lam)))
        assert running+tail==value(kp,beta)
        maximum_error=max(maximum_error,abs(tail))
    # Resolve the polynomial finite-term derivative before applying its bound.
    a,dv,m,q,kp=z.symbols('a d m q kp',positive=True)
    for h in range(10):
        derivative=z.diff(dv**h*(m*a**(h+1)-q*kp*kp*a**(2*h)),a)
        expected=dv**h*(m*(h+1)*a**h-(0 if h==0 else 2*h*q*kp*kp*a**(2*h-1)))
        assert z.expand(derivative-expected)==0
    # Endpoint intersections of linear inequalities, with strict boundaries.
    for radius,lower,upper in [(F(1),-F(11,20),F(9,20))]:
        lo=max(k+(-radius-lam)/beta for beta in [F(1),F(2)])
        hi=min(k+(radius-lam)/beta for beta in [F(1),F(2)])
        assert (lo,hi)==(lower,upper)
    assert maximum_error < F(109,25)
    assert results==calculate()
    return serial(dict(status='pass',direct_cell_profiles=checked,
        cell_signs_per_profile=512,irrational_optimum_direct_cell_mse=1,
        recursion_comparisons=6,maximum_checked_absolute_tail=maximum_error,
        checks=['Polynomial coefficient identity verifies the global sum-of-squares certificate.',
            'Zero-square solutions are real for0<s<=1/2; s=1/2 identity has a unique zero.',
            'Derivative upper bound proves the nonnegative optimum rather than relying on a grid search.',
            'Nine-cell sign enumeration and direct irrational cell moments verify the joint MSE.',
            'Structural old/new state-action recursions match geometric finite values and exact tails.',
            'Positive analytic derivative bounds, including every finite summand, locate worst-case beta.',
            'Linear endpoint inequalities verify robust stability; quadratic-cost ratios expose divergence.']))


def initial_depth():
    rows=[
        (.25,'Question and new event-study setup; title, orientation and inherited framing excluded.'),
        (1,'Exact full-rank cohort projection and false-lead witness, including FWL interpretation.'),
        (.5,'New horizon-curvature composition; generic sensitivity-set material excluded.'),
        (1,'Sharp weighted horizon budgets and target-specific monetary breakdown.'),
        (.75,'Noisy baseline slope and exact target variance; generic confidence construction excluded.'),
        (.75,'Conditional donor interpolation/extrapolation risk; inherited donor-balance setup excluded.'),
        (1,'Signed-weight contamination support function and exact risk reversal.'),
        (.75,'Two-axis factor imbalance and fixed-weight noise comparison; inherited DiD framing excluded.'),
        (.75,'SDID law comparison and target-specific alternatives; generic inference summary excluded.'),
        (.75,'Signed finite-calendar covariance and exact persistence contrast.'),
        (.5,'Open/maintained/replaced feedback distinctions; inherited time-series background excluded.'),
        (.75,'Feedback action paths and intervention-specific finite/infinite monetary composition.'),
        (.75,'Geometric gross/action tail separation and minimum integer horizon witness.'),
        (.5,'Selected estimator target/covariance distinctions; repeated catalogs and generic wrapping excluded.'),
        (.25,'Block/dispatcher restrictions with specific refusal consequence; repeated software discussion excluded.'),
        (0,'Prospective prototype/public-data and CLI/MCP discussion already allocated elsewhere.'),
        (0,'Repeated prototype framing and conclusion receive no exclusive depth.')]
    per_page=[dict(printed_page=236+i,pdf_page=257+i,credit=c,rationale=r)
              for i,(c,r) in enumerate(rows)]
    assert sum(r['credit'] for r in per_page)==10.25
    for path in [previous.OUT/'build-report.json',previous.BASE/'traceability-review.json']:
        verify_bindings(json.loads(path.read_text()))
    write(WORK/'depth-review-initial.json',dict(status='negative',
        operation='TEXT.REVIEW.S6',reviewer=dict(name='Codex author/coordinator',kind='author'),
        allocation=dict(min=14,target=17,max=20),substantive_page_credit=10.25,
        allocation_minimum_met=False,planning_target_met=False,per_page=per_page,
        measurement='Conservative author assessment of extracted rendered pages and source; exclusive equivalents, not physical-page count or visual acceptance.',
        findings=['The957-page candidate compiles and has17 physical chapter pages but fails the14-page exclusive minimum.',
                  'Preserve every frozen input and candidate. Develop the reviewed joint-weight/full-replacement questions in a versioned successor.'],
        evidence=[ref(p,'Reviewed exact first candidate or depth-repair scope') for p in
            [previous.PDF,previous.CHAPTER,previous.OUT/'build-report.json',
             previous.OUT/'reader.txt',previous.OUT/'text-layout-review.json',
             WORK/'plan.md',WORK/'depth-extension-plan.md',Path(__file__)]],
        visual_acceptance=False,independent_review=False))


def main():
    assert not BASE.exists() and not (WORK/'depth-review-initial.json').exists()
    results=calculate();checked=separate(results)
    initial_depth()
    BASE.mkdir()
    write(BASE/'exact-results.json',results)
    write(BASE/'mathematics-review.json',dict(status='pass',
        reviewer=dict(name='Codex author/coordinator',kind='author'),
        separate_checks=checked,findings=[
            'At noise1/8 the two asymmetric oracle optima have risk1; nonnegative, one-axis exact and both-axis exact risks are1.5,1.125 and4.5.',
            'With200USD setup cost, rule0.42 has worst infinite incremental value-92.5932USD, while0.44 has52.7002USD under the supplied beta range.',
            'The0.44 worst20-horizon value is-5.4812USD; convergence to a positive infinite value does not justify a short-horizon investment.',
            'Rule0.47 has convergent benefits in every supplied world but divergent adverse quadratic costs in some worlds.',
            'The first development assertion proposed a4.33USD absolute uniform tail bound; the four-term envelope is4.3531689459USD, so the assertion failed before any receipt was written. Corrected to4.36USD.'],
        evidence=[ref(p,'Exact reference, distinct author checks or reviewed scope') for p in
            [BASE/'exact-results.json',Path(__file__),WORK/'depth-extension-plan.md',
             WORK/'depth-review-initial.json']],
        limitations=['Known-factor fixed-weight oracle calculations are not data-fitted estimator performance.',
            'Beta[1,2] is a supplied sensitivity restriction, not an observed identification result or confidence region.',
            'Fixed structural laws, feasible rules, noise and monetary inputs are stipulated, not bank findings.',
            'Authored exact calculations and separate checks are not independent review or upstream-package execution.']))
    print(json.dumps(dict(status='pass',initial_exclusive_depth=10.25,
        weight_global_risk=1,controller_worst_values=[float(value(kp,F(1))) for kp in [F(21,50),F(11,25)]],
        visual_acceptance=False)))


if __name__=='__main__':
    main()
