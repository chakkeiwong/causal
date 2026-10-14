#!/usr/bin/env python3
"""Build the copy-edited L2 reader successor without overwriting v1."""
import build_l2_reader_20261013 as base

base.BASE = base.DOCS / 'program/execution/2026-10-13/l2/final-v2'
base.OUT = base.BASE / 'reader'
base.NAME = 'causal_proposal_l2_v2_2026-10-13'
base.DRIVER = base.DOCS / (base.NAME + '.tex')
base.PDF = base.DRIVER.with_suffix('.pdf')
base.CHAPTER = base.DOCS / 'program/comprehensive-v14/work/TEXT.DRAFT.L2/chapter-layout-v3.tex'

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=('prepare', 'build'))
    args = parser.parse_args()
    base.prepare() if args.command == 'prepare' else base.build()
