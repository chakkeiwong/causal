#!/usr/bin/env python3
"""Execute preregistered dependent-response/short-panel comparisons."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import time
import numpy as np
from scipy.stats import norm
from threadpoolctl import threadpool_limits
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from causalbank.dependent_inference import (response_alternatives, prewhitened_lrv,
    lag_augmented_projection, panel_moments, linear_gmm)
from causalbank.responses import bartlett_lrv, set_contains
from study_responses import generate


def summarize(values, requested):
    a=np.asarray(values,float)
    return {"coverage":float(a.mean()),"mc_se":float(np.sqrt(a.mean()*(1-a.mean())/requested)),"requested":requested}


def run(spec, reps):
    results={"responses":[],"scalar_lp":[],"common_shock":[],"panels":[]}
    for j,case in enumerate(spec['response_cases']):
        metrics={k:[] for k in ['bartlett_short','bartlett_long','prefilter_bartlett']}
        failures={k:[] for k in metrics}; unbounded={k:[] for k in metrics}
        for r in range(reps):
            x,z,truth=generate(case,spec['horizon'],np.random.default_rng(np.random.SeedSequence([spec['seed'],1,j,r])))
            out=response_alternatives(x,z,spec['horizon'])
            for k,v in out.items():
                if v['status']=='failed':
                    metrics[k].append(False); unbounded[k].append(False); failures[k].append({'repetition':r,'error':v['error']})
                else:
                    metrics[k].append(all(set_contains(s,t) for s,t in zip(v['sets'],truth)))
                    unbounded[k].append(any(lo is None or hi is None for s in v['sets'] for lo,hi in s))
        row={'case':case,'metrics':{k:{**summarize(v,reps),'unbounded':float(np.mean(unbounded[k])),'failures':failures[k]} for k,v in metrics.items()}}
        results['responses'].append(row); print(json.dumps({'response':case['id'],'coverage':{k:v['coverage'] for k,v in row['metrics'].items()}}),flush=True)
    lp=spec['scalar_lp']
    for j,rho in enumerate(lp['roots']):
        metrics=[]
        for r in range(reps):
            rng=np.random.default_rng(np.random.SeedSequence([spec['seed'],2,j,r])); y=np.zeros(lp['dates']+max(lp['horizons'])+1)
            for t in range(1,len(y)): y[t]=rho*y[t-1]+rng.normal()
            est,se=lag_augmented_projection(y,lp['horizons'])
            truth=np.array([rho**h for h in lp['horizons']])
            metrics.append((np.abs(est-truth)<=norm.ppf(1-.05/(2*len(truth)))*se).all())
        row={'rho':rho,**summarize(metrics,reps)}; results['scalar_lp'].append(row); print(json.dumps({'lp':row}),flush=True)
    common=spec['common_shock']
    for j,n in enumerate(common['dates']):
        metrics={'short':[],'prefilter':[]}; widths={k:[] for k in metrics}
        for r in range(reps):
            rng=np.random.default_rng(np.random.SeedSequence([spec['seed'],3,j,r])); x=np.empty(n); state=rng.normal()/np.sqrt(1-common['rho']**2)
            for t in range(n): state=common['rho']*state+rng.normal(); x[t]=common['mean']+state
            estimates=[bartlett_lrv(x[:,None],int(n**.25))[0,0],prewhitened_lrv(x[:,None],int(n**.25))[0][0,0]]
            for k,lrv in zip(metrics,estimates):
                half=norm.ppf(.975)*np.sqrt(lrv/n); metrics[k].append(abs(x.mean()-common['mean'])<=half); widths[k].append(2*half)
        row={'dates':n,'metrics':{k:{**summarize(v,reps),'mean_width':float(np.mean(widths[k]))} for k,v in metrics.items()}}
        results['common_shock'].append(row); print(json.dumps({'common':row}),flush=True)
    for j,case in enumerate(spec['panel_cases']):
        methods=['difference_one','difference_two','system_one','system_two']; metrics={k:[] for k in methods}; biases={k:[] for k in methods}; failures={k:[] for k in methods}
        for r in range(reps):
            rng=np.random.default_rng(np.random.SeedSequence([spec['seed'],4,j,r])); n=case['entities']; T=case['periods']; rho=case['rho']
            alpha=rng.normal(size=n); xstate=np.zeros(n); ystate=np.zeros(n); err=np.zeros(n)
            for t in range(400):
                err=case['serial_error']*err+rng.normal(size=n); xstate=.5*xstate+.4*err+rng.normal(size=n); ystate=alpha+rho*ystate+.6*xstate+err
            ystate+=case['initial_departure']*alpha
            x=np.empty((n,T+1)); y=np.empty_like(x); x[:,0]=xstate; y[:,0]=ystate
            for t in range(1,T+1):
                err=case['serial_error']*err+rng.normal(size=n); x[:,t]=.5*x[:,t-1]+.4*err+rng.normal(size=n); y[:,t]=alpha+rho*y[:,t-1]+.6*x[:,t]+err
            for k in methods:
                try:
                    b,g=panel_moments(y,x,system=k.startswith('system')); fit=linear_gmm(b,g,two_step=k.endswith('two'))
                    error=fit['estimate']-np.array([rho,.6]); se=np.sqrt(np.diag(fit['covariance']))
                    metrics[k].append((np.abs(error)<=norm.ppf(.9875)*se).all()); biases[k].append(error.tolist())
                except (ValueError,np.linalg.LinAlgError) as exc:
                    metrics[k].append(False); failures[k].append({'repetition':r,'error':str(exc)})
        row={'case':case,'metrics':{k:{**summarize(v,reps),'bias':np.mean(biases[k],axis=0).tolist() if biases[k] else None,'failures':failures[k]} for k,v in metrics.items()}}
        results['panels'].append(row); print(json.dumps({'panel':case['id'],'metrics':row['metrics']}),flush=True)
    return results


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--pilot',action='store_true'); args=ap.parse_args()
    path=ROOT/'docs/studies/scope-inference-spec.json'; spec=json.loads(path.read_text()); start=time.perf_counter()
    with threadpool_limits(limits=1): result=run(spec,12 if args.pilot else spec['repetitions'])
    inputs=[path,Path(__file__),ROOT/'src/causalbank/dependent_inference.py',ROOT/'src/causalbank/responses.py',ROOT/'tools/study_responses.py']
    receipt={'mode':'pilot' if args.pilot else 'final','spec':spec,'seconds':time.perf_counter()-start,'results':result,'input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},'scope':'Preregistered finite experiments and model-conditional alternatives; failures retained; not universal qualification.'}
    (ROOT/'docs/studies'/('scope-inference-pilot.json' if args.pilot else 'scope-inference-results.json')).write_text(json.dumps(receipt,indent=2)+'\n')


if __name__=='__main__': main()
