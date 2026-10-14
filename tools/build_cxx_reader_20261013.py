#!/usr/bin/env python3
"""Add the reviewed native comparison while preserving the delivered reader."""
import argparse
import json
from pathlib import Path
import re

import build_java_reader_20261013 as inherited
import build_integrated_monograph_v12 as shared
import master_control as core

ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-13/cxx-discovery'
OUT = BASE / 'reader'
NAME = 'causal_proposal_native_discovery_2026-10-13'
OLD = ROOT / 'docs/causal_proposal_workspace_2026-10-13.tex'
DRIVER = ROOT / 'docs' / (NAME + '.tex')
PDF = DRIVER.with_suffix('.pdf')
PRIOR_AUDIT = ROOT / 'docs/program/execution/2026-10-13/workspace/reader/source-audit.json'
ref = shared.ref


def configure():
    for key in ['BASE', 'OUT', 'NAME', 'OLD', 'DRIVER', 'PDF', 'PRIOR_AUDIT']:
        setattr(inherited, key, globals()[key])


def prepare():
    configure()
    inherited.guard()
    audit = json.loads((BASE / 'source-audit.json').read_text())
    shared.verify_refs(audit)
    book = OLD.read_text()
    marker = r'\input{program/execution/2026-10-13/pcalg-reuse/decision.tex}'
    assert book.count(marker) == 1
    book = book.replace(marker, marker + '\n' +
                        r'\input{program/execution/2026-10-13/cxx-discovery/comparison.tex}', 1)
    marker = 'program/execution/2026-10-13/workspace/refs}'
    assert book.count(marker) == 1
    book = book.replace(marker, 'program/execution/2026-10-13/workspace/refs,program/execution/2026-10-13/cxx-discovery/refs}', 1)
    DRIVER.write_text(book)
    entries = []
    for s in audit['sources']:
        entries.append('@misc{' + s['integrated_citation_key'] + ',\n author={{' + shared.escape(s['author']) +
                       '}},\n title={' + shared.escape(s['title']) + '},\n year={' + str(s['year']) +
                       '},\n note={' + shared.escape(s['version_date']) + '}\n}\n')
    (BASE / 'refs.bib').write_text('\n'.join(entries))
    names = ['comparison.tex', 'source-audit.json', 'candidate-register.json', 'omissions-register.json',
             'identity-review.json', 'exact-results.json', 'exact-replay.json']
    core.write(BASE / 'prepared-inputs.json', {
        'inputs': [ref(p, 'Reviewed preserving input') for p in [OLD, PRIOR_AUDIT, Path(__file__)]] +
                  [ref(BASE / n, 'Reviewed native comparison and evidence') for n in names],
        'generated': [ref(DRIVER, 'Preserving driver'), ref(BASE / 'refs.bib', 'New source identities')]})
    print(json.dumps({'prepared': str(DRIVER.relative_to(ROOT))}))


def build():
    configure()
    OUT.mkdir(exist_ok=True)
    for suffix in ['.aux', '.bbl', '.toc', '.out']:
        p = OUT / (NAME + suffix)
        if not p.exists():
            p.write_text('')
    inherited.build()
    audit = json.loads((OUT / 'source-audit.json').read_text())
    audit['added_bibliography'] = ref(BASE / 'refs.bib', 'Inspected native and host-language primary sources')
    core.write(OUT / 'source-audit.json', audit)
    report = json.loads((OUT / 'build-report.json').read_text())
    aux = (OUT / (NAME + '.aux')).read_text()
    def page(label):
        return int(re.search(r'\\newlabel\{' + re.escape(label) + r'\}\{\{[^}]*\}\{(\d+)\}', aux).group(1))
    first, last = page('exec13:cxx-discovery'), page('exec13:cxx-discovery-end')
    report.pop('java_comparison', None)
    report.update(builder=ref(Path(__file__), 'Preserving native comparison builder'),
                  compile_routine=ref(ROOT / 'tools/build_java_reader_20261013.py', 'Inherited bounded compiler'),
                  predecessor_pdf=ref(OLD.with_suffix('.pdf'), 'Frozen 545-page reader'),
                  pdf=ref(PDF, 'Working native discovery successor'),
                  source_audit=ref(OUT / 'source-audit.json', 'Whole-reader citation audit'),
                  cxx_comparison={'first_printed_page': first, 'last_printed_page': last,
                                  'physical_span': last-first+1, 'coverage_acceptance': False,
                                  'chapter_depth_acceptance': False})
    core.write(OUT / 'build-report.json', report)
    print(json.dumps({'pages': report['pages'], 'citations': report['cited_records'],
                      'cxx_comparison': report['cxx_comparison'], 'warnings': report['warnings']}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['prepare', 'build'])
    args = parser.parse_args()
    prepare() if args.command == 'prepare' else build()
