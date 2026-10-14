#!/usr/bin/env python3
"""Integrate the reviewed Causica reference in a preserving working reader."""
import argparse
from contextlib import redirect_stdout
import json
from pathlib import Path
import re

import audit_reader_traceability_v2_20261013 as trace
import build_native_evaluation_reader_v3_20261014 as engine
import review_causica_reuse_20261014 as work
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = work.ROOT
BASE = work.BASE / 'publication'
OUT = BASE / 'reader'
OLD = ROOT / 'docs/causal_proposal_benchmarking_v3_2026-10-14.tex'
PRIOR = work.AUDIT
NAME = 'causal_proposal_causica_contracts_2026-10-14'
DRIVER = ROOT / 'docs' / (NAME + '.tex')
PDF = DRIVER.with_suffix('.pdf')
BS, NL = chr(92), chr(10)


def prepare():
    assert not DRIVER.exists() and not BASE.exists()
    BASE.mkdir()
    audit = json.loads((work.BASE / 'source-audit.json').read_text())
    verify_bindings(audit)
    verify_bindings(json.loads((work.BASE / 'author-review.json').read_text()))
    assert work.exact() == json.loads((work.BASE / 'exact-results.json').read_text())
    write(BASE / 'source-audit.json', audit)
    chapter = (work.BASE / 'development.template').read_text().replace('§', BS)
    chapter = chapter.replace('.' + BS + 'citep', '. ' + BS + 'citep')
    assert BS + 'section{Causica:' in chapter and '§' not in chapter
    (BASE / 'development.tex').write_text(chapter)
    bib = []
    for s in audit['sources']:
        author = engine.shared.escape(s.get('author') or ' and '.join(s['authors']))
        if s['kind'] != 'paper':
            author = '{' + author + '}'
        bib.append('@misc{' + s['integrated_citation_key'] + ',' + NL + ' author={' + author + '},' + NL +
                   ' title={' + engine.shared.escape(s['title']) + '},' + NL +
                   ' year={' + str(s['year']) + '},' + NL +
                   ' note={' + engine.shared.escape(s['version_date']) + '}' + NL + '}' + NL)
    (BASE / 'refs.bib').write_text(NL.join(bib))
    book = OLD.read_text()
    marker = BS + 'input{program/execution/2026-10-14/causalnex-reuse/decision.tex}'
    new = BS + 'input{program/execution/2026-10-14/causica-reuse/publication/development.tex}'
    assert book.count(marker) == 1
    book = book.replace(marker, marker + NL + new)
    pattern = re.compile(re.escape(BS + 'bibliography{') + '([^}]+)' + re.escape('}'))
    assert len(pattern.findall(book)) == 1
    book = pattern.sub(lambda m: BS + 'bibliography{' + m.group(1) +
                       ',program/execution/2026-10-14/causica-reuse/publication/refs}', book)
    DRIVER.write_text(book)
    write(BASE / 'prepared-inputs.json', {
        'inputs': [ref(p, 'Reviewed preserving input') for p in
                   [OLD, PRIOR, work.BASE / 'development.template', work.BASE / 'author-review.json', Path(__file__)]],
        'generated': [ref(p, 'Successor source') for p in
                      [DRIVER, BASE / 'development.tex', BASE / 'source-audit.json', BASE / 'refs.bib']],
        'credit_policy': 'No automatic chapter-depth or mandatory-repair completion.', 'visual_acceptance': False})
    print(json.dumps({'prepared': str(DRIVER.relative_to(ROOT)), 'added_records': len(audit['sources'])}))


def build():
    for name, value in {'BASE': BASE, 'OUT': OUT, 'OLD': OLD, 'NAME': NAME,
                        'DRIVER': DRIVER, 'PDF': PDF, 'PRIOR_AUDIT': PRIOR}.items():
        setattr(engine, name, value)
    with (BASE / 'compile-summary.log').open('x') as stream:
        with redirect_stdout(stream):
            engine.build()
    report = json.loads((OUT / 'build-report.json').read_text())
    aux = (OUT / (NAME + '.aux')).read_text()
    def page(label):
        pattern = re.escape(BS + 'newlabel{' + label + '}{{') + '[^}]*' + re.escape('}{') + '([0-9]+)'
        return int(re.search(pattern, aux).group(1))
    report.update(builder=ref(Path(__file__), 'Preserving Causica reader builder'),
                  predecessor_pdf=ref(OLD.with_suffix('.pdf'), 'Frozen 756-page reader'),
                  causica_sections={label: page('exec14:' + label) for label in
                                    ['causica-contract', 'causica-contract-end']})
    engine.core.write(OUT / 'build-report.json', report)
    result = trace.audit(DRIVER, OUT / 'source-audit.json')
    write(BASE / 'traceability-review.json', result)
    assert report['cited_records'] == 577 and report['pages'] > 756
    assert result['status'] == 'pass' and not result['issues'] and result['scholarly_pdfs'] == 163
    print(json.dumps({'pages': report['pages'], 'cited_records': report['cited_records'],
                      'sections': report['causica_sections'], 'scholarly_pdfs': result['scholarly_pdfs'],
                      'material_warnings': [w for w in report['warnings'] if 'Underfull' not in w]}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['prepare', 'build'])
    args = parser.parse_args()
    {'prepare': prepare, 'build': build}[args.command]()
