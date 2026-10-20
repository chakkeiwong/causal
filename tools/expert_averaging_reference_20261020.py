#!/usr/bin/env python3
"""Authored exact proposal witnesses; no downloaded implementation or live LLM execution."""
from fractions import Fraction as F
from math import comb
import json


def acyclic(edges):
    nodes={x for edge in edges for x in edge};remaining=set(nodes)
    while remaining:
        roots={v for v in remaining if not any(b==v and a in remaining for a,b in edges)}
        if not roots:return False
        remaining-=roots
    return True


def literal_budget_trace(answers,budget):
    """Only the existence-call control flow of the printed Algorithm1, page17."""
    counted=0;calls=0;accepted=0
    for answer in answers:
        proportion=F(2,5)
        passes=False
        if proportion>=0:
            if proportion>F(1,2):passes=True
            elif budget>counted:
                calls+=1
                passes=answer
        if passes:
            if proportion<=F(1,2):counted+=1
            accepted+=1
    return dict(actual_existence_calls=calls,printed_counter=counted,accepted=accepted,budget=budget)


def calculate():
    p=F(3,4);n=11
    independent=sum(F(comb(n,k))*p**k*(1-p)**(n-k) for k in range(6,n+1))
    shared=p
    assert independent>F(9,10) and shared==F(3,4)
    rejected=literal_budget_trace([False,False,False],1)
    assert rejected['actual_existence_calls']==3 and rejected['printed_counter']==0
    # With accepted adjacency, both directions legal, no budget and orientation
    # votes below theta2, the printed if/elif chain has no final fallback.
    votes=(F(3,4),F(1,4));theta=F(9,10);budget=0
    literal_orientation='forward' if votes[0]>=theta else 'reverse' if votes[1]>=theta else 'query' if budget>0 else None
    assert literal_orientation is None and votes[0]>F(1,2)
    graphs=[{('A','B'),('B','C')},{('B','C'),('C','A')},{('C','A'),('A','B')}]
    assert all(acyclic(g) for g in graphs)
    union=set.union(*graphs)
    frequencies={f'{a}->{b}':str(F(sum((a,b) in g for g in graphs),len(graphs))) for a,b in sorted(union)}
    assert set(frequencies.values())=={'2/3'} and not acyclic(union)
    chain={('offer','uptake'),('uptake','balance')}
    assert ('offer','balance') not in chain
    rho=F(3,5);noise=1-rho**2
    forward_cov=[[F(1),rho],[rho,rho**2+noise]]
    reverse_cov=[[rho**2+noise,rho],[rho,F(1)]]
    assert forward_cov==reverse_cov==[[F(1),rho],[rho,F(1)]]
    effects=[rho,F(0)];value=F(100);cost=F(40)
    margins=[value*t-cost for t in effects];weight=F(9,10)
    vote_effect=weight*effects[0]+(1-weight)*effects[1]
    vote_margin=value*vote_effect-cost
    assert margins==[20,-40] and vote_effect==F(27,50) and vote_margin==14
    return dict(kind='project_authored_exact_proposal_reference',native_execution=False,model_executed=False,
        correlated_votes=dict(voters=n,each_correct=str(p),independent_majority=str(independent),perfectly_shared_majority=str(shared),
            qualification='Two distinct assumed laws; real algorithm error dependence is not estimated here.'),
        printed_pseudocode=dict(rejected_existence_calls=rejected,exhausted_orientation=dict(votes=[str(x) for x in votes],threshold=str(theta),budget=0,
            literal_result=literal_orientation,majority_direction='forward'),
            qualification='Literal traces of printed Algorithm1 only; source code not inspected and no runtime defect is alleged.'),
        graph_aggregation=dict(component_graphs=[[list(e) for e in sorted(g)] for g in graphs],each_acyclic=True,edge_frequencies=frequencies,majority_is_acyclic=False),
        ancestry_not_adjacency=dict(edges=[list(e) for e in sorted(chain)],offer_ancestor_of_balance=True,offer_adjacent_to_balance=False),
        observational_equivalence=dict(distribution='Zero-mean jointly Gaussian with independent structural errors in each model',
            correlation=str(rho),conditional_noise_variance=str(noise),common_covariance=[[str(v) for v in row] for row in forward_cov],
            forward_effect=str(effects[0]),reverse_effect=str(effects[1]),value_per_unit_usd=str(value),assumed_cost_usd=str(cost),
            compatible_margins_usd=[str(x) for x in margins],unjustified_vote_weight=str(weight),vote_weighted_effect=str(vote_effect),
            vote_weighted_margin_usd=str(vote_margin)),
        limitations=['Graph votes and expert accuracy are not calibrated posterior probabilities or effect confidence regions.',
                    'All exact values arise from authored assumptions, not observed bank outcomes or replicated paper results.',
                    'Printed algorithm discrepancies require an immutable implementation, tests and query logs to resolve.',
                    'The two-Gaussian-world example has no time-order restriction; valid extra temporal information can rule out a world.'])


if __name__=='__main__':print(json.dumps(calculate(),indent=2))
