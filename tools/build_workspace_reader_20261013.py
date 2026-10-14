#!/usr/bin/env python3
"""Replace the short I3 chapter in a preserving working-reader successor."""
import argparse
import json
from pathlib import Path
import re

import build_java_reader_20261013 as inherited
import build_integrated_monograph_v12 as shared
import master_control as core

ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-13/workspace'
OUT = BASE / 'reader'
NAME = 'causal_proposal_workspace_2026-10-13'
OLD = ROOT / 'docs/causal_proposal_evaluation_design_2026-10-13.tex'
DRIVER = ROOT / 'docs' / (NAME + '.tex')
PDF = DRIVER.with_suffix('.pdf')
PRIOR_AUDIT = ROOT / 'docs/program/execution/2026-10-13/live-evaluation/reader/source-audit.json'
TAIL = ROOT / 'docs/program/execution/2026-10-13/interfaces/integration-tail.tex'
CHAPTER = ROOT / 'docs/program/comprehensive-v14/work/TEXT.DRAFT.I3/chapter.tex'
ref = shared.ref


def configure():
    for key in ['BASE', 'OUT', 'NAME', 'OLD', 'DRIVER', 'PDF', 'PRIOR_AUDIT']:
        setattr(inherited, key, globals()[key])


def prepare():
    configure()
    inherited.guard()
    audit = json.loads((BASE / 'source-audit.json').read_text())
    shared.verify_refs(audit)
    text = TAIL.read_text()
    start = text.index(r'\chapter{Workspace consumers and complete banking workflows}')
    stop = text.index(r'\chapter{Operating the local causal service and qualifying its limits}')
    tail = text[:start] + r'\input{program/comprehensive-v14/work/TEXT.DRAFT.I3/chapter.tex}' + '\n\n' + text[stop:]
    (BASE / 'integration-tail.tex').write_text(tail)
    book = OLD.read_text()
    marker = r'\input{program/execution/2026-10-13/interfaces/integration-tail.tex}'
    assert book.count(marker) == 1
    book = book.replace(marker, r'\input{program/execution/2026-10-13/workspace/integration-tail.tex}', 1)
    marker = 'program/execution/2026-10-13/live-evaluation/refs}'
    assert book.count(marker) == 1
    book = book.replace(marker, 'program/execution/2026-10-13/live-evaluation/refs,program/execution/2026-10-13/workspace/refs}', 1)
    DRIVER.write_text(book)
    entries = []
    for s in audit['sources']:
        entries.append('@misc{' + s['integrated_citation_key'] + ',\n author={{' + shared.escape(s['author']) +
                       '}},\n title={' + shared.escape(s['title']) + '},\n year={' + str(s['year']) +
                       '},\n note={' + shared.escape(s['version_date']) + '}\n}\n')
    (BASE / 'refs.bib').write_text('\n'.join(entries))
    inputs = [OLD, PRIOR_AUDIT, TAIL, CHAPTER, BASE / 'source-audit.json',
              BASE / 'primary-inspection.json', BASE / 'examples.json', BASE / 'replay.json', Path(__file__)]
    inputs += [BASE / (n + '.tex') for n in ['boundaries', 'decisions', 'observations', 'composition', 'clients']]
    core.write(BASE / 'prepared-inputs.json', {
        'inputs': [ref(p, 'Reviewed preserving input') for p in inputs],
        'generated': [ref(p, 'Prepared source') for p in [DRIVER, BASE / 'integration-tail.tex', BASE / 'refs.bib']],
        'preserved_i2': tail[:start] == text[:start],
        'preserved_i4': tail.split(r'\chapter{Operating', 1)[1] == text.split(r'\chapter{Operating', 1)[1]})
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
    audit['added_bibliography'] = ref(BASE / 'refs.bib', 'Dated primary inspection and generated exact examples')
    core.write(OUT / 'source-audit.json', audit)
    report = json.loads((OUT / 'build-report.json').read_text())
    aux = (OUT / (NAME + '.aux')).read_text()
    def page(label):
        return int(re.search(r'\\newlabel\{' + re.escape(label) + r'\}\{\{[^}]*\}\{(\d+)\}', aux).group(1))
    first, last = page('exec13:i3-start'), page('exec13:i3-end')
    report.update(builder=ref(Path(__file__), 'Preserving I3 builder'),
                  compile_routine=ref(ROOT / 'tools/build_java_reader_20261013.py', 'Inherited bounded compiler'),
                  predecessor_pdf=ref(OLD.with_suffix('.pdf'), 'Frozen 532-page reader'),
                  pdf=ref(PDF, 'Working I3 successor'),
                  source_audit=ref(OUT / 'source-audit.json', 'Whole-reader citation identities'),
                  i3={'first_printed_page': first, 'last_printed_page': last,
                      'physical_span': last - first + 1, 'allocation': {'min': 12, 'target': 15, 'max': 18},
                      'chapter_review_acceptance': False})
    core.write(OUT / 'build-report.json', report)
    print(json.dumps({'pages': report['pages'], 'citations': report['cited_records'],
                      'i3': report['i3'], 'warnings': report['warnings']}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['prepare', 'build'])
    args = parser.parse_args()
    prepare() if args.command == 'prepare' else build()
