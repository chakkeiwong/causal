#!/usr/bin/env python3
"""Two fixed public publisher originals; streamed byte limits; no downloaded code execution."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

BASE = Path(__file__).resolve().parents[1]/'docs/program/execution/2026-10-21/census-prophets-v1'
REQUESTS = (('original', 'https://aclanthology.org/2025.nlp4dh-1.29.pdf', 'pdf'), ('identity', 'https://aclanthology.org/2025.nlp4dh-1.29/', 'html'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--retry-network', action='store_true')
    args = parser.parse_args()
    attempt = 'network' if args.retry_network else 'sandbox'
    folder = BASE/'acquisition'/attempt
    folder.mkdir(exist_ok=False, parents=True)
    for name, url, extension in REQUESTS:
        if args.retry_network:
            prior = json.loads((BASE/'acquisition/sandbox'/(name+'.receipt.json')).read_text())
            assert prior['status'] == 'failed'
        p = folder/(name+'.'+extension)
        started = datetime.now(timezone.utc).isoformat()
        status, error, count, http = 'failed', None, 0, None
        try:
            request = Request(url, headers={'User-Agent': 'causal-proposal-source-audit/1.0', 'Accept': '*/*'})
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
            assert extension != 'pdf' or p.read_bytes().startswith(b'%PDF-'), 'Not a PDF'
            status = 'complete_public_original'
        except Exception as exc:
            error = f'{type(exc).__name__}: {exc}'
        receipt = dict(url=url, started_at=started, finished_at=datetime.now(timezone.utc).isoformat(),
                       status=status, error=error, http_status=http, bytes=count,
                       sha256=hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None,
                       cutoff='2026-10-07', limit_bytes=16*1024*1024,
                       scope='Later publisher acquisition; historical edition identity requires inspection; no downloaded code execution')
        (folder/(name+'.receipt.json')).write_text(json.dumps(receipt, indent=2)+'\n')
        print(json.dumps(dict(name=name, status=status, bytes=count, error=error)), flush=True)


if __name__ == '__main__':
    main()
