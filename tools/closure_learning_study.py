#!/usr/bin/env python3
import argparse
from dataclasses import replace
import json
import time
import numpy as np
from threadpoolctl import threadpool_limits
from closure_common import ROOT,save,coverage
from causalbank.blocked_learning import BlockedIVRequest,fit_blocked
from study_response_extensions import learning_sample


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--pilot',action='store_true');args=ap.parse_args()
    whole=json.loads((ROOT/'docs/studies/closure-spec.json').read_text());spec=whole['learning'];seed=whole['pilot_seed'] if args.pilot else whole['final_seed'];reps=spec['pilot_repetitions'] if args.pilot else spec['repetitions'];start=time.perf_counter()
    request=BlockedIVRequest('sparse_lasso',spec['gap'],.4,penalty_multiplier=spec['penalty_multiplier']);results=[]
    with threadpool_limits(limits=1):
        for ci,case in enumerate(('sparse_linear','omitted_nonlinearity')):
            runs=[]
            for rep in range(reps):
                data=learning_sample(spec,np.random.default_rng([seed,40,ci,rep]));c,y,d,z,oracle=data
                if case=='omitted_nonlinearity':
                    # Both instrument mean and outcome mean omit an interaction,
                    # making the orthogonality product remainder non-negligible.
                    interaction=1.3*c[:,0]*c[:,1];z=z+interaction;y=y+interaction
                    oracle=oracle.copy();oracle[:,0]+=interaction;oracle[:,2]+=interaction
                methods={}
                for learner in ('sparse_lasso','fixed_basis','intercept_challenger','oracle'):
                    result=fit_blocked(replace(request,learner='fixed_basis' if learner=='oracle' else learner),c,y,d,z,oracle_predictions=oracle if learner=='oracle' else None)
                    methods[learner]={k:result[k] for k in ('status','estimate','standard_error','interval','denominator')}
                runs.append(dict(rep=rep,methods=methods))
            summary={}
            for method in runs[0]['methods']:
                rows=[r['methods'][method] for r in runs]
                summary[method]=dict(coverage=coverage(sum(r['interval'][0]<=1.2<=r['interval'][1] for r in rows),reps),
                                     bias=float(np.mean([r['estimate'] for r in rows])-1.2),mean_se=float(np.mean([r['standard_error'] for r in rows])))
            results.append(dict(case=case,truth=1.2,summary=summary,runs=runs));print(json.dumps({'case':case,'summary':summary}),flush=True)
        checks={}
        for name,change in [('late_features',dict(feature_available_after_origin=True)),('insufficient_gap',dict(gap=1)),('arbitrary_learner',dict(learner='user_object')),('persistent_pair_composition',dict(sampling='independent_pairs'))]:
            try:fit_blocked(replace(request,**change),c,y,d,z);checks[name]=False
            except ValueError:checks[name]=True
    output=dict(mode='pilot' if args.pilot else 'final',results=results,rejection_checks=checks,seconds=time.perf_counter()-start,
                scope='Fixed bounded sparse toy law with supplied mixing/rate conditions; misspecification remains adverse, no arbitrary learner guarantee.')
    save('docs/studies/closure-learning-'+('pilot' if args.pilot else 'results')+'.json',output,
         ['tools/closure_learning_study.py','tools/study_response_extensions.py','tools/closure_common.py','src/causalbank/blocked_learning.py','docs/studies/closure-spec.json'])
    raise SystemExit(not all(checks.values()))


if __name__=='__main__':main()
