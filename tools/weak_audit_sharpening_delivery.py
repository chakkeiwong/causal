#!/usr/bin/env python3
"""Prepare and verify a separate, identity-bound weak-audit follow-up delivery."""

import argparse
import contextlib
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import zipfile

import weak_audit_delivery

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = 'docs/program/weak-audit-sharpening-delivery-manifest.json'
AUTHOR = 'docs/reviews/weak-audit-sharpening-author-review.json'
VISUAL = 'docs/reviews/weak-audit-sharpening-visual-inspection-2026-10-11.json'
SOURCE = 'docs/reviews/weak-audit-sharpening-source-review.json'
CHECKS = 'docs/reviews/weak-audit-sharpening-checks.json'
REPLAY = 'docs/reviews/weak-audit-sharpening-verification.json'
TABLE = 'docs/reviews/weak-audit-sharpening-table-generation.json'
PRESERVED = 'docs/reviews/weak-audit-sharpening-initial-preservation.json'
RESULT = 'docs/studies/weak-audit-sharpening-results.json'
SPEC = 'docs/studies/weak-audit-sharpening-spec.json'
FIRST_MANIFEST = 'docs/program/weak-audit-delivery-manifest.json'
BASE_MANIFEST = 'docs/program/reconstruction-delivery-manifest.json'
BASE_PDF = 'docs/causal_foundations.pdf'
FIRST_PDF = 'docs/supplements/weak_audit_projection_2026-10-11.pdf'
FIRST_READER = 'docs/causal_foundations_with_weak_audit_2026-10-11.pdf'
FOLLOWUP_PDF = 'docs/supplements/weak_audit_sharpening_2026-10-11.pdf'
READER = 'docs/causal_foundations_with_audit_followup_2026-10-11.pdf'
RENDER = 'docs/reviews/weak-audit-sharpening-rendered/'
MATCHED_PAGES = [1, 245, 246, 247, 248, 249, 250, 251, 252, 253]
VIEWED = [RENDER + 'contact.png'] + [RENDER + f'page-{i}.png' for i in range(1, 5)]
IMAGES = VIEWED + [RENDER + f'assembly-{side}-{page}.png'
                   for page in MATCHED_PAGES for side in ('source', 'final')]
DOCUMENTS = [(FOLLOWUP_PDF, 4), (READER, 253)]


def read(path):
    return json.loads((ROOT / path).read_text())


def sha(path):
    with (ROOT / path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def pages(path):
    output = subprocess.run(['pdfinfo', str(ROOT / path)], check=True,
                            capture_output=True, text=True).stdout
    match = re.search(r'(?m)^Pages:\s+(\d+)', output)
    require(match is not None, 'Missing PDF page count: ' + path)
    return int(match.group(1))


def document(path, count):
    require(pages(path) == count, 'Wrong PDF page count: ' + path)
    return dict(path=path, sha256=sha(path), pages=count)


def receipt(path, status='pass'):
    data = read(path)
    require(data.get('status') == status and not data.get('issues') and
            not data.get('blocking_findings'), 'Failed receipt: ' + path)
    inputs = data.get('input_sha256')
    require(isinstance(inputs, dict) and inputs, 'Unbound receipt: ' + path)
    for name, expected in inputs.items():
        require(sha(name) == expected, 'Changed receipt input: ' + path + '/' + name)
    return data


def preserved_run():
    row = read(PRESERVED)
    archive = row['archive']
    require(row['status'] == 'preserved_exploratory_not_qualified' and
            row['original_request_count'] == 3600 and row['entries'] == 15 and
            sha(archive) == row['sha256'], 'Changed exploratory preservation')
    with zipfile.ZipFile(ROOT / archive) as saved:
        require(set(saved.namelist()) == set(row['input_sha256']),
                'Changed exploratory archive entries')
        for name, expected in row['input_sha256'].items():
            require(hashlib.sha256(saved.read(name)).hexdigest() == expected,
                    'Changed exploratory archive member: ' + name)
    return row


def prepare():
    # Receipts are made only after the PDFs and the human-reviewed text are final.
    for path, count in ((BASE_PDF, 245), (FIRST_PDF, 4), (FIRST_READER, 249),
                        *DOCUMENTS):
        require(pages(path) == count, 'Wrong input PDF pages: ' + path)
    for page in MATCHED_PAGES:
        require(sha(RENDER + f'assembly-source-{page}.png') ==
                sha(RENDER + f'assembly-final-{page}.png'),
                'Assembled page differs: ' + str(page))
    image_hashes = {path: sha(path) for path in IMAGES}
    visual_inputs = [BASE_PDF, FIRST_PDF, FIRST_READER, FOLLOWUP_PDF, READER,
                     'docs/reviews/weak-audit-sharpening-visual-inspection-2026-10-11.md',
                     'docs/supplements/weak_audit_sharpening_2026-10-11.tex',
                     'docs/supplements/weak-audit-sharpening-table.tex']
    visual = dict(status='pass', date='2026-10-11', issues=[], blocking_findings=[],
                  supplement=document(FOLLOWUP_PDF, 4), reader=document(READER, 253),
                  page_images_viewed=VIEWED, images_sha256=image_hashes,
                  assembly_pixel_matches=MATCHED_PAGES,
                  scope='Author inspection of all four new pages and sampled V10/first-supplement boundaries; every appended source page matches the 253-page assembly.',
                  input_sha256={name: sha(name) for name in visual_inputs})
    (ROOT / VISUAL).write_text(json.dumps(visual, indent=2) + '\n')

    evidence = [SOURCE, CHECKS, REPLAY, TABLE, PRESERVED, RESULT, SPEC, VISUAL,
                FIRST_MANIFEST, BASE_MANIFEST, BASE_PDF, FIRST_PDF, FIRST_READER,
                FOLLOWUP_PDF, READER, 'AGENTS.md',
                'docs/program/weak-audit-sharpening-plan-2026-10-11.md',
                'docs/program/weak-audit-followup-delivery-2026-10-11.md',
                'docs/reviews/weak-audit-sharpening-author-review-2026-10-11.md',
                'docs/reviews/remaining-gaps-weak-audit-sharpening-2026-10-11.md',
                'docs/reviews/weak-audit-sharpening-execution-notes-2026-10-11.md',
                'docs/reviews/weak-audit-sharpening-visual-inspection-2026-10-11.md',
                'docs/supplements/weak_audit_sharpening_2026-10-11.tex',
                'docs/supplements/weak_audit_sharpening_2026-10-11.log',
                'docs/supplements/weak-audit-sharpening-table.tex',
                'tools/weak_audit_sharpening_delivery.py']
    for path in (SOURCE, CHECKS, REPLAY, TABLE, RESULT):
        evidence.extend(read(path)['input_sha256'])
    evidence.extend(IMAGES)
    evidence.append(read(PRESERVED)['archive'])
    author = dict(status='author_reviewed_with_stated_limits', date='2026-10-11',
                  review='docs/reviews/weak-audit-sharpening-author-review-2026-10-11.md',
                  blocking_findings=[],
                  final_documents=[document(path, count) for path, count in DOCUMENTS],
                  scientific_disposition='Project-transformed pointwise response bands and exact binomial audit inversion retain stated-law set coverage; no general width theorem, false-law guarantee or finite-sample response exactness.',
                  capability_disposition='All 2937 paired finite transformed sets narrow, but 558/600 original near-rank and 105/600 higher-audit sets remain whole-line; useful decision precision is open.',
                  remaining='D04 causal truth and D09 useful precision need new information and registered validation; D07/D08/D10 need independent, authentic bank, platform and economic evidence.',
                  scope='Bounded author-reviewed follow-up; V10 and first supplement unchanged, no independent acceptance or bank deployment.',
                  input_sha256={name: sha(name) for name in sorted(set(evidence))})
    (ROOT / AUTHOR).write_text(json.dumps(author, indent=2) + '\n')
    print(json.dumps(dict(status='prepared', images=len(IMAGES),
                          author_inputs=len(author['input_sha256'])), indent=2))


def gates():
    with contextlib.redirect_stdout(io.StringIO()):
        weak_audit_delivery.verify()  # Includes the frozen 7,430-artifact V10 gate.
    first = read(FIRST_MANIFEST)
    require(first['version'] == '2026-10-11-weak-audit-supplement',
            'Wrong first-supplement baseline')
    spec = read(SPEC)
    require(spec['version'] == 2 and spec['seed'] == 10112751 and
            spec['repetitions'] == 600 and len(spec['designs']) == 6 and
            spec['response_error'] == spec['audit_error'] == .025,
            'Changed registered follow-up design')
    for path in (SOURCE, CHECKS, REPLAY, TABLE, VISUAL):
        receipt(path)
    preserved = preserved_run()
    study = receipt(RESULT)
    require(study['requests'] == 3600 and len(study['results']) == 6,
            'Incomplete fresh study')
    replay = read(REPLAY)
    require(replay['requests'] == 3600 and replay['preserved_exploratory_requests'] == 3600 and
            replay['total_both_finite'] == replay['transformed_narrower_total'] == 2937,
            'Unexpected fresh reconstruction totals')
    checks = read(CHECKS)
    witness = checks['observational_equivalence']
    require(checks['maximum_scaled_variance_difference'] < 1e-12 and
            checks['zero_difference_fixture'] == 'unavailable_response_variance' and
            witness['maximum_path_difference'] < 1e-12 and
            387000 < witness['financial_target_difference'] < 388000,
            'Numerical or identification witness changed')
    by_name = {r['design']['name']: r['summary'] for r in study['results']}
    candidate, transformed = spec['methods']
    near = by_name['near_rank_1200']['methods']
    larger = by_name['near_rank_more_audit_1200']['methods']
    false = by_name['false_exogeneity_1200']['methods']
    require(near[candidate]['whole_line'] == near[transformed]['whole_line'] == 558 and
            near[candidate]['finite'] == near[transformed]['finite'] == 42 and
            larger[candidate]['whole_line'] == larger[transformed]['whole_line'] == 105 and
            larger[candidate]['finite'] == larger[transformed]['finite'] == 495 and
            false[candidate]['covered'] == 597 and false[transformed]['covered'] == 561,
            'Changed adverse study findings')
    require(sum(r['summary']['paired']['both_finite'] for r in study['results']) == 2937 and
            all(r['summary']['paired']['transformed_narrower'] ==
                r['summary']['paired']['both_finite'] for r in study['results']),
            'Changed paired precision result')
    visual = read(VISUAL)
    require(visual['page_images_viewed'] == VIEWED and
            visual['assembly_pixel_matches'] == MATCHED_PAGES and
            set(visual['images_sha256']) == set(IMAGES),
            'Incomplete visual inspection')
    for path, expected in visual['images_sha256'].items():
        require(sha(path) == expected, 'Changed rendered image: ' + path)
    for page in MATCHED_PAGES:
        require(sha(RENDER + f'assembly-source-{page}.png') ==
                sha(RENDER + f'assembly-final-{page}.png'),
                'Changed assembled page: ' + str(page))
    require(pages(BASE_PDF) == 245 and pages(FIRST_PDF) == 4 and
            pages(FIRST_READER) == 249 and
            pages(READER) == 245 + 4 + pages(FOLLOWUP_PDF),
            'Wrong assembled reader structure')
    for row in (visual['supplement'], visual['reader']):
        require(document(row['path'], row['pages']) == row,
                'Changed final PDF: ' + row['path'])
    log = (ROOT / 'docs/supplements/weak_audit_sharpening_2026-10-11.log').read_text()
    require(not re.search(r'Overfull|Undefined|LaTeX Warning|Package .* Warning|! LaTeX Error', log),
            'Blocking follow-up LaTeX warning')
    author = receipt(AUTHOR, 'author_reviewed_with_stated_limits')
    require(author['review'] in author['input_sha256'] and
            author['final_documents'] == [document(path, count) for path, count in DOCUMENTS] and
            preserved['archive'] in author['input_sha256'] and
            'docs/studies/weak-audit-sharpening-final.jsonl' in author['input_sha256'] and
            all(path in author['input_sha256'] for path in IMAGES),
            'Incomplete author-reviewed evidence binding')
    return author


def expected_artifacts(author):
    names = set(author['input_sha256']) | {AUTHOR, SOURCE, CHECKS, REPLAY, TABLE,
                                           PRESERVED, VISUAL, RESULT, SPEC,
                                           FIRST_MANIFEST, BASE_MANIFEST}
    require(MANIFEST not in names, 'Circular follow-up manifest')
    return names


def freeze():
    author = gates()
    rows = [dict(path=name, sha256=sha(name), bytes=(ROOT / name).stat().st_size)
            for name in sorted(expected_artifacts(author))]
    manifest = dict(version='2026-10-11-weak-audit-follow-up',
                    status='author_reviewed_with_stated_limits', date='2026-10-11',
                    baseline_manifest=BASE_MANIFEST,
                    first_supplement_manifest=FIRST_MANIFEST,
                    documents=author['final_documents'], author_review=AUTHOR,
                    visual_review=VISUAL, source_review=SOURCE,
                    preserved_initial=PRESERVED,
                    scope='Separate bounded research follow-up; frozen V10 and first supplement retained. No general calibration, independent acceptance, bank validation, deployment or adopted integration.',
                    verification='python3 tools/weak_audit_sharpening_delivery.py verify',
                    artifacts=rows)
    target = ROOT / MANIFEST
    temporary = target.with_suffix('.json.tmp')
    temporary.write_text(json.dumps(manifest, indent=2) + '\n')
    temporary.replace(target)
    print(json.dumps(dict(status='frozen', version=manifest['version'],
                          artifacts=len(rows), documents=manifest['documents']), indent=2))


def verify():
    author = gates()
    manifest = read(MANIFEST)
    require(manifest['version'] == '2026-10-11-weak-audit-follow-up' and
            manifest['status'] == 'author_reviewed_with_stated_limits' and
            manifest['baseline_manifest'] == BASE_MANIFEST and
            manifest['first_supplement_manifest'] == FIRST_MANIFEST and
            manifest['documents'] == author['final_documents'],
            'Wrong follow-up manifest identity')
    paths = [row['path'] for row in manifest['artifacts']]
    require(len(paths) == len(set(paths)) and
            set(paths) == expected_artifacts(author),
            'Missing or duplicated follow-up artifact')
    for row in manifest['artifacts']:
        path = row['path']
        require((ROOT / path).stat().st_size == row['bytes'] and
                sha(path) == row['sha256'], 'Changed follow-up artifact: ' + path)
    print(json.dumps(dict(status='pass', version=manifest['version'],
                          artifacts=len(paths), issues=[],
                          scope='Exact local delivery identity, not independent science or bank validation.'),
                     indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['prepare', 'check', 'freeze', 'verify'])
    try:
        command = parser.parse_args().command
        if command == 'prepare':
            prepare()
        elif command == 'check':
            gates()
            print('Follow-up delivery gates pass with stated limits.')
        elif command == 'freeze':
            freeze()
        else:
            verify()
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError,
            zipfile.BadZipFile) as error:
        raise SystemExit(str(error))
