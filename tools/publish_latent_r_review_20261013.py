#!/usr/bin/env python3
"""Publish the reviewed latent-R delta and renew exact-reader author reviews."""
import json
from pathlib import Path
import re

import build_integrated_monograph_v12 as shared
import latent_r_examples_v3_20261013 as examples
import master_control as core
import run_program as run

ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-13/latent-r'
NEW = BASE / 'v2'
OUT = NEW / 'reader'
OLD = ROOT / 'docs/program/execution/2026-10-13/traceability-successor/v2'
OP = 'SW.CELL.discovery_latent.R'
ref = shared.ref


def write(path, data):
    assert not path.exists(), 'Preserve existing evidence: ' + str(path)
    core.write(path, data)


def verify_bindings(value):
    """Hash-check heterogeneous audit records; the v2 auditor checks paper naming."""
    if isinstance(value, dict):
        if 'path' in value and 'sha256' in value:
            path = core.safe(ROOT, value['path'])
            assert path.is_file() and core.sha(path) == value['sha256'], value['path']
        for child in value.values():
            verify_bindings(child)
    elif isinstance(value, list):
        for child in value:
            verify_bindings(child)


def transition(action, identifier, path):
    state = core.read(ROOT, core.STATE)
    before = core.sha(ROOT / core.STATE)
    event = run.apply(ROOT, state, action, identifier, str(path.relative_to(ROOT)))
    run.commit(ROOT, before, state, event)
    print(json.dumps({'action': action, 'operation': identifier}), flush=True)


def main():
    state = core.read(ROOT, core.STATE)
    before = core.sha(ROOT / core.STATE)
    assert state['execution_runtime']['active']['operation'] == OP
    assert state['reader']['path'] == 'docs/causal_proposal_source_review_v2_2026-10-13.pdf'
    report = json.loads((OUT / 'build-report.json').read_text())
    audit = json.loads((OUT / 'source-audit.json').read_text())
    prior_audit = json.loads((OLD / 'reader/source-audit.json').read_text())
    index = json.loads((NEW / 'traceability-review.json').read_text())
    prior_index = json.loads((OLD / 'traceability-review.json').read_text())
    for obj in [report, audit, json.loads((BASE / 'source-audit-final.json').read_text()),
                json.loads((BASE / 'author-review.json').read_text()),
                json.loads((NEW / 'reader-input/prepared-inputs.json').read_text())]:
        verify_bindings(obj)
    assert index['status'] == 'pass' and index['scholarly_pdfs'] == 147
    assert not any('Overfull' in x or 'undefined' in x.lower() for x in report['warnings'])
    assert json.loads((OUT / 'text-layout-review.json').read_text())['status'] == 'pass'
    previous_sources = {s['integrated_citation_key']: s for s in prior_audit['sources']}
    current_sources = {s['integrated_citation_key']: s for s in audit['sources']}
    assert all(current_sources[k] == v for k, v in previous_sources.items())
    added_keys = sorted(current_sources.keys() - previous_sources.keys())
    assert len(added_keys) == 5
    old_driver = ROOT / 'docs/causal_proposal_source_review_v2_2026-10-13.tex'
    driver = ROOT / report['driver']['path']
    prior_copy = OLD / 'longitudinal-doses-preserving.tex'
    next_copy = BASE / 'reader-input/longitudinal-doses-copyedit.tex'
    old_phrase = r'internal estimator.\cite{v13_sw_causaldrf}'
    new_phrase = r'internal estimator~\citep{v13_sw_causaldrf}.'
    assert prior_copy.read_text().count(old_phrase) == 1
    assert next_copy.read_text() == prior_copy.read_text().replace(old_phrase, new_phrase)
    expected_driver = old_driver.read_text().replace(
        r'\input{program/execution/2026-10-13/pcalg-reuse/decision.tex}',
        r'\input{program/execution/2026-10-13/pcalg-reuse/decision.tex}' + '\n' +
        r'\input{program/execution/2026-10-13/latent-r/v2/comparison.tex}', 1).replace(
        str(prior_copy.relative_to(ROOT / 'docs')), str(next_copy.relative_to(ROOT / 'docs')), 1).replace(
        'program/execution/2026-10-13/identification-review/refs}',
        'program/execution/2026-10-13/identification-review/refs,program/execution/2026-10-13/latent-r/reader-input/refs}', 1)
    assert driver.read_text() == expected_driver
    replaced = {str(old_driver.relative_to(ROOT)), str(prior_copy.relative_to(ROOT))}
    unchanged_files = [r for r in prior_audit['tex_files'] if r['path'] not in replaced]
    for item in unchanged_files:
        core.bound(ROOT, item)
    old_contexts = {r['citation_key']: r for r in prior_index['records']}
    new_contexts = {r['citation_key']: r for r in index['records']}
    changed = []
    for key, source in old_contexts.items():
        a = [(c['path'], c['context']) for c in source['citation_contexts']]
        b = [(c['path'], c['context']) for c in new_contexts[key]['citation_contexts']]
        if a != b:
            changed.append(key)
    assert set(changed) == {'v131_sw_causaldrf', 'v13_project_exact', 'v13_sw_causaldrf',
                            'v13_sw_causalgps', 'v13_sw_grf', 'v13_sw_pygformula'}
    replay = examples.calculate()
    saved = json.loads((BASE / 'exact-results-v3.json').read_text())
    assert replay == saved == json.loads((NEW / 'exact-replay.json').read_text())
    text = re.sub(r'\s+', ' ', (OUT / 'reader.txt').read_text())
    for phrase in ['23.7 R discovery when borrower risk and selection are hidden',
                   'not a sharp identified set', 'USD 40, USD', 'source-level counterexample',
                   'No package execution, finite-sample calibration or accepted R']:
        assert phrase in text, phrase
    findings = {
        'exec13_latentr_primary': 'Pinned manuals and source support RFCI semantics, selection/JCI restrictions, search caps, missing-CI rules, seven conversion branches and incomplete diagnostics. Static traces are explicitly distinguished from native results.',
        'exec13_latentr_colombo2012': 'Definitions 3.1/3.2 and Theorem 3.2 support endpoint and weaker RFCI adjacency claims; Section 4 assumptions concern IID selected Gaussian data, faithfulness, sparsity and signal bounds. No finite graph coverage is inferred.',
        'exec13_latentr_colombo2014': 'Table 2 and Section 4.4 distinguish initial skeleton stability from final RFCI order dependence; the manuscript preserves that restriction.',
        'exec13_latentr_claassen2013': 'Section 5 and the complexity analysis concern fixed-degree faithful oracle models; conditioning-set power and sample limitations prevent a practical-runtime or calibration claim.',
        'exec13_latentr_exact': 'All positive observed tables, selection normalization, net values, test-family illustration and endpoint source trace reproduce exactly. The examples are authored mechanisms and prices, not an exhaustive identified set or upstream execution.'}
    review = {
        'status': 'pass_in_stated_scope', 'reviewer': {'name': 'Codex author/coordinator', 'kind': 'author'},
        'scope': 'Exact-reader source, manuscript, mathematical and economic delta; no coverage/depth or visual acceptance',
        'reviewed_reader': report['pdf'], 'prior_review': state['execution_runtime']['results']['PROPOSAL.Q2'],
        'unchanged_prior_citation_records': len(previous_sources),
        'unchanged_prior_context_keys': len(previous_sources) - len(changed),
        'unchanged_compiled_files': len(unchanged_files),
        'changed_existing_context_keys': changed,
        'changed_context_disposition': 'Preserving chapter copy; exact whole-file comparison permits only the inspected citation punctuation/style change. All scientific content remains identical.',
        'added_records': [{'citation_key': key, 'finding': findings[key],
                           'contexts_reviewed': new_contexts[key]['citation_contexts'],
                           'primary_sources': new_contexts[key]['local_copies'],
                           'inspected_anchors': new_contexts[key]['anchors']} for key in added_keys],
        'evidence': [ref(BASE / p, p) for p in ['author-review.json', 'primary-review.json',
             'source-audit-final.json', 'paper-identities.json', 'candidate-dispositions.json',
             'omissions-register.json', 'exact-results-v3.json', 'v2/hierarchy-repair.json',
             'v2/exact-replay.json', 'v2/traceability-review.json']],
        'text_review': 'Physical pages 229–233 preserve the reviewed argument and independent section 23.7; all-page text bounds pass.',
        'recovery': 'The old tool handle was unavailable, but the prior build completed during recovery. The duplicate-build guard refused to overwrite it; no replacement build was executed. Initial publication validators assumed flat paper naming and anchor schemas and stopped before any mutation. The corrected validator checks all hash bindings and uses the existing v2 auditor for heterogeneous paper and anchor schemas.',
        'visual_acceptance': False,
        'visual_limit': 'Inherited six-image allowance exhausted; rendered-image acceptance remains separate and open.'}
    write(NEW / 'release-source-review.json', review)
    release = {
        'kind': 'working_monograph', 'final_acceptance': False, 'pdf': report['pdf'], 'pages': report['pages'],
        'supersedes': {k: state['reader'][k] for k in ['path', 'sha256']},
        'build_report': ref(OUT / 'build-report.json', 'Completed 630-page preserving reader'),
        'source_review': ref(NEW / 'release-source-review.json', 'Substantive source and reader delta review'),
        'text_layout': ref(OUT / 'text-layout-review.json', 'Whole-reader physical text bounds'),
        'source_artifacts': audit['tex_files'] + [ref(BASE / p, 'Reviewed source and reproduction evidence') for p in
            ['source-audit-final.json', 'primary-review.json', 'author-review.json', 'paper-identities.json',
             'search-protocol.json', 'candidate-dispositions.json', 'omissions-register.json',
             'exact-results-v3.json', 'v2/exact-replay.json', 'v2/traceability-review.json',
             'v2/release-source-review.json', 'v2/hierarchy-repair.json', 'v2/reader/source-audit.json']] +
            [ref(Path(__file__), 'Preserving publication and review continuation')],
        'visual_acceptance': False, 'mandatory_repairs_closed': [],
        'changes': ['Developed R latent-discovery section with three equal-observation banking mechanisms.',
                    'Inspected FCI/RFCI/FCI+ semantics, source-level conversion loss and incomplete diagnostics.',
                    'Corrected chapter hierarchy and one citation-spacing defect.'],
        'sponsor_binding': 'Sponsor is a preserved earlier document; Q5 reconciliation remains open.'}
    write(NEW / 'working-release.json', release)
    binding = ref(NEW / 'working-release.json', 'Reviewed R latent-discovery working monograph')
    run.ledger.validate_working_release(ROOT, binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader'] = {k: report['pdf'][k] for k in ['path', 'sha256']}
    state['reader'].update(pages=report['pages'], status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT, before, state, {'action': 'publish_latent_r_working_reader', 'manifest': binding,
                                    'original_gap_qualification': False, 'final_acceptance': False})
    graph, _, _ = run.combined(ROOT, state)
    node = run.ledger.operation(graph, OP)
    output = ROOT / node['outputs'][0]
    coverage = {'cell': 'discovery_latent::R', 'status': 'pass_bounded_source_review',
        'scope': 'All ten saved search identities plus pinned pcalg aliases and selected one-hop originals',
        'cutoff': '2026-10-07', 'exhaustive_census': False,
        'findings': list(findings.values()), 'release': binding,
        'evidence': review['evidence'], 'native_package_executed': False,
        'integration_decision': 'Restricted adapter proposed; arbitrary graph-as-decision adoption and wholesale port not justified.',
        'remaining': ['Uninspected literature leads retained in omissions; no absent-feature claim.',
                      'Native parser/algorithm fixtures, diagnostic instrumentation and calibration not executed.',
                      'MR01 whole-survey breadth/depth and Q5 remain open.']}
    write(output, coverage)
    receipt = run.ledger.receipt_template(node)
    receipt.update(outcome='pass', execution='performed', scope=coverage['scope'],
                   reviewer=review['reviewer'], limitations=coverage['remaining'],
                   outputs=[ref(output, 'Bounded R latent-discovery source coverage')], nonexecution_reason='',
                   revisit_trigger='New eligible primary source, changed package pin or native qualification evidence')
    facts = [
        ('All ten search identities and six pcalg algorithm aliases have explicit dated, bounded dispositions.',
         ['search-protocol.json', 'candidate-dispositions.json']),
        ('Five added cited sources have authentic local bytes and inspected technical support; 147 scholarly PDFs and 464 source records are traceable in the exact reader.',
         ['source-audit-final.json', 'paper-identities.json', 'v2/traceability-review.json', 'v2/release-source-review.json']),
        ('FCI/RFCI/FCI+, sufficient-graph and other-language alternatives, omissions and restricted reuse choices are explained without unsupported absence or runtime claims.',
         ['omissions-register.json', 'author-review.json', 'v2/comparison.tex'])]
    receipt['criteria'] = [{'index': i, 'verdict': 'pass', 'finding': f,
                            'evidence': [ref(BASE / p, f) for p in paths]} for i, (f, paths) in enumerate(facts)]
    receipt_path = NEW / 'operation-receipt.json'
    write(receipt_path, receipt)
    transition('record', OP, receipt_path)

    # These are substantive delta reviews above, not an automatic grant from file checks.
    q_findings = {
        'Q2': 'All 459 prior source records are unchanged; 453 prior context keys match exactly and six retain identical scientific text in a typography-only preserving copy. Five new source contexts have explicit primary and mathematical author review; all 147 scholarly PDFs are authentic local files.',
        'Q3': 'The prior demonstrated portfolio is unchanged. The added exact three-world example and static endpoint trace reproduce; native R execution, parser behavior, finite-sample calibration and prospective qualification remain unclaimed.',
        'Q4': 'The prior investment argument and conditional next experiments are unchanged. Added contact values follow explicitly stipulated effects and USD 100/20 prices. The next experiment asks which restriction or intervention can resolve decision-relevant ambiguity; no bank ROI or vendor-cost evidence is asserted.'}
    for q in ['Q2', 'Q3', 'Q4']:
        identifier = 'PROPOSAL.' + q
        current = core.read(ROOT, core.STATE)
        prior_result = current['execution_runtime']['results'][identifier]
        prior_receipt = core.read(ROOT, prior_result['path'])
        folder = NEW / q
        folder.mkdir(exist_ok=False)
        note = {'reason': 'The newly published R latent-discovery reader requires an exact-reader review.',
                'prior_result': prior_result, 'reviewed_reader': report['pdf'],
                'evidence': [binding, ref(NEW / 'release-source-review.json', q_findings[q])],
                'next_action': 'Record the reviewed semantic delta, preserving the prior review and every unaltered limitation.'}
        write(folder / 'reopen.json', note)
        transition('reopen', identifier, folder / 'reopen.json')
        current = core.read(ROOT, core.STATE)
        graph, _, _ = run.combined(ROOT, current)
        node = run.ledger.operation(graph, identifier)
        attempt = len(current['execution_runtime']['review_history'][identifier])
        output = ROOT / run.review_output_paths(node, current['reader'], attempt)[0]
        evidence = [prior_result, binding, ref(NEW / 'release-source-review.json', q_findings[q]),
                    ref(NEW / 'exact-replay.json', 'Exact deterministic reproduction; no upstream runtime')]
        reviewed = {'operation': identifier, 'status': 'pass', 'criterion': node['criteria'][0],
                    'reviewer': review['reviewer'], 'reviewed_reader': report['pdf'],
                    'review_attempt': attempt, 'acceptance_scope': 'proposal_only',
                    'scope': 'Exact current-reader author review by inspected preserving delta',
                    'findings': [q_findings[q]], 'evidence': evidence,
                    'limitations': prior_receipt['limitations'] +
                        ['R native FCI/RFCI/FCI+ and parser execution remain unperformed.',
                         'Q1 coverage/depth and Q5 rendered release/sponsor reconciliation remain open.'],
                    'visual_acceptance': False, 'bank_ROI_established': False}
        write(output, reviewed)
        receipt = run.ledger.receipt_template(node)
        receipt.update(outcome='pass', execution='performed', scope=reviewed['scope'],
                       reviewer=review['reviewer'], limitations=reviewed['limitations'],
                       reviewed_reader=report['pdf'], review_attempt=attempt,
                       acceptance_scope='proposal_only', outputs=[ref(output, 'Current-reader ' + q + ' review')],
                       nonexecution_reason='', revisit_trigger='',
                       criteria=[{'index': 0, 'verdict': 'pass', 'finding': q_findings[q], 'evidence': evidence}])
        write(folder / 'operation-receipt.json', receipt)
        transition('record', identifier, folder / 'operation-receipt.json')
    current = core.read(ROOT, core.STATE)
    summary = run.status(ROOT, current)
    print(json.dumps({k: summary[k] for k in ['reader', 'next', 'ready_proposal_operations',
                                             'recorded_proposal_operations', 'proposal_gaps']}), flush=True)


if __name__ == '__main__':
    main()
