"""Generated linkage sensitivity; truth is held outside the analysis functions."""
from pathlib import Path
from hashlib import sha256
import json
import time
from collections import Counter, defaultdict
import numpy as np

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'docs/scientific-gap-closure/2026-10-29'

def generate(rng,rate,scenario,n=1000):
    names=[''.join(rng.choice(list('abcdefghijklmnopqrstuvwxyz'),6)) for _ in range(200)]
    x=rng.uniform(-1,1,n);a=rng.binomial(1,.5,n)
    y=100+30*a+10*x+20*rng.uniform(-1,1,n)
    key=[(names[j],int(d)) for j,d in zip(rng.integers(200,size=n),rng.integers(365,size=n))]
    left=[dict(row_id='L'+str(j),name=k[0],day=k[1],A=int(aa),X=float(xx))
          for j,k,aa,xx in zip(rng.permutation(np.arange(n)*19+1),key,a,x)]
    right=[dict(name=k[0],day=k[1],Y=float(yy)) for k,yy in zip(key,y)]
    owners=list(range(n));K=round(n*rate)
    weights=np.ones(n) if scenario=='independent' else (1+.8*x if scenario=='covariate_dependent' else .2+1.6*(y-70)/90)
    chosen=rng.choice(n,K,replace=False,p=weights/weights.sum())
    for c,j in enumerate(chosen):
        if c%4==0:right[j]['name']=''
        elif c%4==1:
            old=right[j]['name'];p=int(rng.integers(6));letter=chr(97+(ord(old[p])-97+1)%26)
            right[j]['name']=old[:p]+letter+old[p+1:]
        elif c%4==2:
            other=(j+int(rng.integers(1,n)))%n
            right[j]['name'],right[j]['day']=key[other]
        else:
            right.append(dict(name=key[j][0],day=key[j][1],Y=float(rng.uniform(70,160))))
            owners.append(-1)
    for row,rid in zip(right,rng.permutation(np.arange(len(right))*23+3)):row['row_id']='R'+str(rid)
    permutation=rng.permutation(len(right));right=[right[j] for j in permutation];owners=np.array(owners)[permutation]
    truth=dict(outcomes=y,owners=owners,exclusion_budget=K)
    return left,right,truth

def candidates(left,right,fuzzy):
    dates=defaultdict(list)
    for j,row in enumerate(right):dates[row['day']].append(j)
    out=[]
    for row in left:
        keep=[]
        for j in dates[row['day']]:
            name=right[j]['name']
            if name==row['name'] or (fuzzy and (name=='' or sum(a!=b for a,b in zip(name,row['name']))<=1)):
                keep.append(j)
        out.append(keep)
    return out

def matched(left,right,sets):
    proposed=[s[0] if len(s)==1 else None for s in sets];counts=Counter(proposed)
    links=[j if j is not None and counts[j]==1 else None for j in proposed]
    a=np.array([r['A'] for r in left]);keep=np.array([j is not None for j in links]);y=np.array([right[j]['Y'] if j is not None else np.nan for j in links])
    groups=[y[keep & (a==g)] for g in [0,1]]
    if min(map(len,groups))<2:return dict(estimate=None,covered=False,width=None,available=False,matched=int(keep.sum())),links
    estimate=float(groups[1].mean()-groups[0].mean());se=np.sqrt(sum(v.var(ddof=1)/len(v) for v in groups))
    return dict(estimate=estimate,covered=bool(abs(estimate-30)<=1.95996398454*se),width=float(2*1.95996398454*se),available=True,matched=int(keep.sum())),links

def bounds(left,right,sets,K):
    a=np.array([r['A'] for r in left]);n1=a.sum();n0=len(a)-n1;w=np.where(a==1,1/n1,-1/n0)
    lows=np.array([min(right[j]['Y'] for j in s) if s else 70 for s in sets])
    highs=np.array([max(right[j]['Y'] for j in s) if s else 160 for s in sets])
    low=np.minimum(w*lows,w*highs);high=np.maximum(w*lows,w*highs)
    global_low=np.minimum(w*70,w*160);global_high=np.maximum(w*70,w*160)
    lo=float(low.sum()-np.sort(low-global_low)[-K:].sum()) if K else float(low.sum())
    hi=float(high.sum()+np.sort(global_high-high)[-K:].sum()) if K else float(high.sum())
    sampling=90*(np.sqrt(np.log(80)/(2*n1))+np.sqrt(np.log(80)/(2*n0)))
    return [max(-90,lo),min(90,hi)],float(sampling)

def main():
    start=time.monotonic();planfile=OUT/'observation-plan.json';plan=json.loads(planfile.read_text());records=[];inclusions=[]
    for si,scenario in enumerate(plan['scenarios']):
        for ri,rate in enumerate(plan['rates']):
            for rep in range(plan['budget']['replications_per_scenario_rate']):
                rng=np.random.default_rng(np.random.SeedSequence([plan['budget']['seed'],si,ri,rep]))
                left,right,truth=generate(rng,rate,scenario);a=np.array([r['A'] for r in left]);y=truth['outcomes']
                full=float(y[a==1].mean()-y[a==0].mean());se=np.sqrt(y[a==1].var(ddof=1)/sum(a==1)+y[a==0].var(ddof=1)/sum(a==0))
                rows=[dict(method='evaluator_truth',estimate=full,covered=bool(abs(full-30)<=1.95996398454*se),width=float(2*1.95996398454*se),available=True,matched=1000,wrong=0)]
                fuzzy=candidates(left,right,True)
                inclusion=np.array([any(truth['owners'][j]==i for j in s) for i,s in enumerate(fuzzy)])
                assert (~inclusion).sum()<=truth['exclusion_budget']
                inclusions.append(dict(scenario=scenario,rate=rate,replication=rep,inclusion=float(inclusion.mean())))
                for method,sets in [('exact',candidates(left,right,False)),('fuzzy',fuzzy)]:
                    row,links=matched(left,right,sets);row.update(method=method,wrong=sum(j is not None and truth['owners'][j]!=i for i,j in enumerate(links)));rows.append(row)
                for method,K in [('conditional_candidates',0),('corruption_aware',truth['exclusion_budget'])]:
                    interval,sampling=bounds(left,right,fuzzy,K)
                    enclosed=bool(interval[0]-1e-10<=full<=interval[1]+1e-10)
                    if method=='corruption_aware':assert enclosed,'Known-budget bound failed'
                    rows.append(dict(method=method,estimate=None,available=True,covered=bool(interval[0]-sampling<=30<=interval[1]+sampling),
                        width=float(interval[1]-interval[0]+2*sampling),realised_contrast_enclosed=enclosed,raw_width=interval[1]-interval[0],matched=None,wrong=None))
                for row in rows:row.update(scenario=scenario,rate=rate,replication=rep);records.append(row)
                if rep==0:
                    folder=OUT/'observation-samples'/f'{scenario}-{rate}';(folder/'analysis').mkdir(parents=True,exist_ok=True);(folder/'evaluator').mkdir(exist_ok=True)
                    (folder/'analysis'/'tables.json').write_text(json.dumps(dict(left=left,right=right)))
                    (folder/'evaluator'/'truth.json').write_text(json.dumps(dict(outcomes=y.tolist(),owners=truth['owners'].tolist(),exclusion_budget=truth['exclusion_budget'])))
                if time.monotonic()-start>60*plan['budget']['cpu_minutes']:raise RuntimeError('Budget exceeded')
            print(json.dumps(dict(scenario=scenario,rate=rate,replications=rep+1)),flush=True)
    summaries=[]
    for scenario in plan['scenarios']:
        for rate in plan['rates']:
            for method in ['evaluator_truth','exact','fuzzy','conditional_candidates','corruption_aware']:
                rs=[r for r in records if r['scenario']==scenario and r['rate']==rate and r['method']==method];p=sum(r['covered'] for r in rs)/len(rs)
                estimates=np.array([r['estimate'] for r in rs if r['estimate'] is not None]);widths=[r['width'] for r in rs if r['width'] is not None]
                summaries.append(dict(scenario=scenario,rate=rate,method=method,replications=len(rs),coverage_all_requests=p,
                    coverage_mcse=float(np.sqrt(p*(1-p)/len(rs))),mean_width=float(np.mean(widths)),unavailable=sum(not r['available'] for r in rs),
                    bias=float(estimates.mean()-30) if len(estimates) else None,bias_mcse=float(estimates.std(ddof=1)/np.sqrt(len(estimates))) if len(estimates) else None,
                    matched_fraction=float(np.mean([r['matched']/1000 for r in rs])) if rs[0]['matched'] is not None else None,
                    wrong_per_entity=float(np.mean([r['wrong']/1000 for r in rs])) if rs[0]['wrong'] is not None else None,
                    realised_enclosure=float(np.mean([r['realised_contrast_enclosed'] for r in rs])) if 'realised_contrast_enclosed' in rs[0] else None))
    result=dict(complete=True,replications=1800,scenarios=summaries,seconds=time.monotonic()-start,
        plan_sha256=sha256(planfile.read_bytes()).hexdigest(),code_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
        limits=plan['not_concluded'],truth_in_analysis_exports=False)
    for name,obj in [('observation-results.json',result),('observation-replications.json',records),('observation-inclusion.json',inclusions)]:
        (OUT/name).write_text(json.dumps(obj,indent=2 if name=='observation-results.json' else None)+'\n')
    print(json.dumps(dict(complete=True,replications=1800,seconds=result['seconds'])))

if __name__=='__main__':main()
