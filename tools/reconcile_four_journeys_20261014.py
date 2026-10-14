#!/usr/bin/env python3
"""Reconcile four preserved journey trials without rerunning or rewriting them."""
from collections import Counter
from copy import deepcopy
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import run_program as run
import discovery_journey_20261013 as discovery
import funding_journey_successor_20261013 as funding
import observations_journey_20261013 as observations
import servicing_journey_20261014 as servicing
import funding_examples_20261013 as funding_exact
import observations_examples_20261013 as observations_exact
import servicing_observed_examples_20261013 as servicing_exact
from causalbank.artifacts_v12 import encode
from causalbank.runtime_v12 import execution_identity
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

BASE = ROOT / 'docs/program/execution/2026-10-14/four-journeys'
OP = 'IN.REQ.four_banking_journeys'
OUTPUT = ROOT / 'docs/program/comprehensive-v14/work' / OP / 'requirement-review.json'
REVIEWER = {'name': 'Codex author/coordinator', 'kind': 'author'}
READER_BASE = ROOT / 'docs/program/execution/2026-10-14/python-temporal/v3'
LIMITS = [
    'Proposal requirement reconciliation, not four qualified causal products.',
    'Existing deterministic local library/CLI trials; no new service invocations or random sampling.',
    'Correct refusal, syntax or clock output is not an available numeric causal effect.',
    'Four servicing expectation errors and two funding harness amendments remain preserved.',
    'No MCP requalification, actual sibling consumer, live model or upstream package run in these trials.',
    'Bank truth, platform acceptance, real workflow prices and independent review remain later conditional inputs.',
    'Current-reader source/text checks do not close rendered visual acceptance or whole-program coverage.',
]


def read(path):
    return json.loads(path.read_text())


def without_request_id(response):
    value = deepcopy(response)
    if 'invocation_error' in value:
        return {'invocation_error': value['invocation_error']}
    value.pop('request_id', None)
    return value


def acceptance_cases():
    common = [
        'Preserve target, units, horizon, sampling law, set topology and qualification at every boundary.',
        'Retain unavailable and refused requests in the denominator; no fabricated estimate or zero-cost missing value.',
        'Test changed-context replay, malformed input, unknown methods and corrupted artifacts.',
        'Use a separate current MCP suite for a three-surface claim; this evidence covers library and CLI only.',
        'Bind trusted input manifests and test descriptor replacement/FIFO remedies before claiming custody or deadline guarantees.',
    ]
    return {
        'funding': {
            'local_public_next': [
                'Prototype a selected raw-summary estimator with joint fitted-nuisance covariance; compare exact fixed/joint examples and known dependent laws.',
                'Test weak/zero denominators, overlapping horizons, common shocks and incorrect covariance; preserve empty, singleton, disconnected and whole-line results.',
                'Compare household versus record units and known unequal inclusion; flag externally unverified identity instead of treating a declaration as truth.',
                'Map the entire effect set through repricing and incremental spread; retain both profitable and loss-making values.',
                'Use public bank/calendar observations to test availability and preparation, with causal truth confined to declared generated designs.',
            ],
            'later_owner_inputs': ['Dated household/population map and inclusion evidence', 'Assignment/proxy and normalization justification',
                                  'Outcome follow-up, balance units, margins and feasible rate actions', 'Decision tolerances and actual workflow costs'],
            'scientific_obstruction': 'Wrong or missing identity, assignment and joint dependence cannot be repaired by ratio inversion. General learned/dependent nuisance qualification remains research.',
        },
        'servicing': {
            'local_public_next': [
                'Implement one finite observed-history policy estimator and compare complete path enumeration, backward recursion and observed-prefix scores.',
                'Separate policy selection from evaluation and distinguish a fixed trained policy from an unknown optimum.',
                'Vary support, hidden assignment and informative dropout under generated truth; preserve the observational-equivalence counterexamples.',
                'Find a justified precision improvement before an expensive study: the preserved radius exceeds the entire finite policy range.',
                'Correct only future corrupt-input expectations to artifact_access; keep the original 94/98 result.',
            ],
            'later_owner_inputs': ['Eligible cohort, feasible actions and dated observed histories', 'Action and retention mechanism evidence',
                                  'Reward/assistance accounting and policy split', 'Decision precision thresholds and real operating costs'],
            'scientific_obstruction': 'Equal observed laws with unequal hidden-state effects or dropout means require information/restrictions. Arbitrary private state, dependence and unknown optimal policy are not solved by more computation.',
        },
        'discovery': {
            'local_public_next': [
                'Install one pinned discovery adapter behind a graph-family contract; compare with exact oracle graphs before finite-sample recovery.',
                'Test node-order and endpoint conversions, latent/temporal/dependent restrictions and graph-class retention.',
                'Use generated observationally equivalent models to verify honest nonidentification; selected DAG back-door failure is not a universal nonidentification certificate.',
                'Propagate all admissible effects to a decision rule; report class error separately from effect coverage and calibration.',
                'Use public discovery benchmarks with documented interventions and truth limits; refuse to infer truth from package agreement.',
            ],
            'later_owner_inputs': ['Variable meanings, allowed interventions and scientific constraints', 'Sampling clock, regime and latent-variable evidence',
                                  'Accepted graph/effect loss and expert adjudication', 'Consumer owner and prototype comparison costs'],
            'scientific_obstruction': 'An observational equivalence class can contain different intervention effects. General PAG/temporal identification and calibrated effect inference are not installed.',
        },
        'observations': {
            'local_public_next': [
                'Prototype explicit identity/inclusion/label gates with generated known maps; test that truthful-looking timestamps alone cannot satisfy them.',
                'Separate feature availability from outcome ascertainment and censoring; reject future outcomes supplied as pre-action features.',
                'Compare weighted measurement corrections and joint uncertainty using known inclusion/audit laws, including near-singular sensitivity-specificity contrasts.',
                'Test empty, duplicated and false-label records with valid clocks; distinguish a successful clock diagnostic from a passed population audit.',
                'Check public-source lineage and legal availability without asserting authentic borrower identity or causal labels.',
            ],
            'later_owner_inputs': ['Owned population and origin map', 'Selection and joint inclusion design', 'Independent label/audit evidence',
                                  'Feature and follow-up provenance, retention and rights', 'Action model, losses and acceptable residual ambiguity'],
            'scientific_obstruction': 'Hashes preserve bytes, not truth. Marginal inclusion does not establish joint variance, and unknown label sensitivity/specificity can leave prevalence and decisions unidentified.',
        },
        'common': common,
        'schedule': 'Each journey may prototype independently once its own design is reviewed. Bank input acquisition is conditional on prototype merit, not a proposal gate.',
        'acceptance_policy': 'Freeze each selected prototype regime, independent references, tolerances, failures, analysis and costs before final trials; never pool four journeys into one causal qualification rate.',
        'common_limitation_evidence': [ref(ROOT / 'docs/program/execution/2026-10-14/artifact-custody/design-review.json', 'Unimplemented custody repairs and owner boundaries')],
    }


def main():
    assert not OUTPUT.exists() and not (BASE / 'reconciliation.json').exists()
    state = run.core.read(ROOT, run.core.STATE)
    assert state['execution_runtime']['active']['operation'] == OP
    graph, merged, _ = run.combined(ROOT, state)
    identity = execution_identity()
    assert identity['source_sha256'] == '5736465f859bbf0ccf8d3368f957a6434902e79a51bf41a62fc3fa20e1a7709d'
    rows, evidence, totals = [], [], Counter()
    for name, module, size, matches, parity in [
        ('funding', funding, 118, 118, 29), ('servicing', servicing, 98, 94, 24),
        ('discovery', discovery, 98, 98, 24), ('observations', observations, 106, 106, 26),
    ]:
        base = module.BASE
        protocol, result = read(module.DESIGN), read(module.LOCAL)
        journal, fixtures = read(base / 'local-journal.json'), read(base / 'fixtures.json')
        prior_review = read(base / 'local-review.json')
        for value in [protocol, result, prior_review]:
            verify_bindings(value)
        assert read(base / 'environment.json') == identity, name
        node = run.ledger.operation(graph, 'IN.JOURNEY.LOCAL.' + name)
        registration = merged['execution_program']['registrations'][node['id']]
        run.ledger.validate_protocol(ROOT, merged, node, registration)
        assert journal['protocol_sha256'] == result['protocol_sha256'] == registration['sha256']
        assert datetime.fromisoformat(journal['started_at']) > datetime.fromisoformat(registration['registered_at'])
        attempts = journal['attempts']
        assert len(attempts) == len({a['id'] for a in attempts}) == size == result['all_request_count']
        assert sum(a['passed'] for a in attempts) == matches == result['passed_request_count']
        assert result['retained_failures'] and journal['all_requests_retained']
        for segment in journal['segments']:
            prefix = attempts[:segment['prior_request_count']]
            assert hashlib.sha256(encode(prefix)).hexdigest() == segment['prior_attempts_sha256']
        cases = {c['id']: c for c in fixtures['cases']}
        assert len(cases) == parity
        for a in attempts:
            if a['case'] == 'idempotency_drift':
                assert a['response']['status'] == 'rejected'
                assert a['response']['error']['code'] == 'idempotency_conflict'
            else:
                assert module.verdict(cases[a['case']], a['request'], a['response']) == a['failures']
            assert a['passed'] == (not a['failures'])
            if not a['passed']:
                assert name == 'servicing' and a['case'] == 'corrupt_artifact'
                assert a['response']['result'] is None and a['response']['error']['code'] == 'artifact_access'
                assert a['response']['qualification']['level'] == 'none'
        for case in cases:
            group = [a for a in attempts if a['case'] == case]
            assert {(a['route'], a['phase']) for a in group} == {('library','initial'), ('library','restart'), ('cli','initial'), ('cli','restart')}
            canonical = [without_request_id(a['response']) for a in group]
            assert all(r == canonical[0] for r in canonical), (name, case)
            if 'invocation_error' in canonical[0]:
                assert name == 'discovery' and case == 'cycle_invalid'
                for a in group:
                    r = a['response']
                    if a['route'] == 'library':
                        assert r['error_type'] == 'ValueError' and r['message'] == 'DAG declaration contains a directed cycle'
                    else:
                        assert a['process_exit'] == 2
                        assert r['raw']['error'] == {'code': 'invalid_request', 'message': 'DAG declaration contains a directed cycle'}
        assert len(journal['parity']) == parity and all(p['all_four_semantically_equal'] for p in journal['parity'])
        counts = Counter((a['response'].get('status', 'invocation_error'), a['response'].get('disposition', 'invalid_request')) for a in attempts)
        kinds = Counter((a['response'].get('result') or {}).get('kind') for a in attempts if a['response'].get('disposition') == 'computed')
        row = {'journey': name, 'status_of_frozen_trial': result['status'], 'requests': size, 'frozen_matches': matches,
               'parity_cases': parity, 'dispositions': [{'status': k[0], 'disposition': k[1], 'count': v} for k,v in sorted(counts.items())],
               'computed_result_kinds': dict(kinds), 'failed_slots': result['failed_requests'],
               'target': protocol['target'], 'observation_law': protocol['observation_law'], 'sampling_unit': protocol['sampling_unit'],
               'decision_chain': protocol['decision_chain'], 'alternatives': protocol['alternatives'],
               'adverse_cases': protocol['adverse_cases'], 'cost_accounting': protocol['cost_accounting'],
               'evidence_classes': protocol['evidence_classes'], 'limits': protocol['limits'],
               'evidence': [ref(p, 'Preserved '+name+' protocol, complete results, environment or fixture') for p in
                            [module.DESIGN, module.LOCAL, base/'local-journal.json', base/'local-review.json', base/'environment.json', base/'fixtures.json']]}
        rows.append(row); evidence.extend(row['evidence'])
        totals.update(requests=size, frozen_matches=matches, parity_cases=parity)
    assert dict(totals) == {'requests': 420, 'frozen_matches': 416, 'parity_cases': 103}
    exact_rows = []
    for name, calculate, path in [
        ('funding', funding_exact.calculate, funding.BASE/'exact-examples.json'),
        ('servicing', servicing_exact.calculate, ROOT/'docs/program/execution/2026-10-13/servicing/exact-results.json'),
        ('observations', observations_exact.calculate, observations.BASE/'exact-examples.json'),
    ]:
        assert json.loads(json.dumps(calculate())) == read(path), name
        exact_rows.append({'journey': name, 'status': 'pass', 'evidence_class': 'replayed_exact_project_reference', 'original': ref(path, 'Exact preserved reference'),
                           'procedure': ref(ROOT/'tools'/sys.modules[calculate.__module__].__file__.split('/')[-1], 'Pure calculation; main not rerun')})
    audit = read(READER_BASE/'reader/source-audit.json')
    build = read(READER_BASE/'reader/build-report.json')
    assert build['pdf']['sha256'] == state['reader']['sha256']
    tex_paths = {r['path']: r for r in audit['tex_files']}
    source_keys = {s['integrated_citation_key'] for s in audit['sources']}
    aux = (READER_BASE/'reader/causal_proposal_python_temporal_v3_2026-10-14.aux').read_text()
    text = (READER_BASE/'reader/reader.txt').read_text()
    integrated = []
    for name, label, path, key in [
        ('funding', 'exec13:funding-journey', funding.BASE/'section.tex', 'exec13_funding_runtime'),
        ('discovery', 'exec13:discovery-journey', discovery.BASE/'section.tex', 'exec13_discovery_journey'),
        ('observations', 'exec13:observation-journey', observations.BASE/'section.tex', 'exec13_observation_run'),
        ('servicing', 'exec14:servicing-evidence', ROOT/'docs/program/execution/2026-10-14/reader-repair/execution-meaning.tex', 'exec14_servicing_evidence'),
    ]:
        reference = tex_paths[str(path.relative_to(ROOT))]; verify_bindings(reference)
        assert key in source_keys and key in path.read_text()
        match = re.search(re.escape(chr(92)+'newlabel{'+label+'}{{') + r'([^}]+)\}\{([0-9]+)', aux)
        assert match, label
        integrated.append({'journey': name, 'label': label, 'section': match[1], 'printed_start_page': int(match[2]), 'source': reference, 'citation_key': key})
    assert '94 of 98 expected outcomes matched' in ' '.join(text.split())
    assert read(servicing.BASE/'expectation-correction.json')['frozen_result_remains'] == 'negative'
    fund_review = read(funding.BASE/'local-review.json')
    assert fund_review['administrative_amendments'] == fund_review['failed_harness_launches'] == 2
    reconciliation = {'status': 'pass', 'scope': 'Reconciliation of existing evidence; no fresh runtime or sampling trial',
        'reviewer': REVIEWER, 'current_execution_identity': identity, 'totals': dict(totals), 'journeys': rows,
        'exact_replays': exact_rows, 'integrated_manuscript': integrated, 'reviewed_reader': build['pdf'],
        'preserved_negative_evidence': [ref(servicing.BASE/'expectation-correction.json', 'Four frozen expectation mismatches'),
            ref(funding.BASE/'launch-amendment.json', 'First harness amendment'), ref(funding.BASE/'completion-amendment.json', 'Second harness amendment')],
        'evidence': [ref(Path(__file__), 'Read-only data reconciliation and exact replay'), ref(BASE/'plan-review.md', 'Reviewed work and interpretation boundaries')],
        'parity_contract': 'Canonical responses equal excluding request_id. Invalid-request wrappers compare code; this review additionally verifies message, library exception type and CLI exit2.',
        'procedure_repair': ref(BASE/'parity-review-repair.json', 'Preserved overstrict wrapper comparison and source-grounded repair'),
        'limitations': LIMITS, 'bank_qualification': False}
    write(BASE/'reconciliation.json', reconciliation)
    design = acceptance_cases(); verify_bindings(design)
    write(BASE/'acceptance-cases.json', design)
    findings = [
        'All four frozen protocols and complete journals bind the unchanged current runtime and environment. Per-journey public/generated prototype cases and later owner inputs are explicit; no pooled causal qualification is awarded.',
        'Recomputed 420 saved request verdicts, 103 library/CLI/restart comparisons and all prefix hashes. Retain 416 frozen matches, four servicing expectation errors and two funding harness amendments. Exact funding, servicing and observation references reproduce; all four narratives and the negative result are already integrated in the 773-page reader.',
    ]
    evidence = [ref(BASE/'reconciliation.json', 'Complete request/semantic reconciliation and current manuscript bindings'),
                ref(BASE/'acceptance-cases.json', 'Independent next cases, scientific obstructions and conditional owner inputs'),
                ref(BASE/'plan-review.md', 'Plan and review'), ref(Path(__file__), 'Executable evidence review')]
    write(OUTPUT, {'operation': OP, 'status': 'pass', 'scope': 'Proposal requirement development and existing-evidence reconciliation',
                  'reviewer': REVIEWER, 'findings': findings, 'evidence': evidence, 'limitations': LIMITS,
                  'reviewed_reader': build['pdf'], 'implementation_changed': False, 'manuscript_change_needed': False,
                  'original_gap_qualification': False, 'negative_findings_preserved': True})
    receipt = run.ledger.receipt_template(run.ledger.operation(graph, OP))
    receipt.update(outcome='pass', execution='performed', scope='Proposal requirement reconciliation; no product qualification',
                   reviewer=REVIEWER, limitations=LIMITS, outputs=[ref(OUTPUT, 'Reviewed four-journey requirement')],
                   nonexecution_reason='', revisit_trigger='', criteria=[{'index': i, 'verdict': 'pass', 'finding': f, 'evidence': evidence} for i,f in enumerate(findings)])
    write(BASE/'operation-receipt.json', receipt)
    print(json.dumps({'requirement_review': 'pass', **dict(totals), 'fresh_service_calls': 0, 'all_four_integrated': True, 'bank_qualification': False}))


if __name__ == '__main__':
    main()
