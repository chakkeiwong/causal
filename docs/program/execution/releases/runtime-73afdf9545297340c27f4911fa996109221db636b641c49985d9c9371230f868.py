#!/usr/bin/env python3
"""Stable proposal execution entrypoint; resumes work without inventing completion.

Immutable V14/V15 contracts and receipts remain readable by their original tools.
This entrypoint joins the proposal supplement to those contracts in memory and
persists actual outcomes, checkpoints and an active operation in canonical state.
It schedules agent work; it does not run an unattended language-model worker.
"""
import argparse
import copy
import json
from pathlib import Path
import subprocess
import sys

import causal_program_v14 as ledger
import master_control as core
import proposal_program as proposal

BASE = 'docs/program/execution'
CONTRACTS = BASE + '/contracts.json'
FIELDS = ('results', 'registrations', 'blocks', 'progress', 'turns')
require = ledger.require


def bind(root, name, anchor):
    return {'path': name, 'sha256': core.sha(core.safe(root, name)), 'anchor': anchor}


def combined(root, state):
    """Transient union. Never mutate the bound predecessor graph or its scope."""
    graph = copy.deepcopy(ledger.graph_for(root, state))
    supplement = core.read(root, state['execution_runtime']['contracts']['path'])
    graph['nodes'] += supplement['nodes']
    graph['lanes'] = ['public_evidence'] + graph['lanes'] + ['proposal_acceptance']
    merged = copy.deepcopy(state)
    for field in FIELDS[:-1]:
        merged['execution_program'][field].update(state['execution_runtime'][field])
    # Event order joins lanes without changing historical registration sequences.
    nodes = {n['id']: n for n in graph['nodes']}
    merged['execution_program']['turns'] = [
        {'operation': e['operation'], 'lane': nodes[e['operation']]['lane']}
        for e in state['events'] if e.get('operation') in nodes
        and e.get('action') not in ('execution_start', 'execution_checkpoint_resume')]
    stages = dict(proposal.scope_for(root, state)['operation_stages'])
    stages.update({n['id']: 'proposal_now' for n in supplement['nodes']})
    return graph, merged, stages


def queue(root, state):
    graph, merged, stages = combined(root, state)
    ready = [n for n in ledger.ordered_ready(merged, graph)
             if stages[n['id']] == 'proposal_now']
    # Registering an eligible final study is work, not a global dead end.
    registerable = [n for n in graph['nodes']
                   if stages[n['id']] == 'proposal_now' and n['study']
                   and n['id'] not in merged['execution_program']['results']
                   and n['id'] not in merged['execution_program']['registrations']
                   and not ledger.blockers(merged, n, include_protocol=False)]
    active = state['execution_runtime']['active']
    if active:
        ready.sort(key=lambda n: n['id'] != active['operation'])
    return graph, merged, stages, ready, registerable


def status(root, state):
    graph, merged, stages, ready, registerable = queue(root, state)
    ex = merged['execution_program']
    active = state['execution_runtime']['active']
    next_id = (active['operation'] if active else
               ready[0]['id'] if ready else registerable[0]['id'] if registerable else None)
    gaps = []
    for q in proposal.scope_for(root, state)['proposal_acceptance']:
        binding = ex['results'].get('PROPOSAL.' + q['id'])
        receipt = core.read(root, binding['path']) if binding else {}
        current_pass = (receipt.get('outcome') == 'pass' and
                        receipt.get('reviewed_reader', {}).get('sha256') == state['reader']['sha256'])
        gaps.append({'id': q['id'], 'status': 'pass' if current_pass else 'open'})
    return {'controller': 'python3 tools/run_program.py', 'scope_revision': state['proposal_program']['revision'],
            'program': BASE + '/current-program.md', 'operations': len(graph['nodes']),
            'proposal_operations': sum(v == 'proposal_now' for v in stages.values()),
            'recorded_proposal_operations': sum(k in ex['results'] for k, v in stages.items() if v == 'proposal_now'),
            'ready_proposal_operations': len(ready), 'registerable_proposal_studies': len(registerable),
            'active': active, 'next': next_id,
            'next_action': (active['next_action'] if active else
                            ledger.operation(graph, next_id)['action'] if next_id else None),
            'continue': next_id is not None,
            'global_blocker': None if next_id else 'No eligible proposal task; inspect task-specific prerequisites.',
            'public_designs': {f'P{i}.DESIGN': ex['results'].get(f'P{i}.DESIGN', {}).get('outcome',
                              'blocked' if f'P{i}.DESIGN' in ex['blocks'] else 'open') for i in range(1, 7)},
            'proposal_gaps': gaps, 'proposal_accepted': all(x['status'] == 'pass' for x in gaps),
            'product_acceptance_is_current_goal': False, 'reader': state['reader'],
            'background_worker_running': False,
            'automation_scope': 'Durable selection, evidence validation and resumption. An active agent performs scholarly work; a chat reply does not start a background worker.'}


def validate_runtime(root, state):
    """Validate the supplement as rigorously as the preserved operation receipts."""
    runtime = state['execution_runtime']
    require(runtime['schema_version'] == 1, 'Unknown execution schema')
    for field in ('contracts', 'installation'):
        core.bound(root, runtime[field])
    contract = core.read(root, runtime['contracts']['path'])
    for evidence in contract['evidence']:
        core.bound(root, evidence)
    graph, merged, stages = combined(root, state)
    ids = {n['id'] for n in graph['nodes']}
    supplemental = {n['id'] for n in contract['nodes']}
    require(len(ids) == len(graph['nodes']), 'Duplicate operation in unified queue')
    require(supplemental == {f'P{i}.DESIGN' for i in range(1, 7)} | {f'PROPOSAL.Q{i}' for i in range(1, 6)},
            'Missing public design or proposal acceptance contract')
    ledger.validate_graph(state, graph)
    for binding in merged['execution_program']['results'].values():
        receipt = core.read(root, binding['path'])
        require(receipt['outcome'] != 'pass' or receipt['execution'] == 'performed',
                'Passing work must actually have been performed')
    for node in graph['nodes']:
        if stages[node['id']] == 'proposal_now':
            require(not node['requires_inputs'], 'Authentic inputs cannot gate proposal work')
            require(all(stages[d['id']] == 'proposal_now' for d in node['depends']), 'Later stage gates proposal')
    for field in FIELDS[:-1]:
        require(set(runtime[field]) <= supplemental, 'Supplement contains a historical or unknown operation')
    for identifier, binding in runtime['results'].items():
        core.bound(root, binding)
        receipt = core.read(root, binding['path'])
        require(binding['outcome'] == receipt['outcome'] and binding['capabilities'] == receipt.get('capabilities', []),
                'Supplement receipt/state mismatch')
        ledger.validate_operation_receipt(root, merged, ledger.operation(graph, identifier), receipt, binding['sequence'])
        if identifier.startswith('PROPOSAL.') and receipt['outcome'] == 'pass':
            core.bound(root, receipt['reviewed_reader'])
            require(receipt.get('acceptance_scope') == 'proposal_only', 'Proposal review cannot award product acceptance')
    for identifier, checkpoints in runtime['progress'].items():
        for binding in checkpoints:
            core.bound(root, binding)
            validate_note(root, core.read(root, binding['path']), 'progress')
    for identifier, blocked in runtime['blocks'].items():
        require(identifier not in runtime['results'], 'Completed task still blocked')
        core.bound(root, blocked['receipt'])
        evidence = core.read(root, blocked['receipt']['path'])
        validate_note(root, evidence, 'block')
        require(all(blocked[k] == evidence[k] for k in ('reason', 'revisit_trigger', 'evidence')), 'Blocker differs from receipt')
    require(not runtime['registrations'], 'Supplement has no final study contracts')
    for turn in runtime['turns']:
        require(turn['operation'] in supplemental and turn['lane'] == ledger.operation(graph, turn['operation'])['lane'],
                'Invalid supplemental scheduling history')
    active = runtime['active']
    if active:
        node = ledger.operation(graph, active['operation'])
        require(stages[node['id']] == 'proposal_now' and node['id'] not in merged['execution_program']['results'],
                'Active task is completed or outside proposal scope')
        require(not ledger.blockers(merged, node, include_protocol=False), 'Active task has a local blocker')
        require(active.get('next_action') and active.get('started_at'), 'Active task has no resume action')


def validate_state(root, state):
    issues = proposal.validate_state(root, state)
    try:
        validate_runtime(root, state)
    except (ValueError, KeyError, OSError, TypeError) as exc:
        issues.append(str(exc))
    return issues


def validate_note(root, note, command):
    fields = {'block': ('reason', 'revisit_trigger', 'evidence'),
              'resume': ('resolution', 'evidence'),
              'progress': ('finding', 'next_action', 'evidence')}[command]
    require(all(note.get(k) for k in fields), command + ' requires ' + ', '.join(fields))
    for binding in note['evidence']:
        core.bound(root, binding)


def apply(root, state, command, identifier, receipt=None, reason=None):
    """Pure state transition apart from reading bound evidence; caller commits atomically."""
    graph, merged, stages = combined(root, state)
    node = ledger.operation(graph, identifier)
    require(stages[identifier] == 'proposal_now', 'Use explicit historical tools for optional/later claims')
    runtime = state['execution_runtime']
    active = runtime['active']
    supplemental = {n['id'] for n in core.read(root, runtime['contracts']['path'])['nodes']}
    ex = runtime if identifier in supplemental else state['execution_program']
    require(identifier not in ex['results'], 'Task already recorded; create a reviewed successor, do not rerun it')
    event = {'action': 'execution_' + command, 'operation': identifier}
    if command == 'start':
        require(not active or active['operation'] == identifier, 'Checkpoint/yield or finish the active task first')
        require(not ledger.blockers(merged, node, include_protocol=False), 'Task has unmet prerequisites')
        if not active:
            require(reason, 'State why this task is being started')
            checkpoints = ex['progress'].get(identifier, [])
            next_action = (core.read(root, checkpoints[-1]['path'])['next_action'] if checkpoints else node['action'])
            runtime['active'] = {'operation': identifier, 'started_at': core.now(),
                                 'next_action': next_action, 'selection_reason': reason}
        return event
    require(not active or active['operation'] == identifier, 'Another task is active; checkpoint/yield it first')
    require(receipt, 'Evidence receipt is required')
    evidence = core.read(root, receipt)
    binding = bind(root, receipt, 'Reviewed ' + command + ' evidence for ' + identifier)
    binding['sequence'] = len(ex['turns'])
    if command == 'record':
        require(evidence.get('outcome') != 'pass' or evidence.get('execution') == 'performed',
                'Passing work must actually have been performed')
        ledger.validate_operation_receipt(root, merged, node, evidence, binding['sequence'])
        if identifier.startswith('PROPOSAL.') and evidence['outcome'] == 'pass':
            require(evidence.get('acceptance_scope') == 'proposal_only', 'Proposal acceptance scope is required')
            core.bound(root, evidence.get('reviewed_reader', {}))
            require(evidence['reviewed_reader']['path'] == state['reader']['path'] and
                    evidence['reviewed_reader']['sha256'] == state['reader']['sha256'], 'Review is for a stale reader')
            if identifier == 'PROPOSAL.Q5':
                require(all(q['status'] == 'pass' for q in status(root, state)['proposal_gaps'][:4]),
                        'Q1–Q4 must review this exact reader')
        binding.update(outcome=evidence['outcome'], capabilities=evidence.get('capabilities', []))
        ex['results'][identifier] = binding
        ex['blocks'].pop(identifier, None)
        runtime['active'] = None
    elif command == 'register':
        require(identifier not in ex['registrations'], 'Registration is immutable')
        require(not ledger.blockers(merged, node, include_protocol=False), 'Registration prerequisites missing')
        binding['registered_at'] = core.now()
        ledger.validate_protocol(root, merged, node, binding)
        ex['registrations'][identifier] = binding
    elif command == 'block':
        validate_note(root, evidence, 'block')
        ex['blocks'][identifier] = {k: evidence[k] for k in ('reason', 'revisit_trigger', 'evidence')}
        ex['blocks'][identifier]['receipt'] = binding
        runtime['active'] = None
    elif command in ('progress', 'yield'):
        require(active and active['operation'] == identifier, 'Start the task before checkpointing')
        validate_note(root, evidence, 'progress')
        ex['progress'].setdefault(identifier, []).append(binding)
        runtime['active']['next_action'] = evidence['next_action']
        if command == 'yield':
            require(evidence.get('yield_reason'), 'Yield needs a reason; it is not a completion or permission stop')
            runtime['active'] = None
    elif command == 'resume':
        require(identifier in ex['blocks'], 'Task is not blocked')
        validate_note(root, evidence, 'resume')
        ex['blocks'].pop(identifier)
    else:
        raise ValueError('Unknown transition: ' + command)
    ex['turns'].append({'operation': identifier, 'lane': node['lane'], 'action': command})
    event['receipt'] = binding
    return event


def render(root, state):
    view = status(root, state)
    lines = ['# Mission control: causal banking proposal', '',
             '[Current program and execution rules](program/execution/current-program.md) · '
             '[Scope and public-data portfolio](program/master-program-proposal.md) · '
             '[Execution diagnosis and repair](program/execution/review.md)', '',
             f"Current entrypoint: `python3 tools/run_program.py status`, `next`, `check`. "
             'Use `start`, `progress`, `record`, `block`, `resume` and `register` for durable work. '
             'The earlier controllers and numbered plans are historical views.', '',
             f"**{view['recorded_proposal_operations']} / {view['proposal_operations']} proposal operations have recorded outcomes; "
             f"{view['ready_proposal_operations']} are ready.** Next: **{view['next']}**.", '',
             view['next_action'] or 'Inspect scoped dependencies.', '',
             'Public design outcomes: ' + ', '.join(k + ': ' + v for k, v in view['public_designs'].items()) + '.', '',
             'Q1–Q5 acceptance is derived from reviewed receipts, not from plan publication. '
             'All three mandatory manuscript repairs remain subject to their existing coverage and depth contracts. '
             'Bank qualification and adoption are later conditional work, not proposal blockers.', '',
             f"[Current integrated working monograph]({state['reader']['path'].removeprefix('docs/')}) "
             f"— {state['reader']['pages']} pages. [Public-data survey](program/public-data-v15/public-data-survey.pdf).", '',
             'Continue after every result or local blocker. Checkpoints preserve unfinished work and are not permission gates. '
             'Short commands and bounded text output reduce disconnection risk; a disconnect resumes from canonical state. '
             'No unattended research worker is running. An active agent must perform the selected work.', '',
             'Rendered visual acceptance remains pending a fresh image allowance under `/home/ubuntu/AGENTS.md`; '
             'it affects visual review only. Source audits, manuscript work and independent designs remain eligible.', '']
    md = '\n'.join(lines)
    (root / 'docs/mission-control.md').write_text(md)
    html = subprocess.run(['pandoc', '--from=gfm', '--to=html'], input=md, text=True,
                          capture_output=True, check=True, timeout=20).stdout
    (root / 'docs/mission-control.html').write_text("<!doctype html><meta charset='utf-8'><title>Causal proposal execution</title>" + html)


def commit(root, before, state, event):
    core.validate_state, core.render = validate_state, render
    core.commit_state(root, before, state, event)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for command in ('status', 'check', 'render'):
        sub.add_parser(command)
    for command in ('next', 'start'):
        p = sub.add_parser(command); p.add_argument('operation', nargs='?')
        if command == 'start':
            p.add_argument('--reason', default='Continue the eligible queue under the authorized proposal program')
    p = sub.add_parser('template'); p.add_argument('operation')
    for command in ('progress', 'yield', 'record', 'block', 'resume', 'register'):
        p = sub.add_parser(command); p.add_argument('operation'); p.add_argument('--receipt', required=True)
    args = parser.parse_args()
    state = core.read(core.ROOT, core.STATE)
    before = core.sha(core.ROOT / core.STATE)
    require(not (issues := validate_state(core.ROOT, state)), '; '.join(issues))
    if args.command == 'check':
        result = {'status': 'pass', 'issues': [], 'preserved_history': 'pass', 'unified_queue': 'pass'}
    elif args.command == 'status':
        result = status(core.ROOT, state)
    elif args.command == 'render':
        render(core.ROOT, state); result = {'rendered': True}
    else:
        key = args.operation or status(core.ROOT, state)['next']
        require(key is not None, 'No eligible task; inspect scoped dependencies')
        graph, merged, _ = combined(core.ROOT, state)
        node = ledger.operation(graph, key)
        if args.command == 'next':
            ex = merged['execution_program']
            checkpoint = ex['progress'].get(key, [])
            result = {'operation': node, 'blockers': ledger.blockers(merged, node),
                      'recorded': ex['results'].get(key), 'active': state['execution_runtime']['active'],
                      'latest_checkpoint': checkpoint[-1] if checkpoint else None,
                      'rule': 'Perform, review and record; continue another eligible task after every outcome or local blocker.'}
        elif args.command == 'template':
            result = ledger.receipt_template(node)
        else:
            event = apply(core.ROOT, state, args.command, key, getattr(args, 'receipt', None), getattr(args, 'reason', None))
            commit(core.ROOT, before, state, event)
            view = status(core.ROOT, state)
            result = {'action': args.command, 'operation': key, 'next': view['next'],
                      'next_action': view['next_action'], 'continue': view['continue'],
                      'recorded_proposal_operations': view['recorded_proposal_operations']}
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, OSError, subprocess.SubprocessError) as exc:
        raise SystemExit(str(exc))
