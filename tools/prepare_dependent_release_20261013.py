#!/usr/bin/env python3
"""Bind the completed, reviewed learning/discovery reader for ledger delivery."""
import json
from pathlib import Path
import re

import build_integrated_monograph_v12 as shared
import master_control as core

ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-13/dependent-learner'
DISCOVERY = ROOT / 'docs/program/execution/2026-10-13/discovery-journey'
OUT = BASE / 'reader'
ref = shared.ref


def main():
    state = core.read(ROOT, core.STATE)
    report = json.loads((OUT / 'build-report.json').read_text())
    audit = json.loads((OUT / 'source-audit.json').read_text())
    prior = json.loads((ROOT / 'docs/program/execution/2026-10-13/cxx-discovery/reader/source-audit.json').read_text())
    tracing = json.loads((BASE / 'traceability-review.json').read_text())
    assert tracing['status'] == 'pass' and not tracing['issues']
    assert tracing['pdf'] == {**report['pdf'], 'anchor': tracing['pdf']['anchor']}
    assert state['reader']['sha256'] == report['predecessor_pdf']['sha256']
    for path in [BASE / 'argument-review.json', BASE / 'source-audit.json',
                 BASE / 'prepared-inputs.json', OUT / 'source-audit.json',
                 DISCOVERY / 'local-review.json']:
        shared.verify_refs(json.loads(path.read_text()))
    previous = {s['integrated_citation_key']: s for s in prior['sources']}
    current = {s['integrated_citation_key']: s for s in audit['sources']}
    assert all(current[k] == v for k, v in previous.items())
    old_files = [x for x in prior['tex_files'] if x['path'] != report['predecessor_pdf']['path'].replace('.pdf', '.tex')]
    for item in old_files:
        core.bound(ROOT, item)
    assert len(current) - len(previous) == 2
    assert not any('overfull' in w.lower() or 'undefined' in w.lower() or 'missing character' in w.lower() for w in report['warnings'])
    text = re.sub(r'\s+', ' ', (OUT / 'reader.txt').read_text())
    for phrase in ['98 slots', '24 case comparisons', '0/512', 'known', '0.523255814', '18,685']:
        assert phrase in text, phrase
    names = ['plan-review.md', 'primary-reading.json', 'source-audit.json',
             'exact-results.json', 'argument-review.json', 'operation-receipt.json',
             'prepared-inputs.json', 'refs.bib', 'traceability-review.json', 'early-audit-ordering.json']
    dnames = ['plan-review.md', 'argument-review.json', 'fixtures.json', 'local-journal.json',
              'local-review.json', 'local-receipt.json', 'design-receipt.json', 'registration-control.json']
    evidence = ([ref(BASE / name, name) for name in names]
                + [ref(DISCOVERY / name, name) for name in dnames]
                + [ref(OUT / 'build-report.json', 'Final compilation, page map and warnings'),
                   ref(OUT / 'text-layout-review.json', 'Whole-reader text bounds')])
    review = {
        'status': 'pass', 'issues': [],
        'reviewer': {'name': 'Codex author/coordinator', 'kind': 'author'},
        'scope': 'Claim-limited working-reader delta, not whole-proposal acceptance',
        'old_compiled_files_unchanged': len(old_files),
        'prior_citation_records_unchanged': len(previous), 'new_citation_records': 2,
        'findings': [
            'Registered workflow reports 98 expectation checks and 24 parity comparisons with all unavailable/refused cases retained; computed responses are not all effect estimates.',
            'The independent-pilot finite-dependence argument retains the repaired R05-v2 failures and explicitly excludes its unbounded Gaussian AR law.',
            'Exact nuisance, optimizer and projection references support the restricted derivation; no final repeated-sampling study or useful bank precision is claimed.',
            'The two additions appear at printed pages 404–405 and 490–497. Their extracted text and final source identities were inspected.',
            'Final compilation resolves references and citations without overfull boxes or missing-glyph warnings; inherited underfull warnings are retained.',
            'Earlier audit ordering failure is preserved and resolved by auditing the completed final build.'
        ], 'evidence': evidence, 'visual_acceptance': False,
        'visual_limit': 'Inherited session image allowance exhausted; text checks do not confer visual acceptance.'}
    core.write(BASE / 'release-source-review.json', review)
    code = ['prepare_dependent_release_20261013.py', 'build_dependent_reader_20261013.py',
            'dependent_learner_argument_20261013.py', 'finalize_dependent_argument_20261013.py',
            'discovery_journey_20261013.py', 'freeze_discovery_journey_20261013.py',
            'audit_reader_traceability_v2_20261013.py']
    release = {
        'kind': 'working_monograph', 'final_acceptance': False,
        'pdf': report['pdf'], 'pages': report['pages'],
        'supersedes': {k: state['reader'][k] for k in ['path', 'sha256']},
        'build_report': ref(OUT / 'build-report.json', 'Completed 562-page build'),
        'source_review': ref(BASE / 'release-source-review.json', 'Reviewed claim-limited additions'),
        'text_layout': ref(OUT / 'text-layout-review.json', 'Physical text bounds'),
        'source_artifacts': audit['tex_files'] + evidence
            + [ref(BASE / 'release-source-review.json', 'Release review')]
            + [ref(ROOT / 'tools' / name, 'Preserved construction/reproduction code') for name in code],
        'visual_acceptance': False, 'mandatory_repairs_closed': [],
        'changes': ['Integrated the registered discovery workflow exercise.',
                    'Integrated the restricted dependent-learning derivation and exact references.'],
        'sponsor_binding': 'Prior sponsor preserved; exact-reader reconciliation remains Q5 work.'}
    core.write(BASE / 'working-release.json', release)
    print(json.dumps({'manifest': str((BASE / 'working-release.json').relative_to(ROOT)),
                      'pages': release['pages'], 'source_review': 'pass', 'final_acceptance': False}))


if __name__ == '__main__':
    main()
