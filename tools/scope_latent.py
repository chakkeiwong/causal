#!/usr/bin/env python3
"""Joint observational controlled-model and validation-sample experiment."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import time
import numpy as np
from threadpoolctl import threadpool_limits
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from causalbank.validated_latent import ModelShape,pack,fit,contrast,uncertainty


def categorical(prob,rng):
    return (rng.random(len(prob))[:,None]>np.cumsum(prob,axis=1)).sum(axis=1)


def generate(spec,calibration_size,rng):
    n,h=spec['trajectories'],spec['horizon']
    mu,e,q,t,reward=[np.array(spec[k]) for k in ['mu','emission','logger','transition','reward']]
    states=rng.choice(len(mu),size=n,p=mu); o=np.empty((n,h),int); a=np.empty_like(o); r=np.empty((n,h))
    for j in range(h):
        o[:,j]=categorical(e[states],rng); a[:,j]=categorical(q[states],rng)
        r[:,j]=reward[a[:,j],states]+spec['reward_sd']*rng.normal(size=n)
        if j<h-1: states=categorical(t[a[:,j],states],rng)
    labels=rng.integers(0,len(mu),size=calibration_size); cal_o=categorical(e[labels],rng)
    return (o,a,r),(labels,cal_o)


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--pilot',action='store_true'); args=ap.parse_args()
    path=ROOT/'docs/studies/scope-latent-spec.json'; spec=json.loads(path.read_text()); reps=2 if args.pilot else spec['repetitions']
    shape=ModelShape(reward_sd=spec['reward_sd']); truth_parameter=pack(*[np.array(spec[k]) for k in ['mu','emission','logger','transition','reward']],shape)
    truth=contrast(truth_parameter,shape,spec['horizon']); all_results=[]; start=time.perf_counter()
    with threadpool_limits(limits=1):
        for j,size in enumerate(spec['calibration_sizes']):
            rows=[]
            for rep in range(reps):
                rng=np.random.default_rng(np.random.SeedSequence([spec['seed'],j,rep])); obs,cal=generate(spec,size,rng)
                parameter,diagnostics=fit(obs,cal,shape,seed=rep+19,starts=spec['starts'],maxiter=spec['maxiter'])
                info=uncertainty(parameter,obs,cal,shape,spec['horizon'])
                row={'repetition':rep,'estimate':contrast(parameter,shape,spec['horizon']),'fit':diagnostics,'information':info}
                if rep<20:
                    omitted=ModelShape(reward_sd=shape.reward_sd,include_logger=False)
                    p,d=fit(obs,cal,omitted,seed=rep+19,starts=spec['starts'],maxiter=spec['maxiter'])
                    row['omitted_logger']={'estimate':contrast(p,omitted,spec['horizon']),'fit':d}
                rows.append(row)
                if rep%10==0: print(json.dumps({'calibration':size,'repetition':rep,'estimate':row['estimate'],'truth':truth,'fit':diagnostics['optimizer_success'],'information':info.get('available')}),flush=True)
            summary={'calibration':size,'requested':reps,'truth':truth,'bias':float(np.mean([r['estimate']-truth for r in rows])),
                'fit_failures':sum(not r['fit']['optimizer_success'] or r['fit']['on_boundary'] or not r['information']['available'] for r in rows),'coverage':{}}
            for key in ['model_se','sandwich_se','treat_emissions_fixed_se']:
                covered=[r['fit']['optimizer_success'] and not r['fit']['on_boundary'] and r['information']['available'] and abs(r['estimate']-truth)<=1.959963984540054*r['information'].get(key,0) for r in rows]
                summary['coverage'][key]=float(np.mean(covered))
            summary['omitted_logger_bias']=float(np.mean([r['omitted_logger']['estimate']-truth for r in rows if 'omitted_logger' in r]))
            all_results.append({'summary':summary,'runs':rows}); print(json.dumps(summary),flush=True)
    files=[path,Path(__file__),ROOT/'src/causalbank/validated_latent.py']
    receipt={'mode':'pilot' if args.pilot else 'final','spec':spec,'results':all_results,'seconds':time.perf_counter()-start,'input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},'scope':'Private state logging with independently validated invariant emissions; conditional structural model, known reward noise, fixed observable policies, no global optimizer certificate.'}
    (ROOT/'docs/studies'/('scope-latent-pilot.json' if args.pilot else 'scope-latent-results.json')).write_text(json.dumps(receipt,indent=2)+'\n')


if __name__=='__main__': main()
