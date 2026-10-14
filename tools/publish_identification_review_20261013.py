#!/usr/bin/env python3
"""Preserve and review the integrated working reader; do not award acceptance."""
import json
from pathlib import Path
import build_identification_review_20261013 as build
import isolated_identification_reference_20261013 as exact
import master_control as core
import run_program as control

ROOT, BASE, OUT, ref = build.ROOT, build.BASE, build.OUT, build.ref


def main():
    assert not (BASE / 'working-release.json').exists()
    state = core.read(ROOT, core.STATE)
    br = json.loads((OUT / 'build-report.json').read_text())
    audit = json.loads((OUT / 'source-audit.json').read_text())
    prior = json.loads(build.PRIOR_AUDIT.read_text())
    trace = json.loads((BASE / 'traceability-review.json').read_text())
    bounds = json.loads((OUT / 'text-layout-review.json').read_text())
    assert state['reader']['sha256'] == br['predecessor_pdf']['sha256']
    assert trace['status'] == bounds['status'] == 'pass'
    assert trace['pdf']['sha256'] == br['pdf']['sha256']
    assert br['pages'] == bounds['pages'] == 626
    assert br['cited_records'] == 459
    assert all(w.startswith('Underfull') for w in br['warnings'])
    assert build.DRIVER.read_text() == build.expected_driver()
    old = {s['integrated_citation_key']: s for s in prior['sources']}
    new = {s['integrated_citation_key']: s for s in audit['sources']}
    assert len(old) == 458 and all(new[k] == v for k, v in old.items())
    for item in prior['tex_files']:
        core.bound(ROOT, item)
    build.shared.verify_refs(audit)
    assert exact.run() == json.loads((BASE / 'exact-results.json').read_text())
    pages = (OUT / 'reader.txt').read_text().split('\f')
    assert 'seed every original vertex' in pages[429]
    assert 'neither a proof of nonidentification' in pages[429]
    evidence = [ref(p, 'Inspected source, exact result or compiled artifact') for p in [
        BASE / 'plan-review.md', BASE / 'isolated-conditions.tex', BASE / 'exact-results.json',
        BASE / 'source-audit.json', BASE / 'traceability-review.json',
        OUT / 'source-audit.json', OUT / 'build-report.json', OUT / 'text-layout-review.json',
        ROOT / 'tools/isolated_identification_reference_20261013.py',
        ROOT / 'docs/literature/raw/v12_gap4_y0_graph.txt',
        ROOT / 'docs/literature/raw/v12_gap4_y0_id.txt',
        ROOT / 'docs/program/execution/2026-10-13/traceability/semantic-review-06.json',
        ROOT / 'docs/program/execution/2026-10-13/traceability/source-anchor-corrections-01.json']]
    review = {
        'status': 'pass', 'issues': [],
        'scope': 'Author review of added identification limitation and preserving working reader; not whole-reader semantic acceptance',
        'reviewer': {'name': 'Codex author/coordinator', 'kind': 'author'},
        'findings': [
            'The exact A->Y plus isolated Z trace follows graph.py556-567 and ID line3; initial ancestor restriction retains all nodes.',
            'Eight strictly positive cells give means1/4 and3/4 under either Z and effect1/2; missing-node computation is not nonidentification.',
            'The text labels the trace as project work and does not claim an observed native exception or qualified engine.',
            'Admission cases require internal node preservation and distinct handling of unsupported versus unavailable requests.',
            '458 prior citation records and all prior manuscript inputs remain byte-identical; the pcalg page12 correction is bound additively.',
            '626-page build has no unresolved citations, duplicate labels, missing glyph warnings, overfull boxes, empty pages or out-of-page text;72 underfull warnings remain.',
            'Extracted printed pages412-413 retain the equations, scope limitations and integration decision.'
        ],
        'physical_added_section_pages': [429, 430],
        'evidence': evidence,
        'visual_acceptance': False, 'independent_review': False,
        'limits': ['Rendered visual review remains pending under the inherited session limit.',
                   'Whole-reader Q1-Q5 remain open; this is a working successor.']
    }
    core.write(BASE / 'source-review.json', review)
    release = {
        'kind': 'working_monograph', 'final_acceptance': False,
        'pdf': br['pdf'], 'pages': br['pages'],
        'supersedes': {k: state['reader'][k] for k in ['path', 'sha256']},
        'build_report': ref(OUT / 'build-report.json', 'Bounded actual build'),
        'source_review': ref(BASE / 'source-review.json', 'Author review of changed claims and preservation'),
        'text_layout': ref(OUT / 'text-layout-review.json', 'All-page extracted text bounds'),
        'source_artifacts': audit['tex_files'] + evidence + [
            ref(BASE / 'source-review.json', 'Release review'),
            ref(Path(__file__), 'Frozen publication source'),
            ref(ROOT / 'tools/build_identification_review_20261013.py', 'Frozen build source')],
        'visual_acceptance': False, 'mandatory_repairs_closed': [],
        'changes': ['Internal graph modification and isolated-condition limitation integrated; exact identified reference and runtime admission obligations added.'],
        'sponsor_binding': 'Prior sponsor preserved; exact successor coherence remains Q5 work.'
    }
    core.write(BASE / 'working-release.json', release)
    control.ledger.validate_working_release(ROOT, ref(BASE / 'working-release.json', 'Reviewed successor'))
    print(json.dumps({'pages': 626, 'citations': 459, 'preserved_sources': 458,
                      'release': str((BASE / 'working-release.json').relative_to(ROOT))}))


if __name__ == '__main__':
    main()
