#!/usr/bin/env python3
"""Normalize preserved vendor text and bind completed public-read receipts.

No network requests, downloaded code execution, or semantic acceptance.
"""
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-13/commercial-latent'
RAW = ROOT / 'docs/literature/raw'


class VisibleText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.skip += 1
        elif tag in ('p', 'div', 'h1', 'h2', 'h3', 'h4', 'li', 'tr', 'br', 'section'):
            self.parts.append('\n')

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.skip = max(0, self.skip - 1)
        elif tag in ('p', 'div', 'h1', 'h2', 'h3', 'h4', 'li', 'tr', 'section'):
            self.parts.append('\n')

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)


def main():
    requests = json.loads((BASE / 'acquisition-command-results.json').read_text())['requests']
    rows = []
    for r in requests:
        ext = 'pdf' if r['url'].lower().endswith('.pdf') else 'html'
        path = RAW / ('exec13_latent_' + r['id'] + '.' + ext)
        row = {'id': 'exec13_latent_' + r['id'], 'url': r['url'],
               'status': 'saved' if r.get('exit_code') == 0 else 'failed',
               'curl_exit_code': r.get('exit_code'), 'observed_output': r['output'],
               'cutoff': '2026-10-07',
               'cutoff_limit': 'Post-cutoff acquisition does not establish exact historical bytes.',
               'transport': 'Public HTTPS GET; 25 second and 8 MiB caps; no credentials, uploads or remote code execution.'}
        if row['status'] == 'saved':
            data = path.read_bytes()
            row.update(path=str(path.relative_to(ROOT)), sha256=hashlib.sha256(data).hexdigest(),
                       bytes=len(data), local_write_utc=datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat())
            if ext == 'pdf':
                assert data.startswith(b'%PDF-'), 'Non-PDF download'
            else:
                try:
                    source = data.decode('utf-8'); encoding = 'utf-8'
                except UnicodeDecodeError:
                    source = data.decode('cp1252'); encoding = 'cp1252'
                parser = VisibleText(); parser.feed(source)
                text = '\n'.join(' '.join(line.split()) for line in ''.join(parser.parts).splitlines() if line.strip()) + '\n'
                dest = BASE / (r['id'] + '.txt')
                # Earlier recovered normalized text remains preserved.
                if not dest.exists():
                    dest.write_text(text)
                row['normalization'] = {'path': str(dest.relative_to(ROOT)), 'sha256': hashlib.sha256(dest.read_bytes()).hexdigest(),
                                        'source_decoding': encoding, 'purpose': 'Navigation and primary text inspection; raw bytes authoritative.'}
            receipt = RAW / ('exec13_latent_' + r['id'] + '.receipt.json')
            if not receipt.exists():
                receipt.write_text(json.dumps(row, indent=2) + '\n')
        rows.append(row)
    out = BASE / 'acquisition-review.json'
    if out.exists():
        raise ValueError('Acquisition review already preserved; create a successor')
    out.write_text(json.dumps({'requests': rows, 'public_gets': len(rows), 'bank_inputs_required': False}, indent=2) + '\n')
    print(json.dumps({'saved': sum(r['status'] == 'saved' for r in rows), 'failed': sum(r['status'] == 'failed' for r in rows)}))


if __name__ == '__main__':
    main()
