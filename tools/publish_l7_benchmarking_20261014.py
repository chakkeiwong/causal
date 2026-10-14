#!/usr/bin/env python3
"""Publish the already reviewed L7 successor and preserve exact-reader reviews."""
import argparse
import json
from pathlib import Path

import build_l7_benchmarking_v3_20261014 as build
import develop_l7_benchmarking_20261014 as work
import review_l7_benchmarking_v2_20261014 as review
import review_l7_frontier_20261014 as frontier
import master_control as core
import run_program as run
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

ROOT, BASE, OUT = build.ROOT, build.BASE, build.OUT


def verify():
    report = json.loads((OUT / 'build-report.json').read_text())
    for path in [OUT / 'build-report.json', BASE / 'release-source-review.json',
                 BASE / 'draft-operation-receipt.json', BASE / 'review-operation-receipt.json',
                 review.REVIEW]:
        verify_bindings(json.loads(path.read_text()))
    assert report['pages'] == 756 and report['cited_records'] == 573
    assert work.calculate() == json.loads((work.BASE / 'exact-results.json').read_text())
    assert frontier.exact() == json.loads((frontier.BASE / 'exact-results.json').read_text())
    measured = json.loads(review.REVIEW.read_text())
    assert measured['status'] == 'pass' and measured['substantive_page_credit'] == 12
    assert json.loads((OUT / 'text-layout-review.json').read_text())['status'] == 'pass'
    return report


def record():
    verify()
    for identifier, filename in [('TEXT.DRAFT.L7', 'draft-operation-receipt-controller.json'),
                                 ('TEXT.REVIEW.L7', 'review-operation-receipt.json')]:
        state = core.read(ROOT, core.STATE)
        if identifier in state['execution_program']['results']:
            assert state['execution_program']['results'][identifier]['sha256'] == core.sha(BASE / filename)
            continue
        transition('record', identifier, BASE / filename)


def publish():
    report = verify()
    state = core.read(ROOT, core.STATE)
    before = core.sha(ROOT / core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path'] == str(build.OLD.with_suffix('.pdf').relative_to(ROOT))
    assert all(k in state['execution_program']['results'] for k in ['TEXT.DRAFT.L7', 'TEXT.REVIEW.L7'])
    audit = json.loads((OUT / 'source-audit.json').read_text())
    reviewed = json.loads((BASE / 'release-source-review.json').read_text())
    manifest = {
        'kind': 'working_monograph', 'final_acceptance': False,
        'pdf': report['pdf'], 'pages': report['pages'],
        'supersedes': {k: state['reader'][k] for k in ['path', 'sha256']},
        'build_report': ref(OUT / 'build-report.json', 'Preserving 756-page benchmarking reader'),
        'source_review': ref(BASE / 'release-source-review.json', 'Author source, derivation and chapter review'),
        'text_layout': ref(OUT / 'text-layout-review.json', 'All-page extraction and text bounds'),
        'source_artifacts': audit['tex_files'] + reviewed['evidence'] + [
            ref(review.REVIEW, 'Twelve nonduplicate substantive pages across 21 physical pages'),
            ref(BASE / 'receipt-contract-repair.json', 'Preserved rejected receipt and schema repair'),
            ref(Path(__file__).resolve(), 'Recovery, exact reproduction and publication procedure')],
        'visual_acceptance': False, 'mandatory_repairs_closed': [],
        'changes': [
            'Develop exposure sensitivity, selective adjudication and consistent-but-wrong rules.',
            'Compare two newly inspected benchmark originals with explicit conditional reuse.',
            'Record allocated L7 topic/depth completion and preserve wider census and runtime gaps.'],
        'sponsor_binding': 'Preserved sponsor baseline; Q5 reconciliation remains open.'}
    write(BASE / 'working-release.json', manifest)
    binding = ref(BASE / 'working-release.json', 'Reviewed L7 working successor')
    run.ledger.validate_working_release(ROOT, binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader'] = {k: report['pdf'][k] for k in ['path', 'sha256']}
    state['reader'].update(pages=report['pages'], status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT, before, state, {
        'action': 'publish_l7_benchmarking_reader', 'manifest': binding, 'final_acceptance': False})
    print(json.dumps({'published': state['reader'], 'proposal_accepted': False}))


def renew():
    report = verify()
    findings = {
        'Q2': 'All 568 inherited source records and 1,592 inherited citation uses are preserved; two deterministic punctuation replacements retain their scientific text. Five added records yield 573 citations and 162 genuine scholarly PDFs. New benchmark claims are bound to inspected originals; broader census and artifact qualification remain open.',
        'Q3': 'The inherited demonstration portfolio is unchanged. Exact exposure-mixture allocations, eight probability-audit outcomes, wrong-but-consistent rules and benchmark score/threshold arithmetic reproduce. These are exposed project constructions and source comparisons, not fresh live-model evaluations or upstream benchmark executions.',
        'Q4': 'The inherited investment argument is preserved. New examples explain how exposure, selective adjudication and oracle errors can reverse a comparison or miss a stipulated USD 60 consequence. A low-cost public/generated reference and probability audit precede costly experiments. Assumed costs and truthful-label conditions remain explicit; no bank ROI or current vendor pricing is asserted.'}
    for q, finding in findings.items():
        identifier = 'PROPOSAL.' + q
        state = core.read(ROOT, core.STATE)
        assert state['reader']['sha256'] == report['pdf']['sha256']
        previous = state['execution_runtime']['results'][identifier]
        old = json.loads((ROOT / previous['path']).read_text())
        if run.same_reader(old.get('reviewed_reader', {}), report['pdf']):
            assert old['outcome'] == 'pass'
            continue
        folder = BASE / q
        folder.mkdir(exist_ok=False)
        evidence = [previous, ref(BASE / 'working-release.json', 'Exact current working reader'),
                    ref(BASE / 'release-source-review.json', 'Source and derivation review'),
                    ref(review.REVIEW, 'Scoped L7 topic/depth review'),
                    ref(work.BASE / 'exact-results.json', 'Exact development constructions'),
                    ref(frontier.BASE / 'primary-review.json', 'Two primary benchmark papers'),
                    ref(frontier.BASE / 'exact-results.json', 'Score and threshold calculations'),
                    ref(Path(__file__).resolve(), 'Exact-reader author review findings')]
        write(folder / 'reopen.json', {
            'reason': 'Changed reader requires a preserved successor review.',
            'prior_result': previous, 'reviewed_reader': report['pdf'], 'evidence': evidence,
            'next_action': 'Record the reviewed L7 source, demonstration and economic delta.'})
        transition('reopen', identifier, folder / 'reopen.json')
        state = core.read(ROOT, core.STATE)
        graph, _, _ = run.combined(ROOT, state)
        node = run.ledger.operation(graph, identifier)
        attempt = len(state['execution_runtime']['review_history'][identifier])
        output = ROOT / run.review_output_paths(node, state['reader'], attempt)[0]
        limits = list(dict.fromkeys(old['limitations'] + review.LIMITS))
        scope = 'Author exact-reader delta review; proposal evidence only'
        write(output, {
            'operation': identifier, 'status': 'pass', 'criterion': node['criteria'][0],
            'reviewer': review.REVIEWER, 'reviewed_reader': report['pdf'], 'review_attempt': attempt,
            'acceptance_scope': 'proposal_only', 'scope': scope, 'findings': [finding],
            'evidence': evidence, 'limitations': limits, 'visual_acceptance': False})
        receipt = run.ledger.receipt_template(node)
        receipt.update(
            outcome='pass', execution='performed', scope=scope, reviewer=review.REVIEWER,
            limitations=limits, reviewed_reader=report['pdf'], review_attempt=attempt,
            acceptance_scope='proposal_only', outputs=[ref(output, 'Current-reader ' + q + ' author review')],
            nonexecution_reason='', revisit_trigger='',
            criteria=[{'index': 0, 'verdict': 'pass', 'finding': finding, 'evidence': evidence}])
        write(folder / 'operation-receipt.json', receipt)
        transition('record', identifier, folder / 'operation-receipt.json')
    print(json.dumps({'exact_reader_reviews': 'Q2-Q4 pass', 'Q1_Q5': 'open', 'proposal_accepted': False}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['record', 'publish', 'renew'])
    args = parser.parse_args()
    {'record': record, 'publish': publish, 'renew': renew}[args.command]()
