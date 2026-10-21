#!/usr/bin/env python3
"""Exact authored laws: identification, information clocks and numerical error.

No vendor engine or downloaded code is imported or executed. These are specified
population examples, not empirical performance or bank evidence.
"""
from fractions import Fraction as F
from itertools import product
import json


def calculate():
    laws = {name: {(a, d): F(0) for a, d in product(range(2), repeat=2)}
            for name in ['selection', 'causal']}
    for u, noise in product(range(2), repeat=2):
        weight = F(1, 2) * (F(1, 5) if noise else F(4, 5))
        laws['selection'][u ^ noise, 1-u] += weight
        laws['causal'][u, (1-u) ^ noise] += weight
    assert laws['selection'] == laws['causal']
    joint = laws['selection']
    conditional = [sum(p for (a, d), p in joint.items() if a == v and d == 1) /
                   sum(p for (a, _), p in joint.items() if a == v) for v in range(2)]
    # Intervene by replacing only the action equation in each original law.
    risks = {}
    for name in laws:
        risks[name] = []
        for action in range(2):
            risk = F(0)
            for u, noise in product(range(2), repeat=2):
                weight = F(1, 2) * (F(1, 5) if noise else F(4, 5))
                default = 1-u if name == 'selection' else (1-action) ^ noise
                risk += weight * default
            risks[name].append(risk)
    benefits = {k: v[0]-v[1] for k, v in risks.items()}
    assert benefits == dict(selection=F(0), causal=F(3, 5))
    prior_rows = []
    for w in [F(1, 10), F(9, 10)]:
        # Every observed cell has exactly the same likelihood in both models.
        posterior = w*joint[1, 0] / (w*joint[1, 0]+(1-w)*joint[1, 0])
        assert posterior == w
        prior_rows.append(dict(prior_causal=w, posterior_causal=posterior,
                              expected_benefit=F(3, 5)*w,
                              net_usd=1000*F(3, 5)*w-100))
    # H is a persistent hidden state; X0 and X1 are independent given H.
    triples = {}
    for h, x0, x1 in product(range(2), repeat=3):
        triples[h, x0, x1] = F(1, 2) * (F(3, 4) if x0 == h else F(1, 4)) * (
            F(3, 4) if x1 == h else F(1, 4))
    filtered = sum(p for (h, x0, x1), p in triples.items() if h == 1 and x0 == 1) / sum(
        p for (h, x0, x1), p in triples.items() if x0 == 1)
    smoothed = triples[1, 1, 0] / (triples[1, 1, 0]+triples[0, 1, 0])
    assert (filtered, smoothed) == (F(3, 4), F(1, 2))
    assert filtered == F(3, 4)/(F(3, 4)+F(1, 4))
    assert smoothed == (F(3, 4)*F(1, 4))/(2*F(3, 4)*F(1, 4))
    # Observability example, A=.9 I, H=(1,1), noise-free outputs.
    outputs = [[F(9, 10)**t * sum(z) for t in range(8)] for z in [(1, 0), (2, -1)]]
    assert outputs[0] == outputs[1]
    assert F(1)*F(9, 10)-F(1)*F(9, 10) == 0  # determinant of [H;HA]
    # Uniform theta: integrate its first two moments exactly.
    etheta, etheta2 = F(1, 2), F(1, 3)
    within, between = etheta-etheta2, etheta2-etheta**2
    count_var = 2*within+4*between
    assert within+between == F(1, 4) and count_var == F(2, 3)
    weighted_mean = (9*F(1,10)+F(9,10))/10
    expanded_mean = sum([F(1,10)]*9+[F(9,10)])/10
    assert weighted_mean == expanded_mean == F(9,50)
    gamma, horizon, tv, span = F(9, 10), 12, F(1, 50), 100
    total_bound = span*tv*sum(gamma**t for t in range(horizon))
    assert total_bound == span*tv*(1-gamma**horizon)/(1-gamma)
    result = dict(
        evidence_kind='project_authored_exact_population_laws', vendor_runtime=False,
        observational_equivalence=dict(joint={f'{a},{d}':p for (a,d),p in joint.items()},
            conditional_default=conditional, intervention_risks=risks, default_reductions=benefits,
            loss_usd=1000, action_cost_usd=100, net_usd={k:1000*v-100 for k,v in benefits.items()},
            prior_sensitivity=prior_rows, break_even_prior=F(1,6)),
        information_clock=dict(filtered=filtered, smoothed=smoothed,
            action_default_reduction_when_h1=F(1,10), loss_usd=1000, action_cost_usd=60,
            filtered_net_usd=100*filtered-60, smoothed_net_usd=100*smoothed-60),
        observability=dict(A_diagonal=F(9,10), H=[1,1], rank=1, null_vector=[1,-1],
            initial_states=[[1,0],[2,-1]], identical_outputs=outputs[0], contrasts=[1,3]),
        uncertainty=dict(theta_prior='Uniform(0,1)', expected_conditional_variance=within,
            parameter_variance=between, single_predictive_variance=within+between,
            two_outcome_count_variance=count_var, plug_in_count_variance=F(1,2)),
        compressed_chain=dict(values=[F(1,10),F(9,10)],frequencies=[9,1],
            weighted_mean=weighted_mean,unweighted_row_mean=F(1,2)),
        approximation=dict(same_fixed_policy=True, marginal_tv_bound=tv, reward_range_usd=span,
            discount=gamma,horizon=horizon,discounted_value_error_bound_usd=total_bound,
            example_true_p=F(61,100),example_approx_p=F(59,100),action_cost_usd=60,
            true_net_usd=F(1),approximate_net_usd=F(-1)),
        limitations=['Assumed mechanisms and monetary inputs; no empirical estimation or measured bank economics.',
                    'Marginal TV bound is an assumption, not a guarantee supplied by a native inference engine.',
                    'State observability, parameter identification and causal identification are distinct.'])
    return json.loads(json.dumps(result,default=lambda x:str(x) if isinstance(x,F) else x))


if __name__ == '__main__':
    print(json.dumps(calculate(),indent=2))
