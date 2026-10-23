#!/usr/bin/env python3
"""Exact hidden-state decision witnesses, with no upstream execution."""
from fractions import Fraction as F
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def calculate():
 prior=F(1,4);sens=F(3,4);false=F(1,4)
 positive=prior*sens+(1-prior)*false
 post_pos=prior*sens/positive;post_neg=prior*(1-sens)/(1-positive)
 action_value=lambda p:35*p-15*(1-p)
 assert positive==F(3,8) and post_pos==F(1,2) and post_neg==F(1,10)
 planned=positive*max(0,action_value(post_pos))+(1-positive)*max(0,action_value(post_neg))-2
 actual=F(1,2)*action_value(prior)-2
 assert planned==F(7,4) and actual==F(-13,4) and action_value(prior)==F(-5,2)
 gamma=F(1,2);reward=F(1)
 correct=sum(gamma**t*reward for t in range(3))
 source_depth=reward+gamma*(reward+gamma**2*reward)
 assert correct==F(7,4) and source_depth==F(13,8)
 option_literal=F(2)+8+gamma**2*20
 option_clock=F(2)+gamma*8+gamma**2*20
 assert option_literal==15 and option_clock==11
 # Repeated state values: the selected weighted-particle query averages per value,
 # while sampling uses every entry's weight. Unweighted Particles overrides both.
 weighted=[('D',F(1)),('D',F(1)),('H',F(1))]
 total=sum(w for _,w in weighted);sampling=sum(w for s,w in weighted if s=='D')/total
 means={s:sum(w for a,w in weighted if a==s)/sum(a==s for a,w in weighted) for s in ['D','H']}
 query=means['D']/sum(means.values());assert sampling==F(2,3) and query==F(1,2)
 files={name:(ROOT/'docs/literature/raw'/name).read_text() for name in ['exec23_pomdppy_03.txt','exec23_pomdppy_05.txt','exec23_pomdppy_07.txt','exec23_pomdppy_09.txt']}
 assert 'if total_prob > 0:' in files['exec23_pomdppy_05.txt']
 assert 'discount_factor = self._discount_factor**self.depth' in files['exec23_pomdppy_09.txt']
 assert 'sample_generative_model(self._agent, state, action)' in files['exec23_pomdppy_07.txt']
 rollout=files['exec23_pomdppy_07.txt'].split('cpdef _rollout(',1)[1].split('cpdef Action _ucb',1)[0]
 assert 'while depth < self._max_depth:' in rollout and 'depth += nsteps' in rollout and 'if nsteps == 0' not in rollout
 return clean(dict(native_execution=False,posterior=dict(prior=prior,positive_probability=positive,positive=post_pos,negative=post_neg),
  decision=dict(always_act=action_value(prior),signal_cost=2,assumed_sensor_net=planned,uninformative_actual_sensor_net=actual),
  horizon=dict(gamma=gamma,rewards=[1,1,1],one_step_discount=correct,depth_exponent_expression=source_depth),
  option=dict(rewards=[2,8],continuation=20,duration=2,source_default_internal_discount=option_literal,clock_consistent_discount=option_clock),
  support=dict(impossible_observation_normalizer=0,source_zero_mass_return=[0,0],restricted_support_prior={'D':F(1,5),'H':F(4,5)},restricted_next_space=['H'],renormalized_result={'H':1}),
  weighted_particles=dict(entries=weighted,sampling_D=sampling,query_D=query,ordinary_unweighted_D=F(2,3)),
  zero_duration=dict(depth_before=0,duration=0,depth_after=0,outer_budget_checked_between_simulations=True,source_rollout_progress_guard=False)))
def clean(x):
 if isinstance(x,F):return str(x)
 if isinstance(x,dict):return {k:clean(v) for k,v in x.items()}
 if isinstance(x,(list,tuple)):return [clean(v) for v in x]
 return x
if __name__=='__main__':print(json.dumps(calculate(),indent=2))
