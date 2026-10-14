#!/usr/bin/env python3
"""Integrate reviewed custody findings without changing earlier chapter bytes."""
import argparse
from contextlib import redirect_stdout
import json
from pathlib import Path
import re
import subprocess

import audit_reader_traceability_v2_20261013 as trace
import build_native_evaluation_reader_v3_20261014 as engine
import review_artifact_custody_20261014 as work
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = work.ROOT
BASE = work.BASE / 'publication'
OUT = BASE / 'reader'
OLD = ROOT / 'docs/causal_proposal_latent_languages_v2_2026-10-14.tex'
PRIOR = ROOT / 'docs/program/execution/2026-10-14/other-latent/v2/publication/reader/source-audit.json'
NAME = 'causal_proposal_artifact_custody_2026-10-14'
DRIVER = ROOT / 'docs' / (NAME + '.tex')
PDF = DRIVER.with_suffix('.pdf')
SYN = work.BASE / 'development.md'


def prepare():
    assert not DRIVER.exists() and not (BASE / 'prepared-inputs.json').exists()
    audit = json.loads((work.BASE / 'source-audit.json').read_text())
    verify_bindings(audit)
    verify_bindings(json.loads((work.BASE / 'operation-receipt.json').read_text()))
    BASE.mkdir(exist_ok=True)
    subprocess.run(['pandoc', '--from=markdown+raw_tex+tex_math_dollars', '--to=latex',
                    '--wrap=auto', str(SYN), '-o', str(BASE / 'development.tex')],
                   check=True, timeout=20)
    write(BASE / 'source-audit.json', audit)
    bib = []
    for source in audit['sources']:
        bib.append('@misc{' + source['integrated_citation_key'] + ',\n author={{' +
                   engine.shared.escape(source['author']) + '}},\n title={' +
                   engine.shared.escape(source['title']) + '},\n year={2026},\n note={' +
                   engine.shared.escape(source['version_date']) + '}\n}\n')
    (BASE / 'refs.bib').write_text('\n'.join(bib))
    text = OLD.read_text()
    marker = r'\input{program/execution/2026-10-13/interchange/composition.tex}'
    assert text.count(marker) == 1
    text = text.replace(marker, marker + '\n' +
                        r'\input{program/execution/2026-10-14/artifact-custody/publication/development.tex}')
    text = re.sub(r'\\bibliography\{([^}]+)\}', lambda m: r'\bibliography{' + m.group(1) +
                  ',program/execution/2026-10-14/artifact-custody/publication/refs}', text)
    DRIVER.write_text(text)
    write(BASE / 'prepared-inputs.json', {
        'inputs': [ref(p, 'Preserved or reviewed source') for p in [
            OLD, PRIOR, SYN, work.BASE / 'source-audit.json', work.BASE / 'primary-review.json',
            work.BASE / 'local-observations.json', work.BASE / 'design-review.json', Path(__file__).resolve()]],
        'generated': [ref(p, 'Successor input') for p in [DRIVER, BASE / 'development.tex', BASE / 'refs.bib', BASE / 'source-audit.json']],
        'credit_policy': 'No automatic chapter-depth or mandatory-repair credit.',
        'visual_acceptance': False,
    })
    print(json.dumps({'prepared': str(DRIVER.relative_to(ROOT)), 'new_project_sources': 3}))


def build():
    for name, value in {'BASE': BASE, 'OUT': OUT, 'OLD': OLD, 'NAME': NAME,
                        'DRIVER': DRIVER, 'PDF': PDF, 'PRIOR_AUDIT': PRIOR}.items():
        setattr(engine, name, value)
    with (BASE / 'compile-summary.log').open('x') as stream:
        with redirect_stdout(stream):
            engine.build()
    report = json.loads((OUT / 'build-report.json').read_text())
    aux = (OUT / (NAME + '.aux')).read_text()
    report.update(builder=ref(Path(__file__).resolve(), 'Preserving custody builder'),
                  predecessor_pdf=ref(OLD.with_suffix('.pdf'), 'Frozen 715-page working reader'),
                  custody_sections={name: int(re.search(r'\\newlabel\{exec14:' + name +
                                    r'\}\{\{[^}]*\}\{(\d+)\}', aux).group(1))
                                    for name in ['artifact-custody', 'artifact-custody-end']})
    engine.core.write(OUT / 'build-report.json', report)
    result = trace.audit(DRIVER, OUT / 'source-audit.json')
    write(BASE / 'traceability-review.json', result)
    assert result['status'] == 'pass' and not result['issues']
    print(json.dumps({'pages': report['pages'], 'cited_records': report['cited_records'],
                      'custody_sections': report['custody_sections'], 'scholarly_pdfs': result['scholarly_pdfs'],
                      'material_warnings': [w for w in report['warnings'] if 'Underfull' not in w]}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['prepare', 'build'])
    args = parser.parse_args()
    prepare() if args.command == 'prepare' else build()
