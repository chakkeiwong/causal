#!/usr/bin/env python3
"""Finite exact acquisition/decision examples; no LLM or bank execution."""
from fractions import Fraction as F
from itertools import product
import json
from math import log2


def entropy(probabilities):
    return -sum(float(p)*log2(float(p)) for p in probabilities if p)


def one_query(kind, unavailable=F(0)):
    worlds = {(h, z): F(1, 4) for h, z in product(range(2), repeat=2)}
    rows = {}
    for (h, z), prior in worlds.items():
        for signal in [0, 1, 'unavailable']:
            if signal == 'unavailable':
                likelihood = unavailable
            else:
                likelihood = (1-unavailable)*((F(1) if signal == z else F(0)) if kind == 'irrelevant'
                                              else (F(4, 5) if signal == h else F(1, 5)))
            rows[h, z, signal] = prior*likelihood
    outcomes = []
    value = F(0); conditional_entropy = 0.
    for signal in [0, 1, 'unavailable']:
        probability = sum(p for (h, z, s), p in rows.items() if s == signal)
        if not probability:
            continue
        posterior = {world: rows[world[0], world[1], signal]/probability for world in worlds}
        profit = sum(p*(100 if h else -120) for (h, z), p in posterior.items())
        decision = 'deploy' if profit > 0 else 'abstain'
        value += probability*max(F(0), profit)
        conditional_entropy += float(probability)*entropy(posterior.values())
        outcomes.append({'signal': signal, 'probability': probability,
                         'posterior_good': sum(p for (h,z),p in posterior.items() if h),
                         'expected_deploy_profit': profit, 'decision': decision})
    # Independently evaluate realized profit under the chosen signal policy.
    chosen = {r['signal']:r['decision'] for r in outcomes}
    direct = sum(p*(100 if h else -120) for (h,z,s),p in rows.items() if chosen.get(s)=='deploy')
    assert direct == value
    return {'expected_terminal_value': value, 'cost': F(5), 'net_value': value-5,
            'information_bits': entropy(worlds.values())-conditional_entropy,
            'outcomes': outcomes}


def main():
    irrelevant = one_query('irrelevant')
    useful = one_query('useful')
    failed = one_query('useful',F(1,4))
    assert irrelevant['expected_terminal_value']==0
    assert useful['expected_terminal_value']==28 and useful['net_value']==23
    assert failed['expected_terminal_value']==21 and failed['net_value']==16
    assert abs(irrelevant['information_bits']-1)<1e-12
    assert abs(useful['information_bits']-(1-entropy([F(4,5),F(1,5)])))<1e-12
    random_net=(irrelevant['net_value']+useful['net_value'])/2
    assert random_net==9
    # Two conditionally independent useful acquisitions; stop after first is cheaper.
    twovalue=F(0)
    for s1,s2 in product(range(2),repeat=2):
        masses={h:F(1,2)*(F(4,5) if s1==h else F(1,5))
                        *(F(4,5) if s2==h else F(1,5)) for h in range(2)}
        p=sum(masses.values())
        twovalue+=max(F(0),sum(v*(100 if h else -120) for h,v in masses.items()))
    assert twovalue==F(148,5) and twovalue-10==F(98,5)
    # Shared hidden answer error: five copies contain only one query's information.
    correct_repeat_posterior=F(4,5)
    false_independent_posterior=F(4,5)**5/(F(4,5)**5+F(1,5)**5)
    assert false_independent_posterior==F(1024,1025)
    result={'kind':'exact_project_planning_construction','random_draws':0,'live_model_calls':0,
            'bank_interventions':0,'worlds':4,'prior_good':F(1,2),'deploy_payoffs':[100,-120],
            'prior_expected_deploy_profit':F(-10),'prior_optimal_value':F(0),
            'clairvoyant_value':F(50),'currency':'hypothetical USD per stipulated decision',
            'one_acquisition_budget':{'information_gain_policy':irrelevant,
                                      'decision_value_policy':useful,'uniform_random_net_value':random_net},
            'unavailability':{'probability':F(1,4),'charged_for_attempt':True,'all_attempts':failed,
                              'success_only_net_value':F(23)},
            'two_independent_useful_queries':{'expected_terminal_value':twovalue,'net_value':twovalue-10,
                                             'one_query_net_value':F(23),'optimal_stop_after_one':True,
                                             'max_conditional_second_query_gain':F(16,5)},
            'correlated_expert_copies':{'copies':5,'true_posterior_given_all_positive':correct_repeat_posterior,
                                        'incorrect_independence_posterior':false_independent_posterior,
                                        'conditional_error_model':'All copies reuse one Bernoulli answer error'},
            'misspecified_support':{'assumed_good_probability':1,'assumed_value':100,
                                    'actual_payoff_if_omitted_bad_world':-120,
                                    'normalized_pool_mass_is_coverage':False},
            'limits':['Likelihoods, payoffs and costs are stipulated, not empirically calibrated.',
                      'The one-query accuracy is information acquired by an abstract permitted experiment, not a measured LLM accuracy.',
                      'Exact finite sums establish the example only; no general superiority or experimental permission.']}
    def serialize(x):
        if isinstance(x,F):return {'exact':str(x),'decimal':float(x)}
        if isinstance(x,dict):return {k:serialize(v) for k,v in x.items()}
        if isinstance(x,list):return [serialize(v) for v in x]
        return x
    print(json.dumps(serialize(result),indent=2))


if __name__=='__main__':
    main()
