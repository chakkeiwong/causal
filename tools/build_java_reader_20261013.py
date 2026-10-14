#!/usr/bin/env python3
"""Preserve the delivered reader while integrating the Java discovery comparison."""
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
BASE = DOCS / 'program/execution/2026-10-13/java-discovery'
OUT = BASE / 'reader'
NAME = 'causal_proposal_java_2026-10-13'
OLD = DOCS / 'causal_proposal_diagrams_2026-10-13.tex'
DRIVER = DOCS / (NAME + '.tex')
PDF = DRIVER.with_suffix('.pdf')
SOFTWARE = DOCS / 'program/repair-v12/integrated-reader/chapters/software.tex'
PRIOR_AUDIT = DOCS / 'program/execution/2026-10-13/diagrams/reader/source-audit.json'
ref = shared.ref


def guard():
    if any(d['path'] == str(PDF.relative_to(ROOT)) for d in core.read(ROOT, core.STATE)['deliveries']):
        raise ValueError('Delivered release is frozen; create a preserving successor')


def prepare():
    guard()
    audit = json.loads((BASE / 'source-audit.json').read_text())
    shared.verify_refs(audit)
    subprocess.run(['pandoc', '--from=markdown+raw_tex+tex_math_single_backslash',
                    '--to=latex', '--wrap=auto', str(BASE / 'discovery-comparison.md'),
                    '-o', str(BASE / 'discovery-comparison.tex')], check=True, timeout=20)
    body = SOFTWARE.read_text()
    marker = r'\section{Symbolic identification and numerical evaluation}'
    assert body.count(marker) == 1
    body = body.replace(marker, r'\input{program/execution/2026-10-13/java-discovery/discovery-comparison.tex}' + '\n\n' + marker, 1)
    (BASE / 'software-preserving.tex').write_text(body)
    diagram = DOCS / 'program/execution/2026-10-13/diagrams/diagram-development.tex'
    old_wrapper = DOCS / 'program/comprehensive-v14/work/TEXT.DRAFT.L3/chapter.tex'
    fixed = diagram.read_text().replace(r'Chapter\textasciitilde{}\ref{ch:la03-discovery}',
                                       r'Chapter~\ref{ch:la03-discovery}')
    assert fixed != diagram.read_text()
    (BASE / 'diagram-copyedit.tex').write_text(fixed)
    wrapper = old_wrapper.read_text().replace(
        'program/execution/2026-10-13/diagrams/diagram-development.tex',
        'program/execution/2026-10-13/java-discovery/diagram-copyedit.tex')
    (BASE / 'L3-preserving.tex').write_text(wrapper)
    book = OLD.read_text()
    marker = r'\input{program/repair-v12/integrated-reader/chapters/software.tex}'
    assert book.count(marker) == 1
    book = book.replace(marker, r'\input{program/execution/2026-10-13/java-discovery/software-preserving.tex}', 1)
    marker = r'\input{program/comprehensive-v14/work/TEXT.DRAFT.L3/chapter.tex}'
    assert book.count(marker) == 1
    book = book.replace(marker, r'\input{program/execution/2026-10-13/java-discovery/L3-preserving.tex}', 1)
    marker = 'program/execution/2026-10-13/diagrams/refs}'
    assert book.count(marker) == 1
    book = book.replace(marker, 'program/execution/2026-10-13/diagrams/refs,program/execution/2026-10-13/java-discovery/refs}', 1)
    DRIVER.write_text(book)
    entries = []
    for s in audit['sources']:
        entries.append('@misc{' + s['integrated_citation_key'] + ',\n author={{' + shared.escape(s['author']) +
                       '}},\n title={' + shared.escape(s['title']) + '},\n year={' + str(s['year']) +
                       '},\n note={' + shared.escape(s['version_date']) + '}\n}\n')
    (BASE / 'refs.bib').write_text('\n'.join(entries))
    core.write(BASE / 'prepared-inputs.json', {
        'inputs': [ref(p, 'Prepared source identity') for p in
                   [OLD, SOFTWARE, diagram, old_wrapper, PRIOR_AUDIT, Path(__file__), BASE / 'source-audit.json', BASE / 'discovery-comparison.md']],
        'generated': [ref(p, 'Prepared output identity') for p in
                      [DRIVER, BASE / 'software-preserving.tex', BASE / 'discovery-comparison.tex', BASE / 'refs.bib',
                       BASE / 'L3-preserving.tex', BASE / 'diagram-copyedit.tex']]})
    print(json.dumps({'prepared': str(DRIVER.relative_to(ROOT))}))


def build():
    guard()
    shared.verify_refs(json.loads((BASE / 'prepared-inputs.json').read_text()))
    shared.scan(DRIVER)
    OUT.mkdir(exist_ok=True)
    env = dict(os.environ)
    env['TEXINPUTS'] = str(DOCS) + '//:' + env.get('TEXINPUTS', '')
    env['BIBINPUTS'] = str(DOCS) + '//:' + env.get('BIBINPUTS', '')
    command = ['pdflatex', '-no-shell-escape', '-interaction=nonstopmode', '-halt-on-error',
               '-output-directory=' + str(OUT), str(DRIVER)]

    def run(args, name):
        with (OUT / name).open('w') as stream:
            p = subprocess.run(args, cwd=DOCS, env=env, stdout=stream, stderr=subprocess.STDOUT, timeout=55)
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
    assert len(labels) == len(set(labels)), 'Duplicate label'
    cited = {k.strip() for group in re.findall(shared.CITE, joined) for k in group.split(',')}
    entries = {}
    audits = [PRIOR_AUDIT, BASE / 'source-audit.json']
    for p in audits:
        audit = json.loads(p.read_text())
        shared.verify_refs(audit)
        for s in audit['sources']:
            key = s['integrated_citation_key']
            if key in entries and entries[key] != s:
                raise ValueError('Conflicting citation: ' + key)
            entries[key] = s
    assert cited <= entries.keys(), 'Unaudited citations: ' + repr(cited - entries.keys())
    PDF.write_bytes((OUT / (NAME + '.pdf')).read_bytes())
    audit = {'sources': [entries[k] for k in sorted(cited)],
             'tex_files': [ref(p, 'Compiled source') for p in sorted({p for p, _ in files})],
             'source_audits': [ref(p, 'Preserved source audit') for p in audits],
             'added_bibliography': ref(BASE / 'refs.bib', 'Java primary-source bibliography'),
             'cutoff': '2026-10-07', 'visual_acceptance': False}
    shared.verify_refs(audit)
    core.write(OUT / 'source-audit.json', audit)
    subprocess.run(['pdftotext', '-layout', str(PDF), str(OUT / 'reader.txt')], check=True, timeout=25)
    info = subprocess.check_output(['pdfinfo', str(PDF)], text=True, timeout=15)
    pages = int(re.search(r'(?m)^Pages:\s+(\d+)', info).group(1))
    aux = (OUT / (NAME + '.aux')).read_text()

    def page(label):
        return int(re.search(r'\\newlabel\{' + re.escape(label) + r'\}\{\{[^}]*\}\{(\d+)\}', aux).group(1))

    report = {'status': 'compiled_source_and_text_checked_working_draft', 'pages': pages,
              'pdf': ref(PDF, 'Preserving Java-discovery working successor'),
              'driver': ref(DRIVER, 'Preserving driver'), 'builder': ref(Path(__file__), 'Bounded builder'),
              'source_audit': ref(OUT / 'source-audit.json', 'Whole-book citation identities'),
              'predecessor_pdf': ref(OLD.with_suffix('.pdf'), 'Frozen450-page reader'),
              'cited_records': len(cited),
              'warnings': [line for line in log.splitlines() if any(t in line for t in ['Warning', 'Overfull', 'Underfull', 'Missing character'])],
              'java_comparison': {'first_printed_page': page('exec13:java-discovery'),
                                  'last_printed_page': page('exec13:java-discovery-end'),
                                  'coverage_acceptance': False, 'chapter_depth_acceptance': False},
              'final_acceptance': False, 'mandatory_repairs_closed': [], 'visual_acceptance': False,
              'visual_review': 'Pending fresh session: inherited image allowance exhausted'}
    core.write(OUT / 'build-report.json', report)
    layout.OUT = OUT
    layout.main()
    bounds = json.loads((OUT / 'text-layout-review.json').read_text())
    assert bounds['status'] == 'pass' and bounds['pages'] == pages, 'PDF text/bounds check failed'
    print(json.dumps({k: report[k] for k in ['pages', 'cited_records', 'java_comparison', 'warnings']}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['prepare', 'build'])
    args = parser.parse_args()
    prepare() if args.command == 'prepare' else build()
