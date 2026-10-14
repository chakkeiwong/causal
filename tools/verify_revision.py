#!/usr/bin/env python3
"""Independent finite-path checks and focused latent-fit convergence follow-up."""
from pathlib import Path
import itertools
import hashlib
import json
import sys
import numpy as np
from revision_studies import (TRUE_HMM,SEED,hmm_fb,hmm_fit,hmm_sim,hmm_reactive_value,
                              coll_q,coll_scores,P_COLL,INIT_COLL,E_COLL,REWARD_COLL,GAMMA)
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/derivations'


def hmm_check():
    o=np.array([[0,2,1,0],[2,1,2,1]]); a=np.array([[1,0,1],[0,1,1]])
    records=[]
    for joint in [False,True]:
        mu,p,b,q=(TRUE_HMM[k] for k in ['mu','p','b','q'])
        initial=np.zeros(2); pc=np.zeros_like(p); bc=np.zeros_like(b); qc=np.zeros((2,2)); loglike=0.
        for signals,actions in zip(o,a):
            weighted=[]
            for states in itertools.product(range(2),repeat=len(signals)):
                w=mu[states[0]]*b[states[0],signals[0]]
                for t,act in enumerate(actions):
                    w*=p[act,states[t],states[t+1]]*b[states[t+1],signals[t+1]]
                    if joint: w*=q[states[t]] if act else 1-q[states[t]]
                weighted.append((states,w))
            z=sum(w for _,w in weighted); loglike+=np.log(z)
            for states,w in weighted:
                post=w/z; initial[states[0]]+=post
                for t,signal in enumerate(signals): bc[states[t],signal]+=post
                for t,act in enumerate(actions): pc[act,states[t],states[t+1]]+=post; qc[states[t],act]+=post
        got=hmm_fb(o,a,TRUE_HMM,joint)
        errors=[float(np.max(np.abs(np.array(g)-ref))) for g,ref in zip(got,[loglike,initial,pc,bc,qc])]
        assert max(errors)<1e-12,errors
        records.append({'joint_logging':joint,'maximum_error':max(errors),'checks':['observed likelihood','initial posterior counts','transition posterior counts','emission posterior counts','action posterior counts'],'latent_paths_per_sequence':16})
    return records


def dr_check():
    h=3; states=[]; actions=[]; probability=[]
    for ss in itertools.product(range(3),repeat=h+1):
        for aa in itertools.product(range(2),repeat=h):
            pr=INIT_COLL[ss[0]]
            for t in range(h): pr*= (E_COLL[ss[t]] if aa[t] else 1-E_COLL[ss[t]])*P_COLL[aa[t],ss[t],ss[t+1]]
            if pr: states.append(ss); actions.append(aa); probability.append(pr)
    s=np.array(states); a=np.array(actions); prob=np.array(probability); r=REWARD_COLL[s[:,1:]]-12*a
    assert abs(prob.sum()-1)<1e-12
    policy=np.array([0.,1.,1.]); q,v=coll_q(P_COLL,policy,h); truth=float(INIT_COLL@v[0]); rows=[]
    for name,wq,we in [('True Q and logging',False,False),('Zero Q; true logging',True,False),('True Q; wrong logging',False,True),('Both wrong',True,True)]:
        scores,_=coll_scores(s,a,r,P_COLL,policy,wq,we); mean=float(prob@scores['dr'])
        if not (wq and we): assert abs(mean-truth)<1e-10
        rows.append({'specification':name,'expected_score':mean,'truth':truth,'bias':mean-truth})
    score,_=coll_scores(s,a,r,P_COLL,policy)
    wrong=float(prob@score['current_only']); assert abs(wrong-truth)>1
    # Recursively form the value correction independently of the forward sum.
    recursive=np.array([0.,0.,-100.])[s[:,-1]].copy()
    for t in range(h-1,-1,-1):
        num=np.where(a[:,t],policy[s[:,t]],1-policy[s[:,t]])
        den=np.where(a[:,t],E_COLL[s[:,t]],1-E_COLL[s[:,t]])
        recursive=v[t,s[:,t]]+num/den*(r[:,t]+GAMMA*recursive-q[t,s[:,t],a[:,t]])
    err=float(np.max(np.abs(recursive-score['dr']))); assert err<1e-10
    return {'horizon':h,'supported_paths':len(s),'cases':rows,'current_only_expected_value':wrong,'recursive_vs_expanded_max_error':err}


def reducer_repeated_cells():
    sys.path.insert(0,str(ROOT/'src'))
    from causalbank import ScoreReducer
    rng=np.random.default_rng(932)
    entity=np.repeat(np.arange(4),15); date=np.tile(np.repeat(np.arange(5),3),4)
    x=rng.normal(size=(60,2)); x+=rng.normal(size=(4,2))[entity]+rng.normal(size=(5,2))[date]
    centered=x-x.mean(0); reference=np.zeros((2,2))
    for sign,key in [(1,entity),(1,date),(-1,entity*5+date)]:
        labels=np.unique(key); sums=np.array([centered[key==label].sum(0) for label in labels])
        reference+=sign*len(labels)/(len(labels)-1)*(sums.T@sums)/len(x)**2
    chunks=[ScoreReducer(4,5,2) for _ in range(4)]
    for k,c in enumerate(chunks): c.add(x[k::4],entity[k::4],date[k::4])
    for c in chunks[1:]: chunks[0].merge(c)
    got=np.array(chunks[0].result()['covariance']); err=float(np.max(np.abs(got-reference)))
    assert err<1e-13
    return {'rows':60,'repeated_rows_per_intersection':3,'independent_batch_error':err}


def convergence():
    rng=np.random.default_rng(SEED+30)
    hmm_sim(rng,800,12,False)
    o,a=hmm_sim(rng,800,12,True)
    result={}
    for joint in [False,True]:
        theta,diag=hmm_fit(o,a,SEED+33,joint,starts=4,maxiter=2000)
        assert diag['min_likelihood_increment']>=-1e-8
        result['joint' if joint else 'omitted']={'fit':diag,'policy_gain':hmm_reactive_value(theta,[0,0,1])-hmm_reactive_value(theta,[0,0,0]),'parameters':{k:v.tolist() for k,v in theta.items() if joint or k!='q'}}
    return result


def account_checks():
    baseline=30e6; margin=.025; repricing=.0025; cost=1800
    hurdle=(repricing*baseline+12*cost)/(margin-repricing)
    direct=(baseline+hurdle)*(margin-repricing)/12-cost-baseline*margin/12
    assert abs(direct)<1e-8
    econ=json.loads((OUT/'economics.json').read_text())
    threshold=econ['constant_annual_study_threshold']; ann=econ['annuity']
    gap=3+ann*(1.2-.09*threshold); assert abs(gap)<1e-12
    return {'deposit_break_even_additional_usd':hurdle,'deposit_direct_account_residual_usd':direct,'reuse_threshold_cost_gap_usd_million':gap}


def main():
    result={'status':'pass','hmm_enumeration':hmm_check(),'sequential_dr':dr_check(),'financial_accounts':account_checks(),'reducer_repeated_cells':reducer_repeated_cells(),'convergence_followup':convergence(),'scope':'Independent finite-path and financial identities plus same-data longer optimization; not independent scholarly review or general identification/coverage certification'}
    inputs=['tools/revision_studies.py','tools/verify_revision.py','tools/run_data_scale.py','tools/construction_economics.py','docs/derivations/results.json','docs/derivations/environment.json','docs/derivations/data-scale.json','docs/derivations/economics.json','src/causalbank/temporal.py','src/causalbank/scores.py']
    result['input_sha256']={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in inputs}
    (ROOT/'docs/reviews/revision-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='input_sha256'},indent=2))

if __name__=='__main__': main()
