#!/usr/bin/env python3
"""Review and publish the custody delta with exact-reader review continuity."""
import argparse
import json
from pathlib import Path
import re

import build_custody_reader_20261014 as build
import master_control as core
import review_artifact_custody_20261014 as work
import run_program as run
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

ROOT, BASE, OUT = work.ROOT, build.BASE, build.OUT
LIMITS = work.LIMITS + ['No automatic substantive-page or mandatory-repair credit; Q1 remains open.']
NEW_KEYS = {'exec14_custody_' + x for x in ['implementation', 'observations', 'design']}


def review():
    report = json.loads((OUT / 'build-report.json').read_text())
    audit = json.loads((OUT / 'source-audit.json').read_text())
    prior = json.loads(build.PRIOR.read_text())
    index = json.loads((BASE / 'traceability-review.json').read_text())
    for obj in [report, audit, prior, index, json.loads((BASE / 'prepared-inputs.json').read_text())]:
        verify_bindings(obj)
    assert index['status'] == 'pass' and not index['issues'] and index['scholarly_pdfs'] == 156
    assert json.loads((OUT / 'text-layout-review.json').read_text())['status'] == 'pass'
    assert not [w for w in report['warnings'] if 'Underfull' not in w]
    old = {r['integrated_citation_key']: r for r in prior['sources']}
    new = {r['integrated_citation_key']: r for r in audit['sources']}
    assert len(old) == 531 and len(new) == 534 and new.keys() - old.keys() == NEW_KEYS
    assert all(new[k] == row for k, row in old.items())
    compiled = {r['path']: r for r in audit['tex_files']}
    inherited = [r for r in prior['tex_files'] if r['path'] != str(build.OLD.relative_to(ROOT))]
    assert all(compiled[r['path']]['sha256'] == r['sha256'] for r in inherited)
    prev = json.loads((build.PRIOR.parent.parent / 'traceability-review.json').read_text())
    contexts = {r['citation_key']: r['citation_contexts'] for r in index['records']}
    assert all(contexts[r['citation_key']] == r['citation_contexts'] for r in prev['records'])
    text = re.sub(r'\s+', ' ', (OUT / 'reader.txt').read_text())
    for phrase in ['Data custody preserves the meaning of a causal claim',
                   'changed a generated balance from 100 to 900', 'one-second deadline',
                   'This is a proposed repair', 'an empty set is a mathematical outcome',
                   'Retention and revocation', 'Public data can test acquisition']:
        assert phrase.lower() in text.lower(), phrase
    findings = [
        'Scientific context binds population, horizon, graph, information clock and other declarations; byte agreement does not establish their truth.',
        'Fifteen actual generated local cases and sixteen existing tests support selected ordinary refusals, empty/unavailable semantics and replay behavior.',
        'Coherent local content/metadata/supplied-reference replacement under an inconsistent handle was accepted; old trusted reference refused. Scope excludes an inferred remote attack.',
        'FIFO without writer blocked before fstat until child termination; parent preflight lacks the later worker deadline. Nonblocking open is a proposed candidate, not complete race/latency qualification.',
        'Concrete successor repair, adapter, authorization, lifecycle and owner-input cases are prospective and distinguish public prototype evidence from institutional acceptance.',
        'Physical pages 510-514 contain the new section; extracted text and whole-reader bounds checked. Visual acceptance remains pending.',
        'All 531 earlier citation records and contexts and inherited compiled chapter bytes are unchanged; three project records yield 534 records and 156 scholarly PDFs.',
    ]
    evidence = [ref(p, anchor) for p, anchor in [
        (OUT / 'build-report.json', 'Exact 719-page successor'),
        (OUT / 'source-audit.json', '534 cited source records'),
        (OUT / 'reader.txt', 'Inspected custody text and equation'),
        (OUT / 'text-layout-review.json', 'All-page text extraction and bounds'),
        (BASE / 'traceability-review.json', 'Whole-reader source and context index'),
        (BASE / 'prepared-inputs.json', 'Preserving source construction'),
        (work.BASE / 'primary-review.json', 'Inspected implementation'),
        (work.BASE / 'local-observations.json', 'Actual cases, responses and negative findings'),
        (work.BASE / 'local-tests.xml', 'Sixteen passing existing tests'),
        (work.BASE / 'design-review.json', 'Prospective repairs and owner inputs'),
        (build.SYN, 'Connected custody development'),
        (Path(__file__).resolve(), 'Author source/text review procedure'),
    ]]
    write(BASE / 'release-source-review.json', {
        'status': 'pass', 'issues': [], 'reviewer': work.REVIEWER,
        'reviewed_reader': report['pdf'], 'findings': findings, 'evidence': evidence,
        'unchanged_source_records': 531, 'new_source_records': sorted(NEW_KEYS),
        'unchanged_inherited_compiled_sources': len(inherited),
        'unchanged_inherited_citation_contexts': True,
        'limitations': LIMITS, 'visual_acceptance': False, 'bank_ROI_established': False})
    receipt = json.loads((work.BASE / 'operation-receipt.json').read_text())
    for criterion in receipt['criteria']:
        criterion['evidence'].append(ref(BASE / 'release-source-review.json', 'Exact integrated-reader review'))
    write(BASE / 'requirement-operation-receipt.json', receipt)
    print(json.dumps({'review': 'pass', 'pages': report['pages'], 'cited_records': 534}))


def publish():
    state = core.read(ROOT, core.STATE)
    before = core.sha(ROOT / core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path'] == str(build.OLD.with_suffix('.pdf').relative_to(ROOT))
    assert work.OP in state['execution_program']['results']
    report = json.loads((OUT / 'build-report.json').read_text())
    audit = json.loads((OUT / 'source-audit.json').read_text())
    review = json.loads((BASE / 'release-source-review.json').read_text())
    verify_bindings(review)
    manifest = {'kind': 'working_monograph', 'final_acceptance': False, 'pdf': report['pdf'], 'pages': report['pages'],
                'supersedes': {k: state['reader'][k] for k in ['path', 'sha256']},
                'build_report': ref(OUT / 'build-report.json', 'Preserving custody reader'),
                'source_review': ref(BASE / 'release-source-review.json', 'Source, observations and text review'),
                'text_layout': ref(OUT / 'text-layout-review.json', 'All-page text and bounds'),
                'source_artifacts': audit['tex_files'] + review['evidence'], 'visual_acceptance': False,
                'mandatory_repairs_closed': [],
                'changes': ['Integrate scientific-context custody, actual local refusals and two negative boundary findings.',
                            'Develop concrete proposed repairs, cross-repository acceptance and owner inputs.'],
                'sponsor_binding': 'Preserved sponsor baseline; Q5 reconciliation remains open.'}
    write(BASE / 'working-release.json', manifest)
    binding = ref(BASE / 'working-release.json', 'Reviewed custody working successor')
    run.ledger.validate_working_release(ROOT, binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader'] = {k: report['pdf'][k] for k in ['path', 'sha256']}
    state['reader'].update(pages=report['pages'], status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT, before, state, {'action': 'publish_custody_reader', 'manifest': binding, 'final_acceptance': False})
    print(json.dumps({'published': state['reader'], 'proposal_accepted': False}))


def renew():
    report = json.loads((OUT / 'build-report.json').read_text())
    findings = {
        'Q2': 'All 531 earlier source records, contexts and manuscript inputs are preserved; three project records bind inspected source, fifteen actual local generated cases, sixteen passing existing tests, explicit negative findings and prospective repairs. 534 records and 156 scholarly PDFs.',
        'Q3': 'Prior demonstration evidence is preserved. Actual generated local trials substantiate ordinary refusals and two custody limitations without claiming authenticated, race-free, bank or remote-exploit qualification. Static/proposed cases remain distinct.',
        'Q4': 'Earlier economic scenarios are unchanged. Generated prototype cases can qualify meaning-preserving custody and its known local repairs before expensive bank trials; no new prices, bank superiority or ROI are asserted.',
    }
    verify_bindings(json.loads((BASE / 'release-source-review.json').read_text()))
    for q, finding in findings.items():
        identifier = 'PROPOSAL.' + q
        state = core.read(ROOT, core.STATE)
        assert state['reader']['sha256'] == report['pdf']['sha256']
        previous = state['execution_runtime']['results'][identifier]
        old = json.loads((ROOT / previous['path']).read_text())
        folder = BASE / q
        folder.mkdir(exist_ok=False)
        evidence = [previous, ref(BASE / 'working-release.json', 'Exact current reader'),
                    ref(BASE / 'release-source-review.json', 'Reviewed source/observation/design delta'),
                    ref(Path(__file__).resolve(), 'Current review findings')]
        write(folder / 'reopen.json', {'reason': 'Reader changed; preserve and renew the earlier review.',
              'prior_result': previous, 'reviewed_reader': report['pdf'], 'evidence': evidence,
              'next_action': 'Record reviewed custody findings against the new reader.'})
        transition('reopen', identifier, folder / 'reopen.json')
        state = core.read(ROOT, core.STATE)
        graph, _, _ = run.combined(ROOT, state)
        node = run.ledger.operation(graph, identifier)
        attempt = len(state['execution_runtime']['review_history'][identifier])
        output = ROOT / run.review_output_paths(node, state['reader'], attempt)[0]
        limits = list(dict.fromkeys(old['limitations'] + LIMITS))
        scope = 'Author exact-reader delta review; proposal evidence only'
        write(output, {'operation': identifier, 'status': 'pass', 'criterion': node['criteria'][0],
              'reviewer': work.REVIEWER, 'reviewed_reader': report['pdf'], 'review_attempt': attempt,
              'acceptance_scope': 'proposal_only', 'scope': scope, 'findings': [finding],
              'evidence': evidence, 'limitations': limits, 'visual_acceptance': False})
        receipt = run.ledger.receipt_template(node)
        receipt.update(outcome='pass', execution='performed', scope=scope, reviewer=work.REVIEWER,
                       limitations=limits, reviewed_reader=report['pdf'], review_attempt=attempt,
                       acceptance_scope='proposal_only', outputs=[ref(output, 'Current-reader ' + q + ' review')],
                       nonexecution_reason='', revisit_trigger='',
                       criteria=[{'index': 0, 'verdict': 'pass', 'finding': finding, 'evidence': evidence}])
        write(folder / 'operation-receipt.json', receipt)
        transition('record', identifier, folder / 'operation-receipt.json')
    print(json.dumps({'exact_reader_reviews': 'Q2-Q4 pass', 'proposal_accepted': False}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['review', 'publish', 'renew'])
    args = parser.parse_args()
    {'review': review, 'publish': publish, 'renew': renew}[args.command]()
