#!/usr/bin/python3
"""Install one hash-bound dedicated rule file. No arguments or configuration changes."""
import hashlib, json, os, sys, tempfile
from pathlib import Path
ROOT = Path('/home/ubuntu/workspace/causal')
DEST = Path('/home/ubuntu/.codex/rules/causal-research.rules')
EXPECTED_RULES = 'ca550ab3640f6558f11185aea0ac242b87c7aef789aa6f3409f30bab8f58bbb2'
EXPECTED_COLLECTOR = 'b7a5bc21c1dfd991073c4bfdeb40ba52ba3716a25af322c3119e876157f2424a'
if len(sys.argv) != 1:
    raise SystemExit('This fixed installer accepts no arguments')
payload = (ROOT / 'security/causal-research.rules').read_bytes()
assert hashlib.sha256(payload).hexdigest() == EXPECTED_RULES, 'unreviewed rules'
assert hashlib.sha256((ROOT / 'tools/public_sources.py').read_bytes()).hexdigest() == EXPECTED_COLLECTOR, 'unreviewed collector'
assert all(c['pass'] for c in json.loads((ROOT / 'security/rule-check.json').read_text())), 'rule checks failed'
assert not DEST.is_symlink() and DEST.parent.resolve() == DEST.parent, 'symlink rules path'
if DEST.exists() and DEST.read_bytes() != payload:
    raise SystemExit('Unexpected existing dedicated rules; refusing replacement')
if not DEST.exists():
    with tempfile.NamedTemporaryFile(dir=DEST.parent,prefix='.causal-rules-',delete=False) as handle:
        handle.write(payload); handle.flush(); os.fsync(handle.fileno()); temp=Path(handle.name)
    os.replace(temp,DEST)
assert DEST.read_bytes() == payload
receipt={'status':'installed','destination':str(DEST),'sha256':EXPECTED_RULES,'collector_sha256':EXPECTED_COLLECTOR,'default_rules_modified':False,'sandbox_configuration_modified':False,'host_live_reload_verified':False}
(ROOT / 'security/installation-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
