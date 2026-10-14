#!/usr/bin/env python3
"""Review all registered observation outcomes and independent exact references."""
from collections import Counter
from datetime import datetime
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path

import observations_examples_20261013 as examples
import observations_journey_20261013 as journey
import run_program as control

ROOT, BASE = journey.ROOT, journey.BASE
ref, write = journey.ref, journey.write


def main():
    assert not (BASE / 'local-review.json').exists(), 'Preserve completed review'
    state = control.core.read(ROOT, control.core.STATE)
    graph, merged, _ = control.combined(ROOT, state)
    key = 'IN.JOURNEY.LOCAL.observations'
    node = control.ledger.operation(graph, key)
    registration = merged['execution_program']['registrations'][key]
    control.ledger.validate_protocol(ROOT, merged, node, registration)
    result = json.loads(journey.LOCAL.read_text())
    journal = json.loads((BASE / 'local-journal.json').read_text())
    cases = {c['id']: c for c in json.loads((BASE / 'fixtures.json').read_text())['cases']}
    assert result['journal']['sha256'] == ref(BASE / 'local-journal.json', '')['sha256']
    assert result['protocol_sha256'] == journal['protocol_sha256'] == registration['sha256']
    assert len(journal['attempts']) == len({a['id'] for a in journal['attempts']}) == 106
    assert result['all_request_count'] == 106 and len(result['parity']) == 26
    assert datetime.fromisoformat(journal['started_at']) > datetime.fromisoformat(registration['registered_at'])
    from causalbank.artifacts_v12 import encode
    for segment in journal['segments']:
        n = segment['prior_request_count']
        assert segment['prior_attempts_sha256'] == hashlib.sha256(encode(journal['attempts'][:n])).hexdigest()
    numerical_checks = 0
    for attempt in journal['attempts']:
        if attempt['case'] == 'idempotency_drift':
            assert attempt['response']['status'] == 'rejected'
            assert attempt['response']['error']['code'] == 'idempotency_conflict'
            old = journal['prepared_requests']['clock_valid:' + attempt['route']]
            new = json.loads(json.dumps(attempt['request']))
            new['request_id'] = old['request_id']; new['scientific_context']['horizon']['value'] = 12
            assert new == old
            continue
        case = cases[attempt['case']]
        assert journey.verdict(case, attempt['request'], attempt['response']) == attempt['failures']
        if attempt['route'] != 'library' or attempt['phase'] != 'initial':
            continue
        response = attempt['response']; value = response.get('result') or {}
        if response['disposition'] != 'computed' or value.get('kind') != 'effect':
            continue
        body = case['artifact']['body']
        intervals = value['coordinate_sets'][0]['intervals']
        for x in [F(i, 100) for i in range(-120, 121)]:
            if case['operation'] == 'sensitivity.evaluate':
                a, b, c = map(F, body['quadratics'][0])
                inside = a*x*x + b*x + c <= 0
            else:
                y, d = [F(str(v)) for v in body['mean']]
                cov = [[F(str(v)) for v in row] for row in body['lrv']]
                inside = body['n']*(y-x*d)**2 <= 4*(cov[0][0]-2*x*cov[0][1]+x*x*cov[1][1])
            actual = any((lo is None or float(x) >= lo-1e-9) and
                         (hi is None or float(x) <= hi+1e-9) for lo, hi in intervals)
            assert inside == actual, (case['id'], str(x))
            numerical_checks += 1
    assert examples.calculate() == json.loads((BASE / 'exact-examples.json').read_text())
    counts = Counter((a['response'].get('status'), a['response'].get('disposition')) for a in journal['attempts'])
    assert math.isclose(result['full_invocation_wall_seconds'], sum(a['wall_seconds'] for a in journal['attempts']))
    passed = all(a['passed'] for a in journal['attempts']) and all(p['all_four_semantically_equal'] for p in result['parity'])
    assert result['status'] == ('pass' if passed else 'negative')
    findings = [
        'The complete denominator and resume prefixes are retained. Correct unsupported/refused results are boundary passes, not available estimates.',
        'Clock-only diagnostics admit empty rows and valid-time duplicate/false-label data; their explicit boundary withholds identity, inclusion and truth qualification.',
        'The clock operation still computes diagnostics with contradicted identity; estimation refuses the explicit contradiction and otherwise remains conditional on unverified measurement.',
        'Artifact content/custody and context drift are rejected under the local contract. Matching hashes establish byte identity, not truthful provenance.',
        'Follow-up outcomes presented as features fail the feature clock; alternate outcome ascertainment is not implemented by this operation.',
        'Supplied-covariance and generic sensitivity outputs preserve topology and qualifications. Physical prevalence restrictions, automatic audit gating and raw-data correction remain proposed.',
        'Exact finite-law and label examples are generated constructions; prevention efficacy and prices are stipulated, not bank evidence.']
    evidence = [ref(BASE / n, 'Reviewed observation execution or design evidence') for n in
                ['local-journal.json', 'fixtures.json', 'plan-review.md', 'exact-examples.json', 'design-preflight.json', 'argument-review.json', 'registration-control.json']]
    evidence += [ref(journey.LOCAL, 'All 106 fixed invocation outcomes'), ref(journey.DESIGN, 'Prospectively registered protocol'),
                 ref(Path(__file__), 'Independent rational membership and full-denominator review')]
    review = {'status': 'pass' if passed else 'negative', 'issues': result['failed_requests'],
              'reviewer': {'name': 'Codex author/coordinator', 'kind': 'author'},
              'scope': 'Registered fixed local conformance screen; no trustworthy-observation product qualification',
              'request_slots': 106, 'matching_slots': result['passed_request_count'], 'parity_cases': 26,
              'independent_rational_membership_checks': numerical_checks,
              'dispositions': [{'status': k[0], 'disposition': k[1], 'count': v} for k, v in sorted(counts.items())],
              'preserved_resume_prefix_counts': [s['prior_request_count'] for s in journal['segments']],
              'findings': findings, 'evidence': evidence,
              'timing': {k: result[k] for k in ['full_invocation_wall_seconds', 'active_runner_wall_seconds',
                        'parent_peak_rss_kib_aggregate', 'child_peak_rss_kib_aggregate', 'segment_count', 'resource_scope']},
              'truth_or_causal_qualification': False, 'independent_review': False, 'sibling_execution': False}
    write(BASE / 'local-review.json', review)
    receipt = control.ledger.receipt_template(node)
    receipt.update(outcome=review['status'], execution='performed', scope=review['scope'],
        reviewer=review['reviewer'], limitations=result['limits'] + ['Automatic audit-to-estimator gating and raw-data observation correction are not implemented.'],
        outputs=[ref(journey.LOCAL, 'Actual registered observation boundary outcomes')],
        protocol_sha256=registration['sha256'], all_request_denominator=106,
        fresh_data_identity='Generated fixed version 26101309 and two fresh isolated operator roots',
        retained_failures=True, started_at=journal['started_at'], journal=ref(BASE / 'local-journal.json', 'Complete 106-slot execution journal'))
    for i, finding in enumerate([
        'Available clock/artifact/moment/sensitivity operations and explicit unsupported requests were executed against immutable generated fixtures; unavailable truth, fitting and sibling capabilities are unclaimed.',
        'Every request, context hash, result topology, qualifier, refusal, CLI exit and restart response remains in the denominator and passed the frozen references.' if passed else 'Mismatches remain explicit in the full journal and no complete conformance claim is made.']):
        receipt['criteria'][i].update(verdict=review['status'], finding=finding,
                                      evidence=[ref(BASE / 'local-review.json', 'Full author review'), ref(journey.LOCAL, 'Actual outcomes')])
    write(BASE / 'local-receipt.json', receipt)
    print(json.dumps({'status': review['status'], 'requests': 106, 'matches': result['passed_request_count'],
                      'rational_checks': numerical_checks, 'dispositions': review['dispositions']}))


if __name__ == '__main__':
    main()
