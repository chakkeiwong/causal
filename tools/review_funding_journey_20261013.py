#!/usr/bin/env python3
"""Author review of actual funding results with separate analytic references."""
from collections import Counter
from datetime import datetime
from decimal import Decimal, localcontext
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path

import funding_journey_20261013 as journey
import funding_examples_20261013 as examples
import run_program as control

ROOT, BASE = journey.ROOT, journey.BASE
ref, write = journey.ref, journey.write


def main():
    assert not (BASE / 'local-review.json').exists(), 'Preserve reviewed results'
    state = control.core.read(ROOT, control.core.STATE)
    graph, merged, _ = control.combined(ROOT, state)
    key = 'IN.JOURNEY.LOCAL.funding'
    node = control.ledger.operation(graph, key)
    registration = merged['execution_program']['registrations'][key]
    control.ledger.validate_protocol(ROOT, merged, node, registration)
    result = json.loads(journey.LOCAL.read_text())
    journal = json.loads((BASE / 'local-journal.json').read_text())
    fixtures = json.loads((BASE / 'fixtures.json').read_text())['cases']
    assert result['journal']['sha256'] == ref(BASE / 'local-journal.json', '')['sha256']
    assert result['protocol_sha256'] == journal['protocol_sha256'] == registration['sha256']
    assert len(journal['attempts']) == len(set(a['id'] for a in journal['attempts'])) == 118
    assert result['all_request_count'] == result['passed_request_count'] == 118 and result['status'] == 'pass'
    assert all(p['all_four_semantically_equal'] for p in result['parity']) and len(result['parity']) == 29
    assert datetime.fromisoformat(journal['started_at']) > datetime.fromisoformat(registration['registered_at'])
    prior = json.loads((BASE / 'pre-completion-amendment-journal.json').read_text())
    assert prior['attempts'] == journal['attempts'][:116]
    empty = json.loads((BASE / 'pre-amendment-journal.json').read_text())
    assert empty['attempts'] == [] and empty['prepared_requests'] == {}
    for name, before_count in [('launch-amendment.json', 0), ('completion-amendment.json', 116)]:
        note = json.loads((BASE / name).read_text())
        assert note['service_calls_before_amendment'] == before_count
        assert not note['fixtures_or_expectations_changed']
        assert any(x['path'] == str((BASE / name).relative_to(ROOT)) and x['sha256'] == ref(BASE / name, '')['sha256']
                   for x in state['execution_program']['progress'][key])
        assert datetime.fromisoformat(note['recorded_at']) < datetime.fromisoformat(journal['attempts'][before_count]['recorded_at'])
        for evidence in note['evidence']: control.core.bound(ROOT, evidence)
    original = (ROOT / 'tools/funding_journey_20261013.py').read_text()
    repaired = (ROOT / 'tools/funding_journey_successor_20261013.py').read_text()
    assert repaired == original.replace('import argparse\n', 'import argparse\nimport hashlib\n', 1).replace(
        "x['id'] == 'syntax_dag'", "x['id'] == 'strong_fixed_denominator'", 1)
    from causalbank.artifacts_v12 import encode
    for segment in journal['segments']:
        n = segment['prior_request_count']
        assert segment['prior_attempts_sha256'] == hashlib.sha256(encode(journal['attempts'][:n])).hexdigest()
    cases = {c['id']: c for c in fixtures}
    for a in journal['attempts']:
        assert a['passed'] and a['failures'] == []
        if a['case'] != 'idempotency_drift':
            assert journey.verdict(cases[a['case']], a['request'], a['response']) == []
        else:
            assert a['response']['status'] == 'rejected' and a['response']['error']['code'] == 'idempotency_conflict'
            old = journal['prepared_requests']['strong_fixed_denominator:'+a['route']]
            new = json.loads(json.dumps(a['request']))
            new['request_id'] = old['request_id']; new['scientific_context']['horizon']['value'] = 12
            assert new == old
    # Independent numerical roots use Decimal and the hand-derived polynomial,
    # without importing the service's moment or quadratic solver.
    with localcontext() as ctx:
        ctx.prec = 60
        sqrt31 = Decimal(31).sqrt()
        roots = [(Decimal(25)-sqrt31)/12, (Decimal(25)+sqrt31)/12]
        for x in roots:
            assert abs(96*x*x-400*x+396) < Decimal('1e-50')
    selected = {a['case']: a for a in journal['attempts'] if a['route'] == 'library' and a['phase'] == 'initial'}
    endpoints = selected['random_denominator']['response']['result']['coordinate_sets'][0]['intervals'][0]
    assert all(abs(float(r)-e) < 1e-12 for r, e in zip(roots, endpoints))
    # Direct residual inequalities on a fixed rational grid check all eight
    # initial inversion cases plus the two exposed identity/inclusion contexts.
    membership_checks = 0
    for name, a in selected.items():
        r = a['response']; val = r.get('result') or {}
        if a['request']['operation'] != 'estimate.effect' or r['disposition'] != 'computed': continue
        body = cases[name]['artifact']['body']
        means = [F(str(x)) for x in body['mean']]
        cov = [[F(str(x)) for x in row] for row in body['lrv']]
        for index, item in enumerate(val['coordinate_sets']):
            for beta in [F(k, 4) for k in range(-20, 21)]:
                score = body['n'] * (means[index]-beta*means[-1])**2
                variance = cov[index][index]-2*beta*cov[index][-1]+beta**2*cov[-1][-1]
                intended = score <= 4*variance
                in_result = any((lo is None or float(beta) >= lo-1e-9) and (hi is None or float(beta) <= hi+1e-9)
                                for lo, hi in item['intervals'])
                assert intended == in_result, (name, index, beta)
                membership_checks += 1
    exact = examples.calculate()
    assert exact == json.loads((BASE / 'exact-examples.json').read_text())
    # Separate expression/order review of the covariance and finite population:
    assert sum(F(x)**2 * v for x, v in zip([1, 2], [F(1), F(2)])) == 9
    assert (F(1)+2*F(7, 3)+F(3))/4 == F(13, 6)
    assert (F(1, 2)+F(5, 2)+F(7, 2)+F(11, 2))/4 == 3
    alpha = math.erfc(math.sqrt(2))
    assert abs((1-alpha)-.9544997361036416) < 1e-14
    counts = Counter((a['response']['status'], a['response']['disposition']) for a in journal['attempts'])
    assert dict(counts) == {('completed', 'computed'): 48, ('failed', 'unavailable'): 40,
                            ('completed', 'refused'): 8, ('completed', 'unsupported'): 20, ('rejected', 'unavailable'): 2}
    assert math.isclose(sum(a['wall_seconds'] for a in journal['attempts']), result['full_invocation_wall_seconds'])
    sources = [ref(BASE / name, anchor) for name, anchor in [
        ('local-journal.json', 'All 118 exact requests, responses, outcomes and measured invocation durations'),
        ('fixtures.json', '29 fixed cases and unchanged expected results'),
        ('plan-review.md', 'Independent residual derivations, complete decision chain and cost scope'),
        ('exact-examples.json', 'Exact generated nuisance, identity/inclusion and profit results'),
        ('launch-failure.json', 'First harness failure before any service calls'),
        ('launch-amendment.json', 'First prospective administrative repair'),
        ('completion-failure.json', 'Second harness failure after 116 completed requests'),
        ('completion-amendment.json', 'Reviewed repair before the remaining two checks'),
        ('runner-repair.diff', 'Exact preserved original versus successor diff')]]
    sources += [ref(journey.LOCAL, 'Final amended fixed-screen result'), ref(journey.DESIGN, 'Initial prospective registered protocol'),
                ref(ROOT / 'tools/funding_journey_successor_20261013.py', 'Amended completion executable'),
                ref(Path(__file__), 'Author review with independent Decimal roots and rational membership checks')]
    review = {'status': 'pass', 'issues': [], 'reviewer': {'name': 'Codex author', 'kind': 'author'},
        'scope': 'Amended deterministic funding conformance screen; two failed harness launches retained',
        'request_slots': 118, 'matching_slots': 118, 'parity_cases': 29,
        'dispositions': [{'status': k[0], 'disposition': k[1], 'count': v} for k, v in sorted(counts.items())],
        'independent_reference_checks': membership_checks,
        'original_unamended_harness_completed': False, 'administrative_amendments': 2, 'failed_harness_launches': 2,
        'unmodified_result_prefix': 116, 'full_invocation_wall_seconds': result['full_invocation_wall_seconds'],
        'active_runner_wall_seconds': result['active_runner_wall_seconds'], 'timing_limits': [
            'Failed import launch startup duration was not measured; no complete end-to-end author workflow time is claimed.',
            'Active segment timers exclude gaps, initial Python/module startup and repair/review/manuscript work.',
            'Parent and child RSS high-water values are not simultaneous tree memory.'],
        'findings': ['Computed intervals remain conditional on externally supplied covariance and causal premises.',
                     'Unknown identity/inclusion does not force an automatic refusal; contradicted premises do.',
                     'All invalid inputs, unsupported methods, clock failures and changed-context conflicts remain in the denominator.',
                     'The two-outcome rectangle uses alpha about 0.091 and z=2; no 95 percent simultaneous claim is made.',
                     'Known-variance Gaussian nuisance arithmetic changes the illustrative profit sign range; no empirical coverage or bank ROI is demonstrated.'],
        'evidence': sources, 'independent_review': False, 'financial_decision_qualification': False}
    write(BASE / 'local-review.json', review)
    receipt = control.ledger.receipt_template(node)
    receipt.update(outcome='pass', execution='performed', scope=review['scope'], reviewer=review['reviewer'],
        limitations=review['timing_limits']+['Two administrative harness amendments were needed; the original frozen runner alone failed.',
            'No raw-data fitted-nuisance/dependence validity, verified identity/inclusion, live model, consumer or bank qualification.'],
        outputs=[ref(journey.LOCAL, 'Actual conformance result under disclosed reviewed launch amendments')],
        protocol_sha256=registration['sha256'], all_request_denominator=118,
        fresh_data_identity=ref(BASE / 'fixtures.json', 'New deterministic funding inputs'), retained_failures=True,
        started_at=journal['started_at'], journal=ref(BASE / 'local-journal.json', 'All request slots'),
        failed_harness_launches=2, administrative_amendments=[ref(BASE / n, 'Recorded prospective administrative amendment')
            for n in ['launch-amendment.json', 'completion-amendment.json']])
    for i, finding in enumerate([
        'All 118 fixed request slots matched expectations using available local operations and unchanged fixtures after two disclosed harness repairs; no unavailable fitting/adapter/consumer capability is claimed.',
        'All 29 library/CLI/restart comparisons preserved topology, clock failures, conditional/refused/unsupported results and context; two changed-horizon requests were rejected.']):
        receipt['criteria'][i].update(verdict='pass', finding=finding,
            evidence=[ref(BASE / 'local-review.json', 'Full author review including retained failures and independent reference'),
                      ref(BASE / 'local-journal.json', 'Every actual output')])
    write(BASE / 'local-receipt.json', receipt)
    print(json.dumps({k: review[k] for k in ['status', 'request_slots', 'matching_slots', 'independent_reference_checks', 'failed_harness_launches', 'full_invocation_wall_seconds']}))


if __name__ == '__main__':
    main()
