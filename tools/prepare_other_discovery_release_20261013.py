#!/usr/bin/env python3
"""Publish scoped survey value while retaining the unresolved coverage outcome."""
import json
from pathlib import Path
import re

import build_other_discovery_reader_20261013 as builder
import build_integrated_monograph_v12 as shared
import master_control as core
import run_program as run

ROOT = core.ROOT
BASE = builder.BASE
OUT = builder.OUT
OP = 'SW.CELL.discovery_iid.other_relevant'
ref = shared.ref


def main():
    state = core.read(ROOT, core.STATE)
    report = json.loads((OUT / 'build-report.json').read_text())
    audit = json.loads((OUT / 'source-audit.json').read_text())
    prior = json.loads(builder.PRIOR_AUDIT.read_text())
    trace = json.loads((BASE / 'traceability-review.json').read_text())
    assert trace['status'] == 'pass' and trace['issues'] == []
    assert trace['pdf']['sha256'] == report['pdf']['sha256']
    assert state['reader']['sha256'] == report['predecessor_pdf']['sha256']
    checked_paths = [BASE / n for n in ['source-audit.json', 'candidate-register.json', 'author-review.json', 'exact-review.json']]
    checked_paths += [builder.INPUT / n for n in ['source-audit.json', 'prepared-inputs.json']] + [OUT / 'source-audit.json']
    for p in checked_paths:
        shared.verify_refs(json.loads(p.read_text()))
    old = {x['integrated_citation_key']: x for x in prior['sources']}
    new = {x['integrated_citation_key']: x for x in audit['sources']}
    assert len(new)-len(old) == 12 and all(new[k] == v for k, v in old.items())
    for item in prior['tex_files']: core.bound(ROOT, item)
    assert builder.DRIVER.read_text() == builder.expected_driver()
    assert report['pages'] > 587
    assert not any(any(t in w.lower() for t in ['overfull', 'undefined', 'missing character']) for w in report['warnings'])
    text = re.sub(r'\s+', ' ', (OUT / 'reader.txt').read_text())
    for phrase in ['Discovery beyond the principal language interfaces', '2.32635', '1.960',
                   'mkbd_ci_test', 'GNU Library General Public License', 'dimensionless']:
        assert phrase in text, phrase
    bounds = json.loads((OUT / 'text-layout-review.json').read_text())
    assert bounds['status'] == 'pass' and bounds['pages'] == report['pages']
    assert (BASE / 'previous-fetch-manifest.json').read_bytes() == (ROOT / 'docs/literature/fetch-manifest.json').read_bytes()
    names = ['plan-review.md', 'comparison.tex', 'acquisition-results.json', 'source-audit.json',
             'candidate-register.json', 'omissions-register.json', 'exact-results.json', 'exact-replay.json',
             'exact-review.json', 'author-review.json', 'traceability-review.json',
             'reader-input/source-audit.json', 'reader-input/prepared-inputs.json', 'reader-input/refs.bib']
    evidence = [ref(BASE / n, n) for n in names]
    review = {'status': 'pass', 'issues': [], 'reviewer': {'name': 'Codex author/coordinator', 'kind': 'author'},
        'scope': 'Scoped eleven-family primary comparison, exact example and preserving working reader',
        'prior_citation_records_unchanged': len(old), 'new_citation_records': 12,
        'pages': report['other_discovery'],
        'findings': ['Every predecessor source record and manuscript file is preserved.',
            'Eleven selected families have dated primary inspection, explicit reuse decisions and source-level adverse findings.',
            'Three Gaussian laws share the displayed covariance and have different interventions; independent finite second-moment checks and rational replay pass.',
            'All 85 discovered/named candidates are retained; 74 still lack primary inspection. The full cell remains inconclusive.',
            'Compilation, source traceability and extracted text/bounds pass; no software runtime, independent review or visual acceptance is asserted.'],
        'evidence': evidence+[ref(OUT / 'build-report.json', 'Final bounded build'), ref(OUT / 'text-layout-review.json', 'Text bounds')],
        'visual_acceptance': False, 'MR01_acceptance': False, 'runtime_qualification': False}
    core.write(BASE / 'release-source-review.json', review)
    code = ['other_discovery_examples_20261013.py', 'audit_other_discovery_20261013.py',
            'review_other_discovery_20261013.py', 'build_other_discovery_reader_20261013.py',
            'prepare_other_discovery_release_20261013.py']
    release = {'kind': 'working_monograph', 'final_acceptance': False, 'pdf': report['pdf'], 'pages': report['pages'],
        'supersedes': {k: state['reader'][k] for k in ['path', 'sha256']},
        'build_report': ref(OUT / 'build-report.json', 'Other-language discovery working reader'),
        'source_review': ref(BASE / 'release-source-review.json', 'Reviewed scoped comparison and preserved evidence'),
        'text_layout': ref(OUT / 'text-layout-review.json', 'Physical text bounds'),
        'source_artifacts': audit['tex_files']+evidence+[ref(BASE / 'release-source-review.json', 'Release review')]
            +[ref(ROOT / 'tools' / n, 'Preserved source/review/build code') for n in code],
        'visual_acceptance': False, 'mandatory_repairs_closed': [],
        'changes': ['Integrated eleven-family Julia/Rust/MATLAB/JavaScript comparison, reuse conditions and finite graph-contract examples.'],
        'sponsor_binding': 'Prior sponsor preserved; whole-reader coherence remains Q5 work.'}
    core.write(BASE / 'working-release.json', release)
    binding = ref(BASE / 'working-release.json', 'Reviewed preserving other-language discovery reader')
    run.ledger.validate_working_release(ROOT, binding)
    output = ROOT / 'docs/program/comprehensive-v14/work' / OP / 'coverage-review.json'
    assert not output.exists(), 'Preserve earlier coverage output'
    coverage = {'operation': OP, 'outcome': 'inconclusive', 'execution': 'performed',
        'scope': 'Bounded 85-candidate register with eleven primary-inspected families integrated in the monograph',
        'candidate_register': ref(BASE / 'candidate-register.json', 'All known candidates and alias distinctions'),
        'source_audit': ref(builder.INPUT / 'source-audit.json', 'Dated inspected technical and rights sources'),
        'review': ref(BASE / 'author-review.json', 'Author claim and scope review'),
        'omissions': ref(BASE / 'omissions-register.json', 'Unresolved candidates, scholarly originals and rights'),
        'working_reader': binding, 'full_cell_coverage_accepted': False, 'runtime_qualified': False,
        'continuation': 'Inspect the remaining candidate originals and bounded registry/language routes; execute matched qualification only under a registered future protocol.'}
    core.write(output, coverage)
    graph, _, _ = run.combined(ROOT, state); node = run.ledger.operation(graph, OP)
    receipt = run.ledger.receipt_template(node)
    receipt.update(outcome='inconclusive', execution='performed',
        scope='Developed other-language discovery comparison and exact semantic examples; census/qualification remains open',
        reviewer=review['reviewer'], limitations=['74 metadata-only candidates remain and query coverage is bounded.',
            'Named unacquired scholarly originals receive no theorem or empirical-performance credit.',
            'Source comparison and project arithmetic do not qualify runtime, banks or full MR01 coverage.',
            'Visual and independent acceptance remain pending.'], outputs=[ref(output, 'Actual coverage outcome')],
        nonexecution_reason='', revisit_trigger='Further dated candidate/original/rights inspection and registered matched runtime evaluation for specific stronger claims.')
    receipt['criteria'] = [
        {'index': 0, 'verdict': 'inconclusive', 'finding': 'All 85 returned/named candidates and inspected aliases are recorded under bounded queries; 74 candidates and broader registry/language routes remain uninspected, so full coverage is not accepted.',
         'evidence': [ref(BASE / 'candidate-register.json', 'Finite query and candidate record'), ref(BASE / 'plan-review.md', 'Stopping rule')]},
        {'index': 1, 'verdict': 'pass', 'finding': 'New manuscript claims bind primary bytes, cutoff versions, hashes, inspected anchors and claim boundaries; exact project examples reproduce; no unavailable scholarly original is cited.',
         'evidence': [ref(builder.INPUT / 'source-audit.json', 'Claim-source mapping'), ref(BASE / 'exact-review.json', 'Independent calculations'), ref(BASE / 'traceability-review.json', 'Exact-reader traceability')]},
        {'index': 2, 'verdict': 'pass', 'finding': 'Each selected family has a conditional integrate/adopt/port/defer/reject disposition. Missing primary candidates, source arguments and rights remain explicit without an absence claim or source waiver.',
         'evidence': [ref(BASE / 'comparison.tex', 'Substantive alternatives'), ref(BASE / 'omissions-register.json', 'Unresolved sources and remedies'), binding]}]
    core.write(BASE / 'operation-receipt.json', receipt)
    print(json.dumps({'pages': report['pages'], 'outcome': 'inconclusive', 'selected_families': 11,
        'manifest': str((BASE / 'working-release.json').relative_to(ROOT)),
        'receipt': str((BASE / 'operation-receipt.json').relative_to(ROOT))}))


if __name__ == '__main__':
    main()
