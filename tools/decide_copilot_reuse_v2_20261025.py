#!/usr/bin/env python3
"""Preserve preparation failure; materialize exact results before their binding."""
import argparse
import json
from pathlib import Path
import decide_copilot_reuse_20261025 as original
from publish_latent_r_review_v2_20261013 import ref, write


def preserving_write(path, value):
    if path.exists():
        assert json.loads(path.read_text()) == value, path
    else:
        write(path, value)


def prepare():
    preserving_write(original.BASE/'exact-results.json', original.exact.calculate())
    original.write = preserving_write
    original.prepare()
    write(original.BASE/'preparation-repair.json',dict(status='pass',
        reason='The cost illustration was hashed before exact-results.json existed; exact values and source claims unchanged.',
        evidence=[ref(original.BASE/'prepare-review.log','Preserved failing attempt'),
                  ref(Path(original.__file__),'Preserved original script'),
                  ref(Path(__file__),'Dependency-order successor'),
                  ref(original.BASE/'review.json','Completed scoped review')],
        earlier_files_preserved=True,native_execution=False))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','receipt']);a=p.parse_args()
    prepare() if a.command=='prepare' else original.receipt()
