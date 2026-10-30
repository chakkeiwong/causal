#!/usr/bin/env python3
"""Independent-pilot augmentation of randomized recovery of missing histories."""
from pathlib import Path
from hashlib import sha256
import argparse, csv, json, time
import numpy as np
from scipy.stats import norm
from run_servicing_study_20261029 import generate, action
from run_outcome_audit_study_20261030 import records, score, reference

ROOT=Path(__file__).resolve().parents[1]
SEED=9301026
RATES=[.05,.10,.25,.50,1.]

def view(full,audited):
    v=records(full,audited)
    v['N']=np.where(v['available'],full['N'],np.nan)
    v['initial_l']=full['L'][:,0].copy()
    return v

def basis(l,x,a,constant=False):
    if constant:return np.ones((len(l),1))
    return np.column_stack([np.ones(len(l)),l,x,a,l*l,x*x,l*x,a*l,a*x])

def predict(coef,l,x,a,constant=False):
    return basis(l,x,a,constant)@coef

def fit(v,policy,q,constant=False):
    coefs=[None]*3;diagnostics=[]
    for t in range(2,-1,-1):
        ix=np.flatnonzero(v['available'][:,t]);l=v['L'][ix,t];x=v['x'][ix];a=v['A'][ix,t]
        y=v['R'][ix,t].copy()
        if t<2:
            nxt=v['N'][ix,t];y+=predict(coefs[t+1],nxt,x,action(nxt,policy),constant)
        w=np.where(v['observed'][ix,t],1.,1/q)
        z=basis(l,x,a,constant);zw=z*np.sqrt(w)[:,None];yw=y*np.sqrt(w)
        coef,_,rank,singular=np.linalg.lstsq(zw,yw,rcond=None)
        if rank!=z.shape[1]:raise ValueError('Pilot regression lacks full rank')
        coefs[t]=coef;diagnostics.append(dict(t=t,n=len(ix),rank=int(rank),condition=float(singular[0]/singular[-1])))
    return coefs,diagnostics

def augmented(v,policy,coefs,q=None,routine_weight=False,constant=False):
    n=len(v['x']);w=np.ones(n)
    base=predict(coefs[0],v['initial_l'],v['x'],action(v['initial_l'],policy),constant)
    total=base.copy();contrib=np.zeros((n,3))
    for t in range(3):
        keep=v['observed'][:,t] if routine_weight else v['available'][:,t]
        w[~keep]=0.;ix=np.flatnonzero(keep)
        l=v['L'][ix,t];a=v['A'][ix,t];x=v['x'][ix];p=v['p'][ix,t]
        w[ix]*=(a==action(l,policy))/np.where(a==1,p,1-p)
        residual=v['R'][ix,t]-predict(coefs[t],l,x,a,constant)
        if t<2:
            nxt=v['N'][ix,t];residual+=predict(coefs[t+1],nxt,x,action(nxt,policy),constant)
        if routine_weight:
            w[ix]/=v['g'][ix,t];factor=np.ones(len(ix))
        else:factor=np.ones(len(ix)) if q is None else np.where(v['observed'][ix,t],1.,1/q)
        contrib[ix,t]=w[ix]*residual*factor;total[ix]+=contrib[ix,t]
    assert np.isfinite(total).all()
    return total,base,contrib

def validate():
    rng=np.random.default_rng(2902167);d=generate(401,rng,dict(action_clip=[.2,.8],future_censoring=True))
    b=(~d['observed'].all(axis=1))&(rng.random(401)<.25);v=view(d,b);full=view(d,np.ones(401,dtype=bool))
    checks=[]
    for policy in [None,.5]:
        zero=[np.zeros(9)]*3
        np.testing.assert_allclose(augmented(v,policy,zero,.25)[0],score(v,policy,.25),atol=1e-12)
        coefs=[rng.normal(size=9) for _ in range(3)]
        h,baseline,c=augmented(full,policy,coefs);m=np.sum(c*~d['observed'],axis=1);k=h-m
        actual=augmented(v,policy,coefs,.25)[0]
        np.testing.assert_allclose(actual,k+b*m/.25,atol=1e-11)
        np.testing.assert_allclose(augmented(full,policy,coefs,1.)[0],h,atol=1e-12)
        poison={key:value.copy() for key,value in v.items()}
        for key in ['L','A','R','p','g','N']:poison[key][~v['available']]=1e200
        np.testing.assert_array_equal(augmented(poison,policy,coefs,.25)[0],actual)
        f1,_=fit(v,policy,.25);f2,_=fit(poison,policy,.25)
        for c1,c2 in zip(f1,f2):np.testing.assert_array_equal(c1,c2)
        for i in [0,200,400]:
            scalar=baseline[i];weight=1.
            for t in range(3):
                a=d['A'][i,t];p=d['p'][i,t];l=d['L'][i,t];x=d['x'][i]
                weight*=int(a==int(policy is not None and l>policy))/(p if a else 1-p)
                rr=d['R'][i,t]-float(predict(coefs[t],np.array([l]),np.array([x]),np.array([a]))[0])
                if t<2:
                    nxt=d['N'][i,t];aa=int(policy is not None and nxt>policy)
                    rr+=float(predict(coefs[t+1],np.array([nxt]),np.array([x]),np.array([aa]))[0])
                scalar+=weight*rr
            np.testing.assert_allclose(scalar,h[i],atol=1e-11)
        checks.append(dict(policy=policy,zero_q_reduction=True,independent_scalar=True,conditional_recovery=True,mask_poison_fit_and_score=True))
    return checks

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--scenario',choices=['routine','future'],required=True);ap.add_argument('--out',required=True)
    ap.add_argument('--reps',type=int,default=500);args=ap.parse_args()
    out=ROOT/args.out;out.mkdir(parents=True,exist_ok=False);start=time.monotonic();checks=validate()
    refs={r['policy']:r for r in reference()['reference']};r0=refs['always_zero'];r1=refs['threshold_0.5']
    truth=dict(never=r0['value'],threshold=r1['value'],gain=r1['improvement'])
    truth_se=dict(never=r0['mcse'],threshold=r1['mcse'],gain=r1['difference_mcse'])
    plan=dict(scenario=args.scenario,reps=args.reps,pilot_n=5000,evaluation_n=2000,pilot_q=.25,seed=SEED,
      reference=truth,reference_mcse=truth_se,rates=RATES,threshold=.5,
      code_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
      dependencies={name:sha256((ROOT/'tools'/name).read_bytes()).hexdigest() for name in ['run_outcome_audit_study_20261030.py','run_servicing_study_20261029.py']},
      scope='Fixed policies, independent pilot, known action and random follow-up probabilities; conditional simulation evidence')
    (out/'registration.json').write_text(json.dumps(plan,indent=2)+chr(10))
    (out/'validation.json').write_text(json.dumps(checks,indent=2)+chr(10))
    rows=[];components=[];si=['routine','future'].index(args.scenario);z=norm.ppf(.975)
    for rep in range(args.reps):
        rng=np.random.default_rng(np.random.SeedSequence([SEED,si,rep]));law=dict(action_clip=[.2,.8],future_censoring=args.scenario=='future')
        pilot=generate(5000,rng,law);pb=(~pilot['observed'].all(axis=1))&(rng.random(5000)<.25);pv=view(pilot,pb)
        fits=[fit(pv,p,.25)[0] for p in [None,.5]];constants=[fit(pv,p,.25,True)[0] for p in [None,.5]]
        d=generate(2000,rng,law);obs=d['observed'];incomplete=~obs.all(axis=1);u=rng.random(2000)
        fv=view(d,np.ones(2000,dtype=bool));rv=view(d,np.zeros(2000,dtype=bool))
        full_results=[augmented(fv,p,c) for p,c in zip([None,.5],fits)]
        methods=[('augmented_full',np.zeros(2000,dtype=bool),[r[0] for r in full_results]),
          ('augmented_routine_g',np.zeros(2000,dtype=bool),[augmented(rv,p,c,routine_weight=True)[0] for p,c in zip([None,.5],fits)])]
        for q in RATES:
            b=incomplete&(u<q);v=view(d,b)
            methods.append((f'augmented_audit_{q:g}',b,[augmented(v,p,c,q)[0] for p,c in zip([None,.5],fits)]))
            if q==.25:
                methods.append(('constant_audit_0.25',b,[augmented(v,p,c,q,constant=True)[0] for p,c in zip([None,.5],constants)]))
                methods.append(('unaugmented_audit_0.25',b,[score(v,p,q) for p in [None,.5]]))
        for name,b,sc in methods:
            for target,s in [('never',sc[0]),('threshold',sc[1]),('gain',sc[1]-sc[0])]:
                estimate=float(s.mean());se=float(s.std(ddof=1)/np.sqrt(2000));lo=estimate-z*se;hi=estimate+z*se
                rows.append(dict(rep=rep,method=name,target=target,estimate=estimate,se=se,lo=lo,hi=hi,covered=bool(lo<=truth[target]<=hi),
                  positive_lower=bool(lo>0),evaluation_audits=int(b.sum()),pilot_audits=int(pb.sum()),
                  recovered_rewards=int(np.sum(b[:,None]&~obs)),
                  ambiguous_reference=bool(abs(lo-truth[target])<=z*truth_se[target] or abs(hi-truth[target])<=z*truth_se[target])))
        for target,h,c in [('never',full_results[0][0],full_results[0][2]),('threshold',full_results[1][0],full_results[1][2]),
                          ('gain',full_results[1][0]-full_results[0][0],full_results[1][2]-full_results[0][2])]:
            m=np.sum(c*~obs,axis=1)
            components.append(dict(rep=rep,target=target,var_h=float(h.var(ddof=1)),missing_second_moment=float(np.mean(m*m))))
        if (rep+1)%100==0:print(json.dumps(dict(scenario=args.scenario,completed=rep+1,seconds=round(time.monotonic()-start,2))),flush=True)
        if time.monotonic()-start>1200:raise RuntimeError('20-minute per-scenario budget exhausted')
    for name,data in [('replications.csv',rows),('variance-components.csv',components)]:
        with (out/name).open('w',newline='') as f:
            wr=csv.DictWriter(f,fieldnames=data[0]);wr.writeheader();wr.writerows(data)
    summaries=[]
    for name in dict.fromkeys(r['method'] for r in rows):
        for target in truth:
            a=[r for r in rows if r['method']==name and r['target']==target];est=np.array([r['estimate'] for r in a]);err=est-truth[target]
            coverage=float(np.mean([r['covered'] for r in a]))
            summaries.append(dict(method=name,target=target,bias=float(err.mean()),bias_mcse=float(err.std(ddof=1)/np.sqrt(args.reps)),
              rmse=float(np.sqrt(np.mean(err**2))),coverage=coverage,coverage_mcse=float(np.sqrt(coverage*(1-coverage)/args.reps)),
              mean_width=float(np.mean([r['hi']-r['lo'] for r in a])),positive_lower_rate=float(np.mean([r['positive_lower'] for r in a])),
              mean_evaluation_audits=float(np.mean([r['evaluation_audits'] for r in a])),mean_pilot_audits=float(np.mean([r['pilot_audits'] for r in a])),
              mean_recovered_rewards=float(np.mean([r['recovered_rewards'] for r in a])),ambiguous_reference_boundaries=int(sum(r['ambiguous_reference'] for r in a)),
              empirical_estimator_variance=float(est.var(ddof=1)),mean_estimated_variance=float(np.mean([r['se']**2 for r in a]))))
    result=dict(complete=True,registration=plan,summaries=summaries,seconds=time.monotonic()-start,
      warning='Independent-pilot conditional inference; pointwise normal intervals only; no exact coverage, unknown-policy or bank qualification.')
    (out/'result.json').write_text(json.dumps(result,indent=2)+chr(10))
    print(json.dumps(dict(complete=True,path=str(out),seconds=result['seconds'])),flush=True)

if __name__=='__main__':main()
