#!/usr/bin/env python3
"""Exact selective-serving arithmetic and an independently authored premise counterexample."""
from fractions import Fraction as F
from math import comb
import json

def calculate():
 beta=F(1,5);slip=F(1,10)
 wrong2=beta+(1-beta)*slip**2;correct2=(1-beta)*(1-slip)**2;abstain2=1-wrong2-correct2
 wrong3=beta+(1-beta)*sum(F(comb(3,k))*slip**k*(1-slip)**(3-k) for k in [2,3])
 assert (wrong2,correct2,abstain2)==(F(26,125),F(81,125),F(18,125))
 assert wrong3==F(139,625)
 # This toy executor checks derivability only. The admitted leaf is deliberately false in the stipulated world.
 allowed={'arrears'};heads={'deny'};assert not (allowed & heads)
 world=set();admitted={'arrears'};derived={'deny'} if 'arrears' in admitted else set()
 assert 'deny' not in allowed and 'deny' in derived and 'arrears' not in world
 before=(1533,252,306);after=(1482,189,420)
 assert sum(before)==sum(after)==2091
 saved_wrong=before[1]-after[1];withheld_correct=before[0]-after[0];extra_abstain=after[2]-before[2]
 assert (saved_wrong,withheld_correct,extra_abstain)==(63,51,114)
 return dict(kind='independent_reported_count_arithmetic_and_stipulated_model',native_execution=False,
  shared_bias_model=dict(bias_mass=str(beta),independent_slip=str(slip),two_vote_wrong=str(wrong2),two_vote_correct=str(correct2),two_vote_abstention=str(abstain2),two_vote_answered_risk=str(wrong2/(wrong2+correct2)),three_vote_majority_wrong=str(wrong3),infinite_vote_error_floor=str(beta)),
  premise_counterexample=dict(target_write_rejected=True,false_allowed_leaf_admitted=True,conclusion_derivable=True,world_truth_established=False),
  reported_deepseek_contractnli=dict(pool=2091,agreement=list(before),source_recheck=list(after),wrong_removed=63,correct_withheld=51,extra_abstention=114,risk_before=str(F(252,1785)),risk_after=str(F(189,1671)),full_pool_accuracy_change=str(F(-51,2091))),
  stipulated_loss_saving=dict(wrong_cost=10,extra_compute_cost=100,abstention_cost2=63*10-114*2-100,abstention_cost6=63*10-114*6-100),
  limitations=['Reported counts rechecked arithmetically; no raw experiment replay.', 'Bias, independent-slip and monetary inputs are stipulated; no latent parameter estimation or bank economics.', 'Toy gate proves only its declared rule contract, not a source checker or product.'])
if __name__=='__main__':print(json.dumps(calculate(),indent=2))
