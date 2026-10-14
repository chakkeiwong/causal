#!/usr/bin/env python3
"""Reviewed pre-invocation import repair; preserve the registered runner bytes.

The original runner omitted its hashlib import and failed before any service
call. This launch amendment supplies only that standard-library binding. Its
source and review must be recorded prospectively before the fixed trial starts.
"""
import argparse
import hashlib
import json
from pathlib import Path

import funding_journey_20261013 as journey
import run_program as control


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--max-new-attempts', type=int, required=True)
    args = p.parse_args()
    assert args.max_new_attempts > 0
    root, base = journey.ROOT, journey.BASE
    note_path = base / 'launch-amendment.json'
    note = json.loads(note_path.read_text())
    state = control.core.read(root, control.core.STATE)
    saved = state['execution_program']['progress'].get('IN.JOURNEY.LOCAL.funding', [])
    assert any(x['path'] == str(note_path.relative_to(root)) and x['sha256'] == control.core.sha(note_path) for x in saved), 'Record the launch amendment before final calls'
    assert note['service_calls_before_amendment'] == 0 and note['fixtures_or_expectations_changed'] is False
    for evidence in note['evidence']:
        control.core.bound(root, evidence)
    # This is the sole change in the runner's execution namespace. No solver,
    # fixture, expectation, code byte, stopping rule or outcome is replaced.
    assert not hasattr(journey, 'hashlib')
    journey.hashlib = hashlib
    journey.run(args.max_new_attempts)


if __name__ == '__main__':
    main()
