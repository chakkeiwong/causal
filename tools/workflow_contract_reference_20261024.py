#!/usr/bin/env python3
"""Exact authored workflow accounting; never imports or executes vendor code."""
from fractions import Fraction as F


def calculate():
    attempts = [
        dict(trigger='cancelled', run=False, terminal=False, accepted=False, cost=2),
        dict(trigger='started', run=True, terminal=True, accepted=True, cost=4),
        dict(trigger='started', run=True, terminal=True, accepted=False, cost=3),
        dict(trigger='started', run=True, terminal=True, accepted=False, cost=3),
    ]
    n, runs, accepted = len(attempts), sum(x['run'] for x in attempts), sum(x['accepted'] for x in attempts)
    cost = sum(x['cost'] for x in attempts)
    sleep = sum((F(1, 5) * F(11, 10) ** i for i in range(3)), F(0))
    return dict(
        origin='Project-authored stipulated events, durations and USD costs; no native measurements',
        attempts=attempts, requested=n, started=runs, accepted=accepted,
        acceptance_per_request=str(F(accepted, n)), acceptance_per_started=str(F(accepted, runs)),
        total_cost_usd=cost, cost_per_started=str(F(cost, runs)), cost_per_accepted=str(F(cost, accepted)),
        three_backoff_sleeps_seconds=str(sleep),
        three_two_second_requests_plus_sleep_seconds=str(sleep + 6),
        finished_exit_examples=[dict(state='Finished', exit_code=0, artifact_valid=True, acceptable=True),
                                dict(state='Finished', exit_code=7, artifact_valid=False, acceptable=False)],
        native_execution=False,
    )


if __name__ == '__main__':
    import json
    print(json.dumps(calculate(), indent=2))
