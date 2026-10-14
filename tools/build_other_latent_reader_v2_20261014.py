#!/usr/bin/env python3
"""Preserving quotation repair for the latent-language working reader."""
import argparse
import json
from pathlib import Path

import build_other_latent_reader_20261014 as builder
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = builder.ROOT
BASE = builder.work.BASE/'v2/publication'
OUT = BASE/'reader'
OLD = builder.OLD
PRIOR = builder.PRIOR
NAME = 'causal_proposal_latent_languages_v2_2026-10-14'
DRIVER = ROOT/'docs'/(NAME+'.tex')
PDF = DRIVER.with_suffix('.pdf')
SYN = builder.work.BASE/'v2/comparison.md'


def configure():
    for name in ['BASE', 'OUT', 'OLD', 'PRIOR', 'NAME', 'DRIVER', 'PDF']:
        setattr(builder, name, globals()[name])
    builder.work.SYN = SYN


def prepare():
    configure()
    verify_bindings(json.loads((SYN.parent/'repair-review.json').read_text()))
    builder.prepare()
    # The predecessor's input location is literal; substitute only the new
    # input path before this successor is built and separately bind the result.
    text = DRIVER.read_text()
    marker = r'\input{program/execution/2026-10-14/other-latent/publication/comparison.tex}'
    assert text.count(marker) == 1
    text = text.replace(marker, r'\input{program/execution/2026-10-14/other-latent/v2/publication/comparison.tex}')
    text = text.replace(',program/execution/2026-10-14/other-latent/publication/refs}',
                        ',program/execution/2026-10-14/other-latent/v2/publication/refs}')
    DRIVER.write_text(text)
    # Preserve the generated preliminary record before binding corrected paths.
    preliminary = BASE/'prepared-inputs.json'
    saved = BASE/'prepared-inputs-before-path-resolution.json'
    preliminary.rename(saved)
    data = json.loads(saved.read_text())
    data['inputs'] += [ref(Path(__file__), 'Successor wrapper'),
                       ref(SYN.parent/'repair-review.json', 'Preserved quotation repair')]
    data['generated'] = [ref(ROOT/r['path'], r['anchor']) for r in data['generated']]
    write(preliminary, data)


def build():
    configure()
    builder.build()
    report = json.loads((OUT/'build-report.json').read_text())
    report['builder'] = ref(Path(__file__), 'Preserving quotation-repair builder')
    builder.engine.core.write(OUT/'build-report.json', report)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['prepare', 'build'])
    args = parser.parse_args()
    prepare() if args.command == 'prepare' else build()
