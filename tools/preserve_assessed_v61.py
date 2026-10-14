#!/usr/bin/env python3
"""Preserve the final assessed V6.1 bytes before the authorized C revision."""
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    manifest = ROOT / 'docs/program/reconstruction-delivery-manifest.json'
    target = ROOT / 'docs/program/history/v6.1-assessed-delivery.zip'
    receipt = ROOT / 'docs/program/history/v6.1-preservation-receipt.json'
    if target.exists():
        raise SystemExit('Preservation already exists; refusing to overwrite it')
    rows = json.loads(manifest.read_text())['artifacts']
    immutable, archived = [], []
    for row in rows:
        path = ROOT / row['path']
        if path.stat().st_size != row['bytes'] or sha(path) != row['sha256']:
            raise SystemExit('Changed before preservation: ' + row['path'])
        (immutable if path.suffix == '.zip' else archived).append(row)
    additions = [manifest] + list((ROOT / 'docs/reviews').glob('*v6.1*'))
    additions += list((ROOT / 'docs/reviews').glob('gap-closure-plan*'))
    additions += [ROOT / 'docs/program/gap-closure-plan-2026-10-10.md']
    with zipfile.ZipFile(target, 'x', zipfile.ZIP_DEFLATED, compresslevel=3) as archive:
        for row in archived:
            archive.write(ROOT / row['path'], row['path'])
        names = {r['path'] for r in archived}
        for path in additions:
            name = str(path.relative_to(ROOT))
            if name not in names:
                archive.write(path, name)
                names.add(name)
    with zipfile.ZipFile(target) as archive:
        for row in archived:
            with archive.open(row['path']) as stream:
                actual = hashlib.file_digest(stream, 'sha256').hexdigest()
            if actual != row['sha256']:
                raise SystemExit('Archive mismatch: ' + row['path'])
    result = dict(status='pass', version='6.1', preserved_artifacts=len(rows),
                  archived_artifacts=len(archived), archive=str(target.relative_to(ROOT)),
                  sha256=sha(target), manifest_sha256=sha(manifest),
                  existing_immutable_archives=immutable,
                  scope='All final V6.1 manifest entries verified. Prior ZIPs remain at their verified identities; all other entries and the assessed plan are archived and read back.')
    receipt.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'existing_immutable_archives'}, indent=2))


if __name__ == '__main__':
    main()
