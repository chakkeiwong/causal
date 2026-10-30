#!/usr/bin/env python3
import argparse
import json
import time
import numpy as np
from scipy.stats import norm
from scipy.special import expit
from threadpoolctl import threadpool_limits
from reliability_common import ROOT,Journal,SPEC,summarize
from causalbank.nonlinear_variance import TRUTH,simulate,fit,engine,policy_simulation
from causalbank.nonlinear_audited import engine as old_engine,EPSILON
from causalbank.nonlinear_stability import fit_stable


def numerical(seed,policy,s):
    p=TRUTH;data,states=simulate(p,8,3,np.random.default_rng([seed,71,0]));e=engine(s['nodes'],s['limit']);ref=engine(s['refined_nodes'],s['refined_limit'])
    score=np.asarray(ref['observed_gradient'](p,data));numeric=[]
    for j in range(16):
        delta=np.eye(16)[j]*1e-5;numeric.append((float(np.sum(ref['observed'](p+delta,data)))-float(np.sum(ref['observed'](p-delta,data))))/2e-5)
    o,a,r=data[:,:,0],data[:,:,1],data[:,:,2];prob=EPSILON+(1-2*EPSILON)*expit(p[5]+p[6]*states+p[7]*o)
    direct=norm.logpdf(states[:,0],p[13],np.sqrt(np.exp(p[14])))+np.sum(norm.logpdf(o,states,np.sqrt(np.exp(p[4])))+np.where(a==1,np.log(prob),np.log1p(-prob))+norm.logpdf(r,p[8]+p[9]*states+p[10]*a+p[11]*states*a,np.sqrt(np.exp(p[12]))),axis=1)
    means=p[0]*states[:,:-1]+p[1]*np.tanh(states[:,:-1])+p[2]*a[:,:-1];q=np.exp(p[3])*(1-a[:,:-1])+np.exp(p[15])*a[:,:-1]
    direct+=np.sum(norm.logpdf(states[:,1:],means,np.sqrt(q)),axis=1)
    equal=p.copy();equal[15]=equal[3];old=old_engine(s['refined_nodes'],s['refined_limit'])
    equal_ll=float(np.max(abs(np.asarray(ref['observed'](equal,data))-np.asarray(old['observed'](equal[:15],data)))))
    equal_value=float(abs(float(ref['value'](equal,policy))-float(old['value'](equal[:15],policy))))
    llerror=float(abs(np.sum(e['observed'](p,data))-np.sum(ref['observed'](p,data))));scoreerror=float(np.max(abs(np.asarray(e['observed_gradient'](p,data))-score)));valueerror=1000*abs(float(e['value'](p,policy))-float(ref['value'](p,policy)))
    sim,se=policy_simulation(p,policy,200000,[seed,71,1]);truth=float(ref['value'](p,policy))
    checks=dict(all16_scores=float(np.max(abs(score-numeric)))<1e-5,independent_labelled_likelihood=float(np.max(abs(np.asarray(ref['labelled'](p,data,states))-direct)))<1e-10,
                equal_variance_reduction=equal_ll<1e-10 and equal_value<1e-10,grid_likelihood=llerror<s['likelihood_tolerance'],grid_score=scoreerror<s['score_tolerance'],grid_value=valueerror<s['value_tolerance_currency'],independent_value=abs(sim-truth)<4*se)
    return dict(checks=checks,score_difference=float(np.max(abs(score-numeric))),grid_loglik_error=llerror,grid_score_error=scoreerror,grid_value_error_currency=valueerror,equal_variance_loglik_error=equal_ll,simulation=sim,simulation_se=se,reference_value=truth)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--pilot',action='store_true');args=ap.parse_args();all_s=json.loads((ROOT/SPEC).read_text());s=all_s['nonlinear'];seed=all_s['pilot_seed'] if args.pilot else all_s['final_seed'];reps=all_s['pilot_repetitions'] if args.pilot else s['repetitions'];policy=np.asarray(json.loads((ROOT/s['policy_source']).read_text())['planning']['selected_policy']);start=time.perf_counter()
    journal=Journal('nonlinear',['tools/reliability_nonlinear_study.py','src/causalbank/nonlinear_variance.py','src/causalbank/nonlinear_audited.py','src/causalbank/nonlinear_stability.py',s['policy_source']],args.pilot)
    results=[]
    with threadpool_limits(limits=1):
        num=journal.run('numerical',lambda:numerical(all_s['pilot_seed'],policy,s));assert all(num['checks'].values()),num
        truths=journal.run('truths',lambda:dict(correct=float(engine(s['refined_nodes'],s['refined_limit'])['value'](TRUTH,policy))*1000,misspecified=policy_simulation(TRUTH,policy,1000000,[all_s['pilot_seed'],72,0],misspecification=True)))
        for ci,miss in enumerate((False,True)):
            name='action_variance' if not miss else 'omitted_transition';truth=truths['correct'] if not miss else 1000*truths['misspecified'][0]
            def run(i):
                main,_=simulate(TRUTH,s['main_trajectories'],s['horizon'],np.random.default_rng([seed,73,ci,i,0]),misspecification=miss)
                audit,states=simulate(TRUTH,s['audit_trajectories'],s['horizon'],np.random.default_rng([seed,73,ci,i,1]),misspecification=miss)
                new=fit(main,audit,states,policy,nodes=s['nodes'],limit=s['limit'],refined_nodes=s['refined_nodes'],refined_limit=s['refined_limit'],tolerances=(s['likelihood_tolerance'],s['score_tolerance'],s['value_tolerance_currency']))
                old=fit_stable(main,audit,states,policy);old['estimate']=1000*old['value']
                if 'interval' in old:old['interval']=[1000*x for x in old['interval']]
                if 'standard_error' in old:old['standard_error']*=1000
                return dict(methods=dict(heterogeneous_variance=new,homogeneous_challenger=old),audited_action_counts=[int(np.sum(audit[:,:-1,1]==a)) for a in (0,1)])
            rows=[journal.run(f'{name}/{i}',lambda i=i:run(i)) for i in range(reps)]
            results.append(dict(case=name,truth_currency=truth,truth_mcse_currency=0. if not miss else 1000*truths['misspecified'][1],summary=summarize(rows,truth)))
            print(json.dumps({'case':name,'primary':results[-1]['summary']['heterogeneous_variance']}),flush=True)
    journal.finish(dict(mode='pilot' if args.pilot else 'final',numerical=num,frozen_policy=policy,results=results,seconds=time.perf_counter()-start,
                        scope='Audited selected16 model; fixed independently trained observable policy. Both action-specific variances need accurate representative transition audits. No general nonlinear identification, full belief-policy optimality or uniform calibration claim.'))


if __name__=='__main__':main()
