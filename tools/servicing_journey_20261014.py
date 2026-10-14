#!/usr/bin/env python3
"""Servicing interface conformance and exact reference replay, without new draws."""
import argparse
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

import discovery_journey_20261013 as shared

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
BASE = ROOT / 'docs/program/execution/2026-10-14/servicing-journey'
DESIGN = ROOT / 'docs/program/comprehensive-v14/work/IN.JOURNEY.DESIGN.servicing/workflow-protocol.json'
LOCAL = ROOT / 'docs/program/comprehensive-v14/work/IN.JOURNEY.LOCAL.servicing/local-results.json'
ref, write, now = shared.ref, shared.write, shared.now


def context():
    value = shared.context()
    value.update(
        target={'kind': 'fixed_policy_value', 'outcome': 'net_reward', 'treatment': 'assistance',
                'contrast': 'fixed-policy-versus-never-assist'},
        population={'definition': 'Generated eligible customers present before first servicing decision', 'unit': 'customer'},
        variables=[{'id': 'history', 'role': 'covariate', 'unit': 'finite_sufficient_history'},
                   {'id': 'assistance', 'role': 'action', 'unit': 'binary'},
                   {'id': 'retained', 'role': 'observation', 'unit': 'binary'},
                   {'id': 'net_reward', 'role': 'outcome', 'unit': 'utility'}],
        intervention={'kind': 'history_policy', 'value': 'Frozen observable history rule; never-assist comparator'},
        horizon={'value': 2, 'unit': 'decision_periods'}, units=['utility_per_original_customer'],
        sign_convention='policy-minus-never-assist',
        sampling={'law': 'independent_trajectories', 'unit': 'customer', 'fold_unit': 'whole_customer'},
        assumptions=[{'id': name, 'statement': statement, 'status': 'unverified', 'evidence': []}
                     for name, statement in [
                         ('sufficient_history', 'Recorded history suffices for sequential action exchangeability'),
                         ('retention', 'Conditional on history/action, dropout only hides subsequent records'),
                         ('support', 'Every policy-reachable action and retention cell has true positive support'),
                         ('selection', 'Policy and probability models are frozen on a separate training cohort'),
                         ('independence', 'Whole customer histories are independent; within-history dependence is retained'),
                         ('bounded_reward', 'The finite-table argument requires declared bounded rewards')]],
        graph={'kind': 'DAG', 'edges': []})
    for left, right in [('history', 'assistance'), ('history', 'net_reward'),
                        ('assistance', 'net_reward'), ('history', 'retained'), ('assistance', 'retained')]:
        value['graph']['edges'].append({'left_node': left, 'right_node': right,
            'left_mark': 'tail', 'right_mark': 'arrow', 'evidence_type': 'assumption',
            'evidence_refs': [], 'review_status': 'unverified'})
    return value


def fixtures():
    base = context()
    cases = []
    def add(key, operation, params, ctx, expected, artifact=None, mutation=None):
        cases.append({'id': key, 'operation': operation, 'parameters': params, 'context': ctx,
                      'artifact': artifact, 'mutation': mutation, 'expected': expected})
    ok = {'status': 'completed', 'disposition': 'computed', 'qualification': 'execution_only'}
    unsupported = {'status': 'completed', 'disposition': 'unsupported', 'qualification': 'none', 'result': None}
    refused = {**unsupported, 'disposition': 'refused'}
    add('capabilities', 'capabilities.describe', {}, None, {**ok, 'unimplemented': 'design.evaluate'})
    add('syntax_dag', 'graph.review', {'review_kind': 'syntax'}, base, {**ok, 'graph': base['graph']})
    hidden = deepcopy(base)
    hidden['variables'].append({'id': 'private_state', 'role': 'latent', 'unit': 'binary'})
    for right in ['assistance', 'net_reward']:
        hidden['graph']['edges'].append({**base['graph']['edges'][0], 'left_node': 'private_state', 'right_node': right})
    add('syntax_hidden_state', 'graph.review', {'review_kind': 'syntax'}, hidden, {**ok, 'graph': hidden['graph']})
    add('sequential_identification', 'identify.effect', {'method_id': 'sequential_g_formula'}, base, unsupported)
    add('single_backdoor_not_policy', 'identify.effect', {'method_id': 'backdoor'}, base, unsupported)
    for key, method, target in [
        ('fixed_policy_uninstalled', 'known-prefix-score', 'fixed_policy_value'),
        ('estimated_logger_uninstalled', 'estimated-prefix-score', 'fixed_policy_value'),
        ('selected_policy_uninstalled', 'independent-selected-policy', 'realized_trained_policy_value'),
        ('unknown_optimum_uninstalled', 'unrestricted-optimum', 'unknown_optimal_policy_value')]:
        ctx = deepcopy(base); ctx['target']['kind'] = target
        add(key, 'estimate.effect', {'engine_id': 'servicing-proposed', 'estimator_id': method}, ctx, unsupported)
    for key, assumption in [('private_confounding', 'sufficient_history'), ('informative_dropout', 'retention'),
                            ('zero_support', 'support'), ('evaluation_selection', 'selection'),
                            ('shared_calendar', 'independence'), ('unbounded_p4_reward', 'bounded_reward')]:
        ctx = deepcopy(base)
        next(a for a in ctx['assumptions'] if a['id'] == assumption)['status'] = 'contradicted'
        add(key, 'estimate.effect', {'engine_id': 'servicing-proposed', 'estimator_id': 'estimated-prefix-score'}, ctx, refused)
    valid = {'event_at': '2026-01-01T00:00:00+00:00', 'available_at': '2026-01-02T00:00:00+00:00',
             'decision_at': '2026-01-03T00:00:00+00:00'}
    rows = [valid, {**valid, 'available_at': valid['decision_at']},
            {k: v for k, v in valid.items() if k != 'available_at'},
            {**valid, 'event_at': '2026-01-04T00:00:00+00:00'}]
    def clock_artifact(data):
        return {'schema': 'observation-rows/1', 'role': 'observation_rows', 'body': {'rows': data}}
    add('clock_valid', 'audit.observation', {'checks': ['clock']}, base, {**ok, 'clock_failures': []}, clock_artifact([valid]))
    add('clock_leakage', 'audit.observation', {'checks': ['clock']}, base, {**ok, 'clock_failures': [1, 2, 3]}, clock_artifact(rows))
    add('truth_audit_uninstalled', 'audit.observation', {'checks': ['assignment_truth']}, base, unsupported)
    # These are supplied deterministic inequalities, never fitted policy intervals.
    for key, coeff, topology, intervals in [
        ('finite_value_range', [1, 0, -16], 'finite_interval', [[-4, 4]]),
        ('disconnected', [-1, 0, 1], 'unbounded_union', [[None, -1], [1, None]]),
        ('empty', [1, 0, 1], 'empty', []),
        ('whole_line', [-1, 0, -1], 'whole_line', [[None, None]])]:
        ctx = deepcopy(base); ctx['target']['kind'] = 'supplied_deterministic_utility_set'
        add(key, 'sensitivity.evaluate', {'family_id': 'quadratic-sublevel'}, ctx,
            {**ok, 'coordinate_sets': [{'topology': topology, 'intervals': intervals}], 'uncertainty_kind': 'sensitivity'},
            {'schema': 'quadratic-bounds/1', 'role': 'quadratic_bounds', 'body': {'quadratics': [coeff]}})
    for key, mutation, code in [('context_mismatch', 'change_sign_after_import', 'invalid_or_unavailable_input'),
                                ('corrupt_artifact', 'corrupt_after_import', 'input_integrity')]:
        add(key, 'audit.observation', {'checks': ['clock']}, base,
            {'status': 'failed', 'disposition': 'unavailable', 'qualification': 'none', 'result': None, 'error_code': code},
            clock_artifact([valid]), mutation)
    assert len(cases) == 24
    return cases


def make_request(case, refs, phase='initial'):
    request = shared.make_request(case, refs, phase)
    request['idempotency_key'] = 'servicing-journey-26101401-' + case['id']
    return request


def verdict(case, request, response):
    return shared.verdict(case, request, response)


def prepare():
    from causalbank.operation_service_v12 import validate_request
    assert not DESIGN.exists(), 'Preserve the frozen protocol'
    cases = fixtures()
    for case in cases:
        validate_request(make_request(case, []))
    write(BASE / 'fixtures.json', {'kind': 'authored_fixed_servicing_boundary_cases', 'cases': cases,
                                 'seed': 26101401, 'seed_role': 'version identity; no random draws'})
    write(BASE / 'design-preflight.json', {'status': 'pass', 'cases': len(cases), 'schema_valid_cases': len(cases),
        'final_service_invocations': 0,
        'independent_references': ['Exact two-period path sum and independent backward recursion from preserved servicing argument',
            'Equal observed laws but unequal intervention values and missing-outcome means',
            'Factored scalar inequalities and timezone-aware event<=available<decision',
            'Unavailable policy engines are not licensed by declaration or graph syntax']})
    print(json.dumps({'prepared': len(cases), 'prospective_calls': len(cases)*4+2, 'runtime_trial_executed': False}))


def reproduce_references():
    import servicing_observed_examples_20261013 as exact
    from fractions import Fraction
    original = ROOT / 'docs/program/execution/2026-10-13/servicing/exact-results.json'
    result = exact.calculate()
    assert result == json.loads(original.read_text()), 'Preserved exact calculation differs'
    values = {row['policy']: Fraction(row['true']['truth']) for row in result['policies']}
    contrast = values['all'] - values['none']
    assert contrast == Fraction(5, 8)
    gross = contrast * 1000 * 100
    output = BASE / 'exact-reproduction.json'
    write(output, {'status': 'pass', 'random_draws': 0, 'reference_not_runtime_service': True,
        'original': ref(original, 'Exact values, hidden-state/dropout counterexamples and width obstruction'),
        'result': result,
        'financial_scenario': {'assumed_cohort': 1000, 'assumed_USD_per_utility': 100,
            'all_minus_none_utility_per_customer': float(contrast), 'incremental_reward_USD': float(gross),
            'assumed_additional_full_workflow_cost_USD': 10000, 'scenario_net_USD': float(gross - 10000),
            'boundary': 'Stipulated generated-law utility mapping; rewards already deduct assistance cost; no bank ROI or confidence interval'}})
    return ref(output, 'Exact existing examples independently replayed; no new sampling study')


def run(max_new_attempts=None):
    import run_program as control
    from causalbank.artifacts_v12 import ArtifactStore, encode
    from causalbank.operation_contract_v12 import context_digest
    from causalbank.runtime_v12 import Runtime
    state = control.core.read(ROOT, control.core.STATE)
    g, merged, _ = control.combined(ROOT, state)
    key = 'IN.JOURNEY.LOCAL.servicing'
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
    roots = {route: ROOT / '.runtime' / ('servicing-journey-26101401-' + route) for route in ['library', 'cli']}
    if journal_path.exists():
        journal = json.loads(journal_path.read_text())
        assert journal['protocol_sha256'] == registration['sha256']
    else:
        assert all(not p.exists() for p in roots.values()), 'Fresh study requires unused operator roots'
        journal = {'started_at': now(), 'protocol_sha256': registration['sha256'], 'attempts': [],
                   'prepared_requests': {}, 'segments': [],
                   'code': ref(Path(__file__), 'Frozen servicing boundary runner'), 'all_requests_retained': True}
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
                    if case['mutation'] == 'change_sign_after_import':
                        q['scientific_context']['sign_convention'] = 'never-assist-minus-policy'
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
        q = make_request(case, [], 'drift');q['scientific_context']['horizon']['value'] = 3
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
    reference_started = time.monotonic()
    reference = reproduce_references()
    reference_wall_seconds = time.monotonic() - reference_started
    count = len(cases)*4+2
    assert len(journal['attempts']) == count
    passed = all(x['passed'] for x in journal['attempts']) and all(x['all_four_semantically_equal'] for x in parity)
    result = {'operation': key, 'status': 'pass' if passed else 'negative', 'all_request_count': count,
              'passed_request_count': sum(x['passed'] for x in journal['attempts']),
              'failed_requests': [x['id'] for x in journal['attempts'] if not x['passed']],
              'parity': parity, 'exact_reference': reference, 'exact_reference_wall_seconds': reference_wall_seconds,
              'retained_failures': True, 'started_at': journal['started_at'],
              'finished_at': journal['completed_at'], 'protocol_sha256': registration['sha256'],
              'journal': ref(journal_path, 'Every input, response, failure and measured duration'),
              'full_invocation_wall_seconds': sum(x['wall_seconds'] for x in journal['attempts']),
              'active_runner_wall_seconds': sum(x['segment_wall_seconds'] for x in journal['segments']),
              'child_peak_rss_kib_aggregate': max(x['child_peak_rss_kib'] for x in journal['segments']),
              'parent_peak_rss_kib_aggregate': max(x['parent_peak_rss_kib'] for x in journal['segments']),
              'segment_count': len(journal['segments']),
              'resource_scope': 'Invocation wall includes worker/process startup and failed/replayed calls; runner wall includes fixture import and journaling, excludes time between segments and initial Python/module startup. RSS is a process high-water maximum, not concurrent tree memory. No bank cost estimate.',
              'limits': ['Twenty-four authored cases and two changed-target checks; no random-sampling qualification.',
                         'No installed servicing policy estimator, general hidden-state identification, live model or actual sibling consumer.',
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
