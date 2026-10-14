#!/usr/bin/env python3
"""Check and freeze the separate weak-audit supplement, preserving frozen V10."""
import argparse
import contextlib
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess

import delivery_manifest

ROOT = Path(__file__).resolve().parents[1]
TARGET = 'docs/program/weak-audit-delivery-manifest.json'
AUTHOR = 'docs/reviews/weak-audit-author-review.json'
SOURCE = 'docs/reviews/weak-audit-source-review.json'
CHECKS = 'docs/reviews/weak-audit-projection-checks.json'
REPLAY = 'docs/reviews/weak-audit-verification.json'
VISUAL = 'docs/reviews/weak-audit-visual-inspection-2026-10-11.json'
TABLE = 'docs/reviews/weak-audit-table-generation.json'
BASELINE = 'docs/program/reconstruction-delivery-manifest.json'


def read(name):
    return json.loads((ROOT / name).read_text())


def digest(name):
    with (ROOT / name).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def receipt(name, status='pass'):
    data = read(name)
    require(data.get('status') == status and not data.get('issues') and
            not data.get('blocking_findings'), 'Failed receipt: ' + name)
    inputs = data.get('input_sha256')
    require(inputs, 'Unbound receipt: ' + name)
    for path, expected in inputs.items():
        require(digest(path) == expected, 'Changed receipt input: ' + name + '/' + path)
    return data


def pages(name):
    output = subprocess.run(['pdfinfo', str(ROOT / name)], check=True,
                            text=True, capture_output=True).stdout
    match = re.search(r'(?m)^Pages:\s+(\d+)', output)
    require(match, 'No PDF page count: ' + name)
    return int(match.group(1))


def gates():
    baseline = read(BASELINE)
    require(baseline['version'] == '10.0' and len(baseline['artifacts']) == 7430,
            'Wrong frozen baseline')
    with contextlib.redirect_stdout(io.StringIO()):
        require(delivery_manifest.verify(ROOT / BASELINE), 'Frozen V10 identity failed')
    state = read('docs/program/state.json')
    require(state['revision'] == '10.0-precision-streaming' and
            all(phase['status'] == 'complete' for phase in state['phases'] if phase['id'].startswith('J')),
            'Changed V10 program state')
    spec = read('docs/studies/weak-audit-projection-spec.json')
    require(len(spec['designs']) == 5 and spec['repetitions'] == 600 and
            spec['response_error_total'] == spec['audit_error_total'] == .025,
            'Changed registered design')
    for name in (SOURCE, CHECKS, REPLAY, TABLE, VISUAL):
        receipt(name)
    study = read('docs/studies/weak-audit-projection-results.json')
    require(study['status'] == 'pass' and study['requests'] == 3000 and
            len(study['results']) == 5, 'Incomplete final study')
    for name, expected in study['input_sha256'].items():
        require(digest(name) == expected, 'Changed study evidence: ' + name)
    verification = read(REPLAY)
    require(verification['requests'] == 3000 and
            verification['compared_pilot_penalties'] == 2532 and
            verification['whole_line_sets'] == 546, 'Unexpected reconstruction totals')
    by_name = {r['design']['name']: r['summary']['methods'] for r in study['results']}
    require(by_name['near_rank_1200']['weak_audit_projection']['whole_line'] == 546 and
            by_name['near_rank_1200']['weak_audit_projection']['finite'] == 54 and
            by_name['false_exogeneity_1200']['weak_audit_projection']['covered'] == 591,
            'Stale adverse findings')
    visual = read(VISUAL)
    for name, expected in visual['images_sha256'].items():
        require(digest(name) == expected, 'Changed rendered image: ' + name)
    require(len(visual['page_images_viewed']) == 5 and
            visual['assembly_pixel_matches'] == [1, 245, 246, 247, 248, 249],
            'Incomplete rendered inspection')
    folder = 'docs/reviews/weak-audit-rendered/'
    for number in visual['assembly_pixel_matches']:
        require(digest(f'{folder}assembly-source-{number}.png') ==
                digest(f'{folder}assembly-final-{number}.png'),
                'Changed assembled page: ' + str(number))
    for row in (visual['supplement'], visual['reader']):
        require(digest(row['path']) == row['sha256'] and pages(row['path']) == row['pages'],
                'Wrong final PDF: ' + row['path'])
    require(pages('docs/causal_foundations.pdf') == 245 and
            visual['reader']['pages'] == 245 + visual['supplement']['pages'],
            'Wrong assembled page count')
    log = (ROOT / 'docs/supplements/weak_audit_projection_2026-10-11.log').read_text()
    require(not re.search(r'Overfull|Undefined|LaTeX Warning|Package .* Warning|! LaTeX Error', log),
            'Blocking supplement build warning')
    author = receipt(AUTHOR, 'author_reviewed_with_stated_limits')
    require(not author['blocking_findings'] and
            {row['path'] for row in author['final_documents']} ==
            {visual['supplement']['path'], visual['reader']['path']},
            'Incomplete author disposition')
    for row in author['final_documents']:
        require(digest(row['path']) == row['sha256'] and pages(row['path']) == row['pages'],
                'Author-reviewed PDF differs')
    return baseline, visual, author


def freeze():
    baseline, visual, author = gates()
    paths = set(author['input_sha256'])
    for name in (AUTHOR, SOURCE, CHECKS, REPLAY, TABLE, VISUAL, BASELINE,
                 'docs/causal_foundations.pdf'):
        paths.add(name)
    paths.update(visual['images_sha256'])
    for source in read(SOURCE)['cited_primary_works']:
        paths.add(source['local_path'])
    require(TARGET not in paths, 'Circular supplement manifest')
    artifacts = [dict(path=name, sha256=digest(name), bytes=(ROOT / name).stat().st_size)
                 for name in sorted(paths)]
    manifest = dict(version='2026-10-11-weak-audit-supplement',
                    status='author_reviewed_with_stated_limits',
                    date='2026-10-11', baseline_version=baseline['version'],
                    baseline_manifest=BASELINE,
                    documents=author['final_documents'],
                    author_review=AUTHOR, visual_review=VISUAL,
                    source_review=SOURCE,
                    scope='Separate bounded research supplement. Frozen V10 retained; no general calibration, independent acceptance, bank validation, deployment or adopted integration.',
                    verification='python3 tools/weak_audit_delivery.py verify',
                    artifacts=artifacts)
    target = ROOT / TARGET
    temporary = target.with_suffix('.json.tmp')
    temporary.write_text(json.dumps(manifest, indent=2) + '\n')
    temporary.replace(target)
    print(json.dumps(dict(status='frozen', version=manifest['version'],
                          artifacts=len(artifacts), documents=manifest['documents']), indent=2))


def verify():
    gates()
    manifest = read(TARGET)
    require(manifest['version'] == '2026-10-11-weak-audit-supplement' and
            manifest['baseline_manifest'] == BASELINE and
            manifest['status'] == 'author_reviewed_with_stated_limits',
            'Wrong supplement manifest')
    seen = set()
    for row in manifest['artifacts']:
        name = row['path']
        require(name not in seen, 'Duplicate manifest item: ' + name)
        seen.add(name)
        require((ROOT / name).stat().st_size == row['bytes'] and
                digest(name) == row['sha256'], 'Changed manifest artifact: ' + name)
    require(TARGET not in seen and AUTHOR in seen and BASELINE in seen,
            'Missing manifest control evidence')
    print(json.dumps(dict(status='pass', version=manifest['version'],
                          artifacts=len(seen), issues=[],
                          scope='Supplement and preserved baseline file identity, not scientific or bank validation.'), indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['check', 'freeze', 'verify'])
    try:
        command = parser.parse_args().command
        if command == 'freeze':
            freeze()
        elif command == 'verify':
            verify()
        else:
            gates()
            print('Weak-audit supplement gates pass with stated limits.')
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as error:
        raise SystemExit(str(error))
