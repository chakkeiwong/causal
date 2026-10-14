#!/usr/bin/env python3
"""Preserve the assessed V9 before the precision and streaming continuation."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
NAMES = ['Preservation and reviewed design', 'Calibration attribution',
         'Fixed-dictionary funding repair', 'Bounded-memory complete execution',
         'Operation and external qualification', 'Scholarly integration and review',
         'Verified inspected delivery']


def digest(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def preserve():
    target = ROOT / 'docs/program/history/v9-assessed-delivery.zip'
    receipt = ROOT / 'docs/program/history/v9-preservation-receipt.json'
    if target.exists() or receipt.exists():
        raise SystemExit('Refusing to overwrite V9 preservation')
    manifest = ROOT / 'docs/program/reconstruction-delivery-manifest.json'
    old = json.loads(manifest.read_text())
    assert old['version'] == '9.0'
    archived, immutable = [], []
    for row in old['artifacts']:
        path = ROOT / row['path']
        if digest(path) != row['sha256'] or path.stat().st_size != row['bytes']:
            raise SystemExit('Changed V9 artifact: ' + row['path'])
        (immutable if path.suffix == '.zip' else archived).append(row)
    temporary = target.with_suffix('.zip.partial')
    with zipfile.ZipFile(temporary, 'x', zipfile.ZIP_DEFLATED, compresslevel=3) as archive:
        for i, row in enumerate(archived):
            archive.write(ROOT / row['path'], row['path'])
            if i % 1000 == 0:
                print(json.dumps({'archived': i, 'total': len(archived)}), flush=True)
        archive.write(manifest, str(manifest.relative_to(ROOT)))
    with zipfile.ZipFile(temporary) as archive:
        for row in archived:
            with archive.open(row['path']) as f:
                assert hashlib.file_digest(f, 'sha256').hexdigest() == row['sha256']
    temporary.replace(target)
    result = dict(status='pass', version='9.0', preserved_artifacts=len(old['artifacts']),
                  archived_artifacts=len(archived), archive=str(target.relative_to(ROOT)),
                  sha256=digest(target), manifest_sha256=digest(manifest),
                  existing_immutable_archives=immutable,
                  scope='All assessed V9 identities verified; non-ZIP artifacts and manifest archived and read back; earlier immutable archives retained by hash.')
    receipt.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'existing_immutable_archives'}))


if __name__ == '__main__':
    preserve()
