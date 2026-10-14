#!/usr/bin/env python3
"""Preserve the 587-page reader and integrate the other-language comparison."""
import argparse
import json
from pathlib import Path
import re

import build_integrated_monograph_v12 as shared
import build_java_reader_20261013 as inherited
import master_control as core

ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-13/other-discovery'
INPUT = BASE / 'reader-input'
OUT = BASE / 'reader'
NAME = 'causal_proposal_other_discovery_2026-10-13'
OLD = ROOT / 'docs/causal_proposal_operations_2026-10-13.tex'
DRIVER = ROOT / 'docs' / (NAME+'.tex')
PDF = DRIVER.with_suffix('.pdf')
PRIOR_AUDIT = ROOT / 'docs/program/execution/2026-10-13/operational-adoption/reader/source-audit.json'
ref = shared.ref


def configure():
    for key in ['OUT', 'NAME', 'OLD', 'DRIVER', 'PDF', 'PRIOR_AUDIT']:
        setattr(inherited, key, globals()[key])
    inherited.BASE = INPUT


def expected_driver():
    book = OLD.read_text()
    marker = r'\input{program/execution/2026-10-13/cxx-discovery/comparison.tex}'
    assert book.count(marker) == 1
    book = book.replace(marker, marker+'\n'+r'\input{program/execution/2026-10-13/other-discovery/comparison.tex}', 1)
    marker = 'program/execution/2026-10-13/operational-adoption/refs}'
    assert book.count(marker) == 1
    return book.replace(marker, 'program/execution/2026-10-13/operational-adoption/refs,program/execution/2026-10-13/other-discovery/reader-input/refs}', 1)


def prepare():
    configure(); inherited.guard()
    audit = json.loads((INPUT / 'source-audit.json').read_text())
    review = json.loads((BASE / 'author-review.json').read_text())
    assert review['status'] == 'pass'
    shared.verify_refs(audit); shared.verify_refs(review)
    DRIVER.write_text(expected_driver())
    entries = []
    for s in audit['sources']:
        entries.append('@misc{'+s['integrated_citation_key']+',\n author={{'+shared.escape(s['author'])
            +'}},\n title={'+shared.escape(s['title'])+'},\n year={'+str(s['year'])
            +'},\n note={'+shared.escape(s['version_date'])+'}\n}\n')
    (INPUT / 'refs.bib').write_text('\n'.join(entries))
    core.write(INPUT / 'prepared-inputs.json', {
        'inputs': [ref(p, 'Reviewed preserving input') for p in [OLD, PRIOR_AUDIT, BASE / 'comparison.tex',
            INPUT / 'source-audit.json', BASE / 'author-review.json', Path(__file__)]],
        'generated': [ref(p, 'Prepared successor') for p in [DRIVER, INPUT / 'refs.bib']]})
    print(json.dumps({'prepared': str(DRIVER.relative_to(ROOT))}))


def build():
    configure(); OUT.mkdir(exist_ok=True)
    for suffix in ['.aux', '.bbl', '.toc', '.out']:
        p = OUT / (NAME+suffix)
        if not p.exists(): p.write_text('')
    inherited.build()
    audit = json.loads((OUT / 'source-audit.json').read_text())
    audit['added_bibliography'] = ref(INPUT / 'refs.bib', 'Selected other-language primary sources and exact construction')
    core.write(OUT / 'source-audit.json', audit)
    report = json.loads((OUT / 'build-report.json').read_text())
    report.pop('java_comparison', None)
    aux = (OUT / (NAME+'.aux')).read_text()
    def page(label):
        return int(re.search(r'\\newlabel\{'+re.escape(label)+r'\}\{\{[^}]*\}\{(\d+)\}', aux).group(1))
    report.update(builder=ref(Path(__file__), 'Preserving source comparison integration'),
        compile_routine=ref(ROOT / 'tools/build_java_reader_20261013.py', 'Unchanged bounded compiler'),
        pdf=ref(PDF, 'Working monograph with other-language discovery comparison'),
        predecessor_pdf=ref(OLD.with_suffix('.pdf'), 'Preserved 587-page predecessor'),
        source_audit=ref(OUT / 'source-audit.json', 'Whole-reader source identities'),
        other_discovery={'first_printed_page': page('exec13:other-discovery'),
            'last_printed_page': page('exec13:other-discovery-end'),
            'full_cell_coverage_accepted': False, 'package_executions': 0})
    core.write(OUT / 'build-report.json', report)
    print(json.dumps({k: report[k] for k in ['pages', 'cited_records', 'other_discovery']}))


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('command', choices=['prepare', 'build']); args = p.parse_args()
    prepare() if args.command == 'prepare' else build()
