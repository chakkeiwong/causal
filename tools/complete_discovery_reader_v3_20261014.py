#!/usr/bin/env python3
"""Preserve the failed attempt and repair one missing LaTeX brace escape."""
import argparse
import json
from pathlib import Path
import complete_discovery_reader_v2_20261014 as prior

ROOT = prior.ROOT
BASE = prior.PARENT / 'v3'
OUT = BASE / 'reader'
NAME = 'causal_proposal_discovery_review_v3_2026-10-14'
DRIVER = ROOT / 'docs' / (NAME + '.tex')
PDF = DRIVER.with_suffix('.pdf')
ref, write = prior.ref, prior.write


def prepare():
    assert not BASE.exists() and not DRIVER.exists()
    BASE.mkdir()
    source = prior.PARENT / 'discovery-screening-value.tex'
    old = source.read_text()
    new = old.replace(r'$E{Y\mid', r'$E\{Y\mid')
    assert new != old and old.count(r'$E{Y\mid') == 1
    repaired = BASE / 'discovery-screening-value.tex'
    repaired.write_text(new)
    old_prefix = 'program/execution/2026-10-14/l4-completion/v2/'
    new_prefix = 'program/execution/2026-10-14/l4-completion/v3/'
    DRIVER.write_text(prior.DRIVER.read_text().replace(old_prefix, new_prefix))
    chapter = (prior.BASE / 'chapter.tex').read_text().replace(
        'program/execution/2026-10-14/l4-completion/discovery-screening-value.tex',
        new_prefix + 'discovery-screening-value.tex')
    (BASE / 'chapter.tex').write_text(chapter)
    for name in ['refs.bib', 'exact-results.json']:
        (BASE / name).write_bytes((prior.BASE / name).read_bytes())
    audit = json.loads((prior.BASE / 'source-audit.json').read_text())
    item = audit['sources'][0]
    item['local_copy'] = ref(BASE / 'exact-results.json', item['local_copy']['anchor'])
    item['records'][0]['local_copy'] = ref(repaired, 'Complete derivations; one repaired LaTeX brace escape')
    write(BASE / 'source-audit.json', audit)
    write(BASE / 'build-repair.json', {
        'failure': 'First LaTeX pass rejected an unescaped opening brace in the intervention-mean expression.',
        'resolution': 'Correct one opening brace escape in a preserving source copy; mathematics unchanged.',
        'evidence': [ref(prior.OUT / 'pass-1.log', 'Observed compiler failure at source line 32'),
                     ref(source, 'Failed original preserved'), ref(repaired, 'Single escape repair')],
        'next_action': 'Compile the preserving successor and review actual page depth and source custody.'})
    write(BASE / 'prepared-inputs.json', {
        'inputs': [ref(prior.DRIVER, 'Uncompiled predecessor driver'),
                   ref(prior.PRIOR_AUDIT, 'Preserved 505-record successful reader audit'),
                   ref(prior.BASE / 'prepared-inputs.json', 'Preserved failed input contract'),
                   ref(Path(__file__), 'Single-escape repair and preserving build'),
                   ref(Path(prior.__file__), 'Unmodified build routine')],
        'generated': [ref(p, 'Prepared corrected successor input') for p in [DRIVER, BASE / 'chapter.tex', repaired,
                    BASE / 'refs.bib', BASE / 'exact-results.json', BASE / 'source-audit.json', BASE / 'build-repair.json']]})
    print(json.dumps({'prepared': str(DRIVER.relative_to(ROOT)), 'one_escape_corrected': True}))


def build():
    for key in ['BASE', 'OUT', 'NAME', 'DRIVER', 'PDF']:
        setattr(prior, key, globals()[key])
    prior.build()


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('action', choices=['prepare', 'build'])
    prepare() if p.parse_args().action == 'prepare' else build()
