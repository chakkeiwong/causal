#!/usr/bin/env python3
"""Bind and verify the linked-outcome continuation without altering predecessors."""
import argparse
import contextlib
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import zipfile

import weak_audit_sharpening_delivery as prior

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = 'docs/program/linked-funding-delivery-manifest.json'
AUTHOR = 'docs/reviews/linked-funding-author-review.json'
VISUAL = 'docs/reviews/linked-funding-visual-inspection-2026-10-11.json'
BUILD = 'docs/reviews/linked-funding-build.json'
CHECKS = 'docs/reviews/linked-funding-checks.json'
REPLAY = 'docs/reviews/linked-funding-verification.json'
SOURCE = 'docs/reviews/linked-funding-source-review.json'
TABLE = 'docs/reviews/linked-funding-table-generation.json'
ALGEBRA = 'docs/reviews/linked-funding-interpretation-checks.json'
PRESERVED = 'docs/reviews/linked-funding-initial-preservation.json'
RESULT = 'docs/studies/linked-funding-results.json'
SPEC = 'docs/studies/linked-funding-spec.json'
STATE = 'docs/program/linked-funding-state-2026-10-11.json'
RECEIPTS = (BUILD,CHECKS,REPLAY,SOURCE,TABLE,ALGEBRA,RESULT)
DOCUMENTS = [('docs/supplements/linked_funding_2026-10-11.pdf',6),
             ('docs/causal_foundations_with_linked_audits_2026-10-11.pdf',259)]
MATCHES = [1,245]+list(range(246,260))
FOLDER = 'docs/reviews/linked-funding-rendered/'
VIEWED = [FOLDER+f'page-{i}.png' for i in range(1,7)]


def read(p):
    return json.loads((ROOT/p).read_text())


def sha(p):
    with (ROOT/p).open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()


def require(condition,message):
    if not condition:
        raise ValueError(message)


def pages(p):
    result = subprocess.run(['pdfinfo',str(ROOT/p)],check=True,capture_output=True,text=True)
    return int(re.search(r'(?m)^Pages:\s+(\d+)',result.stdout).group(1))


def documents():
    rows = []
    for p,n in DOCUMENTS:
        require(pages(p) == n,'Wrong final PDF page count: '+p)
        rows.append(dict(path=p,pages=n,sha256=sha(p)))
    return rows


def receipt(p,status='pass'):
    row = read(p)
    require(row.get('status') == status and not row.get('issues') and
            not row.get('blocking_findings'),'Failed receipt: '+p)
    require(row.get('input_sha256'),'Unbound receipt: '+p)
    for name,h in row['input_sha256'].items():
        require(sha(name) == h,'Changed receipt input: '+p+'/'+name)
    return row


def prepare():
    build = receipt(BUILD)
    require(build['documents'] == documents(),'Build PDF identity differs')
    visual_md = 'docs/reviews/linked-funding-visual-inspection-2026-10-11.md'
    visual = dict(status='pass',date='2026-10-11',issues=[],blocking_findings=[],
                  final_documents=documents(),page_images_viewed=VIEWED,
                  assembly_pixel_matches=build['assembly_pixel_matches'],
                  all_page_text_matches=build['all_page_text_matches'],
                  images_sha256=build['images_sha256'],
                  scope='Actual final six-page inspection; 259-page text equivalence and 16 stated raster pairs, with inherited visual review for unchanged predecessor pages.',
                  input_sha256={p:sha(p) for p in [BUILD,visual_md]+[p for p,_ in DOCUMENTS]})
    (ROOT/VISUAL).write_text(json.dumps(visual,indent=2)+'\n')
    names = set(RECEIPTS) | {VISUAL,PRESERVED,SPEC,STATE,prior.MANIFEST,
              'docs/program/weak-audit-delivery-manifest.json',
              'docs/program/reconstruction-delivery-manifest.json',
              'docs/program/linked-funding-plan-2026-10-11.md',
              'docs/program/linked-funding-delivery-2026-10-11.md',
              'docs/reviews/linked-funding-author-review-2026-10-11.md',
              'docs/reviews/remaining-gaps-linked-funding-2026-10-11.md',
              'docs/reviews/linked-funding-execution-notes-2026-10-11.md',
              'docs/reviews/linked-funding-environment.json',visual_md,
              'contracts/linked-funding.md','tools/linked_funding_delivery.py','AGENTS.md'}
    for p in RECEIPTS:
        names.update(read(p)['input_sha256'])
    names.update(build['images_sha256'])
    names.add(read(PRESERVED)['archive'])
    author = dict(status='author_reviewed_with_stated_limits',date='2026-10-11',
                  review='docs/reviews/linked-funding-author-review-2026-10-11.md',
                  blocking_findings=[],final_documents=documents(),
                  scientific_disposition='Conditional audit expectation and diagonal added variance extend the selected funding law; causal truth, pilot rates, audit independence and pointwise normal approximation remain premises.',
                  capability_disposition='Finite linked intervals in 4800/4800 fresh requests; exact-rank coverage 559/600 and retained severe false-premise failures prohibit general calibration qualification.',
                  remaining='Derived calibration correction or new design; authentic audit/assignment truth, bank thresholds/prices, independent reviewer and target-platform acceptance.',
                  input_sha256={p:sha(p) for p in sorted(names)})
    (ROOT/AUTHOR).write_text(json.dumps(author,indent=2)+'\n')
    print(json.dumps(dict(status='prepared',author_inputs=len(names),viewed_pages=6),indent=2))


def gates():
    with contextlib.redirect_stdout(io.StringIO()):
        prior.verify()
    for p in RECEIPTS:
        receipt(p)
    spec = read(SPEC)
    require(spec['version'] == 2 and spec['seed'] == 10113131 and
            spec['repetitions'] == 600 and len(spec['designs']) == 8 and
            len(spec['methods']) == 3,'Wrong registered continuation')
    preserved = read(PRESERVED)
    require(preserved['status'] == 'preserved_schema_failure_not_qualified' and
            preserved['requests'] == 600 and preserved['entries'] == 7 and
            sha(preserved['archive']) == preserved['sha256'],'Changed failed partial run')
    with zipfile.ZipFile(ROOT/preserved['archive']) as z:
        require(set(z.namelist()) == set(preserved['input_sha256']),'Wrong partial archive membership')
        for p,h in preserved['input_sha256'].items():
            require(hashlib.sha256(z.read(p)).hexdigest() == h,'Changed partial archive input: '+p)
    checks = read(CHECKS)
    require(len(checks['tests']) == 9 and checks['maximum_relative_dense_difference'] < 2e-10 and
            checks['deterministic_fixture'] == 'unavailable_response_variance',
            'Missing independent numerical qualification')
    replay = read(REPLAY)
    require(replay['requests'] == 4800 and replay['preserved_schema_failure_requests'] == 600 and
            replay['regenerated_request_keys'] == [d['name']+'/0' for d in spec['designs']],
            'Incomplete saved request verification')
    study = read(RESULT)
    require(study['requests'] == 4800 and len(study['results']) == 8,'Incomplete study')
    by_name = {r['design']['name']:r['summary']['methods'] for r in study['results']}
    for row in by_name.values():
        require(all(row[m]['finite'] == 600 for m in ('linked_augmented','linked_ipw')),
                'Changed linked availability')
    require(by_name['near_rank']['transformed_counts']['finite'] == 48 and
            by_name['near_rank']['linked_augmented']['covered'] == 572 and
            by_name['exact_rank']['transformed_counts']['whole_line'] == 600 and
            by_name['exact_rank']['linked_augmented']['covered'] == 559 and
            by_name['false_exogeneity']['linked_augmented']['covered'] == 148 and
            by_name['wrong_inclusion']['linked_augmented']['covered'] == 378 and
            by_name['noisy_labels']['linked_augmented']['covered'] == 528,
            'Changed adverse findings')
    require({s['id'] for s in read(SOURCE)['cited_primary_works']} == {'dml2018','newey1986'},
            'Unreviewed scholarly source role')
    build = read(BUILD)
    require(build['all_page_text_matches'] == 259 and not build['merge_diagnostics'] and
            build['assembly_pixel_matches'] == MATCHES and build['documents'] == documents(),
            'Incomplete final assembly checks')
    for p,h in build['images_sha256'].items():
        require(sha(p) == h,'Changed rendered image: '+p)
    for n in MATCHES:
        require(sha(FOLDER+f'assembly-source-{n}.png') == sha(FOLDER+f'assembly-final-{n}.png'),
                'Changed assembled page: '+str(n))
    log = (ROOT/'docs/supplements/linked_funding_2026-10-11.log').read_text()
    require(not re.search(r'Overfull|Undefined|LaTeX Warning|Package .* Warning|! LaTeX Error',log),
            'Blocking final LaTeX warning')
    visual = receipt(VISUAL)
    require(visual['page_images_viewed'] == VIEWED and visual['final_documents'] == documents() and
            visual['images_sha256'] == build['images_sha256'],'Incomplete actual rendered inspection')
    author = receipt(AUTHOR,'author_reviewed_with_stated_limits')
    require(author['final_documents'] == documents() and author['review'] in author['input_sha256'] and
            all(p in author['input_sha256'] for p in (PRESERVED,RESULT,REPLAY,SOURCE,VISUAL,STATE)),
            'Incomplete author binding')
    state = read(STATE)
    require(state['status'] == 'author_reviewed_with_stated_limits' and state['reader_pages'] == 259 and
            state['delivery_manifest'] == MANIFEST,'Wrong continuation status')
    return author


def artifact_names(author):
    names = set(author['input_sha256']) | {AUTHOR}
    require(MANIFEST not in names,'Circular delivery manifest')
    return names


def freeze():
    author = gates()
    artifacts = [dict(path=p,sha256=sha(p),bytes=(ROOT/p).stat().st_size)
                 for p in sorted(artifact_names(author))]
    manifest = dict(version='2026-10-11-linked-funding',date='2026-10-11',
                    status='author_reviewed_with_stated_limits',
                    predecessor_manifest=prior.MANIFEST,documents=documents(),
                    author_review=AUTHOR,visual_review=VISUAL,source_review=SOURCE,
                    continuation_state=STATE,
                    scope='Separate selected linked-outcome funding research; no general calibration, independent approval, bank validation, deployment or economics qualification.',
                    verification='python3 tools/linked_funding_delivery.py verify',artifacts=artifacts)
    path = ROOT/MANIFEST
    temporary = path.with_suffix('.json.tmp')
    temporary.write_text(json.dumps(manifest,indent=2)+'\n')
    temporary.replace(path)
    print(json.dumps(dict(status='frozen',artifacts=len(artifacts),documents=documents()),indent=2))


def verify():
    author = gates()
    manifest = read(MANIFEST)
    require(manifest['version'] == '2026-10-11-linked-funding' and
            manifest['status'] == 'author_reviewed_with_stated_limits' and
            manifest['predecessor_manifest'] == prior.MANIFEST and manifest['documents'] == documents(),
            'Wrong delivery manifest')
    paths = [r['path'] for r in manifest['artifacts']]
    require(len(paths) == len(set(paths)) and set(paths) == artifact_names(author),
            'Missing or duplicate manifest member')
    for r in manifest['artifacts']:
        require(sha(r['path']) == r['sha256'] and (ROOT/r['path']).stat().st_size == r['bytes'],
                'Changed frozen artifact: '+r['path'])
    print(json.dumps(dict(status='pass',version=manifest['version'],artifacts=len(paths),
                          prior_manifests_verified=3,issues=[],
                          scope='Local file identity and recorded evidence, not independent science or bank validation.'),indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command',choices=['prepare','check','freeze','verify'])
    try:
        command = parser.parse_args().command
        if command == 'prepare': prepare()
        elif command == 'freeze': freeze()
        elif command == 'verify': verify()
        else:
            gates()
            print('Linked-funding delivery gates pass with stated limits.')
    except (ValueError,KeyError,OSError,zipfile.BadZipFile,subprocess.CalledProcessError) as error:
        raise SystemExit(str(error))
