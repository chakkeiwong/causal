#!/usr/bin/env python3
"""Four fixed, bounded official HTTPS GETs; preserve bytes and all failures."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-18/commercial-panels'
REQUESTS = (
    ('stata_did', 'https://www.stata.com/manuals/causaldidregress.pdf', 'pdf'),
    ('stata_hdid', 'https://www.stata.com/manuals/causalhdidregress.pdf', 'pdf'),
    ('eviews_did', 'https://help.eviews.com/content/paneldid-Difference-in-Difference_Estimation.html', 'html'),
    ('eviews_panel_did', 'https://help.eviews.com/content/paneldid-Panel_Difference-in-Difference_Estimation.html', 'html'),
)
DETAILS = (
    ('stata_xthdid', 'https://www.stata.com/manuals/causalxthdidregress.pdf', 'pdf'),
    ('stata_hdid_post', 'https://www.stata.com/manuals/causalhdidregresspostestimation.pdf', 'pdf'),
    ('eviews_topics', 'https://help.eviews.com/help/all-topics.html', 'html'),
)


def get(request):
    name, url, extension = request
    out = BASE / (name + '.' + extension)
    headers = BASE / (name + '.headers')
    log = BASE / (name + '.log')
    assert not out.exists() and not headers.exists() and not log.exists(), name
    command = ['curl', '-fL', '--proto', '=https', '--proto-redir', '=https',
               '--max-time', '25', '--max-filesize', '12582912', '--silent', '--show-error',
               '-D', str(headers), '-o', str(out), '-w',
               '%{http_code} %{url_effective} %{size_download}\n', url]
    started = datetime.now(timezone.utc).isoformat()
    with log.open('w') as handle:
        result = subprocess.run(command, stdout=handle, stderr=subprocess.STDOUT, timeout=30)
    return {'id': name, 'url': url, 'started_at': started,
            'finished_at': datetime.now(timezone.utc).isoformat(),
            'returncode': result.returncode, 'observation': log.read_text().strip(),
            'local_copy': str(out.relative_to(ROOT)) if out.exists() else None,
            'sha256': hashlib.sha256(out.read_bytes()).hexdigest() if out.exists() else None,
            'headers': str(headers.relative_to(ROOT)), 'log': str(log.relative_to(ROOT)),
            'bytes': out.stat().st_size if out.exists() else 0}


def main():
    assert sys.argv[1:] in ([], ['--details'])
    details = sys.argv[1:] == ['--details']
    filename = 'details-acquisition.json' if details else 'alternate-acquisition.json'
    assert not (BASE / filename).exists()
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(get, DETAILS if details else REQUESTS))
    record = {'cutoff': '2026-10-07', 'requests': results,
              'scope': 'Fixed public official HTTPS reads only; no upload or downloaded code execution.'}
    (BASE / filename).write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps({'saved': sum(r['returncode'] == 0 for r in results),
                      'failed': sum(r['returncode'] != 0 for r in results)}))


if __name__ == '__main__':
    main()
