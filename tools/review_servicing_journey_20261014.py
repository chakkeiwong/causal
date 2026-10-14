#!/usr/bin/env python3
"""Review the full fixed servicing suite; preserve the frozen expectation error."""
from collections import Counter
from datetime import datetime
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path

import run_program as control
import servicing_journey_20261014 as journey
from causalbank.artifacts_v12 import encode


def main():
    root, base = journey.ROOT, journey.BASE
    ref, write = journey.ref, journey.write
    assert not (base / 'local-review.json').exists(), 'Preserve reviewed evidence'
    graph, merged, _ = control.combined(root, control.core.read(root, control.core.STATE))
    node = control.ledger.operation(graph, 'IN.JOURNEY.LOCAL.servicing')
    registration = merged['execution_program']['registrations'][node['id']]
    control.ledger.validate_protocol(root, merged, node, registration)
    result = json.loads(journey.LOCAL.read_text())
    journal = json.loads((base / 'local-journal.json').read_text())
    cases = {c['id']: c for c in json.loads((base / 'fixtures.json').read_text())['cases']}
    assert result['journal']['sha256'] == ref(base / 'local-journal.json', '')['sha256']
    assert registration['sha256'] == result['protocol_sha256'] == journal['protocol_sha256']
    assert datetime.fromisoformat(journal['started_at']) > datetime.fromisoformat(registration['registered_at'])
    attempts = journal['attempts']
    assert len(attempts) == len({a['id'] for a in attempts}) == result['all_request_count'] == 98
    assert len(result['parity']) == 24 and all(p['all_four_semantically_equal'] for p in result['parity'])
    for segment in journal['segments']:
        n = segment['prior_request_count']
        assert segment['prior_attempts_sha256'] == hashlib.sha256(encode(attempts[:n])).hexdigest()
    rational_checks = 0
    for a in attempts:
        if a['case'] == 'idempotency_drift':
            assert a['response']['status'] == 'rejected' and a['response']['error']['code'] == 'idempotency_conflict'
            old = journal['prepared_requests']['syntax_dag:' + a['route']]
            new = json.loads(json.dumps(a['request']))
            new['request_id'] = old['request_id']; new['scientific_context']['horizon']['value'] = 2
            assert new == old
            continue
        case = cases[a['case']]
        assert journey.verdict(case, a['request'], a['response']) == a['failures']
        if not a['passed']:
            assert a['case'] == 'corrupt_artifact' and a['failures'] == ['error_code']
            r = a['response']
            assert r['error']['code'] == 'artifact_access' and r['result'] is None
            assert r['status'] == 'failed' and r['qualification']['level'] == 'none'
        if a['route'] == 'library' and a['phase'] == 'initial' and a['request']['operation'] == 'sensitivity.evaluate':
            coeff = list(map(F, case['artifact']['body']['quadratics'][0]))
            intervals = a['response']['result']['coordinate_sets'][0]['intervals']
            for x in [F(i, 20) for i in range(-120, 121)]:
                expected = coeff[0]*x*x + coeff[1]*x + coeff[2] <= 0
                actual = any((lo is None or x >= F(lo)) and (hi is None or x <= F(hi)) for lo, hi in intervals)
                assert expected == actual
                rational_checks += 1
    assert result['status'] == 'negative' and result['passed_request_count'] == 94
    assert len(result['failed_requests']) == 4 and rational_checks == 964
    assert math.isclose(sum(a['wall_seconds'] for a in attempts), result['full_invocation_wall_seconds'])
    control.core.bound(root, result['exact_reference'])
    reference = json.loads((base / 'exact-reproduction.json').read_text())
    assert reference['status'] == 'pass' and reference['result'] == json.loads(
        (root / 'docs/program/execution/2026-10-13/servicing/exact-results.json').read_text())
    correction = {'kind': 'post_run_expectation_diagnosis_not_requalification',
        'case': 'corrupt_artifact', 'registered_expected': 'input_integrity', 'correct_source_contract': 'artifact_access',
        'observed_slots': 4, 'runtime_edit_needed': False, 'frozen_result_remains': 'negative',
        'reason': 'Runtime.invoke catches a failed input byte verification and returns artifact_access before worker dispatch and replay.',
        'future_expectation': {'status': 'failed', 'disposition': 'unavailable', 'qualification': 'none', 'result': None, 'error_code': 'artifact_access'},
        'evidence': [ref(root / 'src/causalbank/runtime_v12.py', 'Runtime.invoke lines 86-90: declared byte verification and artifact_access'),
                     ref(base / 'local-journal.json', 'Four unchanged failures; no numeric result or qualification')],
        'next_action': 'Use artifact_access in any future servicing boundary suite; preserve this result. No runtime repair or full rerun is warranted for the error-name expectation.'}
    write(base / 'expectation-correction.json', correction)
    counts = Counter((a['response']['status'], a['response']['disposition']) for a in attempts)
    review = {'status': 'negative', 'reviewer': {'name': 'Codex author/coordinator', 'kind': 'author'},
        'scope': 'Completed registered servicing interface screen and separate exact reference; one frozen expectation error',
        'requests': 98, 'matched_frozen_expectations': 94, 'failed_slots': result['failed_requests'],
        'parity_cases_passed': 24, 'independent_rational_membership_checks': rational_checks,
        'dispositions': [{'status': k[0], 'disposition': k[1], 'count': v} for k, v in sorted(counts.items())],
        'findings': ['All slots retained; no calls or outcomes changed after registration.',
            'Corrupt bytes were rejected correctly. Error-name mismatch belongs to the authored expectation, not an observed integrity breach.',
            'Unavailable policy estimators and explicitly contradicted assumptions produced no numeric policy values.',
            'All four routes/restarts preserve result meaning; changed horizon under the same key is rejected.',
            'Exact reference reproduced. The conservative interval, hidden-state and informative-dropout obstructions are unchanged.',
            'Generated financial scenario and local timings are not bank ROI, vendor results or accepted consumer execution.'],
        'correction': ref(base / 'expectation-correction.json', 'Source-grounded correction, preserving negative trial'),
        'evidence': [ref(journey.DESIGN, 'Prospective design'), ref(journey.LOCAL, 'Complete result'),
            ref(base / 'local-journal.json', 'Full 98-slot denominator'), result['exact_reference'],
            ref(Path(__file__), 'Author review and independent rational grid')],
        'independent_review': False, 'original_gap_qualification': False}
    write(base / 'local-review.json', review)
    receipt = control.ledger.receipt_template(node)
    receipt.update(outcome='negative', execution='performed', scope=review['scope'], reviewer=review['reviewer'],
        limitations=result['limits'] + ['Four error-code expectation mismatches remain in the registered negative result.'],
        outputs=[ref(journey.LOCAL, 'Actual local outcomes including expectation error')],
        protocol_sha256=registration['sha256'], all_request_denominator=98,
        fresh_data_identity='Authored suite 26101401, two fresh operator roots; exact prior examples openly replayed',
        retained_failures=True, started_at=journal['started_at'], journal=ref(base / 'local-journal.json', 'All 98 slots'))
    for i, verdict, finding in [
        (0, 'pass', 'Only available local operations and explicit unsupported policy requests were executed; no unavailable policy, adapter or consumer capability is claimed.'),
        (1, 'negative', 'Topology, clocks, refusal, context and replay agree; 94/98 frozen checks pass. Four corrupt-artifact calls use artifact_access instead of the incorrectly frozen input_integrity expectation. Negative result preserved.')]:
        receipt['criteria'][i].update(verdict=verdict, finding=finding,
            evidence=[ref(base / 'local-review.json', 'Full reviewed outcome'), ref(base / 'expectation-correction.json', 'Exact discrepancy and disposition')])
    write(base / 'local-receipt.json', receipt)
    print(json.dumps({'outcome': 'negative', 'requests': 98, 'matching': 94, 'parity': 24,
                      'rational_checks': rational_checks, 'runtime_integrity_breach': False, 'dispositions': review['dispositions']}))


if __name__ == '__main__':
    main()
