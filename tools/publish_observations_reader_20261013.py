#!/usr/bin/env python3
"""Publish the observation chapter and review its exact, preserving reader delta."""
import json
from pathlib import Path
import re

import master_control as core
import observations_examples_20261013 as examples
import run_program as run
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-13/observations-journey'
OUT = BASE / 'reader'
OLD = ROOT / 'docs/program/execution/2026-10-13/latent-r/v2'


def main():
    state = core.read(ROOT, core.STATE)
    before = core.sha(ROOT / core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path'] == 'docs/causal_proposal_latent_r_v2_2026-10-13.pdf'
    report = json.loads((OUT / 'build-report.json').read_text())
    audit = json.loads((OUT / 'source-audit.json').read_text())
    index = json.loads((BASE / 'traceability-review.json').read_text())
    old_audit = json.loads((OLD / 'reader/source-audit.json').read_text())
    old_index = json.loads((OLD / 'traceability-review.json').read_text())
    local = json.loads((BASE / 'local-review.json').read_text())
    for obj in [report, audit, local, json.loads((BASE / 'prepared-inputs.json').read_text()),
                json.loads((BASE / 'manuscript-review.json').read_text())]:
        verify_bindings(obj)
    assert index['status'] == 'pass' and index['scholarly_pdfs'] == 147
    assert report['pages'] == 635 and report['cited_records'] == 468
    assert not any('Overfull' in x or 'undefined' in x.lower() for x in report['warnings'])
    assert json.loads((OUT / 'text-layout-review.json').read_text())['status'] == 'pass'
    previous_sources = {s['integrated_citation_key']: s for s in old_audit['sources']}
    current_sources = {s['integrated_citation_key']: s for s in audit['sources']}
    assert len(previous_sources) == 464
    assert all(current_sources[k] == v for k, v in previous_sources.items())
    old_driver = ROOT / 'docs/causal_proposal_latent_r_v2_2026-10-13.tex'
    marker = r'\input{program/execution/2026-10-13/funding-journey/section.tex}'
    expected = old_driver.read_text().replace(marker, marker + '\n' +
        r'\input{program/execution/2026-10-13/observations-journey/section.tex}', 1).replace(
        'program/execution/2026-10-13/latent-r/reader-input/refs}',
        'program/execution/2026-10-13/latent-r/reader-input/refs,program/execution/2026-10-13/observations-journey/refs}', 1)
    assert (ROOT / report['driver']['path']).read_text() == expected
    unchanged = [r for r in old_audit['tex_files'] if r['path'] != str(old_driver.relative_to(ROOT))]
    for item in unchanged:
        core.bound(ROOT, item)
    prior_contexts = {r['citation_key']: r for r in old_index['records']}
    contexts = {r['citation_key']: r for r in index['records']}
    for key, item in prior_contexts.items():
        assert contexts[key]['citation_contexts'] == item['citation_contexts'], key
    replay = examples.calculate()
    assert replay == json.loads((BASE / 'exact-examples.json').read_text())
    assert local['status'] == 'pass' and local['request_slots'] == local['matching_slots'] == 106
    assert local['parity_cases'] == 26 and local['independent_rational_membership_checks'] == 1446
    assert sum(r['count'] for r in local['dispositions']) == 106
    extracted = re.sub(r'\s+', ' ', (OUT / 'reader.txt').read_text())
    for phrase in ['43.14 An observation contract', 'All 106 registered requests matched',
                   '52 computed outputs, 20 unsupported requests', '42.398 seconds',
                   'An empty row array', 'an additional stipulated causal model']:
        assert phrase in extracted, phrase
    findings = {
        'exec13_observation_design': 'The frozen design separates feature/outcome clocks, source integrity, identity, inclusion and label truth; admission is proposed. Its cases and stopping rule preceded the registered 106-slot screen.',
        'exec13_observation_exact': 'Finite-law enumeration reproduces the inclusion variances, zero-inclusion nonidentification, joint-map contrasts, label worlds, covariance example and stipulated contact values. The double-sum variance, joint derivative and one-way projection-coverage implication follow the explicit assumptions; no sampling law or causal efficacy is inferred from recorded labels.',
        'exec13_observation_primary': 'Inspected _audit implements strict feature timing only, accepts empty arrays and does not verify identity or labels. The service preserves conditional supplied-moment inference and refuses explicit contradictions. Automatic relevant-audit admission and raw-data measurement correction are proposed.',
        'exec13_observation_run': 'All registered request slots and negative dispositions remain in the denominator; 26 full-response parity and 1446 rational checks pass. Invocation time is a measured local subset of cost; restart is not process-kill, multi-host or bank qualification.'}
    assert set(current_sources) - set(previous_sources) == set(findings)
    write(BASE / 'exact-replay.json', replay)
    review = {
        'status': 'pass', 'issues': [], 'reviewer': {'name': 'Codex author/coordinator', 'kind': 'author'},
        'scope': 'Observation source, mathematical, registered-outcome and economic delta in exact reader',
        'reviewed_reader': report['pdf'], 'prior_review': state['execution_runtime']['results']['PROPOSAL.Q2'],
        'unchanged_prior_source_records': 464, 'unchanged_prior_context_keys': 464,
        'unchanged_compiled_files': len(unchanged),
        'added_records': [{'citation_key': key, 'finding': finding,
                           'contexts_reviewed': contexts[key]['citation_contexts'],
                           'primary_sources': contexts[key]['local_copies'],
                           'inspected_anchors': contexts[key]['anchors']} for key, finding in findings.items()],
        'evidence': [ref(BASE / p, 'Reviewed evidence and exact reproduction') for p in
                     ['source-audit.json', 'manuscript-review.json', 'local-review.json',
                      'registration-control.json', 'record-control.json', 'exact-replay.json', 'traceability-review.json']],
        'text_review': 'Section 43.14, printed pages 468–473 / physical pages 485–490; complete text and physical bounds inspected.',
        'preflight_repair': 'Initial publication preflight expected the phrase a stipulated causal model; the manuscript correctly says an additional stipulated causal model. Corrected the text probe before any evidence or ledger write; no scientific or manuscript change.',
        'visual_acceptance': False, 'independent_review': False,
        'visual_limit': 'Inherited image allowance exhausted; whole-reader rendered acceptance remains open.'}
    write(BASE / 'release-source-review.json', review)
    release = {
        'kind': 'working_monograph', 'final_acceptance': False, 'pdf': report['pdf'], 'pages': report['pages'],
        'supersedes': {k: state['reader'][k] for k in ['path', 'sha256']},
        'build_report': ref(OUT / 'build-report.json', 'Completed preserving 635-page reader'),
        'source_review': ref(BASE / 'release-source-review.json', 'Substantive delta review'),
        'text_layout': ref(OUT / 'text-layout-review.json', 'Whole-reader extracted text bounds'),
        'source_artifacts': audit['tex_files'] + review['evidence'] +
            [ref(BASE / 'release-source-review.json', 'Exact release source and claim review'),
             ref(OUT / 'source-audit.json', '468 cited sources and 147 scholarly PDFs'),
             ref(Path(__file__), 'Preserving publication and review continuation')],
        'visual_acceptance': False, 'mandatory_repairs_closed': [],
        'changes': ['Developed observation-contract section and exact measurement/decision examples.',
                    'Integrated registered local workflow outcomes and unresolved observation-admission limits.'],
        'sponsor_binding': 'Sponsor remains an earlier document; reconciliation is retained under Q5.'}
    write(BASE / 'working-release.json', release)
    binding = ref(BASE / 'working-release.json', 'Reviewed observation working monograph')
    run.ledger.validate_working_release(ROOT, binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader'] = {k: report['pdf'][k] for k in ['path', 'sha256']}
    state['reader'].update(pages=report['pages'], status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT, before, state, {'action': 'publish_observations_working_reader', 'manifest': binding,
                                    'final_acceptance': False, 'bank_qualification': False})
    q_findings = {
        'Q2': 'All 464 predecessor source records and citation contexts are unchanged. Four added project records have inspected local implementation, authored derivations, frozen protocol and actual registered outcomes; 468 records and 147 genuine scholarly PDFs are traceable in this exact reader.',
        'Q3': 'The previous demonstration portfolio is preserved. The added registered screen reports 106/106 boundary matches, all 106 dispositions, 26 response-parity comparisons and 1446 independent rational checks. Refusals and unsupported cases are not useful causal estimates. Empty-audit admission, noisy labels and identity/inclusion truth remain unresolved; no automatic audit-to-estimator, arbitrary sampling coverage or bank qualification is claimed.',
        'Q4': 'The previous investment scenarios and proposed experiments are preserved. The added label example separates stipulated half-prevention efficacy and USD 1000/200 prices from measured evidence. Inclusion/label uncertainty can reverse a decision; the proposed next experiment targets that consequential missing information. All cost categories are retained, and 42.398 seconds is only the measured local invocation subset, not bank ROI.'}
    for q, finding in q_findings.items():
        identifier = 'PROPOSAL.' + q
        current = core.read(ROOT, core.STATE)
        prior = current['execution_runtime']['results'][identifier]
        prior_receipt = core.read(ROOT, prior['path'])
        folder = BASE / q
        folder.mkdir(exist_ok=False)
        evidence = [prior, binding, ref(BASE / 'release-source-review.json', finding),
                    ref(BASE / 'local-review.json', 'Registered screen, all denominators and limits'),
                    ref(BASE / 'exact-replay.json', 'Exact deterministic reproduction')]
        write(folder / 'reopen.json', {'reason': 'New observation working reader needs exact-release review.',
            'prior_result': prior, 'reviewed_reader': report['pdf'], 'evidence': evidence,
            'next_action': 'Record reviewed delta, preserving the prior review and all unchanged limitations.'})
        transition('reopen', identifier, folder / 'reopen.json')
        current = core.read(ROOT, core.STATE)
        graph, _, _ = run.combined(ROOT, current)
        node = run.ledger.operation(graph, identifier)
        attempt = len(current['execution_runtime']['review_history'][identifier])
        output = ROOT / run.review_output_paths(node, current['reader'], attempt)[0]
        limits = prior_receipt['limitations'] + [
            'Observation clock and supplied-summary conformance do not establish identity, inclusion or label truth.',
            'Relevant nonempty audit admission and raw-data measurement correction remain proposed.',
            'Q1 coverage/depth and Q5 exact rendered review and sponsor coherence remain open.']
        reviewed = {'operation': identifier, 'status': 'pass', 'criterion': node['criteria'][0],
            'reviewer': review['reviewer'], 'reviewed_reader': report['pdf'], 'review_attempt': attempt,
            'acceptance_scope': 'proposal_only', 'scope': 'Current-reader author review through preserving delta',
            'findings': [finding], 'evidence': evidence, 'limitations': limits,
            'visual_acceptance': False, 'bank_ROI_established': False}
        write(output, reviewed)
        receipt = run.ledger.receipt_template(node)
        receipt.update(outcome='pass', execution='performed', scope=reviewed['scope'],
            reviewer=review['reviewer'], limitations=limits, reviewed_reader=report['pdf'],
            review_attempt=attempt, acceptance_scope='proposal_only', outputs=[ref(output, 'Current-reader '+q+' review')],
            nonexecution_reason='', revisit_trigger='',
            criteria=[{'index': 0, 'verdict': 'pass', 'finding': finding, 'evidence': evidence}])
        write(folder / 'operation-receipt.json', receipt)
        transition('record', identifier, folder / 'operation-receipt.json')
    summary = run.status(ROOT, core.read(ROOT, core.STATE))
    print(json.dumps({k: summary[k] for k in ['reader', 'next', 'recorded_proposal_operations', 'proposal_gaps']}), flush=True)


if __name__ == '__main__':
    main()
