#!/usr/bin/env python3
"""Review and publish the pinned DataHub catalog reference decision."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
import build_datahub_reader_20261016 as build
import prepare_datahub_review_20261016 as work
import master_control as core
import run_program as run
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

ROOT, BASE, OUT, WORK = build.ROOT, build.BASE, build.OUT, build.WORK
OUTPUT = work.OUTPUT
FINDINGS = [
    'Sixteen original files match retrieval SHA-256 and pinned Git blobs at a cutoff-compatible revision. License, notices, declared dependencies and maintenance are inspected; distribution/version/dependency closure remains a scoped limitation.',
    'Metadata target, lineage confidence, availability clocks, identity, versions, pagination and incomplete context are distinguished from causal claims. Alternatives, full-cost categories, responsibilities and revisit conditions are developed with exact generated references.',
    'The decision is reference with integration_allowed false. A proposed bounded conversion/failure oracle and actual future SDK/server comparison are specified without granting adapter qualification.']


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
    assert len(old) == 666 and len(new) == 670 and all(new[k] == s for k, s in old.items())
    files = {r['path']: r for r in audit['tex_files']}
    kept = [r for r in prior['tex_files'] if r['path'] != str(build.OLD.relative_to(ROOT))]
    assert all(files[r['path']]['sha256'] == r['sha256'] for r in kept)
    previous = read(build.PRIOR.parent.parent / 'traceability-review.json')
    contexts = {r['citation_key']: Counter(json.dumps(x, sort_keys=True) for x in r['citation_contexts']) for r in index['records']}
    for row in previous['records']:
        assert not Counter(json.dumps(x, sort_keys=True) for x in row['citation_contexts']) - contexts[row['citation_key']]
    text = re.sub(r'-\s+', '-', ' '.join((OUT / 'reader.txt').read_text().split()))
    for phrase in ['Catalog context for causal observations', 'confidenceScore', 'strictly positive observed table',
                   'retrospective leakage', '501 accumulated records', 'repeated-cursor disposition',
                   'No such permission is granted', 'read operations and proposed metadata']:
        assert phrase.lower() in text.lower(), phrase
    assert work.examples.calculate() == read(WORK / 'exact-results.json')
    source = read(WORK / 'source-review.json'); verify_bindings(source)
    assert source['source_count'] == 16 and all(x['git_blob_verified'] for x in source['records'])
    evidence = [ref(p, a) for p, a in [
        (OUT / 'build-report.json', 'Preserving catalog reader'), (OUT / 'source-audit.json', '670 source records'),
        (BASE / 'traceability-review.json', '175 genuine scholarly PDFs and preserved citation contexts'),
        (OUT / 'text-layout-review.json', 'All-page text bounds'), (OUT / 'reader.txt', 'Inspected integrated text'),
        (WORK / 'source-review.json', 'Sixteen original files matched to pinned source tree'),
        (WORK / 'omissions-register.json', 'Distribution, delegated paths, server and semantic limits'),
        (WORK / 'proposed-export-contract.json', 'Bounded public/generated prototype and conversion/failure cases'),
        (WORK / 'exact-results.json', 'Four reproduced generated reference families and five missing-context cases'),
        (WORK / 'author-review.json', 'Bounded reference author review'), (Path(__file__), 'Exact-reader review and transitions')]]
    decision = read(WORK / 'decision-proposal.json')
    assert decision['decision'] == 'reference' and not decision['integration_allowed']
    decision.update(compiled_reader=report['pdf'], manuscript_evidence=evidence)
    write(OUTPUT, decision)
    write(BASE / 'release-source-review.json', {'status': 'pass', 'issues': [], 'reviewer': work.REVIEWER,
        'reviewed_reader': report['pdf'], 'scope': 'Author pinned-source, exact mathematics and extracted-text review',
        'decision': 'reference', 'integration_allowed': False, 'preserved_records': 666, 'new_records': 4,
        'preserved_compiled_sources': len(kept), 'original_contexts_retained': True,
        'evidence': evidence + [ref(OUTPUT, 'Contracted reference decision')],
        'findings': FINDINGS + ['Generated worlds with identical observed tables and catalog lineage yield different intervention values.',
            'Source-defined audit clocks, lineage confidence, 3+ hop categories and accumulated pages require an explicit proposed consumer contract.',
            'No downloaded code, SDK, server, Cloud product, connector or MCP server was executed.'],
        'limitations': work.LIMITS, 'visual_acceptance': False})
    print(json.dumps({'review': 'pass', 'decision': 'reference', 'pages': report['pages'], 'sections': report['datahub_sections']}))


def record():
    verify_bindings(read(BASE / 'release-source-review.json'))
    state = core.read(ROOT, core.STATE); graph, _, _ = run.combined(ROOT, state); node = run.ledger.operation(graph, work.OP)
    receipt = run.ledger.receipt_template(node)
    receipt.update(outcome='pass', execution='performed', scope='Bounded pinned DataHub reference decision; no integration capability',
        reviewer=work.REVIEWER, limitations=work.LIMITS, capabilities=[], outputs=[ref(OUTPUT, 'Reviewed catalog reference decision')],
        nonexecution_reason='', revisit_trigger='Selected minimal permissible pinned path, resolved dependency/notice inventory and actual SDK/server fixture comparison.',
        criteria=[{'index': i, 'verdict': verdict, 'finding': finding,
                   'evidence': [ref(OUTPUT, 'Criterion review'), ref(BASE / 'release-source-review.json', 'Preserving integration')]}
                  for i, (verdict, finding) in enumerate(zip(['pass', 'pass', 'pass'], FINDINGS))])
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
        'build_report': ref(OUT / 'build-report.json', 'Preserving catalog reference reader'),
        'source_review': ref(BASE / 'release-source-review.json', 'Exact-reader author review'),
        'text_layout': ref(OUT / 'text-layout-review.json', 'All-page bounds'),
        'source_artifacts': audit['tex_files'] + reviewed['evidence'], 'visual_acceptance': False, 'mandatory_repairs_closed': [],
        'changes': ['Integrate pinned DataHub source, rights and catalog-semantics comparison.',
                    'Develop four exact semantic examples and a bounded export contract; reference decision grants no integration capability.'],
        'sponsor_binding': 'Preserved sponsor baseline; Q5 reconciliation remains open.'}
    write(BASE / 'working-release.json', manifest); binding = ref(BASE / 'working-release.json', 'Reviewed catalog reference working successor')
    run.ledger.validate_working_release(ROOT, binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader'] = {k: report['pdf'][k] for k in ['path', 'sha256']}
    state['reader'].update(pages=report['pages'], status=status); state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT, before, state, {'action': 'publish_datahub_reference_reader', 'manifest': binding, 'final_acceptance': False})
    print(json.dumps({'published': state['reader']}))


def renew():
    report = read(OUT / 'build-report.json'); verify_bindings(read(BASE / 'release-source-review.json'))
    findings = {
        'Q2': 'All 666 inherited records, contexts and compiled sources survive. Four new records bind sixteen pinned original files, source/rights/dependency scope, exact generated references and a proposed export contract. The reader has 670 traceable records and 175 genuine scholarly PDFs; no catalog metadata claim is promoted to causal truth.',
        'Q3': 'Four exact generated families reproduce observed-law ambiguity, historical availability leakage, identity loss and traversal/pagination meanings. Five missing-context dispositions define the proposed consumer contract. Static source review and authored oracles are distinct from unexecuted DataHub SDK/server behavior; no live model or bank claim is added.',
        'Q4': 'The preserved investment argument gains a narrow public/generated catalog fixture before live integration, with manual mapping, maintenance, infrastructure, rights, semantic review and incident costs. Stipulated USD20/-30 contrasts illustrate consequential assignment ambiguity; actual prices, catalog-owner truth and bank ROI remain unclaimed.'}
    for q, finding in findings.items():
        identifier = 'PROPOSAL.' + q; state = core.read(ROOT, core.STATE)
        assert state['reader']['sha256'] == report['pdf']['sha256']
        previous = state['execution_runtime']['results'][identifier]; old = read(ROOT / previous['path'])
        folder = BASE / q; folder.mkdir(exist_ok=False)
        evidence = [previous, ref(BASE / 'working-release.json', 'Exact current reader'),
                    ref(BASE / 'release-source-review.json', 'Inspected preserving delta'), ref(OUTPUT, 'Reviewed catalog reference decision'),
                    ref(WORK / 'proposed-export-contract.json', 'Concrete prototype and full-cost categories'), ref(Path(__file__), 'Review findings')]
        write(folder / 'reopen.json', {'reason': 'Changed reader requires preserved successor author review.',
            'prior_result': previous, 'reviewed_reader': report['pdf'], 'evidence': evidence,
            'next_action': 'Record reviewed DataHub reference delta with preserved evidence and explicit scope limits.'})
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
