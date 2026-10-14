#!/usr/bin/env python3
"""Preserve the first economics candidate and repair reviewed wording/spacing."""
import argparse
import json
from pathlib import Path

import build_l8_economics_20261014 as previous
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = previous.ROOT
BASE = previous.BASE / 'v2'
OUT = BASE / 'reader'
OLD, PRIOR = previous.OLD, previous.PRIOR
NAME = 'causal_proposal_banking_economics_v2_2026-10-14'
DRIVER = ROOT / 'docs' / (NAME + '.tex')
PDF = DRIVER.with_suffix('.pdf')
CHAPTER = ROOT / 'docs/program/comprehensive-v14/work/TEXT.DRAFT.L8/chapter-v2.tex'
BS, NL = chr(92), chr(10)
REPAIRS = {
    'docs/program/repair-v12/work/LA07/economics-chapter.tex': 'economics-chapter.tex',
    'docs/program/execution/2026-10-14/native-evaluation-reader/v3/cost-development.tex': 'cost-development.tex',
    'docs/program/execution/2026-10-14/l8-economics/development.tex': 'development.tex',
}


def corrected(path, text):
    if path.endswith('/development.tex'):
        before = 'the pilot beats immediate construction only if'
        assert text.count(before) == 1
        return text.replace(before, 'the pilot is weakly preferred to immediate construction exactly when')
    assert text.count('.' + BS + 'cite') == 2
    return text.replace('.' + BS + 'cite', '. ' + BS + 'cite')


def prepare():
    assert not DRIVER.exists() and not CHAPTER.exists()
    verify_bindings(json.loads((previous.OUT / 'build-report.json').read_text()))
    BASE.mkdir(exist_ok=False)
    originals, successors = [], []
    for old, name in REPAIRS.items():
        source, dest = ROOT / old, BASE / name
        dest.write_text(corrected(old, source.read_text()))
        originals.append(ref(source, 'Preserved original candidate input'))
        successors.append(ref(dest, 'Reviewed deterministic wording or citation-space repair'))
    audit = json.loads((previous.BASE / 'source-audit.json').read_text())
    verify_bindings(audit)
    write(BASE / 'source-audit.json', audit)
    (BASE / 'refs.bib').write_bytes((previous.BASE / 'refs.bib').read_bytes())
    CHAPTER.write_text(NL.join(BS + 'input{' + str((BASE / name).relative_to(ROOT / 'docs')) + '}'
                                for name in REPAIRS.values()) + NL)
    book = previous.DRIVER.read_text()
    marker = str(previous.CHAPTER.relative_to(ROOT / 'docs'))
    assert book.count(marker) == 1
    book = book.replace(marker, str(CHAPTER.relative_to(ROOT / 'docs')))
    oldbib = str((previous.BASE / 'refs').relative_to(ROOT / 'docs'))
    assert book.count(oldbib) == 1
    DRIVER.write_text(book.replace(oldbib, str((BASE / 'refs').relative_to(ROOT / 'docs'))))
    write(BASE / 'repair-review.json', {
        'reviewer': previous.REVIEWER, 'status': 'source_repair_prepared',
        'prior_candidate': ref(previous.OUT / 'build-report.json', 'Unpublished first 780-page candidate'),
        'findings': [
            'Two inherited narrative citations joined the preceding sentence without a space.',
            'Two inherited parenthetical citations also lacked a preceding space.',
            'At discount 15/17 pilot and immediate investment tie; weak preference, not strict improvement, includes equality.'
        ],
        'originals': originals, 'successors': successors,
        'scientific_change': 'No equation, assumption or numerical result changed; equality wording made exact.',
        'visual_acceptance': False,
    })
    write(BASE / 'prepared-inputs.json', {
        'inputs': [ref(p, 'Preserved reviewed input') for p in [OLD, PRIOR, previous.DRIVER,
                    previous.OUT / 'build-report.json', previous.BASE / 'derivation-review.json',
                    previous.BASE / 'primary-review.json', Path(__file__).resolve()]] + originals,
        'generated': [ref(p, 'Preserving successor source') for p in [DRIVER, CHAPTER,
                      BASE / 'source-audit.json', BASE / 'refs.bib', BASE / 'repair-review.json']] + successors,
        'visual_acceptance': False,
    })
    print(json.dumps({'prepared': str(DRIVER.relative_to(ROOT)), 'repaired_sources': 3}))


def build():
    for key, value in {'BASE': BASE, 'OUT': OUT, 'OLD': OLD, 'PRIOR': PRIOR, 'NAME': NAME,
                       'DRIVER': DRIVER, 'PDF': PDF, 'CHAPTER': CHAPTER}.items():
        setattr(previous, key, value)
    previous.build()
    report = json.loads((OUT / 'build-report.json').read_text())
    report.update(builder=ref(Path(__file__).resolve(), 'Preserving economics successor builder'),
                  repair_review=ref(BASE / 'repair-review.json', 'Observed defects and exact repairs'))
    previous.engine.core.write(OUT / 'build-report.json', report)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['prepare', 'build'])
    args = parser.parse_args()
    {'prepare': prepare, 'build': build}[args.command]()
