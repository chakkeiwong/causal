#!/usr/bin/env python3
"""Exact authored counterfactual coupling and posterior-factorization examples."""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
import json


def calculate():
    laws = {}
    interventions = {}
    answers = {}
    posteriors = {}
    for world in ['stable', 'switch']:
        law = defaultdict(F)
        posterior = defaultdict(F)
        marginal = {}
        for a,u,v in product([0,1],repeat=3):
            baseline = int(u == v)
            y = baseline if world == 'stable' or a == 0 else 1-baseline
            law[(a,y)] += F(1,8)
            if a == 0 and y == 1:
                posterior[(u,v)] += F(1,8)
        total = sum(posterior.values())
        posterior = {uv:p/total for uv,p in posterior.items()}
        for a in [0,1]:
            marginal[a] = sum(F(1,4)*(int(u==v) if world=='stable' or a==0 else int(u!=v))
                              for u,v in product([0,1],repeat=2))
        cf = sum(p*(int(u==v) if world=='stable' else int(u!=v)) for (u,v),p in posterior.items())
        laws[world] = [{'A':a,'Y':y,'mass':str(p)} for (a,y),p in sorted(law.items())]
        interventions[world] = {str(a):str(p) for a,p in marginal.items()}
        answers[world] = str(cf)
        posteriors[world] = [{'U':u,'V':v,'mass':str(p)} for (u,v),p in posterior.items()]
    assert laws['stable'] == laws['switch']
    assert interventions['stable'] == interventions['switch'] == {'0':'1/2','1':'1/2'}
    assert answers == {'stable':'1','switch':'0'}
    p_u = p_v = F(1,2)
    product_equality = p_u*p_v+(1-p_u)*(1-p_v)
    assert product_equality == F(1,2)
    payoff = {k:str(F(100)*F(p)-20) for k,p in answers.items()}
    payoff['separate_root_marginals'] = str(100*product_equality-20)
    assert payoff == {'stable':'80','switch':'-20','separate_root_marginals':'30'}
    # Stipulated hidden-confounding lending worlds: same observed law, different do laws.
    hidden = [{'world':'risk_only','observed':[[0,0,'1/2'],[1,1,'1/2']], 'P_Y1_do_A1':'1/2','P_Y1_do_A0':'1/2'},
              {'world':'direct_action','observed':[[0,0,'1/2'],[1,1,'1/2']], 'P_Y1_do_A1':'1','P_Y1_do_A0':'0'}]
    return dict(kind='project_authored_exact_reference',native_execution=False,
        assumptions='Independent A,U,V~Bernoulli(1/2); stable:Y(a)=1[U=V]; switch:Y(0)=1[U=V],Y(1)=1[U!=V]. Profile A=0,Y=1.',
        observed_laws=laws,intervention_probabilities=interventions,
        posterior_roots=posteriors,counterfactual_success=answers,
        product_of_root_marginals_success=str(product_equality),
        joint_posterior_equality_probability='1',
        assumed_net_value_USD=payoff,hidden_confounding_lending=hidden,
        limitations=['Known structural models illustrate joint posterior loss; the observed BN alone does not choose the cross-world coupling.',
                    'Source-motivated reference only; no installed aGrUM or dosearch execution.',
                    'USD100 success value and USD20 action cost are assumptions, not bank prices or ROI.'])

if __name__=='__main__':
    print(json.dumps(calculate(),indent=2))
