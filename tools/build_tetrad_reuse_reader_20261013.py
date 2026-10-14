#!/usr/bin/env python3
"""Add the Tetrad reuse decision to a preserved integrated reader."""
import argparse
import json
from pathlib import Path
import re
import subprocess

import build_java_reader_20261013 as inherited
import build_integrated_monograph_v12 as shared
import master_control as core

ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-13/tetrad-reuse'
OUT = BASE / 'reader'
NAME = 'causal_proposal_reuse_2026-10-13'
OLD = ROOT / 'docs/causal_proposal_latent_commercial_2026-10-13.tex'
DRIVER = ROOT / 'docs' / (NAME + '.tex')
PDF = DRIVER.with_suffix('.pdf')
PRIOR_AUDIT = ROOT / 'docs/program/execution/2026-10-13/commercial-latent/reader/source-audit.json'
ref = shared.ref


def configure():
    for key in ['BASE', 'OUT', 'NAME', 'OLD', 'DRIVER', 'PDF', 'PRIOR_AUDIT']:
        setattr(inherited, key, globals()[key])


def prepare():
    configure()
    inherited.guard()
    audit = json.loads((BASE / 'source-audit.json').read_text())
    shared.verify_refs(audit)
    subprocess.run(['pandoc', '--from=markdown+raw_tex+tex_math_single_backslash', '--to=latex',
                    '--wrap=auto', str(BASE / 'decision.md'), '-o', str(BASE / 'decision.tex')],
                   check=True, timeout=20)
    book = OLD.read_text()
    marker = r'\input{program/execution/2026-10-13/java-discovery/software-preserving.tex}'
    assert book.count(marker) == 1
    book = book.replace(marker, marker + '\n' + r'\input{program/execution/2026-10-13/tetrad-reuse/decision.tex}', 1)
    marker = 'program/execution/2026-10-13/commercial-latent/refs}'
    assert book.count(marker) == 1
    book = book.replace(marker, 'program/execution/2026-10-13/commercial-latent/refs,program/execution/2026-10-13/tetrad-reuse/refs}', 1)
    DRIVER.write_text(book)
    bib = []
    for source in audit['sources']:
        bib.append('@misc{' + source['integrated_citation_key'] + ',\n author={{' + shared.escape(source['author']) +
                   '}},\n title={' + shared.escape(source['title']) + '},\n year={' + str(source['year']) +
                   '},\n note={' + shared.escape(source['version_date']) + '}\n}\n')
    (BASE / 'refs.bib').write_text('\n'.join(bib))
    core.write(BASE / 'prepared-inputs.json', {
        'inputs': [ref(p, 'Bound reviewed input') for p in [OLD, PRIOR_AUDIT, BASE / 'decision.md', BASE / 'source-audit.json', Path(__file__)]],
        'outputs': [ref(p, 'Generated source') for p in [DRIVER, BASE / 'decision.tex', BASE / 'refs.bib']]})
    print(json.dumps({'prepared': str(DRIVER.relative_to(ROOT))}))


def build():
    configure()
    inherited.build()
    report = json.loads((OUT / 'build-report.json').read_text())
    aux = (OUT / (NAME + '.aux')).read_text()
    def page(label):
        return int(re.search(r'\\newlabel\{' + re.escape(label) + r'\}\{\{[^}]*\}\{(\d+)\}', aux).group(1))
    audit = json.loads((OUT / 'source-audit.json').read_text())
    audit['added_bibliography'] = ref(BASE / 'refs.bib', 'Tetrad reuse primary evidence and proposal choice')
    core.write(OUT / 'source-audit.json', audit)
    report.update(builder=ref(Path(__file__), 'Preserving Tetrad reuse integration'),
                  compile_routine=ref(ROOT / 'tools/build_java_reader_20261013.py', 'Inherited bounded compiler'),
                  predecessor_pdf=ref(OLD.with_suffix('.pdf'), 'Preserved 475-page reader'),
                  pdf=ref(PDF, 'Working reader with Tetrad reuse decision'),
                  source_audit=ref(OUT / 'source-audit.json', 'Whole-reader identities'))
    report['tetrad_reuse'] = {'first_printed_page': page('exec13:tetrad-reuse'),
                             'last_printed_page': page('exec13:tetrad-reuse-end'),
                             'runtime_admitted': False, 'integration_allowed': False}
    core.write(OUT / 'build-report.json', report)
    print(json.dumps({'pages': report['pages'], 'tetrad_reuse': report['tetrad_reuse'], 'visual_acceptance': False}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['prepare', 'build'])
    args = parser.parse_args()
    prepare() if args.command == 'prepare' else build()
