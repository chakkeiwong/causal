#!/usr/bin/env python3
"""Exact authored arithmetic; no acquired model, simulator or source code runs."""
from fractions import Fraction as F
import json

def calculate():
    table7={
      'gpt4omini':dict(pre=['41.80','34.46','43.22'],icl=['41.22','34.92','47.09'],sft=['68.03','66.94','38.03']),
      'llama33_70b':dict(pre=['41.08','33.73','41.86'],icl=['40.13','35.38','48.55'],sft=['43.10','37.29','38.68']),
      'llama31_8b':dict(pre=['37.75','31.43','34.85'],icl=['39.06','33.19','37.23'],sft=['38.78','33.09','34.56'])}
    delta={k:{label:[str(F(x)-F(y)) for x,y in zip(v['sft'],v[against])] for label,against in [('sft_minus_pre','pre'),('sft_minus_icl','icl')]} for k,v in table7.items()}
    worlds={};observations=[]
    for name,fn in [('causal10',lambda a,u:10*a+20*u),('causal0',lambda a,u:30*u)]:
        obs=[dict(u=u,a=u,y=fn(u,u),probability='1/2') for u in [0,1]]
        mu={a:sum(F(fn(a,u),2) for u in [0,1]) for a in [0,1]}
        tau=mu[1]-mu[0];observed=obs[1]['y']-obs[0]['y'];observations.append([(r['a'],r['y']) for r in obs])
        worlds[name]=dict(observations=obs,do_means={str(a):str(v) for a,v in mu.items()},effect_usd=str(tau),observed_contrast_usd=observed,stipulated_intervention_cost_usd=5,incremental_net_usd=str(tau-5))
    assert observations[0]==observations[1]
    requested=8;compiled=6;semantically_valid=4;causally_accepted=2;total=F(3)+F(30)*F(60,60)
    return dict(source_table7=dict(metric_order=['J-LLM Ref+Doc','J-LLM Ref','J-LLM Doc'],reported_scores=table7,deltas=delta,interpretation='Score differences, not probabilities, significance tests or independent reproductions.'),
        table8_llama70_lora_minus_pre=[str(F(a)-F(b)) for a,b in zip(['40.38','31.64','31.62'],['41.08','33.73','41.86'])],
        authored_causal_worlds=worlds,observationally_identical=True,causal_identification_from_code_execution=False,
        stipulated_full_cost=dict(api_usd='3',expert_minutes=30,expert_usd_per_hour='60',total_usd=str(total),requested=requested,compiled=compiled,semantically_valid=semantically_valid,causally_accepted=causally_accepted,per_request_usd=str(total/requested),per_compiled_usd=str(total/compiled),per_accepted_usd=str(total/causally_accepted)),
        scope='Exact source-table subtraction plus authored causal and accounting witnesses; no native execution, observed productivity, prices or bank evidence.')

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
