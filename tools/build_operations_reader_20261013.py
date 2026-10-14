#!/usr/bin/env python3
"""Replace the short operating chapter with its preserving developed successor."""
import argparse
import json
from pathlib import Path
import re

import build_java_reader_20261013 as inherited
import build_integrated_monograph_v12 as shared
import master_control as core

ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-13/operational-adoption'
OUT = BASE / 'reader'
NAME = 'causal_proposal_operations_2026-10-13'
OLD = ROOT / 'docs/causal_proposal_active_experiments_2026-10-13.tex'
DRIVER = ROOT / 'docs' / (NAME+'.tex')
PDF = DRIVER.with_suffix('.pdf')
PRIOR_AUDIT = ROOT / 'docs/program/execution/2026-10-13/active-experiments/reader/source-audit.json'
OLD_INTEGRATION = ROOT / 'docs/program/execution/2026-10-13/workspace/integration-tail.tex'
CHAPTER = ROOT / 'docs/program/comprehensive-v14/work/TEXT.DRAFT.I4/chapter.tex'
ref = shared.ref


def configure():
    for key in ['BASE', 'OUT', 'NAME', 'OLD', 'DRIVER', 'PDF', 'PRIOR_AUDIT']:
        setattr(inherited, key, globals()[key])


def expected_wrapper():
    original = OLD_INTEGRATION.read_text()
    starts = list(re.finditer(r'\\chapter\{', original))
    assert len(starts) == 1
    assert original[starts[0].start():].strip() == (BASE / 'inherited-operations.tex').read_text().strip()
    return original[:starts[0].start()]+r'\input{program/comprehensive-v14/work/TEXT.DRAFT.I4/chapter.tex}'+'\n'


def expected_driver():
    book = OLD.read_text()
    marker = r'\input{program/execution/2026-10-13/workspace/integration-tail.tex}'
    assert book.count(marker) == 1
    book = book.replace(marker, r'\input{program/execution/2026-10-13/operational-adoption/integration-preserving.tex}', 1)
    marker = 'program/execution/2026-10-13/active-experiments/refs}'
    assert book.count(marker) == 1
    return book.replace(marker, 'program/execution/2026-10-13/active-experiments/refs,program/execution/2026-10-13/operational-adoption/refs}', 1)


def prepare():
    configure(); inherited.guard()
    audit = json.loads((BASE / 'source-audit.json').read_text())
    review = json.loads((BASE / 'author-review.json').read_text())
    assert review['status'] == 'pass'
    shared.verify_refs(audit); shared.verify_refs(review)
    (BASE / 'integration-preserving.tex').write_text(expected_wrapper())
    DRIVER.write_text(expected_driver())
    entries = []
    for s in audit['sources']:
        entries.append('@misc{'+s['integrated_citation_key']+',\n author={{'+shared.escape(s['author'])
            +'}},\n title={'+shared.escape(s['title'])+'},\n year={'+str(s['year'])
            +'},\n note={'+shared.escape(s['version_date'])+'}\n}\n')
    (BASE / 'refs.bib').write_text('\n'.join(entries))
    core.write(BASE / 'prepared-inputs.json', {
        'inputs': [ref(p, 'Reviewed integration input') for p in [OLD, PRIOR_AUDIT, OLD_INTEGRATION, CHAPTER,
            BASE / 'source-audit.json', BASE / 'author-review.json', Path(__file__)]],
        'generated': [ref(p, 'Prepared successor') for p in [DRIVER, BASE / 'integration-preserving.tex', BASE / 'refs.bib']]})
    print(json.dumps({'prepared': str(DRIVER.relative_to(ROOT))}))


def build():
    configure(); OUT.mkdir(exist_ok=True)
    for suffix in ['.aux', '.bbl', '.toc', '.out']:
        p = OUT / (NAME+suffix)
        if not p.exists(): p.write_text('')
    inherited.build()
    audit = json.loads((OUT / 'source-audit.json').read_text())
    audit['added_bibliography'] = ref(BASE / 'refs.bib', 'Operational source, actual fault receipts and exact examples')
    core.write(OUT / 'source-audit.json', audit)
    report = json.loads((OUT / 'build-report.json').read_text())
    report.pop('java_comparison', None)
    aux = (OUT / (NAME+'.aux')).read_text()
    def page(label):
        return int(re.search(r'\\newlabel\{'+re.escape(label)+r'\}\{\{[^}]*\}\{(\d+)\}', aux).group(1))
    report.update(builder=ref(Path(__file__), 'Preserving operating chapter integration'),
        compile_routine=ref(ROOT / 'tools/build_java_reader_20261013.py', 'Unchanged bounded compiler'),
        pdf=ref(PDF, 'Working monograph with developed operational adoption'),
        predecessor_pdf=ref(OLD.with_suffix('.pdf'), 'Preserved 581-page predecessor'),
        source_audit=ref(OUT / 'source-audit.json', 'Whole-reader source identities'),
        operational_adoption={'first_printed_page': page('in:operations'),
            'last_printed_page': page('exec13:operations-end'), 'coverage_acceptance': False, 'new_runtime_trials': 0})
    core.write(OUT / 'build-report.json', report)
    print(json.dumps({k: report[k] for k in ['pages', 'cited_records', 'operational_adoption']}))


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('command', choices=['prepare', 'build']); args = p.parse_args()
    prepare() if args.command == 'prepare' else build()
