#!/usr/bin/env python3
"""Additional exact S6 checks, preserving both previously frozen references."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import sympy as s
import s6_examples_20261017 as original
import s6_robust_panels_20261017 as robust
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT, BASE = original.ROOT, original.BASE
OUT = BASE/'value-checks'


def serial(x):
    if isinstance(x, F): return str(x) if x.denominator != 1 else x.numerator
    if isinstance(x, dict): return {k:serial(v) for k,v in x.items()}
    if isinstance(x, (tuple,list)): return [serial(v) for v in x]
    return x


def calculate():
    # Closed forms compared with direct state/action recursion using Fraction.
    values=[]
    d=F(19,20)
    for name,k,a in [('maintained',F(2,5),F(9,10)),
                     ('open',F(0),F(1,2)),
                     ('replacement',-F(1,5),F(3,10))]:
        finite=[]
        for disc in [F(1),d]:
            prev=F(0);states=[];actions=[]
            for h in range(4):
                act=k*prev+int(h==0)
                prev=prev/2+act
                actions.append(act);states.append(prev)
            direct=sum(disc**h*(100*states[h]-10*actions[h]**2) for h in range(4))-200
            closed=100*(1-(disc*a)**4)/(1-disc*a)-200-10*(
                1+k*k*disc*(1-(disc*a*a)**3)/(1-disc*a*a))
            assert direct == closed
            finite.append(dict(discount=disc,value=direct))
        infinite=100/(1-d*a)-200-10*(1+k*k*d/(1-d*a*a))
        # The exact series through200 and its analytic remainder recover the limit.
        partial=sum(d**h*(100*a**h-10*(F(1) if h==0 else k*a**(h-1))**2)
                    for h in range(201))-200
        remainder=100*(d*a)**201/(1-d*a)-10*k*k*d**201*a**400/(1-d*a*a)
        assert partial+remainder == infinite
        values.append(dict(name=name,coefficient=a,feedback=k,
                           finite=finite,infinite_discounted_value=infinite))
    # Same observed controller and same reduced form, different replacement law.
    worlds=[]
    for rho,beta in [(F(1,2),F(1)),(F(1,10),F(2))]:
        assert rho+beta*F(2,5)==F(9,10)
        coef=rho-beta/5;prev=F(1);path=[]
        for _ in range(4):
            prev=rho*prev+beta*(-prev/5);path.append(prev)
        assert path==[coef**(h+1) for h in range(4)]
        worlds.append(dict(rho=rho,beta=beta,replacement_coefficient=coef,
                           replacement_states=path,gross_margin=100*sum(path)))
    # Exact finite-horizon tail inequalities, with both adjacent integer checks.
    rate=F(171,200)
    tail=lambda h:100*rate**(h+1)/(1-rate)
    h=0
    while tail(h)>10:h+=1
    assert h==27 and tail(h)<=10<tail(h-1)
    action_tail=10*F(2,5)**2*d**4*F(9,10)**6/(1-d*F(9,10)**2)
    full=values[0]['infinite_discounted_value']
    trunc=values[0]['finite'][1]['value']
    assert full-trunc == tail(3)-action_tail
    # The risk threshold is derived independently from the displayed fractions.
    delta_slope=F(7)-F(13,4)
    threshold=F(9,16)/delta_slope
    assert threshold==F(3,20)
    assert F(9,16)+F(13,4)*F(1,10)==F(71,80)
    # Avoid float-producing Python-int paths in the old robust endpoint receipt.
    risks=[]
    for a in [F(1),F(3,2),F(2)]:
        candidate=[]
        for factor,c0,c1 in product([F(-2),F(2)],[F(-1),F(1)],[F(-1),F(1)]):
            errors=[]
            for et,e0,e1 in product([F(-1),F(1)],repeat=3):
                residual=(2-a)*factor-(1-a)*c0-a*c1+et-(1-a)*e0-a*e1
                errors.append(residual**2)
            candidate.append(sum(errors)/len(errors))
        risk=max(candidate)
        formula=1+(1-a)**2+a*a+(2*abs(2-a)+abs(1-a)+abs(a))**2
        assert risk==formula
        risks.append(dict(a=a,exact_worst_mse=risk))
    assert [r['exact_worst_mse'] for r in risks]==[F(11),F(25,2),F(15)]
    return serial(dict(feedback_values=values,closed_loop_worlds=worlds,
        horizon=dict(minimum_H=h,tail_H26=tail(26),tail_H27=tail(27),
                     gross_tail_H3=tail(3),action_tail_H3=action_tail,
                     net_tail_H3=full-trunc),sdid_risk_threshold=threshold,
        robust_donor_risks=risks,
        divergent_cost_example=dict(discount=F(1,2),response_rate=F(3,2),
                                    discounted_rate=F(3,4),squared_rate=F(9,8))))


def main():
    for p in [BASE/'mathematics-review.json',BASE/'robust-mathematics-review.json']:
        verify_bindings(json.loads(p.read_text()))
    exact=json.loads((BASE/'exact-results.json').read_text())
    assert original.calculate()==exact and original.separate(exact)['status']=='pass'
    assert robust.calculate()==json.loads((BASE/'robust-results.json').read_text())
    results=calculate()
    OUT.mkdir(exist_ok=False)
    write(OUT/'exact-results.json',results)
    write(OUT/'mathematics-review.json',dict(status='pass',
        reviewer=dict(name='Codex author/coordinator',kind='author'),
        checks=['Fraction state/action recursion agrees with finite discounted closed form at two discounts.',
                'Two hundred and one direct terms plus exact remainders agree with infinite value.',
                'Two observationally equivalent closed-loop laws disagree under feedback replacement.',
                'Adjacent integer horizons bracket the USD10 tolerance; gross minus action tail equals the exact net remainder.',
                'SDID risk crossover and low-noise example checked separately.',
                'Every donor-factor-contamination and Rademacher-error vertex recomputed with Fraction arithmetic.'],
        findings=['The pre-freeze draft claimed H26 sufficed; its exact bound10.0396USD fails. Corrected to H27, bound8.5839USD.',
                  'Two values in the frozen robust receipt were serialized as11.0 and15.0. Fraction enumeration recovers exact integers11 and15 without changing that receipt.',
                  'Two stray single TeX backslashes at line endings were removed before chapter freeze.'],
        evidence=[ref(p,'Exact reference or identity-bound prior review') for p in
                  [OUT/'exact-results.json',Path(__file__),BASE/'mathematics-review.json',
                   BASE/'robust-mathematics-review.json']],
        limits=['Exact project laws and authored checks, not independent acceptance or an empirical experiment.',
                'Infinite value requires both benefit and squared-action convergence; the tail bound needs a uniform defended envelope.']))
    print(json.dumps(dict(status='pass',minimum_tail_H=27,profiles=3)))


if __name__=='__main__':main()
