"""Exact authored witnesses; does not import or execute any reviewed package."""
from fractions import Fraction
import re


def calculate():
    values = ['x', '7']
    requested = [v for v in values if re.search('[0-9]', v)]
    weakened = list(values)
    batches = [['a', 'b', 'c'], ['b'], ['b']]
    attempts = {k: sum(k in b for b in batches) for k in batches[0]}
    states = [
        dict(name='identified', terminal=True, valid=True, identified=True),
        dict(name='nonidentified', terminal=True, valid=True, identified=False),
        dict(name='structured_output_failed', terminal=True, valid=False, identified=True),
        dict(name='incomplete', terminal=False, valid=True, identified=True),
    ]
    for row in states:
        row['admit_effect'] = row['terminal'] and row['valid'] and row['identified']
    return dict(
        scope='Authored finite mathematical witnesses; not observed package or bank behavior',
        requested_strings=requested, weakened_strings=weakened,
        false_admissions=sorted(set(weakened)-set(requested)),
        selective_attempts=attempts, selective_total=sum(attempts.values()),
        whole_batch_total=3*3, saved_attempts=3*3-sum(attempts.values()),
        stipulated_cost_per_attempt_usd=str(Fraction(1, 4)),
        selective_cost_usd=str(sum(attempts.values())*Fraction(1, 4)),
        whole_batch_cost_usd=str(9*Fraction(1, 4)),
        states=states, admitted=sum(r['admit_effect'] for r in states),
        ordinary_turns=2, separate_compaction_calls=1, total_model_calls=3,
        native_execution=False)


if __name__ == '__main__':
    import json
    print(json.dumps(calculate(), indent=2))
