#!/usr/bin/env python3
"""Publish the scoped pcalg proposal choice and preserve all predecessor evidence."""
import json
from pathlib import Path
import re

import build_integrated_monograph_v12 as shared
import master_control as core
import run_program as run

ROOT = core.ROOT
BASE = ROOT/'docs/program/execution/2026-10-13/pcalg-reuse'
OUT = BASE/'reader'
OP = 'SW.DECISION.seed_046'
ref = shared.ref


def write(path, value):
    assert not path.exists(), 'Preserve delivered evidence: ' + str(path)
    core.write(path, value)


def main():
    state = core.read(ROOT, core.STATE)
    before = core.sha(ROOT/core.STATE)
    assert state['execution_runtime']['active']['operation'] == OP
    assert state['reader']['path'] == 'docs/causal_proposal_commercial_temporal_2026-10-13.pdf'
    report = json.loads((OUT/'build-report.json').read_text())
    audit = json.loads((OUT/'source-audit.json').read_text())
    old_audit = json.loads((ROOT/'docs/program/execution/2026-10-13/commercial-temporal/reader/source-audit.json').read_text())
    for name in ['source-audit.json', 'author-review.json', 'adapter-contract-v2.json', 'reproduction-review.json',
                 'plan-review-02.json', 'prepared-inputs.json', 'reader/source-audit.json']:
        shared.verify_refs(json.loads((BASE/name).read_text()))
    old_driver = ROOT/'docs/causal_proposal_commercial_temporal_2026-10-13.tex'
    new_driver = ROOT/report['driver']['path']
    expected = old_driver.read_text().replace(
        r'\input{program/execution/2026-10-13/tetrad-reuse/decision.tex}',
        r'\input{program/execution/2026-10-13/tetrad-reuse/decision.tex}'+'\n'+
        r'\input{program/execution/2026-10-13/pcalg-reuse/decision.tex}', 1).replace(
        'program/execution/2026-10-13/commercial-temporal/refs}',
        'program/execution/2026-10-13/commercial-temporal/refs,program/execution/2026-10-13/pcalg-reuse/refs}', 1)
    assert new_driver.read_text() == expected
    old_files = [r for r in old_audit['tex_files'] if r['path'] != str(old_driver.relative_to(ROOT))]
    for item in old_files:
        core.bound(ROOT, item)
    old_sources = {s['integrated_citation_key']: s for s in old_audit['sources']}
    new_sources = {s['integrated_citation_key']: s for s in audit['sources']}
    assert all(new_sources[k] == v for k, v in old_sources.items())
    assert set(new_sources)-set(old_sources) == {'exec13_pcalg_reuse_primary', 'exec13_pcalg_reuse_examples'}
    assert (BASE/'exact-results.json').read_bytes() == (BASE/'exact-replay.json').read_bytes()
    text = re.sub(r'\s+', ' ', (OUT/'reader.txt').read_text())
    for phrase in ['selects this pinned path for local prototype',
                   'p value of one', '36 deliberate transposes', '120 currency units',
                   'Runtime qualification remains open']:
        assert phrase in text, phrase
    assert not any('Overfull' in w or 'undefined' in w.lower() for w in report['warnings'])
    evidence_names = ['primary-review.json', 'source-audit.json', 'adapter-contract-v2.json',
        'decision.md', 'author-review.json', 'reproduction-review.json', 'exact-results.json',
        'exact-replay.json', 'fallback-trace.json', 'environment-inspection.json', 'plan-review-02.json']
    source_review = {'status': 'pass', 'issues': [], 'reviewer': {'name': 'Codex author/coordinator', 'kind': 'author'},
        'scope': 'New pcalg section source/claim review and preserving reader delta; no whole-survey or visual acceptance',
        'old_compiled_files_unchanged': len(old_files), 'prior_citation_records_unchanged': len(old_sources),
        'new_citation_records': 2, 'driver_change': 'One added section input and one bibliography entry path only',
        'findings': ['Pinned source statements inspected and independently verified against Git blobs.',
            'All numerical/encoding demonstrations explicitly project references; no pcalg runtime claimed.',
            'Source normalization and finite-fallback hazards motivate a strict new contract, without a valid-input failure claim.',
            'Local integration eligibility does not require a completed adapter; it does not confer runtime qualification.',
            'Exact financial values, named matrix meanings and local/global multiset distinctions survive text extraction.',
            'No unresolved citations/references, overfull boxes, empty pages or text outside physical bounds.'],
        'evidence': [ref(BASE/name, name) for name in evidence_names] + [
            ref(OUT/'build-report.json', 'Compiled exact current reader'), ref(OUT/'text-layout-review.json', 'Physical text bounds')],
        'visual_acceptance': False, 'limitation': 'Rendered image review pending fresh image allowance; this is extracted-text inspection only.'}
    write(BASE/'release-source-review.json', source_review)
    names = evidence_names + ['release-source-review.json', 'prepared-inputs.json', 'refs.bib', 'source-selection.json', 'blob-verification.json']
    release = {'kind': 'working_monograph', 'final_acceptance': False, 'pdf': report['pdf'], 'pages': report['pages'],
        'supersedes': {k: state['reader'][k] for k in ['path', 'sha256']},
        'build_report': ref(OUT/'build-report.json', 'Bounded pcalg integration build'),
        'source_review': ref(BASE/'release-source-review.json', 'Reviewed source/claim and reader delta'),
        'text_layout': ref(OUT/'text-layout-review.json', 'Whole-reader physical text bounds'),
        'source_artifacts': audit['tex_files'] + [ref(BASE/name, 'Reviewed new-section evidence') for name in names] +
            [ref(ROOT/'tools'/name, 'Reproduction/build/publication code') for name in
             ['pcalg_reuse_examples_20261013.py', 'pcalg_fallback_trace_20261013.R', 'prepare_pcalg_reuse_20261013.py',
              'build_pcalg_reuse_reader_20261013.py', 'publish_pcalg_reuse_reader_20261013.py']],
        'visual_acceptance': False, 'mandatory_repairs_closed': [],
        'changes': ['Selected pinned pcalg path for local integration under a corrected strict R design.',
            'Explained conflict preservation, finite CI fallbacks, matrix directions and IDA admission hazards.',
            'Added exact multisets, monetary units,54 independent encoding references and36 transpose checks.'],
        'sponsor_binding': 'Sponsor remains a prior preserved document; Q5 reconciliation is open.'}
    write(BASE/'working-release.json', release)
    binding = ref(BASE/'working-release.json', 'Reviewed pcalg working monograph')
    run.ledger.validate_working_release(ROOT, binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader'] = {k: report['pdf'][k] for k in ['path', 'sha256']}
    state['reader'].update(pages=report['pages'], status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT, before, state, {'action': 'publish_pcalg_reuse_working_reader', 'manifest': binding,
        'original_gap_qualification': False, 'final_acceptance': False})
    graph, _, _ = run.combined(ROOT, state)
    node = run.ledger.operation(graph, OP)
    output = ROOT/node['outputs'][0]
    decision = json.loads(output.read_text())
    assert decision['decision'] == 'integrate' and decision['integration_allowed'] is True
    assert decision['runtime_qualification'] is False
    receipt = run.ledger.receipt_template(node)
    receipt.update(outcome='pass', execution='performed',
        scope='Reviewed pcalg reuse choice selects a pinned restricted R route for local implementation; no engine execution or distribution acceptance.',
        reviewer={'name': 'Codex author/coordinator', 'kind': 'author'},
        limitations=['Actual package/dependency installation and engine fixtures remain in IN.ADAPTER.R.',
            'Independent examples are not a pcalg run or adapter conformance result.',
            'No general sampling calibration, bank qualification, independent acceptance or distribution permission.',
            'Whole proposal and rendered visual acceptance remain open.'],
        capabilities=['integration_allowed'], outputs=[ref(output, 'Actual scoped integration choice')],
        nonexecution_reason='', revisit_trigger=decision['revisit_trigger'])
    receipt['criteria'] = [
        {'index': 0, 'verdict': 'pass', 'finding': 'Canonical package/algorithm aliases, exact source revision, declared GPL>=2,17 imports,3 linking declarations and bounded maintenance evidence inspected. Ten source files match the selected Git tree.',
         'evidence': [ref(BASE/'primary-review.json', 'Pinned primary inspection'), ref(BASE/'source-audit.json', 'Audited version, claims and limitations')]},
        {'index': 1, 'verdict': 'pass', 'finding': 'Linear IID CPDAG and derivative-multiset scope, sampling uncertainty limits, alternatives, complete-request cost, responsibilities and change triggers developed in the integrated reader.',
         'evidence': [ref(output, 'Reuse decision and obligations'), ref(BASE/'author-review.json', 'Substantive author review'), binding]},
        {'index': 2, 'verdict': 'pass', 'finding': 'integration_allowed selects local implementation at the permissible pinned source only. Strict successor contract and independent behavioral references are supplied; runtime execution and distribution remain distinct unawarded claims. No circular requirement for an adapter that is not yet eligible to be built.',
         'evidence': [ref(BASE/'adapter-contract-v2.json', 'Required corrected conversion/failure contract'),
            ref(BASE/'reproduction-review.json', 'Independent exact references'), ref(BASE/'plan-review-02.json', 'Reviewed noncircular local admission scope'), ref(output, 'Bounded capability choice')]}]
    receipt_path = BASE/(OP+'.receipt.json')
    write(receipt_path, receipt)
    print(json.dumps({'published': state['reader'], 'receipt': str(receipt_path.relative_to(ROOT)),
                      'integration_allowed': True, 'runtime_executed': False}))


if __name__ == '__main__':
    main()
