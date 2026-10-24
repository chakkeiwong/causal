#!/usr/bin/env python3
"""Exact authored workflow and cost examples; no external client executed."""
from fractions import Fraction
import json

def calculate():
    timeline=dict(trigger=0,run_created=3,observation_deadline=10,run_completed=12)
    assert timeline['run_created']<timeline['observation_deadline']<timeline['run_completed']
    sleeps=[min(Fraction(1,5)*Fraction(11,10)**k,Fraction(15)) for k in range(100)]
    assert max(sleeps)<=15 and sum(sleeps)>15 and sleeps[-1]==15
    requests=[dict(request='A',attempts=2,runs=['A1','A2']),dict(request='B',attempts=1,runs=[]),dict(request='C',attempts=1,runs=['C1'])]
    costs=dict(preparation=1200,all_attempts=1800,scientific_review=2400,maintenance=600)
    assert sum(costs.values())==6000
    return dict(scope='Authored stipulated examples; no native client/server execution or measured costs',timeline=timeline,
        at_deadline=dict(execution='completion_unknown',scientific='not_accepted'),later_state_requires_reconciliation=True,
        per_sleep_cap_seconds=15,saturated_sleeps=sum(x==15 for x in sleeps),sum_100_sleeps_exceeds_single_cap=True,
        repeated_capped_polling_has_no_total_deadline=True,
        requests=requests,logical_requests=len(requests),attempts=sum(x['attempts'] for x in requests),run_count=sum(len(x['runs']) for x in requests),
        duplicate_successes_do_not_create_new_logical_request=True,
        costs_usd=costs,total_usd=6000,attempted=120,completed=90,admissible=60,
        per_attempt_usd=str(Fraction(6000,120)),per_completion_usd=str(Fraction(6000,90)),per_admissible_usd=str(Fraction(6000,60)))
if __name__=='__main__':print(json.dumps(calculate(),indent=2))
