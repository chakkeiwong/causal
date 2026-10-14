#!/usr/bin/env python3
import argparse
import json
import time
import numpy as np
from threadpoolctl import threadpool_limits
from closure_common import ROOT,save,coverage
from causalbank.nonlinear_audited import TRUTH,simulate,fit,engine
from causalbank.nonlinear_stability import fit_stable


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--pilot',action='store_true');args=ap.parse_args()
    spec=json.loads((ROOT/'docs/studies/closure-nonlinear-followup-spec.json').read_text());old=json.loads((ROOT/'docs/studies/closure-nonlinear-results.json').read_text())
    policy=np.array(old['planning']['selected_policy']);truth=float(engine(121,9.)['value'](TRUTH,policy));seed=spec['pilot_seed'] if args.pilot else spec['seed'];reps=spec['pilot_repetitions'] if args.pilot else spec['repetitions'];start=time.perf_counter();cases=[]
    with threadpool_limits(limits=1):
        for ci,n in enumerate(spec['audit_sizes']):
            rows=[]
            for rep in range(reps):
                main,_=simulate(TRUTH,spec['main_size'],3,np.random.default_rng([seed,ci,rep,0]));audit,states=simulate(TRUTH,n,3,np.random.default_rng([seed,ci,rep,1]))
                methods={'original_rectangle':fit(main,audit,states,policy),'stable_diamond':fit_stable(main,audit,states,policy)}
                rows.append(dict(rep=rep,methods=methods))
                if (rep+1)%20==0:print(json.dumps({'audit_size':n,'completed':rep+1}),flush=True)
            summary={}
            for method in spec['methods']:
                valid=[r['methods'][method] for r in rows if r['methods'][method]['status']=='computed'];covered=sum(r['interval'][0]<=truth<=r['interval'][1] for r in valid)
                summary[method]=dict(available=len(valid),coverage_all=coverage(covered,reps),coverage_given_available=coverage(covered,len(valid)) if valid else None,
                                     bias_given_available=float(np.mean([r['value'] for r in valid])-truth) if valid else None,
                                     mean_se=float(np.mean([r['standard_error'] for r in valid])) if valid else None)
            cases.append(dict(audit_size=n,summary=summary,runs=rows));print(json.dumps({'audit_size':n,'summary':summary}),flush=True)
    output=dict(mode='pilot' if args.pilot else 'final',spec=spec,frozen_policy=policy,truth=truth,results=cases,seconds=time.perf_counter()-start,
                scope='Fresh registered domain and information follow-up. Original failures remain recorded; no outcome-selected switching or claim of uniform coverage.')
    save('docs/studies/closure-nonlinear-followup-'+('pilot' if args.pilot else 'results')+'.json',output,
         ['tools/closure_nonlinear_followup.py','tools/closure_common.py','src/causalbank/nonlinear_stability.py','src/causalbank/nonlinear_audited.py','docs/studies/closure-nonlinear-followup-spec.json','docs/studies/closure-nonlinear-results.json'])


if __name__=='__main__':main()
