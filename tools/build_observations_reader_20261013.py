#!/usr/bin/env python3
"""Bounded preserving build for the reviewed observation-workflow addition."""
import contextlib
import json
from pathlib import Path
import re

import build_java_reader_20261013 as compiler
import master_control as core

ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-13/observations-journey'
OUT = BASE / 'reader'
NAME = 'causal_proposal_observations_2026-10-13'
OLD = ROOT / 'docs/causal_proposal_latent_r_v2_2026-10-13.tex'
DRIVER = ROOT / 'docs' / (NAME + '.tex')
PDF = DRIVER.with_suffix('.pdf')
PRIOR_AUDIT = ROOT / 'docs/program/execution/2026-10-13/latent-r/v2/reader/source-audit.json'


def main():
    assert not PDF.exists(), 'Preserve completed readers'
    for name in ['BASE', 'OUT', 'NAME', 'OLD', 'DRIVER', 'PDF', 'PRIOR_AUDIT']:
        setattr(compiler, name, globals()[name])
    OUT.mkdir(exist_ok=False)
    for suffix in ['.aux', '.bbl', '.toc', '.out']:
        (OUT / (NAME + suffix)).touch(exist_ok=False)
    with (OUT / 'compile-summary.txt').open('x') as stream, contextlib.redirect_stdout(stream):
        compiler.build()
    report = json.loads((OUT / 'build-report.json').read_text())
    report.pop('java_comparison', None)
    audit = json.loads((OUT / 'source-audit.json').read_text())
    prior = json.loads(PRIOR_AUDIT.read_text())
    audit['added_bibliography'] = compiler.ref(BASE / 'refs.bib', 'Observation design, derivation, implementation and registered study')
    audit['additive_anchor_corrections'] = prior.get('additive_anchor_corrections', [])
    core.write(OUT / 'source-audit.json', audit)
    aux = (OUT / (NAME + '.aux')).read_text()
    def page(label):
        prefix = chr(92) + 'newlabel{' + label + '}{{'
        line = next(line for line in aux.splitlines() if line.startswith(prefix))
        return int(line[len(prefix):].split('}{', 2)[1])
    report.update(builder=compiler.ref(Path(__file__), 'Bounded preserving observation compiler'),
                  source_audit=compiler.ref(OUT / 'source-audit.json', 'Whole-reader citations and preserved anchor corrections'),
                  pdf=compiler.ref(PDF, 'Working reader including observed local workflow outcomes'),
                  predecessor_pdf=compiler.ref(OLD.with_suffix('.pdf'), 'Frozen 630-page predecessor'),
                  observations={'first_printed_page': page('exec13:observation-journey'),
                                'last_printed_page': page('exec13:observation-journey-end'),
                                'registered_local_requests': 106, 'bank_qualification': False})
    core.write(OUT / 'build-report.json', report)
    print(json.dumps({'pages': report['pages'], 'cited_records': report['cited_records'],
                      'observations': report['observations'], 'visual_acceptance': False}))


if __name__ == '__main__':
    main()
