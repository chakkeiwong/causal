#!/usr/bin/env python3
"""Exact proposal arithmetic for a hypothetical software comparison."""
from fractions import Fraction as F
import json
from pathlib import Path


def calculate():
    paths = {
        'A': {'valid_answers': 54, 'invalid_answers': 8, 'eligible_failures': 6,
              'justified_refusals': 32, 'operating_cost': 400},
        'B': {'valid_answers': 48, 'invalid_answers': 0, 'eligible_failures': 12,
              'justified_refusals': 40, 'operating_cost': 600},
    }
    for x in paths.values():
        assert x['valid_answers'] + x['eligible_failures'] == 60
        assert x['invalid_answers'] + x['justified_refusals'] == 40
        x['eligible_availability'] = float(F(x['valid_answers'], 60))
        x['false_acceptance'] = float(F(x['invalid_answers'], 40))
        x['all_request_valid_answer_rate'] = float(F(x['valid_answers'], 100))
    value = 100
    difference_before_harm = (paths['A']['valid_answers'] - paths['B']['valid_answers']) * value - (
        paths['A']['operating_cost'] - paths['B']['operating_cost'])
    harm_break_even = F(difference_before_harm, 8)
    assert harm_break_even == 100
    assert 54 * value - 8 * harm_break_even - 400 == 48 * value - 600 == 4200
    return {
        'evidence_kind': 'exact_project_planning_calculation',
        'observed_benchmark': False,
        'bank_roi_claim': False,
        'requests': {'total': 100, 'eligible': 60, 'ineligible': 40},
        'paths': paths,
        'scenario': {'value_per_valid_answer': value, 'currency_unit': 'hypothetical_currency',
                     'harm_break_even_per_invalid_answer': float(harm_break_even),
                     'net_value_at_break_even': 4200,
                     'interpretation': 'A exceeds B only below this harm under these stipulated counts and costs.'},
        'limitations': ['Invented service counts and costs, not package measurements or vendor prices.',
                       'Expected harm and benefit are decision assumptions; no causal calibration is implied.'],
    }


if __name__ == '__main__':
    target = Path(__file__).resolve().parents[1] / 'docs/program/execution/2026-10-13/survey-comparison.json'
    target.write_text(json.dumps(calculate(), indent=2) + '\n')
    print(json.dumps(calculate()['scenario']))
