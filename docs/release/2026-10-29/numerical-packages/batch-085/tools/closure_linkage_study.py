#!/usr/bin/env python3
"""Registered persistent-audit and joint-region comparisons, including failures."""
import argparse
import json
import time
import numpy as np
from scipy.stats import norm
from threadpoolctl import threadpool_limits
from closure_common import ROOT, save, coverage
from causalbank.persistent_audits import audited_pair_effect
from causalbank.ellipsoid_linkage import ellipsoid_projection
from causalbank.linkage_sets import decode_set, binomial_interval, sum_difference_projection, weighted_sum, encode_set
from causalbank.dynamic_funding import FundingTarget


def pair_sample(spec,rng,rate,noise=0.,biased=False):
    n,h=spec['pairs'],spec['dates'];x=rng.choice([-1.,1.],n)
    a=rng.choice([-1.,1.],(n,h))
    slope=spec['beta']+.9*x+rng.normal(0,.65,n)
    focal=slope[:,None]*a+rng.normal(0,.6,(n,1))+rng.normal(0,.7,(n,h))
    other=spec['companion_beta']*a+rng.normal(0,.7,(n,1))+rng.normal(0,.7,(n,h))
    mapping=rng.binomial(1,.5,n)  # exactly singular correctness-count mean model
    candidates=np.stack([np.where(mapping[:,None],focal,other),np.where(mapping[:,None],other,focal)],axis=1)
    q=rate*(1+.5*x);actual=q if not biased else np.minimum(.95,q*(1+.55*x))
    r=rng.binomial(1,actual,n);labels=np.abs(mapping-rng.binomial(1,noise,n))
    return a,candidates,r,labels,q,mapping


def persistent(spec,seed,reps):
    cases=[(f'audit_{q}',q,0.,False) for q in spec['audit_rates']]
    cases += [('label_noise',.3,.15,False),('false_inclusion_law',.3,0.,True)]
    output=[];truth=spec['beta']*spec['monetary_scale']
    for j,(name,rate,noise,biased) in enumerate(cases):
        runs=[]
        for rep in range(reps):
            rng=np.random.default_rng([seed,10,j,rep]);a,y,r,label,q,mapping=pair_sample(spec,rng,rate,noise,biased)
            methods={}
            for method,error,augment in [('augmented',noise,True),('ht',noise,False),('uncorrected_labels',0.,True)]:
                result=audited_pair_effect(a,y,r,label,q,label_error=error,monetary_scale=spec['monetary_scale'],augmentation=augment)
                methods[method]={k:result[k] for k in ('estimate','standard_error','interval','audited_pairs')}
            # Counterexamples: trust candidate 0; ignore unequal audit selection;
            # or treat the same map across H dates as H independent audits.
            means=np.mean(a[:,None,:]*y,axis=2);chosen=means[np.arange(len(a)),1-label]
            for method,z in [('trusted_wrong_alias',means[:,0]),('audited_only',chosen[r.astype(bool)])]:
                est=z.mean()*spec['monetary_scale'];se=z.std(ddof=1)/np.sqrt(len(z))*spec['monetary_scale']
                methods[method]=dict(estimate=est,standard_error=se,interval=[est-1.96*se,est+1.96*se])
            good=methods['augmented'];se=good['standard_error']/np.sqrt(a.shape[1])
            methods['dates_as_audits']=dict(estimate=good['estimate'],standard_error=se,interval=[good['estimate']-1.96*se,good['estimate']+1.96*se])
            runs.append({'rep':rep,'methods':methods})
        summary={}
        for method in runs[0]['methods']:
            rows=[r['methods'][method] for r in runs]
            summary[method]={'coverage':coverage(sum(r['interval'][0]<=truth<=r['interval'][1] for r in rows),reps),
                             'bias':float(np.mean([r['estimate'] for r in rows])-truth),
                             'mean_se':float(np.mean([r['standard_error'] for r in rows])),
                             'mean_width':float(np.mean([r['interval'][1]-r['interval'][0] for r in rows])),
                             'positive_decision_fraction':float(np.mean([r['interval'][0]>0 for r in rows]))}
        output.append({'case':name,'truth':truth,'summary':summary,'runs':runs})
        print(json.dumps({'pair_case':name,'primary':summary['augmented']}),flush=True)
    return output


def regular_from_primitives(m,v,p,n,cost=0.,known=False):
    r=2*np.asarray(p)-1
    if np.any(abs(r)<1e-12):
        return {'status':'unavailable'}
    c=np.array([.5,.5/r[0],.5,.5/r[1]])
    j=-m[[1,3]]/r**2
    estimate=float(c@m-cost)
    variance=float(c@v@c+(0 if known else np.sum(j*j*np.asarray(p)*(1-np.asarray(p))/n)))
    se=np.sqrt(variance)
    return dict(status='computed',estimate=estimate,se=se,interval=[estimate-1.96*se,estimate+1.96*se])


def projection_summary(runs,truth):
    output={}
    methods=runs[0]['methods'].keys()
    for method in methods:
        rows=[r['methods'][method] for r in runs]
        sets=[decode_set(r['financial_set']) if 'financial_set' in r else ([r['interval']] if r.get('status')=='computed' else []) for r in rows]
        covered=sum(any(lo<=truth<=hi for lo,hi in s) for s in sets)
        bounded=[s for s in sets if s and all(np.isfinite(x) for pair in s for x in pair)]
        available=sum(r.get('status') in ('computed','computed_set') for r in rows)
        output[method]={'coverage_all':coverage(covered,len(rows)), 'available':available,
                        'coverage_given_available':covered/available if available else None,
                        'bounded_fraction':len(bounded)/len(rows),
                        'whole_line_fraction':sum(s==[(-np.inf,np.inf)] for s in sets)/len(rows),
                        'disconnected_fraction':sum(len(s)>1 for s in sets)/len(rows),
                        'median_width_given_bounded':float(np.median([sum(b-a for a,b in s) for s in bounded])) if bounded else None}
    return output


def retrospective(spec):
    old=json.loads((ROOT/spec['retrospective_input']).read_text())
    base=json.loads((ROOT/'docs/studies/dynamic-funding-spec.json').read_text())
    obs=json.loads((ROOT/'docs/studies/dynamic-observation-spec.json').read_text())
    target=FundingTarget(horizon=base['horizon'],branches=base['branches'])
    focal=float(target.weights()@(base['beta']*base['rho']**np.arange(target.horizon+1)))
    companion=float(target.weights()@(obs['decoy_beta']*base['rho']**np.arange(target.horizon+1)))
    out=[]
    for case in old['results']:
        p=np.array(case['case']['probability']);r=2*p-1;n=old['spec']['audit_per_stratum'];runs=[]
        mtrue=np.array([(focal+companion)/2,r[0]*(focal-companion)/2,(focal+companion)/2,r[1]*(focal-companion)/2])
        for row in case['runs']:
            m=np.array(row['projection']['transformed_means']);v=np.array(row['projection']['transformed_covariance']);counts=np.array(row['audit_successes']);phat=counts/n
            reg=row['regular'];methods={
                'rectangle':dict(status='computed_set',financial_set=row['projection']['financial_set']),
                'ellipsoid':ellipsoid_projection(m,v,counts,[n,n],offset=-target.direct_cost()),
                'known_audit':regular_from_primitives(m,v,p,n,target.direct_cost(),True),
                'regular_retained':dict(status=reg['status'],interval=reg.get('financial_interval',[])),
                'known_response':regular_from_primitives(mtrue,np.zeros((4,4)),phat,n,target.direct_cost())}
            if np.all(r!=0):
                c=np.array([.5,.5/r[0],.5,.5/r[1]]);j=-mtrue[[1,3]]/r**2
                linear=float(old['financial_truth']+c@(m-mtrue)+j@(phat-p))
                se=float(np.sqrt(c@v@c+np.sum(j*j*p*(1-p)/n)))
                methods['oracle_linearization']=dict(status='computed',interval=[linear-1.96*se,linear+1.96*se])
            else:
                methods['oracle_linearization']=dict(status='unavailable')
            runs.append(dict(rep=row['rep'],methods=methods))
        summary=projection_summary(runs,old['financial_truth'])
        out.append(dict(case=case['case']['name'],summary=summary,runs=runs))
        print(json.dumps({'retrospective':case['case']['name'],'summary':summary}),flush=True)
    return out


def fresh(spec,seed,reps):
    out=[];n=spec['audit_per_stratum'];truth=1.2
    corr=np.array([[1.,.3,.4,0.],[.3,1.,0.,.2],[.4,0.,1.,.3],[0.,.2,.3,1.]])*4/spec['response_n']
    for j,prob in enumerate(spec['regimes']):
        p=np.array(prob);r=2*p-1;mtrue=np.array([.4,.8*r[0],.4,.8*r[1]]);runs=[]
        for rep in range(reps):
            rng=np.random.default_rng([seed,11,j,rep]);m=rng.multivariate_normal(mtrue,corr);counts=rng.binomial(n,p)
            z=norm.ppf(1-.05/16);bands=np.column_stack([m-z*np.sqrt(np.diag(corr)),m+z*np.sqrt(np.diag(corr))])
            sets=[sum_difference_projection(bands[2*s],bands[2*s+1],binomial_interval(int(counts[s]),n,.05/4)) for s in (0,1)]
            methods={'ellipsoid':ellipsoid_projection(m,corr,counts,[n,n]),
                     'rectangle':dict(status='computed_set',financial_set=encode_set(weighted_sum(sets,[.5,.5]))),
                     'regular':regular_from_primitives(m,corr,counts/n,n),
                     'known_audit':regular_from_primitives(m,corr,p,n,known=True)}
            runs.append(dict(rep=rep,methods=methods))
        summary=projection_summary(runs,truth)
        out.append(dict(probability=prob,summary=summary,runs=runs))
        print(json.dumps({'fresh_probability':prob,'ellipsoid':summary['ellipsoid']}),flush=True)
    return out


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--pilot',action='store_true');args=parser.parse_args()
    spec=json.loads((ROOT/'docs/studies/closure-spec.json').read_text());start=time.perf_counter()
    seed=spec['pilot_seed'] if args.pilot else spec['final_seed']
    with threadpool_limits(limits=1):
        pairs=persistent(spec['persistent'],seed,spec['persistent']['pilot_repetitions'] if args.pilot else spec['persistent']['repetitions'])
        projected=fresh(spec['projection'],seed,spec['projection']['pilot_repetitions'] if args.pilot else spec['projection']['fresh_repetitions'])
        previous=[] if args.pilot else retrospective(spec['projection'])
    save('docs/studies/closure-linkage-'+('pilot' if args.pilot else 'results')+'.json',
         dict(mode='pilot' if args.pilot else 'final',persistent=pairs,fresh=projected,retrospective=previous,seconds=time.perf_counter()-start),
         ['tools/closure_linkage_study.py','tools/closure_common.py','src/causalbank/persistent_audits.py','src/causalbank/ellipsoid_linkage.py','src/causalbank/linkage_sets.py','docs/studies/closure-spec.json',spec['projection']['retrospective_input'],'docs/studies/dynamic-funding-spec.json','docs/studies/dynamic-observation-spec.json'])


if __name__=='__main__':
    main()
