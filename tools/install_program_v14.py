#!/usr/bin/env python3
"""Prepare/publish V14 through the original lock and compare-before-write path."""
import argparse
import copy
import json

import master_control as core
import causal_program_v14 as control
from prepare_program_v14 import ref

ROOT = core.ROOT
BASE = ROOT / control.BASE

DOCUMENTS = {
    'plan': 'docs/program/master-program-v14.md',
    'plan_pdf': 'docs/program/master-program-v14.pdf',
    'audit': control.BASE + '/gap-audit.json',
    'audit_text': control.BASE + '/gap-audit.md',
    'graph': control.BASE + '/work-graph.json',
    'dependencies': control.BASE + '/dependency-review.json',
    'review': control.BASE + '/review.md',
    'continuation': control.BASE + '/continuation.md',
    'controller': 'tools/causal_program_v14.py',
    'entrypoint': 'tools/program.py',
    'preparer': 'tools/prepare_program_v14.py',
    'publisher': 'tools/install_program_v14.py',
    'tests': 'tests/test_program_v14.py',
    'pdf_builder': 'tools/build_program_pdf_v14.py',
    'pdf_report': control.BASE + '/program-pdf/build-report.json',
    'pdf_layout': control.BASE + '/program-pdf/text-layout-review.json',
}


def prepare():
    original = core.read(ROOT, control.BASE + '/predecessor-state.json')
    state = copy.deepcopy(original)
    state['revision'] = control.REVISION
    state['work_packages'] = core.read(ROOT, DOCUMENTS['dependencies'])['work_packages']
    state['execution_program'] = {
        'revision': control.REVISION,
        'predecessor': ref(control.BASE + '/predecessor-state.json', 'Complete unchanged V13.1 state'),
        'documents': {name: ref(path, 'Reviewed V14 ' + name) for name, path in DOCUMENTS.items()},
        'results': {}, 'registrations': {}, 'blocks': {}, 'progress': {}, 'turns': [], 'working_releases': [],
    }
    state['gap_execution']['plan'] = state['execution_program']['documents']['plan']
    state['deliveries'].append({'path': DOCUMENTS['plan_pdf'], 'sha256': core.sha(ROOT / DOCUMENTS['plan_pdf']),
                                'status': 'Comprehensive program and audit; text/bounds checked; rendered visual acceptance pending'})
    issues = control.validate_state(ROOT, state)
    if issues:
        raise ValueError('; '.join(issues))
    core.write(BASE / 'candidate-state.json', state)
    print(json.dumps({'prepared': True, 'operations': len(control.graph_for(ROOT, state)['nodes']),
                      'validation': 'pass', 'no_new_package_or_scientific_outcomes': True}))


def publish():
    before = core.sha(ROOT / core.STATE)
    state = core.read(ROOT, control.BASE + '/candidate-state.json')
    if before != state['execution_program']['predecessor']['sha256']:
        raise ValueError('Live state changed since preparation; reconcile before publishing')
    report = core.read(ROOT, control.BASE + '/verification.json')
    core.bound(ROOT, report['candidate_state'])
    if report.get('status') != 'pass' or report.get('tests_passed', 0) < 15 or report.get('unresolved_blocking_control_findings') != []:
        raise ValueError('Missing passing reviewed control verification')
    for evidence in report['evidence']:
        core.bound(ROOT, evidence)
    state['execution_program']['documents']['verification'] = ref(control.BASE + '/verification.json', 'Passing prepublication checks on exact candidate')
    control.install_hooks()
    core.commit_state(ROOT, before, state, {'action': 'install_comprehensive_scoped_program_v14',
        'replaced_broad_dependency_edges': 16, 'retained_original_gaps': 10,
        'no_phase_permission_stops': True, 'new_scientific_outcomes': [], 'external_inputs_received': [],
        'reader_unchanged': state['reader'], 'visual_acceptance': False})
    print(json.dumps(control.overview(state, control.graph_for(ROOT, state)), indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['prepare', 'publish'])
    args = parser.parse_args()
    prepare() if args.command == 'prepare' else publish()
