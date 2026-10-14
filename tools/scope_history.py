#!/usr/bin/env python3
"""Continuous-history, learned-policy and dropout comparison."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import time
import numpy as np
from scipy.special import expit
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.linear_model import LogisticRegression
from threadpoolctl import threadpool_limits
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from causalbank.history_inference import HistoryQuery,evaluate_history


def generate(n,horizon,rng,case='MAR',policy=None,full=False,randomized=False):
    z=rng.uniform(-1,1,n);l=np.clip(rng.normal(size=n),-2.5,2.5)
    previous=np.zeros(n); cumulative=np.zeros(n); lag=l.copy()
    histories=np.empty((n,horizon+1,5));actions=np.empty((n,horizon));rewards=np.empty_like(actions)
    observed=np.empty_like(actions,dtype=bool);alive=np.ones(n,bool)
    for t in range(horizon):
        history=np.column_stack((z,l,lag,previous,cumulative));histories[:,t]=history
        p=(np.full(n,.5) if randomized else expit(-.1+.45*l+.2*z+.3*previous)) if policy is None else policy(history)
        a=rng.binomial(1,p);noise=3*rng.normal(size=n)
        r=8+2*l+.5*z+(2-1.6*l+.4*z-.6*previous)*a+noise
        q=expit(1.7-.3*l-.2*a+.1*z-(.55*noise if case=='MNAR_reward_selection' else 0))
        alive &= rng.random(n)<q
        actions[:,t]=a;rewards[:,t]=r;observed[:,t]=alive if not full else True
        next_l=np.clip(.5*l+.35*a+.15*z+.15*previous+.5*rng.normal(size=n),-2.5,2.5)
        lag=l;l=next_l;previous=a;cumulative=cumulative+a
    histories[:,-1]=np.column_stack((z,l,lag,previous,cumulative))
    risk=np.column_stack((np.ones(n,bool),observed[:,:-1]))
    histories[:,:-1][~risk]=np.nan;histories[:,-1][~observed[:,-1]]=np.nan
    actions[~risk]=np.nan;rewards[~observed]=np.nan
    return {'history':histories,'action':actions,'reward':rewards,'observed':observed}


def learn_policy(spec):
    training=generate(spec['training_trajectories'],spec['horizon'],np.random.default_rng(spec['seed']+1),full=True,randomized=True)
    h=training['history'][:,:-1].reshape(-1,5);a=training['action'].ravel();y=training['reward'].ravel()
    modifier=np.column_stack((np.ones(len(h)),h[:,1],h[:,0],h[:,3]))
    design=np.column_stack((modifier,a[:,None]*modifier))
    coefficient=np.linalg.lstsq(design,y,rcond=None)[0][-4:]
    def learned(history):
        modifier=np.column_stack((np.ones(len(history)),history[:,1],history[:,0],history[:,3]))
        return .2+.5*(modifier@coefficient>.5)
    return [lambda h: np.full(len(h),.2),learned],coefficient


def truth_value(spec,policies):
    # Common random numbers reduce contrast MC error. Fresh seed is independent
    # of the learning and evaluation samples. Policy is held fixed.
    values=[]
    for policy in policies:
        data=generate(spec['truth_trajectories'],spec['horizon'],np.random.default_rng(spec['seed']+2),policy=policy,full=True)
        values.append(data['reward']@ (spec['discount']**np.arange(spec['horizon'])))
    contrast=values[1]-values[0]
    return {'contrast':float(contrast.mean()),'monte_carlo_se':float(contrast.std(ddof=1)/np.sqrt(len(contrast))),
            'values':[float(x.mean()) for x in values]}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--pilot',action='store_true');args=ap.parse_args()
    path=ROOT/'docs/studies/scope-history-spec.json';spec=json.loads(path.read_text());reps=3 if args.pilot else spec['repetitions']
    policies,coef=learn_policy(spec);truth=truth_value(spec,policies);query=HistoryQuery(spec['horizon'],spec['discount'],'independent_randomized_pilot_seed_'+str(spec['seed']+1))
    reg=HistGradientBoostingRegressor(max_iter=70,max_leaf_nodes=7,min_samples_leaf=35,l2_regularization=10,random_state=18)
    clf=LogisticRegression(C=100,max_iter=400);results=[];start=time.perf_counter()
    with threadpool_limits(limits=1):
        for j,case in enumerate(spec['cases']):
            rows=[]
            for rep in range(reps):
                data=generate(spec['trajectories'],spec['horizon'],np.random.default_rng(np.random.SeedSequence([spec['seed'],j,rep])),case)
                row={'repetition':rep}
                for ignore in [False,True]:
                    result=evaluate_history(data,query,policies,reg,clf,seed=33+rep,folds=spec['folds'],ignore_censoring=ignore)
                    result.pop('scores');result.pop('folds');row['ignore_censoring' if ignore else 'joint_score']=result
                rows.append(row)
                if rep%10==0:print(json.dumps({'case':case,'rep':rep,'estimate':row['joint_score']['result']['estimate'],'truth':truth['contrast']}),flush=True)
            summary={}
            for method in ['joint_score','ignore_censoring']:
                estimates=np.array([r[method]['result']['estimate'] for r in rows]);intervals=[r[method]['result']['interval'] for r in rows]
                summary[method]={'bias':float(np.mean(estimates-truth['contrast'])),'rmse':float(np.sqrt(np.mean((estimates-truth['contrast'])**2))),
                    'coverage':float(np.mean([lo<=truth['contrast']<=hi for lo,hi in intervals])),
                    'mean_se':float(np.mean([np.sqrt(r[method]['result']['variance']) for r in rows])),
                    'mean_plugin_bias':float(np.mean([r[method]['plugin_contrast']-truth['contrast'] for r in rows]))}
            results.append({'case':case,'summary':summary,'runs':rows});print(json.dumps({'case':case,'summary':summary}),flush=True)
    files=[path,Path(__file__),ROOT/'src/causalbank/history_inference.py',ROOT/'src/causalbank/causal_workflow.py']
    receipt={'mode':'pilot' if args.pilot else 'final','spec':spec,'policy_coefficients':coef.tolist(),'truth':truth,'results':results,'seconds':time.perf_counter()-start,
        'input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},'scope':spec['scope']}
    (ROOT/'docs/studies'/('scope-history-pilot.json' if args.pilot else 'scope-history-results.json')).write_text(json.dumps(receipt,indent=2)+'\n')


if __name__=='__main__':main()
