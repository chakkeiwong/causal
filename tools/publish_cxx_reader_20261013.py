#!/usr/bin/env python3
"""Publish a reviewed C++ survey delta without claiming full cell acceptance."""
import json
from pathlib import Path
import re

import audit_reader_traceability_v2_20261013 as trace
import build_integrated_monograph_v12 as shared
import master_control as core
import run_program as run

ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-13/cxx-discovery'
OUT = BASE / 'reader'
OP = 'SW.CELL.discovery_iid.Cxx'
ref = shared.ref


def main():
    state = core.read(ROOT, core.STATE)
    before = core.sha(ROOT / core.STATE)
    report = json.loads((OUT / 'build-report.json').read_text())
    old_driver = ROOT / 'docs/causal_proposal_workspace_2026-10-13.tex'
    assert state['reader']['path'] == str(old_driver.with_suffix('.pdf').relative_to(ROOT))
    prior = json.loads((ROOT / 'docs/program/execution/2026-10-13/workspace/reader/source-audit.json').read_text())
    audit = json.loads((OUT / 'source-audit.json').read_text())
    for name in ['source-audit.json', 'prepared-inputs.json', 'reader/source-audit.json', 'identity-review.json']:
        shared.verify_refs(json.loads((BASE / name).read_text()))
    marker = r'\input{program/execution/2026-10-13/pcalg-reuse/decision.tex}'
    expected = old_driver.read_text().replace(marker, marker + '\n' +
        r'\input{program/execution/2026-10-13/cxx-discovery/comparison.tex}', 1).replace(
        'program/execution/2026-10-13/workspace/refs}',
        'program/execution/2026-10-13/workspace/refs,program/execution/2026-10-13/cxx-discovery/refs}', 1)
    driver = ROOT / report['driver']['path']
    assert driver.read_text() == expected
    old_files = [x for x in prior['tex_files'] if x['path'] != str(old_driver.relative_to(ROOT))]
    for item in old_files:
        core.bound(ROOT, item)
    previous = {s['integrated_citation_key']: s for s in prior['sources']}
    current = {s['integrated_citation_key']: s for s in audit['sources']}
    assert all(current[k] == v for k, v in previous.items())
    assert len(current)-len(previous) == 12
    assert (BASE / 'exact-results.json').read_bytes() == (BASE / 'exact-replay.json').read_bytes()
    assert not any('Overfull' in x or 'undefined' in x.lower() for x in report['warnings'])
    text = re.sub(r'\s+', ' ', (OUT / 'reader.txt').read_text())
    for phrase in ['100,000', '200,000', 'seventeen-candidate', 'native runtime performance',
                   'dropping the negative', 'conditional entropy', 'C++20']:
        assert phrase.lower() in text.lower(), phrase
    tracing = trace.audit(driver, OUT / 'source-audit.json')
    core.write(BASE / 'traceability-review.json', tracing)
    assert tracing['status'] == 'pass', tracing['issues']
    names = ['plan-review.json', 'continuation-plan-review.json', 'continuation-acquisition.json',
             'candidate-register.json', 'omissions-register.json', 'identity-review.json',
             'source-audit.json', 'exact-results.json', 'exact-replay.json', 'substantive-review.md',
             'prepared-inputs.json', 'refs.bib', 'initial-build-report.json', 'traceability-review.json',
             'traceability-review-initial.json', 'anchor-compatibility-review.json']
    source_review = {
        'status': 'pass', 'issues': [], 'reviewer': {'name': 'Codex author/coordinator', 'kind': 'author'},
        'scope': 'Claim-limited native comparison and preserving working-reader delta; full cell coverage remains inconclusive',
        'old_compiled_files_unchanged': len(old_files), 'prior_citation_records_unchanged': len(previous),
        'new_citation_records': 12,
        'findings': ['All seventeen bounded candidates have documented dispositions with primary/project claim support.',
                     '43 raw source blobs match selected Git tree entries; decoded API content matches its Git blob.',
                     'Exact examples replay, with independent topological checks and six node permutations.',
                     'Missing rights, missing scorer and secondary-source gaps remain explicit; no paper-summary substitution.',
                     'One initial table overflow was repaired by breaking the long repository label; final build has no overfull boxes.',
                     'No third-party native runtime, coverage, bank or complete repair acceptance is claimed.'],
        'evidence': [ref(BASE / n, n) for n in names] +
                    [ref(BASE / 'comparison.tex', 'Integrated connected native comparison'),
                     ref(OUT / 'build-report.json', 'Final compilation and citation resolution'),
                     ref(OUT / 'text-layout-review.json', 'Whole-reader physical text bounds')],
        'visual_acceptance': False}
    core.write(BASE / 'release-source-review.json', source_review)
    code = ['audit_cxx_discovery_20261013.py', 'cxx_discovery_examples_20261013.py',
            'audit_reader_traceability_v2_20261013.py',
            'build_cxx_reader_20261013.py', 'publish_cxx_reader_20261013.py']
    release = {'kind': 'working_monograph', 'final_acceptance': False,
               'pdf': report['pdf'], 'pages': report['pages'],
               'supersedes': {k: state['reader'][k] for k in ['path', 'sha256']},
               'build_report': ref(OUT / 'build-report.json', 'Native comparison integration'),
               'source_review': ref(BASE / 'release-source-review.json', 'Reviewed preserving delta'),
               'text_layout': ref(OUT / 'text-layout-review.json', 'Physical text bounds'),
               'source_artifacts': audit['tex_files'] +
                   [ref(BASE / n, 'Preserved new evidence') for n in names + ['release-source-review.json']] +
                   [ref(ROOT / 'tools' / n, 'Audit/reproduction/build/publication code') for n in code],
               'visual_acceptance': False, 'mandatory_repairs_closed': [],
               'changes': ['Integrated seventeen-candidate native/hosted/inference comparison and selection reasons.',
                           'Added exact funding orientation, graph ambiguity, entropy and coarsening constructions.',
                           'Preserved incomplete rights/alias/source coverage and all predecessor evidence.'],
               'sponsor_binding': 'Prior sponsor preserved; exact reader reconciliation remains Q5 work.'}
    core.write(BASE / 'working-release.json', release)
    binding = ref(BASE / 'working-release.json', 'Reviewed native discovery working successor')
    run.ledger.validate_working_release(ROOT, binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader'] = {k: report['pdf'][k] for k in ['path', 'sha256']}
    state['reader'].update(pages=report['pages'], status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT, before, state, {'action': 'publish_cxx_working_reader', 'manifest': binding,
                                  'original_gap_qualification': False, 'final_acceptance': False})
    graph, _, _ = run.combined(ROOT, state)
    node = run.ledger.operation(graph, OP)
    coverage = {
        'operation': OP, 'outcome': 'inconclusive', 'execution': 'performed',
        'scope': 'Bounded seventeen-candidate native discovery survey integrated in the working monograph',
        'candidate_register': ref(BASE / 'candidate-register.json', 'Two complete finite queries and direct/known leads'),
        'source_audit': ref(BASE / 'source-audit.json', 'Inspected primary text and exact project examples'),
        'review': ref(BASE / 'substantive-review.md', 'Author review'),
        'omissions': ref(BASE / 'omissions-register.json', 'Essential source/rights and next-action register'),
        'working_reader': binding, 'runtime_qualified': False, 'full_cell_coverage_accepted': False}
    output = ROOT / node['outputs'][0]
    core.write(output, coverage)
    receipt = run.ledger.receipt_template(node)
    receipt.update(outcome='inconclusive', execution='performed', scope=coverage['scope'],
                   reviewer={'name': 'Codex author/coordinator', 'kind': 'author'},
                   limitations=['Essential rights, alias and secondary implementation questions remain unresolved.',
                                'No third-party engine or adapter executed; no sampling calibration or bank estimate.',
                                'No MR01/S2 depth or rendered visual acceptance.'],
                   outputs=[ref(output, 'Reviewed bounded coverage disposition')], nonexecution_reason='',
                   revisit_trigger='Acquire the candidate-specific missing rights/delegated sources in the omissions register and create a reviewed successor coverage operation.')
    receipt['criteria'] = [
        {'index': 0, 'verdict': 'inconclusive',
         'finding': 'All eleven finite-query results and six known/direct leads are identified under the cutoff; complete secondary and alias resolution remains open.',
         'evidence': [ref(BASE / 'candidate-register.json', 'Seventeen candidates and alias distinctions'),
                      ref(BASE / 'continuation-acquisition.json', 'Bounded follow-up acquisition')]},
        {'index': 1, 'verdict': 'pass',
         'finding': 'New technical claims bind primary bytes, versions, inspected anchors and hashes; examples reproduce; only software/project records are newly cited.',
         'evidence': [ref(BASE / 'source-audit.json', 'Primary/project claim support'),
                      ref(BASE / 'identity-review.json', '43 source/tree blob matches'),
                      ref(BASE / 'traceability-review.json', 'Exact-reader traceability review'),
                      ref(BASE / 'release-source-review.json', 'Claims and delta review')]},
        {'index': 2, 'verdict': 'inconclusive',
         'finding': 'Alternatives, rejections and omissions are explicit; essential unavailable rights and incomplete implementation provenance are not waived.',
         'evidence': [ref(BASE / 'omissions-register.json', 'Candidate-specific gaps and actions'), binding]}]
    path = BASE / (OP + '.receipt.json')
    core.write(path, receipt)
    print(json.dumps({'published': state['reader'], 'receipt': str(path.relative_to(ROOT)),
                      'full_cell_coverage': 'inconclusive'}))


if __name__ == '__main__':
    main()
