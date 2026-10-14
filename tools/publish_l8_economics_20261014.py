#!/usr/bin/env python3
"""Publish the reviewed economics successor and renew exact-reader reviews."""
import argparse
import json
from pathlib import Path

import build_l8_economics_v3_20261014 as build
import build_l8_economics_20261014 as work
import l8_economics_examples_20261014 as examples
import review_l8_economics_20261014 as review
import master_control as core
import run_program as run
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

ROOT, BASE, OUT = build.ROOT, build.BASE, build.OUT


def verify():
    report = json.loads((OUT / 'build-report.json').read_text())
    for path in [OUT / 'build-report.json', BASE / 'release-source-review.json',
                 BASE / 'draft-operation-receipt.json', BASE / 'review-operation-receipt.json', review.REVIEW]:
        verify_bindings(json.loads(path.read_text()))
    assert report['pages'] == 780 and report['cited_records'] == 603
    assert examples.calculate() == json.loads((work.BASE / 'exact-results.json').read_text())
    measured = json.loads(review.REVIEW.read_text())
    assert measured['status'] == 'pass' and measured['substantive_page_credit'] == 6.5
    assert measured['allocation_minimum_met'] and not measured['planning_target_met']
    assert json.loads((OUT / 'text-layout-review.json').read_text())['status'] == 'pass'
    return report


def record():
    verify()
    for identifier, filename in [('TEXT.DRAFT.L8', 'draft-operation-receipt.json'),
                                 ('TEXT.REVIEW.L8', 'review-operation-receipt.json')]:
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
    assert all(k in state['execution_program']['results'] for k in ['TEXT.DRAFT.L8', 'TEXT.REVIEW.L8'])
    audit = json.loads((OUT / 'source-audit.json').read_text())
    reviewed = json.loads((BASE / 'release-source-review.json').read_text())
    manifest = {
        'kind': 'working_monograph', 'final_acceptance': False,
        'pdf': report['pdf'], 'pages': report['pages'],
        'supersedes': {k: state['reader'][k] for k in ['path', 'sha256']},
        'build_report': ref(OUT / 'build-report.json', 'Preserving 780-page economics reader'),
        'source_review': ref(BASE / 'release-source-review.json', 'Author source, mathematics and chapter-depth review'),
        'text_layout': ref(OUT / 'text-layout-review.json', 'All-page extraction and text bounds'),
        'source_artifacts': audit['tex_files'] + reviewed['evidence'] + [
            ref(review.REVIEW, '6.5 nonduplicate pages meeting the six-page minimum'),
            ref(Path(__file__).resolve(), 'Exact-reader publication and review procedure')],
        'visual_acceptance': False, 'mandatory_repairs_closed': [],
        'changes': [
            'Develop request-level loss, calibrated review thresholds and dependent retry costs.',
            'Derive ambiguity/regret choices, joint policy value and delayed prototype investment options.',
            'Explain deployment-mixture sensitivity and independent banking prototype routes with later authentic evidence.',
            'Preserve both earlier candidates and repair citation fragments, spacing and break-even wording.'],
        'sponsor_binding': 'Preserved sponsor baseline; Q5 reconciliation remains open.'}
    write(BASE / 'working-release.json', manifest)
    binding = ref(BASE / 'working-release.json', 'Reviewed L8 working successor')
    run.ledger.validate_working_release(ROOT, binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader'] = {k: report['pdf'][k] for k in ['path', 'sha256']}
    state['reader'].update(pages=report['pages'], status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT, before, state, {'action': 'publish_l8_economics_reader', 'manifest': binding, 'final_acceptance': False})
    print(json.dumps({'published': state['reader'], 'proposal_accepted': False}))


def renew():
    report = verify()
    findings = {
        'Q2': 'All 601 inherited source records and citation uses remain through deterministic successor mappings. Two project records yield 603 citations and 172 genuine scholarly PDFs. Three primary rereads retain the original populations and protocols. Citation fragments and equality wording are repaired without changing equations or results.',
        'Q3': 'The inherited demonstrated portfolio remains unchanged. Seven exact project scenario groups reproduce, including independent full-path retry enumeration. Loss routing, ambiguity/regret, joint-policy values, delayed investment and deployment mix are stipulated constructions, not live service or bank performance. Four-journey evidence retains all 420 requests, 416 frozen matches and 103 semantic comparisons, including four incorrect frozen servicing expectations.',
        'Q4': 'The chapter now derives full requested-case loss and costs, review thresholds, dependent retry burdens, robust/regret decisions, joint policy information, pilot stopping and delay, and deployment-mixture reversal. The pilot example compares USD20600 against the existing USD20000 build option. All losses, costs and signal probabilities are stipulated. Public/generated prototypes precede costly authentic experiments; empirical prices, bank value and universal scientific claims remain unawarded.'}
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
        evidence = [previous, ref(BASE / 'working-release.json', 'Exact current reader'),
                    ref(BASE / 'release-source-review.json', 'Source and mathematical review'),
                    ref(review.REVIEW, 'L8 topic/depth review'),
                    ref(work.BASE / 'exact-results.json', 'Seven scenario groups'),
                    ref(work.BASE / 'primary-review.json', 'Three genuine primary rereads'),
                    ref(ROOT / 'docs/program/execution/2026-10-14/four-journeys/reconciliation.json', 'Preserved four-journey findings'),
                    ref(Path(__file__).resolve(), 'Exact-reader author review findings')]
        write(folder / 'reopen.json', {
            'reason': 'Changed reader requires a preserved successor review.',
            'prior_result': previous, 'reviewed_reader': report['pdf'], 'evidence': evidence,
            'next_action': 'Record reviewed economics source, demonstration and investment delta.'})
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
        receipt.update(outcome='pass', execution='performed', scope=scope, reviewer=review.REVIEWER,
                       limitations=limits, reviewed_reader=report['pdf'], review_attempt=attempt,
                       acceptance_scope='proposal_only', outputs=[ref(output, 'Current-reader '+q+' author review')],
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
