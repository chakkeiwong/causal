#!/usr/bin/env python3
"""Recover and publish the saved continuity reader without rewriting its evidence."""
import argparse
from collections import Counter
import json
from pathlib import Path

import integration_continuity_reference_20261017 as examples
import master_control as core
import review_integration_continuity_20261017 as work
import review_integration_continuity_reference_20261017 as arithmetic
import run_program as run
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

ROOT, WORK = core.ROOT, work.BASE
BASE, OUT = WORK / 'publication', WORK / 'publication/reader'


def read(path):
    return json.loads(path.read_text())


def review():
    report = read(OUT / 'build-report.json')
    audit = read(OUT / 'source-audit.json')
    index = read(BASE / 'traceability-review.json')
    preserved = read(WORK / 'preservation-review.json')
    prior = read(work.PRIOR)
    for value in [report, audit, index, preserved, read(BASE / 'prepared-inputs.json'),
                  read(WORK / 'source-review.json'), read(WORK / 'saved-trial-review.json'),
                  read(WORK / 'arithmetic-review.json')]:
        verify_bindings(value)
    assert index['status'] == 'pass' and not index['issues']
    assert index['scholarly_pdfs'] == 187 and report['pages'] == 883
    layout = read(OUT / 'text-layout-review.json')
    assert layout['status'] == 'pass' and not layout['out_of_bounds'] and not layout['empty_pages']
    assert all('Underfull' in warning for warning in report['warnings'])
    old = {s['integrated_citation_key']: s for s in prior['sources']}
    new = {s['integrated_citation_key']: s for s in audit['sources']}
    assert len(old) == 696 and len(new) == 699
    assert all(new[key] == value for key, value in old.items())
    old_driver = 'docs/causal_proposal_other_temporal_2026-10-17.tex'
    kept = [r for r in prior['tex_files'] if r['path'] != old_driver]
    files = {r['path']: r['sha256'] for r in audit['tex_files']}
    assert len(kept) == 206 and all(files[r['path']] == r['sha256'] for r in kept)
    previous_index = read(work.PRIOR.parent.parent / 'traceability-review.json')
    contexts = {r['citation_key']: Counter(json.dumps(c, sort_keys=True)
                for c in r['citation_contexts']) for r in index['records']}
    for row in previous_index['records']:
        assert not Counter(json.dumps(c, sort_keys=True)
                           for c in row['citation_contexts']) - contexts[row['citation_key']]
    calculated = examples.calculate()
    assert calculated == read(WORK / 'exact-results.json')
    assert arithmetic.review()['results'] == calculated
    text = ' '.join((OUT / 'reader.txt').read_text().split()).lower()
    for phrase in preserved['text_checks']:
        assert phrase.lower() in text, phrase
    state = core.read(ROOT, core.STATE)
    assert not state['input_receipts'] and state['execution_runtime']['active'] is None
    for operation in work.OPS:
        assert state['execution_program']['results'][operation]['outcome'] == 'pass'
    evidence = [ref(path, anchor) for path, anchor in [
        (OUT / 'build-report.json', 'Saved exact 883-page reader'),
        (OUT / 'source-audit.json', '699 audited sources'),
        (BASE / 'traceability-review.json', '187 genuine scholarly PDFs and full citation contexts'),
        (OUT / 'text-layout-review.json', 'All-page extracted-text bounds'),
        (OUT / 'reader.txt', 'Inspected continuity and adoption passages'),
        (WORK / 'preservation-review.json', 'All inherited source records and contexts retained'),
        (WORK / 'source-review.json', 'Nine local originals and pinned protocol/SDK originals'),
        (WORK / 'saved-trial-review.json', 'Saved actual and instrumented local trials, not rerun'),
        (WORK / 'exact-results.json', 'Five exact authored reference families'),
        (WORK / 'arithmetic-review.json', 'Separate author recomputation'),
        (WORK / 'proposed-contract.json', 'Fifteen proposed test families'),
        (WORK / 'open-gap-register.json', 'Twelve open gaps with remedies and missing inputs'),
        (WORK / 'evaluation-package-template.json', 'Exact-release owner package without fabricated signatures'),
        (WORK / 'continuity.tex', 'Integrated jobs, shared operations and versioning'),
        (WORK / 'adoption.tex', 'Integrated authentic adoption contract'),
        (Path(__file__), 'Crash recovery and exact-reader author review')]]
    write(BASE / 'release-source-review.json', {
        'status': 'pass', 'issues': [], 'reviewer': work.REVIEWER,
        'reviewed_reader': report['pdf'], 'evidence': evidence,
        'scope': 'Author source, arithmetic, preservation and extracted-text release review; proposal only.',
        'preserved_records': 696, 'new_records': 3, 'preserved_compiled_sources': 206,
        'original_contexts_retained': True,
        'findings': [
            'Report-prefix resumption is bounded; arbitrary estimator resumption is not claimed.',
            'Artifact publication and terminal acknowledgement remain separate; crash-window cancellation is not rollback.',
            'The backward-clock example is an exact formula counterexample, not an observed clock failure.',
            'Parity rereviews 13 scientific and three lifecycle comparisons without claiming new runtime observations.',
            'Modern server discovery, optional client discovery, recognized modern errors and legacy fallback remain distinct.',
            'Nine proposed protocol rows are reference decisions, not an implemented modern adapter.',
            'Six assumed owner gates provide no authentic receipt; all twelve substantive gaps remain open.',
            'The saved reader retains inherited source records, compiled content and citation-context multisets.'],
        'observed_failures_and_repairs': [
            'Crash left a built successor unpublished; recovery verified saved immutable artifacts before publication.',
            'A lookup for a nonexistent aggregate author-review file returned no file; separate requirement reviews and final release review supply the actual evidence.',
            'The preserved initial protocol-table draft was corrected before this release; its unsupported-version and other-modern-error branches now differ.'],
        'limitations': work.LIMITS, 'visual_acceptance': False})
    print(json.dumps({'review': 'pass', 'pages': 883, 'source_records': 699}))


def publish():
    state = core.read(ROOT, core.STATE)
    before = core.sha(ROOT / core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['sha256'] == '88c8169c632060126c4a430df2df22922fea217069988965c89e9a0548cb0bd0'
    report = read(OUT / 'build-report.json')
    audit = read(OUT / 'source-audit.json')
    reviewed = read(BASE / 'release-source-review.json')
    verify_bindings(reviewed)
    manifest = {'kind': 'working_monograph', 'final_acceptance': False,
        'pdf': report['pdf'], 'pages': report['pages'],
        'supersedes': {key: state['reader'][key] for key in ['path', 'sha256']},
        'build_report': ref(OUT / 'build-report.json', 'Saved continuity reader'),
        'source_review': ref(BASE / 'release-source-review.json', 'Exact-reader author review'),
        'text_layout': ref(OUT / 'text-layout-review.json', 'All-page text bounds'),
        'source_artifacts': audit['tex_files'] + reviewed['evidence'],
        'visual_acceptance': False, 'mandatory_repairs_closed': [],
        'changes': ['Develop bounded job resumption, shared operation semantics and independent version axes.',
                    'Distinguish exact authored references, saved runtime findings and fifteen proposed test families.',
                    'Bind adoption to authentic exact-release owners and preserve twelve open repair routes.'],
        'sponsor_binding': 'Preserved sponsor baseline; Q5 reconciliation remains open.'}
    write(BASE / 'working-release.json', manifest)
    binding = ref(BASE / 'working-release.json', 'Reviewed continuity working successor')
    run.ledger.validate_working_release(ROOT, binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader'] = {key: report['pdf'][key] for key in ['path', 'sha256']}
    state['reader'].update(pages=report['pages'], status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT, before, state, {'action': 'publish_integration_continuity_reader',
                                   'manifest': binding, 'final_acceptance': False})
    print(json.dumps({'published': state['reader']}))


def renew():
    report = read(OUT / 'build-report.json')
    verify_bindings(read(BASE / 'release-source-review.json'))
    findings = {
        'Q2': 'All 696 inherited audited records, 206 inherited compiled sources and citation-context multisets remain. Three additions bind exact authored evidence, proposed continuity contracts and pinned MCP/SDK originals. All 699 records and 187 genuine scholarly PDFs pass traceability. Saved observations are not represented as fresh trials.',
        'Q3': 'Separate author recomputation verifies 16 ordered checkpoint selections and four valid prefixes, five lock-respecting cancellation placements plus a crash window, a backward-clock counterexample, USD set arithmetic, nine proposed protocol rows and 64 assumed adoption combinations. None qualifies arbitrary recovery, modern SDK execution or authentic institutional acceptance.',
        'Q4': 'The stipulated effect set minus costs yields [-5000,3000] USD for 1000 accounts. Public/generated prototype comparisons precede expensive bank experiments and include failures, preparation, review, recovery, maintenance and matched quality. Bank precision, actual costs, platform acceptance and ROI remain unknown.'}
    for question, finding in findings.items():
        identifier = 'PROPOSAL.' + question
        state = core.read(ROOT, core.STATE)
        assert state['reader']['sha256'] == report['pdf']['sha256']
        previous = state['execution_runtime']['results'][identifier]
        old = read(ROOT / previous['path'])
        folder = BASE / question
        folder.mkdir(exist_ok=False)
        evidence = [previous, ref(BASE / 'working-release.json', 'Exact current reader'),
            ref(BASE / 'release-source-review.json', 'Source, arithmetic and text release review'),
            ref(WORK / 'arithmetic-review.json', 'Separate author recomputation'),
            ref(WORK / 'proposed-contract.json', 'Public/generated comparison and full costs'),
            ref(WORK / 'open-gap-register.json', 'Open implementation and owner gaps'),
            ref(Path(__file__), 'Question-specific author findings')]
        write(folder / 'reopen.json', {'reason': 'Changed reader requires an exact-reader successor review.',
            'prior_result': previous, 'reviewed_reader': report['pdf'], 'evidence': evidence,
            'next_action': 'Record scoped continuity delta; retain broader acceptance limits.'})
        transition('reopen', identifier, folder / 'reopen.json')
        state = core.read(ROOT, core.STATE)
        graph, _, _ = run.combined(ROOT, state)
        node = run.ledger.operation(graph, identifier)
        attempt = len(state['execution_runtime']['review_history'][identifier])
        output = ROOT / run.review_output_paths(node, state['reader'], attempt)[0]
        limits = list(dict.fromkeys(old['limitations'] + work.LIMITS))
        scope = 'Author exact-reader continuity proposal review'
        write(output, {'operation': identifier, 'status': 'pass', 'criterion': node['criteria'][0],
            'reviewer': work.REVIEWER, 'reviewed_reader': report['pdf'], 'review_attempt': attempt,
            'acceptance_scope': 'proposal_only', 'scope': scope, 'findings': [finding],
            'evidence': evidence, 'limitations': limits, 'visual_acceptance': False})
        receipt = run.ledger.receipt_template(node)
        receipt.update(outcome='pass', execution='performed', scope=scope, reviewer=work.REVIEWER,
            limitations=limits, reviewed_reader=report['pdf'], review_attempt=attempt,
            acceptance_scope='proposal_only', outputs=[ref(output, 'Exact-reader ' + question + ' review')],
            nonexecution_reason='', revisit_trigger='',
            criteria=[{'index': 0, 'verdict': 'pass', 'finding': finding, 'evidence': evidence}])
        write(folder / 'operation-receipt.json', receipt)
        transition('record', identifier, folder / 'operation-receipt.json')
    print(json.dumps({'exact_reader_reviews': 'Q2-Q4 pass', 'Q1_Q5': 'open'}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['review', 'publish', 'renew'])
    args = parser.parse_args()
    {'review': review, 'publish': publish, 'renew': renew}[args.command]()
