#!/usr/bin/env python3
"""Build the reviewed R latent-discovery proposal successor, preserving all predecessors."""
import contextlib
import json
import re
from pathlib import Path

import build_java_reader_20261013 as compiler
import master_control as core

ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-13/latent-r/reader-input'
OUT = BASE.parent / 'reader'
NAME = 'causal_proposal_latent_r_2026-10-13'
OLD = ROOT / 'docs/causal_proposal_source_review_v2_2026-10-13.tex'
DRIVER = ROOT / 'docs' / (NAME + '.tex')
PDF = DRIVER.with_suffix('.pdf')
PRIOR_AUDIT = ROOT / 'docs/program/execution/2026-10-13/traceability-successor/v2/reader/source-audit.json'

def main():
    assert not PDF.exists(), 'Preserve prior build attempts and published readers'
    for name in ['BASE', 'OUT', 'NAME', 'OLD', 'DRIVER', 'PDF', 'PRIOR_AUDIT']:
        setattr(compiler, name, globals()[name])
    OUT.mkdir(exist_ok=True)
    for suffix in ['.aux', '.bbl', '.toc', '.out']:
        (OUT / (NAME + suffix)).touch(exist_ok=False)
    with (OUT / 'compile-summary.txt').open('x') as stream, contextlib.redirect_stdout(stream):
        compiler.build()
    report = json.loads((OUT / 'build-report.json').read_text())
    report.pop('java_comparison', None)
    audit = json.loads((OUT / 'source-audit.json').read_text())
    prior = json.loads(PRIOR_AUDIT.read_text())
    audit['added_bibliography'] = compiler.ref(BASE / 'refs.bib', 'Three authentic originals, pinned source and project reference')
    audit['additive_anchor_corrections'] = prior.get('additive_anchor_corrections', [])
    core.write(OUT / 'source-audit.json', audit)
    report.update(builder=compiler.ref(Path(__file__), 'Bounded preserving latent-discovery compiler'),
                  source_audit=compiler.ref(OUT / 'source-audit.json', 'Whole-reader citations and preserved corrections'),
                  pdf=compiler.ref(PDF, 'Working reader with R latent-discovery comparison'),
                  predecessor_pdf=compiler.ref(OLD.with_suffix('.pdf'), 'Frozen 626-page predecessor'))
    aux = (OUT / (NAME + '.aux')).read_text()
    def page(label):
        return int(re.search(r'\newlabel{' + re.escape(label) + r'}{{[^}]*}{(d+)}', aux).group(1))
    report['latent_r'] = {'first_printed_page': page('exec13:latent-r'),
                          'last_printed_page': page('exec13:latent-r-end'),
                          'native_package_execution': False, 'adapter_qualification': False}
    core.write(OUT / 'build-report.json', report)
    print(json.dumps({'pages': report['pages'], 'cited_records': report['cited_records'],
                      'warnings': len(report['warnings']), 'latent_r': report['latent_r'],
                      'visual_acceptance': False}))

if __name__ == '__main__':
    main()
