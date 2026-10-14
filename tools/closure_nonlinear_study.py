#!/usr/bin/env python3
"""Executed nonlinear likelihood, score, value, uncertainty and challengers."""
import argparse
import itertools
import json
import time
import numpy as np
from threadpoolctl import threadpool_limits
from closure_common import ROOT,save,coverage
from causalbank.nonlinear_audited import (TRUTH,BOUNDS,simulate,fit,engine,audit_start,choose_policy,
    gaussian_loglik,particle_loglik,simulate_policy_value,gaussian_policy_value)


def numerical_checks(seed):
    data,_=simulate(TRUTH,8,3,np.random.default_rng([seed,30,0]));policy=np.array([0.,0.,0.]);p=TRUTH
    ref=engine(121,9.);ref_ll=float(np.sum(ref['observed'](p,data)));ref_score=np.asarray(ref['observed_gradient'](p,data));ref_value=float(ref['value'](p,policy))
    rows=[]
    for nodes,limit in [(41,7.),(61,7.),(81,7.),(121,7.),(121,9.)]:
        e=engine(nodes,limit)
        rows.append(dict(nodes=nodes,limit=limit,loglik=float(np.sum(e['observed'](p,data))),
                         loglik_error=float(np.sum(e['observed'](p,data)))-ref_ll,
                         score_max_error=float(np.max(abs(np.asarray(e['observed_gradient'](p,data))-ref_score))),
                         value=float(e['value'](p,policy)),value_error_currency=1000*(float(e['value'](p,policy))-ref_value)))
    numeric=[];gscore=[]
    for j in range(15):
        delta=np.eye(15)[j]*1e-5
        numeric.append((float(np.sum(ref['observed'](p+delta,data)))-float(np.sum(ref['observed'](p-delta,data))))/(2e-5))
        gscore.append((gaussian_loglik(p+delta,data).sum()-gaussian_loglik(p-delta,data).sum())/(2e-5))
    reduced=p.copy();reduced[1]=0;reduced[6]=0
    reduced_data,_=simulate(reduced,10,4,np.random.default_rng([seed,30,1]))
    exact_error=float(np.max(abs(np.asarray(ref['observed'](reduced,reduced_data))-gaussian_loglik(reduced,reduced_data))))
    direction=np.arange(1,16,dtype=float);direction/=np.linalg.norm(direction);step=.05
    ref_difference=(float(np.sum(ref['observed'](p+step*direction,data)))-float(np.sum(ref['observed'](p-step*direction,data))))/(2*step)
    particles=[]
    for count in (512,4096):
        estimates=[];derivatives=[]
        for repeat in range(8):
            rngseed=seed+100*count+repeat
            estimates.append(float(particle_loglik(p,data,count,rngseed).sum()))
            derivatives.append(float((particle_loglik(p+step*direction,data,count,rngseed).sum()-particle_loglik(p-step*direction,data,count,rngseed).sum())/(2*step)))
        particles.append(dict(particles=count,loglik_errors=np.array(estimates)-ref_ll,
                              finite_difference_errors=np.array(derivatives)-ref_difference,
                              qualification='Monte Carlo challenger with coupled finite differences, not a certified derivative of a resampling path'))
    sim,se=simulate_policy_value(p,policy,200000,[seed,30,2])
    gvalue=gaussian_policy_value(p,policy)
    checks={'score_matches_finite_differences':bool(np.max(abs(ref_score-numeric))<1e-5),
            'gaussian_limit_both_restrictions':exact_error<1e-6,
            'registered_grid_likelihood':abs(rows[1]['loglik_error'])<1e-4,
            'registered_grid_score':rows[1]['score_max_error']<1e-3,
            'registered_grid_value_currency':abs(rows[1]['value_error_currency'])<.1,
            'independent_value_simulation':abs(sim-ref_value)<4*se}
    return dict(checks=checks,grid_comparison=rows,exact_gaussian_error=exact_error,
                score_central_difference_error=float(np.max(abs(ref_score-numeric))),
                gaussian_challenger=dict(loglik_error=float(gaussian_loglik(p,data).sum()-ref_ll),score_max_error=float(np.max(abs(ref_score-gscore))),value_error_currency=1000*(gvalue-ref_value)),
                particle_challenger=particles,independent_value=dict(reference=ref_value,simulation=sim,mc_se=se))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--pilot',action='store_true');args=ap.parse_args()
    whole=json.loads((ROOT/'docs/studies/closure-spec.json').read_text());spec=whole['nonlinear'];seed=whole['pilot_seed'] if args.pilot else whole['final_seed']
    start=time.perf_counter();results=[]
    # Training is independent of every evaluation/audit draw and frozen once.
    pilotdata,pilotstates=simulate(TRUTH,800,3,np.random.default_rng([seed,31,0]));pilot_parameters=audit_start(pilotdata,pilotstates)
    policy,planning=choose_policy(pilot_parameters,3)
    library=list(itertools.product([-1.,0.,1.,8.],repeat=3));approx_values=[gaussian_policy_value(pilot_parameters,p) for p in library]
    approximate_policy=np.array(library[int(np.argmax(approx_values))]);ref=engine(121,9.)
    planning.update(selected_policy=policy,approximate_policy=approximate_policy,
                    approximate_planning_loss=float(ref['value'](pilot_parameters,policy)-ref['value'](pilot_parameters,approximate_policy)),
                    training_parameters=pilot_parameters,training_trajectories=800)
    with threadpool_limits(limits=1):
        numerical=numerical_checks(seed)
        if not all(numerical['checks'].values()):
            save('docs/studies/closure-nonlinear-numerical-failure.json',numerical,['tools/closure_nonlinear_study.py','src/causalbank/nonlinear_audited.py'])
            raise SystemExit('Numerical pilot gate failed; retained details require repair before final inference')
        first=None
        cases=['baseline','weak_measurement','scarce_actions','biased_audit','longer_horizon','misspecification']
        for ci,name in enumerate(cases):
            truth=TRUTH.copy();h=3
            if name=='weak_measurement':truth[4]=np.log(3.)
            if name=='scarce_actions':truth[5]=-3.5
            if name=='longer_horizon':h=6
            fixed_policy=np.resize(policy,h)
            true_value=float(ref['value'](truth,fixed_policy));truth_error=0.
            if name=='misspecification':true_value,truth_error=simulate_policy_value(truth,fixed_policy,1000000,[seed,32,ci],misspecification=True)
            reps=spec['pilot_repetitions'] if args.pilot else (spec['repetitions'] if name=='baseline' else 25)
            rows=[]
            for rep in range(reps):
                main,_=simulate(truth,spec['main_trajectories'],h,np.random.default_rng([seed,33,ci,rep,0]),misspecification=name=='misspecification')
                audit,states=simulate(truth,spec['audit_trajectories'],h,np.random.default_rng([seed,33,ci,rep,1]),misspecification=name=='misspecification')
                if name=='biased_audit':states=states+.4
                fitted=fit(main,audit,states,fixed_policy,nodes=spec['grid_nodes'],limit=spec['grid_limit'])
                fitted['rep']=rep
                if 'interval' in fitted:
                    e=engine(81,9.);coarse=engine(spec['grid_nodes'],spec['grid_limit']);params=fitted['parameters']
                    fitted['refined_value_difference_currency']=1000*(float(e['value'](params,fixed_policy))-fitted['value'])
                    fitted['refined_loglik_difference']=float(np.sum(e['observed'](params,main))-np.sum(coarse['observed'](params,main)))
                    fitted['refined_score_max_difference']=float(np.max(abs(np.asarray(e['observed_gradient'](params,main))-np.asarray(coarse['observed_gradient'](params,main)))))
                    if abs(fitted['refined_value_difference_currency'])>.1 or abs(fitted['refined_loglik_difference'])>1e-4 or fitted['refined_score_max_difference']>1e-3:
                        fitted['status']='unqualified_numerics';fitted['withheld_interval']=fitted.pop('interval')
                    fitted['covers']=bool(fitted['status']=='computed' and fitted['interval'][0]<=true_value<=fitted['interval'][1])
                if name=='baseline' and rep==0:first=(main,audit,states,fitted,fixed_policy)
                rows.append(fitted)
                if (rep+1)%20==0:print(json.dumps({'case':name,'completed':rep+1}),flush=True)
            good=[r for r in rows if r['status']=='computed'];covered=sum(r.get('covers',False) for r in rows)
            summary=dict(requested=reps,available=len(good),coverage_all=coverage(covered,reps),
                         coverage_given_available=coverage(covered,len(good)) if good else None,
                         boundary_fits=sum(r['boundary'] for r in rows),
                         bias_given_available=float(np.mean([r['value'] for r in good])-true_value) if good else None,
                         mean_se=float(np.mean([r['standard_error'] for r in good])) if good else None,
                         max_start_objective_spread=max(r['local_mode_objective_spread'] for r in rows))
            results.append(dict(case=name,truth=true_value,truth_mc_se=truth_error,summary=summary,runs=rows))
            print(json.dumps({'case':name,'summary':summary}),flush=True)
        bootstrap=[]
        if not args.pilot:
            main,audit,states,fitted,policy0=first
            for rep in range(spec['bootstrap_refits']):
                rng=np.random.default_rng([seed,34,rep]);mi=rng.integers(len(main),size=len(main));ai=rng.integers(len(audit),size=len(audit))
                result=fit(main[mi],audit[ai],states[ai],policy0,nodes=spec['grid_nodes'],starts=1,initial=fitted['parameters'],uncertainty=False)
                bootstrap.append(dict(rep=rep,status=result['status'],value=result['value'],boundary=result['boundary']))
    output=dict(mode='pilot' if args.pilot else 'final',planning=planning,numerical=numerical,results=results,bootstrap_refits=bootstrap,
                bootstrap_scope='Independent resampling within each whole-trajectory sample; fixed policy. Forty refits are a diagnostic, not precise tail calibration.',
                seconds=time.perf_counter()-start,
                qualification='Bounded identified reference and conditional policy research inference. Boundary or unreliable fits are unavailable; adverse cases are not promoted by successful optimization.')
    save('docs/studies/closure-nonlinear-'+('pilot' if args.pilot else 'results')+'.json',output,
         ['tools/closure_nonlinear_study.py','tools/closure_common.py','src/causalbank/nonlinear_audited.py','docs/studies/closure-spec.json'])


if __name__=='__main__':main()
