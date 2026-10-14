#!/usr/bin/env python3
"""Compile the two reviewed historical-status repairs without altering predecessors."""
import contextlib
import json
from pathlib import Path

import build_java_reader_20261013 as compiler
import master_control as core

ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-13/traceability-successor'
OUT = BASE / 'reader'
NAME = 'causal_proposal_source_review_2026-10-13'
OLD = ROOT / 'docs/causal_proposal_identification_review_2026-10-13.tex'
DRIVER = ROOT / 'docs' / (NAME + '.tex')
PDF = DRIVER.with_suffix('.pdf')
PRIOR_AUDIT = ROOT / 'docs/program/execution/2026-10-13/identification-review/reader/source-audit.json'


def main():
    assert not PDF.exists(), 'Preserve an existing successor; investigate before rebuilding'
    for name in ['BASE', 'OUT', 'NAME', 'OLD', 'DRIVER', 'PDF', 'PRIOR_AUDIT']:
        setattr(compiler, name, globals()[name])
    OUT.mkdir(exist_ok=True)
    for suffix in ['.aux', '.bbl', '.toc', '.out']:
        (OUT / (NAME + suffix)).touch(exist_ok=False)
    with (OUT / 'compile-summary.txt').open('x') as stream, contextlib.redirect_stdout(stream):
        compiler.build()
    report = json.loads((OUT / 'build-report.json').read_text())
    report.pop('java_comparison', None)
    report['builder'] = compiler.ref(Path(__file__), 'Preserving two-passage successor builder')
    report['pdf'] = compiler.ref(PDF, 'Working reader with reviewed historical-source status')
    report['predecessor_pdf'] = compiler.ref(OLD.with_suffix('.pdf'), 'Frozen 626-page predecessor')
    audit = json.loads((OUT / 'source-audit.json').read_text())
    prior = json.loads(PRIOR_AUDIT.read_text())
    audit['added_bibliography'] = compiler.ref(BASE / 'refs.bib', 'No new sources')
    audit['additive_anchor_corrections'] = prior.get('additive_anchor_corrections', [])
    core.write(OUT / 'source-audit.json', audit)
    report['source_audit'] = compiler.ref(OUT / 'source-audit.json', 'All source records and preserved corrections')
    core.write(OUT / 'build-report.json', report)
    print(json.dumps({'pages': report['pages'], 'cited_records': report['cited_records'],
                      'warnings': len(report['warnings']), 'visual_acceptance': False}))


if __name__ == '__main__':
    main()
