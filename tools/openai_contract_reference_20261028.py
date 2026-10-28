"""Exact authored interface and budget witnesses; no external library execution."""
from fractions import Fraction


def calculate():
    cases = [
        dict(id='complete_identified', complete=True, schema=True, identified=True),
        dict(id='complete_unidentified', complete=True, schema=True, identified=False),
        dict(id='incomplete_valid_prefix', complete=False, schema=True, identified=True),
        dict(id='refused', complete=False, schema=False, identified=False),
    ]
    for case in cases:
        case['admit_effect'] = all(case[k] for k in ['complete', 'schema', 'identified'])
    workflow_attempts, sdk_attempts = 2, 3
    attempts = workflow_attempts * sdk_attempts
    cost = attempts * Fraction(1, 4)
    network_time = attempts * 4
    inner_wait = workflow_attempts * (1 + 2)
    outer_wait = 3
    return dict(cases=cases, admitted=sum(c['admit_effect'] for c in cases),
                workflow_attempts=workflow_attempts, sdk_attempts=sdk_attempts,
                maximum_http_attempts=attempts, stipulated_total_cost_usd=str(cost),
                stipulated_elapsed_seconds=network_time + inner_wait + outer_wait,
                observed_provider_or_bank_performance=False)


if __name__ == '__main__':
    import json
    print(json.dumps(calculate(), indent=2))
