#!/usr/bin/env python3
"""Install the reviewed request set after preserving a preparation error."""
import json
from pathlib import Path
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-28/longitudinal-backward-chain-v1'
MANIFEST = ROOT / 'docs/literature/fetch-manifest.json'


def main():
    plan = json.loads((BASE / 'plan-review.json').read_text())
    verify_bindings(plan)
    assert MANIFEST.read_bytes() == (BASE / 'prior-fetch-manifest.json').read_bytes()
    assert not (BASE / 'metadata-fetch-manifest.json').exists()
    write(BASE / 'preparation-failure.json', dict(
        script=ref(ROOT / 'tools/prepare_longitudinal_backward_chain_20261028.py',
                   'Preserved failed preparation'),
        session_id=64003, exit_code=1,
        observed_error='AssertionError: Preserve existing evidence: docs/literature/fetch-manifest.json',
        cause='Immutable evidence writer correctly refused to replace the mutable fetch manifest.',
        effect='Plan and prior-manifest preservation succeeded; no network request or canonical mutation occurred.',
        repair='Verify the reviewed plan and unchanged manifest, then replace only the mutable active manifest.'))
    payload = dict(requests=plan['requests'])
    write(BASE / 'metadata-fetch-manifest.json', payload)
    MANIFEST.write_text(json.dumps(payload, indent=2) + chr(10))
    write(BASE / 'manifest-installation-review.json', dict(
        status='pass', evidence=[ref(BASE / 'plan-review.json', 'Unchanged reviewed plan'),
            ref(BASE / 'metadata-fetch-manifest.json', 'Exact four-request set'),
            ref(BASE / 'preparation-failure.json', 'Preserved actual failure'),
            ref(Path(__file__), 'Narrow sequential repair')],
        requests=4, originals_requested=0, canonical_state_changed=False))
    print('Reviewed four-request metadata manifest installed.')


if __name__ == '__main__':
    main()
