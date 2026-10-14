#!/usr/bin/env python3
"""Preserve V7 and record the authorized E-phase continuation."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
NAMES = ['Preserve and review', 'Calibration and audit design',
         'Persistent maps and shared calendars', 'Sharper finite-class effects',
         'Nonlinear variance extension', 'Chunked dependent learning',
         'External validation preparation', 'Scholarly review and delivery']


def digest(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def preserve():
    target = ROOT / 'docs/program/history/v7-assessed-delivery.zip'
    receipt = ROOT / 'docs/program/history/v7-preservation-receipt.json'
    if target.exists():
        raise SystemExit('Refusing to overwrite the V7 archive')
    manifest = ROOT / 'docs/program/reconstruction-delivery-manifest.json'
    rows = json.loads(manifest.read_text())['artifacts']
    archived, immutable = [], []
    for row in rows:
        path = ROOT / row['path']
        if digest(path) != row['sha256'] or path.stat().st_size != row['bytes']:
            raise SystemExit('Changed V7 artifact: ' + row['path'])
        (immutable if path.suffix == '.zip' else archived).append(row)
    with zipfile.ZipFile(target, 'x', zipfile.ZIP_DEFLATED, compresslevel=3) as z:
        for row in archived:
            z.write(ROOT / row['path'], row['path'])
        z.write(manifest, str(manifest.relative_to(ROOT)))
    with zipfile.ZipFile(target) as z:
        for row in archived:
            with z.open(row['path']) as f:
                assert hashlib.file_digest(f, 'sha256').hexdigest() == row['sha256']
    result = dict(status='pass', version='7.0', preserved_artifacts=len(rows),
                  archived_artifacts=len(archived), archive=str(target.relative_to(ROOT)),
                  sha256=digest(target), manifest_sha256=digest(manifest),
                  existing_immutable_archives=immutable,
                  scope='All V7 identities verified; non-ZIP artifacts and manifest archived and read back; prior archives retained by verified hash.')
    receipt.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'existing_immutable_archives'}))


def state_change(args):
    path = ROOT / 'docs/program/state.json'
    state = json.loads(path.read_text())
    if args.command == 'activate':
        assert json.loads((ROOT/'docs/program/history/v7-preservation-receipt.json').read_text())['status']=='pass'
        assert not any(p['id'].startswith('E') for p in state['phases'])
        for phase in state['phases']:
            phase['status'] = 'historical'
        for i, name in enumerate(NAMES):
            state['phases'].append(dict(id=f'E{i:02d}', name=name, deliverable=name,
                depends=[] if i == 0 else [f'E{i-1:02d}'], status='in_progress' if i==0 else 'pending', evidence=[]))
        state.update(revision='8.0-reliability-extension', updated='2026-10-10',
                     status='V8 reliability extension in progress; V7 preserved',
                     active_work_program='E00–E07; prior editions historical',
                     plan='docs/program/reliability-extension-plan.md',
                     author_review='docs/reviews/reliability-plan-review.md',
                     gap_review='docs/reviews/remaining-gaps-v7-2026-10-10.md',
                     delivery_status='V7 preserved; V8 not yet delivered',
                     completion_scope='In progress; every new capability requires its own argument and evidence.',
                     next_action='Register designs and execute E01–E06; retain failures and external dependencies.')
    else:
        phase = next(p for p in state['phases'] if p['id']==args.phase)
        assert args.evidence and all((ROOT/p).is_file() for p in args.evidence)
        if args.status == 'complete':
            assert all(next(p for p in state['phases'] if p['id']==d)['status']=='complete' for d in phase['depends'])
        phase.update(status=args.status,evidence=args.evidence)
        if args.next_action:
            state['next_action']=args.next_action
    path.write_text(json.dumps(state,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(dict(status=state['status'],next_action=state['next_action'])))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=['preserve','activate','record'])
    parser.add_argument('--phase');parser.add_argument('--status',choices=['in_progress','complete'])
    parser.add_argument('--evidence',nargs='*',default=[]);parser.add_argument('--next-action')
    args=parser.parse_args()
    preserve() if args.command=='preserve' else state_change(args)
