#!/usr/bin/env python3
"""Exact authored discovery experiments and decision comparisons; no package trial."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-16/s2'


def matmul(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def add(a, b):
    return [[x+y for x, y in zip(u, v)] for u, v in zip(a, b)]


def identity():
    return [[F(i == j) for j in range(3)] for i in range(3)]


def total(b):
    return add(add(identity(), b), matmul(b, b))


def encode(x):
    if isinstance(x, F): return str(x)
    if isinstance(x, dict): return {k: encode(v) for k, v in x.items()}
    if isinstance(x, (tuple, list)): return [encode(v) for v in x]
    return x


def calculate():
    models = {
        'forward': ([[0,0,0],[1,0,0],[0,1,0]],[1,1,1]),
        'reverse': ([[0,F(1,2),0],[0,0,F(2,3)],[0,0,0]],[F(1,2),F(2,3),3]),
        'fork': ([[0,F(1,2),0],[0,0,0],[0,1,0]],[F(1,2),2,1]),
    }
    rows = {}
    for name, (coeff, variance) in models.items():
        b = [[F(x) for x in row] for row in coeff]; l = total(b)
        covariance = [[sum(l[i][k]*F(variance[k])*l[j][k] for k in range(3)) for j in range(3)] for i in range(3)]
        assert covariance == [[1,1,1],[1,2,2],[1,2,3]]
        intervened = [row[:] for row in b]; intervened[1] = [F(0)]*3
        do_m = [row[1] for row in total(intervened)]
        # Separate directed-path enumeration verifies all total coefficients.
        def paths(source, target, visited):
            if source == target: return F(1)
            return sum((b[nxt][source]*paths(nxt,target,visited|{nxt}) for nxt in range(3)
                        if nxt not in visited and b[nxt][source]), F(0))
        path_effect = paths(0,2,{0}); assert path_effect == l[2][0]
        rows[name] = {'B_target_source': b, 'noise_variances': variance, 'covariance': covariance,
                      'effect_X_on_Y': path_effect, 'do_M_one_minus_zero_mean_XMY': do_m,
                      'offer_net_USD': 30*path_effect-8}
    prior_value = sum(r['offer_net_USD'] for r in rows.values())/3
    oracle_value = sum(max(F(0),r['offer_net_USD']) for r in rows.values())/3
    outcome_only = (max(F(0),(rows['forward']['offer_net_USD']+rows['fork']['offer_net_USD'])/2)*2/3)
    assert prior_value == 2 and oracle_value == F(22,3) and outcome_only == F(14,3)
    groups = {}
    for name,r in rows.items():groups.setdefault(str(r['do_M_one_minus_zero_mean_XMY'][2]),[]).append(name)
    maximin = {'offer': min(r['offer_net_USD'] for r in rows.values()), 'decline': F(0)}
    regret = {'offer': max(max(F(0),r['offer_net_USD'])-r['offer_net_USD'] for r in rows.values()),
              'decline': max(max(F(0),r['offer_net_USD']) for r in rows.values())}
    # Cancellation law X=U, M=X+V, Y=(-1+epsilon)X+M+W.
    cancellation = []
    for eps in [F(0),F(1,20),-F(1,20)]:
        total_effect = (-1+eps)+1
        cancellation.append({'epsilon':eps,'direct_effect':-1+eps,'indirect_effect':F(1),
                             'total_effect':total_effect,'cov_XY':eps,'offer_net_USD':30*total_effect-8})
    # Exact selection table: X,U independent fair bits, Y=U, retained only when X=U.
    selected = [{'X':x,'U':u,'Y':u,'probability':F(1,4),'selected':x==u} for x,u in product([0,1],repeat=2)]
    assert sum(r['probability'] for r in selected if r['selected']) == F(1,2)
    # Fixed two-period impulse; average and endpoint are distinct estimands.
    impulse = [F(1),-F(1,2)]; average = sum(impulse)/2
    return encode({'status':'exact_authored_examples','evidence_class':'generated structural laws and stipulated decision costs, not upstream or bank results',
        'chain':rows,'common_covariance':[[1,1,1],[1,2,2],[1,2,3]],'effect_set':[0,1],
        'decision':{'stipulated_model_weights':[F(1,3)]*3,'current_expected_optimal_value_USD':prior_value,
                    'perfect_model_information_value_USD':oracle_value,'incremental_joint_information_USD':oracle_value-prior_value,
                    'Y_only_post_intervention_value_USD':outcome_only,'incremental_Y_only_information_USD':outcome_only-prior_value,
                    'Y_only_groups':groups,'joint_M_intervention_identifies_three_fixed_models':True,
                    'maximin_values':maximin,'maximum_regrets':regret,
                    'limit':'Ideal population contrasts and stipulated model weights; no finite-sample experimental power, observed cost or ROI'},
        'cancellation':cancellation,'selection':{'rows':selected,'selected_probability':F(1,2),
                    'selected_conditional_contrast':1,'population_do_contrast':0},
        'clock':{'rho':-F(1,2),'impulse':impulse,'two_period_average':average,'endpoint':impulse[-1],
                 'USD_per_unit':40,'stipulated_cost_USD':3,'average_net_USD':40*average-3,'endpoint_net_USD':40*impulse[-1]-3},
        'independent_checks':['Structural total matrix I+B+B^2 agrees with separate directed-path enumeration.',
                              'All three Gaussian covariance matrices agree exactly.',
                              'Rational selection enumeration, conditional decision grouping and impulse arithmetic use no implementation solver.']})


if __name__ == '__main__':
    with (BASE/'exact-results.json').open('x') as f:json.dump(calculate(),f,indent=2);f.write('\n')
    print(json.dumps({'exact_examples':'pass','families':4,'upstream_execution':False}))
