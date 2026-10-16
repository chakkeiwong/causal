#!/usr/bin/env python3
"""Integrate the reviewed Julia/Rust/MATLAB temporal proposal without loss."""
import argparse
from contextlib import redirect_stdout
import json
from pathlib import Path
import re

import audit_reader_traceability_v2_20261013 as trace
import build_java_temporal_engine_20261016 as engine
import review_other_temporal_sources_20261017 as work
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT, WORK = work.ROOT, work.BASE
BASE = WORK / 'publication'
OUT = BASE / 'reader'
OLD = ROOT / 'docs/causal_proposal_ontology_2026-10-17.tex'
PRIOR = work.PRIOR
NAME = 'causal_proposal_other_temporal_2026-10-17'
DRIVER = ROOT / 'docs' / (NAME + '.tex')
PDF = DRIVER.with_suffix('.pdf')


def expected_driver():
    book = OLD.read_text()
    marker = r'\input{program/execution/2026-10-16/cxx-temporal/publication-v2/development.tex}'
    assert book.count(marker) == 1
    book = book.replace(marker, marker + '\n' +
        r'\input{program/execution/2026-10-17/other-temporal/development.tex}')
    pattern = re.compile(r'\\bibliography\{([^}]+)\}')
    assert len(pattern.findall(book)) == 1
    return pattern.sub(lambda m: r'\bibliography{' + m.group(1) +
        ',program/execution/2026-10-17/other-temporal/publication/refs}', book)


def prepare():
    assert not DRIVER.exists() and not BASE.exists()
    audit = json.loads((WORK / 'source-audit.json').read_text())
    verify_bindings(audit)
    verify_bindings(json.loads((WORK / 'author-review.json').read_text()))
    BASE.mkdir()
    write(BASE / 'source-audit.json', audit)
    bib = []
    for source in audit['sources']:
        author = engine.shared.escape(source['author'])
        if source['kind'] != 'paper':
            author = '{' + author + '}'
        bib.append('@misc{' + source['integrated_citation_key'] + ',\n author={' +
            author + '},\n title={' + engine.shared.escape(source['title']) +
            '},\n year={' + str(source['year']) + '},\n note={' +
            engine.shared.escape(source['version_date']) + '}\n}\n')
    (BASE / 'refs.bib').write_text('\n'.join(bib))
    DRIVER.write_text(expected_driver())
    write(BASE / 'prepared-inputs.json', {
        'inputs': [ref(path, 'Reviewed preserving input') for path in
            [OLD, PRIOR, WORK / 'author-review.json', WORK / 'development.tex', Path(__file__)]],
        'generated': [ref(path, 'Successor source') for path in
            [DRIVER, BASE / 'source-audit.json', BASE / 'refs.bib']],
        'credit_policy': 'Bounded comparison only; no automatic coverage, depth, integration or product acceptance.',
        'visual_acceptance': False})
    print(json.dumps({'prepared': str(DRIVER.relative_to(ROOT)), 'new_citations': len(audit['sources'])}))


def build():
    for key, value in {'BASE': BASE, 'OUT': OUT, 'OLD': OLD, 'NAME': NAME,
            'DRIVER': DRIVER, 'PDF': PDF, 'PRIOR_AUDIT': PRIOR}.items():
        setattr(engine, key, value)
    with (BASE / 'compile-summary.log').open('x') as stream:
        with redirect_stdout(stream):
            engine.build()
    report = json.loads((OUT / 'build-report.json').read_text())
    aux = (OUT / (NAME + '.aux')).read_text()
    sections = {}
    for label in ['exec17:other-temporal', 'exec17:other-temporal-end', 'tab:exec17-temporal-choice']:
        match = re.search(r'\\newlabel\{' + re.escape(label) + r'\}\{\{[^}]*\}\{(\d+)\}', aux)
        assert match, label
        sections[label] = int(match.group(1))
    report.update(builder=ref(Path(__file__), 'Preserving temporal comparison builder'),
        predecessor_pdf=ref(OLD.with_suffix('.pdf'), 'Frozen 871-page reader'),
        other_temporal_sections=sections)
    engine.core.write(OUT / 'build-report.json', report)
    audited = trace.audit(DRIVER, OUT / 'source-audit.json')
    write(BASE / 'traceability-review.json', audited)
    assert report['cited_records'] == 696 and report['pages'] > 871
    assert audited['status'] == 'pass' and not audited['issues'] and audited['scholarly_pdfs'] == 187
    print(json.dumps({'pages': report['pages'], 'cited_records': report['cited_records'],
        'sections': sections, 'scholarly_pdfs': audited['scholarly_pdfs'],
        'material_warnings': [w for w in report['warnings'] if 'Underfull' not in w]}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['prepare', 'build'])
    args = parser.parse_args()
    {'prepare': prepare, 'build': build}[args.command]()
