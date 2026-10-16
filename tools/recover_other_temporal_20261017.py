#!/usr/bin/env python3
"""Preserve a crash-recovery checkpoint and stage narrow primary follow-ups."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from publish_latent_r_review_v2_20261013 import ref, write

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-17/other-temporal'
RAW = ROOT / 'docs/literature/raw'


def read(path):
    return json.loads(path.read_text())


def stage():
    selections = {
        'mvgc': ['stats/mvgc_cdf.m', 'docs/mvgc_preprint.pdf'],
        'cdnod': ['nonsta_cd_new.m', 'infer_nonsta_dir.m', 'cd_non_con_fun.m'],
        'bnt': ['BNT/CPDs/@root_CPD/root_CPD.m', 'BNT/CPDs/@root_CPD/sample_node.m'],
    }
    pins = read(BASE / 'additional-pins.json')
    pins.update(read(ROOT / 'docs/program/execution/2026-10-13/other-discovery/pins.json'))
    items = []
    for package, paths in selections.items():
        pin = pins[package]
        tree_path = RAW / (f'exec13_other_tree_{package}.json' if package == 'bnt'
                           else f'exec17_other_temporal_tree_{package}.json')
        tree = read(tree_path)
        assert not tree['truncated']
        by_path = {r['path']: r for r in tree['tree'] if r['type'] == 'blob'}
        for index, path in enumerate(paths):
            row = by_path[path]
            extension = 'pdf' if path.endswith('.pdf') else 'txt'
            items.append({'id': f'exec17_other_temporal_follow_{package}_{index}',
                'url': f'https://raw.githubusercontent.com/{pin["repository"]}/{pin["sha"]}/{path}',
                'extension': extension, 'package': package, 'source_path': path,
                'expected_bytes': row['size'], 'blob_sha1': row['sha'], 'pin': pin})
    requests = [{k: item[k] for k in ['id', 'url', 'extension']} for item in items]
    requests.append({'id': 'exec17_other_temporal_cdnod_paper',
        'url': 'https://jmlr.org/papers/volume21/19-232/19-232.pdf', 'extension': 'pdf'})
    write(BASE / 'follow-up-files.json', {'items': items})
    write(BASE / 'acquisition-manifest-v4.json', {'requests': requests,
        'cutoff': '2026-10-07',
        'reason': 'Resolve invoked conditional-test, direction, root-CPD and scholarly premises; no downloaded code execution.'})
    write(BASE / 'crash-recovery.json', {
        'recovered_utc': datetime.now(timezone.utc).isoformat(),
        'observed': ['Canonical controller check passed; 118/376 proposal operations recorded.',
            'Temporal other-language coverage operation remains active; no global blocker.',
            '871-page ontology reader and all staged temporal originals survived.',
            'Ontology commit 677f01acbb0aacbe0319aabd21d94205d32bae8b already remote-verified.',
            'No background research worker; no new image allowance is inferred from crash recovery.'],
        'preserved': [ref(BASE / 'plan.md', 'Reviewed plan'),
            ref(BASE / 'exact-results.json', 'Superseded preliminary mathematical illustration'),
            ref(BASE / 'exact-results-v2.json', 'Current six exact reference families'),
            ref(ROOT / 'docs/program/execution/2026-10-17/variable-ontology/publication/git-publication-677f01ac.json', 'Verified ontology publication')],
        'next_action': 'Finish primary inspection and byte verification, integrate scoped comparison, record/publish, renew exact-reader reviews and continue the next eligible operation.'})
    (ROOT / 'docs/literature/fetch-manifest.json').write_text(json.dumps({'requests': requests}, indent=2) + '\n')
    print(json.dumps({'follow_up_requests': len(requests), 'checkpoint': 'preserved'}))


def verify():
    items = []
    for name in ['selected-files.json', 'additional-files.json', 'follow-up-files.json']:
        items.extend(read(BASE / name)['items'])
    # The three earlier narrow follow-ups predate the selected-file supplement.
    manifest = read(BASE / 'acquisition-manifest-v2.json')
    inherited_pins = read(ROOT / 'docs/program/execution/2026-10-13/other-discovery/pins.json')
    for request in manifest['requests']:
        if request['extension'] != 'txt':
            continue
        package = 'associations' if 'associations' in request['id'] else 'varlingam'
        pin = inherited_pins[package]
        path = request['url'].split('/' + pin['sha'] + '/', 1)[1]
        tree = read(RAW / f'exec13_other_tree_{package}.json')
        row = next(r for r in tree['tree'] if r['path'] == path)
        items.append(dict(request, package=package, source_path=path, pin=pin,
            expected_bytes=row['size'], blob_sha1=row['sha']))
    records = []
    for item in items:
        local = RAW / (item['id'] + '.' + item['extension'])
        data = local.read_bytes()
        receipt = read(RAW / (item['id'] + '.receipt.json'))
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert len(data) == item['expected_bytes'] and blob == item['blob_sha1'], item['id']
        assert receipt['url'] == item['url'] and receipt['sha256'] == hashlib.sha256(data).hexdigest()
        assert item['pin']['date'][:10] <= '2026-10-07'
        records.append(dict(item, local_copy=ref(local, item['source_path']),
            retrieval=ref(RAW / (item['id'] + '.receipt.json'), 'Original collector receipt')))
    write(BASE / 'acquisition-verification-v2.json', {'status': 'pass',
        'records': records, 'files_verified': len(records),
        'scope': 'Original bytes, retrieval SHA-256 and pinned Git blob identity; no runtime qualification.'})
    print(json.dumps({'verified_pinned_originals': len(records)}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['stage', 'verify'])
    args = parser.parse_args()
    {'stage': stage, 'verify': verify}[args.command]()
