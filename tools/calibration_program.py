#!/usr/bin/env python3
"""Preserve the assessed V8 and record the authorized F-phase program."""
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
    target = ROOT / 'docs/program/history/v8-assessed-delivery.zip'
    receipt = ROOT / 'docs/program/history/v8-preservation-receipt.json'
    if target.exists() or receipt.exists():
        raise SystemExit('Refusing to overwrite V8 preservation')
    manifest = ROOT / 'docs/program/reconstruction-delivery-manifest.json'
    old = json.loads(manifest.read_text())
    assert old['version'] == '8.0'
    archived, immutable = [], []
    for row in old['artifacts']:
        path = ROOT / row['path']
        if digest(path) != row['sha256'] or path.stat().st_size != row['bytes']:
            raise SystemExit('Changed V8 artifact: ' + row['path'])
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
    result = dict(status='pass', version='8.0', preserved_artifacts=len(old['artifacts']),
                  archived_artifacts=len(archived), archive=str(target.relative_to(ROOT)),
                  sha256=digest(target), manifest_sha256=digest(manifest),
                  existing_immutable_archives=immutable,
                  scope='All assessed V8 identities verified; non-ZIP artifacts and manifest archived and read back; earlier immutable archives retained by hash.')
    receipt.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'existing_immutable_archives'}))


def state_change(args):
    path = ROOT / 'docs/program/state.json'
    state = json.loads(path.read_text())
    if args.command == 'activate':
        assert json.loads((ROOT / 'docs/program/history/v8-preservation-receipt.json').read_text())['status'] == 'pass'
        assert not any(p['id'].startswith('F') for p in state['phases'])
        for phase in state['phases']:
            phase['status'] = 'historical'
        for i, name in enumerate(NAMES):
            state['phases'].append(dict(id=f'F{i:02d}', name=name, deliverable=name,
                depends=[] if i == 0 else [f'F{i-1:02d}'],
                status='in_progress' if i == 0 else 'pending', evidence=[]))
        state.update(revision='9.0-calibration-completion', updated='2026-10-10',
            status='V9 calibration and bounded-memory program in progress; V8 preserved',
            active_work_program='F00–F06; prior editions historical',
            plan='docs/program/calibration-completion-plan.md',
            author_review='docs/reviews/calibration-plan-review.md',
            gap_review='docs/reviews/remaining-gaps-v8-2026-10-10.md',
            delivery_status='Assessed V8 preserved; V9 not yet delivered',
            completion_scope='In progress; calibration, selected execution and external dependencies have separate evidence requirements.',
            next_action='Derive and independently check the funding nuisance/rate/covariance arguments; run registered diagnostic pilots before fresh final validation.')
    else:
        phase = next(p for p in state['phases'] if p['id'] == args.phase)
        assert args.evidence and all((ROOT / p).is_file() for p in args.evidence)
        if args.status == 'complete':
            assert all(next(p for p in state['phases'] if p['id'] == dep)['status'] == 'complete' for dep in phase['depends'])
        phase.update(status=args.status, evidence=args.evidence)
        if args.next_action:
            state['next_action'] = args.next_action
    path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(dict(status=state['status'], next_action=state['next_action'])))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['preserve', 'activate', 'record'])
    parser.add_argument('--phase')
    parser.add_argument('--status', choices=['in_progress', 'complete'])
    parser.add_argument('--evidence', nargs='*', default=[])
    parser.add_argument('--next-action')
    args = parser.parse_args()
    preserve() if args.command == 'preserve' else state_change(args)
