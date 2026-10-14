#!/usr/bin/env python3
"""Publish a verified execution refresh through the original locked writer."""
import json
from pathlib import Path

import master_control as core
import causal_program_v13_1 as control
import build_gap_successor_v13_1 as book

ROOT = core.ROOT
BASE = ROOT/control.BASE


def main():
    control.install_hooks()
    current = core.read(ROOT, core.STATE)
    if current.get('execution_refresh'):
        raise ValueError('Already published; preserve this execution refresh')
    before = core.sha(ROOT/core.STATE)
    state = core.read(ROOT, str((BASE/'proposed-state.json').relative_to(ROOT)))
    if before != state['execution_refresh']['predecessor']['sha256']:
        raise ValueError('Live state changed since preparation; reconcile it')
    verification = core.read(ROOT, str((BASE/'prepublication-verification.json').relative_to(ROOT)))
    if verification.get('status') != 'pass' or verification.get('tests_passed', 0) < 6:
        raise ValueError('Missing successful preservation and identity verification')
    core.bound(ROOT, verification['proposed_state'])
    if verification['proposed_state']['sha256'] != core.sha(BASE/'proposed-state.json'):
        raise ValueError('Verified candidate differs from proposed state')
    evidence = {'path': str((BASE/'prepublication-verification.json').relative_to(ROOT)),
                'sha256': core.sha(BASE/'prepublication-verification.json'), 'anchor': 'Passing candidate verification'}
    state['execution_refresh']['documents']['verification'] = evidence
    state['gap_execution']['documents']['execution_refresh_verification'] = evidence
    issues = control.validate_state(ROOT, state)
    if issues:
        raise ValueError(str(issues))
    book.check(state['successor_document'], state)
    core.commit_state(ROOT, before, state, {'action': 'publish_v13_1_known_work_execution',
        'reader': state['reader'], 'scoped_dossiers': 8, 'partial_software_cells': 30,
        'exact_project_example_families': 5, 'work_contract_changes': [], 'outcome_changes': [],
        'newly_qualified_gaps': [], 'visual_acceptance': False})
    print(json.dumps({'published': True, 'pages': state['reader']['pages'],
                      'recorded_outcomes': len(state['results']), 'work_packages': len(state['work_packages'])}))


if __name__ == '__main__':
    main()
