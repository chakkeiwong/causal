#!/usr/bin/env python3
"""Exact authored reference models; no runtime, protocol peer or signer is invoked."""
from copy import deepcopy
from fractions import Fraction
import hashlib
from itertools import permutations, product
import json


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True,
        separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def prefix_reference():
    frozen = ('a', 'b', 'c')
    rows = []
    for k in range(4):
        for completed in permutations(frozen, k):
            rows.append({'completed': list(completed),
                'is_prefix': completed == frozen[:k]})
    assert len(rows) == 16 and sum(r['is_prefix'] for r in rows) == 4
    # The ordinary final critical section holds the job lock over P and T.
    # A cancel cannot interleave there unless a crash releases the lock.
    schedules = []
    for position in [0, 1, 2, 3, 5]:
        done = position == 5
        schedules.append({'cancel_after_events': position,
            'events': ['C1', 'C2', 'C3', 'P', 'T'][:position],
            'terminal': 'completed' if done else 'cancelled',
            'published_artifact': done,
            'completed_prefix_length': min(position, 3)})
    crash = {'events': ['C1', 'C2', 'C3', 'P', 'crash', 'cancel'],
        'terminal': 'cancelled', 'published_artifact': True,
        'lesson': 'Cancellation cannot erase an artifact published before the crash.'}
    publication = [
        {'bytes': False, 'descriptor': False, 'terminal_ack': False,
         'proposal': 'Recompute only uncommitted work under the original identity and budget.'},
        {'bytes': True, 'descriptor': False, 'terminal_ack': False,
         'proposal': 'Verify identical deterministic bytes before repairing the descriptor.'},
        {'bytes': True, 'descriptor': True, 'terminal_ack': False,
         'proposal': 'Verify input, report and state identity before acknowledgement; terminal cancellation wins.'},
        {'bytes': True, 'descriptor': True, 'terminal_ack': True,
         'proposal': 'Verify the referenced artifact; preserve terminal state.'},
        {'bytes': False, 'descriptor': True, 'terminal_ack': False,
         'proposal': 'Refuse unavailable/corrupt state; retain evidence for operator reconciliation.'}]
    return {'kind': 'authored_finite_reference_not_runtime_execution',
        'prefix_rows': rows, 'valid_prefixes': 4, 'rejected_nonprefixes': 12,
        'lock_respecting_cancel_schedules': schedules,
        'crash_between_publication_and_acknowledgement': crash,
        'proposed_publication_decisions': publication}


def deadline_reference():
    created, budget = 1000, 60
    rows = []
    for elapsed, adjustment in [(50, 0), (80, -90)]:
        wall_now = created + elapsed + adjustment
        rows.append({'real_elapsed_seconds': elapsed, 'wall_adjustment_seconds': adjustment,
            'wall_now': wall_now, 'formula_remaining_seconds': created + budget - wall_now,
            'elapsed_budget_remaining_seconds': max(0, budget - elapsed)})
    assert [r['formula_remaining_seconds'] for r in rows] == [10, 70]
    return {'kind': 'exact_formula_counterexample_not_observed_host_clock_failure',
        'created': created, 'budget_seconds': budget, 'rows': rows,
        'scope': 'Within-process monotonic elapsed time and a trusted persisted cross-restart deadline need separate designs; no portable reboot-safe clock is supplied.'}


def semantic_reference():
    # A minimal authored target map, deliberately not a complete product request.
    target = {'schema': 'illustrative-target/1', 'population': 'eligible accounts',
        'unit': 'account', 'effect_unit': 'USD', 'horizon_days': 30,
        'sampling_law': 'independent_accounts', 'sign': 'offer_minus_no_offer'}
    changed = []
    for key, value in [('effect_unit', 'thousand_USD'), ('horizon_days', 90),
            ('sampling_law', 'shared_calendar_shocks'), ('sign', 'no_offer_minus_offer')]:
        other = deepcopy(target)
        other[key] = value
        changed.append({'changed_field': key, 'schema_equal': other['schema'] == target['schema'],
            'target_hash_equal': digest(other) == digest(target), 'new_target': other})
    gross = (Fraction(-2), Fraction(6))
    cost, accounts = Fraction(3), 1000
    net = [int(accounts * (x - cost)) for x in gross]
    # USD to thousand USD is meaningful only when BOTH effect and cost convert.
    converted = [accounts * (x / 1000 - cost / 1000) * 1000 for x in gross]
    assert net == [-5000, 3000] and converted == net
    assert all(r['schema_equal'] and not r['target_hash_equal'] for r in changed)
    return {'kind': 'authored_target_identity_and_set_arithmetic', 'target': target,
        'target_sha256': digest(target), 'same_schema_changed_meaning': changed,
        'gross_effect_USD_per_account': [-2, 6], 'cost_USD_per_account': 3,
        'accounts': accounts, 'net_value_USD': net,
        'unit_conversion_with_cost_preserved_USD': [int(x) for x in converted],
        'limitation': 'No data fit, coverage claim or full request-schema validation.'}


def negotiation_reference():
    def choose(event, mutual_modern=True, dual=True):
        if event == 'discover_result':
            return 'modern' if mutual_modern else 'incompatible'
        if event == 'unsupported_protocol_version':
            return 'retry_supported_modern' if mutual_modern else 'incompatible'
        if event == 'other_recognized_modern_error':
            return 'remain_modern_handle_error_without_unconditional_retry'
        return 'legacy_initialize' if dual else 'incompatible'
    cases = [('discover_result', True, True), ('discover_result', False, True),
        ('unsupported_protocol_version', True, True), ('unsupported_protocol_version', False, True),
        ('other_recognized_modern_error', None, True),
        ('other_error_-32601', True, True), ('other_error_-32602', True, True),
        ('probe_timeout', True, True), ('other_error_-32601', True, False)]
    rows = [{'probe_category': e, 'mutual_modern_version': m, 'dual_era_client': d,
        'proposed_action': choose(e, m, d)} for e, m, d in cases]
    assert len(rows) == 9
    assert all(r['proposed_action'] != 'legacy_initialize' for r in rows
        if r['probe_category'] in {'unsupported_protocol_version', 'other_recognized_modern_error'})
    return {'kind': 'authored_decision_table_not_wire_parser_or_client_server_test',
        'rows': rows, 'required_precondition': 'A real implementation must validate discovery/error shapes, version lists and applicable pinned specification before assigning a category.'}


def adoption_reference():
    gates = ['scientific_review', 'data_authority', 'consumer_acceptance',
             'platform_acceptance', 'economic_case', 'sponsor_decision']
    table = []
    for values in product([False, True], repeat=len(gates)):
        table.append({'gates': dict(zip(gates, values)),
            'eligible_for_scoped_adoption': all(values)})
    assert len(table) == 64 and sum(x['eligible_for_scoped_adoption'] for x in table) == 1
    release = {'reader': 'illustrative-reader-A', 'core': 'illustrative-core-A',
        'adapter': 'illustrative-adapter-A', 'consumer': 'illustrative-consumer-A',
        'scientific_context': 'illustrative-context-A', 'platform': 'illustrative-platform-A'}
    stale = []
    for field in release:
        changed = dict(release)
        changed[field] += '-changed'
        stale.append({'changed_field': field, 'exact_release_match': changed == release,
            'action': 'Impact review; bind a successor receipt or explicitly carry unaffected evidence.'})
    missing = {'current_external_receipts': 0, 'eligible_for_scoped_adoption': False,
        'authenticated_owners': [], 'fabricated_signatures': 0}
    return {'kind': 'authored_boolean_contract_not_authentication_implementation',
        'gate_rows': table, 'exact_release_staleness_cases': stale,
        'current_evidence': missing,
        'limitation': 'True inputs assume authentic scoped owner receipts, scientific and business acceptance, and resolved conditions; local truth-table values supply none.'}


def calculate():
    return {'prefix_publication_cancellation': prefix_reference(),
        'deadline': deadline_reference(), 'scientific_meaning': semantic_reference(),
        'protocol_negotiation': negotiation_reference(), 'adoption': adoption_reference()}


if __name__ == '__main__':
    print(json.dumps(calculate(), indent=2, allow_nan=False))
