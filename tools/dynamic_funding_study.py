#!/usr/bin/env python3
"""Registered funding study, including direct same-input statsmodels comparison."""
import argparse,hashlib,json,sys,time
from pathlib import Path
import numpy as np
from scipy.stats import norm
from threadpoolctl import threadpool_limits
import statsmodels.api as sm
from statsmodels.stats.sandwich_covariance import cov_hac
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from causalbank.dynamic_funding import FundingTarget,generate,train_pilot,evaluate


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--pilot',action='store_true');args=ap.parse_args()
    path=ROOT/'docs/studies/dynamic-funding-spec.json';spec=json.loads(path.read_text());reps=3 if args.pilot else spec['repetitions']
    target=FundingTarget(horizon=spec['horizon'],branches=spec['branches']); truth=spec['beta']*spec['rho']**np.arange(target.horizon+1)
    financial_truth=float(target.weights()@truth-target.direct_cost());results=[];start=time.perf_counter()
    with threadpool_limits(limits=1):
        for case,n in enumerate(spec['dates']):
            rows=[]
            for rep in range(reps):
                rng=np.random.default_rng(np.random.SeedSequence([spec['seed'],case,rep,0]))
                pilot=generate(spec,n*spec['pilot_multiple'],rng);fit=train_pilot(pilot,spec['penalties'])
                data=generate(spec,n,np.random.default_rng(np.random.SeedSequence([spec['seed'],case,rep,1])))
                bandwidth=int(2*n**.2);out=evaluate(data,fit,target,bandwidth)
                se=np.sqrt(np.diag(out['covariance']));crit=norm.ppf(1-.05/(2*len(truth)))
                fse=np.sqrt(out['financial_variance']);badse=fse/np.sqrt(spec['branches'])
                row={'rep':rep,'estimate':out['estimate'].tolist(),'se':se.tolist(),'penalty':fit['penalty'],'financial_value':out['financial_value'],'financial_se':fse,
                     'covered_marginal':(abs(out['estimate']-truth)<=1.95996398454*se).tolist(),'covered_joint_bonferroni':bool(np.all(abs(out['estimate']-truth)<=crit*se)),
                     'covered_financial':bool(abs(out['financial_value']-financial_truth)<=1.95996398454*fse),
                     'covered_naive_branch_independence':bool(abs(out['financial_value']-financial_truth)<=1.95996398454*badse)}
                if rep==0:
                    errors=[];variance_errors=[]
                    for h in range(len(truth)):
                        direct=sm.OLS(out['residual_outcomes'][:,h],out['residual_action'][:,None]).fit()
                        errors.append(abs(float(direct.params[0])-out['estimate'][h]));variance_errors.append(abs(float(cov_hac(direct,nlags=bandwidth,use_correction=False)[0,0])-out['covariance'][h,h]))
                    row['direct_statsmodels']={'maximum_estimate_error':max(errors),'maximum_variance_error':max(variance_errors),'scientific_work':'same frozen pilot residuals, origins and Bartlett rule'}
                rows.append(row)
            summary={'dates':n,'replications':reps,'marginal_coverage':np.mean([r['covered_marginal'] for r in rows],axis=0).tolist(),'joint_coverage':float(np.mean([r['covered_joint_bonferroni'] for r in rows])),
                     'financial_coverage':float(np.mean([r['covered_financial'] for r in rows])),'naive_branch_coverage':float(np.mean([r['covered_naive_branch_independence'] for r in rows])),
                     'financial_bias':float(np.mean([r['financial_value'] for r in rows])-financial_truth),'bandwidth':int(2*n**.2)}
            results.append({'summary':summary,'runs':rows});print(json.dumps(summary),flush=True)
    files=[path,Path(__file__),ROOT/'src/causalbank/dynamic_funding.py',ROOT/'src/causalbank/responses.py']
    receipt={'mode':'pilot' if args.pilot else 'final','spec':spec,'truth':truth.tolist(),'financial_truth':financial_truth,'results':results,'seconds':time.perf_counter()-start,
             'input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
    (ROOT/'docs/studies'/('dynamic-funding-pilot.json' if args.pilot else 'dynamic-funding-results.json')).write_text(json.dumps(receipt,indent=2)+'\n')


if __name__=='__main__':main()
