#!/usr/bin/env python3
"""Run the unchanged fixed public collector with a temporary reviewed manifest.

Only the registered HTTPS collector performs networking. Its source and host
allowlist are unchanged. Preserve and restore the frozen manifest in finally;
retain the exact batch, collector transcript and restoration evidence. No upload
or downloaded-code execution occurs. Inspect the report after interrupted runs.
"""
import argparse
from datetime import datetime, timezone
import fcntl
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'docs/literature/fetch-manifest.json'
BASELINE = 'c86a5ff3f9a4b5ecab80e26698da8ba8a641ffca70a640e5508fca187872533d'
COLLECTOR = ROOT / 'tools/public_sources.py'

def digest(data):
    return hashlib.sha256(data).hexdigest()

def collect(batch):
    batch = batch.resolve()
    if not batch.is_relative_to(ROOT / 'docs/program/repair-v12'):
        raise ValueError('Batch must be under the V12 repair directory')
    parsed = json.loads(batch.read_text())
    if not 1 <= len(parsed['requests']) <= 24:
        raise ValueError('Use bounded batches of at most 24 requests')
    if any(not r['id'].startswith('v12_') for r in parsed['requests']):
        raise ValueError('New requests require versioned v12_ identities')
    for row in parsed['requests']:
        receipt = ROOT / 'docs/literature/raw' / (row['id'] + '.receipt.json')
        if receipt.exists() and json.loads(receipt.read_text()).get('url') != row['url']:
            raise ValueError('Cannot change an existing request identity')
    control = ROOT / 'docs/program/repair-v12/source-collection'
    control.mkdir(exist_ok=True)
    run = control / (batch.stem + '-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
    run.mkdir()
    report = {'batch': str(batch.relative_to(ROOT)), 'batch_sha256': digest(batch.read_bytes()),
              'collector_sha256': digest(COLLECTOR.read_bytes()), 'requests': len(parsed['requests']),
              'started_at': datetime.now(timezone.utc).isoformat(), 'scope': 'Public HTTPS reads only; no source inspection or qualification implied.'}
    with (control / 'manifest.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        original = MANIFEST.read_bytes()
        if digest(original) != BASELINE:
            raise ValueError('Frozen manifest identity changed; investigate before fetching')
        (run / 'original-manifest.json').write_bytes(original)
        staged = batch.read_bytes()
        (run / 'batch.json').write_bytes(staged)
        MANIFEST.write_bytes(staged)
        try:
            with (run / 'collector.log').open('w') as log:
                result = subprocess.run([str(COLLECTOR), 'fetch'], cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, timeout=300)
            report['returncode'] = result.returncode
        except (OSError, subprocess.SubprocessError) as error:
            report['error'] = str(error)
        finally:
            current = MANIFEST.read_bytes()
            if current == staged:
                MANIFEST.write_bytes(original)
            report['manifest_restored'] = MANIFEST.read_bytes() == original
            report['manifest_sha256'] = digest(MANIFEST.read_bytes())
            report['completed_at'] = datetime.now(timezone.utc).isoformat()
            receipts = []
            for row in parsed['requests']:
                path = ROOT / 'docs/literature/raw' / (row['id'] + '.receipt.json')
                if path.exists():
                    receipt = json.loads(path.read_text())
                    receipts.append({k: receipt[k] for k in ['id','status','error','path','sha256'] if k in receipt})
            report['receipts'] = receipts
            report['saved'] = sum(r['status'] == 'saved' for r in receipts)
            report['failed'] = sum(r['status'] == 'failed' for r in receipts)
            (run / 'report.json').write_text(json.dumps(report, indent=2)+'\n')
    if not report['manifest_restored']:
        raise ValueError('Manifest changed concurrently; preserved original requires reconciliation')
    print(json.dumps({'report': str((run/'report.json').relative_to(ROOT)), **{k:report[k] for k in ['requests','saved','failed','manifest_restored']}}))

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('batch',type=Path)
    collect(parser.parse_args().batch)
