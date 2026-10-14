#!/usr/bin/env python3
"""Exact treatment-version planning illustration; no empirical study."""
from fractions import Fraction as F
import json


def main():
    baseline = F(2, 5)
    success = [F(21, 50), F(3, 5)]
    cost = [F(10), F(100)]
    rows = []
    for high_share in (F(1, 4), F(3, 4)):
        weights = [1 - high_share, high_share]
        treated = sum(w * y for w, y in zip(weights, success))
        expense = sum(w * c for w, c in zip(weights, cost))
        effect = treated - baseline
        rows.append({'high_version_share': high_share, 'effect': effect,
                     'expected_cost_usd': expense, 'gross_value_usd': 1000 * effect,
                     'net_value_usd': 1000 * effect - expense})
    assert rows[0]['effect'] == F(13, 200)
    assert rows[1]['effect'] == F(31, 200)
    assert rows[0]['net_value_usd'] == F(65, 2)
    assert rows[1]['net_value_usd'] == F(155, 2)
    print(json.dumps({'kind': 'stipulated_treatment_version_example', 'random_draws': 0,
                      'bank_data': False, 'baseline_success': baseline,
                      'version_success': success, 'version_cost_usd': cost,
                      'regimes': rows}, indent=2, default=str))


if __name__ == '__main__':
    main()
