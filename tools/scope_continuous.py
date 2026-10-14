#!/usr/bin/env python3
"""Exact controlled Gaussian likelihood, sensitivity and repeated inference."""
import hashlib
import json
from pathlib import Path
import sys
import time
import numpy as np
from scipy.stats import multivariate_normal
from threadpoolctl import threadpool_limits
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from causalbank.continuous_controlled import likelihood_score,fit,information,value


def generate(n,h,theta,noises,rng):
    f,b,k,c,d=theta;q,ro,ra,rr=noises;x=rng.normal(size=n)
    o=np.empty((n,h));a=np.empty_like(o);r=np.empty_like(o)
    for t in range(h):
        o[:,t]=x+np.sqrt(ro)*rng.normal(size=n);a[:,t]=k*x+np.sqrt(ra)*rng.normal(size=n)
        r[:,t]=c*x+d*a[:,t]+np.sqrt(rr)*rng.normal(size=n)
        x=f*x+b*a[:,t]+np.sqrt(q)*rng.normal(size=n)
    return o,a,r


def exact_joint_covariance(theta,noises,h):
    # Independent construction: express every observed variable as a linear
    # combination of the initial state and all primitive independent noises.
    f,b,k,c,d=theta;q,ro,ra,rr=noises;dimension=1+4*h;x=np.zeros(dimension);x[0]=1;rows=[]
    for t in range(h):
        offset=1+4*t;signal=x.copy();signal[offset]=np.sqrt(ro)
        action=k*x;action[offset+1]=np.sqrt(ra)
        reward=c*x+d*action;reward[offset+2]=np.sqrt(rr)
        rows.extend([signal,action,reward]);x=f*x+b*action;x[offset+3]=np.sqrt(q)
    L=np.array(rows);return L@L.T


def main():
    path=ROOT/'docs/studies/scope-continuous-spec.json';spec=json.loads(path.read_text());theta=np.array(spec['parameter']);noise=spec['noise_variances']
    tiny=generate(4,4,theta,noise,np.random.default_rng(44));ll,score=likelihood_score(theta,tiny,noise)
    stacked=np.stack(tiny,axis=2).reshape(4,-1);direct=multivariate_normal.logpdf(stacked,cov=exact_joint_covariance(theta,noise,4)).sum()
    numerical=[]
    for j in range(5):
        move=np.zeros(5);move[j]=1e-6;numerical.append((likelihood_score(theta+move,tiny,noise)[0]-likelihood_score(theta-move,tiny,noise)[0])/2e-6)
    errors={'joint_gaussian_likelihood':abs(ll-direct),'analytic_score':float(abs(score-numerical).max())}
    assert errors['joint_gaussian_likelihood']<1e-9 and errors['analytic_score']<1e-6,errors
    truth=value(theta,spec['horizon']);rows=[];start=time.perf_counter()
    with threadpool_limits(limits=1):
        for r in range(spec['repetitions']):
            data=generate(spec['trajectories'],spec['horizon'],theta,noise,np.random.default_rng(np.random.SeedSequence([spec['seed'],r])))
            fitted,diag=fit(data,noise);info=information(fitted,data,noise,spec['horizon'])
            omitted,od=fit(data,noise,include_logger=False)
            row={'replication':r,'parameter':fitted.tolist(),'fit':diag,'information':info,'value':value(fitted,spec['horizon']),'omitted_value':value(omitted,spec['horizon']),'omitted_fit':od}
            # BFGS may report precision loss at an otherwise tiny score. Preserve
            # its status; predeclared numerical acceptance uses score < 1e-5.
            row['numerically_usable']=diag['average_score']<1e-5 and info['available']
            rows.append(row)
            if r%40==0:print(json.dumps({'rep':r,'value':row['value'],'truth':truth,'fit':diag}),flush=True)
    summary={'truth':truth,'bias':float(np.mean([r['value']-truth for r in rows])),
        'coverage':float(np.mean([r['numerically_usable'] and abs(r['value']-truth)<=1.95996398454*r['information'].get('se',0) for r in rows])),
        'unusable':sum(not r['numerically_usable'] for r in rows),'optimizer_success_false':sum(not r['fit']['success'] for r in rows),
        'omitted_logger_bias':float(np.mean([r['omitted_value']-truth for r in rows]))}
    files=[path,Path(__file__),ROOT/'src/causalbank/continuous_controlled.py']
    result={'status':'pass','spec':spec,'checks':errors,'summary':summary,'runs':rows,'seconds':time.perf_counter()-start,
      'input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},'scope':spec['scope']}
    (ROOT/'docs/studies/scope-continuous-results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(summary))


if __name__=='__main__':main()
