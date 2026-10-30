#!/usr/bin/env python3
"""Randomly recover missing histories in the frozen servicing experiment."""
from pathlib import Path
from hashlib import sha256
import argparse
import csv
import json
import time
import numpy as np
from scipy.special import expit, logit
from scipy.stats import norm
from run_servicing_study_20261029 import generate, action

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/twelve-hour-closure/2026-10-29'
SEED = 8301026
RATES = [.05, .10, .25, .50, 1.]

def records(full, audited):
    """Only routine records or deliberately recovered full histories enter."""
    available = full['observed'] | audited[:, None]
    view = {'x': full['x'].copy(), 'observed': full['observed'].copy(),
            'available': available, 'audited': audited.copy()}
    for key in ['L', 'A', 'R', 'p', 'g']:
        view[key] = np.where(available, full[key], np.nan)
    return view

def score(view, policy, q=None, routine_weight=False):
    n = len(view['x']); w = np.ones(n); total = np.zeros(n)
    for t in range(3):
        keep = view['observed'][:, t] if routine_weight else view['available'][:, t]
        w[~keep] = 0.
        ix = np.flatnonzero(keep)
        a, p, l = view['A'][ix, t], view['p'][ix, t], view['L'][ix, t]
        pa = np.where(a == 1, p, 1-p)
        w[ix] *= (a == action(l, policy)) / pa
        if routine_weight:
            w[ix] /= view['g'][ix, t]
            factor = np.ones(len(ix))
        else:
            factor = np.ones(len(ix)) if q is None else np.where(view['observed'][ix, t], 1., 1./q)
        total[ix] += w[ix] * view['R'][ix, t] * factor
    assert np.isfinite(total).all()
    return total

def contributions(full, policy):
    w = np.ones(len(full['x'])); c = []
    for t in range(3):
        a = full['A'][:, t]; p = full['p'][:, t]
        w *= (a == action(full['L'][:, t], policy)) / np.where(a == 1, p, 1-p)
        c.append(w * full['R'][:, t])
    return np.array(c).T

def validate():
    rng = np.random.default_rng(1710816)
    full = generate(73, rng, dict(action_clip=[.2,.8], future_censoring=True))
    obs = full['observed']; q = .25; b = (~obs.all(axis=1)) & (rng.random(73) < q)
    view = records(full, b)
    checks = []
    for policy in [None, .5]:
        c = contributions(full, policy); k = np.sum(c*obs,axis=1); m = np.sum(c*(~obs),axis=1)
        z = score(view, policy, q)
        np.testing.assert_allclose(z, k+b*m/q, rtol=1e-14, atol=1e-13)
        # Enumerate both possible audit outcomes conditional on this entire history.
        np.testing.assert_allclose((1-q)*k+q*(k+m/q), k+m, atol=1e-13)
        np.testing.assert_allclose((1-q)*(k-k-m)**2+q*(k+m/q-k-m)**2, (1/q-1)*m*m, rtol=1e-13,atol=1e-12)
        # Independently mask unavailable entries with extreme values. The estimator must not read them.
        poison = {key: value.copy() for key,value in view.items()}
        for key in ['L','A','R','p','g']: poison[key][~view['available']] = 1e200
        np.testing.assert_array_equal(score(poison,policy,q),z)
        complete = records(full,np.ones(73,dtype=bool))
        np.testing.assert_allclose(score(complete,policy,1.),c.sum(axis=1),atol=1e-13)
        checks.append(dict(policy=policy,conditional_expectation=True,conditional_variance=True,mask_poison=True,full_recovery=True))
    return checks

def reference():
    prior = json.loads((ROOT/'docs/scientific-gap-closure/2026-10-29/policy-uncertainty-results.json').read_text())
    return prior

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--scenario',choices=['routine','future','selective'],required=True)
    ap.add_argument('--out',required=True);ap.add_argument('--reps',type=int,default=500);ap.add_argument('--n',type=int,default=2000)
    args=ap.parse_args();out=ROOT/args.out;out.mkdir(parents=True,exist_ok=False)
    start=time.monotonic();checks=validate()
    si=['routine','future','selective'].index(args.scenario)
    rows=[];variance=[];zcrit=norm.ppf(.975)
    # Read exact existing intervention references; do not silently improve truth after evaluation.
    refs={r['policy']:r for r in reference()['reference']}
    zero=refs['always_zero']; target=refs['threshold_0.5']
    truth={'never':zero['value'],'threshold':target['value'],'gain':target['improvement']}
    truth_se={'never':zero['mcse'],'threshold':target['mcse'],'gain':target['difference_mcse']}
    plan=dict(scenario=args.scenario,n=args.n,reps=args.reps,seed=SEED,threshold=.5,rates=RATES,
              code_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
              generator_sha256=sha256((ROOT/'tools/run_servicing_study_20261029.py').read_bytes()).hexdigest(),
              reference_path='docs/scientific-gap-closure/2026-10-29/policy-uncertainty-results.json',
              reference_sha256=sha256((ROOT/'docs/scientific-gap-closure/2026-10-29/policy-uncertainty-results.json').read_bytes()).hexdigest(),
              truth=truth,truth_mcse=truth_se,interval='normal pointwise; empirical evaluation only',
              scope='fixed policies, known action probabilities, generated independent customers; no bank claim')
    (out/'registration.json').write_text(json.dumps(plan,indent=2)+'\n')
    (out/'validation.json').write_text(json.dumps(checks,indent=2)+'\n')
    for rep in range(args.reps):
        rng=np.random.default_rng(np.random.SeedSequence([SEED,si,rep]))
        d=generate(args.n,rng,dict(action_clip=[.2,.8],future_censoring=args.scenario!='routine'))
        obs=d['observed'];incomplete=~obs.all(axis=1);u=rng.random(args.n)
        complete=records(d,np.ones(args.n,dtype=bool));routine=records(d,np.zeros(args.n,dtype=bool))
        methods=[('full_history',None,np.zeros(args.n,dtype=bool),[score(complete,p) for p in [None,.5]]),
                 ('routine_g',None,np.zeros(args.n,dtype=bool),[score(routine,p,routine_weight=True) for p in [None,.5]])]
        if args.scenario!='selective':
            for q in RATES:
                b=incomplete & (u<q);view=records(d,b)
                methods.append((f'audit_{q:g}',q,b,[score(view,p,q) for p in [None,.5]]))
        else:
            # Deliberate violation: completion depends on the unseen first-missed innovation.
            first=np.argmin(obs,axis=1);ix=np.arange(args.n)
            eps=d['N'][ix,first]-.6*d['L'][ix,first]-.25*d['x']+.5*d['A'][ix,first]
            actual=expit(logit(.25)+.8*eps);b=incomplete & (u<actual);view=records(d,b)
            methods.append(('selective_nominal_0.25',.25,b,[score(view,p,.25) for p in [None,.5]]))
        for name,q,b,sc in methods:
            for target,s in [('never',sc[0]),('threshold',sc[1]),('gain',sc[1]-sc[0])]:
                estimate=float(s.mean());se=float(s.std(ddof=1)/np.sqrt(args.n));lo=estimate-zcrit*se;hi=estimate+zcrit*se
                rows.append(dict(rep=rep,method=name,target=target,estimate=estimate,se=se,lo=lo,hi=hi,
                  covered=lo<=truth[target]<=hi,positive_lower=lo>0,audits=int(b.sum()),
                  incomplete=int(incomplete.sum()),recovered_rewards=int(np.sum(b[:,None]&~obs)),
                  ambiguous_reference=abs(lo-truth[target])<=zcrit*truth_se[target] or abs(hi-truth[target])<=zcrit*truth_se[target]))
        c0=contributions(d,None);c1=contributions(d,.5)
        for target,c in [('never',c0),('threshold',c1),('gain',c1-c0)]:
            h=c.sum(axis=1);m=np.sum(c*~obs,axis=1)
            variance.append(dict(rep=rep,target=target,var_h=float(h.var(ddof=1)),missing_second_moment=float(np.mean(m*m)),incomplete_rate=float(incomplete.mean())))
        if (rep+1)%100==0: print(json.dumps(dict(scenario=args.scenario,completed=rep+1,seconds=round(time.monotonic()-start,2))),flush=True)
        if time.monotonic()-start>900: raise RuntimeError('15-minute per-batch budget exhausted')
    with (out/'replications.csv').open('w',newline='') as f:
        wr=csv.DictWriter(f,fieldnames=rows[0]);wr.writeheader();wr.writerows(rows)
    with (out/'variance-components.csv').open('w',newline='') as f:
        wr=csv.DictWriter(f,fieldnames=variance[0]);wr.writeheader();wr.writerows(variance)
    summaries=[]
    for name in dict.fromkeys(r['method'] for r in rows):
        for target in truth:
            a=[r for r in rows if r['method']==name and r['target']==target]
            estimates=np.array([r['estimate'] for r in a]);errors=estimates-truth[target];coverage=np.mean([r['covered'] for r in a])
            summaries.append(dict(method=name,target=target,bias=float(errors.mean()),bias_mcse=float(errors.std(ddof=1)/np.sqrt(args.reps)),
              rmse=float(np.sqrt(np.mean(errors*errors))),coverage=float(coverage),coverage_mcse=float(np.sqrt(coverage*(1-coverage)/args.reps)),
              mean_width=float(np.mean([r['hi']-r['lo'] for r in a])),positive_lower_rate=float(np.mean([r['positive_lower'] for r in a])),
              mean_audits=float(np.mean([r['audits'] for r in a])),mean_incomplete=float(np.mean([r['incomplete'] for r in a])),
              mean_recovered_rewards=float(np.mean([r['recovered_rewards'] for r in a])),ambiguous_reference_boundaries=int(sum(r['ambiguous_reference'] for r in a)),
              empirical_estimator_variance=float(estimates.var(ddof=1)),mean_estimated_variance=float(np.mean([r['se']**2 for r in a]))))
    result=dict(registration=plan,complete=True,seconds=time.monotonic()-start,summaries=summaries,
                warning='Coverage against a numerical reference; normal intervals have no exact finite-sample guarantee. Selective-completion scenario intentionally violates audit independence.')
    (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(complete=True,path=str(out),seconds=result['seconds'])),flush=True)

if __name__=='__main__':main()
