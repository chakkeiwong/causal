#!/usr/bin/env python3
"""Constraint-aware audit designs: exact authored laws and separate checks."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

import sympy as z
import build_s7_reader_20261017 as previous
from publish_latent_r_review_v2_20261013 import ref, write

ROOT, WORK = previous.ROOT, previous.WORK
BASE = WORK/'depth-extension'


def serial(value):
    if isinstance(value, F):
        return str(value) if value.denominator != 1 else value.numerator
    if isinstance(value, dict):
        return {key: serial(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [serial(item) for item in value]
    return value


def coefficients(lam):
    return -8+F(3,4)*lam, -48+F(1,4)*lam


def calculate():
    lam, t0, t1, tau = z.symbols('lambda theta0 theta1 tau', real=True)
    a0, a1 = -8+3*lam/4, -48+lam/4
    assert z.expand(22-lam/4+a0*t0+a1*t1-(22-8*t0-48*t1)-
                    lam*(3*t0/4+t1/4-z.Rational(1,4))) == 0
    assert z.expand(a0-3*a1) == 136
    assert coefficients(F(32,3)) == (0, -F(136,3))
    assert coefficients(F(192)) == (F(136), 0)
    assert z.expand((22-8*t0-48*t1).subs(t0,(4*tau-t1)/3)-
                    (22-32*tau/3-136*t1/3)) == 0
    equal = F(136,3)**2/(4*700)
    priced = F(136,3)**2/(4*455)
    assert equal == F(1156,1575) and priced == F(4624,4095)
    return serial(dict(
        pooled_constraint='3*theta0/4+theta1/4=1/4',
        coefficient_identity='a0-3*a1=136',
        stratum1_estimator=dict(intercept=F(58,3),slope=-F(136,3),lambda_value=F(32,3)),
        stratum0_estimator=dict(intercept=-26,slope=136,lambda_value=192),
        minimum_envelope='4624*min(c0,c1/9)/C',price_ratio_transition=9,
        equal_count=dict(total=700,new_allocation=[0,700],new_bound=equal,
            earlier_allocation=[100,600],earlier_bound=F(28,25)),
        priced=dict(prices=[1,4],budget=1820,new_allocation=[0,455],new_bound=priced,
            earlier_allocation=[140,420],earlier_bound=F(52,35)),
        noisy_pool=dict(value='22-(32/3)*tau-(136/3)*theta1',
            pool_variance_coefficient=F(1024,9),
            stratum_variance_coefficient=F(18496,9),covariance_coefficient=F(8704,9)),
        interpretation='Global optimum of a declared common-one-quarter variance envelope within linear unbiased constraint-adjusted estimators and continuous positive-price allocations; boundary zero samples require zero coefficients.'))


def separate(results):
    # Directly enumerate independent Bernoulli audit data, not the reference formula.
    laws=[]
    for theta0 in [F(1,6),F(1,4),F(1,3)]:
        theta1=1-3*theta0
        for lam,n0,n1 in [(F(0),2,3),(F(32,3),0,3),(F(192),3,0),(F(40),2,2)]:
            a0,a1=coefficients(lam)
            assert n0 or a0==0
            assert n1 or a1==0
            mean=second=F(0)
            for bits in product([0,1],repeat=n0+n1):
                prob=F(1)
                for j,b in enumerate(bits):
                    t=theta0 if j<n0 else theta1
                    prob*=t if b else 1-t
                estimator=22-lam/4
                if n0: estimator+=a0*F(sum(bits[:n0]),n0)
                if n1: estimator+=a1*F(sum(bits[n0:]),n1)
                mean+=prob*estimator;second+=prob*estimator**2
            target=22-8*theta0-48*theta1
            actual=(a0*a0*theta0*(1-theta0)/n0 if n0 else 0)+(
                a1*a1*theta1*(1-theta1)/n1 if n1 else 0)
            assert mean==target and second-mean**2==actual
            laws.append(dict(theta0=theta0,lambda_value=lam,n=[n0,n1],mean=mean,variance=actual))
    # The absolute-value bound proves all real lambda; these rationals check its cases.
    for root_price1 in [F(1),F(2),F(3),F(4)]:
        minimum=F(136)*min(F(1),root_price1/3)
        for lam in [F(-40),F(0),F(32,3),F(40),F(192),F(240)]:
            a0,a1=coefficients(lam)
            assert a0-3*a1==136
            assert abs(a0)+root_price1*abs(a1)>=minimum
        chosen=F(32,3) if root_price1<=3 else F(192)
        a0,a1=coefficients(chosen)
        assert abs(a0)+root_price1*abs(a1)==minimum
    # Recover the noisy-pool variance by expanding independent symbolic errors.
    e,f=z.symbols('e f',real=True)
    squared=z.expand((-z.Rational(32,3)*e-z.Rational(136,3)*f)**2)
    assert squared.coeff(e,2)==z.Rational(1024,9)
    assert squared.coeff(f,2)==z.Rational(18496,9)
    assert squared.coeff(e,1).coeff(f,1)==z.Rational(8704,9)
    assert results==calculate()
    return serial(dict(status='pass',enumerated_laws=laws,
        checks=['Twelve finite Bernoulli audit laws independently reproduce means and variances, including zero-sample boundary designs.',
            'The coefficient identity and weighted absolute-value inequality give a global envelope lower bound; explicit designs attain it.',
            'Price square roots1,2,3,4 and estimator coefficients on both sides of the kinks reproduce the transition and attained bound.',
            'Symbolic substitution and direct squared-error expansion retain noisy-pool variance and cross-covariance.'],
        scope='Distinct author algebra/enumeration, not independent review, package execution or sampled calibration'))


def main():
    assert not (WORK/'depth-review-initial.json').exists()
    assert {p.name for p in BASE.iterdir()} == {'development.tex'}
    entries=[
        (.25,'New complete graph/action/target value; generic observation notation and repeated introductory framing excluded.'),
        (1,'Coherent overlap family, sharp monetary set and distinct graph/action independence.'),
        (1,'Single-edge audit nonidentification and matched coordinated-action alternatives with equal marginal expenses.'),
        (1,'Global pair feasibility plus realizable eight-node topology transport and support failure.'),
        (1,'Target-specific pooled-audit polytope, coherent sharp endpoints and unsupported homogeneous completion.'),
        (.75,'New completion/sampling distinctions and constrained value image; generic total variance and inherited linkage principles discounted.'),
        (.75,'Truthful joint audit unit, derived concentration and prospective473-audit sign criterion; generic uncertainty discussion excluded.'),
        (.75,'Target-weighted and price-constrained audit comparison; generic Cauchy-Schwarz framing discounted.'),
        (.25,'Joint linkage/exposure composition boundary; inherited package descriptions and missingness catalog excluded.'),
        (.5,'Specific incompatibility of row, missingness, sensitivity and network regimes; repeated catalog and interface details excluded.'),
        (.25,'Conditional-graph versus outer-region numerical error; inherited group package catalog and prototype framing excluded.'),
        (0,'Benchmark procedure, acquisition framing and conclusion repeat earlier allocations; no duplicate credit.')]
    assert sum(v for v,_ in entries)==7.5
    write(WORK/'depth-review-initial.json',dict(status='fail',
        reviewer=dict(name='Codex author/coordinator',kind='author'),
        reviewed_reader=ref(previous.PDF,'Unpublished975-page initial candidate'),
        allocation=dict(min=8,target=9,max=11),substantive_page_credit=7.5,
        per_page=[dict(printed_page=259+i,pdf_page=280+i,credit=v,rationale=r) for i,(v,r) in enumerate(entries)],
        allocation_minimum_met=False,visual_acceptance=False,
        finding='Source identities, exact authored references, equation resolution and extracted-text bounds pass; physical chapter length does not cure exclusive-depth shortfall.',
        evidence=[ref(p,'Initial candidate or reviewed plan') for p in
            [previous.OUT/'build-report.json',previous.BASE/'traceability-review.json',
             previous.OUT/'text-layout-review.json',previous.OUT/'reader.txt',previous.CHAPTER,
             WORK/'plan.md',WORK/'depth-extension-plan.md']],
        next_action='Preserve this failure; derive constraint-aware audit design and noisy-pool uncertainty in a preserving successor.'))
    exact=calculate();write(BASE/'exact-results.json',exact)
    checked=separate(exact)
    checked['evidence']=[ref(p,'Exact input, authored source or reviewed plan') for p in
        [BASE/'exact-results.json',BASE/'development.tex',Path(__file__),WORK/'depth-extension-plan.md']]
    write(BASE/'mathematics-review.json',checked)
    print(json.dumps(dict(exact='pass',separate='pass',initial_depth=7.5,initial_outcome='fail')))


if __name__=='__main__':main()
