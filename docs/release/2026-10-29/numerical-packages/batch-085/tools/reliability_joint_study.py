#!/usr/bin/env python3
"""Joint pair/calendar experiment; separate independent design and evaluation."""
import argparse
import json
import time
import numpy as np
from scipy.stats import norm
from threadpoolctl import threadpool_limits
from reliability_common import ROOT, Journal, summarize, SPEC
from causalbank.joint_audited import joint_effect, allocate_audits, bartlett


def sample(s, rng, rates=None, adverse=None):
    n,t=s['pairs'],s['dates']; x=rng.choice([-1.,1.],n); group=(x>0).astype(int)
    a=rng.choice([-1.,1.],(n,t)); slope=s['beta']+.9*x+rng.normal(0,s['pair_sd'],n)
    c=np.empty(t);c[0]=rng.normal(0,s['calendar_sd'])
    for j in range(1,t):c[j]=s['calendar_rho']*c[j-1]+s['calendar_sd']*np.sqrt(1-s['calendar_rho']**2)*rng.normal()
    focal=(slope[:,None]+c)*a+rng.normal(0,.7,(n,t))
    other=(s['companion_beta']+.3*c)*a+rng.normal(0,.7,(n,t))
    mapping=rng.binomial(1,.5,n)
    y=np.stack([np.where(mapping[:,None],focal,other),np.where(mapping[:,None],other,focal)],axis=1)
    q=s['audit_rate']*(1+.5*x) if rates is None else np.asarray(rates)[group]
    actual=np.minimum(.98,q*(1+.55*x)) if adverse=='false_inclusion' else q
    error=s['label_error']+(.14*x if adverse=='selected_label_errors' else 0)
    label=np.abs(mapping-rng.binomial(1,error,n));r=rng.binomial(1,actual,n)
    gold=rng.binomial(1,s['label_error'],s['gold_labels'])
    return a,y,r,label,q,gold,group


def comparison(s, rng, rates=None, adverse=None):
    a,y,r,label,q,gold,group=sample(s,rng,rates,adverse);band=int(2*s['dates']**.25)
    primary=joint_effect(a,y,r,label,q,bandwidth=band,gold_errors=gold,scale=s['monetary_scale'])
    methods={'joint':primary}
    for name,parts in [('pair_only',['pair','validation']),('calendar_only',['calendar','validation']),('ignore_gold_uncertainty',['pair','calendar'])]:
        if primary['status']!='computed':methods[name]=primary;continue
        se=np.sqrt(sum(primary['variance_components'][p] for p in parts));est=primary['estimate'];z=norm.ppf(.975)
        methods[name]=dict(status='computed',estimate=est,standard_error=se,interval=[est-z*se,est+z*se])
    methods['ignore_label_error']=joint_effect(a,y,r,label,q,bandwidth=band,scale=s['monetary_scale'])
    methods['known_label_error_diagnostic']=joint_effect(a,y,r,label,q,bandwidth=band,known_label_error=s['label_error'],scale=s['monetary_scale'])
    return dict(methods=methods,actual_audit_cost=float(r@np.asarray(s['audit_costs'])[group]),
                expected_audit_cost=float(q@np.asarray(s['audit_costs'])[group]))


def checks(s):
    # Exhaustive expectation over audit and symmetric flip, independent of API.
    e=.15;q=.27;f=2.3;o=-.7;av=(f+o)/2;values=[]
    for audit in (0,1):
        for flip in (0,1):
            prob=(q if audit else 1-q)*(e if flip else 1-e)
            values.append(prob*(av+audit/q*(1-2*flip)*(f-o)/(2*(1-2*e))))
    x=np.array([2.,-1.,3.,4.,-.2]);L=2;center=x-x.mean()
    K=np.maximum(0,1-abs(np.arange(5)[:,None]-np.arange(5)[None,:])/(L+1))
    # Independent dense kernel reconstruction and error-rate derivative.
    h=1e-6;fn=lambda z: av+(f-o)/(2*(1-2*z)*q)
    derivative=(f-o)/(q*(1-2*e)**2)
    a,y,r,label,p,gold,_=sample(s,np.random.default_rng(822000))
    invalid=False
    try:joint_effect(a,y,r,label,p,bandwidth=3,sampling='arbitrary_dependence')
    except ValueError:invalid=True
    rank=joint_effect(a,y,r,label,p,bandwidth=3,gold_errors=np.tile([0,1],30))
    d=np.array([.5,3.]);cost=np.array([1.,3.]);prob=np.array([.5,.5]);B=.6
    alloc=allocate_audits(d,cost,prob,B)
    grid=np.linspace(.02001,.99999,20000);q2=(B-.5*grid)/1.5;valid=(q2>=.02)&(q2<=1)
    optimum=float(prob@(d/alloc));grid_min=float(np.min(.5*d[0]/grid[valid]+.5*d[1]/q2[valid]))
    return dict(audit_expectation=abs(sum(values)-f)<1e-12,
                independent_dense_bartlett=abs(bartlett(x,L)-center@K@center/len(x))<1e-12,
                label_derivative=abs((fn(e+h)-fn(e-h))/(2*h)-derivative)<1e-7,
                allocation_budget=abs(prob@(cost*alloc)-B)<1e-12,
                allocation_global_grid=optimum<=grid_min+1e-9,
                unsupported_sampling=invalid,label_rank_refusal=rank['status']=='unqualified_label_rank')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--pilot',action='store_true');args=ap.parse_args()
    allspec=json.loads((ROOT/SPEC).read_text());s=allspec['joint'];seed=allspec['pilot_seed'] if args.pilot else allspec['final_seed'];reps=allspec['pilot_repetitions'] if args.pilot else s['repetitions']
    journal=Journal('joint',['tools/reliability_joint_study.py','src/causalbank/joint_audited.py','src/causalbank/linkage_sets.py'],args.pilot)
    start=time.perf_counter();verified=checks(s);assert all(verified.values()),verified
    # This independent fully labelled pilot pays for histories and labels.
    def design():
        ps=dict(s,pairs=s['audit_pilot_pairs']);a,y,r,label,q,gold,g=sample(ps,np.random.default_rng([allspec['pilot_seed'],900]),[1,1])
        difference=np.mean(a[:,None,:]*y,axis=2);D=(difference[:,0]-difference[:,1])/(2*(1-2*s['label_error']))
        moments=np.array([np.mean(D[g==k]**2) for k in (0,1)])
        alloc=allocate_audits(moments,s['audit_costs'],[.5,.5],s['expected_audit_budget_per_pair'])
        uniform=s['expected_audit_budget_per_pair']/np.mean(s['audit_costs'])
        floor=s['calendar_sd']**2*(1+s['calendar_rho'])/(1-s['calendar_rho'])/s['dates']
        half=norm.ppf(.975)*np.sqrt(floor)*s['monetary_scale']
        return dict(inclusion=alloc,uniform_inclusion=[uniform,uniform],second_moments=moments,
                    pilot_pairs=s['audit_pilot_pairs'],pilot_audit_cost=float(np.sum(np.asarray(s['audit_costs'])[g])),
                    known_error_for_design=s['label_error'],design_information='Pilot allocation conditions on a supplied symmetric error law; evaluation estimates it using independent gold labels.',
                    calendar_halfwidth_floor_currency=float(half),targets=[dict(halfwidth=h,calendar_floor_permits=h>half) for h in s['halfwidth_targets_currency']])
    training=journal.run('audit_design',design);results=[]
    with threadpool_limits(limits=1):
        cases=[('declared_joint',None,None),('uniform_cost',training['uniform_inclusion'],None),('pilot_allocation',training['inclusion'],None),('false_inclusion',None,'false_inclusion'),('selected_label_errors',None,'selected_label_errors')]
        for ci,(name,rates,adverse) in enumerate(cases):
            # The two allocation arms reuse each evaluation RNG, holding law/labels fixed.
            stream=1 if name in ('uniform_cost','pilot_allocation') else ci+10
            rows=[journal.run(f'{name}/{i}',lambda i=i:comparison(s,np.random.default_rng([seed,stream,i]),rates,adverse)) for i in range(reps)]
            summary=summarize(rows,s['beta']*s['monetary_scale'])
            results.append(dict(case=name,summary=summary,mean_actual_audit_cost=float(np.mean([r['actual_audit_cost'] for r in rows])),mean_expected_audit_cost=float(np.mean([r['expected_audit_cost'] for r in rows]))))
            print(json.dumps({'case':name,'joint_coverage':summary['joint']['coverage_all']}),flush=True)
    journal.finish(dict(mode='pilot' if args.pilot else 'final',checks=verified,design=training,results=results,seconds=time.perf_counter()-start,
                        scope='Selected joint law only; false sampling/label declarations can violate coverage and are not automatically detectable.'))


if __name__=='__main__':main()
