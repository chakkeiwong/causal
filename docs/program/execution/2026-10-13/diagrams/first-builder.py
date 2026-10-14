#!/usr/bin/env python3
"""Preserving build for the developed diagram-assistance proposal chapter."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess

import build_integrated_monograph_v12 as shared
import master_control as core
import review_gap_reader_v13 as layout

ROOT = core.ROOT
DOCS = ROOT / 'docs'
BASE = DOCS / 'program/execution/2026-10-13/diagrams'
OUT = BASE / 'reader'
NAME = 'causal_proposal_diagrams_2026-10-13'
OLD = DOCS / 'causal_proposal_interchange_2026-10-13.tex'
DRIVER = DOCS / (NAME + '.tex')
PDF = DRIVER.with_suffix('.pdf')
ref = shared.ref


def guard():
    state = core.read(ROOT, core.STATE)
    if any(d['path'] == str(PDF.relative_to(ROOT)) for d in state['deliveries']):
        raise ValueError('Delivered release is frozen; create a successor')


def prepare():
    guard()
    audit = json.loads((BASE / 'source-audit.json').read_text())
    shared.verify_refs(audit)
    subprocess.run(['pandoc', '--from=markdown+raw_tex+tex_math_single_backslash',
                    '--to=latex', '--wrap=auto', str(BASE / 'diagram-development.md'),
                    '-o', str(BASE / 'diagram-development.tex')], check=True, timeout=20)
    s = audit['sources'][0]
    (BASE / 'refs.bib').write_text(
        '@misc{' + s['integrated_citation_key'] + ',\n'
        ' author={{' + s['author'] + '}},\n'
        ' title={' + s['title'] + '},\n'
        ' year={2026},\n note={Exact stipulated project examples; 13 October 2026}\n}\n')
    book = OLD.read_text()
    marker = ('\\input{program/repair-v12/work/LA07/diagram-chapter.tex}\n'
              '\\input{program/gap-repair-v13/work/LA07/diagram-extension.tex}')
    assert book.count(marker) == 1
    book = book.replace(marker, r'\input{program/comprehensive-v14/work/TEXT.DRAFT.L3/chapter.tex}', 1)
    marker = 'program/execution/2026-10-13/interchange/refs}'
    assert book.count(marker) == 1
    book = book.replace(marker, 'program/execution/2026-10-13/interchange/refs,program/execution/2026-10-13/diagrams/refs}', 1)
    DRIVER.write_text(book)
    print(json.dumps({'prepared': str(DRIVER.relative_to(ROOT))}))


def build():
    guard()
    OUT.mkdir(exist_ok=True)
    env = dict(os.environ)
    env['TEXINPUTS'] = str(DOCS) + '//:' + env.get('TEXINPUTS', '')
    env['BIBINPUTS'] = str(DOCS) + '//:' + env.get('BIBINPUTS', '')
    command = ['pdflatex', '-no-shell-escape', '-interaction=nonstopmode', '-halt-on-error',
               '-output-directory=' + str(OUT), str(DRIVER)]

    def run(args, name):
        with (OUT / name).open('w') as stream:
            p = subprocess.run(args, cwd=DOCS, env=env, stdout=stream,
                               stderr=subprocess.STDOUT, timeout=55)
        if p.returncode:
            raise ValueError('Build failed: ' + str(OUT / name))

    run(command, 'pass-1.log')
    run(['bibtex', str((OUT / NAME).relative_to(DOCS))], 'bibtex-pass.log')
    for i in range(2, 6):
        run(command, f'pass-{i}.log')
        log = (OUT / (NAME + '.log')).read_text(errors='replace')
        if i >= 3 and not any(t in log for t in ['Label(s) may have changed', 'Rerun to get']):
            break
    for token in ['undefined citations', 'undefined references', 'multiply defined', 'Missing character']:
        if token in log:
            raise ValueError('Unresolved build warning: ' + token)
    files = shared.scan(DRIVER)
    joined = '\n'.join(t for _, t in files)
    labels = re.findall(shared.LABEL, joined)
    if len(labels) != len(set(labels)):
        raise ValueError('Duplicate label')
    cited = {k.strip() for g in re.findall(shared.CITE, joined) for k in g.split(',')}
    audits = [DOCS / 'program/execution/2026-10-13/interchange/reader/source-audit.json',
              BASE / 'source-audit.json']
    entries = {}
    for p in audits:
        value = json.loads(p.read_text())
        shared.verify_refs(value)
        for s in value['sources']:
            key = s['integrated_citation_key']
            if key in entries and entries[key] != s:
                raise ValueError('Conflicting citation: ' + key)
            entries[key] = s
    if not cited <= entries.keys():
        raise ValueError('Unaudited citations: ' + repr(cited - entries.keys()))
    PDF.write_bytes((OUT / (NAME + '.pdf')).read_bytes())
    audit = {'sources': [entries[k] for k in sorted(cited)],
             'tex_files': [ref(p, 'Compiled source') for p in sorted({p for p, _ in files})],
             'source_audits': [ref(p, 'Preserved source audit') for p in audits],
             'added_bibliography': ref(BASE / 'refs.bib', 'New exact-example source identity'),
             'cutoff': '2026-10-07', 'visual_acceptance': False}
    shared.verify_refs(audit)
    core.write(OUT / 'source-audit.json', audit)
    subprocess.run(['pdftotext', '-layout', str(PDF), str(OUT / 'reader.txt')], check=True, timeout=25)
    info = subprocess.check_output(['pdfinfo', str(PDF)], text=True, timeout=15)
    pages = int(re.search(r'(?m)^Pages:\s+(\d+)', info).group(1))
    aux = (OUT / (NAME + '.aux')).read_text()

    def page(label):
        return int(re.search(r'\\newlabel\{' + re.escape(label) + r'\}\{\{[^}]*\}\{(\d+)\}', aux).group(1))

    warnings = [l for l in log.splitlines() if any(t in l for t in ['Warning', 'Overfull', 'Underfull', 'Missing character'])]
    report = {'status': 'compiled_source_and_text_checked_working_draft', 'pages': pages,
              'pdf': ref(PDF, 'Integrated diagram-assistance successor'),
              'driver': ref(DRIVER, 'Preserving driver'),
              'builder': ref(Path(__file__), 'Bounded build and reference checks'),
              'source_audit': ref(OUT / 'source-audit.json', 'Whole-book source identities'),
              'predecessor_pdf': ref(OLD.with_suffix('.pdf'), 'Preserved 432-page reader'),
              'cited_records': len(cited), 'warnings': warnings,
              'diagram_chapter': {'first_printed_page': page('la:diagrams'),
                                  'last_printed_page': page('exec13:diagram-development-end'),
                                  'depth_acceptance': False},
              'final_acceptance': False, 'mandatory_repairs_closed': [],
              'visual_acceptance': False,
              'visual_review': 'Pending fresh session: inherited image allowance exhausted'}
    core.write(OUT / 'build-report.json', report)
    layout.OUT = OUT
    layout.main()
    bounds = json.loads((OUT / 'text-layout-review.json').read_text())
    if bounds['status'] != 'pass' or bounds['pages'] != pages:
        raise ValueError('Current PDF layout check failed')
    print(json.dumps({k: report[k] for k in ('pages', 'cited_records', 'diagram_chapter', 'warnings')}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['prepare', 'build'])
    args = parser.parse_args()
    prepare() if args.command == 'prepare' else build()
