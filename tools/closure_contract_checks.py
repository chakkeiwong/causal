#!/usr/bin/env python3
"""Regression of the actual omission and preserved scientific numerics."""
import copy
import json
import sys
import types
import zipfile
import numpy as np
from threadpoolctl import threadpool_limits
from closure_common import ROOT, save
from causalbank.dynamic_product import (DynamicBrief, FundingRequest, run_funding,
    run_funding_request, treasury_report, application_result)
from causalbank.dynamic_funding import FundingTarget
from dynamic_observation_study import make_linked


def main():
    base=json.loads((ROOT/'docs/studies/dynamic-funding-spec.json').read_text())
    obs=json.loads((ROOT/'docs/studies/dynamic-observation-spec.json').read_text())
    fixture=json.loads((ROOT/'docs/studies/observation-fixtures-v6.json').read_text())['cases'][0]
    target=FundingTarget(horizon=base['horizon'],branches=base['branches'])
    brief=DynamicBrief(target,'source','pilot','audit',6)
    kwargs=dict(source_fixture=fixture,pilot=make_linked(base,obs,1440,[1010,0]),
                data=make_linked(base,obs,360,[1010,1]),audit_strata=np.repeat([0,1],100),
                audit_correct=np.r_[np.ones(95),np.zeros(5),np.ones(80),np.zeros(20)].astype(int),
                penalties=base['penalties'])
    old=types.ModuleType('causalbank._preserved_dynamic_product')
    sys.modules[old.__name__]=old
    with zipfile.ZipFile(ROOT/'docs/program/history/v6.1-assessed-delivery.zip') as archive:
        exec(compile(archive.read('src/causalbank/dynamic_product.py'),'<preserved-v6.1>','exec'),old.__dict__)
    checks={};outputs={}
    with threadpool_limits(limits=1):
        for method in ('regular_delta','weak_linkage_projection'):
            before=old.run_funding(brief,**kwargs,inference=method)
            after=run_funding_request(FundingRequest(brief,method),**kwargs)
            fields=('financial_value','financial_se','financial_interval','response','covariance') if method=='regular_delta' else ('financial_set','candidate_financial_means','candidate_financial_covariance')
            checks[method+'_numeric_identity']=all(before[k]==after[k] if k=='financial_set' else np.array_equal(before[k],after[k]) for k in fields)
            checks[method+'_all_consumers']=all(f(after)['inference']==after['inference'] for f in (treasury_report,lambda r:application_result(r,100)))
            outputs[method]={'treasury':treasury_report(after),'application':application_result(after,100)}
        projected=after
    for name,pieces in [('bounded',[{'lower':1.,'upper':2.}]),('rays',[{'lower':None,'upper':-1.},{'lower':2.,'upper':None}]),('whole',[{'lower':None,'upper':None}]),('empty',[])]:
        result=dict(projected,financial_set=pieces)
        a=application_result(result,10);t=treasury_report(result)
        checks[name+'_topology']=len(a['funding_set_per_account'])==len(pieces) and t['funding_contribution_set_currency']==pieces
        checks[name+'_meaning']=a['inference']==t['inference']==result['inference']
        json.dumps(a,allow_nan=False)
    unavailable={'status':'unavailable','reason':'missing audit information','identity':'example'}
    checks['unavailable_no_numeric_claim']=all(f(unavailable)['inference']['numerical_status']=='unavailable' for f in (treasury_report,lambda r:application_result(r,10)))
    try:
        FundingRequest(brief)
        checks['explicit_method_required']=False
    except TypeError:
        checks['explicit_method_required']=True
    copy_out=treasury_report(projected);copy_out['inference']['identification_conditions'].clear()
    checks['consumer_cannot_mutate_source']=bool(projected['inference']['identification_conditions'])
    checks={k:bool(v) for k,v in checks.items()}
    result=dict(status='pass' if all(checks.values()) else 'fail',checks=checks,outputs=outputs,
                scope='Real public calls, exact numeric comparison to archived V6.1, and qualification/topology preservation; no new calibration claim.')
    save('docs/reviews/closure-contract-checks.json',result,['tools/closure_contract_checks.py','tools/closure_common.py','src/causalbank/dynamic_product.py','src/causalbank/inference_description.py','contracts/inference-v3.md','docs/program/history/v6.1-preservation-receipt.json'])
    print(json.dumps({'status':result['status'],'checks':checks},indent=2))
    raise SystemExit(result['status']!='pass')


if __name__=='__main__':
    main()
