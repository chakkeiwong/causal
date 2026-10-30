#!/usr/bin/python3
"""Install only the narrow public-source command into its own rule file."""
from pathlib import Path
from hashlib import sha256
import json
import sys

if len(sys.argv)!=1:raise SystemExit('No arguments accepted')
root=Path('/home/ubuntu/workspace/causal')
expected=json.loads((root/'security/frontier-rule-review-20261029.json').read_text())['sha256']
for name,digest in expected.items():
    assert sha256((root/name).read_bytes()).hexdigest()==digest,name
dest=Path('/home/ubuntu/.codex/rules/causal-frontier-20261029.rules')
assert not dest.is_symlink() and dest.parent.resolve()==dest.parent
payload=(root/'security/causal-frontier-20261029.rules').read_bytes()
if dest.exists():assert dest.read_bytes()==payload,'Unexpected rule contents'
else:
    with dest.open('xb') as handle:handle.write(payload)
receipt=dict(status='installed',destination=str(dest),rule_sha256=sha256(payload).hexdigest(),
             global_rules_modified=False,sandbox_settings_modified=False,live_reload_verified=False)
(root/'security/frontier-installation-20261029.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt))
