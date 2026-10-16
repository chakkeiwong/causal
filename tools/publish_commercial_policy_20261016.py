#!/usr/bin/env python3
"""Review and publish a preserving, bounded commercial policy comparison."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
import build_commercial_policy_reader_20261016 as build
import prepare_commercial_policy_20261016 as work
import master_control as core
import run_program as run
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

ROOT, BASE, OUT, WORK = build.ROOT, build.BASE, build.OUT, build.WORK
OUTPUT = ROOT / 'docs/program/comprehensive-v14/work' / work.OP / 'coverage-review.json'
FINDINGS = [
    'Eleven named families and their aliases, six irrelevant inherited scholarly hits, ten initial routes and four alternate routes are retained. Search breadth, unavailable originals and exact historical editions prevent a complete market-coverage finding.',
    'Six original official pages, inherited audited technical manuals and the genuine Jiang/Li PDF support only the stated technical claims. Hashes, versions, inspected anchors, later-acquisition limits, exact generated references and actual local refusal observations are bound.',
    'The comparison identifies static, sequential, adapting-learner, predictive and supplied-model alternatives. Source-specific omissions, acquisition routes, commercial rights, prototype steps and unresolved science are explicit; no vendor absence is inferred from failed acquisition.']


def read(path):
    return json.loads(path.read_text())


def review():
    report = read(OUT / 'build-report.json'); audit = read(OUT / 'source-audit.json')
    prior = read(build.PRIOR); index = read(BASE / 'traceability-review.json')
    for obj in [report, audit, prior, index, read(BASE / 'prepared-inputs.json'), read(WORK / 'author-review.json')]:
        verify_bindings(obj)
    assert index['status'] == 'pass' and not index['issues'] and index['scholarly_pdfs'] == 175
    layout = read(OUT / 'text-layout-review.json')
    assert layout['status'] == 'pass' and not layout['out_of_bounds'] and not layout['empty_pages']
    assert not [w for w in report['warnings'] if 'Underfull' not in w]
    assert build.DRIVER.read_text() == build.expected_driver()
    old = {s['integrated_citation_key']: s for s in prior['sources']}
    new = {s['integrated_citation_key']: s for s in audit['sources']}
    assert len(old) == 660 and len(new) == 666 and all(new[k] == s for k, s in old.items())
    files = {r['path']: r for r in audit['tex_files']}
    kept = [r for r in prior['tex_files'] if r['path'] != str(build.OLD.relative_to(ROOT))]
    assert all(files[r['path']]['sha256'] == r['sha256'] for r in kept)
    previous = read(build.PRIOR.parent.parent / 'traceability-review.json')
    contexts = {r['citation_key']: Counter(json.dumps(x, sort_keys=True) for x in r['citation_contexts']) for r in index['records']}
    for row in previous['records']:
        assert not Counter(json.dumps(x, sort_keys=True) for x in row['citation_contexts']) - contexts[row['citation_key']]
    text = re.sub(r'-\s+', '-', ' '.join((OUT / 'reader.txt').read_text().split()))
    for phrase in ['Commercial policy evaluation: what an offline score permits', '42.5', '84.5',
                   '50,000', '25 August 2026', 'microsoft/learning-loop', 'average_rewards_at_k',
                   '127/32', 'indexing parents', 'eleven named families', 'no absence']:
        assert phrase.lower() in text.lower(), phrase
    assert work.examples.calculate() == read(WORK / 'exact-results.json')
    probe = read(WORK / 'local-probe.json'); verify_bindings(probe)
    assert len(probe['policy_method_probes']) == 3
    assert all(x['response']['disposition'] == 'unsupported' and x['response']['result'] is None for x in probe['policy_method_probes'])
    evidence = [ref(p, a) for p, a in [
        (OUT / 'build-report.json', 'Preserving commercial policy reader'), (OUT / 'source-audit.json', '666 source records'),
        (BASE / 'traceability-review.json', '175 genuine scholarly PDFs and preserved citation contexts'),
        (OUT / 'text-layout-review.json', 'All-page text bounds'), (OUT / 'reader.txt', 'Inspected integrated text'),
        (WORK / 'primary-review.json', 'Six official originals, inherited manuals and genuine primary paper'),
        (WORK / 'search-ledger.json', 'Bounded portfolio and all inherited query leads'),
        (WORK / 'omissions-register.json', 'Open sources, editions, rights and scientific questions'),
        (WORK / 'comparison-design.json', 'Source-specific choices and concrete public/generated prototype'),
        (WORK / 'exact-results.json', 'Four reproduced exact generated families'),
        (WORK / 'local-probe.json', 'Actual three local common-service refusals'),
        (WORK / 'author-review.json', 'Bounded author review'), (Path(__file__), 'Exact-reader review and transitions')]]
    write(OUTPUT, {'operation': work.OP, 'outcome': 'inconclusive', 'reviewer': work.REVIEWER,
        'scope': 'Bounded commercial policy comparison for a research/product proposal',
        'criteria_verdicts': ['inconclusive', 'pass', 'pass'], 'findings': FINDINGS,
        'evidence': evidence, 'limitations': work.LIMITS, 'whole_census_closed': False,
        'mandatory_repairs_closed': [], 'vendor_execution': False, 'visual_acceptance': False,
        'next_action': 'Broaden named-family and long-tail search; acquire exact-edition missing originals and rights. Select a matched public/generated prototype; keep hidden-state, dependent and selected-policy uncertainty scoped.'})
    write(BASE / 'release-source-review.json', {'status': 'pass', 'issues': [], 'reviewer': work.REVIEWER,
        'reviewed_reader': report['pdf'], 'scope': 'Author source, exact mathematics, saved local observation and extracted-text review',
        'coverage_outcome': 'inconclusive', 'preserved_records': 660, 'new_records': 6,
        'preserved_compiled_sources': len(kept), 'original_contexts_retained': True,
        'evidence': evidence + [ref(OUTPUT, 'Contracted bounded coverage verdict')],
        'findings': FINDINGS + ['Existing Stata policy value is recognized; Azure retirement is distinguished from a successor lead; recommendation metrics and model optimization do not establish sequential causal value.',
            'Exact examples establish only their generated laws. Local service refusals are distinct from research-module availability and vendor execution.'],
        'limitations': work.LIMITS, 'visual_acceptance': False})
    print(json.dumps({'review': 'pass', 'coverage': 'inconclusive', 'pages': report['pages'], 'sections': report['commercial_policy_sections']}))


def record():
    verify_bindings(read(BASE / 'release-source-review.json'))
    state = core.read(ROOT, core.STATE); graph, _, _ = run.combined(ROOT, state); node = run.ledger.operation(graph, work.OP)
    receipt = run.ledger.receipt_template(node)
    receipt.update(outcome='inconclusive', execution='performed', scope='Bounded proposal comparison; not commercial market-census closure',
        reviewer=work.REVIEWER, limitations=work.LIMITS, capabilities=[], outputs=[ref(OUTPUT, 'Reviewed commercial coverage contract')],
        nonexecution_reason='', revisit_trigger='Broader bounded candidate search, accessible exact-edition originals and a matched prototype requiring a commercial comparison.',
        criteria=[{'index': i, 'verdict': verdict, 'finding': finding,
                   'evidence': [ref(OUTPUT, 'Criterion review'), ref(BASE / 'release-source-review.json', 'Preserving integration')]}
                  for i, (verdict, finding) in enumerate(zip(['inconclusive', 'pass', 'pass'], FINDINGS))])
    write(BASE / 'operation-receipt.json', receipt); transition('record', work.OP, BASE / 'operation-receipt.json')


def publish():
    state = core.read(ROOT, core.STATE); before = core.sha(ROOT / core.STATE)
    assert state['execution_runtime']['active'] is None and work.OP in state['execution_program']['results']
    assert state['reader']['path'] == str(build.OLD.with_suffix('.pdf').relative_to(ROOT))
    status = state['reader']['status']; assert status == 'Working monograph; not I02 acceptance'
    report = read(OUT / 'build-report.json'); audit = read(OUT / 'source-audit.json')
    reviewed = read(BASE / 'release-source-review.json'); verify_bindings(reviewed)
    manifest = {'kind': 'working_monograph', 'final_acceptance': False, 'pdf': report['pdf'], 'pages': report['pages'],
        'supersedes': {k: state['reader'][k] for k in ['path', 'sha256']},
        'build_report': ref(OUT / 'build-report.json', 'Preserving commercial policy reader'),
        'source_review': ref(BASE / 'release-source-review.json', 'Exact-reader author review'),
        'text_layout': ref(OUT / 'text-layout-review.json', 'All-page bounds'),
        'source_artifacts': audit['tex_files'] + reviewed['evidence'], 'visual_acceptance': False, 'mandatory_repairs_closed': [],
        'changes': ['Integrate eleven-family commercial policy comparison and four exact banking reference families.',
                    'Recognize existing static and supplied-model capabilities; specify sequential, selection, rights and acquisition gaps.'],
        'sponsor_binding': 'Preserved sponsor baseline; Q5 reconciliation remains open.'}
    write(BASE / 'working-release.json', manifest); binding = ref(BASE / 'working-release.json', 'Reviewed commercial policy working successor')
    run.ledger.validate_working_release(ROOT, binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader'] = {k: report['pdf'][k] for k in ['path', 'sha256']}
    state['reader'].update(pages=report['pages'], status=status); state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT, before, state, {'action': 'publish_commercial_policy_reader', 'manifest': binding, 'final_acceptance': False})
    print(json.dumps({'published': state['reader']}))


def renew():
    report = read(OUT / 'build-report.json'); verify_bindings(read(BASE / 'release-source-review.json'))
    findings = {
        'Q2': 'All 660 inherited citation records, contexts and compiled sources remain. Six additions bind six official originals, four exact generated reference families, local dispatcher observations and the proposed comparison. The 666-record reader has 175 genuine scholarly PDFs. Unknown historical editions, inaccessible originals and bounded census coverage remain explicit.',
        'Q3': 'Four finite generated reference families reproduce by exact enumeration and separate structural/closed-form calculations. Saved schema-valid requests establish three local common-service refusals only. No vendor, separate policy research module, live model or bank study was executed in this increment; proposed prototype behavior is labeled.',
        'Q4': 'The preserved investment scenarios gain explicit target-versus-estimator, selection and capacity examples with stipulated money. A public/generated matched prototype precedes any licensed comparison, with preparation, rights, conversion, diagnostics, review and maintenance costs included. No actual vendor price, bank ROI or qualified optimal policy is claimed.'}
    for q, finding in findings.items():
        identifier = 'PROPOSAL.' + q; state = core.read(ROOT, core.STATE)
        assert state['reader']['sha256'] == report['pdf']['sha256']
        previous = state['execution_runtime']['results'][identifier]; old = read(ROOT / previous['path'])
        folder = BASE / q; folder.mkdir(exist_ok=False)
        evidence = [previous, ref(BASE / 'working-release.json', 'Exact current reader'),
                    ref(BASE / 'release-source-review.json', 'Inspected preserving delta'), ref(OUTPUT, 'Bounded coverage verdict'),
                    ref(WORK / 'comparison-design.json', 'Concrete prototype and full-cost categories'), ref(Path(__file__), 'Review findings')]
        write(folder / 'reopen.json', {'reason': 'Changed reader requires preserved successor author review.',
            'prior_result': previous, 'reviewed_reader': report['pdf'], 'evidence': evidence,
            'next_action': 'Record reviewed commercial policy delta with preserved evidence and explicit scope limits.'})
        transition('reopen', identifier, folder / 'reopen.json')
        state = core.read(ROOT, core.STATE); graph, _, _ = run.combined(ROOT, state); node = run.ledger.operation(graph, identifier)
        attempt = len(state['execution_runtime']['review_history'][identifier]); output = ROOT / run.review_output_paths(node, state['reader'], attempt)[0]
        limits = list(dict.fromkeys(old['limitations'] + work.LIMITS)); scope = 'Author exact-reader proposal delta review'
        write(output, {'operation': identifier, 'status': 'pass', 'criterion': node['criteria'][0], 'reviewer': work.REVIEWER,
            'reviewed_reader': report['pdf'], 'review_attempt': attempt, 'acceptance_scope': 'proposal_only', 'scope': scope,
            'findings': [finding], 'evidence': evidence, 'limitations': limits, 'visual_acceptance': False})
        receipt = run.ledger.receipt_template(node)
        receipt.update(outcome='pass', execution='performed', scope=scope, reviewer=work.REVIEWER, limitations=limits,
            reviewed_reader=report['pdf'], review_attempt=attempt, acceptance_scope='proposal_only',
            outputs=[ref(output, 'Current-reader ' + q + ' author review')], nonexecution_reason='', revisit_trigger='',
            criteria=[{'index': 0, 'verdict': 'pass', 'finding': finding, 'evidence': evidence}])
        write(folder / 'operation-receipt.json', receipt); transition('record', identifier, folder / 'operation-receipt.json')
    print(json.dumps({'exact_reader_reviews': 'Q2-Q4 pass', 'Q1_Q5': 'open'}))


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('command', choices=['review', 'record', 'publish', 'renew']); args = p.parse_args()
    {'review': review, 'record': record, 'publish': publish, 'renew': renew}[args.command]()
