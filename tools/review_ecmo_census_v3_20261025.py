#!/usr/bin/env python3
"""Preserve failed review and resume with a JSON-stable exact calculation."""
import json
from pathlib import Path
import review_ecmo_census_20261024 as prior
import ecmo_graph_reference_v2_20261025 as exact
from publish_latent_r_review_v2_20261013 import ref, write

def preserving_write(path, value):
    if path.exists():
        assert json.loads(path.read_text()) == value, path
    else:
        write(path, value)

def main():
    prior.exact = exact
    prior.write = preserving_write
    prior.main()
    write(prior.BASE / 'serialization-repair-v3.json', dict(
        status='pass', repaired_on='2026-10-25',
        cause='Tuple/list mismatch after JSON serialization; numerical values are unchanged.',
        evidence=[
            ref(prior.BASE / 'source-review.log', 'Preserved failing assertion'),
            ref(Path(prior.__file__), 'Original review logic'),
            ref(Path(exact.original.__file__), 'Original exact calculation dependency'),
            ref(Path(exact.__file__), 'JSON-stable exact calculation successor'),
            ref(Path(__file__), 'Preserving continuation'),
            ref(prior.BASE / 'review.json', 'Completed review')],
        original_source_bytes_unchanged=True, native_execution=False))

if __name__ == '__main__':
    main()
