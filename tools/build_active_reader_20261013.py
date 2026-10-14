#!/usr/bin/env python3
"""Integrate active experiment selection while preserving the 571-page reader."""
import argparse
import json
from pathlib import Path
import re

import build_java_reader_20261013 as inherited
import build_integrated_monograph_v12 as shared
import master_control as core

ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-13/active-experiments'
OUT = BASE / 'reader'
NAME = 'causal_proposal_active_experiments_2026-10-13'
OLD = ROOT / 'docs/causal_proposal_commercial_identification_2026-10-13.tex'
DRIVER = ROOT / 'docs' / (NAME+'.tex')
PDF = DRIVER.with_suffix('.pdf')
PRIOR_AUDIT = ROOT / 'docs/program/execution/2026-10-13/commercial-identification/reader/source-audit.json'
ref = shared.ref


def configure():
    for key in ['BASE', 'OUT', 'NAME', 'OLD', 'DRIVER', 'PDF', 'PRIOR_AUDIT']:
        setattr(inherited, key, globals()[key])


def expected_driver():
    book = OLD.read_text()
    marker = r'\input{program/execution/2026-10-13/llm-census/temporal.tex}'
    assert book.count(marker) == 1
    book = book.replace(marker, marker+'\n'+r'\input{program/execution/2026-10-13/active-experiments/chapter.tex}', 1)
    marker = 'program/execution/2026-10-13/commercial-identification/refs}'
    assert book.count(marker) == 1
    return book.replace(marker, 'program/execution/2026-10-13/commercial-identification/refs,program/execution/2026-10-13/active-experiments/refs}', 1)


def prepare():
    configure(); inherited.guard()
    audit = json.loads((BASE / 'source-audit.json').read_text())
    review = json.loads((BASE / 'author-review.json').read_text())
    assert review['status'] == 'pass'
    shared.verify_refs(audit); shared.verify_refs(review)
    DRIVER.write_text(expected_driver())
    entries = []
    paper_authors = {
        'exec13_active_2609_33357': "Huang, Nan and Tapia-Pacheco, Mario and Zhou, Kun and Huang, Yiming and Barrientos D{\\'i}az, Kevin Jos{\\'e} and Amariuta, Tiffany and Shang, Jingbo",
        'exec13_active_2609_15973': 'Yang, Ling and Yin, Zhenfei and Wu, Yingcheng'}
    for s in audit['sources']:
        key = s['integrated_citation_key']
        author = '{'+paper_authors[key]+'}' if key in paper_authors else '{{'+shared.escape(s['author'])+'}}'
        entries.append('@misc{'+key+',\n author='+author
            +',\n title={'+shared.escape(s['title'])+'},\n year={'+str(s['year'])
            +'},\n note={'+shared.escape(s['version_date'])+'}\n}\n')
    (BASE / 'refs.bib').write_text('\n'.join(entries))
    core.write(BASE / 'prepared-inputs.json', {
        'inputs': [ref(p, 'Reviewed integration input') for p in
                   [OLD, PRIOR_AUDIT, BASE / 'source-audit.json', BASE / 'chapter.tex', BASE / 'author-review.json', Path(__file__)]],
        'generated': [ref(DRIVER, 'Preserving driver'), ref(BASE / 'refs.bib', 'Seven added audited references')]})
    print(json.dumps({'prepared': str(DRIVER.relative_to(ROOT))}))


def build():
    configure(); OUT.mkdir(exist_ok=True)
    for suffix in ['.aux', '.bbl', '.toc', '.out']:
        p = OUT / (NAME+suffix)
        if not p.exists(): p.write_text('')
    inherited.build()
    audit = json.loads((OUT / 'source-audit.json').read_text())
    audit['added_bibliography'] = ref(BASE / 'refs.bib', 'Active-design primary sources and exact project construction')
    core.write(OUT / 'source-audit.json', audit)
    report = json.loads((OUT / 'build-report.json').read_text())
    report.pop('java_comparison', None)
    aux = (OUT / (NAME+'.aux')).read_text()
    def page(label):
        return int(re.search(r'\\newlabel\{'+re.escape(label)+r'\}\{\{[^}]*\}\{(\d+)\}', aux).group(1))
    report.update(builder=ref(Path(__file__), 'Preserving active-experiment integration'),
        compile_routine=ref(ROOT / 'tools/build_java_reader_20261013.py', 'Unchanged bounded compiler'),
        pdf=ref(PDF, 'Working monograph with developed active experiment selection'),
        predecessor_pdf=ref(OLD.with_suffix('.pdf'), 'Preserved 571-page predecessor'),
        source_audit=ref(OUT / 'source-audit.json', 'Whole-reader source audit'),
        active_experiments={'first_printed_page': page('exec13:active-experiments'),
                            'last_printed_page': page('exec13:active-experiments-end'),
                            'coverage_acceptance': False, 'live_model_calls': 0})
    core.write(OUT / 'build-report.json', report)
    print(json.dumps({k: report[k] for k in ['pages', 'cited_records', 'active_experiments']}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['prepare', 'build'])
    args = parser.parse_args()
    prepare() if args.command == 'prepare' else build()
