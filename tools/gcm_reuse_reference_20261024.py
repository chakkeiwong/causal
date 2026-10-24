#!/usr/bin/env python3
"""Authored structural and finite-population witnesses; no upstream execution."""
from fractions import Fraction as F
from itertools import combinations
import json

def calculate():
    # A stipulated invariant SCM Y=2*A+N. Individual noise remains fixed
    # in a counterfactual, while population simulation redraws it.
    a,y,beta=F(1),F(5),F(2);noise=y-beta*a
    cf=beta*F(0)+noise
    assert noise==cf==3
    # Distinct cross-world couplings have identical Bernoulli(1/2)
    # interventional marginals and identical randomized observed laws.
    coupled=[(0,0),(1,1)];flipped=[(0,1),(1,0)]
    def conditional(rows):
        chosen=[x1 for x0,x1 in rows if x0==0]
        return F(sum(chosen),len(chosen))
    assert conditional(coupled)==0 and conditional(flipped)==1
    for rows in [coupled,flipped]:
        assert F(sum(v[0] for v in rows),2)==F(1,2)
        assert F(sum(v[1] for v in rows),2)==F(1,2)
    # Complete finite-population enumeration for sampling3 of4 without
    # replacement. Compare with a size4 with-replacement empirical mean.
    data=list(map(F,[0,0,2,2]));mean=sum(data)/4
    means=[sum(c)/3 for c in combinations(data,3)]
    subset_variance=sum((m-mean)**2 for m in means)/len(means)
    empirical_population_variance=sum((x-mean)**2 for x in data)/4
    ordinary_bootstrap_mean_variance=empirical_population_variance/4
    assert subset_variance==F(1,9) and ordinary_bootstrap_mean_variance==F(1,4)
    # Dict outputs with equal per-key counts can still have disjoint
    # replicate identities; matching list lengths is not alignment.
    draws=[{'a':0},{'b':0},{'a':1},{'b':10},{'a':2},{'b':20}]
    collected={}
    for i,row in enumerate(draws):
        for k,v in row.items():collected.setdefault(k,[]).append((i,v))
    assert set(i for i,_ in collected['a']).isdisjoint(i for i,_ in collected['b'])
    class_effect=F(2,5)-F(1,5)
    assert class_effect==F(1,5)
    return dict(status='exact_authored_reference',downloaded_code_executed=False,
        structural=dict(factual_action='1',factual_outcome='5',coefficient='2',recovered_noise=str(noise),
            individual_do_zero=str(cf),population_do_zero_mean='0',
            assumption='Invariant supplied Y=2A+N with population E[N]=0;not learned causal truth'),
        cross_world=dict(coupled=coupled,flipped=flipped,marginal_success='1/2',average_effect='0',
            success_under_one_given_failure_under_zero=[str(conditional(coupled)),str(conditional(flipped))],
            qualification='Same observed and intervention laws;individual counterfactual differs'),
        subsampling=dict(data=list(map(str,data)),subset_size=3,replace=False,means=list(map(str,means)),
            subset_variance=str(subset_variance),ordinary_size4_bootstrap_mean_variance=str(ordinary_bootstrap_mean_variance),
            qualification='Conditional finite empirical laws;not interval coverage evidence'),
        summary_alignment=dict(requested=len(draws),per_key_count={k:len(v) for k,v in collected.items()},
            replicate_ids={k:[i for i,_ in v] for k,v in collected.items()},
            artificial_paired_values=[[a[1],b[1]] for a,b in zip(collected['a'],collected['b'])],
            qualification='Equal list lengths do not establish common replicate identity'),
        labels=dict(default_probability_effect=str(class_effect),complement_effect=str(-class_effect),
            qualification='Explicit positive class fixes event and sign'),
        banking=dict(accounts=1000,loss_per_default_usd=100,default_probability_effect=str(class_effect),
            expected_extra_loss_usd=str(1000*100*class_effect),
            qualification='Stipulated population effect and unit cost;not bank evidence'),
        costs=dict(total_usd=5400,requested=270,finite=225,accepted=180,
            per_requested=str(F(5400,270)),per_finite=str(F(5400,225)),per_accepted=str(F(5400,180)),
            qualification='Authored denominators and prices;not measured economics'))

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
