#!/usr/bin/env python3
"""Equal realized information budget: weighting, pilot splits and cross-fitting."""
from pathlib import Path
from hashlib import sha256
import argparse,csv,json,time
import numpy as np
from scipy.stats import norm
from run_servicing_study_20261029 import generate
from run_outcome_audit_study_20261030 import score,reference
from run_outcome_audit_precision_20261030 import view,fit,augmented,validate

ROOT=Path(__file__).resolve().parents[1]
SEED=10301026

def subset(v,indices):return {k:a[indices].copy() for k,a in v.items()}

def evaluate(train,evaluation):
    fits=[fit(train,p,.25)[0] for p in [None,.5]]
    return [augmented(evaluation,p,c,.25)[0] for p,c in zip([None,.5],fits)]

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--scenario',choices=['routine','future'],required=True);ap.add_argument('--out',required=True)
    args=ap.parse_args();out=ROOT/args.out;out.mkdir(parents=True,exist_ok=False);start=time.monotonic();checks=validate()
    refs={r['policy']:r for r in reference()['reference']};r0=refs['always_zero'];r1=refs['threshold_0.5']
    truth=dict(never=r0['value'],threshold=r1['value'],gain=r1['improvement'])
    truth_se=dict(never=r0['mcse'],threshold=r1['mcse'],gain=r1['difference_mcse'])
    plan=dict(scenario=args.scenario,reps=500,total_n=7000,recovery_q=.25,seed=SEED,pilot_splits=[5000,2000,1000],cross_fit_folds=2,
      truth=truth,truth_mcse=truth_se,code_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
      dependency_hashes={n:sha256((ROOT/'tools'/n).read_bytes()).hexdigest() for n in ['run_servicing_study_20261029.py','run_outcome_audit_study_20261030.py','run_outcome_audit_precision_20261030.py']},
      scope='Same7000 initial records and exact same realized recovery histories for every method;fixed policies;normal intervals evaluated empirically.')
    (out/'registration.json').write_text(json.dumps(plan,indent=2)+chr(10));(out/'validation.json').write_text(json.dumps(checks,indent=2)+chr(10))
    rows=[];si=['routine','future'].index(args.scenario);z=norm.ppf(.975)
    for rep in range(500):
        rng=np.random.default_rng(np.random.SeedSequence([SEED,si,rep]));d=generate(7000,rng,dict(action_clip=[.2,.8],future_censoring=args.scenario=='future'))
        b=(~d['observed'].all(axis=1))&(rng.random(7000)<.25);v=view(d,b)
        methods=[('weighting_7000',7000,[score(v,p,.25) for p in [None,.5]])]
        for train_n in [5000,2000,1000]:
            train=subset(v,slice(0,train_n));ev=subset(v,slice(train_n,None));s=evaluate(train,ev)
            methods.append((f'pilot_{train_n}',7000-train_n,s))
        left=subset(v,slice(0,3500));right=subset(v,slice(3500,None))
        sleft=evaluate(right,left);sright=evaluate(left,right)
        methods.append(('cross_fit_two_folds',7000,[np.concatenate([l,r]) for l,r in zip(sleft,sright)]))
        for name,n,sc in methods:
            for target,s in [('never',sc[0]),('threshold',sc[1]),('gain',sc[1]-sc[0])]:
                est=float(s.mean());se=float(s.std(ddof=1)/np.sqrt(n));lo=est-z*se;hi=est+z*se
                rows.append(dict(rep=rep,method=name,target=target,n_scored=n,initial_records=7000,recovered_histories=int(b.sum()),
                  recovered_rewards=int(np.sum(b[:,None]&~d['observed'])),estimate=est,se=se,lo=lo,hi=hi,
                  covered=bool(lo<=truth[target]<=hi),positive_lower=bool(lo>0),
                  ambiguous_reference=bool(abs(lo-truth[target])<=z*truth_se[target] or abs(hi-truth[target])<=z*truth_se[target])))
        if (rep+1)%100==0:print(json.dumps(dict(scenario=args.scenario,completed=rep+1,seconds=round(time.monotonic()-start,2))),flush=True)
        if time.monotonic()-start>1200:raise RuntimeError('20-minute study budget exhausted')
    with (out/'replications.csv').open('w',newline='') as f:
        wr=csv.DictWriter(f,fieldnames=rows[0]);wr.writeheader();wr.writerows(rows)
    summaries=[];paired=[]
    for method in dict.fromkeys(r['method'] for r in rows):
        for target in truth:
            a=[r for r in rows if r['method']==method and r['target']==target];est=np.array([r['estimate'] for r in a]);err=est-truth[target];cov=float(np.mean([r['covered'] for r in a]))
            summaries.append(dict(method=method,target=target,bias=float(err.mean()),bias_mcse=float(err.std(ddof=1)/np.sqrt(500)),rmse=float(np.sqrt(np.mean(err**2))),
              coverage=cov,coverage_mcse=float(np.sqrt(cov*(1-cov)/500)),mean_width=float(np.mean([r['hi']-r['lo'] for r in a])),
              positive_lower_rate=float(np.mean([r['positive_lower'] for r in a])),mean_recovered_histories=float(np.mean([r['recovered_histories'] for r in a])),
              mean_recovered_rewards=float(np.mean([r['recovered_rewards'] for r in a])),empirical_estimator_variance=float(est.var(ddof=1)),
              mean_estimated_variance=float(np.mean([r['se']**2 for r in a])),ambiguous_reference_boundaries=int(sum(r['ambiguous_reference']for r in a))))
            base=[r for r in rows if r['method']=='weighting_7000'and r['target']==target]
            diff=np.array([(x['hi']-x['lo'])-(y['hi']-y['lo'])for x,y in zip(a,base)])
            assert all(x['recovered_histories']==y['recovered_histories'] and x['initial_records']==y['initial_records'] for x,y in zip(a,base))
            paired.append(dict(method=method,target=target,mean_width_difference=float(diff.mean()),width_difference_mcse=float(diff.std(ddof=1)/np.sqrt(500)),exact_resource_equality=True))
    result=dict(complete=True,registration=plan,seconds=time.monotonic()-start,summaries=summaries,paired_vs_weighting=paired,
      limits='Pooled-score standard error for cross-fitting is a tested candidate,not proved general finite-sample validity;500replications cannot establish uniform coverage. Initial and recovery costs equal by construction,computation not priced.')
    (out/'result.json').write_text(json.dumps(result,indent=2)+chr(10));print(json.dumps(dict(complete=True,path=str(out),seconds=result['seconds'])),flush=True)

if __name__=='__main__':main()
