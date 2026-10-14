#!/usr/bin/env python3
"""Build a preserving reader with the isolated-condition source finding."""
import argparse
import contextlib
import json
from pathlib import Path
import build_integrated_monograph_v12 as shared
import build_java_reader_20261013 as compiler
import isolated_identification_reference_20261013 as exact
import master_control as core

ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-13/identification-review'
OUT = BASE / 'reader'
NAME = 'causal_proposal_identification_review_2026-10-13'
OLD = ROOT / 'docs/causal_proposal_frontier_evidence_2026-10-13.tex'
DRIVER = ROOT / 'docs' / (NAME + '.tex')
PDF = DRIVER.with_suffix('.pdf')
PRIOR_AUDIT = ROOT / 'docs/program/execution/2026-10-13/frontier-synthesis/reader/source-audit.json'
CHAPTER = ROOT / 'docs/program/comprehensive-v14/work/TEXT.DRAFT.I1/chapter.tex'
ref = shared.ref


def expected_driver():
    text = OLD.read_text()
    marker = r'\input{program/comprehensive-v14/work/TEXT.DRAFT.I1/chapter.tex}'
    assert text.count(marker) == 1
    text = text.replace(marker, r'\input{program/execution/2026-10-13/identification-review/I1-preserving.tex}', 1)
    marker = 'program/execution/2026-10-13/frontier-synthesis/refs}'
    assert text.count(marker) == 1
    text = text.replace(marker, 'program/execution/2026-10-13/frontier-synthesis/refs,program/execution/2026-10-13/identification-review/refs}', 1)
    return text.replace('Proposal working edition with developed frontier evidence',
                        'Proposal working edition with reviewed identification limits', 1)


def prepare():
    assert not (BASE / 'prepared-inputs.json').exists()
    shared.verify_refs(json.loads(PRIOR_AUDIT.read_text()))
    results = exact.run()
    core.write(BASE / 'exact-results.json', results)
    (BASE / 'I1-preserving.tex').write_text(
        r'\input{program/comprehensive-v14/work/TEXT.DRAFT.I1/chapter.tex}' + '\n' +
        r'\input{program/execution/2026-10-13/identification-review/isolated-conditions.tex}' + '\n')
    source = {
        'integrated_citation_key': 'exec13_isolated_reference',
        'kind': 'project_derivation',
        'title': 'Isolated-condition graph preservation and exact identification reference',
        'author': 'Causal banking proposal project', 'year': 2026,
        'version_date': '2026-10-13',
        'source_identity': 'Project trace of pinned y0 source and independent rational enumeration',
        'local_copy': ref(BASE / 'exact-results.json', 'Node loss trace and eight positive observed cells'),
        'code': ref(ROOT / 'tools/isolated_identification_reference_20261013.py', 'Project reference without imported y0'),
        'primary_source': ref(ROOT / 'docs/literature/raw/v12_gap4_y0_graph.txt', 'from_edges464-480; remove_in_edges556-567; ancestors755-759'),
        'inspected_anchors': ['source_traced_nodes_after_remove_in_edges', 'identified_conditional_means', 'required_admission_cases'],
        'supported_claims': [
            'The inspected construction drops isolated Z outside intervention A in the A->Y plus Z example.',
            'A positive generated law identifies conditional means1/4 and3/4 and effect1/2 at both Z values.',
            'Initial node conversion alone cannot establish preservation throughout internal modification.'
        ],
        'limits': 'Project source trace and exact law only; no y0 execution, actual native exception or runtime admission.'
    }
    correction = ROOT / 'docs/program/execution/2026-10-13/traceability/source-anchor-corrections-01.json'
    core.write(BASE / 'source-audit.json', {
        'sources': [source], 'cutoff': '2026-10-07',
        'additive_anchor_corrections': [ref(correction, 'Operative pcalg page12 correction; historical record retained')]
    })
    (BASE / 'refs.bib').write_text(
        '@misc{exec13_isolated_reference,\n author={{Causal banking proposal project}},\n'
        ' title={Isolated-condition graph preservation and exact identification reference},\n'
        ' year={2026},\n note={13 October 2026; project source trace and exact law}\n}\n')
    DRIVER.write_text(expected_driver())
    core.write(BASE / 'prepared-inputs.json', {
        'inputs': [ref(p, 'Preserved or reviewed build input') for p in [
            OLD, PRIOR_AUDIT, CHAPTER, BASE / 'isolated-conditions.tex',
            BASE / 'plan-review.md', BASE / 'source-audit.json',
            BASE / 'exact-results.json', correction, Path(__file__)]],
        'generated': [ref(p, 'Successor build input') for p in [
            DRIVER, BASE / 'I1-preserving.tex', BASE / 'refs.bib']]
    })
    print(json.dumps({'prepared': str(DRIVER.relative_to(ROOT)), 'new_sources': 1}))


def build():
    for key in ['BASE', 'OUT', 'NAME', 'OLD', 'DRIVER', 'PDF', 'PRIOR_AUDIT']:
        setattr(compiler, key, globals()[key])
    OUT.mkdir(exist_ok=True)
    for suffix in ['.aux', '.bbl', '.toc', '.out']:
        path = OUT / (NAME + suffix)
        if not path.exists():
            path.write_text('')
    with (OUT / 'compile-summary.txt').open('w') as stream, contextlib.redirect_stdout(stream):
        compiler.build()
    report = json.loads((OUT / 'build-report.json').read_text())
    report.pop('java_comparison', None)
    report.update(builder=ref(Path(__file__), 'Preserving identification review builder'),
                  pdf=ref(PDF, 'Working reader with identification source finding'),
                  predecessor_pdf=ref(OLD.with_suffix('.pdf'), 'Preserved625-page reader'))
    audit = json.loads((OUT / 'source-audit.json').read_text())
    audit['added_bibliography'] = ref(BASE / 'refs.bib', 'New project reference')
    audit['additive_anchor_corrections'] = json.loads((BASE / 'source-audit.json').read_text())['additive_anchor_corrections']
    core.write(OUT / 'source-audit.json', audit)
    report['source_audit'] = ref(OUT / 'source-audit.json', 'Complete successor source records plus additive correction')
    core.write(OUT / 'build-report.json', report)
    print(json.dumps({'pages': report['pages'], 'citations': report['cited_records'],
                      'warnings': len(report['warnings']), 'final_acceptance': False}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['prepare', 'build'])
    args = parser.parse_args()
    prepare() if args.command == 'prepare' else build()
