#!/usr/bin/env python3
"""Three fixed pinned public source archives; streamed byte limits; no downloaded code execution."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

BASE = Path(__file__).resolve().parents[1]/'docs/program/execution/2026-10-21/gsynth-reuse-v1'
REQUESTS = (('gsynth_upstream', 'https://codeload.github.com/xuyiqing/gsynth/tar.gz/f288aa23697fa77791157a254c73eef6a351fbbf'), ('gsynth_cran', 'https://codeload.github.com/cran/gsynth/tar.gz/96a9021ff29a96942b19c947c7c6943890e78864'), ('fect_cran', 'https://codeload.github.com/cran/fect/tar.gz/bbc71a2de6d26656af972114455e40224b7ec032'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--retry-network', action='store_true')
    args = parser.parse_args()
    attempt = 'sources-network' if args.retry_network else 'sources-sandbox'
    folder = BASE/'acquisition'/attempt
    folder.mkdir(exist_ok=False, parents=True)
    for name, url in REQUESTS:
        if args.retry_network:
            prior = json.loads((BASE/'acquisition/sources-sandbox'/(name+'.receipt.json')).read_text())
            assert prior['status'] == 'failed'
        p = folder/(name+'.tgz')
        started = datetime.now(timezone.utc).isoformat()
        status, error, count, http = 'failed', None, 0, None
        try:
            request = Request(url, headers={'User-Agent': 'causal-proposal-source-audit/1.0', 'Accept': 'application/json'})
            with urlopen(request, timeout=20) as response, p.open('xb') as output:
                http = response.status
                while True:
                    block = response.read(min(65536, 16*1024*1024-count+1))
                    if not block:
                        break
                    if count+len(block) > 16*1024*1024:
                        raise ValueError('16 MiB streamed byte limit exceeded; partial bytes retained')
                    output.write(block)
                    count += len(block)
            assert p.read_bytes()[:2] == bytes([31,139]), 'Not a gzip archive'
            status = 'complete_pinned_archive'
        except Exception as exc:
            error = f'{type(exc).__name__}: {exc}'
        receipt = dict(url=url, started_at=started, finished_at=datetime.now(timezone.utc).isoformat(),
                       status=status, error=error, http_status=http, bytes=count,
                       sha256=hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None,
                       cutoff='2026-10-07', limit_bytes=16*1024*1024,
                       scope='Selected pinned source archive; no downloaded code execution; technical inspection follows')
        (folder/(name+'.receipt.json')).write_text(json.dumps(receipt, indent=2)+'\n')
        print(json.dumps(dict(name=name, status=status, bytes=count, error=error)), flush=True)


if __name__ == '__main__':
    main()
