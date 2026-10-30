#!/usr/bin/env python3
"""One fresh registered finite-window follow-up; original failures remain."""
import json
import time
import numpy as np
from threadpoolctl import threadpool_limits
from reliability_common import ROOT,Journal,SPEC,summarize
from reliability_joint_study import sample
from reliability_learning_study import data,request
from causalbank.joint_audited import joint_effect
from causalbank.chunked_learning import fit_chunked
from causalbank.blocked_learning import blocked_covariance

def main():
    follow='docs/studies/reliability-followup-spec.json';f=json.loads((ROOT/follow).read_text());s=json.loads((ROOT/SPEC).read_text());start=time.perf_counter()
    inputs=[follow,'tools/reliability_followup_study.py','tools/reliability_joint_study.py','tools/reliability_learning_study.py','src/causalbank/joint_audited.py','src/causalbank/chunked_learning.py','src/causalbank/blocked_learning.py','tools/study_response_extensions.py']
    journal=Journal('followup',inputs);results=[]
    with threadpool_limits(limits=1):
        js=dict(s['joint'],pairs=f['joint']['pairs'],dates=f['joint']['dates'])
        def joint(i):
            a,y,r,label,q,gold,g=sample(js,np.random.default_rng([f['seed'],1,i]));methods={}
            for multiplier in f['joint']['windows']:
                methods[f'window_{multiplier}']=joint_effect(a,y,r,label,q,bandwidth=int(multiplier*js['dates']**.25),gold_errors=gold,scale=js['monetary_scale'])
            return dict(methods=methods)
        rows=[journal.run(f'joint/{i}',lambda i=i:joint(i)) for i in range(f['joint']['repetitions'])]
        results.append(dict(case='joint_larger',pairs=js['pairs'],dates=js['dates'],summary=summarize(rows,js['beta']*js['monetary_scale'])))
        ls=dict(s['learning'],n=f['learning']['n'])
        def learning(i):
            c,y=data(ls,np.random.default_rng([f['seed'],2,i]));fit=fit_chunked(request(ls),c,y,chunk_rows=ls['chunk_rows']);methods={}
            for multiplier in f['learning']['windows']:
                band=int(multiplier*len(fit['scores'])**.2);var=blocked_covariance(fit['scores'],fit['folds'],band)/(len(fit['scores'])*fit['denominator']**2);se=float(np.sqrt(var));point=fit['estimate']
                methods[f'window_{multiplier}']=dict(status='computed',estimate=point,standard_error=se,interval=[point-1.96*se,point+1.96*se],bandwidth=band,
                    inference=dict(fit['inference'],numerical_status='Same frozen fitting algorithm, separately registered longer Bartlett window; no gap-crossing lag pairs'))
            return dict(methods=methods)
        rows=[journal.run(f'learning/{i}',lambda i=i:learning(i)) for i in range(f['learning']['repetitions'])]
        results.append(dict(case='learning_larger',n=ls['n'],summary=summarize(rows,1.2)))
    journal.finish(dict(results=results,seconds=time.perf_counter()-start,scope='Fresh registered follow-up; sample size and window change jointly across original/follow-up designs. Matched windows within the follow-up identify a covariance-window contribution, not universal calibration.'))

if __name__=='__main__':main()
