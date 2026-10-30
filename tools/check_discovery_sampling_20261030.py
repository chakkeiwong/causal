"""Audit retained simulation accounting and regenerate only selected arithmetic witnesses."""
from pathlib import Path
from collections import Counter,defaultdict
import hashlib,json,math,sys
import numpy as np
from scipy.stats import t
from threadpoolctl import threadpool_limits
import run_discovery_sampling_20261030 as study
O=study.O/'discovery-sampling-attempt-1'
def main():
    result=json.loads((O/'results.json').read_text());manifest=json.loads((O/'manifest.json').read_text())
    for name,key in [('results.json','results_sha256'),('case-results.jsonl','case_sha256'),('reference-results.jsonl','reference_sha256')]:assert hashlib.sha256((O/name).read_bytes()).hexdigest()==manifest[key]
    rows=[json.loads(x) for x in (O/'case-results.jsonl').read_text().splitlines()];assert len(rows)==10800
    by={(r['mechanism'],r['n'],r['replicate'],r['alpha'],r['method']):r for r in rows};assert len(by)==len(rows)
    groups=defaultdict(list)
    for row in rows:
        key=(row['mechanism'],row['n'],row['alpha'],row['method']);groups[key].append(row)
        assert row['effect']['covers']==(row['effect']['lower']<=row['truth_effect']<=row['effect']['upper'])
    for s in result['summaries']:
        g=groups[(s['mechanism'],s['n'],s['alpha'],s['method'])];assert len(g)==200
        assert s['coverage']['count']==sum(r['effect']['covers'] for r in g)
        for k,v in s['counts'].items():assert v==sum(r[k] for r in g)
    models=study.mechanisms();streams=np.random.SeedSequence(result['seed']).spawn(1800);max_error=0.;checked=0;checks=[]
    for mi,m in enumerate(models):
        pop=study.population(m)
        for ni,n in enumerate([100,500,2000]):
            for rep in [0,99,199]:
                rng=np.random.default_rng(streams[mi*600+ni*200+rep]);data=rng.standard_normal((n,len(m['b'])))@m['load'].T
                for alpha in [.01,.05]:
                    for method in ['full','screen','depth2']:
                        row=by[(m['name'],n,rep,alpha,method)];ctrl=row['effect']['controls'];z=np.column_stack([np.ones(n)]+[data[:,i] for i in ctrl]);q,_=np.linalg.qr(z,mode='reduced');x=data[:,m['x']];y=data[:,m['y']];rx=x-q@(q.T@x);ry=y-q@(q.T@y);b=float(rx@ry/(rx@rx));e=ry-b*rx;df=n-len(ctrl)-2;se=math.sqrt(float(e@e)/df/float(rx@rx));lo=b-t.ppf(.975,df)*se;hi=b+t.ppf(.975,df)*se
                        for k,v in [('estimate',b),('se',se),('lower',lo),('upper',hi)]:error=abs(v-row['effect'][k]);assert error<1e-9;max_error=max(max_error,error)
                        checked+=1
                if rep==0 and n==100:
                    # Relabel one stored dataset, execute one cross-check, and map edges back.
                    perm=list(reversed(range(len(m['b']))));oracle=study.SampleOracle(data[:,perm],.05,{});run=study.core.skeleton_search(oracle);mapped={tuple(sorted((perm[a],perm[b]))) for a,b in run['links']};reference={tuple(e) for e in by[(m['name'],n,rep,.05,'full')]['links']};assert mapped==reference;checks.append(m['name'])
    audit={'status':'pass','case_records':len(rows),'groups_checked':len(groups),'independent_QR_interval_checks':checked,'maximum_absolute_error':max_error,'variable_reversal_checks':checks,'scope':'Retained accounting, independently residualized intervals, fixed-seed witnesses and one relabel per mechanism; not a new experiment or general validity theorem.'}
    (O/'verification.json').write_text(json.dumps(audit,indent=2)+chr(10));print(json.dumps(audit,indent=2))
if __name__=='__main__':
    with threadpool_limits(limits=1):main()
