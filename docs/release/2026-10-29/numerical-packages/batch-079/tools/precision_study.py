#!/usr/bin/env python3
"""Registered fixed-procedure fresh grid; each completed request is journaled."""
import argparse
import json
import numpy as np
from threadpoolctl import threadpool_limits
from precision_common import ROOT, SPEC, Journal, summary
from causalbank.dynamic_funding import FundingTarget
from causalbank.funding_calibration import simulate_rows, fit_funding, DECLARATIONS
from causalbank.streaming_pilot import fit_streaming_pilot


def main(pilot):
    spec=json.loads((ROOT/SPEC).read_text())
    base=json.loads((ROOT/spec['base']).read_text())
    observation=json.loads((ROOT/spec['observation']).read_text())
    target=FundingTarget(horizon=base['horizon'],branches=base['branches'])
    seed=spec['pilot_seed'] if pilot else spec['seed']
    reps=spec['pilot_repetitions'] if pilot else spec['repetitions']
    journal=Journal('pilot' if pilot else 'final',['tools/precision_study.py'])
    results=[]
    for ci,design in enumerate(spec['designs']):
        law=dict(base,rho=design.get('rho',base['rho']))
        obs=dict(observation,correct_pair_probability=design['probability'])
        n=design['dates']; correlation=design.get('innovation_correlation',0.)
        truth=float(target.weights()@(base['beta']*law['rho']**np.arange(target.horizon+1))-target.direct_cost())
        def one(i):
            data=simulate_rows(law,obs,n,[seed,ci,i,1],correlation)
            prior=simulate_rows(law,obs,8*n,[seed,ci,i,2],correlation)
            counts=np.random.default_rng([seed,ci,i,3]).binomial(design['audit'],design['probability'])
            sizes=[design['audit']]*2
            methods={'joint_horizon':fit_funding(data,target,counts,sizes,declarations=DECLARATIONS)}
            for multiple in spec['pilot_multipliers']:
                result=fit_streaming_pilot(prior[:multiple*n],data,target,counts,sizes,base['penalties'],chunk_size=spec['chunk_size'],declarations=DECLARATIONS)
                result.pop('coefficient',None)
                methods[f'pilot{multiple}_horizon']=result
            return dict(methods=methods,audit_successes=counts,pilot_dates=[4*n,8*n])
        rows=[journal.run(f'{design["name"]}/{i}',lambda i=i:one(i)) for i in range(reps)]
        result=dict(design=design,truth=truth,summary=summary(rows,truth))
        results.append(result)
        print(json.dumps(dict(design=design['name'],requests=reps,coverage={k:v['coverage_all'] for k,v in result['summary']['methods'].items()})),flush=True)
    journal.finish(dict(status='pass',mode='pilot' if pilot else 'final',repetitions=reps,results=results,scope='Fixed selected synthetic laws and procedures; statistical shortfalls are retained, not a gate failure. Availability and paired comparisons remain separate from coverage compatibility.'))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--pilot',action='store_true')
    with threadpool_limits(limits=1): main(parser.parse_args().pilot)
