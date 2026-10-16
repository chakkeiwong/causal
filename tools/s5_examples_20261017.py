#!/usr/bin/env python3
"""Exact authored S5 laws; no upstream estimators or statistical study runs."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'docs/program/execution/2026-10-17/s5'
CHAPTER = ROOT/'docs/program/comprehensive-v14/work/TEXT.DRAFT.S5/chapter.tex'


def serial(value):
    if isinstance(value, (F, sp.Rational)): return str(value)
    if isinstance(value, dict): return {k: serial(v) for k,v in value.items()}
    if isinstance(value, (list, tuple)): return [serial(v) for v in value]
    return value


def compete(default, prepay, periods=2, upfront=0):
    live=F(1); fd=fp=active=F(0)
    for _ in range(periods):
        active+=live
        fd+=live*default;fp+=live*prepay
        live*=1-default-prepay
    assert fd+fp+live==1
    return dict(default=fd,prepayment=fp,event_free=live,
                target_complement=1-fd,active_periods=active,
                net_USD=20*active-1000*fd-50*fp-upfront)


def frailty(hazards, periods=3):
    alive=[F(1,2)]*2;survival=[F(1)];h=[]
    for _ in range(periods):
        h.append(sum(p*x for p,x in zip(alive,hazards))/sum(alive))
        alive=[p*(1-x) for p,x in zip(alive,hazards)]
        survival.append(sum(alive))
    return dict(survival=survival,marginal_hazards=h,risk=1-survival[-1],
                restricted_time=sum(survival[:-1]))


def calculate():
    # Tail bounds include the observed S(m) contribution for integer event times.
    K,m=6,3
    observed=[[F(1),F(4,5),F(13,20),F(1,2)],
              [F(1),F(9,10),F(4,5),F(3,5)]]
    tails=[]
    for s in observed:
        low=s+[F(0)]*(K-m);high=s+[s[-1]]*(K-m)
        interval=[sum(low[:K]),sum(high[:K])]
        assert interval==[sum(s[:m])+s[m],sum(s[:m])+(K-m)*s[m]]
        tails.append(dict(observed_survival=s,lower_witness=low,
                          upper_witness=high,restricted_time=interval))
    diff=[tails[0]['restricted_time'][0]-tails[1]['restricted_time'][1],
          tails[0]['restricted_time'][1]-tails[1]['restricted_time'][0]]
    horizon=dict(m=m,K=K,policies=tails,difference=diff,
                 net_difference_USD=[20*x-3 for x in diff])
    f0=frailty([F(4,5),F(1,10)])
    f1=frailty([F(2,5),F(1,20)])
    assert all(a>b for a,b in zip([F(4,5),F(1,10)],[F(2,5),F(1,20)]))
    assert f1['marginal_hazards'][-1]>f0['marginal_hazards'][-1]
    assert f1['risk']<f0['risk']
    selection=dict(reference=f0,policy=f1,
        net_difference_USD=20*(f1['restricted_time']-f0['restricted_time'])-
                           1000*(f1['risk']-f0['risk'])-3)
    c0=compete(F(1,10),F(1,10))
    c1=compete(F(3,25),F(3,5),upfront=3)
    wrong=compete(F(3,25)*(1-F(3,5)),F(3,5),upfront=3)
    ordered=dict(reference=c0,policy=c1,wrong_direct_mapping=wrong,
        reference_conditional_target=F(1,9),policy_conditional_target=F(3,10),
        net_difference_USD=c1['net_USD']-c0['net_USD'],
        wrong_net_difference_USD=wrong['net_USD']-c0['net_USD'])
    # Same observed joint law, different off-natural treatment innovations.
    worlds=[]
    observed_laws=[]
    for world in [0,1]:
        obs={};value=F(0)
        for u,v in product([0,1],repeat=2):
            a1=u
            a2=v if world==0 or a1==u else 1
            key=f'{a1}{a2}{a2}'
            obs[key]=obs.get(key,F(0))+F(1,4)
            shifted_a1=1-u
            shifted_a2=v if world==0 or shifted_a1==u else 1
            value+=F(1,4)*shifted_a2
        observed_laws.append(obs)
        worlds.append(dict(world=world,observed_law=obs,natural_modified_mean=value,
                           redrawn_stochastic_mean=F(1,2)))
    assert observed_laws[0]==observed_laws[1]
    natural=dict(worlds=worlds,support='Every observed (A1,A2) cell has probability1/4.',
        standard_randomization='Outcome and covariate structural innovations are constants.',
        strong_condition='World1 reuses U1 in the future natural action innovation; strong condition fails.')
    a=sp.symbols('a',real=True)
    cut=sp.Rational(3,4);delta=sp.Rational(1,4)
    def map_integral(expr):
        return sp.integrate(expr(a+delta,a),(a,0,cut))+sp.integrate(expr(a,a),(a,cut,1))
    mu=map_integral(lambda d,z:d)
    second=map_integral(lambda d,z:d**2)
    derivative=map_integral(lambda d,z:d*(2*z-1))
    residual=sp.integrate(a*(1-a),(a,delta,cut))+4*sp.integrate(a*(1-a),(a,cut,1))
    clipbase=sp.integrate(a+delta,(a,0,cut))
    pushforward=dict(delta=delta,mean=mu,second_moment=second,
        assignment_variance=second-mu**2,assignment_path_derivative=derivative,
        bernoulli_outcome_residual_variance=residual,
        full_bernoulli_variance=residual+second-mu**2,
        perturbed_mean_at_epsilon_quarter=mu+derivative/4,
        density_intervals=[[0,delta,0],[delta,cut,1],[cut,1,2]],
        capped_endpoint_mass=delta,capped_identified_set=[clipbase,clipbase+delta],
        capped_net_difference_USD=[100*clipbase-50-3,100*(clipbase+delta)-50-3])
    # Ordered probability and cumulative weight conversion are separate issues.
    p=[F(1,2),F(2,5)]
    weights=dict(incremental_denominators=p,cumulative_denominators=[p[0],p[0]*p[1]],
        incremental_ratios=[1/p[0],1/p[1]],cumulative_ratios=[1/p[0],1/(p[0]*p[1])],
        cumulative_floor_quarter_final=1/max(F(1,4),p[0]*p[1]),
        incremental_floor_quarter_final=1/(max(F(1,4),p[0])*max(F(1,4),p[1])))
    p0,p1=F(1,5),F(3,10)
    paired=p1-p0-(p1-p0)**2
    independent=p0*(1-p0)+p1*(1-p1)
    numerical=dict(p0=p0,p1=p1,mean_difference=p1-p0,paired_variance=paired,
        independent_variance=independent,paired_M10000_variance=paired/10000,
        independent_M10000_variance=independent/10000,
        two_identical_rows_variance_ratio=2,
        failure_accounting=dict(attempted=200,available=160,covered=152,
            availability=F(160,200),conditional_coverage=F(152,160),request_coverage=F(152,200)))
    eps=F(1,50);K=3
    ds=[min(F(1),t*eps) for t in range(K+1)]
    envelope=dict(K=K,transition_error=eps,history_TV_bounds=ds,
        running_margin_error_USD=sum(20*x for x in ds[:-1]),
        terminal_default_error_USD=1000*ds[-1],
        total_error_USD=sum(20*x for x in ds[:-1])+1000*ds[-1])
    return serial(dict(status='exact_authored_reference',horizon=horizon,selection=selection,
        ordered_events=ordered,natural_vs_redrawn=natural,pushforward=pushforward,
        probability_weights=weights,numerical_uncertainty=numerical,sequential_error=envelope))


def separate(saved):
    """Different algebra/endpoint/path enumeration checks, all author-owned."""
    assert calculate()==saved
    # Sum the event distribution rather than the survival-area implementation.
    for row in saved['horizon']['policies']:
        for which in ['lower','upper']:
            s=list(map(F,row[which+'_witness']))
            distribution=[s[j-1]-s[j] for j in range(1,7)]+[s[6]]
            assert sum(distribution)==1 and min(distribution)>=0
            truncated=sum(F(min(j,6))*prob for j,prob in enumerate(distribution,1))
            assert truncated==F(row['restricted_time'][0 if which=='lower' else 1])
    # Closed-form frailty mixture moments instead of risk-set iteration.
    for name,haz in [('reference',[F(4,5),F(1,10)]),('policy',[F(2,5),F(1,20)])]:
        row=saved['selection'][name]
        surv=[sum((1-x)**t for x in haz)/2 for t in range(4)]
        assert list(map(str,surv))==row['survival']
        assert str(1-surv[3])==row['risk']
    # Enumerate all two-period first-event histories, including absorbing exits.
    for name,d,p,c in [('reference',F(1,10),F(1,10),0),
                       ('policy',F(3,25),F(3,5),3),
                       ('wrong_direct_mapping',F(6,125),F(3,5),3)]:
        first={'D':d,'P':p,'N':1-d-p};fd=fp=active=F(0)
        for x,y in product(first,repeat=2):
            prob=first[x]*first[y]
            fd+=prob*(x=='D' or (x=='N' and y=='D'))
            fp+=prob*(x=='P' or (x=='N' and y=='P'))
            active+=prob*(1+(x=='N'))
        row=saved['ordered_events'][name]
        assert [str(fd),str(fp),str(active)]==[row['default'],row['prepayment'],row['active_periods']]
        assert str(20*active-1000*fd-50*fp-c)==row['net_USD']
    # Integrate the pushforward density directly, not the natural-action map.
    z=sp.symbols('z',real=True)
    for power,key in [(1,'mean'),(2,'second_moment')]:
        moment=sp.integrate(z**power,(z,sp.Rational(1,4),sp.Rational(3,4)))+\
               2*sp.integrate(z**power,(z,sp.Rational(3,4),1))
        assert str(moment)==saved['pushforward'][key]
    # Differentiate the full target under a normalized assignment submodel.
    e=sp.symbols('e',real=True)
    theta=sp.integrate((z+sp.Rational(1,4))*(1+e*(2*z-1)),(z,0,sp.Rational(3,4)))+\
          sp.integrate(z*(1+e*(2*z-1)),(z,sp.Rational(3,4),1))
    assert str(sp.diff(theta,e))==saved['pushforward']['assignment_path_derivative']
    # Uniform-threshold pairs: delta is Bernoulli with probability0.1.
    vals=[(0,F(1,5)),(1,F(1,10)),(0,F(7,10))]
    mean=sum(F(x)*p for x,p in vals)
    var=sum(p*(F(x)-mean)**2 for x,p in vals)
    assert str(var)==saved['numerical_uncertainty']['paired_variance']
    return dict(status='pass',method='Separate event distributions, mixture formulas, absorbing-path enumeration, pushforward integrals and normalized path derivatives.',
        exact_families=8,observed_joint_law_equal=True,
        limitations=['Author checks, not an independent review or finite-sample coverage experiment.',
                     'No upstream package code executed; monetary quantities and transition envelopes are stipulated.'])


def main():
    from publish_latent_r_review_v2_20261013 import ref,write
    saved=calculate();write(BASE/'exact-results.json',saved)
    review=separate(saved)
    review['evidence']=[ref(BASE/'exact-results.json','Eight exact authored families'),
                        ref(Path(__file__),'Reference calculations and separate author checks')]
    write(BASE/'mathematics-review.json',review)
    print(json.dumps(dict(status=review['status'],families=8,
        horizon=saved['horizon']['net_difference_USD'],
        competing_delta=saved['ordered_events']['net_difference_USD'],
        pushforward=saved['pushforward'])))


if __name__=='__main__':main()
