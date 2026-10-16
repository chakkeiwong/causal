#!/usr/bin/env python3
"""Record the reviewed reference choice and publish its preserving reader."""
import argparse
from collections import Counter
import json
from pathlib import Path
import build_dagma_reader_v2_20261016 as build
import review_dagma_reuse_20261016 as work
import master_control as core
import run_program as run
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

ROOT, BASE, OUT, WORK = build.ROOT, build.BASE, build.OUT, build.WORK


def review():
    report = json.loads((OUT/'build-report.json').read_text())
    audit = json.loads((OUT/'source-audit.json').read_text())
    prior = json.loads(build.PRIOR.read_text()); index = json.loads((BASE/'traceability-review.json').read_text())
    for obj in [report, audit, prior, index, json.loads((BASE/'prepared-inputs.json').read_text()),
                json.loads((WORK/'author-review.json').read_text())]: verify_bindings(obj)
    assert index['status'] == 'pass' and not index['issues'] and index['scholarly_pdfs'] == 175
    layout = json.loads((OUT/'text-layout-review.json').read_text())
    assert layout['status'] == 'pass' and not layout['out_of_bounds'] and not layout['empty_pages']
    assert not [w for w in report['warnings'] if 'Underfull' not in w]
    assert build.DRIVER.read_text() == build.expected_driver()
    old = {s['integrated_citation_key']: s for s in prior['sources']}
    new = {s['integrated_citation_key']: s for s in audit['sources']}
    assert len(old) == 643 and len(new) == 646 and all(new[k] == s for k, s in old.items())
    files = {r['path']: r for r in audit['tex_files']}
    kept = [r for r in prior['tex_files'] if r['path'] != str(build.OLD.relative_to(ROOT))]
    assert all(files[r['path']]['sha256'] == r['sha256'] for r in kept)
    previous = json.loads((build.PRIOR.parent.parent/'traceability-review.json').read_text())
    contexts = {r['citation_key']: Counter(json.dumps(x, sort_keys=True) for x in r['citation_contexts']) for r in index['records']}
    for row in previous['records']:
        assert not Counter(json.dumps(x, sort_keys=True) for x in row['citation_contexts']) - contexts[row['citation_key']]
    text = ' '.join((OUT/'reader.txt').read_text().split())
    for phrase in ['Reusing DAGMA without changing the scientific question',
                   'constructs a ValueError without raising it', '3.125', 'first-layer norm',
                   'They do not show that the optimizer admitted', 'src/VERSION']:
        assert phrase in text, phrase
    evidence = [ref(p, a) for p, a in [
        (OUT/'build-report.json', 'Preserving DAGMA reader'), (OUT/'source-audit.json', '646 source records'),
        (BASE/'traceability-review.json', '175 genuine scholarly PDFs and retained citation contexts'),
        (OUT/'text-layout-review.json', 'All-page extracted text bounds'),
        (OUT/'reader.txt', 'Inspected source-module, units and reuse argument'),
        (WORK/'source-review.json', 'Five original blobs and primary theorem anchors'),
        (WORK/'runtime-probes.json', 'Seven actual bounded source-module cases'),
        (WORK/'exact-results.json', 'Independent domain and mathematical references'),
        (WORK/'independent-arithmetic-review.json', 'Exact rational financial and path checks'),
        (WORK/'proposed-adapter-contract.json', 'Proposed conversion and failure semantics'),
        (WORK/'decision-proposal.json', 'Reference choice and alternatives'),
        (WORK/'omissions-register.json', 'Outstanding build, research and external inputs'),
        (WORK/'publication-preflight-failure.json', 'Preserved preparation failure and correction'),
        (Path(__file__), 'Exact-reader review and transitions')]]
    write(BASE/'release-source-review.json', {
        'status': 'pass', 'issues': [], 'reviewer': work.REVIEWER, 'reviewed_reader': report['pdf'],
        'scope': 'Author source, numerical, mathematical and extracted-text review; reference decision only',
        'preserved_records': 643, 'new_records': 3, 'preserved_compiled_sources': len(kept),
        'original_contexts_retained': True, 'evidence': evidence,
        'findings': [
            'Five original source files match pinned Git blobs and recorded SHA-256 identities; the genuine paper supports the stated domain and limiting premises.',
            'Seven observed source-module cases and domain/derivative oracles support specific wrapper obligations without asserting a failure rate.',
            'Units and nonlinear norm examples preserve causal assumptions and distinguish local derivatives from finite changes.',
            'Reference use is selected with integration disabled; build closure, calibration and later ownership remain explicit.'],
        'limitations': work.LIMITS, 'visual_acceptance': False})
    print(json.dumps({'review': 'pass', 'pages': report['pages'], 'sections': report['dagma_sections']}))


def record():
    reviewed = json.loads((BASE/'release-source-review.json').read_text()); verify_bindings(reviewed)
    state = core.read(ROOT, core.STATE); graph, _, _ = run.combined(ROOT, state)
    node = run.ledger.operation(graph, work.OP)
    decision = json.loads((WORK/'decision-proposal.json').read_text())
    decision.update(manuscript_review=ref(BASE/'release-source-review.json', 'Reviewed preserving manuscript'),
                    compiled_reader=json.loads((OUT/'build-report.json').read_text())['pdf'])
    write(work.OUTPUT, decision)
    receipt = run.ledger.receipt_template(node)
    facts = [
        ('Original repository identity, five pinned source blobs, Apache terms, unpinned dependencies, missing version reference and bounded maintenance evidence are inspected; complete distribution closure is explicitly deferred.',
         ['source-review.json', 'omissions-register.json']),
        ('Target, uncertainty, alternatives, ownership, full costs and revisit trigger are developed in the decision and manuscript; actual source-module probes and independent references support the limits.',
         ['decision-proposal.json', 'runtime-probes.json', 'exact-results.json', 'independent-arithmetic-review.json']),
        ('Reference selection enables no integration capability. A proposed conversion/failure contract and behavioral oracles specify the prerequisites for a later permissible wrapper.',
         ['proposed-adapter-contract.json', 'runtime-probes.json'])]
    receipt.update(outcome='pass', execution='performed', scope='Reviewed reference reuse decision; no installed package or adapter qualification',
                   reviewer=work.REVIEWER, limitations=work.LIMITS, capabilities=[],
                   outputs=[ref(work.OUTPUT, 'Reviewed DAGMA reference decision')], nonexecution_reason='',
                   revisit_trigger=decision['revisit_trigger'],
                   criteria=[{'index': i, 'verdict': 'pass', 'finding': f,
                              'evidence': [ref(WORK/n, n) for n in names]+[ref(BASE/'release-source-review.json', 'Integrated author review')]}
                             for i, (f, names) in enumerate(facts)])
    write(BASE/'operation-receipt.json', receipt); transition('record', work.OP, BASE/'operation-receipt.json')


def publish():
    state = core.read(ROOT, core.STATE); before = core.sha(ROOT/core.STATE)
    assert state['execution_runtime']['active'] is None and work.OP in state['execution_program']['results']
    assert state['reader']['path'] == str(build.OLD.with_suffix('.pdf').relative_to(ROOT))
    report = json.loads((OUT/'build-report.json').read_text()); audit = json.loads((OUT/'source-audit.json').read_text())
    reviewed = json.loads((BASE/'release-source-review.json').read_text()); verify_bindings(reviewed)
    manifest = {'kind': 'working_monograph', 'final_acceptance': False, 'pdf': report['pdf'], 'pages': report['pages'],
        'supersedes': {k: state['reader'][k] for k in ['path', 'sha256']},
        'build_report': ref(OUT/'build-report.json', 'Preserving DAGMA reader'),
        'source_review': ref(BASE/'release-source-review.json', 'Exact-reader author review'),
        'text_layout': ref(OUT/'text-layout-review.json', 'All-page text bounds'),
        'source_artifacts': audit['tex_files'] + reviewed['evidence'] + [ref(work.OUTPUT, 'Recorded reuse decision')],
        'visual_acceptance': False, 'mandatory_repairs_closed': [],
        'changes': ['Develop original-source DAGMA reuse with seven actual boundary cases and a proposed adapter contract.',
                    'Explain domain validity, diagnostics, unit transformations and nonlinear intervention semantics.'],
        'sponsor_binding': 'Preserved sponsor baseline; Q5 reconciliation remains open.'}
    write(BASE/'working-release.json', manifest); binding = ref(BASE/'working-release.json', 'Reviewed DAGMA working successor')
    run.ledger.validate_working_release(ROOT, binding); state['execution_program']['working_releases'].append(binding)
    state['reader'] = {k: report['pdf'][k] for k in ['path', 'sha256']}
    state['reader'].update(pages=report['pages'], status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT, before, state, {'action': 'publish_dagma_reader', 'manifest': binding, 'final_acceptance': False})
    print(json.dumps({'published': state['reader']}))


def renew():
    report = json.loads((OUT/'build-report.json').read_text())
    verify_bindings(json.loads((BASE/'release-source-review.json').read_text()))
    findings = {
        'Q2': 'All 643 inherited source records and citation contexts remain. Three additions bind five pinned originals, primary rereads, actual source-module execution and authored references; 646 records and 175 genuine scholarly PDFs are traceable.',
        'Q3': 'Seven bounded executions of unchanged original linear source expose input, constraint, topology and diagnostic boundaries. Independent derivative/domain and exact rational unit/financial references pass. Full package, nonlinear execution, adapter and statistical qualification remain unclaimed.',
        'Q4': 'Exact stipulated local net derivatives of 180 and -220 USD show why a nonlinear adjacency norm cannot settle a servicing decision. The proposal assigns build, copy, conversion, diagnostic and maintenance costs and requires public/generated merit before costly bank trials. No real prices or bank ROI are asserted.'}
    for q, finding in findings.items():
        identifier = 'PROPOSAL.'+q; state = core.read(ROOT, core.STATE)
        assert state['reader']['sha256'] == report['pdf']['sha256']
        previous = state['execution_runtime']['results'][identifier]; old = json.loads((ROOT/previous['path']).read_text())
        folder = BASE/q; folder.mkdir(exist_ok=False)
        evidence = [previous, ref(BASE/'working-release.json', 'Exact current reader'),
                    ref(BASE/'release-source-review.json', 'Inspected delta'), ref(work.OUTPUT, 'Reference disposition'),
                    ref(WORK/'independent-arithmetic-review.json', 'Reproduced illustrative financial meaning'), ref(Path(__file__), 'Review findings')]
        write(folder/'reopen.json', {'reason': 'Changed reader requires preserved successor author review.',
              'prior_result': previous, 'reviewed_reader': report['pdf'], 'evidence': evidence,
              'next_action': 'Record the reviewed DAGMA delta, preserving all scope limits.'})
        transition('reopen', identifier, folder/'reopen.json')
        state = core.read(ROOT, core.STATE); graph, _, _ = run.combined(ROOT, state); node = run.ledger.operation(graph, identifier)
        attempt = len(state['execution_runtime']['review_history'][identifier])
        output = ROOT/run.review_output_paths(node, state['reader'], attempt)[0]
        limits = list(dict.fromkeys(old['limitations']+work.LIMITS)); scope = 'Author exact-reader proposal delta review'
        write(output, {'operation': identifier, 'status': 'pass', 'criterion': node['criteria'][0],
              'reviewer': work.REVIEWER, 'reviewed_reader': report['pdf'], 'review_attempt': attempt,
              'acceptance_scope': 'proposal_only', 'scope': scope, 'findings': [finding], 'evidence': evidence,
              'limitations': limits, 'visual_acceptance': False})
        receipt = run.ledger.receipt_template(node)
        receipt.update(outcome='pass', execution='performed', scope=scope, reviewer=work.REVIEWER, limitations=limits,
                       reviewed_reader=report['pdf'], review_attempt=attempt, acceptance_scope='proposal_only',
                       outputs=[ref(output, 'Current-reader '+q+' author review')], nonexecution_reason='', revisit_trigger='',
                       criteria=[{'index': 0, 'verdict': 'pass', 'finding': finding, 'evidence': evidence}])
        write(folder/'operation-receipt.json', receipt); transition('record', identifier, folder/'operation-receipt.json')
    print(json.dumps({'exact_reader_reviews': 'Q2-Q4 pass', 'Q1_Q5': 'open'}))


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('command', choices=['review', 'record', 'publish', 'renew']); args = p.parse_args()
    {'review': review, 'record': record, 'publish': publish, 'renew': renew}[args.command]()
