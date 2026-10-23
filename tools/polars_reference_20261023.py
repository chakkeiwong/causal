#!/usr/bin/env python3
"""Exact authored data-contract witnesses; no Polars code is imported."""
from fractions import Fraction as F
from itertools import product
import json

def q(x):
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"

def mean(xs):
    return sum(xs, F(0)) / len(xs)

def calculate():
    customers = [['A', 1, 10], ['B', 1, 0], ['C', 0, 0], ['D', 0, 0]]
    events = ['A', 'A', 'A', 'B', 'C', 'D']
    joined = [r for r in customers for key in events if r[0] == key]
    contrast = lambda rows: mean([F(r[2]) for r in rows if r[1] == 1]) - mean([F(r[2]) for r in rows if r[1] == 0])
    before, after = contrast(customers), contrast(joined)
    assert before == 5 and after == F(15, 2)
    cost = F(6)
    # These are descriptive contrasts and stipulated cost comparisons, not ATEs.
    observed = [F(2), F(4)]
    observed_mean = mean(observed)
    possible_full_means = [mean(observed + [F(v)]) for v in [0,8]]
    assert observed_mean == 3 and possible_full_means == [F(2),F(14,3)]
    decision = 100
    records = [dict(event=90,available=105,value=0),dict(event=80,available=85,value=4),dict(event=101,available=101,value=10)]
    event_backward = max((r for r in records if r['event']<=decision),key=lambda r:r['event'])
    nearest = min(records,key=lambda r:abs(r['event']-decision))
    eligible = max((r for r in records if r['event']<=decision and r['available']<=decision),key=lambda r:r['event'])
    assert [event_backward['value'],nearest['value'],eligible['value']] == [0,10,4]
    draws = [(F(x+y,2),F(y+z,2)) for x,y,z in product([-1,1],repeat=3)]
    assert mean([a for a,b in draws]) == mean([b for a,b in draws]) == 0
    va=mean([a*a for a,b in draws]);vb=mean([b*b for a,b in draws]);cov=mean([a*b for a,b in draws])
    actual=mean([((a+b)/2)**2 for a,b in draws]);independent=(va+vb)/4
    assert va==vb==F(1,2) and cov==F(1,4) and actual==F(3,8) and independent==F(1,4)
    return dict(provenance='Project-owned exact examples under supplied laws; no native execution or causal qualification',
        fanout=dict(customer_rows=customers,event_ids=events,joined_rows=len(joined),customer_contrast=q(before),event_weighted_contrast=q(after),stipulated_cost=q(cost),customer_margin=q(before-cost),event_weighted_margin=q(after-cost)),
        missing=dict(observed=observed_mean.numerator,zero_imputed=q(possible_full_means[0]),possible_full_means=[q(v) for v in possible_full_means],unobserved_values=[0,8]),
        information_clock=dict(decision=decision,records=records,event_backward=event_backward,nearest=nearest,available_backward=eligible),
        overlapping_windows=dict(independent_sign_draws=len(draws),window_variance=q(va),covariance=q(cov),mean_variance=q(actual),incorrect_independence_variance=q(independent),ratio=q(actual/independent)))

if __name__ == '__main__':
    print(json.dumps(calculate(),indent=2))
