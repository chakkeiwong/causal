#!/usr/bin/env python3
"""Preserving working-reader build with the restricted Python identification adapter."""
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
BASE = DOCS / 'program/execution/2026-10-13/python-integration'
OUT = BASE / 'reader'
NAME = 'causal_proposal_python_2026-10-13'
OLD = DOCS / 'causal_proposal_research_2026-10-13.tex'
DRIVER = DOCS / (NAME + '.tex')
PDF = DRIVER.with_suffix('.pdf')
ref = shared.ref


def guard():
    if any(d['path'] == str(PDF.relative_to(ROOT)) for d in core.read(ROOT, core.STATE)['deliveries']):
        raise ValueError('Delivered release is frozen; create a successor')


def prepare():
    guard()
    audit = json.loads((BASE / 'source-audit.json').read_text())
    shared.verify_refs(audit)
    entries = []
    for s in audit['sources']:
        note = s['version_date']
        if s['source_identity'].startswith('https://'):
            accessed = note.split('accessed ')[1][:10]
            note = 'Revision cc6644d3b470, 2026-04-13; accessed ' + accessed
        entries.append('@misc{' + s['integrated_citation_key'] + ',\n author={{' +
                       shared.escape(s['author']) + '}},\n title={' + shared.escape(s['title']) +
                       '},\n year={2026},\n note={' + shared.escape(note) + '}\n}\n')
    (BASE / 'refs.bib').write_text('\n'.join(entries))
    subprocess.run(['pandoc', str(BASE / 'chapter.md'), '--from=markdown+raw_tex+tex_math_single_backslash',
                    '--to=latex', '--top-level-division=chapter', '-o', str(BASE / 'chapter.tex')],
                   check=True, timeout=25)
    book = OLD.read_text()
    marker = r'\input{program/repair-v12/work/IN06/integration-chapters.tex}'
    assert book.count(marker) == 1
    book = book.replace(marker, marker + '\n' + r'\input{program/execution/2026-10-13/python-integration/chapter.tex}', 1)
    marker = "\\addcontentsline{toc}{chapter}{Reader's contract}"
    book = book.replace(marker, marker + r'''

Chapter \ref{exec13:python-identification} develops a restricted Python
identification adapter, with exact positive and negative references and a
source-level conditional-identification counterexample. The proposed workaround
preserves the conditional query; no downloaded engine was executed.
''', 1)
    marker = 'program/execution/2026-10-13/research/refs}'
    assert book.count(marker) == 1
    book = book.replace(marker, 'program/execution/2026-10-13/research/refs,program/execution/2026-10-13/python-integration/refs}', 1)
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
    audits = [DOCS / 'program/execution/2026-10-13/research/reader/source-audit.json', BASE / 'source-audit.json']
    entries = {}
    for p in audits:
        value = json.loads(p.read_text())
        shared.verify_refs(value)
        for s in value['sources']:
            k = s['integrated_citation_key']
            if k in entries and entries[k] != s:
                raise ValueError('Conflicting citation: ' + k)
            entries[k] = s
    if not cited <= entries.keys():
        raise ValueError('Unaudited citations: ' + repr(cited - entries.keys()))
    PDF.write_bytes((OUT / (NAME + '.pdf')).read_bytes())
    audit = {'sources': [entries[k] for k in sorted(cited)],
             'tex_files': [ref(p, 'Compiled source') for p in sorted({p for p, _ in files})],
             'source_audits': [ref(p, 'Preserved evidence') for p in audits],
             'added_bibliography': ref(BASE / 'refs.bib', 'Pinned software and exact-reference identities'),
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
              'pdf': ref(PDF, 'Integrated Python design successor'), 'driver': ref(DRIVER, 'Preserving driver'),
              'builder': ref(Path(__file__), 'Bounded source and text builder'),
              'source_audit': ref(OUT / 'source-audit.json', 'Whole-book sources'),
              'predecessor_pdf': ref(OLD.with_suffix('.pdf'), 'Preserved 420-page reader'),
              'cited_records': len(cited), 'warnings': warnings,
              'python_chapter': {'first_printed_page': page('exec13:python-identification'),
                                   'last_printed_page': page('exec13:python-identification-end'),
                                   'qualification': False},
              'final_acceptance': False, 'mandatory_repairs_closed': [], 'visual_acceptance': False,
              'visual_review': 'Pending fresh session: inherited image allowance exhausted'}
    core.write(OUT / 'build-report.json', report)
    layout.OUT = OUT
    layout.main()
    print(json.dumps({k: report[k] for k in ('pages', 'cited_records', 'python_chapter', 'warnings')}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['prepare', 'build'])
    args = parser.parse_args()
    prepare() if args.command == 'prepare' else build()
