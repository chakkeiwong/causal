#!/usr/bin/env python3
"""Authored exact checks; no model calls or upstream Bayesian-discovery execution."""
from fractions import Fraction as F
from itertools import product
import json

def calculate():
    # Two independent directed edge indicators, each Bernoulli(1/2).
    legal=[x for x in product([0,1],repeat=2) if x!=(1,1)]
    mass=F(len(legal),4);edge=F(sum(x[0] for x in legal),len(legal))
    assert mass==F(3,4) and edge==F(1,3)
    # Same response law is consistent with wholly correct or wholly wrong advice.
    output_frequency=F(9,10)
    truth_conditional=[F(1),F(0)]
    assert output_frequency not in truth_conditional
    # Four-way feedback posterior with rho=(.4,.3,.2,.1), claimed pi=.7,
    # report in category2. The other likelihoods are .1.
    rho=[F(4,10),F(3,10),F(2,10),F(1,10)];pi=F(7,10)
    weights=[r*(pi if k==1 else (1-pi)/3) for k,r in enumerate(rho)]
    z=sum(weights);posterior=[x/z for x in weights]
    assert z==F(7,25) and posterior==[F(1,7),F(3,4),F(1,14),F(1,28)]
    # Exact differences of reported means, not reconstructed empirical trials.
    values={'Sachs':('23.4','21.7','26.7'), 'MAGIC-7':('13.76','16.07','16.24'),
            'MAGIC-ORIGINAL':('153.00','160.05',None),'Summer':('12.17','12.42','9.68')}
    changes={k:{'GPT_minus_baseline':str(F(g)-F(b)),'DeepSeek_minus_baseline':str(F(d)-F(b)) if d else None} for k,(b,g,d) in values.items()}
    assert changes['MAGIC-ORIGINAL']['GPT_minus_baseline']=='141/20'
    # Perfectly anticorrelated scores have AUROC 0, so .5 is not the minimum.
    labels=[1,0];scores=[0,1]
    auc=sum(F(scores[i]>scores[j])+F(scores[i]==scores[j],2) for i in range(2) for j in range(2) if labels[i]==1 and labels[j]==0)
    assert auc==0
    return dict(kind='project_exact_counterexamples_and_reported_mean_arithmetic',acyclic_conditioning=dict(admitted_mass=str(mass),edge_marginal=str(edge),no_edge_mass='1/3'),four_way_feedback=dict(normalizer=str(z),posterior=[str(x) for x in posterior]),response_frequency=str(output_frequency),compatible_truth_values=[str(x) for x in truth_conditional],reported_eshd_mean_differences=changes,reverse_ranking_auc=str(auc),limitations=['No reproduction of empirical means or reported error bars.','Four-way posterior is conditional on the stipulated feedback channel; response repetition does not validate it.'])

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
