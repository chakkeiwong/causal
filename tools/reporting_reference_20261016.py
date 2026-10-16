#!/usr/bin/env python3
"""Exact authored reporting examples; no model, bank, or upstream execution."""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-16/reporting-monitoring'


def calculate():
    gross = {0, 100}
    net = sorted(x - 40 for x in gross)
    midpoint = F(sum(net), len(net))
    counts = {'computed_correct': 48, 'computed_incorrect': 12,
              'ambiguous': 20, 'unsupported': 10, 'retrieval_failure': 10}
    assert sum(counts.values()) == 100
    # Equiprobable cases, fixed true value, and a stipulated acceptance event.
    intervals = [(0, 1)] * 95 + [(2, 3)] * 5
    covers = [lo <= F(1, 2) <= hi for lo, hi in intervals]
    accepted = list(range(5)) + list(range(95, 100))
    marginal = F(sum(covers), len(covers))
    selective = F(sum(covers[i] for i in accepted), len(accepted))
    tmax = 12
    no_alarm = F(19, 20) ** tmax
    one_or_more = sum(F(comb(tmax, k)) * F(1, 20)**k * F(19, 20)**(tmax-k)
                      for k in range(1, tmax+1))
    assert one_or_more == 1 - no_alarm
    spending = sum(F(1, 20*t*(t+1)) for t in range(1, tmax+1))
    assert spending == F(tmax, 20*(tmax+1))
    # This graph expresses proposed semantic dependencies, not a causal DAG.
    parents = {'design': {'clock', 'assignment'}, 'estimate': {'design', 'cohort'},
               'economics': {'estimate', 'price'}, 'report': {'economics', 'estimate'},
               'other_estimate': {'other_cohort'}}
    def affected(start):
        reached = {start}
        while True:
            more = {k for k, v in parents.items() if v & reached}
            if more <= reached:
                return sorted(reached - {start})
            reached |= more
    changes = {k: affected(k) for k in ['clock', 'assignment', 'price', 'other_cohort']}
    assert changes['price'] == ['economics', 'report']
    assert changes['clock'] == ['design', 'economics', 'estimate', 'report']
    assert changes['other_cohort'] == ['other_estimate']
    return {
        'evidence_kind': 'executed_exact_project_derivation',
        'set_reporting': {'gross_usd': sorted(gross), 'cost_usd': 40, 'net_usd': net,
                          'midpoint_usd': str(midpoint), 'midpoint_in_set': midpoint in net,
                          'probability_law': None, 'confidence_level': None},
        'denominators': {'counts': counts, 'total': 100, 'computed': 60,
                         'conditional_accuracy': str(F(48, 60)),
                         'all_request_computed_correct': str(F(48, 100)),
                         'refusal_correctness': 'requires separate case labels'},
        'selection': {'marginal_coverage': str(marginal), 'accepted': accepted,
                      'acceptance_rate': str(F(len(accepted), 100)),
                      'coverage_given_acceptance': str(selective),
                      'claim': 'stipulated finite joint law; not observed critic behavior'},
        'repeated_looks': {'looks': tmax, 'per_look_alpha': '1/20',
                          'independent_any_alarm': str(one_or_more),
                          'independent_any_alarm_decimal': float(one_or_more),
                          'spending_sum': str(spending),
                          'four_equal_monitor_budget_each': '1/80',
                          'premise': 'valid per-look null probabilities; conditional validity for adaptive selection'},
        'dependency_invalidation': {'parents': {k: sorted(v) for k,v in parents.items()},
                                    'affected': changes,
                                    'state': 'historical bytes unchanged; current applicability separately reviewed'}
    }


if __name__ == '__main__':
    output = BASE / 'exact-results.json'
    with output.open('x') as stream:
        json.dump(calculate(), stream, indent=2); stream.write('\n')
    print('Five exact reference families reproduced; no upstream or model execution.')
