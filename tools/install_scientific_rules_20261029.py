#!/usr/bin/python3
"""Install one dedicated reviewed rule; no arguments or global setting changes."""
from hashlib import sha256
from pathlib import Path
import json
import sys

if len(sys.argv) != 1:
    raise SystemExit('No arguments accepted')
root = Path('/home/ubuntu/workspace/causal')
expected = {
    'tools/public_sources.py': 'b7a5bc21c1dfd991073c4bfdeb40ba52ba3716a25af322c3119e876157f2424a',
    'tools/scientific_sources_20261029.py': '35d458488aa60bde1bb684a06812d9e868742cbf631a7e77c8698f2e63d2492a',
    'security/causal-scientific-20261029.rules': 'ab3812c6d674323b22db03b2a1273092b414b07774b6f01525a3dbb919899fc6',
}
for name, digest in expected.items():
    assert sha256((root / name).read_bytes()).hexdigest() == digest, name
dest = Path('/home/ubuntu/.codex/rules/causal-scientific-20261029.rules')
assert not dest.is_symlink() and dest.parent.resolve() == dest.parent
payload = (root / 'security/causal-scientific-20261029.rules').read_bytes()
if dest.exists():
    assert dest.read_bytes() == payload, 'Unexpected existing rule; refusing replacement'
else:
    with dest.open('xb') as handle:
        handle.write(payload)
receipt = dict(status='installed', destination=str(dest), rule_sha256=sha256(payload).hexdigest(),
               global_rules_modified=False, sandbox_settings_modified=False, live_reload_verified=False)
(root / 'security/scientific-installation-20261029.json').write_text(json.dumps(receipt, indent=2))
print(json.dumps(receipt))
