#!/usr/bin/env python3
"""Review and publish the Causica proposal reference without enabling a runtime."""
import argparse
import json
from pathlib import Path

import build_causica_reader_20261014 as build
import review_causica_reuse_20261014 as work
import master_control as core
import run_program as run
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

ROOT, BASE, OUT = build.ROOT, build.BASE, build.OUT


def review():
    report = json.loads((OUT / 'build-report.json').read_text())
    audit = json.loads((OUT / 'source-audit.json').read_text())
    prior = json.loads(build.PRIOR.read_text())
    index = json.loads((BASE / 'traceability-review.json').read_text())
    for obj in [report, audit, prior, index, json.loads((BASE / 'prepared-inputs.json').read_text()),
                json.loads((work.BASE / 'author-review.json').read_text())]:
        verify_bindings(obj)
    assert index['status'] == 'pass' and not index['issues'] and index['scholarly_pdfs'] == 163
    assert json.loads((OUT / 'text-layout-review.json').read_text())['status'] == 'pass'
    assert not [w for w in report['warnings'] if 'Underfull' not in w]
    old = {s['integrated_citation_key']: s for s in prior['sources']}
    new = {s['integrated_citation_key']: s for s in audit['sources']}
    assert len(old) == 573 and len(new) == 577 and all(new[k] == s for k, s in old.items())
    files = {r['path']: r for r in audit['tex_files']}
    kept = [r for r in prior['tex_files'] if r['path'] != str(build.OLD.relative_to(ROOT))]
    assert all(files[r['path']]['sha256'] == r['sha256'] for r in kept)
    previous = json.loads((build.PRIOR.parent.parent / 'traceability-review.json').read_text())
    contexts = {r['citation_key']: r['citation_contexts'] for r in index['records']}
    assert all(contexts[r['citation_key']] == r['citation_contexts'] for r in previous['records'])
    assert work.exact() == json.loads((work.BASE / 'exact-results.json').read_text())
    text = ' '.join((OUT / 'reader.txt').read_text().split())
    for phrase in ['Causica: a generative reference', 'A vector score needs a vector reference',
                   'same borrower', '277 packages', 'USD 15', 'USD 35', 'one simultaneous',
                   'default recursive', 'not an observed failure frequency']:
        assert phrase.lower() in text.lower(), phrase
    evidence = [ref(p, a) for p, a in [
        (OUT / 'build-report.json', 'Exact preserving successor'),
        (OUT / 'source-audit.json', '577 citations and original source identities'),
        (BASE / 'traceability-review.json', 'Every inherited context retained; 163 genuine scholarly PDFs'),
        (OUT / 'text-layout-review.json', 'All-page text bounds and extraction'),
        (OUT / 'reader.txt', 'Inspected integrated Causica section'),
        (work.BASE / 'primary-review.json', 'Eighteen pinned source blobs and genuine DECI paper'),
        (work.BASE / 'exact-results.json', 'Independent exact algebra and literal source references'),
        (work.BASE / 'conversion-contract.json', 'Proposed adapter, DAG and vector-score boundaries'),
        (work.BASE / 'author-review.json', 'Scoped reference decision'),
        (Path(__file__).resolve(), 'Exact-reader review and publication procedure')]]
    write(BASE / 'release-source-review.json', {
        'status': 'pass', 'issues': [], 'reviewer': work.REVIEWER, 'reviewed_reader': report['pdf'],
        'scope': 'Author review of the source, exact examples and proposed Causica reference; no native execution',
        'evidence': evidence, 'preserved_records': 573, 'new_records': 4,
        'preserved_compiled_sources': len(kept), 'original_contexts_retained': True,
        'findings': [
            'The primary theorem retains its infinite-data, model-identifiability and complete-data assumptions.',
            'Intervention/conditioning, factual noise, graph axes and model uncertainty remain distinct.',
            'Initialized cyclic mass and two-pass residual are explicit source-based examples, not fitted failure rates.',
            'A multicomponent exact prediction has zero correct error but sqrt(18) under the inspected reference reduction; native qualification remains pending.',
            'Reference selected with concrete public/generated remedies and no integration capability.',
            'All inherited scientific source bytes and citation contexts remain unchanged.'],
        'limitations': work.LIMITS, 'visual_acceptance': False})
    print(json.dumps({'review': 'pass', 'pages': report['pages'], 'new_records': 4}))


def publish():
    state = core.read(ROOT, core.STATE)
    before = core.sha(ROOT / core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path'] == str(build.OLD.with_suffix('.pdf').relative_to(ROOT))
    assert work.OP in state['execution_program']['results']
    report = json.loads((OUT / 'build-report.json').read_text())
    audit = json.loads((OUT / 'source-audit.json').read_text())
    reviewed = json.loads((BASE / 'release-source-review.json').read_text())
    verify_bindings(reviewed)
    manifest = {
        'kind': 'working_monograph', 'final_acceptance': False, 'pdf': report['pdf'], 'pages': report['pages'],
        'supersedes': {k: state['reader'][k] for k in ['path', 'sha256']},
        'build_report': ref(OUT / 'build-report.json', 'Preserving Causica reader'),
        'source_review': ref(BASE / 'release-source-review.json', 'Exact-reader author review'),
        'text_layout': ref(OUT / 'text-layout-review.json', 'All-page text bounds'),
        'source_artifacts': audit['tex_files'] + reviewed['evidence'],
        'visual_acceptance': False, 'mandatory_repairs_closed': [],
        'changes': ['Develop pinned Causica, primary DECI assumptions and intervention/factual-noise semantics.',
                    'Derive cycle and vector-score counterexamples and explicit prototype remedies.',
                    'Specify reference reuse, costs and owner obligations without enabling integration.'],
        'sponsor_binding': 'Preserved sponsor baseline; Q5 reconciliation remains open.'}
    write(BASE / 'working-release.json', manifest)
    binding = ref(BASE / 'working-release.json', 'Reviewed Causica working successor')
    run.ledger.validate_working_release(ROOT, binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader'] = {k: report['pdf'][k] for k in ['path', 'sha256']}
    state['reader'].update(pages=report['pages'], status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT, before, state, {'action': 'publish_causica_reader', 'manifest': binding, 'final_acceptance': False})
    print(json.dumps({'published': state['reader'], 'proposal_accepted': False}))


def renew():
    report = json.loads((OUT / 'build-report.json').read_text())
    verify_bindings(json.loads((BASE / 'release-source-review.json').read_text()))
    findings = {
        'Q2': 'All 573 inherited source records and contexts retained; four new records produce 577, including 163 genuine scholarly PDFs. Eighteen source blobs match the exact local-cutoff tree; the DECI theorem and source-specific findings have explicit anchors.',
        'Q3': 'Inherited demonstrations remain unchanged. Exact Gaussian conditioning/intervention, factual-noise, cyclic-update, vector-score and graph-mixture calculations reproduce. No Causica training, upstream test execution or trained-model failure rate is asserted.',
        'Q4': 'Stipulated net values 12 and minus28 USD versus weighted2 illustrate structural decision risk; they establish no bank ROI. A generated/public prototype tests the identified semantic problems before licensed or expensive bank trials, with complete workflow costs proposed for measurement.'}
    for q, finding in findings.items():
        identifier = 'PROPOSAL.' + q
        state = core.read(ROOT, core.STATE)
        assert state['reader']['sha256'] == report['pdf']['sha256']
        previous = state['execution_runtime']['results'][identifier]
        old = json.loads((ROOT / previous['path']).read_text())
        folder = BASE / q
        folder.mkdir(exist_ok=False)
        evidence = [previous, ref(BASE / 'working-release.json', 'Exact current working reader'),
                    ref(BASE / 'release-source-review.json', 'Source, math and text review'),
                    ref(work.OUTPUT, 'Reference decision and explicit prototype obligations'),
                    ref(work.BASE / 'exact-results.json', 'Exact constructions'),
                    ref(Path(__file__).resolve(), 'Exact-reader review findings')]
        write(folder / 'reopen.json', {'reason': 'Changed reader requires a preserved successor review.',
            'prior_result': previous, 'reviewed_reader': report['pdf'], 'evidence': evidence,
            'next_action': 'Record the exact-reader scoped Causica source, demonstration and economics review.'})
        transition('reopen', identifier, folder / 'reopen.json')
        state = core.read(ROOT, core.STATE)
        graph, _, _ = run.combined(ROOT, state)
        node = run.ledger.operation(graph, identifier)
        attempt = len(state['execution_runtime']['review_history'][identifier])
        output = ROOT / run.review_output_paths(node, state['reader'], attempt)[0]
        limits = list(dict.fromkeys(old['limitations'] + work.LIMITS))
        scope = 'Author exact-reader delta review; proposal evidence only'
        write(output, {'operation': identifier, 'status': 'pass', 'criterion': node['criteria'][0],
            'reviewer': work.REVIEWER, 'reviewed_reader': report['pdf'], 'review_attempt': attempt,
            'acceptance_scope': 'proposal_only', 'scope': scope, 'findings': [finding],
            'evidence': evidence, 'limitations': limits, 'visual_acceptance': False})
        receipt = run.ledger.receipt_template(node)
        receipt.update(outcome='pass', execution='performed', scope=scope, reviewer=work.REVIEWER,
            limitations=limits, reviewed_reader=report['pdf'], review_attempt=attempt, acceptance_scope='proposal_only',
            outputs=[ref(output, 'Current-reader ' + q + ' author review')], nonexecution_reason='', revisit_trigger='',
            criteria=[{'index': 0, 'verdict': 'pass', 'finding': finding, 'evidence': evidence}])
        write(folder / 'operation-receipt.json', receipt)
        transition('record', identifier, folder / 'operation-receipt.json')
    print(json.dumps({'exact_reader_reviews': 'Q2-Q4 pass', 'Q1_Q5': 'open', 'proposal_accepted': False}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['review', 'publish', 'renew'])
    args = parser.parse_args()
    {'review': review, 'publish': publish, 'renew': renew}[args.command]()
