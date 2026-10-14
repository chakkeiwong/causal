#!/usr/bin/env python3
"""Preserve the delivered book and integrate the observed-history derivation."""
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
BASE = DOCS / 'program/execution/2026-10-13/servicing'
OUT = BASE / 'reader'
NAME = 'causal_proposal_servicing_2026-10-13'
OLD = DOCS / 'causal_proposal_java_adapter_2026-10-13.tex'
DRIVER = DOCS / (NAME + '.tex')
PDF = DRIVER.with_suffix('.pdf')
PRIOR_AUDIT = DOCS / 'program/execution/2026-10-13/java-integration/reader/source-audit.json'
ARGUMENT = DOCS / 'program/comprehensive-v14/work/SCI.ARGUMENT.R03S/argument-and-counterexamples.md'
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
                    '--to=latex', '--top-level-division=chapter', '--wrap=auto', str(ARGUMENT),
                    '-o', str(BASE / 'chapter.tex')], check=True, timeout=20)
    tex = (BASE / 'chapter.tex').read_text()
    old = r''' e_t(a\mid h)=\Pr(A_t=a\mid H_t=h,O_{t-1}=1),\qquad
 g_t(h,a)=\Pr(C_t=1\mid H_t=h,A_t=a,O_{t-1}=1).'''
    new = r'''\begin{aligned}
 e_t(a\mid h)&=\Pr(A_t=a\mid H_t=h,O_{t-1}=1),\\
 g_t(h,a)&=\Pr(C_t=1\mid H_t=h,A_t=a,O_{t-1}=1).
\end{aligned}'''
    assert tex.count(old) == 1
    (BASE / 'chapter.tex').write_text(tex.replace(old, new, 1))
    book = OLD.read_text()
    marker = r'\input{program/execution/2026-10-13/research/chapter.tex}'
    assert book.count(marker) == 1
    book = book.replace(marker, marker + '\n' + r'\input{program/execution/2026-10-13/servicing/chapter.tex}', 1)
    marker = "\\addcontentsline{toc}{chapter}{Reader's contract}"
    book = book.replace(marker, marker + r'''

Chapter \ref{exec13:servicing-observed} develops finite-table servicing-policy
inference with estimated action and observation probabilities, independent
evaluation, and explicit selection targets. Exact counterexamples preserve
the hidden-information obstruction; the finite guarantee can be too wide
for a useful choice. No new repeated-sampling qualification is claimed.
''', 1)
    marker = 'program/execution/2026-10-13/java-integration/refs}'
    assert book.count(marker) == 1
    book = book.replace(marker, 'program/execution/2026-10-13/java-integration/refs,program/execution/2026-10-13/servicing/refs}', 1)
    DRIVER.write_text(book)
    entries = []
    for s in audit['sources']:
        entries.append('@misc{' + s['integrated_citation_key'] + ',\n author={{' + shared.escape(s['author']) +
                       '}},\n title={' + shared.escape(s['title']) + '},\n year={' + str(s['year']) +
                       '},\n note={' + shared.escape(s['version_date']) + '}\n}\n')
    (BASE / 'refs.bib').write_text('\n'.join(entries))
    core.write(BASE / 'prepared-inputs.json', {
        'inputs': [ref(p, 'Reviewed input identity') for p in [OLD, PRIOR_AUDIT, Path(__file__),
                    ROOT / 'tools/build_java_reader_20261013.py', ARGUMENT, BASE / 'source-audit.json']],
        'generated': [ref(p, 'Prepared output identity') for p in [DRIVER, BASE / 'chapter.tex', BASE / 'refs.bib']]})
    print(json.dumps({'prepared': str(DRIVER.relative_to(ROOT))}))


def build():
    configure()
    inherited.build()
    report = json.loads((OUT / 'build-report.json').read_text())
    aux = (OUT / (NAME + '.aux')).read_text()

    def page(label):
        return int(re.search(r'\\newlabel\{' + re.escape(label) + r'\}\{\{[^}]*\}\{(\d+)\}', aux).group(1))

    report['builder'] = ref(Path(__file__), 'Servicing integration and preserved bounded compiler')
    report['compile_routine'] = ref(ROOT / 'tools/build_java_reader_20261013.py', 'Unmodified inherited bounded build')
    report['predecessor_pdf'] = ref(OLD.with_suffix('.pdf'), 'Frozen 461-page Java adapter reader')
    report['pdf'] = ref(PDF, 'Integrated observed-history servicing working successor')
    audit = json.loads((OUT / 'source-audit.json').read_text())
    audit['added_bibliography'] = ref(BASE / 'refs.bib', 'Servicing project derivations and preserved study bibliography')
    core.write(OUT / 'source-audit.json', audit)
    report['source_audit'] = ref(OUT / 'source-audit.json', 'Whole-book citation identities including servicing')
    report['servicing_argument'] = {'first_printed_page': page('exec13:servicing-observed'),
                                    'last_printed_page': page('exec13:servicing-observed-end'),
                                    'new_final_study': False, 'original_gap_qualification': False}
    core.write(OUT / 'build-report.json', report)
    print(json.dumps({'pages': report['pages'], 'servicing': report['servicing_argument'],
                      'visual_acceptance': False}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['prepare', 'build'])
    args = parser.parse_args()
    prepare() if args.command == 'prepare' else build()
