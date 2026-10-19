#!/usr/bin/env python3
"""Five fixed official HTTPS reads, each bounded and preserved independently."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-19/dynamic-commercial-v1'
REQUESTS = (
    ('stata_ab', 'https://www.stata.com/manuals/xtxtabond.pdf', 'pdf'),
    ('stata_system', 'https://www.stata.com/manuals/xtxtdpdsys.pdf', 'pdf'),
    ('stata_lp', 'https://www.stata.com/manuals/tslpirf.pdf', 'pdf'),
    ('eviews_panel', 'https://help.eviews.com/content/panel-Estimating_a_Panel_Equation.html', 'html'),
    ('matlab_irf', 'https://www.mathworks.com/help/econ/varm.irf.html', 'html'),
)


def main():
    assert (BASE / 'plan-review.json').exists()
    out = BASE / 'acquisition'
    out.mkdir(exist_ok=True)
    for name, url, extension in REQUESTS:
        receipt = out / (name + '.receipt.json')
        if receipt.exists():
            prior = json.loads(receipt.read_text())
            if prior['returncode'] == 0:
                assert hashlib.sha256((out / (name + '.' + extension)).read_bytes()).hexdigest() == prior['sha256']
            print(json.dumps(dict(id=name, status='preserved_existing_attempt')), flush=True)
            continue
        target, headers, log = [out / (name + suffix) for suffix in ['.'+extension, '.headers', '.log']]
        assert not any(p.exists() for p in [target, headers, log]), name
        started = datetime.now(timezone.utc).isoformat()
        command = ['curl', '-fL', '--proto', '=https', '--proto-redir', '=https',
            '--max-time', '20', '--max-filesize', '12582912', '--silent', '--show-error',
            '-D', str(headers), '-o', str(target), '-w', '%{http_code} %{url_effective} %{size_download}\n', url]
        with log.open('x') as stream:
            try:
                result = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT, timeout=25)
                code = result.returncode
            except subprocess.TimeoutExpired:
                code = 124
        record = dict(id=name, url=url, started_at=started, finished_at=datetime.now(timezone.utc).isoformat(),
            returncode=code, observation=log.read_text(), local_copy=str(target.relative_to(ROOT)) if target.exists() else None,
            sha256=hashlib.sha256(target.read_bytes()).hexdigest() if target.exists() else None,
            bytes=target.stat().st_size if target.exists() else 0, headers=str(headers.relative_to(ROOT)), log=str(log.relative_to(ROOT)),
            cutoff='2026-10-07', historical_byte_identity='Post-cutoff acquisition; exact historical edition bytes require separate evidence.',
            transport='Five fixed public HTTPS GETs only; no upload, credentials, settings change or downloaded code execution.')
        with receipt.open('x') as stream:
            json.dump(record, stream, indent=2); stream.write('\n')
        print(json.dumps(dict(id=name, returncode=code, bytes=record['bytes'])), flush=True)


if __name__ == '__main__':
    main()
