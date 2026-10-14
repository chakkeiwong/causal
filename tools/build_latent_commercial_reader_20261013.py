#!/usr/bin/env python3
"""Integrate the commercial latent-variable comparison without rewriting evidence."""
import argparse
import json
from pathlib import Path
import re
import subprocess

import build_java_reader_20261013 as inherited
import build_integrated_monograph_v12 as shared
import master_control as core

ROOT = core.ROOT
DOCS = ROOT / 'docs'
BASE = DOCS / 'program/execution/2026-10-13/commercial-latent'
OUT = BASE / 'reader'
NAME = 'causal_proposal_latent_commercial_2026-10-13'
OLD = DOCS / 'causal_proposal_servicing_2026-10-13.tex'
DRIVER = DOCS / (NAME + '.tex')
PDF = DRIVER.with_suffix('.pdf')
PRIOR_AUDIT = DOCS / 'program/execution/2026-10-13/servicing/reader/source-audit.json'
ref = shared.ref


def configure():
    for key in ['BASE', 'OUT', 'NAME', 'OLD', 'DRIVER', 'PDF', 'PRIOR_AUDIT']:
        setattr(inherited, key, globals()[key])


def prepare():
    configure()
    inherited.guard()
    audit = json.loads((BASE / 'source-audit.json').read_text())
    shared.verify_refs(audit)
    subprocess.run(['pandoc', '--from=markdown+raw_tex+tex_math_single_backslash',
                    '--to=latex', '--wrap=auto', str(BASE / 'comparison.md'),
                    '-o', str(BASE / 'comparison.tex')], check=True, timeout=20)
    book = OLD.read_text()
    marker = r'\input{program/execution/2026-10-13/commercial/comparison.tex}'
    assert book.count(marker) == 1
    book = book.replace(marker, marker + '\n' + r'\input{program/execution/2026-10-13/commercial-latent/comparison.tex}', 1)
    marker = "\\addcontentsline{toc}{chapter}{Reader's contract}"
    assert book.count(marker) == 1
    book = book.replace(marker, marker + r'''

Section \ref{exec13:latent-commercial} compares commercial latent-model fitting,
clustering and trial-specific causal effects. It develops hidden-risk and
compliance examples and distinguishes these operations from causal discovery
under hidden confounding. Vendor capabilities are documented, not executed here.
''', 1)
    marker = 'program/execution/2026-10-13/servicing/refs}'
    assert book.count(marker) == 1
    book = book.replace(marker, 'program/execution/2026-10-13/servicing/refs,program/execution/2026-10-13/commercial-latent/refs}', 1)
    DRIVER.write_text(book)
    entries = []
    for source in audit['sources']:
        entries.append('@misc{' + source['integrated_citation_key'] + ',\n author={{' + shared.escape(source['author']) +
                       '}},\n title={' + shared.escape(source['title']) + '},\n year={' + str(source['year']) +
                       '},\n note={' + shared.escape(source['version_date']) + '}\n}\n')
    (BASE / 'refs.bib').write_text('\n'.join(entries))
    core.write(BASE / 'prepared-inputs.json', {
        'inputs': [ref(p, 'Reviewed input identity') for p in [OLD, PRIOR_AUDIT, Path(__file__),
                    ROOT / 'tools/build_java_reader_20261013.py', BASE / 'comparison.md', BASE / 'source-audit.json']],
        'generated': [ref(p, 'Prepared output identity') for p in [DRIVER, BASE / 'comparison.tex', BASE / 'refs.bib']]})
    print(json.dumps({'prepared': str(DRIVER.relative_to(ROOT))}))


def build():
    configure()
    inherited.build()
    report = json.loads((OUT / 'build-report.json').read_text())
    aux = (OUT / (NAME + '.aux')).read_text()
    def page(label):
        return int(re.search(r'\\newlabel\{' + re.escape(label) + r'\}\{\{[^}]*\}\{(\d+)\}', aux).group(1))
    report['builder'] = ref(Path(__file__), 'Commercial latent-model integration with preserved bounded compiler')
    report['compile_routine'] = ref(ROOT / 'tools/build_java_reader_20261013.py', 'Unmodified inherited bounded build')
    report['predecessor_pdf'] = ref(OLD.with_suffix('.pdf'), 'Frozen469-page servicing reader')
    report['pdf'] = ref(PDF, 'Commercial latent-variable working successor')
    audit = json.loads((OUT / 'source-audit.json').read_text())
    audit['added_bibliography'] = ref(BASE / 'refs.bib', 'Commercial latent-model primary documentation and project examples')
    core.write(OUT / 'source-audit.json', audit)
    report['source_audit'] = ref(OUT / 'source-audit.json', 'Whole-book citation identities')
    report['commercial_latent'] = {'first_printed_page': page('exec13:latent-commercial'),
                                   'last_printed_page': page('exec13:latent-commercial-end'),
                                   'vendor_runtime_executed': False, 'coverage_acceptance': False}
    core.write(OUT / 'build-report.json', report)
    print(json.dumps({'pages': report['pages'], 'commercial_latent': report['commercial_latent'],
                      'visual_acceptance': False}))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('command', choices=['prepare', 'build'])
    args = p.parse_args()
    prepare() if args.command == 'prepare' else build()
