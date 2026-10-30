#!/usr/bin/env python3
"""Fresh dynamic funding calibration; independently trained covariance diagnosis."""
import argparse
import json
import time
import numpy as np
from scipy.stats import norm, t
from threadpoolctl import threadpool_limits
from reliability_common import ROOT, Journal, SPEC, summarize
from dynamic_observation_study import make_linked
from causalbank.dynamic_funding import FundingTarget, train_pilot
from causalbank.responses import bartlett_lrv
from causalbank.linked_observation import linked_response
from closure_linkage_study import regular_from_primitives


def primitives(base,obs,design,seed,target,validate=False):
    law=dict(obs,correct_pair_probability=design['probability'])
    pilot=make_linked(base,law,design['pilot_dates'],[*seed,0]);fit=train_pilot(pilot,base['penalties'])
    data=make_linked(base,law,design['dates'],[*seed,1]);pred=data['x']@fit['coefficient']
    v=data['action']-pred[:,0];res=data['outcomes']-pred[:,1:];eta=[];scores=[]
    d=target.horizon+1;weights=target.weights()
    for group in (0,1):
        indicator=data['stratum']==group;q=np.mean(indicator*v*v)
        estimate=np.mean(indicator[:,None]*v[:,None]*res,axis=0)/q
        eta.append(estimate);scores.append(indicator[:,None]*v[:,None]*(res-v[:,None]*estimate)/q)
    B=np.zeros((4,4*d))
    for k in (0,1):
        B[2*k,2*k*d:(2*k+1)*d]=weights;B[2*k,(2*k+1)*d:(2*k+2)*d]=weights
        B[2*k+1,2*k*d:(2*k+1)*d]=weights;B[2*k+1,(2*k+1)*d:(2*k+2)*d]=-weights
    B*=.5
    means=B@np.asarray(eta).ravel();projected=np.column_stack(scores)@B.T
    if validate:
        n=design['audit_per_stratum'];p=np.asarray(design['probability']);band=int(2*design['dates']**.2)
        direct=linked_response(data,fit,p*n,[n,n],target,band)
        reconstructed=regular_from_primitives(means,bartlett_lrv(projected,band)/design['dates'],p,n,target.direct_cost())
        assert abs(reconstructed['estimate']-direct['financial_value'])<1e-7
        assert abs(reconstructed['se']-direct['financial_se'])<1e-7
    return means,projected,fit['penalty']


def convert(row):
    if row['status']!='computed':return row
    return dict(status='computed',estimate=row['estimate'],standard_error=float(row['se']),interval=row['interval'])


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--pilot',action='store_true');args=ap.parse_args()
    s=json.loads((ROOT/SPEC).read_text());c=s['calibration'];base=json.loads((ROOT/'docs/studies/dynamic-funding-spec.json').read_text());obs=json.loads((ROOT/'docs/studies/dynamic-observation-spec.json').read_text());target=FundingTarget(horizon=base['horizon'],branches=base['branches'])
    truth=float(target.weights()@(base['beta']*base['rho']**np.arange(target.horizon+1))-target.direct_cost())
    seed=s['pilot_seed'] if args.pilot else s['final_seed'];reps=s['pilot_repetitions'] if args.pilot else c['repetitions'];training_reps=s['pilot_repetitions'] if args.pilot else c['oracle_covariance_training_draws']
    inputs=['tools/reliability_calibration_study.py','tools/dynamic_observation_study.py','tools/closure_linkage_study.py','src/causalbank/dynamic_funding.py','src/causalbank/linked_observation.py','src/causalbank/responses.py','docs/studies/dynamic-funding-spec.json','docs/studies/dynamic-observation-spec.json']
    journal=Journal('calibration',inputs,args.pilot);start=time.perf_counter();results=[]
    designs=[dict(name='original_720',**c['original_baseline'])]+[dict(name=f'expanded_{n}',dates=n,pilot_dates=c['pilot_dates'],audit_per_stratum=c['audit_per_stratum'],probability=c['probability']) for n in c['dates']]
    with threadpool_limits(limits=1):
        primitives(base,obs,designs[0],[s['pilot_seed'],63,0],target,validate=True)
        for di,design in enumerate(designs):
            def train(i):
                m,_,penalty=primitives(base,obs,design,[s['pilot_seed'],60,di,i],target)
                return dict(mean=m,pilot_penalty=penalty)
            training=[journal.run(f'{design["name"]}/training/{i}',lambda i=i:train(i)) for i in range(training_reps)]
            training_m=np.array([r['mean'] for r in training]);oracle=np.cov(training_m,rowvar=False);p=np.array(design['probability']);coef=np.array([.5,.5/(2*p[0]-1),.5,.5/(2*p[1]-1)]);oracle_variance=float(coef@oracle@coef)
            def evaluate(i):
                m,scores,penalty=primitives(base,obs,design,[seed,61,di,i],target)
                n=design['audit_per_stratum'];counts=np.random.default_rng([seed,62,di,i]).binomial(n,p);methods={}
                for multiplier in c['bandwidth_multipliers']:
                    bandwidth=int(multiplier*design['dates']**c['bandwidth_exponent']);cov=bartlett_lrv(scores,bandwidth)/design['dates']
                    methods[f'bandwidth_{multiplier}']=convert(regular_from_primitives(m,cov,counts/n,n,target.direct_cost()))
                    methods[f'known_audit_bandwidth_{multiplier}']=convert(regular_from_primitives(m,cov,p,n,target.direct_cost(),True))
                # Independent reference covariance includes pilot fitting variation.
                phat=counts/n;rhat=2*phat-1;cref=np.array([.5,.5/rhat[0],.5,.5/rhat[1]]);j=-m[[1,3]]/rhat**2
                estimate=float(cref@m-target.direct_cost());variance=float(cref@oracle@cref+np.sum(j*j*phat*(1-phat)/n));se=np.sqrt(variance);critical=t.ppf(.975,training_reps-1)
                methods['independent_reference_covariance']=dict(status='computed',estimate=estimate,standard_error=float(se),interval=[estimate-critical*se,estimate+critical*se])
                est=float(coef@m-target.direct_cost());se=np.sqrt(oracle_variance)
                methods['known_audit_independent_reference']=dict(status='computed',estimate=est,standard_error=float(se),interval=[est-critical*se,est+critical*se])
                return dict(methods=methods,primitive_mean=m,audit_successes=counts,pilot_penalty=penalty)
            rows=[journal.run(f'{design["name"]}/evaluation/{i}',lambda i=i:evaluate(i)) for i in range(reps)]
            summary=summarize(rows,truth);results.append(dict(design=design,summary=summary,training_draws=training_reps,independent_reference_covariance=oracle,known_audit_training_bias=float(training_m.mean(axis=0)@coef-target.direct_cost()-truth),oracle_variance=oracle_variance))
            print(json.dumps({'design':design['name'],'primary':summary['bandwidth_2']['coverage_all']}),flush=True)
    journal.finish(dict(mode='pilot' if args.pilot else 'final',checks=dict(direct_public_estimate_and_covariance=True),financial_truth=truth,results=results,seconds=time.perf_counter()-start,
                        qualification='Fresh selected-mechanism diagnostics, not unique attribution of historical failures or a universal calibrated repair. Independent reference covariance is estimated from separate synthetic draws; its Student multiplier acknowledges finite training, but is not an exact finite-sample theorem for these non-Gaussian estimated responses.'))


if __name__=='__main__':main()
