#!/usr/bin/env python3
"""Normalize inert official documents and bind bounded acquisition results."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys

from vendor_text_20261013 import Document

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-13/commercial-temporal'
RAW = ROOT / 'docs/literature/raw'


def ref(path, anchor):
    return {'path': str(path.relative_to(ROOT)),
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'anchor': anchor}


def main():
    number = sys.argv[1]
    assert number.isdigit()
    source = BASE / ('acquisition-commands-' + number + '.json')
    destination = BASE / ('acquisition-review-' + number + '.json')
    assert not destination.exists()
    rows = []
    for row in json.loads(source.read_text())['requests']:
        key = 'exec13_temporal_' + row['id']
        path = RAW / (key + '.' + row['extension'])
        receipt = RAW / (key + '.receipt.json')
        assert not receipt.exists()
        record = {'id': key, 'url': row['url'], 'curl_exit_code': row['exit_code'],
                  'status': 'saved' if row['exit_code'] == 0 else 'failed',
                  'observed_output': row['output'], 'cutoff': '2026-10-07',
                  'accessed_utc': datetime.now(timezone.utc).isoformat(),
                  'cutoff_limit': 'Post-cutoff acquisition; edition dates and historical availability need separate evidence.',
                  'transport': 'Public HTTPS GET; 25-second and 8-MiB caps; TLS verified; no credentials or downloaded code execution.'}
        headers = BASE / (row['id'] + '.headers')
        if headers.exists():
            record['headers'] = ref(headers, 'Preserved HTTP response headers')
        if record['status'] == 'saved':
            data = path.read_bytes()
            record.update(local_copy=ref(path, 'Authentic acquired primary bytes'), bytes=len(data),
                          local_write_utc=datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat())
            text = BASE / (row['id'] + '.txt')
            assert not text.exists()
            if row['extension'] == 'pdf':
                assert data.startswith(b'%PDF-')
                subprocess.run(['pdftotext', '-layout', str(path), str(text)], check=True, timeout=25)
            else:
                try:
                    decoded = data.decode('utf-8'); encoding = 'utf-8'
                except UnicodeDecodeError:
                    decoded = data.decode('cp1252'); encoding = 'cp1252'
                parser = Document(); parser.feed(decoded)
                text.write_text(parser.text + '\n')
                links = BASE / (row['id'] + '.links.json')
                links.write_text(json.dumps(parser.links, indent=2) + '\n')
                record.update(encoding=encoding, links=ref(links, 'Inert official navigation links'))
            record['text_copy'] = ref(text, 'Extracted primary text; original bytes authoritative')
        receipt.write_text(json.dumps(record, indent=2) + '\n')
        rows.append(ref(receipt, record['status'] + ': ' + row['id']))
    destination.write_text(json.dumps({'command_results': ref(source, 'Observed bounded command results'),
        'normalizer': ref(Path(__file__), 'Local extraction code'), 'receipts': rows}, indent=2) + '\n')
    print(json.dumps({'review': str(destination.relative_to(ROOT)), 'requests': len(rows)}))


if __name__ == '__main__':
    main()
