#!/usr/bin/env python3
"""Scoped execution control with unchanged scientific and external acceptance gates."""
import argparse
from collections import Counter
from datetime import datetime
import contextlib
import copy
import io
import json
import re
import subprocess
import sys

import master_control as core
import causal_program_v13 as v13
import causal_program_v13_1 as predecessor
import repair_control_v12 as v12

REVISION = '14.0-scoped-dependency-program'
BASE = 'docs/program/comprehensive-v14'
OUTCOMES = {'pass', 'negative', 'inconclusive'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def graph_for(root, state):
    return core.read(root, state['execution_program']['documents']['graph']['path'])


def operation(graph, identifier):
    matches = [n for n in graph['nodes'] if n['id'] == identifier]
    require(len(matches) == 1, 'Unknown or duplicate operation: ' + identifier)
    return matches[0]


def dependency_blockers(execution, requirements):
    reasons = []
    for dep in requirements:
        result = execution['results'].get(dep['id'])
        if not result or result['outcome'] not in dep['outcomes']:
            reasons.append('requires ' + dep['id'] + ' disposition ' + '/'.join(dep['outcomes']))
        elif dep.get('capability') and dep['capability'] not in result.get('capabilities', []):
            reasons.append('requires ' + dep['id'] + ' capability ' + dep['capability'])
    return reasons


def blockers(state, node, include_protocol=True):
    execution = state['execution_program']
    reasons = dependency_blockers(execution, node['depends'])
    reasons += ['missing authentic input ' + x for x in node['requires_inputs'] if x not in state['input_receipts']]
    if node['id'] in execution['blocks']:
        reasons.append('recorded blocker: ' + execution['blocks'][node['id']]['reason'])
    if include_protocol and node['study'] and node['id'] not in execution['registrations']:
        reasons.append('requires prospective operation registration')
    return reasons


def ordered_ready(state, graph):
    execution = state['execution_program']
    turns = execution['turns']
    last = {lane: -1 for lane in graph['lanes']}
    counts = Counter()
    for index, turn in enumerate(turns):
        last[turn['lane']] = index
        counts[turn['operation']] += 1
    candidates = [n for n in graph['nodes'] if n['id'] not in execution['results'] and not blockers(state, n)]
    return sorted(candidates, key=lambda n: (last[n['lane']], graph['lanes'].index(n['lane']),
                                            counts[n['id']], n['priority'], n['id']))


def validate_graph(state, graph):
    nodes = graph['nodes']
    ids = {x['id'] for x in nodes}
    require(len(ids) == len(nodes), 'Duplicate operation')
    require(graph.get('phase_policy') and graph.get('qualifies_original_gaps_automatically') is False,
            'Missing continuation or scientific-qualification boundary')
    parents = {x['id'] for x in state['work_packages']}
    inputs = {x['id'] for x in state['external_inputs']}
    visited, visiting = set(), set()
    for node in nodes:
        require(node['lane'] in graph['lanes'], 'Unknown lane')
        require(set(node['parents']) <= parents and node['parents'], 'Unknown/empty parent scope')
        require(set(node['requires_inputs']) <= inputs, 'Unknown external input')
        require(all(node.get(k) for k in ('title', 'action', 'outputs', 'criteria', 'owner_role', 'failure_action')), 'Incomplete operation contract')
        require(not ({'phase', 'requires_phase', 'phase_gate'} & set(node)), 'Phases must not gate execution')
        for path in node['outputs']:
            core.safe(core.ROOT, path)
        for d in node['depends']:
            require(d['id'] in ids and d['outcomes'] and set(d['outcomes']) <= OUTCOMES, 'Invalid operation prerequisite')
            if d.get('capability'):
                require(d['capability'] in operation(graph, d['id'])['capabilities'], 'Undeclared prerequisite capability')

    def visit(identifier):
        require(identifier not in visiting, 'Operation dependency cycle: ' + identifier)
        if identifier in visited:
            return
        visiting.add(identifier)
        for dep in operation(graph, identifier)['depends']:
            visit(dep['id'])
        visiting.remove(identifier); visited.add(identifier)

    for identifier in ids:
        visit(identifier)
    for parent, deps in graph['package_gates'].items():
        require(parent in parents and deps, 'Invalid package rollup')
        for d in deps:
            require(d['id'] in ids and set(d['outcomes']) <= OUTCOMES, 'Invalid rollup prerequisite')
    # Coverage remains a machine-checkable obligation, independent of prose summaries.
    for prefix, count in [('SW.CELL.', 102), ('LL.TASK.', 14), ('IN.REQ.', 12), ('TEXT.DRAFT.', 22), ('TEXT.REVIEW.', 22), ('EXT.PREP.', 12), ('EXT.VALIDATE.', 12)]:
        require(sum(x.startswith(prefix) for x in ids) == count, 'Dropped required coverage: ' + prefix)
    contract = core.read(core.ROOT, 'docs/program/repair-v12/coverage-contract.json')
    cells = {'SW.CELL.' + c['id'].replace('::', '.').replace('++', 'xx') for c in contract['software_cells']}
    require({x for x in ids if x.startswith('SW.CELL.')} == cells, 'Replaced a required software cell')
    require({x.removeprefix('LL.TASK.') for x in ids if x.startswith('LL.TASK.')} == {x['id'] for x in contract['llm_tasks']}, 'Changed the LLM task coverage')
    require({x.removeprefix('IN.REQ.') for x in ids if x.startswith('IN.REQ.')} == set(contract['integration_requirements']), 'Changed integration coverage')
    chapter_ids = {x['id'] for x in core.read(core.ROOT, 'docs/program/repair-v12/chapter-plan.json')['chapters']}
    require({x.removeprefix('TEXT.REVIEW.') for x in ids if x.startswith('TEXT.REVIEW.')} == chapter_ids, 'Changed chapter allocations')


def validate_protocol(root, state, node, binding):
    core.bound(root, binding)
    spec = core.read(root, binding['path'])
    require(node['study'], 'Only study operations have prospective protocols')
    require(spec.get('operation_id') == node['id'] and spec.get('operation_contract_sha256') == core.digest_object(node), 'Protocol belongs to another operation')
    for key in core.PROTOCOL_FIELDS:
        require(spec.get(key) not in (None, '', []), 'Protocol missing ' + key)
    require(isinstance(spec['replications'], int) and not isinstance(spec['replications'], bool) and spec['replications'] > 0, 'Invalid replications')
    require(isinstance(spec['seed'], int) and not isinstance(spec['seed'], bool), 'Protocol needs a frozen integer seed')
    require(spec['stopping_rule'] == 'fixed_design_no_outcome_stopping', 'Final study requires fixed prospective stopping')
    core.bound(root, spec['derivation_review'])
    core.inputs_bound(root, spec)
    require(spec.get('screen_operating_characteristics') and spec.get('width_and_availability_rules') and spec.get('fresh_data_provenance'), 'Protocol lacks power, usefulness or fresh data')
    require(spec.get('execution_inputs'), 'Protocol needs exact method/code/input identities')
    for evidence in spec['execution_inputs']:
        core.bound(root, evidence)
    review_ref = spec.get('successor_review', {})
    core.bound(root, review_ref)
    review = core.read(root, review_ref['path'])
    require(review.get('operation_id') == node['id'], 'Argument review belongs to another operation')
    require(review.get('design_approved') is True and review.get('unresolved_design_blockers') == [] and
            review.get('scope_matches_contract') is True and review.get('retained_predecessor_failures') is True,
            'Study requires a reviewed argument/scope and no unresolved design blockers')
    require(binding.get('sequence') is not None, 'Registration must be recorded prospectively in the control ledger')
    require(binding.get('registered_at'), 'Protocol needs its actual registration time')


def validate_operation_receipt(root, state, node, receipt, sequence):
    require(receipt.get('operation_id') == node['id'] and receipt.get('operation_contract_sha256') == core.digest_object(node), 'Receipt belongs to another operation contract')
    outcome = receipt.get('outcome')
    require(outcome in OUTCOMES, 'Invalid operation outcome')
    reviewer = receipt.get('reviewer', {})
    require(receipt.get('scope') and isinstance(reviewer, dict) and reviewer.get('name') and reviewer.get('kind') in ('author', 'independent', 'external_owner') and isinstance(receipt.get('limitations'), list), 'Receipt lacks scope, named review or limits')
    require(receipt.get('original_gap_qualification') is False, 'An operation cannot award an original gap or final package')
    require(receipt.get('execution') in ('performed', 'not_performed'), 'Execution must distinguish a run from a disposition')
    caps = receipt.get('capabilities', [])
    require(set(caps) <= set(node['capabilities']), 'Undeclared capability')
    require(not caps or (outcome == 'pass' and receipt['execution'] == 'performed'), 'Only an executed passing review may enable a capability')
    # A negative/unavailable disposition is recordable without pretending a blocked trial ran.
    disposition_only = receipt['execution'] == 'not_performed' and outcome in ('negative', 'inconclusive')
    if disposition_only:
        require(receipt.get('nonexecution_reason') and receipt.get('revisit_trigger'), 'Nonexecution needs a reason and exact revisit trigger')
    else:
        require(not blockers(state, node), 'Operation is not ready: ' + '; '.join(blockers(state, node)))
    criteria = receipt.get('criteria', [])
    require(len(criteria) == len(node['criteria']) and {x.get('index') for x in criteria} == set(range(len(node['criteria']))), 'Missing or duplicate criterion review')
    for criterion in criteria:
        require(criterion.get('verdict') in ('pass', 'negative', 'inconclusive') and criterion.get('finding') and criterion.get('evidence'), 'Criterion needs a verdict, finding and bound evidence')
        if outcome == 'pass':
            require(criterion['verdict'] == 'pass', 'Passing operation has an unresolved criterion')
        for evidence in criterion['evidence']:
            core.bound(root, evidence)
    if outcome == 'pass':
        outputs = receipt.get('outputs', [])
        require({r['path'] for r in outputs} == set(node['outputs']), 'Passing receipt must bind the declared deliverable')
        for output in outputs:
            core.bound(root, output)
    if node['study'] and not disposition_only:
        binding = state['execution_program']['registrations'].get(node['id'])
        require(binding is not None, 'Missing prospective registration')
        validate_protocol(root, state, node, binding)
        require(binding['sequence'] < sequence, 'Study receipt must follow its registration')
        require(receipt.get('protocol_sha256') == binding['sha256'], 'Study receipt differs from its registration')
        count = receipt.get('all_request_denominator')
        require(isinstance(count, int) and not isinstance(count, bool) and count > 0 and receipt.get('fresh_data_identity'), 'Study needs all-request counts and fresh data identity')
        require(receipt.get('retained_failures') is True, 'Study must retain failed and unavailable requests')
        require(datetime.fromisoformat(receipt['started_at']) > datetime.fromisoformat(binding['registered_at']), 'Study began before registration')
        core.bound(root, receipt['journal'])


def validate_receipt(root, state, task, receipt):
    # Preserve the original receipt, repair, study and exact-release external rules.
    v13.validate_receipt(root, state, task, receipt)
    if state.get('revision') == REVISION:
        graph = graph_for(root, state)
        unmet = dependency_blockers(state['execution_program'], graph['package_gates'].get(task['id'], []))
        require(not unmet, 'Package lacks its scoped operation evidence: ' + '; '.join(unmet))


def validate_working_release(root, binding):
    """Admit a versioned working book without rewriting its predecessor or I02."""
    core.bound(root, binding)
    manifest = core.read(root, binding['path'])
    require(manifest.get('kind') == 'working_monograph' and manifest.get('final_acceptance') is False,
            'Working delivery cannot award author release or scientific acceptance')
    for key in ('pdf', 'build_report', 'source_review', 'text_layout'):
        core.bound(root, manifest[key])
    require(manifest.get('source_artifacts'), 'Working book needs its preserved source artifacts')
    for source in manifest['source_artifacts']:
        core.bound(root, source)
    build = core.read(root, manifest['build_report']['path'])
    for key in ('path', 'sha256'):
        require(build['pdf'][key] == manifest['pdf'][key], 'Build report differs from delivered PDF')
    require(build['pages'] == manifest['pages'], 'Working book page count differs from build report')
    source_review = core.read(root, manifest['source_review']['path'])
    require(source_review.get('status') == 'pass' and source_review.get('issues') == [], 'Working book source/claim review has unresolved issues')
    require(source_review.get('evidence'), 'Source/claim review must bind its audited evidence')
    for evidence in source_review['evidence']:
        core.bound(root, evidence)
    bounds = core.read(root, manifest['text_layout']['path'])
    require(bounds.get('status') == 'pass' and bounds.get('pages') == manifest['pages'], 'Working PDF text/layout check failed')
    with core.safe(root, manifest['pdf']['path']).open('rb') as stream:
        require(stream.read(5) == b'%PDF-', 'Working delivery is not an actual PDF')
    info = subprocess.check_output(['pdfinfo', str(core.safe(root, manifest['pdf']['path']))], text=True, timeout=15)
    require(int(re.search(r'(?m)^Pages:\s+(\d+)', info).group(1)) == manifest['pages'], 'PDF bytes disagree with declared page count')
    return manifest


def validate_state(root, state):
    try:
        require(state.get('revision') == REVISION, 'Not the V14 execution program')
        execution = state['execution_program']
        core.bound(root, execution['predecessor'])
        prior = core.read(root, execution['predecessor']['path'])
        issues = predecessor.validate_state(root, prior)
        require(not issues, 'Preserved predecessor: ' + '; '.join(issues))
        for binding in execution['documents'].values():
            core.bound(root, binding)
        contracts = core.read(root, execution['documents']['dependencies']['path'])
        require(state['work_packages'] == contracts['work_packages'], 'Unreviewed package contract change')
        old = {x['id']: x for x in prior['work_packages']}
        for task in state['work_packages']:
            original = old[task['id']]
            if task != original:
                require(task['id'] not in prior['results'] and task['id'] not in prior['registrations'], 'Cannot change a resolved or registered contract')
                require({k: v for k, v in task.items() if k != 'depends'} == {k: v for k, v in original.items() if k != 'depends'}, 'Only reviewed dependency changes are allowed')
        for key in ('gaps', 'streams', 'external_inputs', 'attempts', 'major_repairs', 'repair_program',
                    'baseline_manifest_sha256', 'working_document', 'successor_document', 'execution_refresh', 'latex_roots'):
            require(state[key] == prior[key], 'Changed preserved contract/evidence: ' + key)
        for key in ('results', 'registrations', 'input_receipts'):
            for identifier, binding in prior[key].items():
                require(state[key].get(identifier) == binding, 'Changed historical ' + key + ': ' + identifier)
        for delivery in prior['deliveries']:
            require(delivery in state['deliveries'], 'Removed historical delivery')
            core.bound(root, dict(delivery, anchor='Preserved delivery'))
        reader = copy.deepcopy(prior['reader'])
        seen_pdfs = {x['path'] for x in prior['deliveries']}
        for binding in execution.get('working_releases', []):
            release = validate_working_release(root, binding)
            require(release['supersedes'] == {k: reader[k] for k in ('path', 'sha256')}, 'Working book does not preserve the predecessor chain')
            require(release['pdf']['path'] not in seen_pdfs, 'Working delivery cannot overwrite a historical PDF')
            seen_pdfs.add(release['pdf']['path'])
            require(any(d['path'] == release['pdf']['path'] and d['sha256'] == release['pdf']['sha256'] for d in state['deliveries']), 'Current working book is missing from deliveries')
            reader = {k: release['pdf'][k] for k in ('path', 'sha256')}
            reader.update(pages=release['pages'], status='Working monograph; not I02 acceptance')
        require(state['reader'] == reader, 'Current reader differs from its preserved working-delivery chain')
        expected_gap = copy.deepcopy(prior['gap_execution'])
        expected_gap['plan'] = execution['documents']['plan']
        require(state['gap_execution'] == expected_gap, 'Changed preserved gap execution records or canonical plan')
        graph = graph_for(root, state)
        validate_graph(state, graph)
        identifiers = {n['id'] for n in graph['nodes']}
        for kind in ('results', 'registrations', 'blocks', 'progress'):
            require(set(execution[kind]) <= identifiers, 'Unknown operation in ' + kind)
        for identifier, binding in execution['registrations'].items():
            validate_protocol(root, state, operation(graph, identifier), binding)
        for identifier, binding in execution['results'].items():
            core.bound(root, binding)
            receipt = core.read(root, binding['path'])
            require(binding['outcome'] == receipt['outcome'] and binding.get('capabilities', []) == receipt.get('capabilities', []), 'Operation receipt/state mismatch')
            validate_operation_receipt(root, state, operation(graph, identifier), receipt, binding['sequence'])
        for identifier, blocked in execution['blocks'].items():
            require(identifier not in execution['results'] and blocked.get('reason') and blocked.get('revisit_trigger'), 'Invalid blocker record')
            for evidence in blocked['evidence']:
                core.bound(root, evidence)
            core.bound(root, blocked['receipt'])
        for turn in execution['turns']:
            require(turn['operation'] in identifiers and turn['lane'] == operation(graph, turn['operation'])['lane'], 'Invalid fair-scheduling history')
        for identifier, checkpoints in execution['progress'].items():
            for binding in checkpoints:
                core.bound(root, binding)
                progress = core.read(root, binding['path'])
                require(progress.get('finding') and progress.get('next_action') and progress.get('evidence'), 'Progress needs observed evidence and a concrete continuation')
                for evidence in progress['evidence']:
                    core.bound(root, evidence)
        # The legacy structural checker invokes the active receipt and protocol hooks.
        # Set them explicitly even for imported validation, then restore the caller.
        saved = core.validate_receipt, core.validate_protocol
        try:
            core.validate_receipt, core.validate_protocol = validate_receipt, v13.validate_protocol
            issues = v12.LEGACY_VALIDATE_STATE(root, state)
        finally:
            core.validate_receipt, core.validate_protocol = saved
        require(not issues, '; '.join(issues))
        return []
    except (KeyError, ValueError, OSError, TypeError, AssertionError) as exc:
        return [str(exc)]


def overview(state, graph):
    execution = state['execution_program']
    ready = ordered_ready(state, graph)
    by_lane = []
    for lane in graph['lanes']:
        rows = [n for n in graph['nodes'] if n['lane'] == lane]
        eligible = [n for n in ready if n['lane'] == lane]
        by_lane.append({'lane': lane, 'total': len(rows), 'recorded': sum(n['id'] in execution['results'] for n in rows),
                        'ready': len(eligible), 'next': eligible[0]['id'] if eligible else None})
    old = v13.summary(state)
    return {'revision': REVISION, 'controller': 'python3 tools/program.py', 'program': execution['documents']['plan']['path'],
            'audit': execution['documents']['audit']['path'], 'operations': len(graph['nodes']),
            'operation_outcomes': len(execution['results']), 'ready_operations': len(ready),
            'blocked_operations': len(graph['nodes']) - len(ready) - len(execution['results']),
            'package_outcomes': len(state['results']), 'packages': len(state['work_packages']),
            'qualified_original_gaps': old['qualified_gaps_in_declared_scope'],
            'missing_external_inputs': old['missing_external_inputs'], 'reader': state['reader'],
            'next': ready[0]['id'] if ready else None, 'lanes': by_lane,
            'continue': bool(ready), 'stop_reason': None if ready else 'No eligible operation; inspect scoped blockers and authentic-input requirements.',
            'automation_scope': 'Selects and records reviewed work. It does not autonomously write chapters, prove science, run model calls or award acceptance.'}


def render(root, state):
    graph = graph_for(root, state)
    view = overview(state, graph)
    lines = ['# Mission control: causal banking master program V14', '',
             'The monograph and product remain unfinished. All three mandatory repairs remain open.', '',
             f"{view['package_outcomes']}/48 packages have recorded outcomes; {len(view['qualified_original_gaps'])}/10 original gaps fully qualified. "
             f"{view['ready_operations']} of {view['operations']} scoped operations are ready; next: **{view['next']}**.", '',
             '[Reviewed program and PDF](program/master-program-v14.md) · [Program PDF](program/master-program-v14.pdf) · '
             '[Comprehensive audit](program/comprehensive-v14/gap-audit.md) · [Dependency review](program/comprehensive-v14/dependency-review.json) · '
             '[Plan review](program/comprehensive-v14/review.md) · [State](program/state.json)', '',
             'Current commands: `python3 tools/program.py status`, `next`, `check`. The receipt-bound historical `tools/causal_program.py` remains preserved; it reports package-level history and does not schedule V14 operations.', '',
             f"[Current working monograph]({state['reader']['path'].removeprefix('docs/')}) — {state['reader']['pages']} pages, not I02 acceptance.", '',
             'Work proceeds by specific prerequisites. After every result or blocker, record evidence, recompute readiness and continue into another ready lane. There are no phase-stop or checkpoint-permission gates. Final scientific, source, page, external and release acceptance gates remain in force.', '',
             '| Lane | Ready / total | Recorded outcomes | Next operation |', '|---|---|---|---|']
    lines += [f"| {x['lane']} | {x['ready']} / {x['total']} | {x['recorded']} | {x['next'] or 'Awaiting true prerequisites'} |" for x in view['lanes']]
    lines += ['', 'Thirty of 102 software cells are partially inspected; none is closed. All 14 LLM tasks need further development, all 12 integration obligations remain broader than the existing local prototype, and all 22 chapter allocations remain partial. Twelve authentic input categories remain empty. The audit records evidence, omissions and the exact remaining work.', '',
              'Scoped source/implementation outcomes do not automatically complete their parent packages. Use `package next ID` for retained package acceptance obligations and `next OPERATION` for executable work. The current graph replaces 16 broad package edges with matching scoped evidence.', '',
              'Rendered visual acceptance remains pending under the inherited image allowance in /home/ubuntu/AGENTS.md; it blocks visual acceptance only.', '']
    text = '\n'.join(lines)
    (root / 'docs/mission-control.md').write_text(text)
    html = subprocess.run(['pandoc', '--from=gfm', '--to=html'], input=text, capture_output=True, text=True, check=True, timeout=20).stdout
    (root / 'docs/mission-control.html').write_text("<!doctype html><meta charset='utf-8'><title>Causal program V14</title>" + html)


def install_hooks():
    core.validate_state = validate_state
    core.validate_receipt = validate_receipt
    core.validate_protocol = v13.validate_protocol
    core.render = render


def commit(root, before, state, node, action, details):
    state['execution_program']['turns'].append({'operation': node['id'], 'lane': node['lane'], 'action': action})
    core.commit_state(root, before, state, {'action': 'v14_' + action, 'operation': node['id'], **details})


def receipt_template(node):
    return {'operation_id': node['id'], 'operation_contract_sha256': core.digest_object(node),
            'outcome': 'inconclusive', 'execution': 'not_performed', 'scope': '', 'reviewer': {'name': '', 'kind': 'author'}, 'limitations': [],
            'original_gap_qualification': False, 'capabilities': [], 'outputs': [],
            'nonexecution_reason': '', 'revisit_trigger': '',
            'criteria': [{'index': i, 'verdict': 'inconclusive', 'finding': '', 'evidence': []} for i in range(len(node['criteria']))]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ('status', 'check', 'render'):
        sub.add_parser(name)
    p = sub.add_parser('next'); p.add_argument('operation', nargs='?')
    p = sub.add_parser('template'); p.add_argument('operation')
    for name in ('record', 'register', 'block', 'resume', 'progress'):
        p = sub.add_parser(name); p.add_argument('operation'); p.add_argument('--receipt', required=True)
    p = sub.add_parser('package'); p.add_argument('arguments', nargs=argparse.REMAINDER)
    p = sub.add_parser('intake'); p.add_argument('input'); p.add_argument('--receipt', required=True)
    p = sub.add_parser('deliver'); p.add_argument('--manifest', required=True)
    args = parser.parse_args()
    install_hooks()
    state = core.read(core.ROOT, core.STATE)
    before = core.sha(core.ROOT / core.STATE)
    issues = validate_state(core.ROOT, state)
    require(not issues, '; '.join(issues))
    graph = graph_for(core.ROOT, state)
    if args.command == 'status':
        result = overview(state, graph)
    elif args.command == 'check':
        # Baseline source and final-document identity checks retain their scope.
        source = core.source_check(core.ROOT, state['latex_roots'])
        require(not source['issues'], 'Source checks failed: ' + '; '.join(source['issues']))
        import build_gap_successor_v13_1 as book
        prior = core.read(core.ROOT, state['execution_program']['predecessor']['path'])
        preserved_book = book.check(prior['successor_document'], prior)
        current = ({'status': 'pass', 'pages': state['reader']['pages'], 'final_acceptance': False}
                   if state['execution_program'].get('working_releases') else preserved_book)
        result = {'status': 'pass', 'issues': [], 'operations': len(graph['nodes']),
                  'package_contracts': len(state['work_packages']), 'preserved_predecessor': 'pass',
                  'current_working_document': current, 'preserved_working_document': preserved_book, 'source_check': source,
                  'scope': 'Dependency/receipt/source/identity integrity; no automated scientific or external acceptance.'}
    elif args.command == 'render':
        render(core.ROOT, state); result = {'rendered': True}
    elif args.command == 'deliver':
        binding = {'path': args.manifest, 'sha256': core.sha(core.safe(core.ROOT, args.manifest)), 'anchor': 'Reviewed versioned working-book delivery'}
        release = validate_working_release(core.ROOT, binding)
        state['execution_program'].setdefault('working_releases', []).append(binding)
        state['reader'] = {k: release['pdf'][k] for k in ('path', 'sha256')}
        state['reader'].update(pages=release['pages'], status='Working monograph; not I02 acceptance')
        state['deliveries'].append({**state['reader']})
        core.commit_state(core.ROOT, before, state, {'action': 'v14_deliver_working_book', 'manifest': binding,
                                                  'original_gap_qualification': False, 'final_acceptance': False})
        result = {'delivered': state['reader'], 'continuation': overview(state, graph)}
    elif args.command in ('package', 'intake'):
        forwarded = args.arguments if args.command == 'package' else ['intake', args.input, '--receipt', args.receipt]
        require(forwarded and forwarded[0] in ('next', 'template', 'register', 'record', 'intake'), 'Use operation-level status/check; only reviewed package receipt operations are forwarded')
        sys.argv = [sys.argv[0]] + forwarded
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            core.cli()
        state = core.read(core.ROOT, core.STATE)
        result = {'package_result': stream.getvalue().strip(), 'continuation': overview(state, graph)}
    else:
        selected = args.operation if args.command != 'next' else args.operation or overview(state, graph)['next']
        if selected is None:
            result = overview(state, graph)
        else:
            node = operation(graph, selected)
            if args.command == 'next':
                result = {'operation': node, 'blockers': blockers(state, node),
                          'recorded': state['execution_program']['results'].get(node['id']),
                          'continuation_rule': 'Do the eligible scoped work, review it, record result or blocker, and continue the next ready lane without a phase stop.'}
            elif args.command == 'template':
                result = receipt_template(node)
            else:
                execution = state['execution_program']
                require(node['id'] not in execution['results'], 'Operation already has a preserved outcome; use a reviewed successor for new scope')
                binding = {'path': args.receipt, 'sha256': core.sha(core.safe(core.ROOT, args.receipt)),
                           'anchor': 'Reviewed ' + args.command + ' evidence for ' + node['id'],
                           'sequence': len(execution['turns'])}
                evidence = core.read(core.ROOT, args.receipt)
                if args.command == 'record':
                    validate_operation_receipt(core.ROOT, state, node, evidence, binding['sequence'])
                    binding.update(outcome=evidence['outcome'], capabilities=evidence.get('capabilities', []))
                    execution['results'][node['id']] = binding
                    execution['blocks'].pop(node['id'], None)
                elif args.command == 'register':
                    require(node['id'] not in execution['registrations'], 'Registration is immutable')
                    require(not blockers(state, node, include_protocol=False), 'Protocol execution inputs are not ready')
                    binding['registered_at'] = core.now()
                    validate_protocol(core.ROOT, state, node, binding)
                    execution['registrations'][node['id']] = binding
                elif args.command == 'block':
                    require(evidence.get('reason') and evidence.get('revisit_trigger') and evidence.get('evidence'), 'Blocker needs a reason, evidence and revisit trigger')
                    for item in evidence['evidence']:
                        core.bound(core.ROOT, item)
                    execution['blocks'][node['id']] = {'reason': evidence['reason'], 'revisit_trigger': evidence['revisit_trigger'],
                                                     'evidence': evidence['evidence'], 'receipt': binding}
                elif args.command == 'progress':
                    require(evidence.get('finding') and evidence.get('next_action') and evidence.get('evidence'), 'Progress needs observed evidence and a concrete continuation')
                    for item in evidence['evidence']:
                        core.bound(core.ROOT, item)
                    execution['progress'].setdefault(node['id'], []).append(binding)
                else:
                    require(node['id'] in execution['blocks'], 'Operation is not blocked')
                    require(evidence.get('resolution') and evidence.get('evidence'), 'Resume requires evidence that the blocking condition changed')
                    for item in evidence['evidence']:
                        core.bound(core.ROOT, item)
                    execution['blocks'].pop(node['id'])
                commit(core.ROOT, before, state, node, args.command, {'receipt': binding})
                result = {'status': args.command + 'ed', 'operation': node['id'], 'continuation': overview(state, graph)}
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, OSError, subprocess.SubprocessError) as exc:
        raise SystemExit(str(exc))
