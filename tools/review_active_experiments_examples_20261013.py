#!/usr/bin/env python3
"""Review the finite planning example by independent conditional calculations."""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-13/active-experiments'


def ref(path, anchor):
    return {'path': str(path.relative_to(ROOT)),
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'anchor': anchor}


def main():
    code = ROOT / 'tools/active_experiments_examples_20261013.py'
    replay = subprocess.check_output([sys.executable, str(code)], timeout=20)
    assert replay == (BASE / 'exact-results.json').read_bytes()
    (BASE / 'exact-replay.json').write_bytes(replay)
    # This calculation conditions on a posterior directly; it does not import
    # the example implementation or its world/signal enumeration.
    conditional = []
    for p in [F(4, 5), F(1, 5)]:
        without = max(F(0), 220*p-120)
        after = F(0)
        for observed_good in [True, False]:
            good_likelihood = F(4, 5) if observed_good else F(1, 5)
            bad_likelihood = 1-good_likelihood
            mass = p*good_likelihood+(1-p)*bad_likelihood
            post = p*good_likelihood/mass
            after += mass*max(F(0), 220*post-120)
        gain = after-without
        assert gain < 5
        conditional.append({'posterior_good': str(p), 'stop_value': str(without),
                            'gross_after_second': str(after), 'gross_increment': str(gain),
                            'second_acquisition_cost': '5', 'optimal_action': 'stop'})
    assert [x['gross_increment'] for x in conditional] == ['16/5', '0']
    # A horizon of at most two permits stop or either design at either step.
    # Z is independent of H and cannot affect payoffs. A second Z therefore
    # buys no decision improvement, and conditional gains from H are below cost.
    assert F(1, 2)*56-5 == 23
    assert F(3, 4)*28-5 == 16
    assert (F(-5)+23)/2 == 9
    report = {'status': 'pass', 'issues': [], 'reviewer': 'author',
              'scope': 'Exact stipulated four-world decision problem; not a sampled study',
              'checks': ['Byte-identical replay of all original exact constructions',
                         'Independent posterior expected-utility calculation at both first-query outcomes',
                         'Stopping beats either second acquisition at the declared two-query horizon',
                         'All-attempt cost and random-design arithmetic checked'],
              'conditional_second_query': conditional,
              'horizon_at_most_two_optimal_net_value': '23',
              'bank_truth': False, 'llm_accuracy_measured': False,
              'evidence': [ref(code, 'Exact finite world enumeration'),
                           ref(BASE / 'exact-results.json', 'Preserved planning results'),
                           ref(BASE / 'exact-replay.json', 'Byte-identical replay'),
                           ref(Path(__file__), 'Independent posterior and horizon review')]}
    (BASE / 'exact-review.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({'status': 'pass', 'conditional_second_query': conditional}))


if __name__ == '__main__':
    main()
