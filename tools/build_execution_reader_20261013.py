#!/usr/bin/env python3
"""Build a preserving proposal successor with software and formulation reviews."""
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
BASE = DOCS / 'program/execution/2026-10-13'
OUT = BASE / 'reader'
NAME = 'causal_proposal_execution_2026-10-13'
OLD = DOCS / 'causal_proposal_public_data_2026-10-12.tex'
DRIVER = DOCS / (NAME + '.tex')
PDF = DRIVER.with_suffix('.pdf')
CHAPTER = DOCS / 'program/comprehensive-v14/work/TEXT.DRAFT.S1/chapter.tex'
FORMULATION = DOCS / 'program/comprehensive-v14/work/LL.TASK.business_translation/task-synthesis.md'
ref = shared.ref


def guard():
    state = core.read(ROOT, core.STATE)
    if any(d['path'] == str(PDF.relative_to(ROOT)) for d in state['deliveries']):
        raise ValueError('Delivered PDF/source artifacts are frozen; create a successor')


def prepare():
    guard()
    sources = []
    for path in (BASE / 'source-audit.json', BASE / 'source-audit-supplement.json',
                 BASE / 'formulation-source-audit.json', BASE / 'survey-review-audit.json'):
        audit = json.loads(path.read_text())
        shared.verify_refs(audit)
        sources.extend(audit['sources'])
    entries = []
    for item in sources:
        key = item['integrated_citation_key']
        author = '{{' + shared.escape(item['author']) + '}}'
        year = item['year'] if item['kind'] == 'paper' else 2023 if key == 'exec13_mcmcabn' else 2026
        url = item['source_identity']
        entries.append('@misc{' + key + ',\n author=' + author + ',\n title={' +
                       shared.escape(item['title']) + '},\n year={' + str(year) +
                       '},\n note={' + shared.escape(item['version_date']) + '}' +
                       (',\n url={' + url + '}' if url.startswith('https://') else '') + '\n}\n')
    (BASE / 'new-refs.bib').write_text('\n'.join(entries))
    formulation_tex = BASE / 'formulation.tex'
    subprocess.run(['pandoc', str(FORMULATION), '--from=markdown+raw_tex+tex_math_single_backslash',
                    '--to=latex', '--top-level-division=section', '-o', str(formulation_tex)],
                   check=True, timeout=25)
    raw = formulation_tex.read_text()
    widths = [.15, .5, .35]
    columns = ''.join(r'>{\raggedright\arraybackslash}p{\dimexpr ' + str(w) +
                      r'\linewidth-2\tabcolsep\relax}' for w in widths)
    raw = raw.replace(r'\begin{longtable}[]{@{}lll@{}}', r'\begin{longtable}[]{@{}' + columns + r'@{}}')
    raw = re.sub(r'(\\begin\{minipage\}\[[bt]\])\{[0-9.]+\\columnwidth\}', r'\1{\\linewidth}', raw)
    formulation_tex.write_text(raw)
    book = OLD.read_text()
    book = book.replace(r'\date{12 October 2026', r'\date{13 October 2026', 1)
    book = book.replace('Proposal working edition with public-data survey',
                        'Proposal working edition with developed software contract', 1)
    marker = r'\input{program/repair-v12/integrated-reader/chapters/software.tex}'
    assert book.count(marker) == 1
    book = book.replace(marker, r'\input{program/comprehensive-v14/work/TEXT.DRAFT.S1/chapter.tex}' + '\n' +
                        r'\input{program/execution/2026-10-13/survey-method-completion.tex}' + '\n' + marker, 1)
    marker = r'\input{program/gap-repair-v13/work/LA07/translation-extension.tex}'
    assert book.count(marker) == 1
    book = book.replace(marker, marker + '\n' + r'\input{program/execution/2026-10-13/formulation.tex}', 1)
    marker = "\\addcontentsline{toc}{chapter}{Reader's contract}"
    assert book.count(marker) == 1
    book = book.replace(marker, marker + r'''

Chapter \ref{exec13:survey} develops the survey method and a common causal
software contract. It compares five documented R paths, derives exact examples
of graph and target ambiguity, and specifies the proposed R and optional DoWhy
boundaries. The algebraic examples have been reproduced; the new package
paths remain source-reviewed designs rather than executed integrations.
Section \ref{exec13:formulation} extends the business-formulation discussion
with seven primary studies, three candidate package paths and an exact
example distinguishing population, trimmed and overlap-weighted effects.
''', 1)
    marker = 'program/public-data-v15/dataset-refs}'
    assert book.count(marker) == 1
    book = book.replace(marker, 'program/public-data-v15/dataset-refs,program/execution/2026-10-13/new-refs}', 1)
    DRIVER.write_text(book)
    print(json.dumps({'prepared': str(DRIVER.relative_to(ROOT)), 'chapter_words_rough': len(CHAPTER.read_text().split())}))


def build():
    guard()
    OUT.mkdir(exist_ok=True)
    env = dict(os.environ)
    env['TEXINPUTS'] = str(DOCS) + '//:' + env.get('TEXINPUTS', '')
    env['BIBINPUTS'] = str(DOCS) + '//:' + env.get('BIBINPUTS', '')
    command = ['pdflatex', '-no-shell-escape', '-interaction=nonstopmode', '-halt-on-error',
               '-output-directory=' + str(OUT), str(DRIVER)]

    def run(args, logfile):
        with (OUT / logfile).open('w') as stream:
            result = subprocess.run(args, cwd=DOCS, env=env, stdout=stream,
                                    stderr=subprocess.STDOUT, timeout=55)
        if result.returncode:
            raise ValueError('Build failed: ' + str(OUT / logfile))

    run(command, 'pass-1.log')
    run(['bibtex', str((OUT / NAME).relative_to(DOCS))], 'bibtex-pass.log')
    for index in range(2, 6):
        run(command, f'pass-{index}.log')
        log = (OUT / (NAME + '.log')).read_text(errors='replace')
        if index >= 3 and not any(t in log for t in ['Label(s) may have changed', 'Rerun to get']):
            break
    for token in ['undefined citations', 'undefined references', 'multiply defined', 'Missing character']:
        if token in log:
            raise ValueError('Unresolved build warning: ' + token)
    PDF.write_bytes((OUT / (NAME + '.pdf')).read_bytes())
    files = shared.scan(DRIVER)
    joined = '\n'.join(t for _, t in files)
    labels = re.findall(shared.LABEL, joined)
    if len(labels) != len(set(labels)):
        raise ValueError('Duplicate LaTeX label')
    cited = {key.strip() for group in re.findall(shared.CITE, joined) for key in group.split(',')}
    audits = [DOCS / 'program/public-data-v15/reader/source-audit.json',
              BASE / 'source-audit.json', BASE / 'source-audit-supplement.json',
              BASE / 'formulation-source-audit.json', BASE / 'survey-review-audit.json']
    entries = {}
    for path in audits:
        value = json.loads(path.read_text())
        shared.verify_refs(value)
        for item in value['sources']:
            key = item['integrated_citation_key']
            if key in entries and item != entries[key]:
                raise ValueError('Conflicting citation record: ' + key)
            entries[key] = item
    if not cited <= entries.keys():
        raise ValueError('Unaudited citations: ' + repr(cited - entries.keys()))
    audit = {'sources': [entries[k] for k in sorted(cited)],
             'tex_files': [ref(p, 'Compiled source') for p in sorted({p for p, _ in files})],
             'source_audits': [ref(p, 'Preserved primary-source claim audit') for p in audits],
             'added_bibliography': ref(BASE / 'new-refs.bib', 'Source identity and version'),
             'cutoff': '2026-10-07', 'visual_acceptance': False}
    shared.verify_refs(audit)
    core.write(OUT / 'source-audit.json', audit)
    subprocess.run(['pdftotext', '-layout', str(PDF), str(OUT / 'reader.txt')], check=True, timeout=25)
    info = subprocess.check_output(['pdfinfo', str(PDF)], text=True, timeout=15)
    pages = int(re.search(r'(?m)^Pages:\s+(\d+)', info).group(1))
    aux = (OUT / (NAME + '.aux')).read_text()

    def label_page(name):
        return int(re.search(r'\\newlabel\{' + re.escape(name) + r'\}\{\{[^}]*\}\{(\d+)\}', aux).group(1))

    first, last = label_page('exec13:survey'), label_page('exec13:survey-reviewed-end')
    ll_first, ll_last = label_page('exec13:formulation'), label_page('exec13:formulation-end')
    warnings = [line for line in log.splitlines() if any(t in line for t in ['Warning', 'Overfull', 'Underfull', 'Missing character'])]
    report = {'status': 'compiled_source_and_text_checked_working_draft', 'pages': pages,
              'pdf': ref(PDF, 'Integrated proposal successor'), 'driver': ref(DRIVER, 'Preserving driver'),
              'builder': ref(Path(__file__), 'Bounded build and inherited source verification'),
              'source_audit': ref(OUT / 'source-audit.json', 'Whole-book citations and exact compiled inputs'),
              'predecessor_pdf': ref(OLD.with_suffix('.pdf'), 'Preserved 393-page proposal'),
              'numbered_chapters': len(re.findall(r'\\contentsline \{chapter\}\{\\numberline', (OUT / (NAME + '.toc')).read_text())),
              'cited_records': len(cited), 'warnings': warnings,
              'S1': {'printed_first_page': first, 'printed_last_page': last, 'body_pages': last - first + 1,
                     'allocation': {'min': 8, 'target': 10, 'max': 12},
                     'draft_end_page': label_page('exec13:survey-end'),
                     'review_completion_start': label_page('exec13:survey-coverage'),
                     'overlap_credit': 'Physical span only; substantive credit requires chapter-review.json; no S2/LLM/integration credit'},
              'business_translation_extension': {'printed_first_page': ll_first, 'printed_last_page': ll_last,
                                                 'physical_span': ll_last - ll_first + 1,
                                                 'depth_acceptance': False},
              'final_acceptance': False, 'mandatory_repairs_closed': [], 'visual_acceptance': False,
              'visual_review': 'Pending fresh session: inherited image allowance exhausted'}
    core.write(OUT / 'build-report.json', report)
    layout.OUT = OUT
    layout.main()
    print(json.dumps({k: report[k] for k in ['pages', 'numbered_chapters', 'cited_records', 'S1',
                                           'business_translation_extension', 'warnings']}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['prepare', 'build'])
    args = parser.parse_args()
    prepare() if args.command == 'prepare' else build()
