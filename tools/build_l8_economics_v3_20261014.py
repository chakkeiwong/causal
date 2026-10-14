#!/usr/bin/env python3
"""Preserve v2 and attach inherited citations grammatically to their claims."""
import argparse
import json
from pathlib import Path

import build_l8_economics_20261014 as original
import build_l8_economics_v2_20261014 as second
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = original.ROOT
BASE = original.BASE / 'v3'
OUT = BASE / 'reader'
OLD, PRIOR = original.OLD, original.PRIOR
NAME = 'causal_proposal_banking_economics_v3_2026-10-14'
DRIVER = ROOT / 'docs' / (NAME + '.tex')
PDF = DRIVER.with_suffix('.pdf')
CHAPTER = ROOT / 'docs/program/comprehensive-v14/work/TEXT.DRAFT.L8/chapter-v3.tex'
BS, NL = chr(92), chr(10)
REPAIRS = second.REPAIRS


def corrected(path, text):
    text = second.corrected(path, text)
    if path.endswith('/economics-chapter.tex'):
        for phrase, key in [('overlap', 'v12_la_2607_22443'), ('separately', 'v12_la_2607_08093')]:
            before = phrase + '. ' + BS + 'cite{' + key + '}'
            after = phrase + '~' + BS + 'citep{' + key + '}.'
            assert text.count(before) == 1
            text = text.replace(before, after)
    return text


def prepare():
    assert not DRIVER.exists() and not CHAPTER.exists()
    verify_bindings(json.loads((second.OUT / 'build-report.json').read_text()))
    BASE.mkdir(exist_ok=False)
    originals, successors = [], []
    for old, name in REPAIRS.items():
        source, dest = ROOT / old, BASE / name
        dest.write_text(corrected(old, source.read_text()))
        originals.append(ref(source, 'Preserved original source'))
        successors.append(ref(dest, 'Deterministic citation or break-even wording successor'))
    write(BASE / 'source-audit.json', json.loads((original.BASE / 'source-audit.json').read_text()))
    (BASE / 'refs.bib').write_bytes((original.BASE / 'refs.bib').read_bytes())
    CHAPTER.write_text(NL.join(BS + 'input{' + str((BASE / name).relative_to(ROOT / 'docs')) + '}'
                                for name in REPAIRS.values()) + NL)
    book = second.DRIVER.read_text()
    marker = str(second.CHAPTER.relative_to(ROOT / 'docs'))
    assert book.count(marker) == 1
    book = book.replace(marker, str(CHAPTER.relative_to(ROOT / 'docs')))
    oldbib = str((second.BASE / 'refs').relative_to(ROOT / 'docs'))
    assert book.count(oldbib) == 1
    DRIVER.write_text(book.replace(oldbib, str((BASE / 'refs').relative_to(ROOT / 'docs'))))
    write(BASE / 'repair-review.json', {
        'status': 'source_repair_prepared', 'reviewer': original.REVIEWER,
        'prior_candidate': ref(second.OUT / 'build-report.json', 'Preserved unpublished v2 candidate'),
        'prior_repairs': ref(second.BASE / 'repair-review.json', 'Spacing and equality wording repairs'),
        'finding': 'V2 separated author citations from preceding sentences but left them as sentence fragments. Attach both as parenthetical citations before the sentence period.',
        'originals': originals, 'successors': successors,
        'scientific_change': 'No assumptions, equations, numerical results or citation identities changed.',
        'visual_acceptance': False,
    })
    write(BASE / 'prepared-inputs.json', {
        'inputs': [ref(p, 'Preserved input') for p in [OLD, PRIOR, second.DRIVER,
                    second.OUT / 'build-report.json', original.BASE / 'derivation-review.json',
                    original.BASE / 'primary-review.json', Path(__file__).resolve()]] + originals,
        'generated': [ref(p, 'Reviewed successor source') for p in [DRIVER, CHAPTER,
                      BASE / 'source-audit.json', BASE / 'refs.bib', BASE / 'repair-review.json']] + successors,
        'visual_acceptance': False,
    })
    print(json.dumps({'prepared': str(DRIVER.relative_to(ROOT)), 'repaired_sources': 3}))


def build():
    for key, value in {'BASE': BASE, 'OUT': OUT, 'OLD': OLD, 'PRIOR': PRIOR, 'NAME': NAME,
                       'DRIVER': DRIVER, 'PDF': PDF, 'CHAPTER': CHAPTER}.items():
        setattr(original, key, value)
    original.build()
    report = json.loads((OUT / 'build-report.json').read_text())
    report.update(builder=ref(Path(__file__).resolve(), 'Final economics successor builder'),
                  repair_review=ref(BASE / 'repair-review.json', 'Exact preserved corrections'))
    original.engine.core.write(OUT / 'build-report.json', report)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['prepare', 'build'])
    args = parser.parse_args()
    {'prepare': prepare, 'build': build}[args.command]()
