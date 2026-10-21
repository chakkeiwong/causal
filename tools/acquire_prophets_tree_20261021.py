#!/usr/bin/env python3
"""Fixed bounded public discovery reads; metadata only, no downloaded execution."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

BASE = Path(__file__).resolve().parents[1]/'docs/program/execution/2026-10-21/prophets-repository-v1'
REQUESTS = (
    ('commit', 'https://api.github.com/repos/rahulbshrestha/causal-reasoning/git/commits/2f7835a00a62545259ce4a6757d7659fc07358fe'),
    ('tree', 'https://api.github.com/repos/rahulbshrestha/causal-reasoning/git/trees/bb1d51ddc341c511c506b0a217e4a2c787ddb8d6?recursive=1'),
)



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--retry-network', action='store_true')
    args = parser.parse_args()
    attempt = 'tree-network' if args.retry_network else 'tree-sandbox'
    folder = BASE/'acquisition'/attempt
    folder.mkdir(exist_ok=False, parents=True)
    for name, url in REQUESTS:
        if args.retry_network:
            prior = json.loads((BASE/'acquisition/tree-sandbox'/(name+'.receipt.json')).read_text())
            assert prior['status'] == 'failed'
        p = folder/(name+'.json')
        started = datetime.now(timezone.utc).isoformat()
        status, error, count, http = 'failed', None, 0, None
        try:
            request = Request(url, headers={'User-Agent': 'causal-proposal-source-audit/1.0', 'Accept': 'application/json'})
            with urlopen(request, timeout=20) as response, p.open('xb') as output:
                http = response.status
                while True:
                    block = response.read(min(65536, 2*1024*1024-count+1))
                    if not block:
                        break
                    if count+len(block) > 2*1024*1024:
                        raise ValueError('2 MiB streamed byte limit exceeded; partial bytes retained')
                    output.write(block)
                    count += len(block)
            json.loads(p.read_bytes())
            status = 'complete_metadata_only'
        except Exception as exc:
            error = f'{type(exc).__name__}: {exc}'
        receipt = dict(url=url, started_at=started, finished_at=datetime.now(timezone.utc).isoformat(),
                       status=status, error=error, http_status=http, bytes=count,
                       sha256=hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None,
                       cutoff='2026-10-07', limit_bytes=2*1024*1024,
                       scope='Current search/registry response; filter candidate dates separately; not technical or absence evidence')
        (folder/(name+'.receipt.json')).write_text(json.dumps(receipt, indent=2)+'\n')
        print(json.dumps(dict(name=name, status=status, bytes=count, error=error)), flush=True)


if __name__ == '__main__':
    main()
