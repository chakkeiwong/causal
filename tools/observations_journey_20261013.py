#!/usr/bin/env python3
"""Frozen observation-workflow boundary cases; final calls require registration."""
import argparse
from copy import deepcopy
import hashlib
import json
import math
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

import discovery_journey_20261013 as shared
import funding_journey_successor_20261013 as funding
import observations_examples_20261013 as examples

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
BASE = ROOT / 'docs/program/execution/2026-10-13/observations-journey'
DESIGN = ROOT / 'docs/program/comprehensive-v14/work/IN.JOURNEY.DESIGN.observations/workflow-protocol.json'
LOCAL = ROOT / 'docs/program/comprehensive-v14/work/IN.JOURNEY.LOCAL.observations/local-results.json'
ref, write, now = shared.ref, shared.write, shared.now
ALPHA = math.erfc(math.sqrt(2))


def context():
    ctx = shared.context()
    ctx['target'] = {'kind': 'twelve_month_event_risk_difference', 'outcome': 'event',
                     'treatment': 'contact', 'contrast': '1-versus-0'}
    ctx['variables'] = [{'id': 'contact', 'role': 'action', 'unit': 'binary'},
                        {'id': 'event', 'role': 'outcome', 'unit': 'binary_adverse_event'}]
    ctx['intervention'] = {'kind': 'set', 'value': 'contact=1'}
    ctx['units'] = ['event_probability']
    ctx['population'] = {'definition': 'Generated eligible borrower origins; inclusion and label law are supplied declarations', 'unit': 'borrower_origin'}
    ctx['sampling'] = {'law': 'declared_clustered_origins', 'unit': 'borrower_origin', 'fold_unit': 'household'}
    ctx['assumptions'] = [
        {'id': key, 'statement': statement, 'status': 'unverified', 'evidence': []}
        for key, statement in [('measurement', 'Origin identity, label sensitivity/specificity and inclusion law need separate evidence.'),
                               ('joint_covariance', 'Supplied covariance includes shared-map, audit-estimation and sampling uncertainty.'),
                               ('causal_effect', 'Assignment, positivity and the contact effect are not established by an observation audit.')]]
    ctx['graph'] = None
    return ctx


def fixtures():
    base = context(); out = []
    ok = {'status': 'completed', 'disposition': 'computed', 'qualification': 'execution_only'}
    unsupported = {'status': 'completed', 'disposition': 'unsupported', 'qualification': 'none', 'result': None}
    failed = {'status': 'failed', 'disposition': 'unavailable', 'qualification': 'none',
              'result': None, 'error_code': 'invalid_or_unavailable_input'}
    row = {'event_at': '2026-01-01T00:00:00+00:00', 'available_at': '2026-01-02T00:00:00+00:00',
           'decision_at': '2026-01-03T00:00:00+00:00'}
    def art(rows, schema='observation-rows/1'):
        return {'schema': schema, 'role': 'observation_rows', 'body': {'rows': rows}}
    def add(key, operation, params, expected, artifact=None, ctx=None, mutation=None):
        out.append({'id': key, 'operation': operation, 'parameters': params, 'expected': expected,
                    'artifact': artifact, 'context': deepcopy(base if ctx is None else ctx), 'mutation': mutation})
    def audit(key, rows, bad, ctx=None):
        add(key, 'audit.observation', {'checks': ['clock']},
            {**ok, 'clock_failures': bad, 'row_count': len(rows), 'all_declared_clocks_pass': not bad,
             'audit_boundary': 'Timestamp consistency only; source ownership, inclusion and truth remain unverified'}, art(rows), ctx)
    valid = [row, {**row, 'available_at': row['event_at']},
             {**row, 'event_at': '2026-01-01T08:00:00+08:00', 'available_at': '2026-01-02T08:00:00+08:00'}]
    audit('clock_valid', valid, [])
    bad = [{**row, 'available_at': row['decision_at']},
           {**row, 'available_at': '2026-01-04T00:00:00+00:00'},
           {**row, 'available_at': '2026-01-02T00:00:00'},
           {'event_at': row['event_at'], 'decision_at': row['decision_at']},
           {**row, 'event_at': '2026-01-02T01:00:00+00:00'},
           {**row, 'event_at': 42}]
    audit('clock_invalid', bad, list(range(6)))
    audit('clock_empty', [], [])
    audit('clock_duplicate_origins', [{**row, 'origin_id': 'same-borrower', 'value': 20}]*2, [])
    audit('clock_false_labels', [{**row, 'declared_label': 1, 'generated_truth': 0}], [])
    contradicted = deepcopy(base); contradicted['assumptions'][0]['status'] = 'contradicted'
    audit('clock_contradicted_identity', [row], [], contradicted)
    for key, checks in [('joint_checks', ['clock', 'identity']), ('inclusion', ['inclusion']), ('noisy_labels', ['label_truth'])]:
        add('audit_' + key + '_unsupported', 'audit.observation', {'checks': checks}, dict(unsupported), art([row]))
    alternate = deepcopy(base)
    alternate['observation_clock'].update(rule='explicit_alternative', alternative_justification='Outcomes occur during subsequent follow-up; this is not a feature admission clock.')
    add('alternate_clock_unsupported', 'audit.observation', {'checks': ['clock']}, dict(unsupported), art([row]), alternate)
    add('missing_rows', 'audit.observation', {'checks': ['clock']}, dict(failed))
    add('wrong_artifact_schema', 'audit.observation', {'checks': ['clock']}, dict(failed), art([row], 'moment-summary/1'))
    add('malformed_rows', 'audit.observation', {'checks': ['clock']}, dict(failed), art({'row': row}))
    for key, mutation, error in [('clock_context_mismatch', 'change_clock_after_import', 'invalid_or_unavailable_input'),
                                 ('corrupt_artifact', 'corrupt_after_import', 'artifact_access'),
                                 ('custody_mismatch', 'change_custody_after_import', 'artifact_access'),
                                 ('population_hash_mismatch', 'change_population_after_import', 'invalid_or_unavailable_input')]:
        add(key, 'audit.observation', {'checks': ['clock']}, {**failed, 'error_code': error}, art([row]), mutation=mutation)
    audit('future_outcomes_misclassified_as_features', [{**row, 'event_at': '2026-07-01T00:00:00+00:00',
                                                       'available_at': '2026-07-02T00:00:00+00:00'}], [0])
    add('measurement_fitting_unimplemented', 'estimate.effect', {'engine_id': 'raw-measurement-correction', 'estimator_id': 'joint-audit'}, dict(unsupported))
    # Stipulated Gaussian summaries only, not moments estimated from the binary label example.
    moment = {'schema': 'moment-summary/1', 'role': 'moment_summary',
              'body': {'mean': [.24, .8], 'lrv': [[.04, 0], [0, 0]], 'n': 100, 'alpha': ALPHA, 'simultaneous': False}}
    params = {'engine_id': 'reference-moment-sets', 'estimator_id': 'gaussian-residual-inversion'}
    mctx = deepcopy(base); mctx['units'] = ['event_probability']
    mctx['target']['kind'] = 'measurement_prevalence_surrogate_not_causal_effect'
    mctx['target']['contrast'] = 'supplied_report_rate_minus_false_positive_over_sensitivity_difference'
    mctx['intervention'] = {'kind': 'measurement_only', 'value': 'No intervention contrast is estimated; contact is the separately proposed downstream action.'}
    for key, variance, interval in [('moment_unverified_measurement', .04, [.25, .35]),
                                    ('moment_corrected_covariance', .16, [.2, .4])]:
        a = deepcopy(moment); a['body']['lrv'][0][0] = variance
        add(key, 'estimate.effect', params, {**ok, 'qualification': 'conditional_inference',
            'coordinate_sets': [{'topology': 'finite_interval', 'intervals': [interval]}],
            'uncertainty_kind': 'pointwise_confidence', 'coverage': 'pointwise', 'level': 1-ALPHA}, a, mctx)
    cctx = deepcopy(mctx); cctx['assumptions'][0]['status'] = 'contradicted'
    add('moment_contradicted_measurement', 'estimate.effect', params,
        {'status': 'completed', 'disposition': 'refused', 'qualification': 'none', 'result': None}, deepcopy(moment), cctx)
    for key, coefficients, topology, intervals in [
        ('finite', [80, -48, 7], 'finite_interval', [[.25, .35]]),
        ('whole', [0, 0, 0], 'whole_line', [[None, None]]),
        ('empty', [0, 0, 1], 'empty', []),
        ('rays', [-1, 0, 1], 'unbounded_union', [[None, -1], [1, None]])]:
        add('sensitivity_' + key, 'sensitivity.evaluate', {'family_id': 'quadratic-sublevel'},
            {**ok, 'coordinate_sets': [{'topology': topology, 'intervals': intervals}],
             'uncertainty_kind': 'sensitivity', 'coverage': 'none', 'level': None},
            {'schema': 'quadratic-bounds/1', 'role': 'quadratic_bounds', 'body': {'quadratics': [coefficients]}},
            mctx if key != 'rays' else base)
    assert len(out) == 26
    return out


def make_request(case, refs, phase='initial'):
    request = funding.make_request(case, refs, phase)
    request['idempotency_key'] = 'observations-journey-' + case['id']
    return request


def verdict(case, q, r):
    failures = funding.verdict(case, q, r)
    payload = (r.get('result') or {}).get('payload', {})
    for key, field in [('row_count', 'rows'), ('all_declared_clocks_pass', 'all_declared_clocks_pass'), ('audit_boundary', 'boundary')]:
        if key in case['expected'] and payload.get(field) != case['expected'][key]:
            failures.append(key)
    return failures


def prepare():
    from statistics import NormalDist
    from causalbank.operation_service_v12 import validate_request
    assert not DESIGN.exists() and not (BASE / 'fixtures.json').exists(), 'Preserve frozen design'
    cases = fixtures()
    for case in cases:
        validate_request(make_request(case, []))
    assert abs(NormalDist().inv_cdf(1-ALPHA/2)-2) < 1e-14
    assert examples.calculate() == json.loads((BASE / 'exact-examples.json').read_text())
    write(BASE / 'fixtures.json', {'kind': 'authored_fixed_observation_boundary_cases', 'seed': 26101309,
                                  'seed_role': 'Fixture version only; no random sampling', 'cases': cases})
    write(BASE / 'design-preflight.json', {'status': 'pass', 'issues': [], 'cases': len(cases),
          'schema_valid_declarations': len(cases), 'final_service_invocations': 0,
          'independent_references': 'Explicit timestamp orders, exact finite laws and factored polynomials; normal critical two from a separate standard-library calculation.',
          'scope': 'Request validation only, no final service call', 'prospective_invocations': 4*len(cases)+2,
          'endpoint_tolerance': {'absolute': 1e-9, 'relative': 1e-10}})
    print(json.dumps({'prepared_cases': len(cases), 'prospective_invocations': 4*len(cases)+2, 'final_trial_executed': False}))


def run(max_new_attempts=None):
    import run_program as control
    from causalbank.artifacts_v12 import ArtifactStore, encode
    from causalbank.operation_contract_v12 import context_digest
    from causalbank.runtime_v12 import Runtime
    state = control.core.read(ROOT, control.core.STATE)
    g, merged, _ = control.combined(ROOT, state)
    key = 'IN.JOURNEY.LOCAL.observations'
    node = control.ledger.operation(g, key)
    registration = merged['execution_program']['registrations'].get(key)
    assert registration, 'Register the exact reviewed protocol before invoking the trial'
    control.ledger.validate_protocol(ROOT, merged, node, registration)
    if LOCAL.exists():
        existing = json.loads(LOCAL.read_text())
        assert existing['protocol_sha256'] == registration['sha256']
        assert ref(BASE / 'local-journal.json', '')['sha256'] == existing['journal']['sha256']
        print(json.dumps({'already_completed': True, 'status': existing['status'], 'no_trials_repeated': True}))
        return
    cases = json.loads((BASE / 'fixtures.json').read_text())['cases']
    journal_path = BASE / 'local-journal.json'
    roots = {route: ROOT / '.runtime' / ('observations-journey-26101309-' + route) for route in ['library', 'cli']}
    if journal_path.exists():
        journal = json.loads(journal_path.read_text())
        assert journal['protocol_sha256'] == registration['sha256']
    else:
        assert all(not p.exists() for p in roots.values()), 'Fresh study requires unused operator roots'
        journal = {'started_at': now(), 'protocol_sha256': registration['sha256'], 'attempts': [],
                   'prepared_requests': {}, 'segments': [],
                   'code': ref(Path(__file__), 'Frozen observation boundary runner; uses reviewed checkpoint/restart pattern'), 'all_requests_retained': True}
        write(journal_path, journal)
    assert len({a['id'] for a in journal['attempts']}) == len(journal['attempts'])
    segment_started = time.monotonic()
    before_count = len(journal['attempts'])
    segment = {'started_at': now(), 'prior_request_count': before_count,
               'prior_attempts_sha256': hashlib.sha256(encode(journal['attempts'])).hexdigest()}
    journal['segments'].append(segment)
    write(journal_path, journal)
    def checkpoint():
        segment.update(finished_at=now(), new_request_count=len(journal['attempts'])-before_count,
                       segment_wall_seconds=time.monotonic()-segment_started,
                       child_peak_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                       parent_peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        write(journal_path, journal)
        if max_new_attempts and len(journal['attempts'])-before_count >= max_new_attempts:
            print(json.dumps({'checkpoint': True, 'completed_requests': len(journal['attempts']),
                              'remaining_requests': len(cases)*4+2-len(journal['attempts'])}), flush=True)
            return True
        return False
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
                prepared_id = case['id'] + ':' + route
                if prepared_id not in journal['prepared_requests']:
                    refs = []
                    if case['artifact']:
                        a = case['artifact']; body = {**a['body'], 'context_sha256': context_digest(case['context'])}
                        if case['mutation'] == 'corrupt_after_import':
                            body['fixture_identity'] = case['id']
                        refs = [store.put(body, a['schema'], a['role'])]
                    q = make_request(case, refs)
                    if case['mutation'] == 'change_clock_after_import':
                        q['scientific_context']['observation_clock']['available_time'] = 'revised_available_at'
                    if case['mutation'] == 'change_units_after_import':
                        q['scientific_context']['units'] = ['USD_average_balance_per_percentage_point']
                    if case['mutation'] == 'change_custody_after_import':
                        q['artifact_inputs'][0]['custody'] = 'unverified_other_owner'
                    if case['mutation'] == 'change_population_after_import':
                        q['scientific_context']['population']['definition'] = 'A different selected population'
                    journal['prepared_requests'][prepared_id] = q
                    write(journal_path, journal)
                q = deepcopy(journal['prepared_requests'][prepared_id])
                q['request_id'] = case['id'] + '-' + phase
                if case['mutation'] == 'corrupt_after_import':
                    (store.folder / (q['artifact_inputs'][0]['artifact_id'] + '.json')).write_text('{}')
                r, elapsed, status = call(route, q)
                failures = verdict(case, q, r)
                if route == 'cli':
                    expected_exit = 2 if 'invocation_error' in case['expected'] else 4 if case['expected']['status'] == 'failed' else 0
                    if status != expected_exit:
                        failures.append('cli_exit')
                saved = {'id': attempt_id, 'case': case['id'], 'route': route, 'phase': phase,
                         'request': q, 'response': r, 'wall_seconds': elapsed, 'process_exit': status,
                         'failures': failures, 'passed': not failures, 'recorded_at': now()}
                journal['attempts'].append(saved); write(journal_path, journal)
                if checkpoint(): return
        print(json.dumps({'case': case['id'], 'completed_requests': len(journal['attempts']),
                          'failures': sum(not x['passed'] for x in journal['attempts'])}), flush=True)
    # Change a real previously completed request while retaining its key.
    for route in ['library', 'cli']:
        attempt_id = 'idempotency_drift:' + route
        if any(x['id'] == attempt_id for x in journal['attempts']): continue
        case = next(x for x in cases if x['id'] == 'clock_valid')
        q = deepcopy(journal['prepared_requests'][case['id']+':'+route]); q['request_id'] = case['id']+'-drift'
        q['scientific_context']['horizon']['value'] = 24
        r, elapsed, status = call(route, q)
        passed = (r.get('status') == 'rejected' and (r.get('error') or {}).get('code') == 'idempotency_conflict'
                  and r.get('result') is None and (route != 'cli' or status == 4))
        journal['attempts'].append({'id': attempt_id, 'case': 'idempotency_drift', 'route': route,
            'phase': 'changed_target', 'request': q, 'response': r, 'wall_seconds': elapsed,
            'process_exit': status, 'passed': passed, 'failures': [] if passed else ['changed target reused'], 'recorded_at': now()})
        write(journal_path, journal)
        if checkpoint(): return
    parity = []
    def canonical(response):
        if 'invocation_error' in response: return {'invocation_error': response['invocation_error']}
        return {k: v for k, v in response.items() if k != 'request_id'}
    for case in cases:
        rows = [x for x in journal['attempts'] if x['case'] == case['id']]
        parity.append({'case': case['id'], 'all_four_semantically_equal':
                       all(canonical(x['response']) == canonical(rows[0]['response']) for x in rows)})
    checkpoint()
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
              'active_runner_wall_seconds': sum(x['segment_wall_seconds'] for x in journal['segments']),
              'child_peak_rss_kib_aggregate': max(x['child_peak_rss_kib'] for x in journal['segments']),
              'parent_peak_rss_kib_aggregate': max(x['parent_peak_rss_kib'] for x in journal['segments']),
              'segment_count': len(journal['segments']),
              'resource_scope': 'Invocation wall includes worker/process startup and failed/replayed calls; runner wall includes fixture import and journaling, excludes time between segments and initial Python/module startup. RSS is a process high-water maximum, not concurrent tree memory. No bank cost estimate.',
              'limits': ['Twenty-six authored observation cases and two changed-horizon checks; no empirical coverage qualification.',
                         'No raw-data measurement fitting, verified identity/inclusion/label truth, live model or actual sibling consumer.',
                         'CLI/library restart replay only; MCP conformance is separate inherited/future evidence.']}
    write(LOCAL, result)
    print(json.dumps({k: result[k] for k in ['status', 'all_request_count', 'passed_request_count', 'failed_requests', 'full_invocation_wall_seconds']}))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('command', choices=['prepare', 'run'])
    p.add_argument('--max-new-attempts', type=int)
    args = p.parse_args()
    if args.max_new_attempts is not None and args.max_new_attempts < 1:
        p.error('--max-new-attempts must be positive')
    prepare() if args.command == 'prepare' else run(args.max_new_attempts)
