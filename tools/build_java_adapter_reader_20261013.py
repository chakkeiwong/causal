#!/usr/bin/env python3
"""Add Java adapter design using the preserved bounded compilation routine."""
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
BASE = DOCS / 'program/execution/2026-10-13/java-integration'
OUT = BASE / 'reader'
NAME = 'causal_proposal_java_adapter_2026-10-13'
OLD = DOCS / 'causal_proposal_java_2026-10-13.tex'
DRIVER = DOCS / (NAME + '.tex')
PDF = DRIVER.with_suffix('.pdf')
PRIOR_AUDIT = DOCS / 'program/execution/2026-10-13/java-discovery/reader/source-audit.json'
ref = shared.ref


def configure():
    # Change only this process's module configuration, never the frozen source.
    for key in ['BASE', 'OUT', 'NAME', 'OLD', 'DRIVER', 'PDF', 'PRIOR_AUDIT']:
        setattr(inherited, key, globals()[key])


def prepare():
    configure()
    inherited.guard()
    audit = json.loads((BASE / 'source-audit.json').read_text())
    shared.verify_refs(audit)
    subprocess.run(['pandoc', '--from=markdown+raw_tex+tex_math_single_backslash',
                    '--to=latex', '--wrap=auto', str(BASE / 'adapter.md'), str(BASE / 'encoding.md'),
                    '-o', str(BASE / 'adapter.tex')], check=True, timeout=20)
    book = OLD.read_text()
    marker = r'\input{program/execution/2026-10-13/interchange/composition.tex}'
    assert book.count(marker) == 1
    book = book.replace(marker, marker + '\n' + r'\input{program/execution/2026-10-13/java-integration/adapter.tex}', 1)
    marker = 'program/execution/2026-10-13/java-discovery/refs}'
    assert book.count(marker) == 1
    book = book.replace(marker, 'program/execution/2026-10-13/java-discovery/refs,program/execution/2026-10-13/java-integration/refs}', 1)
    DRIVER.write_text(book)
    entries = []
    for s in audit['sources']:
        entries.append('@misc{' + s['integrated_citation_key'] + ',\n author={{' + shared.escape(s['author']) +
                       '}},\n title={' + shared.escape(s['title']) + '},\n year={' + str(s['year']) +
                       '},\n note={' + shared.escape(s['version_date']) + '}\n}\n')
    (BASE / 'refs.bib').write_text('\n'.join(entries))
    core.write(BASE / 'prepared-inputs.json', {
        'inputs': [ref(p, 'Prepared source identity') for p in [OLD, PRIOR_AUDIT, Path(__file__),
                    ROOT / 'tools/build_java_reader_20261013.py', BASE / 'source-audit.json', BASE / 'adapter.md',
                    BASE / 'encoding.md', BASE / 'wire-profile.json']],
        'generated': [ref(p, 'Prepared output identity') for p in [DRIVER, BASE / 'adapter.tex', BASE / 'refs.bib']]})
    print(json.dumps({'prepared': str(DRIVER.relative_to(ROOT))}))


def build():
    configure()
    inherited.build()
    report = json.loads((OUT / 'build-report.json').read_text())
    aux = (OUT / (NAME + '.aux')).read_text()

    def page(label):
        return int(re.search(r'\\newlabel\{' + re.escape(label) + r'\}\{\{[^}]*\}\{(\d+)\}', aux).group(1))

    report['builder'] = ref(Path(__file__), 'Preserving adapter integration and reused bounded compiler')
    report['compile_routine'] = ref(ROOT / 'tools/build_java_reader_20261013.py', 'Unmodified inherited bounded build function')
    report['predecessor_pdf'] = ref(OLD.with_suffix('.pdf'), 'Frozen457-page Java comparison reader')
    report['pdf'] = ref(PDF, 'Integrated Java adapter proposal successor')
    report['java_adapter'] = {'first_printed_page': page('exec13:java-adapter'),
                              'last_printed_page': page('exec13:java-wire-end'),
                              'implementation_accepted': False, 'chapter_depth_acceptance': False}
    core.write(OUT / 'build-report.json', report)
    print(json.dumps({'pages': report['pages'], 'adapter': report['java_adapter'], 'visual_acceptance': False}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['prepare', 'build'])
    args = parser.parse_args()
    prepare() if args.command == 'prepare' else build()
