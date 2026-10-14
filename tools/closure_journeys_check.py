#!/usr/bin/env python3
from dataclasses import replace
import json
import numpy as np
from threadpoolctl import threadpool_limits
from closure_common import ROOT,save
from causalbank.closure_journeys import JourneyRequest,run_journey,treasury_consumer,application_consumer
from causalbank.nonlinear_audited import TRUTH,simulate
from closure_linkage_study import pair_sample
from closure_discovery_study import sample


def main():
    spec=json.loads((ROOT/'docs/studies/closure-spec.json').read_text());checks={};results=[]
    requests=[JourneyRequest('persistent_funding','independent_pairs','eligible_deposit_customers','pair','action_then_outcome','audited_pair_CLT',1000.),
              JourneyRequest('nonlinear_servicing','independent_trajectories','eligible_servicing_customers','customer','signal_action_reward_transition','audited_nonlinear_delta',1000.),
              JourneyRequest('discovery_decision','independent_gaussian_episodes','eligible_credit_episodes','episode','Z_then_A_then_Y','outer_graph_union',1000.)]
    old=json.loads((ROOT/'docs/studies/closure-nonlinear-results.json').read_text());policy=np.array(old['planning']['selected_policy'])
    with threadpool_limits(limits=1):
        for j,request in enumerate(requests):
            for new in range(2):
                rng=np.random.default_rng([101072,j,new])
                if j==0:
                    config=dict(spec['persistent'],pairs=1200 if new else 800,dates=12 if new else 8)
                    a,y,r,l,q,_=pair_sample(config,rng,.3)
                    payload=dict(action=a,candidates=y,audited=r,labels=l,inclusion_probability=q)
                elif j==1:
                    main,_=simulate(TRUTH,80,3,rng);audit,s=simulate(TRUTH,640,3,rng)
                    payload=dict(main=main,audit=audit,states=s,policy=policy if not new else np.array([0.,0.,0.]))
                else:payload=dict(episodes=sample(rng,600,1.5 if new else 1.),information='randomized_encouragement' if new else 'observational_latent')
                out=run_journey(request,payload);t=treasury_consumer(out);a=application_consumer(out,2000)
                checks[request.family+f'_{new}_meaning']=t['inference']==a['inference']==out['inference']
                checks[request.family+f'_{new}_topology']=len(out['financial_set'])==len(a['financial_set_per_account'])
                results.append(dict(request=request.__dict__,treasury=t,application=a))
        for name,request in [('clock',replace(requests[0],clock='received_after_outcome')),('population',replace(requests[0],population='')),('unit',replace(requests[0],unit='account_date')),('sampling',replace(requests[0],sampling='common_calendar')),('inference',replace(requests[2],inference='selected_graph_pointwise')),('policy_information',replace(requests[1],policy_information='current_audited_hidden_state'))]:
            try:request.validate();checks[name+'_rejected']=False
            except ValueError:checks[name+'_rejected']=True
    identity=results[0]['treasury']['identity'];checks['new_request_identity_differs']=identity!=results[1]['treasury']['identity']
    result=dict(status='pass' if all(checks.values()) else 'fail',checks=checks,journeys=results,
                scope='Three local bounded journeys, two consumers and new eligible requests; no accepted sibling integration or user-workflow savings claim.')
    save('docs/reviews/closure-journeys.json',result,['tools/closure_journeys_check.py','tools/closure_common.py','src/causalbank/closure_journeys.py','src/causalbank/persistent_audits.py','src/causalbank/nonlinear_stability.py','src/causalbank/nonlinear_audited.py','src/causalbank/latent_temporal_sets.py','tools/closure_linkage_study.py','tools/closure_discovery_study.py','docs/studies/closure-nonlinear-results.json'])
    print(json.dumps({'status':result['status'],'checks':checks},indent=2));raise SystemExit(result['status']!='pass')


if __name__=='__main__':main()
