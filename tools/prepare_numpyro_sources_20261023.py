#!/usr/bin/env python3
"""Select immutable NumPyro primary text; never import downloaded code."""
import hashlib
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-23/numpyro-reuse-v1'
RAW = ROOT / 'docs/literature/raw'
FILES = [
    'LICENSE.md', 'pyproject.toml', 'numpyro/version.py',
    'numpyro/primitives.py', 'numpyro/handlers.py', 'numpyro/infer/util.py',
    'numpyro/infer/mcmc.py', 'numpyro/infer/hmc.py', 'numpyro/infer/hmc_gibbs.py',
    'numpyro/infer/initialization.py', 'numpyro/util.py', 'numpyro/diagnostics.py',
    'numpyro/contrib/funsor/infer_util.py', 'test/test_handlers.py',
    'test/infer/test_mcmc.py', 'test/infer/test_infer_util.py',
    'test/contrib/test_infer_discrete.py',
]


def main():
    commit = json.loads((RAW / 'exec23_numpyro_cutoff.json').read_text())[0]
    tree = json.loads((RAW / 'exec23_numpyro_tree.json').read_text())
    assert commit['sha'] == '033f7e2e57bd0396fba8493ae246debe52f2c973'
    assert tree['sha'] == commit['commit']['tree']['sha'] and not tree['truncated']
    date = commit['commit']['committer']['date']
    assert datetime.fromisoformat(date.replace('Z', '+00:00')).astimezone(ZoneInfo('Asia/Shanghai')).date().isoformat() <= '2026-10-07'
    entries = {x['path']: x for x in tree['tree']}
    selected, requests = [], []
    for i, path in enumerate(FILES):
        item = entries[path]
        assert item['type'] == 'blob'
        key = f'exec23_numpyro_{i:02d}'
        selected.append(dict(id=key, path=path, blob=item['sha'], size=item['size']))
        requests.append(dict(id=key, url=f'https://raw.githubusercontent.com/pyro-ppl/numpyro/{commit["sha"]}/{path}', extension='txt'))
    selection = dict(commit=commit['sha'], tree=tree['sha'], date=date, selected=selected)
    for name, data in [('source-selection.json', selection), ('source-fetch-manifest.json', dict(requests=requests))]:
        target = BASE / name
        assert not target.exists()
        target.write_text(json.dumps(data, indent=2) + '\n')
    (ROOT / 'docs/literature/fetch-manifest.json').write_bytes((BASE / 'source-fetch-manifest.json').read_bytes())
    print(json.dumps(dict(selected=len(selected), bytes=sum(x['size'] for x in selected), commit=commit['sha'])))


if __name__ == '__main__':
    main()
