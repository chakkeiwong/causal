#!/usr/bin/env python3
"""Sequential review, recording and publication of a bounded temporal survey."""
import argparse
from collections import Counter
import json
from pathlib import Path

import build_other_temporal_reader_20261017 as build
import master_control as core
import review_other_temporal_sources_20261017 as work
import run_program as run
import temporal_reference_v2_20261017 as examples
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

ROOT, BASE, OUT, WORK = build.ROOT, build.BASE, build.OUT, build.WORK


def read(path):
    return json.loads(path.read_text())


def review():
    report, audit, prior = read(OUT / 'build-report.json'), read(OUT / 'source-audit.json'), read(build.PRIOR)
    index = read(BASE / 'traceability-review.json')
    for obj in [report, audit, prior, index, read(BASE / 'prepared-inputs.json'),
            read(WORK / 'author-review.json')]:
        verify_bindings(obj)
    assert index['status'] == 'pass' and not index['issues'] and index['scholarly_pdfs'] == 187
    layout = read(OUT / 'text-layout-review.json')
    assert layout['status'] == 'pass' and not layout['out_of_bounds'] and not layout['empty_pages']
    assert not [w for w in report['warnings'] if 'Underfull' not in w]
    assert build.DRIVER.read_text() == build.expected_driver()
    old = {s['integrated_citation_key']: s for s in prior['sources']}
    new = {s['integrated_citation_key']: s for s in audit['sources']}
    assert len(old) == 686 and len(new) == 696 and all(new[k] == s for k, s in old.items())
    files = {r['path']: r for r in audit['tex_files']}
    kept = [r for r in prior['tex_files'] if r['path'] != str(build.OLD.relative_to(ROOT))]
    assert all(files[r['path']]['sha256'] == r['sha256'] for r in kept)
    previous = read(build.PRIOR.parent.parent / 'traceability-review.json')
    contexts = {r['citation_key']: Counter(json.dumps(c, sort_keys=True)
        for c in r['citation_contexts']) for r in index['records']}
    for row in previous['records']:
        assert not Counter(json.dumps(c, sort_keys=True)
            for c in row['citation_contexts']) - contexts[row['citation_key']]
    text = ' '.join((OUT / 'reader.txt').read_text().split())
    for phrase in ['Temporal discovery in Julia, Rust and MATLAB', 'USD 25 per account',
            'USD 109.375', 'not a p-value', 'target-row/source-column',
            'not a blanket restriction', 'appearing or disappearing edges',
            'minimum 1/20', 'MVGC2', 'rejection probability 1/20']:
        assert phrase in text, phrase
    assert examples.calculate() == read(WORK / 'exact-results-v2.json')
    evidence = [ref(path, anchor) for path, anchor in [
        (OUT / 'build-report.json', 'Preserving temporal comparison reader'),
        (OUT / 'source-audit.json', '696 source records'),
        (BASE / 'traceability-review.json', '187 genuine scholarly PDFs and retained contexts'),
        (OUT / 'text-layout-review.json', 'All-page text bounds'),
        (OUT / 'reader.txt', 'Inspected integrated temporal comparison'),
        (WORK / 'source-review.json', 'Forty pinned originals, inherited licenses and original papers'),
        (WORK / 'primary-clarification.json', 'CD-NOD classical definition and explicit generalization'),
        (WORK / 'candidate-register.json', 'Forty-three retained entries and aliases'),
        (WORK / 'omissions-register.json', 'Ten concrete limitations and revisit routes'),
        (WORK / 'exact-results-v2.json', 'Six exact authored mathematical families'),
        (WORK / 'arithmetic-review.json', 'Alternative enumeration, scalar recurrences and rank checks'),
        (WORK / 'proposed-contract.json', 'Six package decisions and public/generated prototype'),
        (WORK / 'author-review.json', 'Criterion-specific author review'),
        (WORK / 'recovery-review.json', 'Preserved crash recovery and source correction'),
        (work.OUTPUT, 'Bounded coverage finding'),
        (Path(__file__), 'Exact-reader preservation review and sequential transitions')]]
    write(BASE / 'release-source-review.json', {
        'status': 'pass', 'issues': [], 'reviewer': work.REVIEWER,
        'reviewed_reader': report['pdf'],
        'scope': 'Author primary-source, exact mathematics and extracted-text review; ecosystem coverage inconclusive.',
        'preserved_records': 686, 'new_records': 10, 'preserved_compiled_sources': len(kept),
        'original_contexts_retained': True, 'evidence': evidence,
        'findings': read(WORK / 'author-review.json')['findings'] + [
            'The CD-NOD classical soft-intervention definition is distinguished from its broader changing-mechanism extension.',
            'All predecessor source records, compiled sources and citation-context multisets remain.',
            'Extracted equations, table and substantive comparison inspected; no additional images consumed.'],
        'observed_failures_and_repairs': [
            'Recovered legacy-byte decoding failure is preserved in recovery-review.json; original bytes remain unchanged.',
            'One progress command lacked --receipt and failed argument parsing before mutation; the corrected command recorded the reviewed progress.',
            'No unavailable original, runtime or visual review is represented as completed.'],
        'limitations': work.LIMITS, 'visual_acceptance': False})
    print(json.dumps({'review': 'pass', 'pages': report['pages'],
        'sections': report['other_temporal_sections'], 'coverage': 'inconclusive'}))


def record():
    verify_bindings(read(BASE / 'release-source-review.json'))
    author = read(WORK / 'author-review.json')
    state = core.read(ROOT, core.STATE)
    graph, _, _ = run.combined(ROOT, state)
    node = run.ledger.operation(graph, work.OP)
    receipt = run.ledger.receipt_template(node)
    receipt.update(outcome='inconclusive', execution='performed',
        scope='Six-family Julia/Rust/MATLAB temporal and interventional source comparison; broader census remains open.',
        reviewer=work.REVIEWER, limitations=work.LIMITS, capabilities=[],
        outputs=[ref(work.OUTPUT, 'Reviewed bounded temporal coverage')], nonexecution_reason='',
        revisit_trigger='Inspect omitted leads and later pages, complete rights, qualify temporal null laws and frozen executable boundaries before enabling adapters.',
        criteria=[{'index': i, 'verdict': author['criteria_verdicts'][i], 'finding': finding,
            'evidence': [ref(WORK / 'author-review.json', 'Criterion review'),
                ref(BASE / 'release-source-review.json', 'Preserving integration')]}
            for i, finding in enumerate(author['findings'])])
    write(BASE / 'operation-receipt.json', receipt)
    transition('record', work.OP, BASE / 'operation-receipt.json')


def publish():
    state = core.read(ROOT, core.STATE)
    before = core.sha(ROOT / core.STATE)
    assert state['execution_runtime']['active'] is None and work.OP in state['execution_program']['results']
    assert state['reader']['path'] == str(build.OLD.with_suffix('.pdf').relative_to(ROOT))
    status = state['reader']['status']
    assert status == 'Working monograph; not I02 acceptance'
    report, audit, reviewed = read(OUT / 'build-report.json'), read(OUT / 'source-audit.json'), read(BASE / 'release-source-review.json')
    verify_bindings(reviewed)
    manifest = {'kind': 'working_monograph', 'final_acceptance': False,
        'pdf': report['pdf'], 'pages': report['pages'],
        'supersedes': {key: state['reader'][key] for key in ['path', 'sha256']},
        'build_report': ref(OUT / 'build-report.json', 'Preserving temporal comparison reader'),
        'source_review': ref(BASE / 'release-source-review.json', 'Exact-reader author review'),
        'text_layout': ref(OUT / 'text-layout-review.json', 'All-page text bounds'),
        'source_artifacts': audit['tex_files'] + reviewed['evidence'],
        'visual_acceptance': False, 'mandatory_repairs_closed': [],
        'changes': ['Integrate six temporal software families, two new genuine papers and forty pinned originals.',
            'Explain predictive, structural, surgical and changing-mechanism targets through six exact authored families.',
            'Specify reuse choices, concrete omissions and staged public/generated prototype before expensive bank validation.'],
        'sponsor_binding': 'Preserved sponsor baseline; Q5 reconciliation remains open.'}
    write(BASE / 'working-release.json', manifest)
    binding = ref(BASE / 'working-release.json', 'Reviewed temporal comparison working successor')
    run.ledger.validate_working_release(ROOT, binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader'] = {key: report['pdf'][key] for key in ['path', 'sha256']}
    state['reader'].update(pages=report['pages'], status=status)
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT, before, state, {'action': 'publish_other_temporal_reader',
        'manifest': binding, 'final_acceptance': False})
    print(json.dumps({'published': state['reader']}))


def renew():
    report = read(OUT / 'build-report.json')
    verify_bindings(read(BASE / 'release-source-review.json'))
    findings = {
        'Q2': 'All 686 inherited source records, compiled sources and citation contexts remain. Ten additions bind forty pinned originals, three inherited license originals, two new genuine papers, authored mathematics and the proposed contract. All 696 records and 187 scholarly PDFs pass traceability; incomplete coverage, rights and code paths remain explicit.',
        'Q3': 'Six exact authored families reproduce common-calendar information without effects, structural VAR conversion and propagation, unit-dependent flags, exchangeable ranks, supplied-model observational equivalence and opposing eras. Separate atom enumeration and scalar recurrences verify arithmetic. No upstream runtime, general temporal calibration or bank truth is claimed.',
        'Q4': 'Stipulated spurious USD25/account and USD109.375 innovation responses motivate preserving causal target, physical clock and units. The proposed generated then permitted-public comparison includes preparation, licensing, failures, review, hardware and maintenance. Expensive bank validation follows prototype merit; runtime advantage, actual prices and bank ROI remain unknown.'}
    for question, finding in findings.items():
        identifier = 'PROPOSAL.' + question
        state = core.read(ROOT, core.STATE)
        assert state['reader']['sha256'] == report['pdf']['sha256']
        previous = state['execution_runtime']['results'][identifier]
        old = read(ROOT / previous['path'])
        folder = BASE / question
        folder.mkdir(exist_ok=False)
        evidence = [previous, ref(BASE / 'working-release.json', 'Exact current reader'),
            ref(BASE / 'release-source-review.json', 'Inspected temporal comparison delta'),
            ref(work.OUTPUT, 'Bounded coverage review'),
            ref(WORK / 'arithmetic-review.json', 'Alternative exact verification'),
            ref(WORK / 'proposed-contract.json', 'Proposed staged comparison and full costs'),
            ref(Path(__file__), 'Question-specific review findings')]
        write(folder / 'reopen.json', {'reason': 'Changed reader requires a preserved successor author review.',
            'prior_result': previous, 'reviewed_reader': report['pdf'], 'evidence': evidence,
            'next_action': 'Record reviewed temporal comparison delta with preserved scope and limits.'})
        transition('reopen', identifier, folder / 'reopen.json')
        state = core.read(ROOT, core.STATE)
        graph, _, _ = run.combined(ROOT, state)
        node = run.ledger.operation(graph, identifier)
        attempt = len(state['execution_runtime']['review_history'][identifier])
        output = ROOT / run.review_output_paths(node, state['reader'], attempt)[0]
        limits = list(dict.fromkeys(old['limitations'] + work.LIMITS))
        scope = 'Author exact-reader proposal delta review'
        write(output, {'operation': identifier, 'status': 'pass', 'criterion': node['criteria'][0],
            'reviewer': work.REVIEWER, 'reviewed_reader': report['pdf'], 'review_attempt': attempt,
            'acceptance_scope': 'proposal_only', 'scope': scope, 'findings': [finding],
            'evidence': evidence, 'limitations': limits, 'visual_acceptance': False})
        receipt = run.ledger.receipt_template(node)
        receipt.update(outcome='pass', execution='performed', scope=scope, reviewer=work.REVIEWER,
            limitations=limits, reviewed_reader=report['pdf'], review_attempt=attempt,
            acceptance_scope='proposal_only', outputs=[ref(output, 'Current-reader ' + question + ' author review')],
            nonexecution_reason='', revisit_trigger='',
            criteria=[{'index': 0, 'verdict': 'pass', 'finding': finding, 'evidence': evidence}])
        write(folder / 'operation-receipt.json', receipt)
        transition('record', identifier, folder / 'operation-receipt.json')
    print(json.dumps({'exact_reader_reviews': 'Q2-Q4 pass', 'Q1_Q5': 'open'}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['review', 'record', 'publish', 'renew'])
    args = parser.parse_args()
    {'review': review, 'record': record, 'publish': publish, 'renew': renew}[args.command]()
