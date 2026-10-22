#!/usr/bin/env python3
"""Carry the exact v2 line-break repair into the v3 builder's bound inputs."""
from pathlib import Path
from publish_latent_r_review_v2_20261013 import ref, write

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT / 'docs/program/execution/2026-10-23/semantics-reader-v2/layout-correction.json'
BASE = ROOT / 'docs/program/execution/2026-10-23/semantics-reader-v3'


def main():
    new = BASE / 'layout-correction.json'
    assert OLD.is_file() and not new.exists()
    new.write_bytes(OLD.read_bytes())
    write(BASE / 'layout-carryforward.json', dict(status='pass',
        predecessor=ref(OLD, 'Exact v2 line-break correction'),
        carried_record=ref(new, 'Byte-identical v2 correction for v3 input manifest'),
        byte_identical=OLD.read_bytes() == new.read_bytes()))
    print('Carried the byte-identical layout correction into v3.')


if __name__ == '__main__':
    main()
