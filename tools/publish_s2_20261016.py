#!/usr/bin/env python3
"""Record and publish reviewed discovery synthesis without changing frozen evidence."""
import argparse
import json
from pathlib import Path

import build_s2_reader_v2_20261016 as build
import prepare_s2_v2_20261016 as work
import review_s2_20261016 as review
import master_control as core
import run_program as run
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

ROOT, BASE, OUT = build.ROOT, build.BASE, build.OUT


def read(path):
    return json.loads(path.read_text())


def verify():
    report = read(OUT / 'build-report.json')
    for path in [OUT / 'build-report.json', BASE / 'release-source-review.json',
                 BASE / 'draft-operation-receipt.json', BASE / 'review-operation-receipt.json', review.REVIEW]:
        verify_bindings(read(path))
    measured = read(review.REVIEW)
    assert report['pages'] == 845 and report['cited_records'] == 660
    assert measured['status'] == 'pass' and measured['substantive_page_credit'] == 16.5
    assert measured['allocation_minimum_met'] and not measured['planning_target_met']
    assert work.examples.calculate() == read(work.BASE / 'exact-results.json')
    assert read(OUT / 'text-layout-review.json')['status'] == 'pass'
    return report


def record():
    verify()
    for identifier, name in [('TEXT.DRAFT.S2', 'draft-operation-receipt.json'), ('TEXT.REVIEW.S2', 'review-operation-receipt.json')]:
        state = core.read(ROOT, core.STATE)
        if identifier in state['execution_program']['results']:
            assert state['execution_program']['results'][identifier]['sha256'] == core.sha(BASE / name)
            continue
        transition('record', identifier, BASE / name)


def publish():
    report = verify(); state = core.read(ROOT, core.STATE); before = core.sha(ROOT / core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path'] == str(build.OLD.with_suffix('.pdf').relative_to(ROOT))
    assert all(k in state['execution_program']['results'] for k in ['TEXT.DRAFT.S2', 'TEXT.REVIEW.S2'])
    audit = read(OUT / 'source-audit.json'); reviewed = read(BASE / 'release-source-review.json')
    manifest = {
        'kind': 'working_monograph', 'final_acceptance': False, 'pdf': report['pdf'], 'pages': report['pages'],
        'supersedes': {k: state['reader'][k] for k in ['path', 'sha256']},
        'build_report': ref(OUT / 'build-report.json', 'Preserving 845-page discovery reader'),
        'source_review': ref(BASE / 'release-source-review.json', 'Author source, math and exclusive chapter-depth review'),
        'text_layout': ref(OUT / 'text-layout-review.json', 'All-page text bounds'),
        'source_artifacts': audit['tex_files'] + reviewed['evidence'] + [
            ref(review.REVIEW, '16.5 nonduplicate substantive pages; target 20 not met'), ref(Path(__file__), 'Publication and review procedure')],
        'visual_acceptance': False, 'mandatory_repairs_closed': [],
        'changes': ['Connect independent, latent, temporal and experimental discovery to banking decisions.',
                    'Derive exact cancellation, observational equivalence, intervention-information, selection and horizon examples.',
                    'Review distributed S2 subject depth without duplicate credit or closing the broader software census.'],
        'sponsor_binding': 'Preserved sponsor baseline; Q5 reconciliation remains open.'}
    write(BASE / 'working-release.json', manifest); binding = ref(BASE / 'working-release.json', 'Reviewed S2 working successor')
    run.ledger.validate_working_release(ROOT, binding); state['execution_program']['working_releases'].append(binding)
    state['reader'] = {k: report['pdf'][k] for k in ['path', 'sha256']}
    state['reader'].update(pages=report['pages'], status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT, before, state, {'action': 'publish_s2_reader', 'manifest': binding, 'final_acceptance': False})
    print(json.dumps({'published': state['reader'], 'proposal_accepted': False}))


def renew():
    report = verify()
    findings = {
        'Q2': '658 inherited source records, compiled content and citation contexts remain; two project additions yield 660 records and 175 genuine scholarly PDFs. Four genuine primary-paper rereads, four software excerpts and 29 inherited keys support the synthesis.',
        'Q3': 'Exact rational matrix algebra and separate paths reproduce three identical observational Gaussian laws with effects {0,1}. Direct intervention substitutions, selection enumeration, cancellation and impulse arithmetic agree. No new upstream trial, universal discovery guarantee or graph-confidence region inferred.',
        'Q4': 'Stipulated offer values 22/-8/-8 USD imply different maximin and minimax-regret actions; stipulated equal scenario weights give current value 2 and ideal information improvements 16/3 or 8/3 USD. Average and endpoint responses give 7 versus -23 USD. These are generated decision illustrations, not trial budgets or bank ROI.'}
    for q, finding in findings.items():
        identifier = 'PROPOSAL.' + q; state = core.read(ROOT, core.STATE)
        assert state['reader']['sha256'] == report['pdf']['sha256']
        previous = state['execution_runtime']['results'][identifier]; old = read(ROOT / previous['path'])
        if run.same_reader(old.get('reviewed_reader', {}), report['pdf']):
            assert old['outcome'] == 'pass'
            continue
        folder = BASE / q; folder.mkdir(exist_ok=False)
        evidence = [previous, ref(BASE / 'working-release.json', 'Exact current reader'),
                    ref(BASE / 'release-source-review.json', 'Author source/math review'),
                    ref(review.REVIEW, 'S2 exclusive topic/depth review'),
                    ref(work.BASE / 'exact-results.json', 'Exact authored reference families'),
                    ref(Path(__file__), 'Exact-reader findings')]
        write(folder / 'reopen.json', {
            'reason': 'Changed reader requires preserved successor author review.', 'prior_result': previous,
            'reviewed_reader': report['pdf'], 'evidence': evidence,
            'next_action': 'Record scoped S2 source, mathematics and decision delta.'})
        transition('reopen', identifier, folder / 'reopen.json')
        state = core.read(ROOT, core.STATE); graph, _, _ = run.combined(ROOT, state); node = run.ledger.operation(graph, identifier)
        attempt = len(state['execution_runtime']['review_history'][identifier])
        output = ROOT / run.review_output_paths(node, state['reader'], attempt)[0]
        limits = list(dict.fromkeys(old['limitations'] + review.LIMITS)); scope = 'Author exact-reader delta review; proposal evidence only'
        write(output, {'operation': identifier, 'status': 'pass', 'criterion': node['criteria'][0], 'reviewer': work.REVIEWER,
                       'reviewed_reader': report['pdf'], 'review_attempt': attempt, 'acceptance_scope': 'proposal_only',
                       'scope': scope, 'findings': [finding], 'evidence': evidence, 'limitations': limits, 'visual_acceptance': False})
        receipt = run.ledger.receipt_template(node)
        receipt.update(outcome='pass', execution='performed', scope=scope, reviewer=work.REVIEWER, limitations=limits,
                       reviewed_reader=report['pdf'], review_attempt=attempt, acceptance_scope='proposal_only',
                       outputs=[ref(output, 'Current-reader ' + q + ' author review')], nonexecution_reason='', revisit_trigger='',
                       criteria=[{'index': 0, 'verdict': 'pass', 'finding': finding, 'evidence': evidence}])
        write(folder / 'operation-receipt.json', receipt); transition('record', identifier, folder / 'operation-receipt.json')
    print(json.dumps({'exact_reader_reviews': 'Q2-Q4 pass', 'Q1_Q5': 'open', 'proposal_accepted': False}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('command', choices=['record', 'publish', 'renew'])
    args = parser.parse_args(); {'record': record, 'publish': publish, 'renew': renew}[args.command]()
