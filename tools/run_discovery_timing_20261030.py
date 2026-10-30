"""Prospective follow-up using the same random draws and a declared information clock."""
from pathlib import Path
import json,time,hashlib
import numpy as np
from threadpoolctl import threadpool_limits
import run_discovery_sampling_20261030 as s

def main():
    O=s.O/'discovery-timing-attempt-1';O.mkdir(exist_ok=False);rows=[];start=time.monotonic()
    try:
        first=s.O/'discovery-sampling-attempt-1';original=[json.loads(x) for x in (first/'case-results.jsonl').read_text().splitlines()];lookup={(r['mechanism'],r['n'],r['replicate'],r['alpha'],r['method']):r for r in original}
        seed=json.loads((first/'results.json').read_text())['seed'];streams=np.random.SeedSequence(seed).spawn(1800);population=[]
        models=s.mechanisms()[:2]
        for m in models:
            old=s.population(m);reduced={**m,'b':[r[:5] for r in m['b'][:5]],'arcs':[(a,b) for a,b in m['arcs'] if b!=5],'collider':None};p=s.population(reduced);assert np.allclose(reduced['cov'],m['cov'][:5,:5]);population.append(p)
        s.save(O/'population.json',population)
        with (O/'case-results.jsonl').open('w') as f:
          for mi,m in enumerate(models):
            truth={s.core.edge(a,b) for a,b in m['arcs'] if b!=5}
            for ni,n in enumerate([100,500,2000]):
              for rep in range(200):
                s.budget();rng=np.random.default_rng(streams[mi*600+ni*200+rep]);data=(rng.standard_normal((n,6))@m['load'].T)[:,:5];cache={}
                for alpha in [.01,.05]:
                  for method in ['full','screen','depth2']:
                    oracle=s.SampleOracle(data,alpha,cache);run=s.core.skeleton_search(oracle,screen=method=='screen',cap=2 if method=='depth2' else None);links={tuple(e) for e in run['links']};selected=[z for z in m['baseline'] if s.core.edge(z,m['x']) in links and s.core.edge(z,m['y']) in links];old=lookup[(m['name'],n,rep,alpha,method)];old_common={tuple(e) for e in old['links'] if 5 not in e}
                    row=dict(mechanism=m['name'],n=n,replicate=rep,alpha=alpha,method=method,truth_effect=m['effect'],wrong_skeleton=links!=truth,false_links=len(links-truth),missing_links=len(truth-links),xy_retained=s.core.edge(m['x'],m['y']) in links,incomplete=run['completion']=='incomplete_search',queries=run['distinct_queries'],links=run['links'],effect=s.ols(data,m,selected),previous_common_wrong=old_common!=truth,previous_covers=old['effect']['covers'],previous_estimate=old['effect']['estimate']);rows.append(row);f.write(json.dumps(row)+chr(10))
              f.flush();print(json.dumps({'mechanism':m['name'],'n':n,'rows':len(rows),'seconds':round(time.monotonic()-start,2)}),flush=True)
        # Summarize only the two declared mechanisms, with no artificial cancellation rerun.
        from collections import defaultdict,Counter
        groups=defaultdict(list)
        for row in rows:groups[(row['mechanism'],row['n'],row['alpha'],row['method'])].append(row)
        summary=[]
        for key,g in sorted(groups.items()):
            k=sum(r['effect']['covers'] for r in g);errors=sum(r['wrong_skeleton'] for r in g);dc=np.array([int(r['effect']['covers'])-int(r['previous_covers']) for r in g]);dg=np.array([int(r['wrong_skeleton'])-int(r['previous_common_wrong']) for r in g]);b=np.array([r['effect']['estimate']-r['truth_effect'] for r in g])
            summary.append(dict(mechanism=key[0],n=key[1],alpha=key[2],method=key[3],replicates=len(g),wrong_skeleton=errors,error_rate=errors/len(g),incomplete=sum(r['incomplete'] for r in g),xy_retained=sum(r['xy_retained'] for r in g),coverage=k/len(g),coverage_wilson95=s.wilson(k,len(g)),bias=float(np.mean(b)),mean_interval_length=float(np.mean([r['effect']['upper']-r['effect']['lower'] for r in g])),coverage_paired_difference=float(np.mean(dc)),coverage_difference_mcse=float(np.std(dc,ddof=1)/np.sqrt(len(g))),common_skeleton_paired_difference=float(np.mean(dg)),skeleton_difference_mcse=float(np.std(dg,ddof=1)/np.sqrt(len(g))),selected_controls=dict(Counter(','.join(map(str,r['effect']['controls'])) or 'none' for r in g))))
        result=dict(status='completed_declared_timing_followup',seed=seed,datasets=1200,searches=len(rows),elapsed_seconds=round(time.monotonic()-start,3),population=population,summaries=summary,limits=['Prospective after first-study inspection','Same data/parameters, only known later descendant excluded','No general advice to remove variables from arbitrary graphs','Cancellation unchanged and not rerun','Naive selected-control intervals remain unqualified'])
        s.save(O/'results.json',result);s.save(O/'manifest.json',dict(script_sha256=s.sha(Path(__file__)),plan_sha256=s.sha(s.O/'discovery-timing-plan.md'),parent_results_sha256=s.sha(first/'results.json'),results_sha256=s.sha(O/'results.json'),cases_sha256=s.sha(O/'case-results.jsonl')));print(json.dumps({k:result[k] for k in ['status','datasets','searches','elapsed_seconds']}),flush=True)
    except Exception as e:s.save(O/'failure.json',dict(error=repr(e),completed_rows=len(rows)));raise
if __name__=='__main__':
    with threadpool_limits(limits=1):main()
