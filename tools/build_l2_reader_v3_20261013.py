#!/usr/bin/env python3
"""Build the actual copy-edited L2 TeX input as a preserving reader."""
import argparse
import json
import re
from pathlib import Path

import build_l2_reader_20261013 as base
import build_integrated_monograph_v12 as shared
import master_control as core

base.BASE = base.DOCS / 'program/execution/2026-10-13/l2/final-v3'
base.OUT = base.BASE / 'reader'
base.NAME = 'causal_proposal_l2_v3_2026-10-13'
base.DRIVER = base.DOCS / (base.NAME + '.tex')
base.PDF = base.DRIVER.with_suffix('.pdf')
base.CHAPTER = base.DOCS / 'program/comprehensive-v14/work/TEXT.DRAFT.L2/chapter-layout-v3.tex'


def prepare():
    assert not base.DRIVER.exists() and not base.BASE.exists()
    text = base.OLD.read_text()
    marker = r'\input{program/execution/2026-10-13/formulation.tex}'
    insertion = r'\input{program/comprehensive-v14/work/TEXT.DRAFT.L2/chapter-layout-v3.tex}'
    assert text.count(marker) == 1 and insertion not in text
    base.BASE.mkdir(parents=True)
    base.DRIVER.write_text(text.replace(marker, marker + '\n' + insertion, 1))
    (base.BASE / 'refs.bib').write_text('% Inherited, source-audited citations only.\n')
    prior = json.loads(base.PRIOR_AUDIT.read_text())
    keys = {k.strip() for group in re.findall(shared.CITE, base.CHAPTER.read_text())
            for k in group.split(',')}
    known = {s['integrated_citation_key'] for s in prior['sources']}
    assert keys <= known, repr(keys-known)
    core.write(base.BASE / 'source-audit.json', {
        'sources': [], 'cutoff': '2026-10-07',
        'inherited_citation_keys': sorted(keys),
        'inherited_source_audit': shared.ref(base.PRIOR_AUDIT, 'Audited predecessor bibliography'),
        'chapter': shared.ref(base.CHAPTER, 'Versioned layout-corrected L2 chapter')})
    inputs = [base.OLD, base.CHAPTER, base.PRIOR_AUDIT,
              base.DOCS / 'program/comprehensive-v14/work/TEXT.DRAFT.L2/chapter.tex',
              base.DOCS / 'program/execution/2026-10-13/l2/source-audit-v2.json',
              base.DOCS / 'program/execution/2026-10-13/l2/review-v2.json',
              Path(__file__), Path(base.__file__)]
    core.write(base.BASE / 'prepared-inputs.json', {
        'inputs': [shared.ref(p, 'Preserved or reviewed input') for p in inputs],
        'generated': [shared.ref(p, 'Preserving reader input') for p in
                      (base.DRIVER, base.BASE / 'refs.bib', base.BASE / 'source-audit.json')]})
    print(json.dumps({'prepared': str(base.DRIVER.relative_to(base.ROOT)),
                      'inherited_citations': len(keys)}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=('prepare', 'build'))
    args = parser.parse_args()
    prepare() if args.command == 'prepare' else base.build()
