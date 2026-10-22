#!/usr/bin/env python3
"""Exact authored finite target; no vendor runtime or sampling experiment."""
from fractions import Fraction as F
import json


def fraction(value):
    return str(value.numerator) if value.denominator == 1 else str(value)


def calculate():
    # Two stipulated equal-weight cohorts. Effects and cost are USD per customer.
    target = [dict(cohort='A', weight=F(1, 2), effect=F(10), cost=F(1)),
              dict(cohort='B', weight=F(1, 2), effect=F(-30), cost=F(1))]
    gross = sum(row['weight'] * row['effect'] for row in target)
    cost = sum(row['weight'] * row['cost'] for row in target)
    net = gross - cost
    # Independent equal-size finite population accounting, in cents.
    direct_net = F((1000 - 100) + (-3000 - 100), 2 * 100)
    assert net == direct_net == -11 and gross == -10
    observed = [target[0]]
    available = sum(row['weight'] * (row['effect'] - row['cost']) for row in observed)
    available /= sum(row['weight'] for row in observed)
    assert available == 9 and available - net == 20

    variants = []
    for reason in ['failed', 'skipped', 'error_tolerated_without_effect']:
        ledger = [dict(request='effect-A', cohort='A', declared_weight='1/2',
                       disposition='returned', returned_effect_usd='10'),
                  dict(request='effect-B', cohort='B', declared_weight='1/2',
                       disposition=reason, returned_effect_usd=None)]
        assert len(ledger) == 2 and sum(row['returned_effect_usd'] is not None for row in ledger) == 1
        variants.append(dict(illustration=reason, ledger=ledger, requested=2, returned=1,
            returned_fraction='1/2', target_net_identified_from_returns_alone=False,
            available_population_net_usd=fraction(available), target_net_with_stipulated_truth_usd=fraction(net)))

    assumed_bounds = (F(-50), F(50))
    lower, upper = [F(1, 2) * 10 + F(1, 2) * effect - 1 for effect in assumed_bounds]
    assert (lower, upper) == (F(-21), F(29)) and lower <= net <= upper
    # Two table versions can share row count and max date while values change.
    before = [('A', 1, 10), ('B', 2, -30)]
    after = [('A', 1, 10), ('B', 2, 30)]
    proxy = lambda rows: (len(rows), max(row[1] for row in rows))
    assert before != after and proxy(before) == proxy(after) == (2, 2)
    assert F(sum(row[2] for row in after), len(after)) - 1 == 19
    return dict(kind='exact_authored_mathematics', native_execution=False,
        empirical_coverage=False, measured_bank_returns=False,
        target='Fixed all-contact versus no-contact policy; two equal-weight stipulated cohorts',
        assumptions=['Cohort effects +10 and -30 USD per customer are stipulated truth.',
            'Each contacted customer costs 1 USD; no-contact incremental value and cost are zero.',
            'The requested target keeps both cohort weights at one half.',
            'Missing effects are not imputed or treated as random missingness.',
            'Statuses illustrate an authored request ledger; they are not Dataiku run results.'],
        target_gross_usd=fraction(gross), target_cost_usd=fraction(cost), target_net_usd=fraction(net),
        available_population_net_usd=fraction(available), available_minus_target_usd=fraction(available-net),
        variants=variants,
        partial_identification=dict(assumed_missing_effect_bounds_usd=[fraction(x) for x in assumed_bounds],
            target_net_bounds_usd=[fraction(lower), fraction(upper)],
            guaranteed_positive=False, statistical_confidence_interval=False),
        unchanged_query_proxy=dict(before=before, after=after,
            row_count_and_max_date=list(proxy(before)), changed_target_net_usd='19',
            limitation='A logical counterexample for this chosen proxy, not a native trigger experiment.'))


if __name__ == '__main__':
    print(json.dumps(calculate(), indent=2) + '\n')
