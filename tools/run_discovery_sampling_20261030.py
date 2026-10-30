"""Declared Gaussian sampling study; project code, not native package evaluation."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
from collections import defaultdict
import argparse, hashlib, json, math, platform, sys, time
import numpy as np
import scipy
from scipy.stats import norm, t
from threadpoolctl import threadpool_limits
import run_discovery_repair_20261029 as core

R=Path(__file__).resolve().parents[1]
O=R/'docs/twelve-hour-closure/2026-10-29'
START=time.monotonic()
def budget():
    if time.monotonic()-START>1200:raise TimeoutError('Twenty-minute declared compute budget')
core.check_budget=budget
def save(p,d):p.write_text(json.dumps(d,indent=2)+chr(10))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def mechanisms():
    out=[]
    for name,scale in [('strong',F(1)),('weak',F(1,8))]:
        arcs=[(z,v) for z in range(3) for v in [3,4]]+[(3,5),(4,5)]
        b=[[F(0) for j in range(6)] for i in range(6)]
        for z,w in enumerate([F(1),F(4,5),F(6,5)]):b[3][z]=scale*w
        for z,w in enumerate([F(7,10),F(11,10),F(9,10)]):b[4][z]=scale*w
        b[5][3]=F(11,10);b[5][4]=F(3,5)
        out.append(dict(name=name,arcs=arcs,b=b,x=3,y=4,baseline=[0,1,2],collider=5,effect=0,faithful_expected=True))
    b=[[F(0),F(0),F(0)],[F(1),F(0),F(0)],[F(-1),F(1),F(0)]]
    out.append(dict(name='cancellation',arcs=[(0,1),(0,2),(1,2)],b=b,x=1,y=2,baseline=[0],collider=None,effect=1,faithful_expected=False))
    return out
def population(m):
    n=len(m['b']);a=core.inverse([[F(i==j)-m['b'][i][j] for j in range(n)] for i in range(n)])
    cov=[[sum(a[i][k]*a[j][k] for k in range(n)) for j in range(n)] for i in range(n)]
    oracle=core.Oracle(n,m['arcs']);violations=[];minimum=1.;tested=0
    def conditional(i,j,z):
        if not z:return cov[i][j]
        inv=core.inverse([[cov[u][v] for v in z] for u in z])
        return cov[i][j]-sum(cov[i][u]*inv[r][c]*cov[v][j] for r,u in enumerate(z) for c,v in enumerate(z))
    for i,j in combinations(range(n),2):
        rest=[k for k in range(n) if k not in [i,j]]
        for size in range(n-1):
            for z in combinations(rest,size):
                c=conditional(i,j,z);sep=oracle.moral(i,j,z);path=oracle.path_oracle(i,j,z);assert sep==path;tested+=1
                if (c==0)!=sep:violations.append(dict(pair=[i,j],given=list(z),zero_covariance=c==0,d_separated=sep))
                if c:minimum=min(minimum,abs(float(c))/math.sqrt(float(conditional(i,i,z)*conditional(j,j,z))))
    if m['faithful_expected']:assert not violations,(m['name'],violations)
    else:assert violations,'Expected a recorded faithfulness failure'
    m['load']=np.array([[float(v) for v in row] for row in a]);m['cov']=np.array([[float(v) for v in row] for row in cov])
    return dict(mechanism=m['name'],coefficients=[[str(v) for v in row] for row in m['b']],covariance=[[str(v) for v in row] for row in cov],queries_checked=tested,minimum_nonzero_partial_correlation=minimum,faithfulness_violations=violations)
class SampleOracle:
    def __init__(self,data,alpha,cache):
        self.n=data.shape[1];self.sample_n=len(data);self.data=data;self.cov=np.cov(data,rowvar=False);self.alpha=alpha;self.cut=norm.ppf(1-alpha/2);self.cache=cache;self.calls=[]
    def partial(self,x,y,given):
        key=(min(x,y),max(x,y),tuple(sorted(given)))
        if key not in self.cache:
            indices=[x,y]+list(given);cov=self.cov[np.ix_(indices,indices)];prec=np.linalg.inv(cov)
            rho=-prec[0,1]/math.sqrt(prec[0,0]*prec[1,1]);assert abs(rho)<1
            self.cache[key]=float(rho)
        return self.cache[key]
    def independent(self,x,y,given):
        self.calls.append((min(x,y),max(x,y),tuple(sorted(given))))
        rho=self.partial(x,y,given);stat=math.sqrt(self.sample_n-len(given)-3)*abs(np.arctanh(rho))
        return stat<=self.cut
def ols(data,m,controls):
    x=data[:,m['x']];y=data[:,m['y']];design=np.column_stack([np.ones(len(x)),x]+[data[:,z] for z in controls]);beta=np.linalg.lstsq(design,y,rcond=None)[0];res=y-design@beta;df=len(x)-design.shape[1]
    var=float(res@res/df);se=math.sqrt(var*np.linalg.inv(design.T@design)[1,1]);critical=t.ppf(.975,df);estimate=float(beta[1]);lo=estimate-critical*se;hi=estimate+critical*se
    return dict(estimate=estimate,se=se,lower=float(lo),upper=float(hi),covers=bool(lo<=m['effect']<=hi),controls=controls)
def independent_checks(data,m):
    oracle=SampleOracle(data,.05,{});n=data.shape[1];max_error=0.;queries=0
    for i,j in combinations(range(n),2):
        others=[k for k in range(n) if k not in [i,j]]
        for size in range(n-1):
            for z in combinations(others,size):
                design=np.column_stack([np.ones(len(data))]+[data[:,k] for k in z]);ri=data[:,i]-design@np.linalg.lstsq(design,data[:,i],rcond=None)[0];rj=data[:,j]-design@np.linalg.lstsq(design,data[:,j],rcond=None)[0]
                rho=float(ri@rj/math.sqrt((ri@ri)*(rj@rj)));error=abs(rho-oracle.partial(i,j,z));assert error<1e-10;max_error=max(max_error,error);queries+=1
    fit=ols(data,m,m['baseline']);z=np.column_stack([np.ones(len(data))]+[data[:,k] for k in m['baseline']]);rx=data[:,m['x']]-z@np.linalg.lstsq(z,data[:,m['x']],rcond=None)[0];ry=data[:,m['y']]-z@np.linalg.lstsq(z,data[:,m['y']],rcond=None)[0];b=float(rx@ry/(rx@rx));res=ry-b*rx;se=math.sqrt(float(res@res)/(len(data)-len(m['baseline'])-2)/float(rx@rx));assert abs(b-fit['estimate'])<1e-10 and abs(se-fit['se'])<1e-10
    return dict(mechanism=m['name'],partial_queries=queries,max_precision_residual_error=max_error,ols_residualization_error=abs(b-fit['estimate']))
def wilson(k,n):
    z=norm.ppf(.975);p=k/n;den=1+z*z/n;center=(p+z*z/(2*n))/den;half=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    return [float(center-half),float(center+half)]
def summarize(rows):
    groups=defaultdict(list)
    for row in rows:groups[(row['mechanism'],row['n'],row['alpha'],row['method'])].append(row)
    results=[]
    for key,g in sorted(groups.items()):
        counts={k:sum(int(r[k]) for r in g) for k in ['wrong_skeleton','xy_retained','incomplete']};covers=sum(r['effect']['covers'] for r in g);truth=g[0]['truth_effect'];errors=np.array([r['effect']['estimate']-truth for r in g]);lengths=[r['effect']['upper']-r['effect']['lower'] for r in g]
        results.append(dict(mechanism=key[0],n=key[1],alpha=key[2],method=key[3],replicates=len(g),counts=counts,proportions={k:{'estimate':v/len(g),'wilson95':wilson(v,len(g))} for k,v in counts.items()},coverage={'count':covers,'estimate':covers/len(g),'wilson95':wilson(covers,len(g))},bias=float(np.mean(errors)),rmse=float(np.sqrt(np.mean(errors**2))),mean_interval_length=float(np.mean(lengths)),mean_distinct_queries=float(np.mean([r['queries'] for r in g])),selected_controls=dict(__import__('collections').Counter(','.join(map(str,r['effect']['controls'])) or 'none' for r in g))))
    paired=[]
    for m in ['strong','weak','cancellation']:
      for n in [100,500,2000]:
       for alpha in [.01,.05]:
        full={r['replicate']:r for r in groups[(m,n,alpha,'full')]}
        for method in ['screen','depth2']:
         alternative={r['replicate']:r for r in groups[(m,n,alpha,method)]};diff=np.array([int(alternative[i]['wrong_skeleton'])-int(full[i]['wrong_skeleton']) for i in sorted(full)]);mean=float(np.mean(diff));se=float(np.std(diff,ddof=1)/math.sqrt(len(diff)))
         paired.append(dict(mechanism=m,n=n,alpha=alpha,comparison=method+' minus full',skeleton_error_difference=mean,monte_carlo_se=se,normal95=[mean-1.96*se,mean+1.96*se]))
    return results,paired
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=O/'discovery-sampling-attempt-1');args=p.parse_args();out=args.output;out.mkdir(parents=True,exist_ok=False)
    rows=[];references=[];checks=[]
    try:
      models=mechanisms();population_results=[population(m) for m in models];save(out/'population.json',population_results)
      seed=2026103001;streams=np.random.SeedSequence(seed).spawn(len(models)*3*200);s=iter(streams)
      with (out/'case-results.jsonl').open('w') as f, (out/'reference-results.jsonl').open('w') as rf:
       for m in models:
        truth={core.edge(*e) for e in m['arcs']}
        for n in [100,500,2000]:
         for rep in range(200):
          budget();rng=np.random.default_rng(next(s));data=rng.standard_normal((n,len(m['b'])))@m['load'].T
          if rep==0 and n==100:checks.append(independent_checks(data,m));save(out/'independent-checks.json',checks)
          ref=dict(mechanism=m['name'],n=n,replicate=rep,truth_effect=m['effect'],all_baseline=ols(data,m,m['baseline']),unadjusted=ols(data,m,[]))
          if m['collider'] is not None:ref['invalid_later_control']=ols(data,m,m['baseline']+[m['collider']])
          references.append(ref);rf.write(json.dumps(ref)+chr(10))
          cache={}
          for alpha in [.01,.05]:
           for method in ['full','screen','depth2']:
            oracle=SampleOracle(data,alpha,cache);run=core.skeleton_search(oracle,screen=method=='screen',cap=2 if method=='depth2' else None);links={tuple(e) for e in run['links']};selected=[z for z in m['baseline'] if core.edge(z,m['x']) in links and core.edge(z,m['y']) in links]
            row=dict(mechanism=m['name'],n=n,replicate=rep,alpha=alpha,method=method,truth_effect=m['effect'],wrong_skeleton=links!=truth,false_links=len(links-truth),missing_links=len(truth-links),xy_retained=core.edge(m['x'],m['y']) in links,incomplete=run['completion']=='incomplete_search',queries=run['distinct_queries'],links=run['links'],effect=ols(data,m,selected));rows.append(row);f.write(json.dumps(row)+chr(10))
         f.flush();rf.flush();print(json.dumps({'completed':m['name'],'n':n,'rows':len(rows),'seconds':round(time.monotonic()-START,2)}),flush=True)
      summaries,paired=summarize(rows);reference_summary=[]
      for m in models:
       for n in [100,500,2000]:
        group=[r for r in references if r['mechanism']==m['name'] and r['n']==n]
        for method in ['all_baseline','unadjusted','invalid_later_control']:
         if method not in group[0]:continue
         fits=[r[method] for r in group];k=sum(x['covers'] for x in fits);err=np.array([x['estimate']-m['effect'] for x in fits]);reference_summary.append(dict(mechanism=m['name'],n=n,method=method,replicates=len(group),coverage=k/len(group),wilson95=wilson(k,len(group)),bias=float(np.mean(err)),rmse=float(np.sqrt(np.mean(err**2))),mean_interval_length=float(np.mean([x['upper']-x['lower'] for x in fits]))))
      result=dict(status='completed_declared_sampling_study',seed=seed,replicates_per_cell=200,datasets=len(references),searches=len(rows),elapsed_seconds=round(time.monotonic()-START,3),population=population_results,independent_checks=checks,summaries=summaries,paired=paired,references=reference_summary,limits=['Finite constructed Gaussian suite','Cancellation violates faithfulness','Selected-control intervals are deliberately naive diagnostic comparators','No native package, live LLM, graph orientation, bank outcome or general finite-sample guarantee'])
      save(out/'results.json',result);save(out/'manifest.json',dict(script_sha256=sha(Path(__file__)),plan_sha256=sha(O/'discovery-sampling-plan.md'),inherited_search_sha256=sha(R/'tools/run_discovery_repair_20261029.py'),results_sha256=sha(out/'results.json'),case_sha256=sha(out/'case-results.jsonl'),reference_sha256=sha(out/'reference-results.jsonl'),python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__))
      print(json.dumps({k:result[k] for k in ['status','datasets','searches','elapsed_seconds']}),flush=True)
    except Exception as e:
      save(out/'failure.json',dict(error=repr(e),rows=len(rows),seconds=time.monotonic()-START));raise
if __name__=='__main__':
    with threadpool_limits(limits=1):main()
