#!/usr/bin/env python3
"""Frozen, bounded I2 reference examples; no performance/coverage benchmark."""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from causalbank.operation_contract_v12 import context_digest, validate_response
from causalbank.runtime_v12 import Runtime, execution_identity

BASE = ROOT / 'docs/program/execution/2026-10-13/interfaces'
OUT = BASE / 'examples'
STATE = ROOT / '.runtime/interface-i2-20261013'


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise ValueError('Preserve prior evidence; output already exists: ' + str(path))
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + '\n')


def ref(path, anchor):
    return {'path': str(path.relative_to(ROOT)),
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'anchor': anchor}


def context():
    return {
        'target': {'kind': 'average_effect', 'outcome': 'net_value',
                   'treatment': 'offer', 'contrast': '1-versus-0'},
        'population': {'definition': 'Generated eligible accounts at decision', 'unit': 'account'},
        'variables': [{'id': 'offer', 'role': 'action', 'unit': 'binary'},
                      {'id': 'net_value', 'role': 'outcome', 'unit': 'USD'},
                      {'id': 'risk', 'role': 'adjustment', 'unit': 'score'}],
        'intervention': {'kind': 'set', 'value': 'offer=1'},
        'horizon': {'value': 12, 'unit': 'months'}, 'units': ['USD'],
        'sign_convention': 'offer-minus-no-offer',
        'observation_clock': {'event_time': 'event_at', 'available_time': 'available_at',
                              'decision_time': 'decision_at', 'rule': 'strict_before_decision',
                              'alternative_justification': None},
        'sampling': {'law': 'independent_units', 'unit': 'account', 'fold_unit': 'account'},
        'assumptions': [{'id': 'graph_truth', 'statement': 'The supplied graph represents this generated example',
                         'status': 'unverified', 'evidence': []}],
        'graph': {'kind': 'DAG', 'edges': [
            {'left_node': a, 'right_node': b, 'left_mark': 'tail', 'right_mark': 'arrow',
             'evidence_type': 'assumption', 'evidence_refs': [], 'review_status': 'unverified'}
            for a, b in [('risk', 'offer'), ('risk', 'net_value'), ('offer', 'net_value')]]},
        'source_evidence': []}


def request(name, op, parameters, ctx=None, refs=None):
    return {'schema_version': 'causalbank.request/1.0.0', 'request_id': name,
            'operation': op, 'artifact_inputs': refs or [],
            'budget': {'wall_seconds': 12, 'memory_bytes': 1073741824,
                       'max_output_bytes': 100000, 'model_calls': 0},
            'parameters': parameters, 'scientific_context': ctx, 'idempotency_key': None}


def cli(q):
    env = {**os.environ, 'PYTHONPATH': str(ROOT / 'src'),
           'CAUSALBANK_STATE_ROOT': str(STATE), 'OPENBLAS_NUM_THREADS': '1',
           'OMP_NUM_THREADS': '1', 'MKL_NUM_THREADS': '1'}
    proc = subprocess.run([sys.executable, '-m', 'causalbank.cli_v12', 'operation', q['operation']],
                          input=json.dumps(q), text=True, capture_output=True, cwd=ROOT,
                          env=env, timeout=18)
    return {'exit_code': proc.returncode, 'response': json.loads(proc.stdout), 'stderr': proc.stderr}


def prepare():
    if OUT.exists() or STATE.exists():
        raise ValueError('Use a fresh successor directory for a new run')
    runtime = Runtime(STATE)
    ctx = context()
    cases = []

    def add(name, op, params, expected, c=ctx, refs=None):
        q = request(name, op, params, c, refs)
        path = OUT / 'requests' / (name + '.json')
        write(path, q)
        cases.append({'name': name, 'request': ref(path, 'Frozen complete request'), 'expected': expected})

    add('capabilities', 'capabilities.describe', {}, {'status': 'completed', 'disposition': 'computed'}, c=None)
    add('graph-syntax', 'graph.review', {'review_kind': 'syntax'}, {'status': 'completed', 'disposition': 'computed'})
    add('backdoor', 'identify.effect', {'method_id': 'backdoor'}, {'status': 'completed', 'disposition': 'computed', 'qualification': 'conditional_inference'})
    add('unsupported-discovery', 'graph.discover', {'algorithm_id': 'none', 'algorithm_version': '0'}, {'status': 'completed', 'disposition': 'unsupported'})
    c = copy.deepcopy(ctx); c['sampling']['law'] = 'dependent_months'
    add('unsupported-sampling', 'identify.effect', {'method_id': 'backdoor'}, {'status': 'completed', 'disposition': 'unsupported'}, c=c)
    c = copy.deepcopy(ctx); c['assumptions'][0]['status'] = 'contradicted'
    add('contradicted-premise', 'identify.effect', {'method_id': 'backdoor'}, {'status': 'completed', 'disposition': 'refused'}, c=c)
    algebra = [
        ('finite', [1, 0, -4], 'finite_interval', [[-2.0, 2.0]], 'b^2 <= 4'),
        ('empty', [1, 0, 1], 'empty', [], 'b^2 + 1 > 0 for every real b'),
        ('whole', [-1, 0, -1], 'whole_line', [[None, None]], '-b^2 - 1 < 0 for every real b'),
        ('disconnected', [-1, 0, 4], 'unbounded_union', [[None, -2.0], [2.0, None]], 'b^2 >= 4')]
    for name, coeff, topology, intervals, proof in algebra:
        data = {'context_sha256': context_digest(ctx), 'quadratics': [coeff]}
        write(OUT / 'inputs' / (name + '.json'), data)
        artifact = runtime.store.put(data, 'quadratic-bounds/1', 'quadratic_bounds')
        add(name, 'sensitivity.evaluate', {'family_id': 'quadratic-sublevel'},
            {'status': 'completed', 'disposition': 'computed', 'topology': topology,
             'intervals': intervals, 'independent_algebra': proof}, refs=[artifact])
    moments = {'context_sha256': context_digest(ctx), 'mean': [1., 0.],
               'lrv': [[.01, 0.], [0., 1.]], 'n': 100, 'alpha': .05, 'simultaneous': True}
    write(OUT / 'inputs/moments.json', moments)
    artifact = runtime.store.put(moments, 'moment-summary/1', 'moment_summary')
    params = {'engine_id': 'reference-moment-sets', 'estimator_id': 'gaussian-residual-inversion'}
    add('weak-moments', 'estimate.effect', params, {'status': 'completed', 'disposition': 'computed',
        'topology': 'unbounded_union', 'qualification': 'conditional_inference'}, refs=[artifact])
    c = copy.deepcopy(ctx); c['sign_convention'] = 'no-offer-minus-offer'
    add('changed-context', 'estimate.effect', params, {'status': 'failed', 'disposition': 'unavailable',
        'error_code': 'invalid_or_unavailable_input'}, c=c, refs=[artifact])
    rows = {'context_sha256': context_digest(ctx), 'rows': [
        {'event_at': '2026-01-01T00:00:00+00:00', 'available_at': '2026-01-02T00:00:00+00:00', 'decision_at': '2026-01-03T00:00:00+00:00'},
        {'event_at': '2026-01-01T00:00:00+00:00', 'available_at': '2026-01-03T00:00:00+00:00', 'decision_at': '2026-01-03T00:00:00+00:00'},
        {'event_at': '2026-01-01T00:00:00+00:00', 'decision_at': '2026-01-03T00:00:00+00:00'}]}
    write(OUT / 'inputs/clocks.json', rows)
    artifact = runtime.store.put(rows, 'observation-rows/1', 'observation_rows')
    add('clock', 'audit.observation', {'checks': ['clock']}, {'status': 'completed', 'disposition': 'computed'}, refs=[artifact])
    write(OUT / 'context.json', ctx)
    write(OUT / 'protocol.json', {
        'purpose': 'Deterministic chapter demonstrations, not empirical causal-performance qualification',
        'prepared_at': '2026-10-13', 'script': ref(Path(__file__), 'Frozen example implementation'),
        'execution_identity': execution_identity(), 'cases': cases,
        'lifecycle_plan': ['replay with changed correlation ID', 'same-key changed budget rejects',
                           'report summary retains computed/unsupported/refused declarations',
                           'poll payload state to terminal; resubmission still returns queued handle',
                           'cancel completed report does not roll back output', 'invalid CLI input returns exit 2'],
        'limits': ['No MCP execution in this continuation', 'No model calls', 'No statistical coverage or bank claim']})
    print(json.dumps({'prepared_cases': len(cases), 'protocol': str((OUT / 'protocol.json').relative_to(ROOT))}))


def verify_protocol():
    p = json.loads((OUT / 'protocol.json').read_text())
    assert p['script']['sha256'] == ref(Path(__file__), '')['sha256']
    assert p['execution_identity'] == execution_identity()
    for c in p['cases']:
        assert c['request']['sha256'] == ref(ROOT / c['request']['path'], '')['sha256']
    return p


def run_cases(first):
    p = verify_protocol()
    runtime = Runtime(STATE)
    cases = p['cases'][:6] if first else p['cases'][6:]
    for c in cases:
        q = json.loads((ROOT / c['request']['path']).read_text())
        a = runtime.invoke(q); b = cli(q)
        e = c['expected']
        checks = {'equal_responses': a == b['response'],
                  'status': a['status'] == e['status'], 'disposition': a['disposition'] == e['disposition'],
                  'exit': b['exit_code'] == (4 if e['status'] == 'failed' else 0)}
        if 'qualification' in e:
            checks['qualification'] = a['qualification']['level'] == e['qualification']
        if 'topology' in e:
            checks['topology'] = a['result']['coordinate_sets'][0]['topology'] == e['topology']
        if 'intervals' in e:
            checks['independent_set'] = a['result']['coordinate_sets'][0]['intervals'] == e['intervals']
            checks['nonprobabilistic'] = a['result']['uncertainty']['coverage'] == 'none' and a['result']['uncertainty']['level'] is None
        if 'error_code' in e:
            checks['error_code'] = a['error']['code'] == e['error_code']
        if c['name'] == 'clock':
            checks['late_and_missing'] = a['result']['payload']['clock_failures'] == [1, 2]
        if c['name'] == 'capabilities':
            checks['exact_scope'] = len(a['result']['payload']['implemented']) == 9 and 'graph.discover' not in a['result']['payload']['implemented']
        if c['name'] == 'graph-syntax':
            checks['preserved_graph'] = a['result']['payload']['graph'] == q['scientific_context']['graph']
        validate_response(q, a)
        path = OUT / 'results' / (c['name'] + '.json')
        write(path, {'request': c['request'], 'library': a, 'cli': b, 'checks': checks})
        print(json.dumps({'case': c['name'], 'checks_pass': all(checks.values()), 'exit': b['exit_code']}), flush=True)
        if not all(checks.values()):
            raise ValueError('Recorded unexpected result: ' + c['name'])


def lifecycle():
    verify_protocol()
    runtime = Runtime(STATE)
    q = request('replay-first', 'capabilities.describe', {})
    q['idempotency_key'] = 'i2-capability-replay'
    first = runtime.invoke(q)
    again = copy.deepcopy(q); again['request_id'] = 'replay-second'
    second = runtime.invoke(again)
    expected = copy.deepcopy(first); expected['request_id'] = 'replay-second'
    changed = copy.deepcopy(again); changed['budget']['wall_seconds'] = 11
    conflict = runtime.invoke(changed)
    refs = [runtime.store.put(json.loads((OUT / 'results' / (n + '.json')).read_text())['library'],
             'causalbank.response/1.0.0', 'canonical_response')
            for n in ['backdoor', 'unsupported-discovery', 'contradicted-premise']]
    reportq = request('report-submit', 'report.build', {'artifact_ids': [r['artifact_id'] for r in refs]}, refs=refs)
    reportq['idempotency_key'] = 'i2-report-declarations'
    submitted = runtime.invoke(reportq); submitted_cli = cli(reportq)
    jid = submitted['result']['payload']['job_id']
    jq = request('report-poll', 'job.status', {'job_id': jid})
    polls = []
    deadline = time.monotonic() + 8
    while time.monotonic() < deadline:
        state = runtime.invoke(jq); polls.append(state)
        if state['result']['payload']['state'] in {'completed', 'failed', 'cancelled'}:
            break
        time.sleep(.05)
    terminal = polls[-1]
    report_ref = terminal['result']['payload']['result_ref']
    report = runtime.store.get(report_ref) if report_ref else None
    resubmitted = runtime.invoke(reportq)
    cancelled = runtime.invoke(request('cancel-after-completion', 'job.cancel', {'job_id': jid}))
    invalid = copy.deepcopy(q); invalid['unrequested_option'] = True
    invalid_cli = cli(invalid)
    checks = {
        'replay_correlation_only': second == expected,
        'budget_conflict_rejected': conflict['status'] == 'rejected' and conflict['error']['code'] == 'idempotency_conflict',
        'submission_equal': submitted == submitted_cli['response'] and submitted_cli['exit_code'] == 0,
        'submission_is_handle': submitted['status'] == 'queued',
        'terminal_payload': terminal['status'] == 'completed' and terminal['result']['payload']['state'] == 'completed',
        'report_declarations': report is not None and [s['declared_disposition'] for s in report['summaries']] == ['computed', 'unsupported', 'refused'],
        'report_schema_only': report is not None and all(s['verification'] == 'schema_only_not_causal_or_external_review' for s in report['summaries']),
        'resubmission_is_handle': resubmitted == submitted,
        'cancel_is_not_rollback': cancelled['result']['payload']['state'] == 'completed' and cancelled['result']['payload']['result_ref'] == report_ref,
        'invalid_request_exit2': invalid_cli['exit_code'] == 2 and invalid_cli['response']['error']['code'] == 'invalid_request'}
    write(OUT / 'lifecycle.json', {'first': first, 'second': second, 'conflict': conflict,
          'report_request': reportq, 'submitted': submitted, 'submitted_cli': submitted_cli,
          'polls': polls, 'terminal': terminal, 'report': report, 'resubmitted': resubmitted,
          'cancelled': cancelled, 'invalid_cli': invalid_cli, 'checks': checks})
    print(json.dumps({'lifecycle_checks': checks, 'poll_count': len(polls)}))
    assert all(checks.values())


def review():
    p = verify_protocol()
    records = [OUT / 'results' / (c['name'] + '.json') for c in p['cases']] + [OUT / 'lifecycle.json']
    checks = {str(path.relative_to(OUT)): all(json.loads(path.read_text())['checks'].values()) for path in records}
    write(OUT / 'review.json', {'status': 'pass' if all(checks.values()) else 'fail', 'checks': checks,
          'protocol': ref(OUT / 'protocol.json', 'Prospectively frozen deterministic examples'),
          'records': [ref(path, 'Observed library/CLI behavior') for path in records],
          'scientific_cases': len(p['cases']), 'mcp_rerun': False,
          'execution_identity': execution_identity(), 'bank_or_empirical_accuracy_claim': False})
    print(json.dumps({'status': 'pass' if all(checks.values()) else 'fail', 'scientific_cases': len(p['cases'])}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['prepare', 'run-first', 'run-second', 'lifecycle', 'review'])
    args = parser.parse_args()
    {'prepare': prepare, 'run-first': lambda: run_cases(True), 'run-second': lambda: run_cases(False),
     'lifecycle': lifecycle, 'review': review}[args.command]()
