#!/usr/bin/env python3
"""Replay original delivery gates with a hash-proven historical AGENTS overlay."""
import contextlib
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

import program_baseline as original

ROOT = original.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-13/prototype-review'


def ref(path):
    return {'path': str(path.relative_to(ROOT)), 'sha256': original.sha(path)}


def main():
    overlay = BASE / 'baseline-overlay.json'
    result = BASE / 'baseline-verification-repaired.json'
    summary = BASE / 'baseline-recovery-review.json'
    if any(p.exists() for p in (overlay, result, summary)):
        raise ValueError('Use a preserving successor; these review outputs already exist')
    record = json.loads((ROOT / original.RECORD).read_text())
    manifests = [json.loads((ROOT / name).read_text()) for name in record['manifests']]
    rows = [r for m in manifests for r in m['artifacts'] if r['path'] == 'AGENTS.md']
    assert rows and len({(r['sha256'], r['bytes']) for r in rows}) == 1
    saved = BASE / 'AGENTS.historical.md'
    assert original.sha(saved) == rows[0]['sha256'] and saved.stat().st_size == rows[0]['bytes']
    record['controls']['AGENTS.md'] = {'archive_path': str(saved.relative_to(ROOT)),
        'sha256': rows[0]['sha256'], 'bytes': rows[0]['bytes']}
    record['successor_note'] = 'Review-only read overlay; active instructions and original baseline/manifest remain unchanged.'
    original.write(overlay, record)
    original.RECORD = str(overlay.relative_to(ROOT))
    original.RECEIPT = str(result.relative_to(ROOT))
    with (BASE / 'baseline-repaired.log').open('w') as log, contextlib.redirect_stdout(log):
        original.verify()
    reviewed = json.loads(result.read_text())
    review = {'status': 'pass', 'replay_executed_at': datetime.now(timezone.utc).isoformat(),
        'finding': 'The only mismatched manifest member was the mutable AGENTS.md control. The reconstructed original has exactly its pre-existing 2496-byte SHA-256. Original unmodified nested delivery gates now pass in the historical read view.',
        'recovery_method': 'Replace only the current execution-entrypoint paragraph with the user-provided historical paragraph; require exact pre-existing SHA-256 before using it. No research evidence was reconstructed.',
        'unique_artifacts': reviewed['unique_artifacts'], 'manifests': reviewed['manifests_verified'],
        'evidence': [ref(ROOT / 'docs/program/master/baseline.json'), ref(saved), ref(overlay), ref(result),
                     ref(BASE / 'baseline-identity-scan.json'), ref(Path(__file__))],
        'limits': ['Historical gates and artifact identities, not a new statistical study or independent scientific review.',
                   'The inherited verifier receipt date describes its historical baseline; replay_executed_at records this execution.',
                   'Current instructions remain in force and were not modified.']}
    original.write(summary, review)
    print(json.dumps({k: review[k] for k in ('status', 'unique_artifacts', 'manifests', 'finding')}))


if __name__ == '__main__':
    main()
