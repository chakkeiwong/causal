#!/usr/bin/env python3
"""Exact evidence-composition examples; no model or source acquisition calls."""
from fractions import Fraction as F
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-13/frontier-synthesis'

def main():
    scores={'cot':(F(69,100),F(90,100)),'tools':(F(76,100),F(73,100))}
    threshold=F(17,24)
    def mix(pair,w):return w*pair[0]+(1-w)*pair[1]
    assert mix(scores['cot'],threshold)==mix(scores['tools'],threshold)
    weights=[F(1,2),F(4,5)]
    mixture=[{'formal_task_weight':str(w),'cot':str(mix(scores['cot'],w)),'tools':str(mix(scores['tools'],w)),'difference':str(mix(scores['tools'],w)-mix(scores['cot'],w))} for w in weights]
    assert [r['difference'] for r in mixture]==['-1/20','11/500']
    margins=[F(96,100),F(95,100),F(90,100),F(97,100),F(98,100)]
    chain=F(1)
    for p in margins:chain*=p
    # All possible success patterns, each with independent-product probability.
    import itertools
    independent=F(0)
    for bits in itertools.product([0,1],repeat=5):
        mass=F(1)
        for yes,p in zip(bits,margins):mass*=p if yes else 1-p
        if all(bits):independent+=mass
    assert independent==chain==F(2438289,3125000)
    # Two100-case populations with the same marginals, disjoint versus nested failures.
    failures=[4,5,10,3,2];disjoint=[];nested=[];offset=0
    for n in failures:
        disjoint.append(set(range(offset,offset+n)));offset+=n
        nested.append(set(range(n)))
    lo=F(100-len(set.union(*disjoint)),100);hi=F(100-len(set.union(*nested)),100)
    assert (lo,hi)==(F(19,25),F(9,10))
    # Binary answer-key example:90/100 agreement can mean80% or100% truth accuracy.
    pred=[0]*100;labels=[0]*90+[1]*10
    truth_low=labels.copy();truth_low[:10]=[1]*10
    truth_high=[0]*100
    def accuracy(a,b):return F(sum(x==y for x,y in zip(a,b)),len(a))
    assert accuracy(pred,labels)==F(9,10)
    assert accuracy(pred,truth_low)==F(4,5) and accuracy(pred,truth_high)==1
    assert accuracy(labels,truth_low)==accuracy(labels,truth_high)==F(9,10)
    # Identical observed information; gain500 or0, action cost250.
    grid=[F(i,100) for i in range(101)]
    risks=[(max(250*p,250*(1-p)),p) for p in grid]
    best=min(risks)
    assert best==(F(125),F(1,2))
    result={'kind':'exact_authored_frontier_evidence_examples','live_calls':0,'random_draws':0,
        'benchmark_mixture':{'reported_scores':{k:[str(x) for x in v] for k,v in scores.items()},'switch_weight':str(threshold),'examples':mixture,'limit':'Weighted published point scores; no confidence bound, joint-case data or bank task distribution.'},
        'workflow_composition':{'stage_probabilities':[str(p) for p in margins],'conditional_chain_success':str(chain),'decimal':float(chain),'same_marginals_min_joint':str(lo),'same_marginals_max_joint':str(hi),'reference_cases':100,'limit':'Conditional chain multiplication is exact without stage independence; marginal multiplication instead imposes a joint-law premise.'},
        'oracle_error':{'agreement':'9/10','stipulated_key_error':'1/10','attainable_truth_accuracy':['4/5','1'],'constructed_cases_per_world':100,'limit':'Stipulated truth/key vectors; does not estimate any benchmark error rate.'},
        'decision_ambiguity':{'effects_USD':['0','500'],'action_cost_USD':'250','minimax_action_probability':str(best[1]),'minimax_expected_regret_USD':str(best[0]),'always_act_worst_regret_USD':'250','always_decline_worst_regret_USD':'250','limit':'Two stipulated equal-observed-law worlds; randomized minimax expected regret is not a banking recommendation.'}}
    path=BASE/'exact-results.json';assert not path.exists();path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'pass','switch_weight':float(threshold),'chain':float(chain),'joint_bounds':[float(lo),float(hi)],'oracle_bounds':[.8,1],'minimax_regret':125}))

if __name__=='__main__':main()
