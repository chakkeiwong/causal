#!/usr/bin/env python3
"""Exact authored witnesses; does not import or execute vendor sources."""
from fractions import Fraction as F


def calculate():
    capital, cost = F(1000), F(20)
    revision_values = [capital * b - cost for b in [F(3, 100), F(4, 100)]]
    gain, attempt_cost = F(12), F(7)
    attempts = [gain - n * attempt_cost for n in [1, 2]]
    # A supplied response is a logical witness, not an observed server response.
    statuses = [
        dict(executionStatus='Succeeded', isCompleted=True),
        dict(executionStatus='Failed', isCompleted=True),
        dict(executionStatus='HypotheticalOtherTerminal', isCompleted=True),
        dict(executionStatus='Running', isCompleted=False),
    ]
    truth = []
    for s in statuses:
        predicate = 'raise' if s['executionStatus'] == 'Failed' else ('accept' if s['isCompleted'] else 'wait')
        truth.append(dict(response=s, inspected_domino_predicate=predicate,
                          proposed_success_allowlist=s['executionStatus'] == 'Succeeded' and s['isCompleted']))
    assert revision_values == [10, 20] and attempts == [5, -2]
    return dict(kind='authored_exact_mathematics_and_predicate_witnesses', native_execution=False,
        revision=dict(capital_usd=str(capital), stipulated_coefficients=['3/100', '4/100'],
                      cost_usd=str(cost), net_usd=[str(x) for x in revision_values], difference_usd='10'),
        duplicate=dict(gain_once_usd=str(gain), cost_per_attempt_usd=str(attempt_cost),
                       attempts=[1,2], net_usd=[str(x) for x in attempts],
                       assumption='One stipulated useful gain; every attempted side effect incurs the same cost.'),
        terminal_predicate=truth,
        sas_zero_timeout=dict(while_guard='0 < 0 is false', body_executed=False,
                              explicit_post_loop_return=False, python_result='None'),
        limits=['Not empirical bank returns, statistical estimates, native tests or server-schema claims.',
                'A non-success terminal response is hypothetical; actual vendor state spaces require separate evidence.',
                'A task with a successful exit still needs bound outputs and scientific validation.'])


if __name__ == '__main__':
    import json
    print(json.dumps(calculate(), indent=2))
