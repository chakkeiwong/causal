#!/usr/bin/env python3
"""Seven fixed official HTTPS reads; bounded bytes/time, inert originals only."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'docs/program/execution/2026-10-20/mediation-commercial-v1'
REQUESTS = (
    ('stata_post', 'https://www.stata.com/manuals/causalmediatepostestimation.pdf', 'pdf'),
    ('stata_multiple', 'https://www.stata.com/manuals/causalmediatemultiple.pdf', 'pdf'),
    ('sas_causalmed', 'https://support.sas.com/documentation/onlinedoc/stat/151/causalmed.pdf', 'pdf'),
    ('mplus_ch17', 'https://www.statmodel.com/download/usersguide/Chapter17.pdf', 'pdf'),
    ('process_faq', 'https://www.processmacro.org/faq.html', 'html'),
    ('ibm_amos29', 'https://public.dhe.ibm.com/software/analytics/spss/documentation/amos/29.0/en/Manuals/IBM_SPSS_Amos_User_Guide.pdf', 'pdf'),
    ('stata_intro', 'https://www.stata.com/manuals/causalmediateintro.pdf', 'pdf'),
)


def acquire(item, attempt):
    name, url, extension = item
    folder = BASE/'acquisition'/attempt
    folder.mkdir(exist_ok=True, parents=True)
    receipt = folder/(name+'.receipt.json')
    if receipt.exists():
        old = json.loads(receipt.read_text())
        if old['returncode'] == 0:
            assert hashlib.sha256((folder/(name+'.'+extension)).read_bytes()).hexdigest() == old['sha256']
        return dict(id=name, status='preserved_existing_attempt', returncode=old['returncode'])
    target, headers, log = [folder/(name+s) for s in ['.'+extension, '.headers', '.log']]
    assert not any(p.exists() for p in [target, headers, log])
    started = datetime.now(timezone.utc).isoformat()
    command = ['curl', '--http1.1', '-fL', '--proto', '=https', '--proto-redir', '=https',
        '--max-time', '20', '--max-filesize', '16777216', '--silent', '--show-error',
        '-D', str(headers), '-o', str(target), '-w', '%{http_code} %{url_effective} %{size_download}\n', url]
    with log.open('x') as stream:
        try:
            code = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT, timeout=25).returncode
        except subprocess.TimeoutExpired:
            code = 124
    valid_pdf = extension != 'pdf' or target.exists() and target.read_bytes().startswith(b'%PDF-')
    record = dict(id=name, url=url, started_at=started,
        finished_at=datetime.now(timezone.utc).isoformat(), returncode=code,
        observation=log.read_text(), format_valid=valid_pdf,
        local_copy=str(target.relative_to(ROOT)) if target.exists() else None,
        sha256=hashlib.sha256(target.read_bytes()).hexdigest() if target.exists() else None,
        bytes=target.stat().st_size if target.exists() else 0,
        headers=str(headers.relative_to(ROOT)), log=str(log.relative_to(ROOT)), cutoff='2026-10-07',
        historical_byte_identity='Later acquisition does not authenticate exact cutoff-era edition bytes.',
        transport='Fixed public HTTPS GETs; no local data uploaded, credentials, settings change or downloaded code execution.')
    with receipt.open('x') as stream:
        json.dump(record, stream, indent=2); stream.write('\n')
    return dict(id=name, returncode=code, bytes=record['bytes'], format_valid=valid_pdf)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--retry-network', action='store_true')
    args = parser.parse_args()
    assert (BASE/'plan.md').exists()
    attempt = 'network' if args.retry_network else 'sandbox'
    if args.retry_network:
        for name, _, _ in REQUESTS:
            prior = json.loads((BASE/'acquisition/sandbox'/(name+'.receipt.json')).read_text())
            assert prior['returncode'] in [5, 6, 7], 'Only retry preserved connection/DNS failures'
    with ThreadPoolExecutor(max_workers=3) as pool:
        for result in pool.map(lambda row: acquire(row, attempt), REQUESTS):
            print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
