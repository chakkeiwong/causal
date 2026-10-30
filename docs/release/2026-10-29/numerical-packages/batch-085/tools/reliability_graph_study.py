#!/usr/bin/env python3
import argparse
import json
import time
import numpy as np
from scipy.stats import t
from threadpoolctl import threadpool_limits
from reliability_common import ROOT, Journal, SPEC, summarize
from causalbank.gaussian_effect_pivots import effect_confidence, quadratic_sublevel
from causalbank.latent_temporal_sets import effect_set
from causalbank.linkage_sets import decode_set
from closure_discovery_study import sample


def checks():
    rng=np.random.default_rng(822100);fail=0;total=0
    for _ in range(200):
        coef=rng.normal(size=3);pieces=quadratic_sublevel(*coef)
        for z in rng.normal(0,4,50):
            total+=1;fail+=bool(any(lo<=z<=hi for lo,hi in pieces))!=bool(coef[0]*z*z+coef[1]*z+coef[2]<=0)
    x=sample(rng,120,strength=.1);out=effect_confidence(x,information='randomized_encouragement');z=x[:,0];a=x[:,1];y=x[:,2];design=np.column_stack([np.ones(len(z)),z]);pieces=decode_set(out['effect_set']);mismatch=0
    for beta in np.linspace(-20,20,201):
        target=y-beta*a;coef=np.linalg.lstsq(design,target,rcond=None)[0];res=target-design@coef
        se=np.sqrt(res@res/(len(z)-2)*np.linalg.inv(design.T@design)[1,1]);accept=abs(coef[1])<=t.ppf(.975,len(z)-2)*se
        mismatch+=accept!=any(lo<=beta<=hi for lo,hi in pieces)
    return dict(random_polynomial_membership=fail==0,direct_null_test_membership=mismatch==0,
                bounded=len(quadratic_sublevel(1,0,-1))==1,two_rays=len(quadratic_sublevel(-1,0,1))==2,
                empty=quadratic_sublevel(1,0,1)==[],whole=quadratic_sublevel(-1,0,-1)==[(-np.inf,np.inf)],
                constant_zero=quadratic_sublevel(0,0,0)==[(-np.inf,np.inf)],linear=len(quadratic_sublevel(0,1,1))==1,
                rank_refused=effect_confidence(np.ones((20,3)),information='observed_sufficiency')['status']=='unqualified_design')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--pilot',action='store_true');args=ap.parse_args();s=json.loads((ROOT/SPEC).read_text());seed=s['pilot_seed'] if args.pilot else s['final_seed'];reps=s['pilot_repetitions'] if args.pilot else s['graphs']['repetitions']
    journal=Journal('graphs',['tools/reliability_graph_study.py','tools/closure_discovery_study.py','src/causalbank/gaussian_effect_pivots.py','src/causalbank/latent_temporal_sets.py','src/causalbank/linkage_sets.py'],args.pilot)
    start=time.perf_counter();verified=checks();assert all(verified.values()),verified;results=[]
    cases=[('strong_valid',1.,0.,.8),('weak_valid',.05,0.,.8),('zero_stage',0.,0.,.8),('false_exclusion',1.,.8,.8),('sufficient',1.,.3,0.),('omitted_cause',1.,.4,1.2)]
    with threadpool_limits(limits=1):
        for ci,(name,strength,direct,hidden) in enumerate(cases):
            def run(i):
                x=sample(np.random.default_rng([seed,40,ci,i]),s['graphs']['episodes'],strength,direct,hidden);methods={}
                for info in ('observational_latent','randomized_encouragement','observed_sufficiency'):
                    methods['pivot_'+info]=effect_confidence(x,information=info)
                    old=effect_set(x,information=info);methods['v7_'+info]=dict(status='computed_set',effect_set=old['effect_set'])
                return dict(methods=methods)
            rows=[journal.run(f'{name}/{i}',lambda i=i:run(i)) for i in range(reps)]
            results.append(dict(case=name,truth=.7,summary=summarize(rows,.7)))
            print(json.dumps({'case':name,'encouragement':results[-1]['summary']['pivot_randomized_encouragement']['coverage_all']}),flush=True)
    journal.finish(dict(mode='pilot' if args.pilot else 'final',checks=verified,results=results,seconds=time.perf_counter()-start,
                        scope='Exact Gaussian true-null pivots for declared finite information classes; adverse supplied restrictions remain false.'))


if __name__=='__main__':main()
