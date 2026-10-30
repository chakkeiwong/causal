#!/usr/bin/env python3
import argparse,hashlib,json,sys,time
from pathlib import Path
import numpy as np
from threadpoolctl import threadpool_limits
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from causalbank.dynamic_funding import FundingTarget,generate,train_pilot
from causalbank.linked_observation import interpret_source,mix_candidate_histories,linked_response


def make_linked(base,spec,n,seed):
    first=generate(base,n,np.random.default_rng(seed));alternative=dict(base,beta=spec['decoy_beta'])
    second=generate(alternative,n,np.random.default_rng(seed))
    links=np.random.default_rng(np.random.SeedSequence([*seed,91]))
    return mix_candidate_histories(first,second,links,spec['correct_pair_probability'])


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--pilot',action='store_true');args=ap.parse_args()
    path=ROOT/'docs/studies/dynamic-observation-spec.json';spec=json.loads(path.read_text());basepath=ROOT/spec['funding_spec'];base=json.loads(basepath.read_text());target=FundingTarget(horizon=base['horizon'],branches=base['branches'])
    truth=base['beta']*base['rho']**np.arange(target.horizon+1);ftruth=float(target.weights()@truth-target.direct_cost());start=time.perf_counter();results=[]
    fixtures_path=ROOT/'docs/studies/observation-fixtures-v6.json';fixtures=json.loads(fixtures_path.read_text());interpretations=[]
    for fixture in fixtures['cases']:
        result=interpret_source(fixture);accepted=result['status']=='conditional_acceptance'
        interpretations.append({'case':fixture['id'],'result':result,'wrong_acceptance':accepted and result['candidates'][0]['balance']!=fixture['evaluation_truth']})
    with threadpool_limits(limits=1):
        for case,m in enumerate(spec['audit_per_stratum']):
            rows=[]
            for rep in range(3 if args.pilot else spec['repetitions']):
                pilot=make_linked(base,spec,spec['pilot_dates'],[spec['seed'],case,rep,0]);pfit=train_pilot(pilot,base['penalties'])
                data=make_linked(base,spec,spec['dates'],[spec['seed'],case,rep,1]);rng=np.random.default_rng(np.random.SeedSequence([spec['seed'],case,rep,2]));audit=rng.binomial(m,spec['correct_pair_probability'])
                out=linked_response(data,pfit,audit,[m,m],target,int(2*spec['dates']**.2),spec['stratum_weights'])
                row={'rep':rep,'status':out['status'],'audit_success':audit.tolist()}
                if out['status']=='computed':
                    v=out['financial_value'];se=out['financial_se'];fixed=out['financial_fixed_calibration_se'];naive=out['naive_financial_value'];nse=out['naive_financial_se']
                    # A biased audit is kept distinct from the correct independent audit.
                    biased=linked_response(data,pfit,np.array([.98,.95])*m,[m,m],target,int(2*spec['dates']**.2),spec['stratum_weights'])
                    row.update(estimate=out['estimate'].tolist(),financial=v,se=se,fixed_calibration_se=fixed,naive_financial=naive,naive_se=nse,
                               coverage_joint=abs(v-ftruth)<=1.95996398454*se,coverage_fixed=abs(v-ftruth)<=1.95996398454*fixed,
                               coverage_naive=abs(naive-ftruth)<=1.95996398454*nse,biased_audit_financial=biased['financial_value'],
                               coverage_biased_audit=abs(biased['financial_value']-ftruth)<=1.95996398454*biased['financial_se'])
                rows.append(row)
            valid=[r for r in rows if r['status']=='computed'];summary={'audit_rows_per_stratum':m,'requested':len(rows),'available':len(valid),
                **{k:sum(r.get(k,False) for r in rows)/len(rows) for k in ('coverage_joint','coverage_fixed','coverage_naive','coverage_biased_audit')},
                'bias_available':float(np.mean([r['financial'] for r in valid])-ftruth),'naive_bias':float(np.mean([r['naive_financial'] for r in valid])-ftruth),
                'mean_joint_se':float(np.mean([r['se'] for r in valid])),'mean_fixed_calibration_se':float(np.mean([r['fixed_calibration_se'] for r in valid]))}
            results.append({'summary':summary,'runs':rows});print(json.dumps(summary),flush=True)
    # Indeterminate mixing cannot be turned into a single map by regularizing the denominator.
    rank=linked_response(data,pfit,[50,50],[100,100],target,int(2*spec['dates']**.2))
    files=[path,basepath,fixtures_path,Path(__file__),ROOT/'src/causalbank/dynamic_funding.py',ROOT/'src/causalbank/linked_observation.py',ROOT/'src/causalbank/responses.py']
    result={'mode':'pilot' if args.pilot else 'final','spec':spec,'financial_truth':ftruth,'fixtures':interpretations,'rank_failure':rank['status'],'results':results,'seconds':time.perf_counter()-start,
            'input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
    (ROOT/'docs/studies'/('dynamic-observation-pilot.json' if args.pilot else 'dynamic-observation-results.json')).write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':main()
