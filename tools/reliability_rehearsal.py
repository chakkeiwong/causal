#!/usr/bin/env python3
"""Local synthetic interface and refusal rehearsal, not external acceptance."""
import json
import numpy as np
from threadpoolctl import threadpool_limits
from reliability_common import ROOT,SPEC
from closure_common import save,default
from reliability_joint_study import sample
from reliability_learning_study import data,request
from closure_discovery_study import sample as graph_sample
from causalbank.reliability_operations import execute
from causalbank.nonlinear_variance import TRUTH,simulate


def main():
    s=json.loads((ROOT/SPEC).read_text());checks={};outputs=[]
    with threadpool_limits(limits=1):
        a,y,r,label,q,gold,g=sample(s['joint'],np.random.default_rng(821400));inp=dict(action=a,candidates=y,audited=r,labels=label,inclusion=q);opts=dict(bandwidth=7,gold_errors=gold)
        outputs.append(execute('persistent_calendar',inp,opts));rank=execute('persistent_calendar',inp,dict(bandwidth=7,gold_errors=np.tile([0,1],50)));checks['rank_status_preserved']=rank['status']=='unqualified_label_rank' and 'interval' not in rank['result'];outputs.append(rank)
        x=graph_sample(np.random.default_rng(821401),200);outputs.append(execute('finite_gaussian_effect',dict(data=x),dict(information='randomized_encouragement')));outputs.append(execute('finite_gaussian_effect',dict(data=x),dict(information='observational_latent')))
        checks['whole_line_preserved']=outputs[-1]['result']['effect_set']==[{'lower':None,'upper':None}]
        c,t=data(s['learning'],np.random.default_rng(821402));outputs.append(execute('fixed_dictionary_calendar',dict(request=request(s['learning']),controls=c,targets=t),dict(chunk_rows=128)))
        policy=np.asarray(json.loads((ROOT/s['nonlinear']['policy_source']).read_text())['planning']['selected_policy']);main,_=simulate(TRUTH,80,3,np.random.default_rng(821403));audit,states=simulate(TRUTH,640,3,np.random.default_rng(821404));outputs.append(execute('audited_nonlinear_policy',dict(main=main,audit=audit,states=states,policy=policy),{}))
        for route,inputs,options in [('persistent_calendar',inp,dict(opts,sampling='arbitrary_dependence')),('finite_gaussian_effect',dict(data=x),dict(information='randomized_encouragement',sampling='dependent_histories')),('unknown_route',{}, {})]:
            try:execute(route,inputs,options);checks['refusal_'+route]=False
            except ValueError:checks['refusal_'+route]=True
    # Simulate both proposed consumers by independent serialization/read-back.
    checks['consumer_qualifications']=True
    for out in outputs:
        payload={k:v for k,v in out['result'].items() if k not in ('scores','folds','covariance')};public=dict(out,result=payload)
        first=json.loads(json.dumps(public,default=default,allow_nan=False));second=json.loads(json.dumps(public,default=default,allow_nan=False))
        checks['consumer_qualifications']&=first==second and first['result'].get('inference')==out['result'].get('inference')
    if not all(checks.values()):raise AssertionError(checks)
    save('docs/reviews/reliability-local-rehearsal.json',dict(status='pass',checks=checks,fixtures=[dict(route=o['route'],status=o['status'],unit=o['unit'],inference=o['result'].get('inference')) for o in outputs],
        scope='Local author-owned synthetic route/status/refusal/serialization rehearsal. No external reviewer, actual bank owner, consumer maintainer, analyst or multi-host acceptance.'),
        ['tools/reliability_rehearsal.py','src/causalbank/reliability_operations.py','src/causalbank/joint_audited.py','src/causalbank/gaussian_effect_pivots.py','src/causalbank/chunked_learning.py','src/causalbank/blocked_learning.py','src/causalbank/nonlinear_variance.py','src/causalbank/nonlinear_audited.py','tools/reliability_joint_study.py','tools/reliability_learning_study.py','tools/study_response_extensions.py','tools/closure_discovery_study.py',SPEC,s['nonlinear']['policy_source'],'contracts/reliability.md','docs/program/external-validation-v8.md'])
    print(json.dumps(dict(status='pass',checks=checks)))

if __name__=='__main__':main()
