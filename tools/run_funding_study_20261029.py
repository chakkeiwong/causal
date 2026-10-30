from pathlib import Path
from hashlib import sha256
import json
import time
import numpy as np
from scipy.stats import norm

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/scientific-gap-closure/2026-10-29'

def within(v):return v-v.mean(axis=0)-v.mean(axis=1)[:,None]+v.mean()

def fit(x,y):
    N,T=x.shape;n=N*T;z=norm.ppf(.975)
    rows=[]
    for name,xx,yy,k,base_leverage in [('pooled',x-x.mean(),y-y.mean(),2,1/n),
                   ('within',within(x),within(y),N+T,1/N+1/T-1/n)]:
        denom=np.sum(xx*xx);b=np.sum(xx*yy)/denom;res=yy-b*xx
        scores=xx*res;leverage=base_leverage+xx**2/denom
        iid=np.sum(scores**2/(1-leverage))/denom**2
        variants={'HC2':iid}
        if name=='within':
            scale=(n-1)/(n-k)
            unit=N/(N-1)*scale*np.sum(scores.sum(axis=1)**2)/denom**2
            date=T/(T-1)*scale*np.sum(scores.sum(axis=0)**2)/denom**2
            intersection=n/(n-k)*np.sum(scores**2)/denom**2
            variants.update(institution=unit,two_way=unit+date-intersection)
        for cov,var in variants.items():
            valid=bool(np.isfinite(var) and var>0)
            width=2*z*np.sqrt(var) if valid else None
            rows.append(dict(method=name+'_'+cov,estimate=float(b),variance=float(var),available=valid,
                covered=bool(valid and abs(b-.4)<=width/2),width=float(width) if valid else None))
    return rows

def main():
    start=time.monotonic();path=OUT/'funding-plan.json';plan=json.loads(path.read_text());records=[]
    for si,scenario in enumerate(plan['scenarios']):
        for rep in range(plan['budget']['replications']):
            rng=np.random.default_rng(np.random.SeedSequence([plan['budget']['seed'],si,rep]))
            N,T=60,20;alpha=rng.normal(size=N);x=np.zeros((N,T+1))
            for t in range(1,T+1):x[:,t]=.5*x[:,t-1]+rng.normal(size=N)
            exposure=x[:,:T];y=alpha[:,None]+.2*np.sin(np.arange(1,T+1)/3)+.4*exposure+rng.normal(size=(N,T))
            if scenario=='heterogeneous_common_shocks':y+=rng.normal(size=N)[:,None]*rng.normal(size=T)
            correct=y.copy()
            if scenario=='mislinked_outcomes':y[:5,10:]=correct[np.roll(np.arange(5),-1),10:]
            for row in fit(exposure,y):row.update(scenario=scenario,replication=rep);records.append(row)
            if scenario=='mislinked_outcomes':
                oracle=next(r for r in fit(exposure,correct) if r['method']=='within_institution')
                oracle.update(method='evaluator_correct_mapping',scenario=scenario,replication=rep);records.append(oracle)
            if time.monotonic()-start>60*plan['budget']['cpu_minutes']:raise RuntimeError('Budget exceeded')
        print(json.dumps(dict(scenario=scenario,replications=plan['budget']['replications'])),flush=True)
    summaries=[]
    for scenario in plan['scenarios']:
        for method in sorted({r['method'] for r in records if r['scenario']==scenario}):
            rs=[r for r in records if r['scenario']==scenario and r['method']==method]
            errors=np.array([r['estimate']-.4 for r in rs]);p=sum(r['covered'] for r in rs)/len(rs)
            summaries.append(dict(scenario=scenario,method=method,bias=float(errors.mean()),
                bias_mcse=float(errors.std(ddof=1)/np.sqrt(len(rs))),rmse=float(np.sqrt(np.mean(errors**2))),
                coverage_all_requests=p,coverage_mcse=float(np.sqrt(p*(1-p)/len(rs))),
                unavailable=sum(not r['available'] for r in rs),
                mean_width=float(np.mean([r['width'] for r in rs if r['available']]))))
    out=dict(complete=True,plan_sha256=sha256(path.read_bytes()).hexdigest(),code_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
      replications=900,scenarios=summaries,break_aware_refusals=300,
      refusal_scope='Supplied audit flag detects injected corruption; no learned detection-rate claim',
      target=.4,units='Generated homogeneous slope, not a bank elasticity',seconds=time.monotonic()-start,
      scope='Generated proposal evidence; no FDIC extract or constant-unit bank panel qualification')
    (OUT/'funding-results.json').write_text(json.dumps(out,indent=2)+chr(10))
    (OUT/'funding-replications.json').write_text(json.dumps(records)+chr(10))
    print(json.dumps(out))

if __name__=='__main__':main()
