#!/usr/bin/env python3
"""Exact authored examples; no external models or package code are executed."""
from fractions import Fraction as F
from math import comb

def calculate():
    independent_error = sum(F(comb(5, k)) * F(1, 10)**k * F(9, 10)**(5-k) for k in range(3, 6))
    utility = {'public_world': {'contact': F(8), 'wait': F(3)},
               'bank_world': {'contact': F(-4), 'wait': F(3)}}
    values = {
        'observation_loss': {'repayment_days': [5, 25], 'ever_repaid': [1, 1],
                             'repaid_by_day_10': [1, 0], 'principal_usd': 10000,
                             'day_10_cash_usd': [10000, 0]},
        'translation': {'goal_strict_max_usd': 100, 'wrong_inclusive_max_usd': 100,
                        'counterexample_cost_usd': 100,
                        'wrong_spec_passes': 100 <= 100, 'true_spec_passes': 100 < 100},
        'judge_error': {'marginal_error': '1/10', 'judges': 5,
                        'independent_majority_error': str(independent_error),
                        'independent_majority_error_decimal': float(independent_error),
                        'shared_majority_error': '1/10'},
        'transport': {'utility_usd': {w: {a: str(v) for a, v in d.items()} for w, d in utility.items()},
                      'public_selected_action': 'contact', 'bank_best_action': 'wait',
                      'bank_regret_usd': str(utility['bank_world']['wait']-utility['bank_world']['contact'])},
        'economics': {'total_usd': 240, 'attempts': 40, 'tool_completed': 30,
                     'accepted_answers': 8, 'correct_refusals': 6,
                     'usd_per_attempt': str(F(240,40)),
                     'usd_per_tool_completion': str(F(240,30)),
                     'usd_per_accepted_answer': str(F(240,8))}
    }
    assert independent_error == F(107,12500)
    assert values['transport']['bank_regret_usd'] == '7'
    assert values['translation']['wrong_spec_passes'] and not values['translation']['true_spec_passes']
    return values

if __name__ == '__main__':
    import json
    print(json.dumps(calculate(), indent=2))
