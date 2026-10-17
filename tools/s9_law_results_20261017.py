#!/usr/bin/env python3
"""Independent exact probability laws and decision-bound calculations for S9."""
from collections import Counter
from fractions import Fraction as F
from itertools import product
import json


def calculate():
    signs=(-1,1)
    shared=Counter(a-b for a,b,c in product(signs,repeat=3))
    split=Counter(a-ca-b+cb for a,ca,b,cb in product(signs,repeat=4))
    shared_n=8;split_n=16
    shared_p={str(k):str(F(v,shared_n)) for k,v in sorted(shared.items())}
    split_p={str(k):str(F(v,split_n)) for k,v in sorted(split.items())}
    outcomes=set(shared)|set(split)
    tv=sum(abs(F(shared[k],shared_n)-F(split[k],split_n)) for k in outcomes)/2
    prob_shared=F(sum(v for k,v in shared.items() if k>0),shared_n)
    prob_split=F(sum(v for k,v in split.items() if k>0),split_n)
    return dict(shared_difference_law=shared_p,split_difference_law=split_p,
        total_variation=str(tv),positive_probability=dict(shared=str(prob_shared),split=str(prob_split),
            absolute_difference=str(abs(prob_shared-prob_split))),
        decision_stability=dict(scalar_sufficient_condition='abs(theta-threshold)>epsilon',
            action_ranking_sufficient_condition='best_value-second_best_value>epsilon_best+epsilon_runner_up',
            uniform_action_regret_bound='2*epsilon_max',
            equality_case='At a boundary the declared error bounds alone do not certify the same selected action.'),
        exact_inputs=dict(signs=['-1','+1'],shared_paths=shared_n,split_paths=split_n),
        limitations=['Finite stipulated random laws and deterministic perturbation bounds.',
                     'No CausalML estimator variance, upstream library execution or empirical bank decision is measured.'])


def check(value):
    assert value['shared_difference_law']=={'-2':'1/4','0':'1/2','2':'1/4'}
    assert value['split_difference_law']=={'-4':'1/16','-2':'1/4','0':'3/8','2':'1/4','4':'1/16'}
    assert value['total_variation']=='1/8'
    assert value['positive_probability']==dict(shared='1/4',split='5/16',absolute_difference='1/16')
    # For any finite action set, max-score perturbations bounded by epsilon
    # cannot exceed 2 epsilon regret; the gap condition handles heterogeneous errors.
    return dict(status='pass',checks=['Exact Fraction enumeration matches the eight- and sixteen-path laws.',
        'Total variation is1/8; zero-threshold choice probabilities differ by1/16.',
        'Scalar threshold and argmax stability conditions follow by the triangle inequality.',
        'No equality of upstream distributions or estimator calibration is inferred.'])


if __name__=='__main__':
    out=calculate();print(json.dumps(dict(result=out,review=check(out)),indent=2))
