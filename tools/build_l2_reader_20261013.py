#!/usr/bin/env python3
"""Build a preserving reader with the repaired L2 translation chapter."""
import argparse
import contextlib
import json
from pathlib import Path

import build_integrated_monograph_v12 as shared
import build_java_reader_20261013 as compiler
import master_control as core

ROOT = core.ROOT
DOCS = ROOT / 'docs'
BASE = DOCS / 'program/execution/2026-10-13/l2/final'
OUT = BASE / 'reader'
NAME = 'causal_proposal_l2_2026-10-13'
OLD = DOCS / 'causal_proposal_data_code_2026-10-13.tex'
DRIVER = DOCS / (NAME + '.tex')
PDF = DRIVER.with_suffix('.pdf')
CHAPTER = DOCS / 'program/comprehensive-v14/work/TEXT.DRAFT.L2/chapter.tex'
PRIOR_AUDIT = DOCS / 'program/execution/2026-10-13/data-code/final/reader/source-audit.json'
ref = shared.ref


def prepare():
    assert not DRIVER.exists() and not BASE.exists(), 'Preserve existing prepared reader'
    text = OLD.read_text()
    marker = r'\input{program/execution/2026-10-13/formulation.tex}'
    assert text.count(marker) == 1
    text = text.replace(marker, marker + '\n' +
                        r'\input{program/comprehensive-v14/work/TEXT.DRAFT.L2/chapter.tex}', 1)
    BASE.mkdir(parents=True)
    DRIVER.write_text(text)
    (BASE / 'refs.bib').write_text('% L2 uses source-audited bibliography entries already present in the predecessor.\n')
    prior = json.loads(PRIOR_AUDIT.read_text())
    import re
    cited = {k.strip() for group in re.findall(shared.CITE, CHAPTER.read_text())
             for k in group.split(',')}
    known = {x['integrated_citation_key'] for x in prior['sources']}
    assert cited <= known, 'L2 cites a source not present in the audited predecessor: ' + repr(cited-known)
    audit = {'sources': [], 'cutoff': '2026-10-07',
             'inherited_citation_keys': sorted(cited),
             'inherited_source_audit': ref(PRIOR_AUDIT, 'Exact-reader source identities and inspected anchors'),
             'chapter': ref(CHAPTER, 'Corrected source-audited chapter')}
    core.write(BASE / 'source-audit.json', audit)
    core.write(BASE / 'prepared-inputs.json', {
        'inputs': [ref(p, 'Preserved or reviewed input') for p in
                   [OLD, CHAPTER, PRIOR_AUDIT,
                    DOCS / 'program/execution/2026-10-13/l2/repair-progress-01.json',
                    DOCS / 'program/execution/2026-10-13/l2/source-audit-v2.json',
                    DOCS / 'program/execution/2026-10-13/l2/review-v2.json', Path(__file__)]],
        'generated': [ref(p, 'Preserving reader input') for p in
                      [DRIVER, BASE / 'refs.bib', BASE / 'source-audit.json']]})
    print(json.dumps({'prepared': str(DRIVER.relative_to(ROOT)), 'inherited_citations': len(cited)}))


def build():
    assert not PDF.exists() and not OUT.exists(), 'Preserve existing reader'
    shared.verify_refs(json.loads((BASE / 'prepared-inputs.json').read_text()))
    for name in ('BASE', 'OUT', 'NAME', 'OLD', 'DRIVER', 'PDF', 'PRIOR_AUDIT'):
        setattr(compiler, name, globals()[name])
    OUT.mkdir()
    with (OUT / 'compile-summary.txt').open('x') as stream, contextlib.redirect_stdout(stream):
        compiler.build()
    report = json.loads((OUT / 'build-report.json').read_text())
    report.pop('java_comparison', None)
    aux = (OUT / (NAME + '.aux')).read_text()
    import re
    match = re.search(r'\\newlabel\{exec13:l2-translation\}\{\{[^}]*\}\{(\d+)\}', aux)
    assert match, 'Missing new L2 chapter label'
    report.update(builder=ref(Path(__file__), 'Bounded preserving L2 builder'),
                  pdf=ref(PDF, 'L2 working monograph'),
                  predecessor_pdf=ref(OLD.with_suffix('.pdf'), 'Preserved 650-page reader'),
                  l2={'first_printed_page': int(match.group(1)),
                      'bank_truth': False, 'independent_review': False})
    core.write(OUT / 'build-report.json', report)
    print(json.dumps({k: report[k] for k in ('pages', 'cited_records', 'l2')}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=('prepare', 'build'))
    args = parser.parse_args()
    prepare() if args.command == 'prepare' else build()
