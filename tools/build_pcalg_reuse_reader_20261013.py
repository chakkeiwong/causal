#!/usr/bin/env python3
"""Integrate a reviewed pcalg reuse section without changing earlier deliveries."""
import argparse
import json
from pathlib import Path
import re
import subprocess

import build_java_reader_20261013 as inherited
import build_integrated_monograph_v12 as shared
import master_control as core

ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-13/pcalg-reuse'
OUT = BASE / 'reader'
NAME = 'causal_proposal_pcalg_2026-10-13'
OLD = ROOT / 'docs/causal_proposal_commercial_temporal_2026-10-13.tex'
DRIVER = ROOT / 'docs' / (NAME + '.tex')
PDF = DRIVER.with_suffix('.pdf')
PRIOR_AUDIT = ROOT / 'docs/program/execution/2026-10-13/commercial-temporal/reader/source-audit.json'
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
    marker = r'\input{program/execution/2026-10-13/tetrad-reuse/decision.tex}'
    assert book.count(marker) == 1
    book = book.replace(marker, marker + '\n' + r'\input{program/execution/2026-10-13/pcalg-reuse/decision.tex}', 1)
    marker = 'program/execution/2026-10-13/commercial-temporal/refs}'
    assert book.count(marker) == 1
    book = book.replace(marker, 'program/execution/2026-10-13/commercial-temporal/refs,program/execution/2026-10-13/pcalg-reuse/refs}', 1)
    DRIVER.write_text(book)
    bibliography = []
    for source in audit['sources']:
        bibliography.append('@misc{' + source['integrated_citation_key'] + ',\n author={{' + shared.escape(source['author']) +
            '}},\n title={' + shared.escape(source['title']) + '},\n year={' + str(source['year']) +
            '},\n note={' + shared.escape(source['version_date']) + '}\n}\n')
    (BASE / 'refs.bib').write_text('\n'.join(bibliography))
    core.write(BASE / 'prepared-inputs.json', {'inputs': [ref(p, 'Reviewed source input') for p in
        [OLD, PRIOR_AUDIT, BASE/'source-audit.json', BASE/'decision.md', BASE/'author-review.json',
         Path(__file__), ROOT/'tools/build_java_reader_20261013.py']],
        'generated': [ref(p, 'Prepared source') for p in [DRIVER, BASE/'decision.tex', BASE/'refs.bib']]})
    print(json.dumps({'prepared': str(DRIVER.relative_to(ROOT))}))


def build():
    configure()
    OUT.mkdir(exist_ok=True)
    for suffix in ['.aux', '.bbl', '.toc', '.out']:
        path = OUT / (NAME + suffix)
        if not path.exists():
            path.write_text('')
    inherited.build()
    report = json.loads((OUT/'build-report.json').read_text())
    audit = json.loads((OUT/'source-audit.json').read_text())
    audit['added_bibliography'] = ref(BASE/'refs.bib', 'Pinned pcalg primary sources and independent project references')
    core.write(OUT/'source-audit.json', audit)
    aux = (OUT / (NAME + '.aux')).read_text()
    def page(label):
        return int(re.search(r'\\newlabel\{' + re.escape(label) + r'\}\{\{[^}]*\}\{(\d+)\}', aux).group(1))
    report.update(builder=ref(Path(__file__), 'Preserving pcalg reuse integration'),
        compile_routine=ref(ROOT/'tools/build_java_reader_20261013.py', 'Unmodified bounded compiler'),
        predecessor_pdf=ref(OLD.with_suffix('.pdf'), 'Frozen523-page Q3-reviewed reader'),
        pdf=ref(PDF, 'Working reader with reviewed pcalg proposal choice'),
        source_audit=ref(OUT/'source-audit.json', 'Whole-reader citation identities'),
        pcalg_reuse={'first_printed_page': page('exec13:pcalg-reuse'),
                     'last_printed_page': page('exec13:pcalg-reuse-end'),
                     'runtime_executed': False, 'integration_allowed': True,
                     'capability_scope': 'Selected local implementation path; no runtime or distribution qualification'})
    core.write(OUT/'build-report.json', report)
    print(json.dumps({'pages': report['pages'], 'citations': report['cited_records'], 'pcalg_reuse': report['pcalg_reuse']}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['prepare', 'build'])
    args = parser.parse_args()
    prepare() if args.command == 'prepare' else build()
