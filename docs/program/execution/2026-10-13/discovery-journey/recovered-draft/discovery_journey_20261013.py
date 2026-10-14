#!/usr/bin/env python3
"""Frozen discovery-boundary fixtures and prospectively registered local run."""
import argparse
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
BASE = ROOT / 'docs/program/execution/2026-10-13/discovery-journey'
DESIGN = ROOT / 'docs/program/comprehensive-v14/work/IN.JOURNEY.DESIGN.discovery/workflow-protocol.json'
LOCAL = ROOT / 'docs/program/comprehensive-v14/work/IN.JOURNEY.LOCAL.discovery/local-results.json'


def now():
    return datetime.now(timezone.utc).isoformat()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')


def ref(path, anchor):
    return {'path': str(path.relative_to(ROOT)), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'anchor': anchor}


def context():
    return {'target': {'kind': 'average_effect', 'outcome': 'value', 'treatment': 'offer', 'contrast': '1-versus-0'},
            'population': {'definition': 'Synthetic eligible accounts at the offer date', 'unit': 'account'},
            'variables': [{'id': 'offer', 'role': 'action', 'unit': 'binary'},
                          {'id': 'value', 'role': 'outcome', 'unit': 'USD'}],
            'intervention': {'kind': 'set', 'value': 'offer=1'}, 'horizon': {'value': 12, 'unit': 'months'},
            'units': ['USD'], 'sign_convention': 'offer-minus-no-offer',
            'observation_clock': {'event_time': 'event_at', 'available_time': 'available_at',
                                  'decision_time': 'decision_at', 'rule': 'strict_before_decision',
                                  'alternative_justification': None},
            'sampling': {'law': 'independent_units', 'unit': 'account', 'fold_unit': 'account'},
            'assumptions': [{'id': 'graph_truth', 'statement': 'Supplied graph and consistency/positivity are imposed, not verified',
                             'status': 'unverified', 'evidence': []}],
            'graph': {'kind': 'DAG', 'edges': [{'left_node': 'offer', 'right_node': 'value',
                       'left_mark': 'tail', 'right_mark': 'arrow', 'evidence_type': 'assumption',
                       'evidence_refs': [], 'review_status': 'unverified'}]}, 'source_evidence': []}


def fixtures():
    base = context()
    cpdag = deepcopy(base); cpdag['graph']['kind'] = 'CPDAG'; cpdag['graph']['edges'][0]['right_mark'] = 'tail'
    pag = deepcopy(base); pag['graph']['kind'] = 'PAG'; pag['graph']['edges'][0]['left_mark'] = 'circle'
    dependent = deepcopy(base); dependent['sampling']['law'] = 'dependent_months'
    contradicted = deepcopy(base); contradicted['assumptions'][0]['status'] = 'contradicted'
    cycle = deepcopy(base); cycle['graph']['edges'].append({**cycle['graph']['edges'][0], 'left_mark': 'arrow', 'right_mark': 'tail'})
    rows = [{'event_at': '2026-01-01T00:00:00+00:00', 'available_at': '2026-01-02T00:00:00+00:00', 'decision_at': '2026-01-03T00:00:00+00:00'},
            {'event_at': '2026-01-01T00:00:00+00:00', 'available_at': '2026-01-03T00:00:00+00:00', 'decision_at': '2026-01-03T00:00:00+00:00'},
            {'event_at': '2026-01-01T00:00:00+00:00', 'decision_at': '2026-01-03T00:00:00+00:00'},
            {'event_at': '2026-01-03T00:00:00+00:00', 'available_at': '2026-01-02T00:00:00+00:00', 'decision_at': '2026-01-04T00:00:00+00:00'}]
    out = []
    def add(key, op, parameters, ctx, expected, artifact=None, mutation=None):
        out.append({'id': key, 'operation': op, 'parameters': parameters, 'context': ctx,
                    'artifact': artifact, 'mutation': mutation, 'expected': expected})
    ok = {'status': 'completed', 'disposition': 'computed', 'qualification': 'execution_only'}
    unsupported = {'status': 'completed', 'disposition': 'unsupported', 'qualification': 'none', 'result': None}
    add('capabilities', 'capabilities.describe', {}, None, {**ok, 'unimplemented': 'graph.discover'})
    for key, ctx in [('dag', base), ('cpdag', cpdag), ('pag', pag)]:
        add('syntax_' + key, 'graph.review', {'review_kind': 'syntax'}, ctx, {**ok, 'graph': ctx['graph']})
    add('backdoor_dag', 'identify.effect', {'method_id': 'backdoor'}, base,
        {**ok, 'qualification': 'conditional_inference', 'expression_operator': 'adjustment_contrast'})
    add('backdoor_cpdag', 'identify.effect', {'method_id': 'backdoor'}, cpdag, unsupported)
    add('backdoor_dependent', 'identify.effect', {'method_id': 'backdoor'}, dependent, unsupported)
    add('contradicted', 'identify.effect', {'method_id': 'backdoor'}, contradicted,
        {'status': 'completed', 'disposition': 'refused', 'qualification': 'none', 'result': None})
    add('discover_unimplemented', 'graph.discover', {'algorithm_id': 'native-uninstalled', 'algorithm_version': 'proposal'}, base, unsupported)
    add('temporal_unimplemented', 'graph.review', {'review_kind': 'temporal'}, base, unsupported)
    add('cycle_invalid', 'graph.review', {'review_kind': 'syntax'}, cycle, {'invocation_error': 'invalid_request'})
    for key, coeff, topology, intervals in [
        ('rays', [-1, 0, 1], 'unbounded_union', [[None, -1], [1, None]]),
        ('empty', [1, 0, 1], 'empty', []),
        ('whole', [-1, 0, -1], 'whole_line', [[None, None]]),
        ('singleton', [1, -2, 1], 'finite_interval', [[1, 1]])]:
        add('set_' + key, 'sensitivity.evaluate', {'family_id': 'quadratic-sublevel'}, base,
            {**ok, 'coordinate_sets': [{'topology': topology, 'intervals': intervals}], 'uncertainty_kind': 'sensitivity'},
            {'schema': 'quadratic-bounds/1', 'role': 'quadratic_bounds', 'body': {'quadratics': [coeff]}})
    add('clock_failures', 'audit.observation', {'checks': ['clock']}, base,
        {**ok, 'clock_failures': [1, 2, 3]}, {'schema': 'observation-rows/1', 'role': 'observation_rows', 'body': {'rows': rows}})
    moment = {'schema': 'moment-summary/1', 'role': 'moment_summary',
              'body': {'mean': [1, 1], 'lrv': [[1, 0], [0, 1]], 'n': 100, 'alpha': .05, 'simultaneous': False}}
    params = {'engine_id': 'reference-moment-sets', 'estimator_id': 'gaussian-residual-inversion'}
    add('context_mismatch', 'estimate.effect', params, base,
        {'status': 'failed', 'disposition': 'unavailable', 'qualification': 'none', 'result': None,
         'error_code': 'invalid_or_unavailable_input'}, moment, 'change_sign_after_import')
    add('corrupt_artifact', 'estimate.effect', params, base,
        {'status': 'failed', 'disposition': 'unavailable', 'qualification': 'none', 'result': None,
         'error_code': 'artifact_access'}, moment, 'corrupt_after_import')
    add('engine_uninstalled', 'estimate.effect', {'engine_id': 'native-uninstalled', 'estimator_id': 'proposal'}, base, unsupported)
    assert len(out) == 19
    return out


def prepare():
    from causalbank.operation_service_v12 import validate_request
    from causalbank.operation_contract_v12 import context_digest
    BASE.mkdir(parents=True, exist_ok=True)
    cases = fixtures()
    for case in cases:
        q = make_request(case, [])
        try:
            validate_request(q)
            assert 'invocation_error' not in case['expected'], case['id']
        except ValueError as exc:
            assert case['id'] == 'cycle_invalid' and 'directed cycle' in str(exc)
    write(BASE / 'fixtures.json', {'kind': 'authored_fixed_boundary_cases', 'cases': cases,
                                 'seed': 26101307, 'seed_role': 'fixture-version identity; no random draws'})
    write(BASE / 'design-preflight.json', {
        'status': 'pass', 'issues': [], 'cases': len(cases), 'schema_valid_cases': 18,
        'intentional_invalid_cycle': 1, 'invocation_performed': False,
        'independent_oracles': ['Backdoor graph is A->Y with no backdoor path; supplied CPDAG is not a DAG.',
                                'Factor -x^2+1<=0 gives two rays; x^2+1 gives empty; -x^2-1 whole line; (x-1)^2 singleton.',
                                'Timezone-aware event<=available<decision admits row 0 only.',
                                'Context digest changes when sign changes; cached old context cannot be reused.'],
        'base_context_sha256': context_digest(context())})
    print(json.dumps({'prepared': len(cases), 'prospective_calls': len(cases)*4+2,
                      'runtime_trial_executed': False}))


def make_request(case, refs, phase='initial'):
    return {'schema_version': 'causalbank.request/1.0.0', 'request_id': case['id'] + '-' + phase,
            'operation': case['operation'], 'artifact_inputs': refs,
            'budget': {'wall_seconds': 15, 'memory_bytes': 1024**3, 'max_output_bytes': 100000, 'model_calls': 0},
            'parameters': deepcopy(case['parameters']), 'scientific_context': deepcopy(case['context']),
            'idempotency_key': 'discovery-journey-' + case['id']}


def verdict(case, q, r):
    from causalbank.operation_contract_v12 import context_digest
    e = case['expected']; failures = []
    if 'invocation_error' in e:
        return [] if r.get('invocation_error') == e['invocation_error'] else ['expected invalid request']
    if 'invocation_error' in r:
        return ['unexpected invocation error']
    for field in ['status', 'disposition']:
        if r.get(field) != e[field]: failures.append(field)
    if r.get('qualification', {}).get('level') != e['qualification']: failures.append('qualification')
    if r.get('context_sha256') != context_digest(q['scientific_context']): failures.append('context_sha256')
    value = r.get('result') or {}; payload = value.get('payload', {})
    checks = {'result': r.get('result'), 'graph': payload.get('graph'),
              'expression_operator': payload.get('expression', {}).get('operator'),
              'coordinate_sets': value.get('coordinate_sets'), 'clock_failures': payload.get('clock_failures'),
              'uncertainty_kind': (value.get('uncertainty') or {}).get('kind'),
              'error_code': (r.get('error') or {}).get('code')}
    for field, actual in checks.items():
        if field in e and actual != e[field]: failures.append(field)
    if 'unimplemented' in e and e['unimplemented'] not in payload.get('unimplemented', []):
        failures.append('unimplemented')
    return failures


def run():
    import run_program as control
    from causalbank.artifacts_v12 import ArtifactStore, encode
    from causalbank.operation_contract_v12 import context_digest
    from causalbank.runtime_v12 import Runtime
    state = control.core.read(ROOT, control.core.STATE)
    g, merged, _ = control.combined(ROOT, state)
    key = 'IN.JOURNEY.LOCAL.discovery'
    node = control.ledger.operation(g, key)
    registration = merged['execution_program']['registrations'].get(key)
    assert registration, 'Register the exact reviewed protocol before invoking the trial'
    control.ledger.validate_protocol(ROOT, merged, node, registration)
    cases = json.loads((BASE / 'fixtures.json').read_text())['cases']
    journal_path = BASE / 'local-journal.json'
    if journal_path.exists():
        journal = json.loads(journal_path.read_text())
        assert journal['protocol_sha256'] == registration['sha256']
    else:
        journal = {'started_at': now(), 'protocol_sha256': registration['sha256'], 'attempts': [],
                   'code': ref(Path(__file__), 'Frozen local boundary runner'), 'all_requests_retained': True}
        write(journal_path, journal)
    roots = {route: ROOT / '.runtime' / ('discovery-journey-26101307-' + route) for route in ['library', 'cli']}
    env = dict(os.environ, PYTHONPATH=str(ROOT / 'src'), OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
    def call(route, q):
        started = time.monotonic()
        if route == 'library':
            try:
                answer = Runtime(roots[route]).invoke(q)
                status = None
            except (ValueError, KeyError, TypeError) as exc:
                answer = {'invocation_error': 'invalid_request', 'error_type': type(exc).__name__, 'message': str(exc)[:200]}
                status = None
            except Exception as exc:
                answer = {'invocation_error': 'unexpected_exception', 'error_type': type(exc).__name__, 'message': str(exc)[:200]}
                status = None
        else:
            try:
                p = subprocess.run([sys.executable, '-m', 'causalbank.cli_v12', 'operation', q['operation']],
                                   input=encode(q), capture_output=True, cwd=ROOT,
                                   env=dict(env, CAUSALBANK_STATE_ROOT=str(roots[route])), timeout=20)
                answer = json.loads(p.stdout); status = p.returncode
                if 'schema_version' not in answer:
                    answer = {'invocation_error': answer.get('error', {}).get('code', 'invalid_json_response'),
                              'raw': answer}
            except Exception as exc:
                answer = {'invocation_error': 'process_failure', 'error_type': type(exc).__name__}
                status = None
        return answer, time.monotonic()-started, status
    for case in cases:
        for route in ['library', 'cli']:
            for phase in ['initial', 'restart']:
                attempt_id = case['id'] + ':' + route + ':' + phase
                if any(x['id'] == attempt_id for x in journal['attempts']): continue
                store = ArtifactStore(roots[route])
                refs = []
                if case['artifact']:
                    a = case['artifact']; body = {**a['body'], 'context_sha256': context_digest(case['context'])}
                    if case['mutation'] == 'corrupt_after_import':
                        body['fixture_identity'] = case['id']
                    refs = [store.put(body, a['schema'], a['role'])]
                q = make_request(case, refs, phase)
                if case['mutation'] == 'change_sign_after_import':
                    q['scientific_context']['sign_convention'] = 'no-offer-minus-offer'
                if case['mutation'] == 'corrupt_after_import':
                    (store.folder / (refs[0]['artifact_id'] + '.json')).write_text('{}')
                r, elapsed, status = call(route, q)
                failures = verdict(case, q, r)
                saved = {'id': attempt_id, 'case': case['id'], 'route': route, 'phase': phase,
                         'request': q, 'response': r, 'wall_seconds': elapsed, 'process_exit': status,
                         'failures': failures, 'passed': not failures, 'recorded_at': now()}
                journal['attempts'].append(saved); write(journal_path, journal)
        print(json.dumps({'case': case['id'], 'completed_requests': len(journal['attempts']),
                          'failures': sum(not x['passed'] for x in journal['attempts'])}), flush=True)
    # Change a real previously completed request while retaining its key.
    for route in ['library', 'cli']:
        attempt_id = 'idempotency_drift:' + route
        if any(x['id'] == attempt_id for x in journal['attempts']): continue
        case = next(x for x in cases if x['id'] == 'syntax_dag')
        q = make_request(case, [], 'drift');q['scientific_context']['horizon']['value'] = 24
        r, elapsed, status = call(route, q)
        passed = r.get('status') == 'rejected' and (r.get('error') or {}).get('code') == 'idempotency_conflict' and r.get('result') is None
        journal['attempts'].append({'id': attempt_id, 'case': 'idempotency_drift', 'route': route,
            'phase': 'changed_target', 'request': q, 'response': r, 'wall_seconds': elapsed,
            'process_exit': status, 'passed': passed, 'failures': [] if passed else ['changed target reused'], 'recorded_at': now()})
        write(journal_path, journal)
    parity = []
    def canonical(response):
        if 'invocation_error' in response: return {'invocation_error': response['invocation_error']}
        return {k: v for k, v in response.items() if k != 'request_id'}
    for case in cases:
        rows = [x for x in journal['attempts'] if x['case'] == case['id']]
        parity.append({'case': case['id'], 'all_four_semantically_equal':
                       all(canonical(x['response']) == canonical(rows[0]['response']) for x in rows)})
    journal.update(completed_at=now(), parity=parity)
    write(journal_path, journal)
    count = len(cases)*4+2
    assert len(journal['attempts']) == count
    passed = all(x['passed'] for x in journal['attempts']) and all(x['all_four_semantically_equal'] for x in parity)
    result = {'operation': key, 'status': 'pass' if passed else 'negative', 'all_request_count': count,
              'passed_request_count': sum(x['passed'] for x in journal['attempts']),
              'failed_requests': [x['id'] for x in journal['attempts'] if not x['passed']],
              'parity': parity, 'retained_failures': True, 'started_at': journal['started_at'],
              'finished_at': journal['completed_at'], 'protocol_sha256': registration['sha256'],
              'journal': ref(journal_path, 'Every input, response, failure and measured duration'),
              'full_invocation_wall_seconds': sum(x['wall_seconds'] for x in journal['attempts']),
              'child_peak_rss_kib_aggregate': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
              'resource_scope': 'Includes worker/process startup and failed/replayed calls; aggregate child high-water RSS, not per-case memory or a bank cost estimate.',
              'limits': ['Nineteen authored cases and two changed-target checks; no random-sampling qualification.',
                         'No installed discovery engine, general PAG identification, live model or actual sibling consumer.',
                         'CLI/library restart replay only; MCP conformance is separate inherited/future evidence.']}
    write(LOCAL, result)
    print(json.dumps({k: result[k] for k in ['status', 'all_request_count', 'passed_request_count', 'failed_requests', 'full_invocation_wall_seconds']}))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('command', choices=['prepare', 'run'])
    args = p.parse_args()
    prepare() if args.command == 'prepare' else run()
