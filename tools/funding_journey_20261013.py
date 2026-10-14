#!/usr/bin/env python3
"""Prospective funding boundary screen, using the preserved discovery runner pattern."""
import argparse
from copy import deepcopy
import json
import math
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

import discovery_journey_20261013 as shared

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
BASE = ROOT / 'docs/program/execution/2026-10-13/funding-journey'
DESIGN = ROOT / 'docs/program/comprehensive-v14/work/IN.JOURNEY.DESIGN.funding/workflow-protocol.json'
LOCAL = ROOT / 'docs/program/comprehensive-v14/work/IN.JOURNEY.LOCAL.funding/local-results.json'
ref, write, now = shared.ref, shared.write, shared.now
ALPHA = math.erfc(math.sqrt(2))  # Two-sided standard-normal critical is 2.
UNIT = 'million_USD_average_balance_per_percentage_point'
PARAMS = {'engine_id': 'reference-moment-sets', 'estimator_id': 'gaussian-residual-inversion'}


def context():
    return {'target': {'kind': 'normalized_structural_response', 'outcome': 'balance', 'treatment': 'quote',
                       'contrast': 'one-percentage-point-normalization'},
            'population': {'definition': 'Authored funding portfolio with fixed household identities and a monthly origin clock', 'unit': 'portfolio_month'},
            'variables': [{'id': 'quote', 'role': 'action', 'unit': 'percentage_point'},
                          {'id': 'balance', 'role': 'outcome', 'unit': 'million_USD_twelve_month_average'}],
            'intervention': {'kind': 'normalized_shock', 'value': 'quote increase one percentage point; a quarter-point decision additionally assumes local linearity'},
            'horizon': {'value': 12, 'unit': 'months'}, 'units': [UNIT],
            'sign_convention': 'increase-minus-no-increase',
            'observation_clock': {'event_time': 'event_at', 'available_time': 'available_at', 'decision_time': 'decision_at',
                                  'rule': 'strict_before_decision', 'alternative_justification': None},
            'sampling': {'law': 'dependent_monthly_origins', 'unit': 'portfolio_month', 'fold_unit': 'time_block'},
            'assumptions': [
                {'id': key, 'statement': statement, 'status': 'unverified', 'evidence': []}
                for key, statement in [
                    ('causal_normalization', 'Proxy exclusion/exogeneity and a stable normalized response are supplied premises.'),
                    ('joint_covariance', 'Supplied LRV includes all fitted nuisance, serial, cross-outcome and denominator uncertainty; validity is unverified.'),
                    ('identity_inclusion', 'Target household map, population and positive inclusion probabilities require separate evidence.'),
                    ('local_linearity', 'Scaling to a quarter-point intervention is a scenario assumption, not established by a moment artifact.')]],
            'graph': None, 'source_evidence': []}


def fixtures():
    base = context(); out = []
    ok = {'status': 'completed', 'disposition': 'computed', 'qualification': 'conditional_inference'}
    unavailable = {'status': 'failed', 'disposition': 'unavailable', 'qualification': 'none',
                   'result': None, 'error_code': 'invalid_or_unavailable_input'}
    unsupported = {'status': 'completed', 'disposition': 'unsupported', 'qualification': 'none', 'result': None}
    def add(key, op, parameters, ctx, expected, artifact=None, mutation=None):
        out.append({'id': key, 'operation': op, 'parameters': parameters, 'context': deepcopy(ctx),
                    'expected': expected, 'artifact': artifact, 'mutation': mutation})
    def moment(mean, lrv, n=400, simultaneous=False):
        return {'schema': 'moment-summary/1', 'role': 'moment_summary',
                'body': {'mean': mean, 'lrv': lrv, 'n': n, 'alpha': ALPHA*(2 if simultaneous else 1), 'simultaneous': simultaneous}}
    def estimate(key, a, intervals, ctx=base, simultaneous=False):
        top = lambda x: 'empty' if not x else 'whole_line' if x == [[None, None]] else 'unbounded_union' if any(None in z for z in x) else 'finite_interval'
        add(key, 'estimate.effect', PARAMS, ctx, {**ok, 'coordinate_sets': [{'topology': top(x), 'intervals': x} for x in intervals],
            'uncertainty_kind': 'joint_confidence' if simultaneous else 'pointwise_confidence',
            'coverage': 'simultaneous' if simultaneous else 'pointwise', 'level': 1-a['body']['alpha'],
            'numerical_boundary': 'Double-precision numerical inversion; no finite-sample or uniform guarantee',
            'model_boundary': 'Gaussian moment approximation and supplied covariance/causal premises'}, a)
    strong = moment([2, 1], [[1, 0], [0, 0]])
    estimate('strong_fixed_denominator', strong, [[[1.9, 2.1]]])
    estimate('estimated_nuisance_covariance', moment([2, 1], [[9, 0], [0, 0]]), [[[1.7, 2.3]]])
    estimate('random_denominator', moment([2, 1], [[1, 0], [0, 1]], n=100),
             [[[(25-math.sqrt(31))/12, (25+math.sqrt(31))/12]]])
    estimate('weak_denominator_rays', moment([1, 0], [[0, 0], [0, 1]], n=4), [[[None, -1], [1, None]]])
    estimate('no_information_whole', moment([0, 0], [[1, 0], [0, 1]], n=4), [[[None, None]]])
    estimate('incompatible_zero_noise_empty', moment([1, 0], [[0, 0], [0, 0]], n=4), [[]])
    estimate('zero_noise_singleton', moment([2, 1], [[0, 0], [0, 0]], n=4), [[[2, 2]]])
    vector = deepcopy(base)
    vector['target'].update(kind='ordered_vector_balance_then_cost', outcome='funding_outcomes')
    vector['variables'] += [{'id': 'cost', 'role': 'outcome', 'unit': 'million_USD_cumulative'},
                            {'id': 'funding_outcomes', 'role': 'outcome', 'unit': 'ordered_twelve_month_average_balance_then_cumulative_cost'}]
    vector['units'] += ['million_USD_cumulative_cost_per_percentage_point']
    estimate('two_outcome_bonferroni', moment([2, 1, 1], [[1, .5, 0], [.5, 4, 0], [0, 0, 0]], simultaneous=True),
             [[[1.9, 2.1]], [[.8, 1.2]]], vector, True)
    for key, field, value in [
        ('invalid_units_dimension', 'mean', [2, 1, 1]),
        ('nonsymmetric_covariance', 'lrv', [[1, 1], [0, 1]]),
        ('indefinite_covariance', 'lrv', [[1, 2], [2, 1]]),
        ('too_few_origins', 'n', 2), ('invalid_alpha', 'alpha', 1),
        ('invalid_simultaneous_type', 'simultaneous', 'true')]:
        a = deepcopy(strong); a['body'][field] = value
        add(key, 'estimate.effect', PARAMS, base, dict(unavailable), a)
    add('missing_moment_artifact', 'estimate.effect', PARAMS, base, dict(unavailable))
    for key, mutation, error in [('clock_context_mismatch', 'change_clock_after_import', 'invalid_or_unavailable_input'),
                                ('units_context_mismatch', 'change_units_after_import', 'invalid_or_unavailable_input'),
                                ('corrupt_artifact', 'corrupt_after_import', 'artifact_access')]:
        add(key, 'estimate.effect', PARAMS, base, {**unavailable, 'error_code': error}, deepcopy(strong), mutation)
    for key, statement in [('unresolved_link_map', 'Two household partitions fit the records; map unresolved.'),
                           ('unknown_inclusion', 'Selection probabilities and unobserved households remain unknown.')]:
        ctx = deepcopy(base); ctx['assumptions'][2]['statement'] = statement
        estimate(key, deepcopy(strong), [[[1.9, 2.1]]], ctx)
    for key, index in [('contradicted_identity', 2), ('contradicted_covariance', 1)]:
        ctx = deepcopy(base); ctx['assumptions'][index]['status'] = 'contradicted'
        add(key, 'estimate.effect', PARAMS, ctx, {'status': 'completed', 'disposition': 'refused',
            'qualification': 'none', 'result': None}, deepcopy(strong))
    continuous = deepcopy(base)
    continuous['sampling']['law'] = 'independent_units'
    continuous['graph'] = {'kind': 'DAG', 'edges': [{'left_node': 'quote', 'right_node': 'balance', 'left_mark': 'tail',
        'right_mark': 'arrow', 'evidence_type': 'assumption', 'evidence_refs': [], 'review_status': 'unverified'}]}
    add('continuous_backdoor_unsupported', 'identify.effect', {'method_id': 'backdoor'}, continuous, dict(unsupported))
    dependent = deepcopy(continuous); dependent['target']['contrast'] = '1-versus-0'
    dependent['sampling']['law'] = 'dependent_monthly_origins'
    add('panel_backdoor_unsupported', 'identify.effect', {'method_id': 'backdoor'}, dependent, dict(unsupported))
    rows = [
        {'event_at': '2026-01-01T00:00:00+00:00', 'available_at': '2026-01-02T00:00:00+00:00', 'decision_at': '2026-01-03T00:00:00+00:00'},
        {'event_at': '2026-01-01T00:00:00+00:00', 'available_at': '2026-01-03T00:00:00+00:00', 'decision_at': '2026-01-03T00:00:00+00:00'},
        {'event_at': '2026-01-01T00:00:00+00:00', 'decision_at': '2026-01-03T00:00:00+00:00'},
        {'event_at': '2026-01-03T00:00:00+00:00', 'available_at': '2026-01-02T00:00:00+00:00', 'decision_at': '2026-01-04T00:00:00+00:00'},
        {'event_at': '2026-01-01T00:00:00', 'available_at': '2026-01-02T00:00:00', 'decision_at': '2026-01-03T00:00:00'}]
    add('clock_failures', 'audit.observation', {'checks': ['clock']}, base,
        {'status': 'completed', 'disposition': 'computed', 'qualification': 'execution_only', 'clock_failures': [1, 2, 3, 4]},
        {'schema': 'observation-rows/1', 'role': 'observation_rows', 'body': {'rows': rows}})
    add('identity_inclusion_audit_unavailable', 'audit.observation', {'checks': ['identity', 'inclusion']}, base, dict(unsupported))
    add('nuisance_fitting_uninstalled', 'estimate.effect', {'engine_id': 'fitted-joint-nuisance', 'estimator_id': 'proposal'}, base, dict(unsupported))
    add('design_unimplemented', 'design.evaluate', {'candidate_design_ids': ['quarter-point-funding']}, base, dict(unsupported))
    add('economic_break_even_sensitivity', 'sensitivity.evaluate', {'family_id': 'quadratic-sublevel'}, base,
        {'status': 'completed', 'disposition': 'computed', 'qualification': 'execution_only',
         'coordinate_sets': [{'topology': 'unbounded_union', 'intervals': [[28/15, None]]}], 'uncertainty_kind': 'sensitivity'},
        {'schema': 'quadratic-bounds/1', 'role': 'quadratic_bounds', 'body': {'quadratics': [[0, -3750, 7000]]}})
    assert len(out) == 29
    return out


def make_request(case, refs, phase='initial'):
    return {'schema_version': 'causalbank.request/1.0.0', 'request_id': case['id']+'-'+phase,
            'operation': case['operation'], 'artifact_inputs': refs,
            'budget': {'wall_seconds': 15, 'memory_bytes': 1024**3, 'max_output_bytes': 100000, 'model_calls': 0},
            'parameters': deepcopy(case['parameters']), 'scientific_context': deepcopy(case['context']),
            'idempotency_key': 'funding-journey-'+case['id']}


def close(left, right):
    if isinstance(left, (float, int)) and not isinstance(left, bool) and isinstance(right, (float, int)) and not isinstance(right, bool):
        return math.isclose(left, right, rel_tol=1e-10, abs_tol=1e-9)
    if type(left) is not type(right): return False
    if isinstance(left, list): return len(left) == len(right) and all(close(a, b) for a, b in zip(left, right))
    if isinstance(left, dict): return left.keys() == right.keys() and all(close(left[k], right[k]) for k in left)
    return left == right


def verdict(case, q, r):
    from causalbank.operation_contract_v12 import context_digest
    e = case['expected']; failures = []
    if 'invocation_error' in r: return ['unexpected invocation error']
    for field in ['status', 'disposition']:
        if r.get(field) != e[field]: failures.append(field)
    if r.get('qualification', {}).get('level') != e['qualification']: failures.append('qualification')
    if r.get('context_sha256') != context_digest(q['scientific_context']): failures.append('context_sha256')
    value = r.get('result') or {}; payload = value.get('payload', {}); uncertainty = value.get('uncertainty') or {}
    checks = {'result': r.get('result'), 'coordinate_sets': value.get('coordinate_sets'),
              'clock_failures': payload.get('clock_failures'), 'uncertainty_kind': uncertainty.get('kind'),
              'coverage': uncertainty.get('coverage'), 'level': uncertainty.get('level'),
              'numerical_boundary': uncertainty.get('numerical_error'), 'model_boundary': payload.get('model_boundary'),
              'error_code': (r.get('error') or {}).get('code')}
    for field, actual in checks.items():
        if field in e and not close(actual, e[field]): failures.append(field)
    if value.get('kind') == 'effect':
        if value.get('units') != q['scientific_context']['units']: failures.append('units')
        if uncertainty.get('sampling_law') != q['scientific_context']['sampling']['law']: failures.append('sampling_law')
        if uncertainty.get('assumptions') != [a['id'] for a in q['scientific_context']['assumptions']]: failures.append('assumptions')
    return failures


def prepare():
    from causalbank.operation_service_v12 import validate_request
    from statistics import NormalDist
    import funding_examples_20261013 as examples
    assert not DESIGN.exists(), 'Preserve frozen protocol'
    assert not (BASE / 'fixtures.json').exists(), 'Preserve frozen fixtures'
    cases = fixtures()
    for case in cases: validate_request(make_request(case, []))
    assert abs(NormalDist().inv_cdf(1-ALPHA/2)-2) < 1e-14
    assert examples.calculate() == json.loads((BASE / 'exact-examples.json').read_text())
    write(BASE / 'fixtures.json', {'kind': 'authored_fixed_funding_boundary_cases', 'seed': 26101308,
                                 'seed_role': 'Version identity only; no random draws', 'cases': cases})
    write(BASE / 'design-preflight.json', {'status': 'pass', 'issues': [], 'cases': len(cases),
          'schema_valid_declarations': len(cases), 'final_service_invocations': 0,
          'alpha': ALPHA, 'alpha_family_two_outcomes': 2*ALPHA, 'normal_critical_independent_reference': 2,
          'oracle': 'Analytic normal residual inequality and exact covariance/inclusion/economics calculations; no service estimator called.',
          'endpoint_tolerance': {'absolute': 1e-9, 'relative': 1e-10},
          'adversarial_artifacts': 'Request schemas valid; deliberately invalid artifact bodies reach worker validation only during registered execution.'})
    print(json.dumps({'prepared_cases': len(cases), 'prospective_invocations': 4*len(cases)+2, 'final_trial_executed': False}))


def run(max_new_attempts=None):
    import run_program as control
    from causalbank.artifacts_v12 import ArtifactStore, encode
    from causalbank.operation_contract_v12 import context_digest
    from causalbank.runtime_v12 import Runtime
    state = control.core.read(ROOT, control.core.STATE)
    g, merged, _ = control.combined(ROOT, state)
    key = 'IN.JOURNEY.LOCAL.funding'
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
    roots = {route: ROOT / '.runtime' / ('funding-journey-26101308-' + route) for route in ['library', 'cli']}
    if journal_path.exists():
        journal = json.loads(journal_path.read_text())
        assert journal['protocol_sha256'] == registration['sha256']
    else:
        assert all(not p.exists() for p in roots.values()), 'Fresh study requires unused operator roots'
        journal = {'started_at': now(), 'protocol_sha256': registration['sha256'], 'attempts': [],
                   'prepared_requests': {}, 'segments': [],
                   'code': ref(Path(__file__), 'Frozen funding boundary runner; adapted from preserved discovery pattern'), 'all_requests_retained': True}
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
        case = next(x for x in cases if x['id'] == 'syntax_dag')
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
              'limits': ['Twenty-nine authored funding cases and two changed-horizon checks; no empirical coverage qualification.',
                         'No raw-data nuisance fitting, verified identity/inclusion, live model or actual sibling consumer.',
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
