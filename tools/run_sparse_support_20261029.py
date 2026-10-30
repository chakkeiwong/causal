"""Compare prespecified small-cell intervals in generated normal populations."""
from hashlib import sha256
import json
from pathlib import Path
import time
import numpy as np
from scipy.stats import t as student

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/scientific-synthesis/2026-10-29'


def proportion(x):
    p=float(np.mean(x));n=len(x)
    return {'value':p,'mcse':float(np.sqrt(p*(1-p)/n)),'denominator':n}


def main():
    start=time.monotonic();raw=(OUT/'uncertainty-plan.json').read_bytes();plan=json.loads(raw)
    seeds=np.random.SeedSequence(plan['seed']).spawn(2);allresults=[]
    for seed,(name,sd) in zip(seeds,plan['noise_laws'].items()):
        rng=np.random.default_rng(seed);result={k:[] for k in ['wald','pooled_t','bonferroni_t']};failures=0
        for _ in range(3000):
            s=rng.integers(0,2,500);e=np.where(s==0,.5,.02);a=rng.binomial(1,e)
            cells=2*s+a;y=50*s+100*s*a+rng.normal(size=500)*np.array(sd)[cells]
            groups=[y[cells==i] for i in range(4)];ns=np.array([len(g) for g in groups])
            if min(ns)<2:failures+=1;continue
            means=np.array([g.mean() for g in groups]);var=np.array([g.var(ddof=1) for g in groups])
            estimate=np.dot([-.5,.5,-.5,.5],means)
            wald=1.959963984540054*np.sqrt(np.sum(.25*var/ns))
            pooled_variance=np.sum((ns-1)*var)/(ns.sum()-4)
            pooled=student.ppf(.975,ns.sum()-4)*np.sqrt(pooled_variance*np.sum(.25/ns))
            conservative=np.sum(.5*student.ppf(1-.05/8,ns-1)*np.sqrt(var/ns))
            for k,half in [('wald',wald),('pooled_t',pooled),('bonferroni_t',conservative)]:
                result[k].append((estimate-half<=50<=estimate+half,2*half,estimate-half>40))
        summaries={}
        for k,rows in result.items():
            x=np.array(rows);summaries[k]={'conditional_coverage':proportion(x[:,0]),
              'unconditional_coverage':float(x[:,0].sum()/3000),'mean_width':float(x[:,1].mean()),
              'median_width':float(np.median(x[:,1])),'recommend_offer':proportion(x[:,2])}
        allresults.append({'noise_law':name,'sd':sd,'replications':3000,'unavailable':failures,'methods':summaries})
    output={'plan_sha256':sha256(raw).hexdigest(),'code_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
            'results':allresults,'seconds':round(time.monotonic()-start,3),'kind':'constructed Gaussian populations only'}
    (OUT/'uncertainty-results.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))


if __name__=='__main__':main()
