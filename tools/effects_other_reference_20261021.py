#!/usr/bin/env python3
"""Authored finite-law references; no upstream engine executed or simulated."""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
import json


def calculate():
    # Known nuisance means, independent units, binary treatment, no hidden confounding.
    e, tau = (F(1, 2), F(1, 10)), (F(-4), F(12))
    numerator = denominator = ate = att_num = treated = F(0)
    for w, a in product(range(2), repeat=2):
        p = F(1, 2)*(e[w] if a else 1-e[w])
        y, mean_y = a*tau[w], e[w]*tau[w]
        numerator += p*(a-e[w])*(y-mean_y)
        denominator += p*(a-e[w])**2
        att_num += p*a*tau[w]
        treated += p*a
    ate = sum(tau)/2
    slope = numerator/denominator
    assert (ate, slope, att_num/treated) == (F(4), F(4, 17), F(-4, 3))

    # MCAR is not needed for MAR; different response rates change the marginal population.
    rho = (F(9, 10), F(1, 10))
    responded = selected_effect = response_adjusted = F(0)
    for w, a, r in product(range(2), repeat=3):
        p = F(1, 4)*(rho[w] if r else 1-rho[w])
        responded += p*r
        selected_effect += p*r*tau[w]
        y = a*tau[w]
        response_adjusted += p*r*(2*a*y-2*(1-a)*y)/rho[w]
    complete = selected_effect/responded
    assert complete == F(-12, 5) and response_adjusted == ate

    # Exact dimensional witness for the scalar expression in the selected source.
    draws, effect = tuple(map(F, [-1, -1, 1, 1])), F(2)
    reported = sum((effect-z)**2 for z in draws)/3/2
    scaled = sum((100*effect-100*z)**2 for z in draws)/3/2
    assert reported == F(10, 3) and scaled/reported == 10000
    assignments = list(product(range(2), repeat=4))
    count_one = F(sum(sum(a)==1 for a in assignments), 16)
    no_comparison_arm = F(sum(sum(a) in (0, 4) for a in assignments), 16)
    assert (count_one, no_comparison_arm) == (F(1, 4), F(1, 8))

    # Two supplied structural models give the same observed law, but different interventions.
    observed = []
    effects = []
    for model in ['causal', 'confounded']:
        law = defaultdict(F)
        intervention_difference = F(0)
        for u in range(2):
            a = u
            y = a if model == 'causal' else u
            law[(a, y)] += F(1, 2)
            intervention_difference += F(1, 2)*((1-0) if model == 'causal' else (u-u))
        observed.append(dict(law)); effects.append(intervention_difference)
    assert observed[0] == observed[1] and effects == [F(1), F(0)]

    # Influence-function standard deviation versus standard error, independently calculated.
    influence = tuple(map(F, [-3, -1, 1, 3]))
    mean_ic = sum(influence)/4
    sample_variance = sum((z-mean_ic)**2 for z in influence)/3
    se_squared = sample_variance/4
    assert (sample_variance, se_squared) == (F(20, 3), F(5, 3))

    return dict(
        scope='Exact project-authored laws; no Julia execution, fitted learner, empirical coverage or bank observation',
        residual_target=dict(ate=str(ate), att=str(att_num/treated), residual_slope=str(slope),
            numerator=str(numerator), denominator=str(denominator), cost='2',
            ate_margin=str(ate-2), residual_margin=str(slope-2)),
        response_selection=dict(population_ate=str(ate), complete_case_average=str(complete),
            response_adjusted=str(response_adjusted), response_probability=str(responded),
            complete_case_margin=str(complete-2), population_margin=str(ate-2)),
        dimensional_check=dict(reported=str(reported), outcome_scale='100', reported_scale=str(scaled/reported),
            standard_error_required_scale='100'),
        assignment_law=dict(uniform_binary_probability_one_treated=str(count_one),
            fixed_one_design_probability_one_treated='1', uniform_binary_probability_empty_arm=str(no_comparison_arm)),
        supplied_scm=dict(observed_laws_equal=True, observed_atoms={'0,0':'1/2','1,1':'1/2'},
            intervention_effects=list(map(str,effects)), cost='1/2', margins=[str(v-F(1,2)) for v in effects]),
        influence_scale=dict(sample_variance=str(sample_variance), n=4, se_squared=str(se_squared)))


if __name__ == '__main__':
    print(json.dumps(calculate(), indent=2))
