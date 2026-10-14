#!/usr/bin/env python3
"""Preserve the 410-page reader while integrating the vendor-source comparison."""
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
BASE = DOCS / 'program/execution/2026-10-13/commercial'
OUT = BASE / 'reader'
NAME = 'causal_proposal_commercial_2026-10-13'
OLD = DOCS / 'causal_proposal_execution_2026-10-13.tex'
DRIVER = DOCS / (NAME + '.tex')
PDF = DRIVER.with_suffix('.pdf')
ref = shared.ref


def guard():
    state = core.read(ROOT, core.STATE)
    if any(d['path'] == str(PDF.relative_to(ROOT)) for d in state['deliveries']):
        raise ValueError('Delivered artifacts are frozen; create a successor')


def prepare():
    guard()
    audit = json.loads((BASE / 'source-audit.json').read_text())
    shared.verify_refs(audit)
    entries = []
    for s in audit['sources']:
        entries.append('@misc{' + s['integrated_citation_key'] + ',\n author={{' +
                       shared.escape(s['author']) + '}},\n title={' + shared.escape(s['title']) +
                       '},\n year={' + str(s['year']) + '},\n note={' +
                       shared.escape(s['version_date']) + '},\n url={' + s['source_identity'] + '}\n}\n')
    (BASE / 'refs.bib').write_text('\n'.join(entries))
    book = OLD.read_text()
    marker = r'\input{program/repair-v12/integrated-reader/chapters/software.tex}'
    assert book.count(marker) == 1
    book = book.replace(marker, marker + '\n' +
                        r'\input{program/execution/2026-10-13/commercial/comparison.tex}', 1)
    marker = "\\addcontentsline{toc}{chapter}{Reader's contract}"
    book = book.replace(marker, marker + r'''

Section \ref{exec13:commercial} compares documented GeNIe/SMILE and BayesiaLab
paths with the proposed product, including graph ambiguity, interface semantics
and deployment rights. Stata's supplied-model SEM path is kept distinct.
This bounded comparison leaves unavailable vendor sources and unexecuted
commercial trials explicit; it does not complete the commercial survey.
''', 1)
    marker = 'program/execution/2026-10-13/new-refs}'
    assert book.count(marker) == 1
    book = book.replace(marker, 'program/execution/2026-10-13/new-refs,program/execution/2026-10-13/commercial/refs}', 1)
    DRIVER.write_text(book)
    print(json.dumps({'prepared': str(DRIVER.relative_to(ROOT)), 'new_documentation_records': len(entries)}))


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
            raise ValueError('Build failed; inspect ' + str(OUT / name))

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
    cited = {key.strip() for group in re.findall(shared.CITE, joined) for key in group.split(',')}
    audits = [DOCS / 'program/execution/2026-10-13/reader/source-audit.json', BASE / 'source-audit.json']
    entries = {}
    for path in audits:
        value = json.loads(path.read_text())
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
             'source_audits': [ref(p, 'Preserved source evidence') for p in audits],
             'added_bibliography': ref(BASE / 'refs.bib', 'Vendor identities and dated versions'),
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
              'pdf': ref(PDF, 'Integrated commercial-comparison successor'),
              'driver': ref(DRIVER, 'Preserving driver'), 'builder': ref(Path(__file__), 'Bounded builder'),
              'source_audit': ref(OUT / 'source-audit.json', 'Whole-book source identities'),
              'predecessor_pdf': ref(OLD.with_suffix('.pdf'), 'Preserved 410-page reader'),
              'cited_records': len(cited), 'warnings': warnings,
              'commercial_extension': {'first_printed_page': page('exec13:commercial'),
                                       'last_printed_page': page('exec13:commercial-end'),
                                       'S8_depth_acceptance': False},
              'final_acceptance': False, 'mandatory_repairs_closed': [], 'visual_acceptance': False,
              'visual_review': 'Pending fresh session: inherited image allowance exhausted'}
    core.write(OUT / 'build-report.json', report)
    layout.OUT = OUT
    layout.main()
    print(json.dumps({k: report[k] for k in ('pages', 'cited_records', 'commercial_extension', 'warnings')}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['prepare', 'build'])
    args = parser.parse_args()
    prepare() if args.command == 'prepare' else build()
