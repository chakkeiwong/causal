#!/usr/bin/env python3
"""Build the public-data survey and a preserving integrated monograph successor."""
import argparse
import json
import os
import re
import subprocess
from pathlib import Path

import build_integrated_monograph_v12 as shared
import master_control as core
import review_gap_reader_v13 as layout

ROOT = core.ROOT
DOCS = ROOT / 'docs'
BASE = DOCS / 'program/public-data-v15'
NAME = 'causal_proposal_public_data_2026-10-12'
OLD = DOCS / 'causal_integrated_working_v13_1_2026-10-12.tex'


def ref(path, anchor):
    return shared.ref(path, anchor)


def prepare():
    source_audit = json.loads((BASE / 'source-audit.json').read_text())
    shared.verify_refs(source_audit)
    chapter = BASE / 'survey.tex'
    subprocess.run(['pandoc', str(BASE / 'survey.md'), '--from=markdown+raw_tex+tex_math_single_backslash',
                    '--to=latex', '--top-level-division=chapter', '-o', str(chapter)], check=True, timeout=25)
    raw = chapter.read_text()
    # Wrap the three-column portfolio/evidence tables in their actual cell widths.
    for count, widths in [(3, [.22, .36, .42])]:
        token = r'\begin{longtable}[]{@{}' + 'l' * count + r'@{}}'
        columns = ''.join(r'>{\raggedright\arraybackslash}p{\dimexpr ' + str(w) + r'\linewidth-2\tabcolsep\relax}' for w in widths)
        raw = raw.replace(token, r'\begin{longtable}[]{@{}' + columns + r'@{}}')
    raw = re.sub(r'(\\begin\{minipage\}\[[bt]\])\{[0-9.]+\\columnwidth\}', r'\1{\\linewidth}', raw)
    chapter.write_text(raw)
    entries = []
    authors = {
        'pd15_uci_bank': 'UCI Machine Learning Repository',
        'pd15_uci_credit': 'UCI Machine Learning Repository',
        'pd15_fdic_sod': 'Federal Deposit Insurance Corporation',
        'pd15_fdic_api_spec': 'Federal Deposit Insurance Corporation',
        'pd15_y9c': 'Board of Governors of the Federal Reserve System',
        'pd15_h8': 'Board of Governors of the Federal Reserve System',
        'pd15_scf': 'Board of Governors of the Federal Reserve System',
        'pd15_hmda_schema': 'Consumer Financial Protection Bureau',
        'pd15_freddie': 'Freddie Mac', 'pd15_fannie': 'Fannie Mae',
        'pd15_criteo': 'Criteo AI Lab', 'pd15_nsw_docs': 'causaldata contributors',
        'pd15_lalonde_pinned': 'MatchIt contributors',
        'pd15_acic_pinned': 'ACIC competition maintainers',
        'pd15_cevae_pinned': 'CEVAE authors', 'pd15_nhefs_pinned': 'causallib contributors',
        'pd15_mpdta': 'did contributors', 'pd15_causalbench_pinned': 'CausalBench authors',
        'pd15_febrl_source': 'Python Record Linkage Toolkit contributors',
        'pd15_paysim_pinned': 'PaySim authors', 'pd15_cladder_pinned': 'CLadder authors',
        'pd15_corr2cause_pinned': 'Corr2Cause authors',
        'pd15_profile': 'Causal banking research project',
    }
    for e in source_audit['sources']:
        key = e['integrated_citation_key']
        # The two inherited records already have bibliography entries in the book.
        if key in ['public401k', 'public_macrodata_dynamic']:
            continue
        title = shared.escape(e['title'])
        url = e['source_identity']
        note = shared.escape(str(e['version_date']))
        entries.append('@misc{' + key + ',\n author={{' + authors[key] + '}},\n' +
                       ' title={' + title + '},\n year={2026},\n note={' + note + '}' +
                       (',\n url={' + url + '}' if url.startswith('https://') else '') + '\n}\n')
    (BASE / 'dataset-refs.bib').write_text('\n'.join(entries))
    support = '\n'.join([r'\providecommand{\tightlist}{\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}',
                          r'\usepackage{calc}', r'\providecommand{\passthrough}[1]{#1}',
                          r'\setlength{\emergencystretch}{4em}']) + '\n'
    (BASE / 'support.tex').write_text(support)
    standalone = r'''\documentclass[11pt,a4paper,openany]{book}
\input{preamble}
\input{program/public-data-v15/support}
\raggedbottom
\title{\sffamily\bfseries Public Data for a Causal Banking Proposal\\[12pt]
\Large Dataset survey, prototype portfolio and the case for later experiments}
\author{Causal banking research and product proposal}
\date{12 October 2026\\Literature cutoff: 7 October 2026}
\begin{document}
\frontmatter\maketitle
\begingroup\setlength{\parskip}{0pt}\tableofcontents\endgroup
\mainmatter
\input{program/public-data-v15/survey}
\backmatter
\bibliographystyle{plainnat}
\bibliography{causal_banking_refs,program/public-data-v15/dataset-refs}
\end{document}
'''
    (BASE / 'public-data-survey.tex').write_text(standalone)
    book = OLD.read_text().replace('Integrated working edition, revision 13.1', 'Proposal working edition with public-data survey', 1)
    book = book.replace(r'\input{preamble}', r'\input{preamble}' + '\n' + r'\input{program/public-data-v15/support}', 1)
    marker = r"\addcontentsline{toc}{chapter}{Reader's contract}"
    note = r'''

The immediate deliverable is a product proposal and bounded prototype evidence.
Public financial observations, experimental benchmarks and clearly identified
synthetic mechanisms can establish technical merit before costly bank experiments.
Chapters \ref{pd15:evidence}--\ref{pd15:investment} add a systematic 24-family
dataset survey, six focused study families and a value-of-information argument.
They include a newly executed public bank-data profile; the proposed studies
are not presented as completed experiments.

References elsewhere in this book to authentic bank truth, independent product
acceptance, production interfaces and measured bank ROI describe later conditional
qualification. They are not prerequisites for completing this proposal.
The software, language-model and integration repairs remain open. Current local
demonstrations and public data support only their explicitly stated claims.
'''
    book = book.replace(marker, marker + note, 1)
    marker = r'\input{reconstruction/21_investment}'
    book = book.replace(marker, marker + '\n' + r'\input{program/public-data-v15/survey}', 1)
    marker = 'program/gap-execution-v13_1/reader/new-refs}'
    book = book.replace(marker, 'program/gap-execution-v13_1/reader/new-refs,program/public-data-v15/dataset-refs}', 1)
    (DOCS / (NAME + '.tex')).write_text(book)
    print(json.dumps({'prepared': True, 'survey_words': len((BASE / 'survey.md').read_text().split())}))


def build(kind):
    integrated = kind == 'book'
    out = BASE / ('reader' if integrated else 'survey-reader')
    out.mkdir(exist_ok=True)
    driver = DOCS / (NAME + '.tex') if integrated else BASE / 'public-data-survey.tex'
    name = driver.stem
    pdf = DOCS / (NAME + '.pdf') if integrated else BASE / 'public-data-survey.pdf'
    state = core.read(ROOT, core.STATE)
    if any(d['path'] == str(pdf.relative_to(ROOT)) for d in state['deliveries']):
        raise ValueError('Delivered bytes are frozen; use a successor')
    env = dict(os.environ)
    env['TEXINPUTS'] = str(DOCS) + '//:' + env.get('TEXINPUTS', '')
    env['BIBINPUTS'] = str(DOCS) + '//:' + env.get('BIBINPUTS', '')
    command = ['pdflatex', '-no-shell-escape', '-interaction=nonstopmode', '-halt-on-error', '-output-directory=' + str(out), str(driver)]
    def run(args, logfile):
        with (out / logfile).open('w') as stream:
            r = subprocess.run(args, cwd=DOCS, env=env, stdout=stream, stderr=subprocess.STDOUT, timeout=55)
        if r.returncode:
            raise ValueError('Build failed: ' + str(out / logfile))
    run(command, 'pass-1.log')
    run(['bibtex', str((out / name).relative_to(DOCS))], 'bibtex-pass.log')
    for i in range(2, 6):
        run(command, f'pass-{i}.log')
        log = (out / (name + '.log')).read_text(errors='replace')
        if i >= 3 and not any(t in log for t in ['Label(s) may have changed', 'Rerun to get']):
            break
    for token in ['undefined citations', 'undefined references', 'multiply defined', 'Missing character']:
        if token in log:
            raise ValueError('Unresolved build warning: ' + token)
    pdf.write_bytes((out / (name + '.pdf')).read_bytes())
    files = shared.scan(driver)
    combined = '\n'.join(t for _, t in files)
    labels = re.findall(shared.LABEL, combined)
    if len(labels) != len(set(labels)):
        raise ValueError('Duplicate label')
    cited = {k.strip() for group in re.findall(shared.CITE, combined) for k in group.split(',')}
    inherited_path = DOCS / 'program/gap-execution-v13_1/reader/source-audit.json'
    inherited = core.read(ROOT, str(inherited_path.relative_to(ROOT)))
    entries = {e['integrated_citation_key']: e for e in inherited['sources']}
    entries.update({e['integrated_citation_key']: e for e in core.read(ROOT, str((BASE / 'source-audit.json').relative_to(ROOT)))['sources']})
    if not cited <= entries.keys():
        raise ValueError('Unaudited citations: ' + repr(cited - entries.keys()))
    audit = {'sources': [entries[k] for k in sorted(cited)],
             'tex_files': [ref(p, 'Compiled source') for p in sorted({p for p, _ in files})],
             'dataset_bibliography': ref(BASE / 'dataset-refs.bib', 'Source identities and dates'),
             'dataset_survey': ref(BASE / 'source-audit.json', 'Inspected claims and limitations'),
             'inherited_audit': ref(inherited_path, 'Preserved full predecessor audit'),
             'cutoff': '2026-10-07', 'visual_acceptance': False}
    shared.verify_refs(audit)
    core.write(out / 'source-audit.json', audit)
    subprocess.run(['pdftotext', '-layout', str(pdf), str(out / 'reader.txt')], check=True, timeout=25)
    info = subprocess.check_output(['pdfinfo', str(pdf)], text=True, timeout=15)
    pages = int(re.search(r'(?m)^Pages:\s+(\d+)', info).group(1))
    warnings = [l for l in log.splitlines() if any(t in l for t in ['Warning', 'Overfull', 'Underfull', 'Missing character'])]
    report = {'status': 'compiled_source_and_text_checked_working_draft', 'pages': pages,
              'pdf': ref(pdf, 'Integrated proposal successor' if integrated else 'Public-data survey'),
              'driver': ref(driver, 'Versioned driver'), 'builder': ref(Path(__file__), 'Preserving survey/book builder'),
              'source_audit': ref(out / 'source-audit.json', 'Every cited source and compiled input'),
              'numbered_chapters': len(re.findall(r'\\contentsline \{chapter\}\{\\numberline', (out / (name + '.toc')).read_text())),
              'cited_records': len(cited), 'warnings': warnings,
              'final_acceptance': False, 'mandatory_repairs_closed': [], 'visual_acceptance': False,
              'visual_review': 'Pending fresh session: inherited image allowance exhausted'}
    if integrated:
        report['predecessor_pdf'] = ref(OLD.with_suffix('.pdf'), 'Preserved 375-page book')
    core.write(out / 'build-report.json', report)
    layout.OUT = out
    layout.main()
    print(json.dumps({k: report[k] for k in ['pages', 'numbered_chapters', 'cited_records', 'warnings']}))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('command', choices=['prepare', 'survey', 'book'])
    args = p.parse_args()
    prepare() if args.command == 'prepare' else build(args.command)
