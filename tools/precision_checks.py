#!/usr/bin/env python3
"""Independent dense tuning/inference checks for the streaming pilot."""
import json
import numpy as np
from threadpoolctl import threadpool_limits
from precision_common import ROOT, SCIENCE_INPUTS, save
from causalbank.dynamic_funding import FundingTarget, train_pilot
from causalbank.funding_calibration import simulate_rows, pilot_data, DECLARATIONS
from causalbank.funding_pilot_rates import fit_growing_pilot
from causalbank.streaming_pilot import fit_streaming_pilot, train_streaming_pilot


def main():
    base=json.loads((ROOT/'docs/studies/dynamic-funding-spec.json').read_text())
    obs=json.loads((ROOT/'docs/studies/dynamic-observation-spec.json').read_text())
    worst=0.; cases=0; checks={}
    def close(a,b):
        nonlocal worst
        a,b=np.asarray(a),np.asarray(b)
        error=float(np.max(np.abs(a-b)/np.maximum(1,np.abs(a))))
        worst=max(worst,error)
        assert np.allclose(a,b,rtol=1e-9,atol=1e-9), error
    for h,n in ((0,73),(6,241),(6,720)):
        law=dict(base,horizon=h)
        target=FundingTarget(horizon=h)
        data=simulate_rows(law,obs,n,[10102111,n])
        prior=simulate_rows(law,obs,4*n+1,[10102113,n])
        original=train_pilot(pilot_data(prior),base['penalties'])
        for block in (1,5,37,4096):
            trained=train_streaming_pilot(prior,base['penalties'],block)
            assert trained['penalty']==original['penalty']
            close(original['coefficient'],trained['coefficient'])
            close(original['validation_losses'],trained['validation_losses'])
            for covariance in ('innovation_horizon','bartlett'):
                dense=fit_growing_pilot(prior,data,target,[950,800],[1000,1000],base['penalties'],covariance=covariance,declarations=DECLARATIONS)
                streamed=fit_streaming_pilot(prior,data,target,[950,800],[1000,1000],base['penalties'],chunk_size=block,covariance=covariance,declarations=DECLARATIONS)
                assert dense['status']==streamed['status'] and dense['qualifications']==streamed['qualifications']
                assert dense['pilot_penalty']==streamed['pilot_penalty']
                for key in ('estimate','response_estimates','calendar_variance','audit_variance','standard_error','interval','coefficient'):
                    if key in dense: close(dense[key],streamed[key])
                cases+=1
    checks['chronological_tuning_refit_dense_equivalence']=True
    checks['financial_and_both_covariances_awkward_blocks']=True
    repeated=train_streaming_pilot(prior,[10.,10.],5)
    reference=train_pilot(pilot_data(prior),[10.,10.])
    assert repeated['penalty']==reference['penalty'] and repeated['validation_losses'][0]==repeated['validation_losses'][1]
    checks['identical_penalty_first_tie']=True
    for counts,status in (([500,800],'unavailable_mapping_rank'),([1000,800],'unavailable_audit_boundary')):
        result=fit_streaming_pilot(prior,data,target,counts,[1000,1000],base['penalties'],declarations=DECLARATIONS)
        assert result['status']==status and 'interval' not in result
    checks['audit_refusals']=True
    invalid=[]
    def reject(label,call):
        try: call()
        except ValueError: invalid.append(label)
        else: raise AssertionError(label)
    args=[prior,data,target,[950,800],[1000,1000],base['penalties']]
    reject('short_pilot',lambda:fit_streaming_pilot(prior[:10],*args[1:],declarations=DECLARATIONS))
    reject('declarations',lambda:fit_streaming_pilot(*args))
    reject('chunk_zero',lambda:fit_streaming_pilot(*args,chunk_size=0,declarations=DECLARATIONS))
    reject('chunk_boolean',lambda:fit_streaming_pilot(*args,chunk_size=True,declarations=DECLARATIONS))
    reject('invalid_count',lambda:fit_streaming_pilot(prior,data,target,[1001,800],[1000,1000],base['penalties'],declarations=DECLARATIONS))
    corrupted=prior.copy();corrupted[3,4]=np.nan
    reject('nonfinite_pilot',lambda:train_streaming_pilot(corrupted,base['penalties']))
    corrupted=prior.copy();corrupted[:,0]=0
    reject('rank',lambda:train_streaming_pilot(corrupted,base['penalties']))
    corrupted=prior.copy();corrupted[:,1]=1
    reject('zero_target_scale',lambda:train_streaming_pilot(corrupted,base['penalties']))
    reject('negative_penalty',lambda:train_streaming_pilot(prior,[-1.]))
    checks['invalid_requests']=len(invalid)==9
    save('docs/reviews/precision-streaming-checks.json',dict(status='pass',checks=checks,cases=cases,invalid_cases=invalid,maximum_scaled_difference=worst,scope='Author-owned independent dense fixtures; selected stable-rank numeric equivalence and refusal behavior, not general calibration or external acceptance.'),SCIENCE_INPUTS+['tools/precision_checks.py'])
    print(json.dumps(dict(status='pass',cases=cases,invalid_cases=len(invalid),maximum_scaled_difference=worst)))


if __name__=='__main__':
    with threadpool_limits(limits=1): main()
