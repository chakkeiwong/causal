#!/usr/bin/env python3
"""Extract acquired vendor text and bind bytes; no capability inference."""
import hashlib
import json
from pathlib import Path
import subprocess
from vendor_text_20261013 import Document

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-13/commercial-identification'


def main():
    rows = []
    for batch in sorted(BASE.glob('acquisition-*.json')):
        if 'review' in batch.name:
            continue
        for result in json.loads(batch.read_text()):
            if result.get('status') != 'fulfilled':
                rows.append({'status': 'tool_error', 'batch': str(batch.relative_to(ROOT))})
                continue
            row = result['value']
            path = ROOT / 'docs/literature/raw' / ('exec13_ident_' + row['id'] + '.' + row['extension'])
            record = {key: row[key] for key in ['id', 'vendor', 'url', 'extension']}
            record.update(command_result=row['result'], status='unavailable')
            if path.exists():
                data = path.read_bytes()
                record['raw_copy'] = {'path': str(path.relative_to(ROOT)), 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}
                if row['result'].get('exit_code') != 0:
                    record['status'] = 'failed_transfer_bytes_not_evidence'
                elif row['extension'] == 'pdf':
                    if data.startswith(b'%PDF-'):
                        out = BASE / (row['id'] + '.txt')
                        p = subprocess.run(['pdftotext', '-layout', str(path), str(out)], capture_output=True, text=True, timeout=20)
                        record['status'] = 'extracted_primary_candidate' if p.returncode == 0 else 'pdf_extraction_failed'
                        record['extract_returncode'] = p.returncode
                    else:
                        record['status'] = 'non_pdf_response_not_evidence'
                else:
                    parser = Document()
                    parser.feed(data.decode('utf-8', errors='replace'))
                    (BASE / (row['id'] + '.txt')).write_text(parser.text + '\n')
                    (BASE / (row['id'] + '.links.json')).write_text(json.dumps(parser.links, indent=2) + '\n')
                    record['status'] = ('login_page_not_technical_evidence' if 'https://login.causalens.com/' in row['result']['output']
                                        else 'extracted_primary_candidate')
                out = BASE / (row['id'] + '.txt')
                if out.exists():
                    record['text_copy'] = {'path': str(out.relative_to(ROOT)), 'sha256': hashlib.sha256(out.read_bytes()).hexdigest()}
            rows.append(record)
    (BASE / 'acquisition-review.json').write_text(json.dumps({'requests': rows, 'runtime_executed': False}, indent=2) + '\n')
    print(json.dumps({'requests': len(rows), 'dispositions': [(r.get('id'), r['status']) for r in rows]}))


if __name__ == '__main__':
    main()
