#!/usr/bin/env python3
"""Exact project-owned workflow witnesses; never import or execute vendor code."""
from fractions import Fraction as F
import json


def q(value):
    return str(value.numerator) if value.denominator == 1 else f'{value.numerator}/{value.denominator}'


def calculate():
    # Stipulated service times, not measurements of SAS or any server.
    polls, pause, request = 3, F(1, 2), F(2)
    poll_sleep = polls * pause
    total = polls * (pause + request)
    assert poll_sleep == F(3, 2) and total == F(15, 2)

    # An offset over a changing collection is not a frozen sampling frame.
    initial = [1, 2, 3, 4]
    first = initial[:2]
    after_deletion = initial[1:]
    second = after_deletion[2:4]
    observed = first + second
    outcomes = {1: 1, 2: 0, 3: 1, 4: 0}
    initial_mean = F(sum(outcomes[k] for k in initial), len(initial))
    observed_mean = F(sum(outcomes[k] for k in observed), len(observed))
    assert observed == [1, 2, 4] and initial_mean == F(1, 2) and observed_mean == F(1, 3)

    # Supplied state records: no claim about a particular product's runtime.
    jobs = [
        dict(status='Finished', exit_code=0, artifact_bound=True),
        dict(status='Finished', exit_code=7, artifact_bound=True),
        dict(status='Failed', exit_code=None, artifact_bound=False),
        dict(status='Canceled', exit_code=None, artifact_bound=False),
    ]
    terminal = {'Canceled', 'Failed', 'Finished', 'Killed'}
    terminal_n = sum(j['status'] in terminal for j in jobs)
    accepted_n = sum(j['status'] == 'Finished' and j['exit_code'] == 0 and j['artifact_bound'] for j in jobs)
    cost = F(3) * len(jobs)
    assert terminal_n == 4 and accepted_n == 1

    # A bounded successful revisit does not establish permanent stability.
    history = [(F(0), 'Finished'), (F(1, 5), 'Finished'), (F(1), 'Running')]
    assert history[0][1] == history[1][1] and history[2][1] != history[0][1]
    return dict(
        provenance='Exact authored counterexamples under supplied laws; no native execution or measured prices',
        polling=dict(polls=polls, pause_seconds=q(pause), request_seconds=q(request),
                     sleep_only_seconds=q(poll_sleep), total_seconds=q(total), hard_deadline_proved=False),
        changing_frame=dict(initial=initial, after_deletion=after_deletion, observed=observed,
                            omitted_initial_ids=sorted(set(initial)-set(observed)),
                            initial_mean=q(initial_mean), observed_mean=q(observed_mean)),
        terminal_accounting=dict(supplied_jobs=jobs, terminal=terminal_n, accepted=accepted_n,
                                 total_cost_usd=q(cost), cost_per_terminal_usd=q(cost/terminal_n),
                                 cost_per_accepted_usd=q(cost/accepted_n), causal_validity_proved=False),
        finite_revisit=dict(history=[dict(seconds=q(t), status=s) for t,s in history],
                            first_two_agree=True, permanent_stability=False),
    )


if __name__ == '__main__':
    print(json.dumps(calculate(), indent=2))
