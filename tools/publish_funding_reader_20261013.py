#!/usr/bin/env python3
"""Prepare a reviewed working funding release without granting final acceptance."""
import json
from pathlib import Path
import re

import build_funding_reader_20261013 as b
import build_integrated_monograph_v12 as shared
import master_control as core
import run_program as control

ROOT, BASE, OUT = b.ROOT, b.BASE, b.OUT
ref = shared.ref


def main():
    assert not (BASE / 'working-release.json').exists(), 'Preserve completed release'
    state = core.read(ROOT, core.STATE)
    build = json.loads((OUT / 'build-report.json').read_text())
    audit = json.loads((OUT / 'source-audit.json').read_text())
    prior = json.loads(b.PRIOR_AUDIT.read_text())
    trace = json.loads((BASE / 'traceability-review.json').read_text())
    bounds = json.loads((OUT / 'text-layout-review.json').read_text())
    assert trace['status'] == bounds['status'] == 'pass' and trace['issues'] == []
    assert trace['pdf']['sha256'] == build['pdf']['sha256']
    assert state['reader']['sha256'] == build['predecessor_pdf']['sha256']
    assert build['pages'] == bounds['pages'] == 601 and build['cited_records'] == 446
    assert not any(any(t in w.lower() for t in ['overfull', 'undefined', 'missing character']) for w in build['warnings'])
    assert b.DRIVER.read_text() == b.expected_driver()
    old = {x['integrated_citation_key']: x for x in prior['sources']}
    new = {x['integrated_citation_key']: x for x in audit['sources']}
    assert len(old) == 443 and len(new)-len(old) == 3 and all(new[k] == v for k, v in old.items())
    for item in prior['tex_files']: core.bound(ROOT, item)
    for name in ['source-audit.json', 'manuscript-review.json', 'prepared-inputs.json', 'local-review.json', 'local-receipt.json']:
        shared.verify_refs(json.loads((BASE / name).read_text()))
    shared.verify_refs(audit)
    text = (OUT / 'reader.txt').read_text()
    flat = re.sub(r'\s+', ' ', text)
    for phrase in ['0.49501', '28/15', '56.46', '451', '118', 'unknown inclusion', 'two disclosed harness repairs']:
        assert phrase in flat, phrase
    pages = text.split('\f')
    marker = 'A treasury team considering a deposit-rate change'
    found = [i+1 for i,p in enumerate(pages) if marker in re.sub(r'\s+', ' ', p)]
    assert len(found) == 1, found
    physical = {'first': found[0], 'last': found[0]+build['funding_journey']['last_printed_page']-build['funding_journey']['first_printed_page']}
    artifacts = ['plan-review.md', 'fixtures.json', 'design-preflight.json', 'environment.json', 'argument-review.json',
        'exact-examples.json', 'supplementary-mathematical-review.json', 'section.tex', 'source-audit.json', 'refs.bib',
        'local-journal.json', 'local-review.json', 'local-receipt.json', 'launch-failure.json', 'launch-amendment.json',
        'completion-failure.json', 'completion-amendment.json', 'runner-repair.diff', 'manuscript-review.json',
        'prepared-inputs.json', 'traceability-review.json', 'layout-repair.json']
    evidence = [ref(BASE / name, name) for name in artifacts]
    review = {'status': 'pass', 'issues': [], 'reviewer': {'name': 'Codex author/coordinator', 'kind': 'author'},
        'scope': 'Preserving funding narrative, exact generated references and amended local conformance evidence',
        'prior_citation_records_unchanged': 443, 'new_citation_records': 3,
        'printed_pages': build['funding_journey'], 'physical_pages': physical,
        'findings': ['All predecessor manuscript files and 443 citation records remain byte-preserved.',
            'The new funding chapter section connects target/clock, identity/inclusion, joint nuisance covariance, full effect sets and scenario economics.',
            'The 118 service slots, 29 parity comparisons and 451 independent rational checks pass; two failed harness launches and prospective amendments remain disclosed.',
            'Exact Gaussian/inclusion arithmetic is separate from declared dependent contexts and no general statistical validity is inferred.',
            'Compilation, text bounds and citation traceability pass; visual, independent and whole-proposal acceptance remain open.'],
        'evidence': evidence+[ref(OUT / 'build-report.json', 'Final repaired compilation'), ref(OUT / 'text-layout-review.json', 'Physical text bounds')],
        'visual_acceptance': False, 'MR03_acceptance': False, 'bank_qualification': False}
    core.write(BASE / 'release-source-review.json', review)
    code = ['funding_examples_20261013.py', 'funding_journey_20261013.py', 'freeze_funding_journey_20261013.py',
            'launch_funding_journey_20261013.py', 'funding_journey_successor_20261013.py',
            'review_funding_journey_20261013.py', 'build_funding_reader_20261013.py', 'publish_funding_reader_20261013.py']
    release = {'kind': 'working_monograph', 'final_acceptance': False, 'pdf': build['pdf'], 'pages': build['pages'],
        'supersedes': {k: state['reader'][k] for k in ['path', 'sha256']},
        'build_report': ref(OUT / 'build-report.json', 'Compiled funding working reader'),
        'source_review': ref(BASE / 'release-source-review.json', 'New source/claim and predecessor-preservation review'),
        'text_layout': ref(OUT / 'text-layout-review.json', 'All-page physical text bounds'),
        'source_artifacts': audit['tex_files']+evidence+[ref(BASE / 'release-source-review.json', 'Final source review')]
            +[ref(ROOT / 'tools' / name, 'Preserved exact execution/review/build source') for name in code],
        'visual_acceptance': False, 'mandatory_repairs_closed': [],
        'changes': ['Integrated complete funding decision journey with exact nuisance/identity/inclusion/economics examples and transparently amended 118-slot local study.'],
        'sponsor_binding': 'Prior sponsor preserved; final exact-reader coherence remains Q5 work.'}
    core.write(BASE / 'working-release.json', release)
    control.ledger.validate_working_release(ROOT, ref(BASE / 'working-release.json', 'Reviewed funding working release'))
    print(json.dumps({'pages': build['pages'], 'printed_pages': [436, 441], 'physical_pages': physical,
                      'pdf': build['pdf'], 'manifest': str((BASE / 'working-release.json').relative_to(ROOT))}))


if __name__ == '__main__':
    main()
