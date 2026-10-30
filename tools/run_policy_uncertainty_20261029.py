"""Trajectory bootstrap of a specified conditional transition model."""
from pathlib import Path
from hashlib import sha256
import json
import time
import numpy as np
from scipy.special import ndtri
from scipy.stats import qmc
from run_servicing_study_20261029 import generate, gfit, ipw, direct, POLICIES, LABELS

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/scientific-gap-closure/2026-10-29'

def simulate(policy,x,innov,b,sigma,omit=False):
    l=.4*x+innov[:,0];total=np.zeros(len(x))
    for t in range(3):
        a=np.zeros(len(x)) if policy is None else (l>policy).astype(float)
        nxt=b[0]+b[1]*l+(b[2]*a if omit else b[2]*x+b[3]*a)+sigma*innov[:,t+1]
        total+=10-2*nxt**2-a+.5*a*x;l=nxt
    return total

def sufficient(d,omit):
    n=len(d['x']);p=3 if omit else 4
    zz=np.zeros((n,p,p));zy=np.zeros((n,p));yy=np.zeros(n);count=np.zeros(n)
    for t in range(3):
        obs=d['observed'][:,t].astype(float)
        cols=[np.ones(n),d['L'][:,t],d['A'][:,t]] if omit else [np.ones(n),d['L'][:,t],d['x'],d['A'][:,t]]
        z=np.column_stack(cols);y=d['N'][:,t]
        zz+=np.einsum('ni,nj,n->nij',z,z,obs);zy+=z*(obs*y)[:,None];yy+=obs*y*y;count+=obs
    return zz,zy,yy,count

def from_sufficient(stats,counts):
    zz,zy,yy,n=stats;mat=np.einsum('n,nij->ij',counts,zz);rhs=counts@zy
    b=np.linalg.solve(mat,rhs);df=counts@n-len(b);rss=counts@yy-b@rhs
    if df<=0 or rss<=0 or not np.isfinite(b).all():raise ValueError('Invalid bootstrap regression')
    return b,float(np.sqrt(rss/df))

def normals(power,seed):
    u=qmc.Sobol(d=5,scramble=True,seed=seed).random_base2(power)
    assert np.all((u>0)&(u<1))
    z=ndtri(u);return z[:,0],z[:,1:]

def main():
    start=time.monotonic();path=OUT/'policy-uncertainty-plan.json';plan=json.loads(path.read_text());bud=plan['budget'];seed=bud['seed']
    rng=np.random.default_rng(seed+1);rx=rng.normal(size=bud['reference_n']);ri=rng.normal(size=(len(rx),4))
    reference_arrays=[direct(p,rx,ri) for p in POLICIES]
    reference=[dict(policy=label,value=float(v.mean()),mcse=float(v.std(ddof=1)/np.sqrt(len(v))),
         improvement=float((v-reference_arrays[0]).mean()),difference_mcse=float((v-reference_arrays[0]).std(ddof=1)/np.sqrt(len(v))))
         for label,v in zip(LABELS,reference_arrays)]
    integration=[]
    for j in range(8):
        qx,qi=normals(bud['integration_power'],seed+100+j)
        integration.append([float(simulate(p,qx,qi,np.array([0,.6,.25,-.5]),1).mean()) for p in POLICIES])
    gx,gi=normals(bud['integration_power'],seed+100)
    old=json.loads((OUT/'servicing-plan.json').read_text());records=[]
    for si,name in enumerate(plan['scenarios']):
        sc=next(s for s in old['scenarios'] if s['id']==name)
        for rep in range(bud['replications_per_scenario']):
            rng=np.random.default_rng(np.random.SeedSequence([seed,si,rep]))
            training=generate(bud['training_n'],rng,sc);selected=1+int(np.argmax([ipw(training,p)[0].mean() for p in POLICIES[1:]]))
            d=generate(bud['evaluation_n'],rng,sc);omit=sc['gcomp_omit_x'];stats=sufficient(d,omit)
            b,sigma=from_sufficient(stats,np.ones(bud['evaluation_n']));check_b,check_s=gfit(d,omit)
            assert np.max(np.abs(b-check_b))<1e-10 and abs(sigma-check_s)<1e-10
            indices=list(dict.fromkeys([0,3,selected]));means={pi:float(simulate(POLICIES[pi],gx,gi,b,sigma,omit).mean()) for pi in indices}
            draws={pi:[] for pi in indices}
            for j in range(bud['bootstrap_draws']):
                counts=np.bincount(rng.integers(bud['evaluation_n'],size=bud['evaluation_n']),minlength=bud['evaluation_n'])
                bb,ss=from_sufficient(stats,counts)
                for pi in indices:draws[pi].append(float(simulate(POLICIES[pi],gx,gi,bb,ss,omit).mean()))
            zero=ipw(d,None)[0]
            for label,pi in [('fixed_threshold',3),('selected_threshold',selected)]:
                score=ipw(d,POLICIES[pi])[0];paired=score-zero
                for target,estimate,values,truth,mcse,ipw_score in [
                    ('value',means[pi],np.array(draws[pi]),reference[pi]['value'],reference[pi]['mcse'],score),
                    ('improvement',means[pi]-means[0],np.array(draws[pi])-draws[0],reference[pi]['improvement'],reference[pi]['difference_mcse'],paired)]:
                    qlo,qhi=np.quantile(values,[.025,.975]);lo=2*estimate-qhi;hi=2*estimate-qlo
                    se=ipw_score.std(ddof=1)/np.sqrt(len(score));iv=float(ipw_score.mean());ilo=iv-1.95996398454*se;ihi=iv+1.95996398454*se
                    for method,value,l,h in [('gcomp_bootstrap',estimate,lo,hi),('prefix_ipw',iv,ilo,ihi)]:
                        records.append(dict(scenario=name,replication=rep,policy=label,selected_index=pi,target=target,method=method,
                         estimate=float(value),reference=truth,reference_mcse=mcse,covered=bool(l<=truth<=h),interval=[float(l),float(h)],
                         reference_boundary_ambiguous=bool(abs(l-truth)<=1.96*mcse or abs(h-truth)<=1.96*mcse),positive_lower_bound=bool(l>0)))
            if time.monotonic()-start>60*bud['cpu_minutes']:raise RuntimeError('Budget exhausted')
            if (rep+1)%25==0: print(json.dumps(dict(scenario=name,replications=rep+1,seconds=round(time.monotonic()-start,1))),flush=True)
    summaries=[]
    for name in plan['scenarios']:
        for policy in ['fixed_threshold','selected_threshold']:
            for target in ['value','improvement']:
                for method in ['gcomp_bootstrap','prefix_ipw']:
                    rs=[r for r in records if all(r[k]==v for k,v in dict(scenario=name,policy=policy,target=target,method=method).items())]
                    errors=np.array([r['estimate']-r['reference'] for r in rs]);p=np.mean([r['covered'] for r in rs])
                    summaries.append(dict(scenario=name,policy=policy,target=target,method=method,coverage=float(p),coverage_mcse=float(np.sqrt(p*(1-p)/len(rs))),
                     bias=float(errors.mean()),bias_mcse=float(errors.std(ddof=1)/np.sqrt(len(rs))),mean_width=float(np.mean([r['interval'][1]-r['interval'][0] for r in rs])),
                     reference_boundary_ambiguous=sum(r['reference_boundary_ambiguous'] for r in rs),positive_lower_fraction=float(np.mean([r['positive_lower_bound'] for r in rs])),
                     selection_counts={LABELS[i]:sum(r['selected_index']==i for r in rs) for i in range(1,5)}))
    result=dict(complete=True,replications=300,bootstrap_draws_per_replication=199,reference=reference,integration_scrambles=integration,
        scenarios=summaries,seconds=time.monotonic()-start,plan_sha256=sha256(path.read_bytes()).hexdigest(),code_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
        scope=plan['not_concluded'],uncertainty_target=plan['target'])
    (OUT/'policy-uncertainty-results.json').write_text(json.dumps(result,indent=2)+'\n')
    (OUT/'policy-uncertainty-replications.json').write_text(json.dumps(records)+'\n')
    print(json.dumps(dict(complete=True,replications=300,seconds=result['seconds'])))

if __name__=='__main__':main()
