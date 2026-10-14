#!/usr/bin/env python3
"""Independent audit-law expectation and global-outer-projection checks."""
import json
from itertools import product
import numpy as np
from scipy.stats import chi2
from closure_common import save
from causalbank.persistent_audits import audited_pair_effect
from causalbank.ellipsoid_linkage import ellipsoid_projection
from causalbank.linkage_sets import decode_set


def main():
    checks={};max_error=0.
    # Enumerate audit selection and label noise conditional on arbitrary pair
    # summaries; no random experiment is needed to establish this identity.
    for u,v,q,e,m in product([-2.,3.],[.1,4.],[.1,.8],[0.,.15],[0,1]):
        candidate=[u,v] if m else [v,u];t=(u+v)/2;expectation=0.
        for audited,flip in product([0,1],repeat=2):
            weight=(q if audited else 1-q)*(e if flip else 1-e)
            label=abs(m-flip)
            corrected=t+(2*label-1)*(candidate[0]-candidate[1])/(2*(1-2*e))
            expectation+=weight*(t+audited/q*(corrected-t))
        max_error=max(max_error,abs(expectation-u))
    checks['enumerated_audit_and_noise_unbiasedness']=max_error<1e-12
    rng=np.random.default_rng(101011);worst=0.
    for case in range(80):
        a=rng.normal(size=(4,4));v=a@a.T+.1*np.eye(4);m=rng.normal(size=4)
        counts=np.array([95,80]) if case%2 else np.array([10,25])
        result=ellipsoid_projection(m,v,counts,[100,100]);lo,hi=decode_set(result['financial_set'])[0]
        for _ in range(100):
            p=np.array([rng.uniform(*x) for x in result['audit_intervals']]);r=2*p-1
            direction=rng.normal(size=4);direction/=np.linalg.norm(direction)
            point=m+np.linalg.cholesky(v)@direction*np.sqrt(chi2.ppf(.975,4))*rng.random()**.25
            value=np.array([.5,.5/r[0],.5,.5/r[1]])@point
            worst=max(worst,lo-value,value-hi)
    checks['independent_primal_points_retained']=worst<1e-10
    checks['rank_zero_fallback']=ellipsoid_projection(np.ones(4),np.eye(4),[50,50],[100,100])['financial_set']==[{'lower':None,'upper':None}]
    checks['singular_response_fallback']=ellipsoid_projection(np.ones(4),np.zeros((4,4)),[95,80],[100,100])['numerical_status']=='conservative_outer_fallback'
    a=np.ones((4,2));y=np.ones((4,2,2));r=np.ones(4);labels=np.ones(4);q=np.ones(4)*.5
    for name,kw in [('shared_calendar',dict(sampling='common_calendar')),('unknown_label_error',dict(label_error=None)),('invalid_inclusion',dict(inclusion_probability=np.zeros(4)))]:
        args=dict(action=a,candidates=y,audited=r,labels=labels,inclusion_probability=q);args.update(kw)
        try:audited_pair_effect(**args);checks[name+'_rejected']=False
        except ValueError:checks[name+'_rejected']=True
    checks={k:bool(v) for k,v in checks.items()}
    result=dict(status='pass' if all(checks.values()) else 'fail',checks=checks,
                conditional_expectation_max_error=max_error,primal_points=8000,maximum_outer_violation=worst,
                scope='Independent algebra and feasibility checks; sampling qualification remains conditional on stated laws.')
    save('docs/reviews/closure-linkage-checks.json',result,['tools/closure_linkage_checks.py','tools/closure_common.py','src/causalbank/persistent_audits.py','src/causalbank/ellipsoid_linkage.py','src/causalbank/linkage_sets.py'])
    print(json.dumps(result,indent=2));raise SystemExit(result['status']!='pass')


if __name__=='__main__':main()
