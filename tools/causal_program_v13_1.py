#!/usr/bin/env python3
"""Execution refresh view; all V13 scientific contracts and gates remain active."""
import contextlib
import io
import json
import subprocess
import sys

import master_control as core
import causal_program_v13 as v13
import build_gap_successor_v13_1 as book

BASE = 'docs/program/gap-execution-v13_1'
EXECUTION_REVISION = '13.1-known-work-continuation'


def validate_state(root, state):
    issues = v13.validate_state(root, state)
    if issues:
        return issues
    try:
        refresh = state['execution_refresh']
        core.bound(root, refresh['predecessor'])
        prior = core.read(root, refresh['predecessor']['path'])
        for name in ['work_packages', 'gaps', 'streams', 'external_inputs', 'attempts', 'major_repairs',
                     'repair_program', 'baseline_manifest_sha256', 'working_document']:
            if state[name] != prior[name]:
                raise ValueError('Execution refresh changed preserved contract: '+name)
        for name in ['results', 'registrations', 'input_receipts']:
            for key, value in prior[name].items():
                if state[name].get(key) != value:
                    raise ValueError('Execution refresh changed historical '+name+': '+key)
        for key, value in prior['gap_execution']['documents'].items():
            if state['gap_execution']['documents'].get(key) != value:
                raise ValueError('Execution refresh changed preserved V13 document: '+key)
        for delivery in prior['deliveries']:
            if delivery not in state['deliveries']:
                raise ValueError('Execution refresh removed a delivered artifact')
            core.bound(root, dict(delivery, anchor='Preserved delivery'))
        for value in refresh['documents'].values():
            core.bound(root, value)
        if state['gap_execution']['plan'] != refresh['documents']['plan']:
            raise ValueError('Canonical program pointer differs from execution plan')
        queue = core.read(root, refresh['documents']['queue']['path'])
        if {r['id'] for r in queue['gaps']} != {g['id'] for g in state['gaps']}:
            raise ValueError('Execution queue omits a required gap')
        ids = {t['id'] for t in state['work_packages']}
        for unit in queue['units']:
            if not set(unit['parents']) <= ids or not unit['next_action'] or not unit['completion_evidence']:
                raise ValueError('Execution unit lacks a valid parent, action or completion evidence')
        if state['successor_document'] != refresh['documents']['book_report']:
            raise ValueError('Current book report differs from refresh report')
        report = core.read(root, state['successor_document']['path'])
        if any(state['reader'][key] != report['pdf'][key] for key in ['path', 'sha256']) or state['reader']['pages'] != report['pages']:
            raise ValueError('Current reader differs from refreshed book identity')
        return []
    except (KeyError, ValueError, OSError, TypeError) as exc:
        return [str(exc)]


def summary(state):
    out = v13.summary(state)
    out['contract_revision'] = state['revision']
    out['execution_revision'] = state['execution_refresh']['revision']
    out['controller'] = 'python3 tools/causal_program_v13_1.py'
    out['program_view'] = state['execution_refresh']['documents']['plan']['path']
    out['execution_queue'] = state['execution_refresh']['documents']['queue']['path']
    return out


def render(root, state):
    # Reuse the complete task/dependency view, then replace its hard-coded V13
    # navigation with the canonical execution-refresh links.
    v13.render(root, state)
    path = root/'docs/mission-control.md'
    raw = path.read_text().replace('master program V13', 'master program V13.1', 1)
    raw = raw.replace('program/master-program-v13.md', 'program/master-program-v13_1.md')
    raw = raw.replace('program/master-program-v13.pdf', 'program/master-program-v13_1.pdf')
    raw = raw.replace('program/gap-repair-v13/review.md', 'program/gap-execution-v13_1/review.md')
    raw = raw.replace('program/gap-repair-v13/continuation.md', 'program/gap-execution-v13_1/continuation.md')
    raw = raw.replace('| Package | Outcome/readiness | Remaining prerequisite |',
        'The V13 contracts remain intact. The execution refresh distinguishes known local work, missing authentic inputs and unresolved scientific arguments. '
        'Eight deeper package dossiers and five project examples are integrated; 30/102 software cells are partially inspected, zero complete. '
        '[Execution queue](program/gap-execution-v13_1/execution-queue.json).\n\n'
        '| Package | Outcome/readiness | Remaining prerequisite |', 1)
    path.write_text(raw)
    html = subprocess.run(['pandoc', '--from=gfm', '--to=html'], input=raw, text=True,
                          capture_output=True, check=True, timeout=20).stdout
    (root/'docs/mission-control.html').write_text("<!doctype html><meta charset='utf-8'><title>Causal program V13.1</title>"+html)


def install_hooks():
    v13.install_hooks()
    core.validate_state = validate_state
    core.summary = summary
    core.render = render


def main():
    install_hooks()
    if len(sys.argv) > 1 and sys.argv[1] == 'check':
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            try:
                core.cli()
            except SystemExit as exc:
                if exc.code not in (None, 0):
                    print(stream.getvalue(), file=sys.stderr)
                    raise
        result = json.loads(stream.getvalue())
        state = core.read(core.ROOT, core.STATE)
        prior = core.read(core.ROOT, state['execution_refresh']['predecessor']['path'])
        result['preserved_v13_document'] = book.prior.check(prior['successor_document'])
        result['current_working_document'] = book.check(state['successor_document'], state)
        result['scope'] += ' V13.1 preserves V13 contracts/results and verifies the execution queue and both book identities.'
        print(json.dumps(result, indent=2))
    else:
        core.cli()


if __name__ == '__main__':
    main()
