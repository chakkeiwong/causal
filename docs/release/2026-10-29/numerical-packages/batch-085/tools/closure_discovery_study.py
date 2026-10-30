#!/usr/bin/env python3
import argparse
import json
import time
import numpy as np
from closure_common import ROOT,save,coverage
from causalbank.latent_temporal_sets import effect_set,unrestricted_witness,ratio_region
from causalbank.linkage_sets import decode_set


def sample(rng,n,strength=1.,direct=0.,hidden=.8):
    z,u,e,r=rng.normal(size=(4,n));a=strength*z+hidden*u+e;y=.7*a+direct*z+hidden*u+r
    return np.column_stack([z,a,y])


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--pilot',action='store_true');args=ap.parse_args()
    whole=json.loads((ROOT/'docs/studies/closure-spec.json').read_text());spec=whole['discovery'];seed=whole['pilot_seed'] if args.pilot else whole['final_seed'];reps=spec['pilot_repetitions'] if args.pilot else spec['repetitions']
    start=time.perf_counter();results=[]
    cases=[('hidden_strong',1.,0.,.8),('hidden_weak',.05,0.,.8),('false_exclusion',1.,.8,.8),('sufficient',1.,.3,0.),('omitted_prior_cause',1.,.4,1.2)]
    for ci,(name,strength,direct,hidden) in enumerate(cases):
        runs=[]
        for rep in range(reps):
            x=sample(np.random.default_rng([seed,20,ci,rep]),spec['episodes'],strength,direct,hidden)
            methods={}
            for information in ('observational_latent','randomized_encouragement','observed_sufficiency'):
                result=effect_set(x,information=information,alpha=spec['alpha'])
                methods[information]={'set':result['effect_set'],'graphs':result['enumerated_graphs']}
            # The deliberately naive OLS effect treats hidden confounding as absent.
            design=np.column_stack([np.ones(len(x)),x[:,:2]]);coef=np.linalg.lstsq(design,x[:,2],rcond=None)[0]
            resid=x[:,2]-design@coef;se=np.sqrt((resid@resid)/(len(x)-3)*np.linalg.inv(design.T@design)[2,2])
            methods['selected_sufficient_regression']={'set':[{'lower':coef[2]-1.96*se,'upper':coef[2]+1.96*se}]}
            runs.append({'rep':rep,'methods':methods})
        summary={}
        for method in runs[0]['methods']:
            sets=[decode_set(r['methods'][method]['set']) for r in runs];bounded=[s for s in sets if s and all(np.isfinite(v) for p in s for v in p)]
            summary[method]={'coverage':coverage(sum(any(a<=.7<=b for a,b in s) for s in sets),reps),
                             'bounded_fraction':len(bounded)/reps,'whole_line_fraction':sum(s==[(-np.inf,np.inf)] for s in sets)/reps,
                             'median_width_given_bounded':float(np.median([sum(b-a for a,b in s) for s in bounded])) if bounded else None}
        results.append(dict(case=name,truth=.7,summary=summary,runs=runs))
        print(json.dumps({'case':name,'summary':summary}),flush=True)
    example=sample(np.random.default_rng(5050),600);cov=np.cov(example,rowvar=False);witnesses=[unrestricted_witness(cov,b) for b in (-20.,0.,.7,20.)]
    witness_error=max(np.max(abs(w['recovered_covariance']-cov)) for w in witnesses)
    checks={'same_law_distinct_effects':bool(witness_error<1e-10),
            'positive_witness_noises':all(np.all(w['noise_variances']>0) for w in witnesses),
            'two_rays':len(ratio_region([1.,2.],[-1.,1.]))==2,
            'zero_compatibility_retained':ratio_region([-.1,.1],[-1.,1.])==[(-np.inf,np.inf)]}
    try:effect_set(example,sampling='dependent_calendar');checks['unsupported_sampling_rejected']=False
    except ValueError:checks['unsupported_sampling_rejected']=True
    output=dict(mode='pilot' if args.pilot else 'final',results=results,checks=checks,witnesses=witnesses,witness_max_error=witness_error,
                seconds=time.perf_counter()-start,scope='Finite Gaussian class and conservative graph/parameter retention; false restrictions are adverse fixtures, not covered designs.')
    save('docs/studies/closure-discovery-'+('pilot' if args.pilot else 'results')+'.json',output,
         ['tools/closure_discovery_study.py','tools/closure_common.py','src/causalbank/latent_temporal_sets.py','src/causalbank/linkage_sets.py','docs/studies/closure-spec.json'])
    raise SystemExit(not all(checks.values()))


if __name__=='__main__':main()
