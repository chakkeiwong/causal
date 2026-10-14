#!/usr/bin/env python3
"""Develop I2 in a preserving reader; retain every prior delivered artifact."""
import argparse
import hashlib
import json
from pathlib import Path
import re

import build_java_reader_20261013 as inherited
import build_integrated_monograph_v12 as shared
import master_control as core

ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-13/interfaces'
OUT = BASE / 'reader'
NAME = 'causal_proposal_interfaces_2026-10-13'
OLD = ROOT / 'docs/causal_proposal_census_2026-10-13.tex'
DRIVER = ROOT / 'docs' / (NAME + '.tex')
PDF = DRIVER.with_suffix('.pdf')
PRIOR_AUDIT = ROOT / 'docs/program/execution/2026-10-13/llm-census/reader/source-audit.json'
TAIL = ROOT / 'docs/program/execution/2026-10-13/interchange/integration-tail.tex'
CHAPTER = ROOT / 'docs/program/comprehensive-v14/work/TEXT.DRAFT.I2/chapter.tex'
ref = shared.ref


def configure():
    for key in ['BASE', 'OUT', 'NAME', 'OLD', 'DRIVER', 'PDF', 'PRIOR_AUDIT']:
        setattr(inherited, key, globals()[key])


def prepare():
    configure()
    inherited.guard()
    shared.verify_refs(json.loads((BASE / 'source-audit.json').read_text()))
    printed = json.loads((BASE / 'printed-listings/review.json').read_text())
    blocks = re.findall(r'\\begin\{lstlisting\}\[language=Python\]\n(.*?)\\end\{lstlisting\}',
                        CHAPTER.read_text(), re.S)
    assert [hashlib.sha256(b.encode()).hexdigest() for b in blocks] == printed['listing_hashes']
    book = OLD.read_text()
    marker = r'\chapter{Workspace consumers and complete banking workflows}'
    tail = TAIL.read_text()
    assert tail.count(marker) == 1
    preserved = marker + tail.split(marker)[1]
    successor = r'\input{program/comprehensive-v14/work/TEXT.DRAFT.I2/chapter.tex}' + '\n\n' + preserved
    (BASE / 'integration-tail.tex').write_text(successor)
    location = r'\input{program/execution/2026-10-13/interchange/integration-tail.tex}'
    assert book.count(location) == 1
    book = book.replace(location, r'\input{program/execution/2026-10-13/interfaces/integration-tail.tex}', 1)
    bib = 'program/execution/2026-10-13/llm-census/refs}'
    assert book.count(bib) == 1
    book = book.replace(bib, 'program/execution/2026-10-13/llm-census/refs,program/execution/2026-10-13/interfaces/refs}', 1)
    style = r'\bibliographystyle{plainnat}'
    assert book.count(style) == 1
    book = book.replace(style, r'\bibliographystyle{program/execution/2026-10-13/interfaces/causalplainnat}', 1)
    DRIVER.write_text(book)
    audit = json.loads((BASE / 'source-audit.json').read_text())
    entries = []
    for s in audit['sources']:
        entries.append('@misc{' + s['integrated_citation_key'] + ',\n author={{' + shared.escape(s['author']) +
                       '}},\n title={' + shared.escape(s['title']) + '},\n year={' + str(s['year']) +
                       '},\n note={' + shared.escape(s['version_date']) + '}\n}\n')
    (BASE / 'refs.bib').write_text('\n'.join(entries))
    core.write(BASE / 'prepared-inputs.json', {
        'inputs': [ref(p, 'Reviewed input for preserving I2 development') for p in
                   [OLD, PRIOR_AUDIT, TAIL, CHAPTER, BASE / 'source-audit.json',
                    BASE / 'examples/review.json', BASE / 'printed-listings/review.json',
                    BASE / 'causalplainnat.bst', BASE / 'build-repair.json', Path(__file__)]],
        'outputs': [ref(p, 'Generated preserving source') for p in
                    [DRIVER, BASE / 'integration-tail.tex', BASE / 'refs.bib']],
        'consumer_and_operations_tail_unchanged': preserved == successor.split('\n\n', 1)[1]})
    print(json.dumps({'prepared': str(DRIVER.relative_to(ROOT)), 'consumer_operations_preserved': True}))


def build():
    configure()
    # Recursive TeX search can find a preserved failed attempt's .bbl on a
    # fresh first pass. Local empty auxiliaries keep that attempt out of input.
    OUT.mkdir(exist_ok=True)
    for suffix in ['.aux', '.bbl', '.toc', '.out']:
        path = OUT / (NAME + suffix)
        if not path.exists():
            path.write_text('')
    inherited.build()
    report = json.loads((OUT / 'build-report.json').read_text())
    audit = json.loads((OUT / 'source-audit.json').read_text())
    audit['added_bibliography'] = ref(BASE / 'refs.bib', 'New implementation/example source record')
    core.write(OUT / 'source-audit.json', audit)
    aux = (OUT / (NAME + '.aux')).read_text()

    def page(label):
        return int(re.search(r'\\newlabel\{' + re.escape(label) + r'\}\{\{[^}]*\}\{(\d+)\}', aux).group(1))

    first, last = page('exec13:i2-start'), page('exec13:i2-end')
    report.update(builder=ref(Path(__file__), 'Preserving I2 chapter builder'),
                  compile_routine=ref(ROOT / 'tools/build_java_reader_20261013.py', 'Inherited bounded compiler'),
                  source_audit=ref(OUT / 'source-audit.json', 'Whole-reader citation audit'),
                  predecessor_pdf=ref(OLD.with_suffix('.pdf'), 'Frozen 487-page reader'),
                  pdf=ref(PDF, 'Working I2 successor'),
                  i2={'first_printed_page': first, 'last_printed_page': last,
                      'physical_span': last-first+1, 'allocation': {'min': 10, 'target': 13, 'max': 16},
                      'chapter_review_acceptance': False})
    core.write(OUT / 'build-report.json', report)
    print(json.dumps({'pages': report['pages'], 'citations': report['cited_records'], 'i2': report['i2'],
                      'visual_acceptance': False}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['prepare', 'build'])
    args = parser.parse_args()
    prepare() if args.command == 'prepare' else build()
