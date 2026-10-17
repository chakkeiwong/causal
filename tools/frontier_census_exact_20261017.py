#!/usr/bin/env python3
"""Authored exact laws; no model calls, package trials or observed banking data."""
from fractions import Fraction as F


def calculate():
    initial = [F(3, 5), F(1, 5), F(1, 5)]
    transition = [[F(9, 10), F(1, 20), F(1, 20)],
                  [F(1, 5), F(3, 10), F(1, 2)],
                  [F(1, 10), F(3, 5), F(3, 10)]]
    final = [sum(initial[i]*transition[i][j] for i in range(3)) for j in range(3)]
    correction = sum(initial[i]*transition[i][0] for i in [1, 2])/(1-initial[0])
    wrong_switch = sum(initial[i]*(1-transition[i][i]) for i in [1, 2])/(1-initial[0])
    bad_flip = 1-transition[0][0]
    correct_identity = initial[0]*(1-bad_flip)+(1-initial[0])*correction
    invalid_multiclass_identity = initial[0]*(1-bad_flip)+(1-initial[0])*wrong_switch
    assert final[0] == correct_identity == F(3, 5)
    assert wrong_switch == F(7, 10) and correction == F(3, 20)
    assert invalid_multiclass_identity == F(41, 50)
    # Source-reported rounded L2 (binary) values: consistency check, not raw-data reconstruction.
    rows = [('historical_table_row_1', F('0.878'), F('0.127'), F('0.649'), F('0.845')),
            ('historical_table_row_2', F('0.980'), F('0.379'), F('0.333'), F('0.615')),
            ('historical_table_row_3', F('0.967'), F('0.752'), F('1.000'), F('0.273'))]
    table = []
    for label, p, b, c, reported in rows:
        implied = p*(1-b)+(1-p)*c
        assert abs(implied-reported) <= F(1, 1000)
        table.append(dict(row=label, implied=implied, reported=reported,
                          absolute_rounding_difference=abs(implied-reported)))
    worlds = []
    for name, alpha, beta, tau in [('positive', F(7,20),F(1,5),F(1,10)),
                                    ('zero', F(3,10),F(2,5),F(0)),
                                    ('negative', F(1,4),F(3,5),-F(1,10))]:
        joint = {(a,y):F(0) for a in [0,1] for y in [0,1]}
        response = {}
        for u in [0,1]:
            pa = F(1,4)+F(1,2)*u
            for a in [0,1]:
                py = alpha+beta*u+tau*a
                assert 0 < py < 1
                response[f'{u},{a}'] = py
                for y in [0,1]:
                    joint[a,y] += F(1,2)*(pa if a else 1-pa)*(py if y else 1-py)
        means = [alpha+beta/2+tau*a for a in [0,1]]
        assert means[1]-means[0] == tau
        # Independent exogenous-uniform threshold enumeration, not the same marginal formula.
        empirical = {(a,y):F(0) for a in [0,1] for y in [0,1]}
        intervention = [F(0),F(0)]
        for u in [0,1]:
            for e_a in range(4):
                a = int(F(2*e_a+1,8) < F(1,4)+F(1,2)*u)
                for e_y in range(20):
                    y = int(F(2*e_y+1,40) < response[f'{u},{a}'])
                    empirical[a,y] += F(1,160)
                    for do_a in [0,1]:
                        intervention[do_a] += F(int(F(2*e_y+1,40) < response[f'{u},{do_a}']),160)
        assert joint == empirical and means == intervention
        worlds.append(dict(name=name,alpha=alpha,beta=beta,tau=tau,
            observed_joint={f'{a},{y}':v for (a,y),v in joint.items()},
            outcome_probabilities=response,interventional_means=means,
            stipulated_net_usd=100*tau-5))
    assert all(w['observed_joint']==worlds[0]['observed_joint'] for w in worlds)
    assert all(v>0 for v in worlds[0]['observed_joint'].values())
    return dict(multiclass=dict(initial=initial,transition=transition,final=final,
        correction=correction,wrong_switch=wrong_switch,bad_flip=bad_flip,
        correct_final_accuracy=correct_identity,invalid_final_accuracy=invalid_multiclass_identity),
        binary_reported_table=table,confounded_worlds=worlds,
        checks=['Exact transition normalization and final law',
                'Wrong-label switch differs from correction in three-label example',
                'Published binary table agrees within reported rounding',
                'Three positive observed laws identical with positive, zero and negative effects',
                'Independent threshold enumeration agrees for observed and intervention laws'],
        limitations=['Project constructions and source rounding check only; no empirical accuracy, bank ROI or upstream execution.'])


def serial(value):
    if isinstance(value,F):return str(value)
    if isinstance(value,dict):return {k:serial(v) for k,v in value.items()}
    if isinstance(value,list):return [serial(v) for v in value]
    return value


if __name__=='__main__':
    import json
    print(json.dumps(serial(calculate()),indent=2))
