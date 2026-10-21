#!/usr/bin/env python3
"""Two fixed public publisher originals; streamed byte limits; no downloaded code execution."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

BASE = Path(__file__).resolve().parents[1]/'docs/program/execution/2026-10-21/prophets-repository-v1'
REQUESTS = (('file-00', 'https://raw.githubusercontent.com/rahulbshrestha/causal-reasoning/2f7835a00a62545259ce4a6757d7659fc07358fe/LICENSE', 'txt'), ('file-01', 'https://raw.githubusercontent.com/rahulbshrestha/causal-reasoning/2f7835a00a62545259ce4a6757d7659fc07358fe/README.md', 'md'), ('file-02', 'https://raw.githubusercontent.com/rahulbshrestha/causal-reasoning/2f7835a00a62545259ce4a6757d7659fc07358fe/requirements.txt', 'txt'), ('file-03', 'https://raw.githubusercontent.com/rahulbshrestha/causal-reasoning/2f7835a00a62545259ce4a6757d7659fc07358fe/src/model_inference.py', 'py'), ('file-04', 'https://raw.githubusercontent.com/rahulbshrestha/causal-reasoning/2f7835a00a62545259ce4a6757d7659fc07358fe/src/prompts.py', 'py'), ('file-05', 'https://raw.githubusercontent.com/rahulbshrestha/causal-reasoning/2f7835a00a62545259ce4a6757d7659fc07358fe/src/utils.py', 'py'), ('file-06', 'https://raw.githubusercontent.com/rahulbshrestha/causal-reasoning/2f7835a00a62545259ce4a6757d7659fc07358fe/src/tree-of-thoughts.ipynb', 'ipynb'), ('file-07', 'https://raw.githubusercontent.com/rahulbshrestha/causal-reasoning/2f7835a00a62545259ce4a6757d7659fc07358fe/src/program-of-thoughts.ipynb', 'ipynb'), ('file-08', 'https://raw.githubusercontent.com/rahulbshrestha/causal-reasoning/2f7835a00a62545259ce4a6757d7659fc07358fe/src/benchmark-cladder-openai.ipynb', 'ipynb'), ('file-09', 'https://raw.githubusercontent.com/rahulbshrestha/causal-reasoning/2f7835a00a62545259ce4a6757d7659fc07358fe/data/results/cladder-rq3-commonsensical.csv', 'csv'), ('file-10', 'https://raw.githubusercontent.com/rahulbshrestha/causal-reasoning/2f7835a00a62545259ce4a6757d7659fc07358fe/data/results/cladder-rq3-anticommonsensical.csv', 'csv'), ('file-11', 'https://raw.githubusercontent.com/rahulbshrestha/causal-reasoning/2f7835a00a62545259ce4a6757d7659fc07358fe/data/results/cladder-rq3-nonsensical.csv', 'csv'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--retry-network', action='store_true')
    parser.add_argument('--batch', type=int, choices=[0,1,2], required=True)
    args = parser.parse_args()
    attempt = 'files-network' if args.retry_network else 'files-sandbox'
    folder = BASE/'acquisition'/attempt
    folder.mkdir(exist_ok=True, parents=True)
    for name, url, extension in REQUESTS[args.batch*4:(args.batch+1)*4]:
        assert not (folder/(name+'.receipt.json')).exists()
        if args.retry_network:
            prior = json.loads((BASE/'acquisition/files-sandbox'/(name+'.receipt.json')).read_text())
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
                       scope='Pinned raw repository bytes; authenticate against tree Git blob identities before claims; no downloaded execution')
        (folder/(name+'.receipt.json')).write_text(json.dumps(receipt, indent=2)+'\n')
        print(json.dumps(dict(name=name, status=status, bytes=count, error=error)), flush=True)


if __name__ == '__main__':
    main()
