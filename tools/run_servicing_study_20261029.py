"""Frozen generated sequential policy study; all rewards are illustrative units."""
from pathlib import Path
from hashlib import sha256
import json
import time
import numpy as np
from scipy.special import expit, logit
from scipy.stats import norm

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/scientific-gap-closure/2026-10-29'
POLICIES=[None,-.5,0.,.5,1.]
LABELS=['always_zero','threshold_-0.5','threshold_0','threshold_0.5','threshold_1']

def action(l,policy):
    return np.zeros(len(l),dtype=int) if policy is None else (l>policy).astype(int)

def generate(n,rng,scenario):
    x=rng.normal(size=n); l=.4*x+rng.normal(size=n);prev=np.zeros(n); alive=np.ones(n,dtype=bool)
    states=[];acts=[];rewards=[];probs=[];obsprobs=[];observed=[];nexts=[]
    for t in range(3):
        p=np.clip(expit(.3*x-.5*l+.2*prev),*scenario['action_clip']);a=rng.binomial(1,p)
        eps=rng.normal(size=n);nxt=.6*l+.25*x-.5*a+eps
        reward=10-2*nxt**2-a+.5*a*x
        g=.65+.30*expit(.3*l-.2*a)
        actual=expit(logit(g)+1.5*eps) if scenario['future_censoring'] else g
        alive=alive & (rng.random(n)<actual)
        states.append(l);acts.append(a);rewards.append(reward);probs.append(p);obsprobs.append(g);observed.append(alive.copy());nexts.append(nxt)
        l=nxt;prev=a
    # Full histories are generated for the evaluator. Estimators mask unobserved transitions.
    return dict(x=x,L=np.array(states).T,A=np.array(acts).T,R=np.array(rewards).T,
                p=np.array(probs).T,g=np.array(obsprobs).T,observed=np.array(observed).T,N=np.array(nexts).T)

def ipw(d,policy):
    n=len(d['x']);weight=np.ones(n);score=np.zeros(n);ess=[];maxw=[]
    for t in range(3):
        match=d['A'][:,t]==action(d['L'][:,t],policy)
        pa=np.where(d['A'][:,t]==1,d['p'][:,t],1-d['p'][:,t])
        weight*=match*d['observed'][:,t]/(pa*d['g'][:,t])
        score+=weight*d['R'][:,t]
        sq=np.sum(weight**2);ess.append(float(weight.sum()**2/sq) if sq else 0.)
        maxw.append(float(weight.max()))
    assert np.isfinite(score).all()
    return score,ess,maxw

def direct(policy,x,innov,coef=None,sigma=1.,omit=False):
    l=.4*x+innov[:,0];total=np.zeros(len(x))
    for t in range(3):
        a=action(l,policy)
        if coef is None:nxt=.6*l+.25*x-.5*a+innov[:,t+1]
        else:
            design=np.column_stack([np.ones(len(x)),l,a] if omit else [np.ones(len(x)),l,x,a])
            nxt=design@coef+sigma*innov[:,t+1]
        total+=10-2*nxt**2-a+.5*a*x;l=nxt
    return total

def gfit(d,omit):
    observed=d['observed'];x=np.broadcast_to(d['x'][:,None],observed.shape)[observed]
    l=d['L'][observed];a=d['A'][observed];y=d['N'][observed]
    z=np.column_stack([np.ones(len(y)),l,a] if omit else [np.ones(len(y)),l,x,a])
    b,_,rank,_=np.linalg.lstsq(z,y,rcond=None)
    if rank!=z.shape[1]:raise ValueError('Singular g-computation regression')
    sigma=float(np.sqrt(np.sum((y-z@b)**2)/(len(y)-z.shape[1])))
    return b,sigma

def main():
    start=time.monotonic();planpath=OUT/'servicing-plan.json';plan=json.loads(planpath.read_text());budget=plan['budget']
    rng=np.random.default_rng(plan['seeds']['reference']);x=rng.normal(size=budget['reference_n']);innov=rng.normal(size=(len(x),4))
    ref_arrays=[direct(p,x,innov) for p in POLICIES]
    reference=[dict(policy=l,value=float(v.mean()),mcse=float(v.std(ddof=1)/np.sqrt(len(v))),
                    improvement_vs_zero=float((v-ref_arrays[0]).mean()),
                    difference_mcse=float((v-ref_arrays[0]).std(ddof=1)/np.sqrt(len(v))))
               for l,v in zip(LABELS,ref_arrays)]
    (OUT/'servicing-reference.json').write_text(json.dumps(reference,indent=2)+chr(10))
    records=[];summaries=[];z=norm.ppf(.975)
    for si,scenario in enumerate(plan['scenarios']):
        for rep in range(budget['replications_per_scenario']):
            rng=np.random.default_rng(np.random.SeedSequence([plan['seeds']['evaluation'],si,rep]))
            training=generate(budget['training_n'],rng,scenario)
            selected=1+int(np.argmax([ipw(training,p)[0].mean() for p in POLICIES[1:]]))
            evaluation=generate(budget['evaluation_n'],rng,scenario)
            coef,sigma=gfit(evaluation,scenario['gcomp_omit_x'])
            sim=np.random.default_rng(np.random.SeedSequence([plan['seeds']['gcomp'],si,rep]))
            gx=sim.normal(size=budget['gcomp_n']);gi=sim.normal(size=(len(gx),4))
            scores=[];rows=[]
            for pi,policy in enumerate(POLICIES):
                score,ess,maxw=ipw(evaluation,policy);scores.append(score)
                value=float(score.mean());se=float(score.std(ddof=1)/np.sqrt(len(score)))
                matching=np.all(evaluation['observed'] & (evaluation['A']==action(evaluation['L'].ravel(),policy).reshape(evaluation['L'].shape)),axis=1)
                case=float(evaluation['R'][matching].sum(axis=1).mean()) if matching.any() else None
                gvalue=float(direct(policy,gx,gi,coef,sigma,scenario['gcomp_omit_x']).mean())
                truth=reference[pi]['value'];mcse=reference[pi]['mcse'];lo=value-z*se;hi=value+z*se
                rows.append(dict(policy=LABELS[pi],reference_index=pi,ipw=value,ipw_se=se,interval=[lo,hi],
                    reference_covered=bool(lo<=truth<=hi),
                    ambiguous_reference_boundary=bool(abs(lo-truth)<=z*mcse or abs(hi-truth)<=z*mcse),
                    complete_case=case,complete_case_n=int(matching.sum()),gcomp=gvalue,ess=ess,max_weight=maxw))
            for row,score in zip(rows,scores):
                paired=score-scores[0];row['paired_vs_zero']=float(paired.mean());row['paired_se']=float(paired.std(ddof=1)/np.sqrt(len(paired)))
            chosen=dict(rows[selected]);chosen['policy']='selected_threshold';chosen['selected_label']=LABELS[selected]
            chosen['finite_set_regret']=float(max(r['value'] for r in reference[1:])-reference[selected]['value'])
            for row in rows+[chosen]:row.update(scenario=scenario['id'],replication=rep);records.append(row)
            if time.monotonic()-start>60*budget['cpu_minutes_max']:raise RuntimeError('Budget exhausted; no completion claim')
        for name in LABELS+['selected_threshold']:
            rs=[r for r in records if r['scenario']==scenario['id'] and r['policy']==name]
            truths=np.array([reference[r['reference_index']]['value'] for r in rs]);out={}
            for method in ['ipw','complete_case','gcomp']:
                keep=[i for i,r in enumerate(rs) if r[method] is not None];delta=np.array([rs[i][method]-truths[i] for i in keep])
                out[method]=dict(available=len(keep),unavailable=len(rs)-len(keep),bias=float(delta.mean()),rmse=float(np.sqrt(np.mean(delta**2))),
                                 bias_mcse=float(delta.std(ddof=1)/np.sqrt(len(delta))))
            covered=np.array([r['reference_covered'] for r in rs]);coverage=float(covered.mean())
            summary=dict(scenario=scenario['id'],policy=name,replications=len(rs),methods=out,
                reference_point_coverage=coverage,coverage_mcse=float(np.sqrt(coverage*(1-coverage)/len(rs))),
                ambiguous_reference_boundaries=sum(r['ambiguous_reference_boundary'] for r in rs),
                mean_interval_width=float(np.mean([r['interval'][1]-r['interval'][0] for r in rs])),
                mean_prefix_ess=np.mean([r['ess'] for r in rs],axis=0).tolist(),
                minimum_prefix_ess=np.min([r['ess'] for r in rs],axis=0).tolist(),maximum_prefix_weight=np.max([r['max_weight'] for r in rs],axis=0).tolist(),
                mean_paired_vs_zero=float(np.mean([r['paired_vs_zero'] for r in rs])),
                mean_paired_se=float(np.mean([r['paired_se'] for r in rs])))
            if name=='selected_threshold':
                summary['selection_counts']={label:sum(r['selected_label']==label for r in rs) for label in LABELS[1:]}
                summary['mean_finite_set_regret']=float(np.mean([r['finite_set_regret'] for r in rs]))
            summaries.append(summary)
        (OUT/'servicing-replications.json').write_text(json.dumps(records)+chr(10))
        (OUT/'servicing-results.json').write_text(json.dumps(dict(plan_sha256=sha256(planpath.read_bytes()).hexdigest(),
          code_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),reference=reference,scenarios=summaries,
          seconds=time.monotonic()-start,completed_scenarios=si+1,complete=si+1==len(plan['scenarios']),
          scope=plan['kind'],normal_intervals=True,exact_coverage_claim=False,gcomp_uncertainty='not estimated',
          claims='Conditional generated study; no bank effect, general policy optimality or live-model performance'),indent=2)+chr(10))
        print(json.dumps(dict(scenario=scenario['id'],replications=budget['replications_per_scenario'],seconds=round(time.monotonic()-start,2))),flush=True)

if __name__=='__main__':main()
