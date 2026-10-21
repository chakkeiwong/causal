#!/usr/bin/env python3
"""Fixed bounded public discovery reads; metadata only, no downloaded execution."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

BASE = Path(__file__).resolve().parents[1]/'docs/program/execution/2026-10-21/effects-other-v1'
REQUESTS = (
    ('rust_repos', 'https://api.github.com/search/repositories?q=causal+language%3ARust+created%3A%3C%3D2026-10-07&per_page=20'),
    ('rust_effect_repos', 'https://api.github.com/search/repositories?q=%22treatment+effect%22+language%3ARust+created%3A%3C%3D2026-10-07&per_page=20'),
    ('crates_causal', 'https://crates.io/api/v1/crates?q=causal&per_page=20'),
    ('crates_treatment', 'https://crates.io/api/v1/crates?q=treatment&per_page=20'),
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--retry-network', action='store_true')
    args = parser.parse_args()
    attempt = 'discovery-network' if args.retry_network else 'discovery-sandbox'
    folder = BASE/'acquisition'/attempt
    folder.mkdir(exist_ok=False)
    for name, url in REQUESTS:
        if args.retry_network:
            prior = json.loads((BASE/'acquisition/discovery-sandbox'/(name+'.receipt.json')).read_text())
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
