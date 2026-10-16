#!/usr/bin/env python3
"""Review and publish the recovered commercial comparison without granting coverage."""
import argparse
from collections import Counter
import json
from pathlib import Path

import build_commercial_matrix_reader_20261016 as build
import master_control as core
import run_program as run
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

ROOT, BASE, OUT, WORK = build.ROOT, build.BASE, build.OUT, build.WORK
REVIEWER = {'name': 'Codex author/coordinator', 'kind': 'author'}
LIMITS = [
    'The nine-vendor comparison remains inconclusive; MATLAB originals and exact editions remain unresolved.',
    'No vendor execution, purchased entitlement, real prices, bank ROI or qualified survival adapter.',
    'Q1 coverage/depth and Q5 sponsor/rendered acceptance remain open.',
    'No new images inspected: the inherited six-preview session allowance is exhausted.']


def review():
    report = json.loads((OUT/'build-report.json').read_text())
    audit = json.loads((OUT/'source-audit.json').read_text())
    prior = json.loads(build.PRIOR.read_text())
    index = json.loads((BASE/'traceability-review.json').read_text())
    for obj in [report, audit, prior, index, json.loads((BASE/'prepared-inputs.json').read_text()),
                json.loads((WORK/'author-review.json').read_text())]:
        verify_bindings(obj)
    assert report['pages'] == 818 and report['cited_records'] == 643
    assert index['status'] == 'pass' and not index['issues'] and index['scholarly_pdfs'] == 175
    layout = json.loads((OUT/'text-layout-review.json').read_text())
    assert layout['status'] == 'pass' and not layout['empty_pages'] and not layout['out_of_bounds']
    assert not [w for w in report['warnings'] if 'Underfull' not in w]
    old = {s['integrated_citation_key']: s for s in prior['sources']}
    new = {s['integrated_citation_key']: s for s in audit['sources']}
    assert len(old) == 641 and len(new) == 643 and all(new[k] == s for k, s in old.items())
    files = {r['path']: r for r in audit['tex_files']}
    kept = [r for r in prior['tex_files'] if r['path'] != str(build.OLD.relative_to(ROOT))]
    assert all(files[r['path']]['sha256'] == r['sha256'] for r in kept)
    previous = json.loads((build.PRIOR.parent.parent/'traceability-review.json').read_text())
    contexts = {r['citation_key']: Counter(json.dumps(x, sort_keys=True) for x in r['citation_contexts']) for r in index['records']}
    for row in previous['records']:
        assert not Counter(json.dumps(x, sort_keys=True) for x in row['citation_contexts']) - contexts[row['citation_key']]
    probes = json.loads((WORK/'survival-method-probes.json').read_text())
    verify_bindings(probes)
    assert len(probes['profiles']) == 3
    assert all(p['response']['disposition'] == 'unsupported' and p['response']['result'] is None for p in probes['profiles'])
    text = ' '.join((OUT/'reader.txt').read_text().split())
    for phrase in ['Commercial survival options against the proposed service', 'SAS/STAT 14.1',
                   'Prices and those rights are unavailable', 'two attempted official method originals returned HTTP 403']:
        assert phrase in text, phrase
    evidence = [ref(p, a) for p, a in [
        (OUT/'build-report.json', 'Completed recovered 818-page build'),
        (OUT/'source-audit.json', '643 citation records'),
        (BASE/'traceability-review.json', '175 genuine scholarly PDFs and preserved contexts'),
        (OUT/'text-layout-review.json', 'All 818 page text bounds'),
        (OUT/'reader.txt', 'Inspected new section on printed pages 325–326'),
        (build.MATRIX, 'Nine vendor families with current and proposed capabilities'),
        (WORK/'primary-review.json', 'Official sources and bounded capability comparison'),
        (WORK/'author-review.json', 'Reviewed scope and limitations'),
        (WORK/'survival-method-probes.json', 'Three actual local unsupported outcomes'),
        (WORK/'harness-repair-01.json', 'Preserved initial review failure and repair'),
        (Path(__file__), 'Exact-reader publication review')]]
    write(BASE/'release-source-review.json', {
        'status': 'pass', 'issues': [], 'reviewer': REVIEWER, 'reviewed_reader': report['pdf'],
        'scope': 'Author source and extracted-text review of a preserving commercial comparison',
        'preserved_records': 641, 'new_records': 2, 'preserved_compiled_sources': len(kept),
        'original_contexts_retained': True, 'evidence': evidence,
        'findings': [
            'The new section faithfully separates documented vendor routes, observed local refusal and proposed capabilities.',
            'Fourteen official originals support eight families; the ninth family and exact edition/rights gaps remain explicit.',
            'The three local responses are dispatch probes, not survival-estimator evaluation or vendor runs.',
            'Public/generated prototypes precede costly licensed trials; no price or advantage is invented.'],
        'limitations': LIMITS, 'visual_acceptance': False})
    print(json.dumps({'review': 'pass', 'pages': 818, 'inherited_contexts_preserved': True}))


def publish():
    state = core.read(ROOT, core.STATE); before = core.sha(ROOT/core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path'] == str(build.OLD.with_suffix('.pdf').relative_to(ROOT))
    assert state['execution_program']['results']['SW.COMM.longitudinal_survival']['outcome'] == 'inconclusive'
    report = json.loads((OUT/'build-report.json').read_text())
    audit = json.loads((OUT/'source-audit.json').read_text())
    reviewed = json.loads((BASE/'release-source-review.json').read_text()); verify_bindings(reviewed)
    manifest = {
        'kind': 'working_monograph', 'final_acceptance': False, 'pdf': report['pdf'], 'pages': report['pages'],
        'supersedes': {k: state['reader'][k] for k in ['path', 'sha256']},
        'build_report': ref(OUT/'build-report.json', 'Recovered preserving commercial reader'),
        'source_review': ref(BASE/'release-source-review.json', 'Exact-reader author review'),
        'text_layout': ref(OUT/'text-layout-review.json', 'All-page text bounds'),
        'source_artifacts': audit['tex_files'] + reviewed['evidence'],
        'visual_acceptance': False, 'mandatory_repairs_closed': [],
        'changes': ['Integrate commercial survival comparison and observed local method refusals.',
                    'Explain bounded prototype profiles and later licensed matched trials, retaining omissions.'],
        'sponsor_binding': 'Preserved sponsor baseline; Q5 reconciliation remains open.'}
    write(BASE/'working-release.json', manifest)
    binding = ref(BASE/'working-release.json', 'Reviewed commercial comparison working successor')
    run.ledger.validate_working_release(ROOT, binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader'] = {k: report['pdf'][k] for k in ['path', 'sha256']}
    state['reader'].update(pages=report['pages'], status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT, before, state, {'action': 'publish_commercial_survival_matrix', 'manifest': binding, 'final_acceptance': False})
    print(json.dumps({'published': state['reader']}))


def renew():
    report = json.loads((OUT/'build-report.json').read_text())
    verify_bindings(json.loads((BASE/'release-source-review.json').read_text()))
    findings = {
        'Q2': 'All 641 inherited source records and citation uses remain. Two project records bind the inspected matrix and actual local dispatch evidence; 643 citations and 175 scholarly PDFs are traceable. Vendor coverage and historical edition limits remain explicit.',
        'Q3': 'Prior demonstrated evidence is preserved. Three authored method identifiers actually returned unsupported with null results. These establish a bounded dispatcher limit, not a native survival benchmark. No vendor runtime or new calibration is claimed.',
        'Q4': 'The comparison explains what a public/generated prototype should establish before paying for a licensed trial. Exact entitlement, rights, full workflow costs and prices remain unknown. The preceding investment case is preserved without inventing ROI or vendor superiority.'}
    for q, finding in findings.items():
        identifier = 'PROPOSAL.' + q; state = core.read(ROOT, core.STATE)
        assert state['reader']['sha256'] == report['pdf']['sha256']
        previous = state['execution_runtime']['results'][identifier]
        old = json.loads((ROOT/previous['path']).read_text())
        folder = BASE/q; folder.mkdir(exist_ok=False)
        evidence = [previous, ref(BASE/'working-release.json', 'Exact current reader'),
                    ref(BASE/'release-source-review.json', 'Inspected preserving delta'),
                    ref(build.MATRIX, 'Reviewed comparison with unresolved evidence'),
                    ref(WORK/'survival-method-probes.json', 'Actual local outcomes'), ref(Path(__file__), 'Review findings')]
        write(folder/'reopen.json', {'reason': 'Recovered successor requires an exact-reader review.',
              'prior_result': previous, 'reviewed_reader': report['pdf'], 'evidence': evidence,
              'next_action': 'Record the reviewed commercial comparison with all inherited limits.'})
        transition('reopen', identifier, folder/'reopen.json')
        state = core.read(ROOT, core.STATE); graph, _, _ = run.combined(ROOT, state)
        node = run.ledger.operation(graph, identifier)
        attempt = len(state['execution_runtime']['review_history'][identifier])
        output = ROOT/run.review_output_paths(node, state['reader'], attempt)[0]
        limits = list(dict.fromkeys(old['limitations'] + LIMITS)); scope = 'Author exact-reader proposal delta review'
        write(output, {'operation': identifier, 'status': 'pass', 'criterion': node['criteria'][0],
              'reviewer': REVIEWER, 'reviewed_reader': report['pdf'], 'review_attempt': attempt,
              'acceptance_scope': 'proposal_only', 'scope': scope, 'findings': [finding], 'evidence': evidence,
              'limitations': limits, 'visual_acceptance': False})
        receipt = run.ledger.receipt_template(node)
        receipt.update(outcome='pass', execution='performed', scope=scope, reviewer=REVIEWER, limitations=limits,
                       reviewed_reader=report['pdf'], review_attempt=attempt, acceptance_scope='proposal_only',
                       outputs=[ref(output, 'Current-reader '+q+' author review')], nonexecution_reason='', revisit_trigger='',
                       criteria=[{'index': 0, 'verdict': 'pass', 'finding': finding, 'evidence': evidence}])
        write(folder/'operation-receipt.json', receipt); transition('record', identifier, folder/'operation-receipt.json')
    print(json.dumps({'exact_reader_reviews': 'Q2-Q4 pass', 'Q1_Q5': 'open'}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('command', choices=['review', 'publish', 'renew'])
    args = parser.parse_args(); {'review': review, 'publish': publish, 'renew': renew}[args.command]()
