#!/usr/bin/env python3
"""Exhaustive authored policy/censoring law and exact covariance reference.

No upstream code is executed. The failed probability law is retained in
ltmle-reuse-v1/failed-draft-1; this successor validates every binary history.
"""
from fractions import Fraction as F
from itertools import product
import json


def mean(xs):
    return sum(xs, F()) / len(xs)


def covariance(xs, ys):
    return sum((x - mean(xs)) * (y - mean(ys)) for x, y in zip(xs, ys)) / (len(xs) - 1)


def p_hardship(h, a0):
    return {(0, 0): F(1, 4), (0, 1): F(1, 8),
            (1, 0): F(3, 4), (1, 1): F(1, 2)}[h, a0]


def p_default(h, a0, l, a1):
    return F(1, 10) + F(h, 10) + F(l, 5) - F(a0, 25) - F(a1, 20)


def calculate():
    probabilities = [p_default(*z) for z in product((0, 1), repeat=4)]
    assert min(probabilities) == F(1, 100) and max(probabilities) == F(2, 5)
    policies = {
        'status_quo': (lambda h: 0, lambda l: 0),
        'targeted_dynamic': (lambda h: h, lambda l: l),
        'broad_contact': (lambda h: 1, lambda l: 1),
    }
    risks, results = {}, {}
    # A separately calculated moment identity checks the path enumeration.
    expected = {
        'status_quo': (F(5, 12), F(0), F(0)),
        'targeted_dynamic': (F(1, 3), F(1, 3), F(1, 3)),
        'broad_contact': (F(1, 4), F(1), F(1)),
    }
    for name, (d0, d1) in policies.items():
        risk = observed_mass = observed_default = contact_cost = ipcw = F()
        mass = F()
        for h, l in product((0, 1), repeat=2):
            ph = F(1, 3) if h else F(2, 3)
            a0, a1 = d0(h), d1(l)
            pl = p_hardship(h, a0)
            path = ph * (pl if l else 1 - pl)
            py = p_default(h, a0, l, a1)
            pc = F(3, 4) if l else F(9, 10)
            risk += path * py
            contact_cost += path * (6 * a0 + 4 * a1)
            # C=1 means observed; C and Y independent conditional on history.
            for c, y in product((0, 1), repeat=2):
                joint = path * (pc if c else 1-pc) * (py if y else 1-py)
                assert joint >= 0
                mass += joint
                observed_mass += joint * c
                observed_default += joint * c * y
                ipcw += joint * c * y / pc
        el, ea0, ea1 = expected[name]
        moment_risk = F(1, 10) + F(1, 30) + el/5 - ea0/25 - ea1/20
        assert mass == 1 and risk == moment_risk == ipcw
        assert contact_cost == 6 * ea0 + 4 * ea1
        risks[name] = risk
        results[name] = dict(default_probability=str(risk), observed_probability=str(observed_mass),
            complete_case_default_probability=str(observed_default/observed_mass),
            complete_case_bias=str(observed_default/observed_mass - risk),
            ipcw_population_identity=str(ipcw), expected_contacts=[str(ea0), str(ea1)],
            expected_contact_cost_usd=str(contact_cost), total_probability=str(mass),
            independent_moment_identity=str(moment_risk))
    for name, result in results.items():
        avoided = 1000*(risks['status_quo']-risks[name])
        result['avoided_default_loss_vs_status_quo_usd'] = str(avoided)
        result['net_value_vs_status_quo_usd'] = str(avoided-F(result['expected_contact_cost_usd']))
    assert [risks[x] for x in policies] == [F(13, 60), F(17, 100), F(7, 75)]
    assert [results[x]['net_value_vs_status_quo_usd'] for x in policies] == ['0', '130/3', '340/3']

    # Four hypothetical household influence pairs, with two identical records
    # per household. These are a covariance fixture, not estimated package ICs.
    x = list(map(F, [-3, -1, 1, 3]))
    y = list(map(F, [-2, 0, 0, 2]))
    diff = [a-b for a, b in zip(x, y)]
    n = len(x)
    cov = [[covariance(a, b)/n for b in (x, y)] for a in (x, y)]
    joint_contrast = cov[0][0]+cov[1][1]-2*cov[0][1]
    direct_contrast = covariance(diff, diff)/n
    duplicate_x = [a for a in x for _ in range(2)]
    row_variance = covariance(duplicate_x, duplicate_x)/len(duplicate_x)
    assert joint_contrast == direct_contrast == F(1, 3)
    assert cov[0][0] == F(5, 3) and row_variance == F(5, 7)
    return dict(status='exact_authored_reference_not_native_execution',
        law=dict(P_H1='1/3', P_hardship={'0,0':'1/4','0,1':'1/8','1,0':'3/4','1,1':'1/2'},
            P_default='1/10 + H/10 + L1/5 - A0/25 - A1/20',
            P_observed={'L1=0':'9/10','L1=1':'3/4'},
            censoring_condition='C independent of Y given H,A0,L1,A1; C=1 observed',
            default_loss_usd=1000, contact_costs_usd=[6,4],
            policies={'status_quo':'A0=0,A1=0','targeted_dynamic':'A0=H,A1=L1','broad_contact':'A0=1,A1=1'}),
        probability_validation=dict(binary_histories=16, minimum_default_probability=str(min(probabilities)),
            maximum_default_probability=str(max(probabilities)), total_mass_each_policy='1', independent_moment_checks='pass'),
        results=results,
        covariance_fixture=dict(household_pairs=[[str(a),str(b)] for a,b in zip(x,y)],
            records_per_household=2, covariance_of_means=[[str(v) for v in row] for row in cov],
            joint_contrast_variance=str(joint_contrast), direct_contrast_variance=str(direct_contrast),
            incorrectly_dropping_covariance=str(cov[0][0]+cov[1][1]),
            household_variance=str(cov[0][0]), iid_row_variance=str(row_variance),
            exact_variance_ratio=str(cov[0][0]/row_variance),
            independent_units=4, nominal_rows=8,
            scope='Exact sample covariance fixture; no package influence curves or coverage claim.'),
        limitations=['A stipulated law defines mathematical truth, not bank returns.',
            'Population IPCW identity uses known observation probabilities and is not a fitted estimator trial.',
            'Nuisance fitting, treatment support in logged data, sequential exchangeability and calibration remain separate.',
            'Four household pairs illustrate covariance algebra and do not justify a small-sample confidence approximation.'])


if __name__ == '__main__':
    print(json.dumps(calculate(), indent=2))
