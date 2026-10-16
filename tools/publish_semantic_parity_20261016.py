#!/usr/bin/env python3
"""Review, record and publish the recovered semantic-parity proposal increment."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
import build_semantic_parity_reader_20261016 as build
import review_semantic_parity_20261016 as work
import master_control as core
import run_program as run
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

ROOT, BASE, OUT, WORK = build.ROOT, build.BASE, build.OUT, build.WORK


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
    assert len(old) == 656 and len(new) == 658 and all(new[k] == s for k, s in old.items())
    files = {r['path']: r for r in audit['tex_files']}
    kept = [r for r in prior['tex_files'] if r['path'] != str(build.OLD.relative_to(ROOT))]
    assert all(files[r['path']]['sha256'] == r['sha256'] for r in kept)
    previous = read(build.PRIOR.parent.parent / 'traceability-review.json')
    contexts = {r['citation_key']: Counter(json.dumps(x, sort_keys=True) for x in r['citation_contexts']) for r in index['records']}
    for row in previous['records']:
        assert not Counter(json.dumps(x, sort_keys=True) for x in row['citation_contexts']) - contexts[row['citation_key']]
    text = re.sub(r'-\s+', '-', ' '.join((OUT / 'reader.txt').read_text().split()))
    for phrase in ['What exact agreement across three interfaces establishes', 'thirteen scientific requests',
                   'all nine advertised operations', 'nonprobabilistic', 'JSONDecodeError',
                   'stored execution state', 'CallToolResult', 'AnyIO', 'repair is specified',
                   'cancellation after completion', 'No transport comparison can supply']:
        assert phrase in text, phrase
    assert work.independent_meanings() == read(WORK / 'independent-meanings.json')
    assert work.observations() == read(WORK / 'observation-review.json')
    evidence = [ref(p, a) for p, a in [
        (OUT / 'build-report.json', 'Preserving interface reader'), (OUT / 'source-audit.json', '658 source records'),
        (BASE / 'traceability-review.json', '175 genuine scholarly PDFs and preserved citation contexts'),
        (OUT / 'text-layout-review.json', 'All-page text bounds'), (OUT / 'reader.txt', 'Inspected integrated text'),
        (WORK / 'source-review.json', 'Current source snapshots and six matched SDK originals'),
        (WORK / 'observation-review.json', '13 scientific, three lifecycle and three adverse cases'),
        (WORK / 'independent-meanings.json', 'Separate algebra and clock/context meanings'),
        (WORK / 'proposed-contract.json', 'Error/identity repair and local/external acceptance plan'),
        (WORK / 'plan-review.json', 'Reviewed plan and scope'), (WORK / 'author-review.json', 'Criterion review'),
        (work.OUTPUT, 'Bounded proposal requirement review'), (Path(__file__), 'Exact-reader review and transitions')]]
    write(BASE / 'release-source-review.json', {'status': 'pass', 'issues': [], 'reviewer': work.REVIEWER,
        'reviewed_reader': report['pdf'], 'scope': 'Author source, saved-observation, algebra and extracted-text review',
        'preserved_records': 656, 'new_records': 2, 'preserved_compiled_sources': len(kept), 'original_contexts_retained': True,
        'evidence': evidence, 'findings': [
            'Exact response agreement is restricted to the common negotiated request domain and bounded generated cases.',
            'Capability asymmetry, scientific refusal and stored replay corruption are distinct and retained.',
            'SDK validation ownership and complete transport identity are supported by actual source paths.',
            'Error repair, local cases and later owner inputs are proposed; no implementation repair or universal parity is claimed.',
            'All inherited source records, contexts and economic claims remain; no new bank economics or live model claim.'],
        'limitations': work.LIMITS, 'visual_acceptance': False})
    print(json.dumps({'review': 'pass', 'pages': report['pages'], 'sections': report['semantic_parity_sections']}))


def record():
    reviewed = read(BASE / 'release-source-review.json'); verify_bindings(reviewed)
    author = read(WORK / 'author-review.json')
    state = core.read(ROOT, core.STATE); graph, _, _ = run.combined(ROOT, state); node = run.ledger.operation(graph, work.OP)
    receipt = run.ledger.receipt_template(node)
    receipt.update(outcome='pass', execution='performed', scope='Bounded proposal evidence and acceptance design for library/CLI/MCP semantic parity',
        reviewer=work.REVIEWER, limitations=work.LIMITS, capabilities=[], outputs=[ref(work.OUTPUT, 'Reviewed integration requirement')],
        nonexecution_reason='', revisit_trigger='Execute a fresh successor repair protocol and actual consumer/platform tests when implementing the proposed prototype.',
        criteria=[{'index': i, 'verdict': 'pass', 'finding': finding,
                   'evidence': [ref(WORK / 'author-review.json', 'Criterion review'), ref(BASE / 'release-source-review.json', 'Preserving integration')]}
                  for i, finding in enumerate(author['findings'])])
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
        'build_report': ref(OUT / 'build-report.json', 'Preserving semantic-parity reader'),
        'source_review': ref(BASE / 'release-source-review.json', 'Exact-reader author review'),
        'text_layout': ref(OUT / 'text-layout-review.json', 'All-page bounds'),
        'source_artifacts': audit['tex_files'] + reviewed['evidence'], 'visual_acceptance': False, 'mandatory_repairs_closed': [],
        'changes': ['Integrate actual common-domain interface agreement and adverse error observations.',
                    'Specify replay-error, validation and transport-identity repairs with local and later owner acceptance cases.'],
        'sponsor_binding': 'Preserved sponsor baseline; Q5 reconciliation remains open.'}
    write(BASE / 'working-release.json', manifest); binding = ref(BASE / 'working-release.json', 'Reviewed semantic-parity working successor')
    run.ledger.validate_working_release(ROOT, binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader'] = {k: report['pdf'][k] for k in ['path', 'sha256']}
    state['reader'].update(pages=report['pages'], status=status); state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT, before, state, {'action': 'publish_semantic_parity_reader', 'manifest': binding, 'final_acceptance': False})
    print(json.dumps({'published': state['reader']}))


def renew():
    report = read(OUT / 'build-report.json'); verify_bindings(read(BASE / 'release-source-review.json'))
    findings = {
        'Q2': 'All 656 inherited citation records and contexts remain. Two additions bind frozen requests/responses, current local source snapshots, six hash-matched SDK originals and the proposed acceptance contract. The reader has 658 traceable records and 175 genuine scholarly PDFs; observed/static/proposed claims and limits remain explicit.',
        'Q3': 'Thirteen scientific comparisons and three lifecycle comparisons cover nine advertised local operations through actual library/CLI/MCP stdio; three adverse cases retain the replay corruption attribution defect. Saved objects are independently compared, replay restoration checked, and set/moment/clock meanings recalculated. No trial was rerun, no new live-model or bank claim is added.',
        'Q4': 'The preserving delta leaves prior baseline, cost and value-of-information scenarios intact. It specifies a low-cost generated successor experiment for a demonstrated interface defect before consumer/platform investment, including semantic preparation, maintenance, storage, investigation and qualification costs. Actual bank prices, ROI and owner acceptance remain unclaimed.'}
    for q, finding in findings.items():
        identifier = 'PROPOSAL.' + q; state = core.read(ROOT, core.STATE)
        assert state['reader']['sha256'] == report['pdf']['sha256']
        previous = state['execution_runtime']['results'][identifier]; old = read(ROOT / previous['path'])
        folder = BASE / q; folder.mkdir(exist_ok=False)
        evidence = [previous, ref(BASE / 'working-release.json', 'Exact current reader'),
                    ref(BASE / 'release-source-review.json', 'Inspected preserving delta'), ref(work.OUTPUT, 'Reviewed proposal requirement'),
                    ref(WORK / 'proposed-contract.json', 'Concrete next experiment and full-cost categories'), ref(Path(__file__), 'Review findings')]
        write(folder / 'reopen.json', {'reason': 'Changed reader requires preserved successor author review.',
            'prior_result': previous, 'reviewed_reader': report['pdf'], 'evidence': evidence,
            'next_action': 'Record reviewed semantic-parity delta with preserved evidence and explicit scope limits.'})
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
