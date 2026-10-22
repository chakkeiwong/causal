#!/usr/bin/env python3
"""Carry the exact v2 traceability failure into its explicit v3 review inputs."""
import json
from pathlib import Path
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT / 'docs/program/execution/2026-10-23/semantics-reader-v2/traceability-failure.json'
BASE = ROOT / 'docs/program/execution/2026-10-23/semantics-reader-v3'


def main():
    new = BASE / 'traceability-failure.json'
    assert OLD.is_file() and not new.exists()
    record = json.loads(OLD.read_text())
    verify_bindings(record)
    new.write_bytes(OLD.read_bytes())
    write(BASE / 'failure-carryforward.json', dict(status='pass',
        predecessor=ref(OLD, 'Exact v2 failed traceability record'),
        carried_record=ref(new, 'Byte-identical failure record for v3 input manifest'),
        byte_identical=OLD.read_bytes() == new.read_bytes(),
        reason='The immutable v3 generator binds a same-directory failure receipt; this copy preserves the earlier record without changing it.'))
    print(json.dumps(dict(path=str(new.relative_to(ROOT)), byte_identical=True)))


if __name__ == '__main__':
    main()
