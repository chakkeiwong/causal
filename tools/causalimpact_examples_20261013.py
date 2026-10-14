#!/usr/bin/env python3
"""Exact authored examples of forecast attribution and output semantics, not an engine run."""
from fractions import Fraction as F
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1] / 'docs/program/execution/2026-10-13/causalimpact-reuse'


def q7(values, p):
    """Exact type-7 empirical quantile, for the stated finite draw construction."""
    values = sorted(map(F, values))
    h = (len(values) - 1) * F(p)
    j = h.numerator // h.denominator
    return values[j] if j == len(values) - 1 else values[j] + (h-j)*(values[j+1]-values[j])


def calculate():
    # Two structural laws agree on every observed row. The intervention changes
    # a donor in law A, but leaves it unaffected in law B.
    rows = []
    for t in range(1, 13):
        a = int(t > 8)
        x0 = 10 + t
        x = x0 + 15*a
        y = 100 + 2*x0 + 20*a
        law_b_y = 100 + 2*x - 10*a
        assert y == law_b_y
        forecast = 100 + 2*x
        assert y-forecast == -10*a
        rows.append(dict(t=t,treated=a,observed_x=x,observed_y=y,
                         forecast=forecast,law_a_controlled_effect=20*a,
                         law_b_controlled_effect=-10*a))
    effect_a = sum(r['law_a_controlled_effect'] for r in rows)
    effect_b = sum(r['law_b_controlled_effect'] for r in rows)
    assert effect_a == 80 and effect_b == -40

    # These are hand-constructed dependent predictive draws, not an MCMC sample.
    draws = [[80,120],[120,80],[80,120],[120,80]]
    alpha = F(1,20)
    point_intervals = [[q7([r[t] for r in draws],alpha/2),
                        q7([r[t] for r in draws],1-alpha/2)] for t in range(2)]
    cumulative = [q7([sum(r) for r in draws],p) for p in [alpha/2,1-alpha/2]]
    naive_sum = [sum(x[j] for x in point_intervals) for j in range(2)]
    assert point_intervals == [[80,120],[80,120]]
    assert cumulative == [200,200] and naive_sum == [160,240]
    actual_sum = 220
    effect_interval = [actual_sum-cumulative[1], actual_sum-cumulative[0]]
    assert effect_interval == [20,20]
    p_tail = F(min(sum(s >= actual_sum for s in [sum(r) for r in draws]+[actual_sum]),
                   sum(s <= actual_sum for s in [sum(r) for r in draws]+[actual_sum])),len(draws)+1)
    assert p_tail == F(1,5)

    counterfactual = [F(-1),F(1),F(2)]
    ratios = [F(10)/x-1 for x in counterfactual]
    mean_ratio = sum(ratios)/3
    ratio_of_means = F(10)/(sum(counterfactual)/3)-1
    assert ratios == [-11,9,4] and mean_ratio == F(2,3) and ratio_of_means == 14
    # Snapshot balance effects are thousands of dollars at three dates.
    stocks = [10,10,10]
    assert sum(stocks) == 30 and stocks[-1] == 10
    return {
        'kind':'exact_project_constructions',
        'engine_executed':False,
        'contamination':{'rows':rows,'same_observed_rows':12,'pre_fit_residuals':[0]*8,
            'four_day_true_flow_effect_law_a':effect_a,'four_day_true_flow_effect_law_b':effect_b,
            'formula':'observed forecast contrast = tau - beta*gamma',
            'law_a':{'beta':2,'donor_effect':15,'response_effect':20},
            'law_b':{'beta':2,'donor_effect':0,'response_effect':-10},
            'stipulated_four_day_program_cost':20,
            'net_value_law_a':effect_a-20,'net_value_law_b':effect_b-20,
            'limit':'Law B exogenous donor path is the observed path, including its post-date shift. No finite-data estimator distinguishes the two observationally identical laws without restrictions.'},
        'dependent_draws':{'draws':draws,'marginal_intervals':point_intervals,
            'correct_sum_interval':cumulative,'sum_of_marginal_endpoints':naive_sum,
            'actual_sum':actual_sum,'effect_interval':effect_interval,
            'one_sided_tail_area_with_observed_draw':p_tail,
            'limit':'Finite artificial draws illustrate transformations, not posterior convergence or frequentist coverage.'},
        'relative_effect':{'counterfactual_totals':counterfactual,'actual_total':10,
            'draw_ratios':ratios,'mean_of_ratios':mean_ratio,'ratio_of_means':ratio_of_means,
            'zero_denominator':'undefined; no invented finite ratio'},
        'stocks':{'snapshot_effects_thousand_USD':stocks,'end_date_effect_thousand_USD':10,
            'sum_of_snapshots_thousand_USD_days':30,
            'limit':'A sum of daily balances is an exposure-time quantity; it is not USD30000 of new funding or revenue.'}}


def serial(value):
    if isinstance(value,F):
        return value.numerator if value.denominator == 1 else str(value)
    if isinstance(value,dict):
        return {k:serial(v) for k,v in value.items()}
    if isinstance(value,list):
        return [serial(v) for v in value]
    return value


if __name__ == '__main__':
    path = BASE/'exact-results.json'
    data = serial(calculate())
    if path.exists():
        assert json.loads(path.read_text()) == data
    else:
        path.write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({'exact_replay':'pass','same_observed_rows':12,
                      'net_values':[60,-60],'native_engine_run':False}))
