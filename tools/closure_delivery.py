#!/usr/bin/env python3
"""Bind the executed V7 scope only after current author/evidence/image gates."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / 'docs/program/reconstruction-delivery-manifest.json'
REVIEW = 'docs/reviews/gap-closure-author-review-2026-10-10.json'


def read(name):
    return json.loads((ROOT / name).read_text())


def digest(name):
    with (ROOT / name).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check_hashes(mapping, context):
    for name, expected in mapping.items():
        require(digest(name) == expected, f'{context}: changed {name}')


def receipt(name, status='pass'):
    result = read(name)
    require(result.get('status') == status, 'Failed receipt: ' + name)
    require(not result.get('issues'), 'Unresolved issues: ' + name)
    check_hashes(result.get('input_sha256', {}), name)
    return result


def gates():
    state = read('docs/program/state.json')
    require(state['revision'] == '7.0-gap-closure', 'Not the V7 revision')
    phases = [p for p in state['phases'] if p['id'].startswith('C')]
    require({p['id'] for p in phases} == {f'C{i:02d}' for i in range(9)}, 'Missing C phases')
    for phase in state['phases']:
        require(phase['status'] == ('complete' if phase in phases else 'historical'),
                'Incorrect phase status: ' + phase['id'])
        if phase in phases:
            require(phase['evidence'] and all((ROOT / p).is_file() for p in phase['evidence']),
                    'Missing phase evidence: ' + phase['id'])
    for name in ('docs/reviews/closure-verification.json',
                 'docs/reviews/reconstruction-build.json', 'docs/reconstruction/checks.json',
                 'docs/literature/closure-source-review.json',
                 'docs/literature/closure-runtime-audit.json', 'docs/program/consistency-check.json'):
        receipt(name)
    audit = receipt('docs/reviews/foundations-audit.json')
    for row in audit['verification_receipts'] + [audit['build_receipt']] + audit['source_copies']:
        check_hashes({row['path']: row['sha256']}, 'Source/build audit')
    sources = read('docs/literature/sources.json')
    check_hashes({s['local_path']: s['sha256'] for s in sources}, 'Registered sources')
    review = receipt(REVIEW, 'author_reviewed_with_stated_limits')
    require(not review['blocking_findings'], 'Blocking author findings')
    require(set(review['gap_dispositions']) == {f'G{i}' for i in range(1, 7)}, 'Missing gap dispositions')
    for gap in review['gap_dispositions'].values():
        require(gap.get('scholarly') and gap.get('capability') and gap.get('remaining'),
                'Missing separate scholarly/capability judgment')
    visual = receipt('docs/reviews/reconstruction-visual-inspection.json')
    require(not visual['blocking_findings'], 'Blocking visual findings')
    check_hashes(visual['image_sha256'], 'Actually inspected images')
    rendered = {d['pdf']: d for d in read('docs/reviews/foundations-render-receipt.json')}
    inspected = {d['pdf']: d for d in visual['documents']}
    require(set(rendered) == set(inspected) == {d['path'] for d in audit['documents']},
            'Missing rendered/inspected document')
    for document in audit['documents']:
        name = document['path']; seen = inspected[name]; render = rendered[name]
        require(digest(name) == document['sha256'] == seen['sha256'] == render['sha256'],
                'PDF identity differs across gates: ' + name)
        require(document['pages'] == seen['pages'] == render['pages'], 'Page count mismatch')
        require(set(seen['contact_sheets_viewed']) == set(render['contact_sheets']), 'Uninspected sheet')
        require(seen['detail_pages_viewed'] and not seen['blocking_findings'], 'Incomplete detail review')
        require(len(seen['detail_pages_viewed']) == len(seen['detail_images_viewed']), 'Detail image mismatch')
        for image in seen['contact_sheets_viewed'] + seen['detail_images_viewed']:
            require(image in visual['image_sha256'], 'Unbound inspected image: ' + image)
    preservation = receipt('docs/program/history/v6.1-preservation-receipt.json')
    check_hashes({preservation['archive']: preservation['sha256']}, 'Preserved V6.1')
    check_hashes({r['path']: r['sha256'] for r in preservation['existing_immutable_archives']},
                 'Historical immutable archives')
    return state, audit, sources, review, rendered


def freeze():
    state, audit, sources, review, rendered = gates()
    paths = set()
    for pattern in ('README.md', 'AGENTS.md', 'pyproject.toml', '.gitignore',
                    'tools/**/*.py', 'src/**/*.py', 'contracts/**/*', 'security/**/*', 'docs/**/*'):
        paths.update(p for p in ROOT.glob(pattern) if p.is_file()
                     and '__pycache__' not in p.parts and p.suffix not in ('.pyc', '.tmp'))
    paths.discard(TARGET)
    # These inputs are current evidence; old receipts remain historical bytes.
    # Never refresh stale study hashes merely to satisfy this gate.
    artifacts = [dict(path=str(p.relative_to(ROOT)), sha256=digest(p), bytes=p.stat().st_size)
                 for p in sorted(paths)]
    manifest = dict(
        version='7.0', status='author_reviewed_bounded_gap_closure', date='2026-10-10',
        publication_cutoff='2026-10-07', documents=audit['documents'],
        review=review['review'], author_review_receipt=REVIEW,
        program_state='docs/program/state.json',
        rendered_review='docs/reviews/reconstruction-visual-inspection.json',
        source_trace='docs/literature/reconstruction-source-trace.json',
        deferred_obligations='docs/program/deferred-gaps-2026-10-10.md',
        gap_review='docs/reviews/remaining-gaps-v7-2026-10-10.md',
        source_closure=dict(registered_works=len(sources),
                            scholarly_pdfs=sum(s['kind'] == 'paper' for s in sources),
                            active_cited_works=audit['cited_works'], claims=audit['claims']),
        scope=state['completion_scope'],
        verification='python3 tools/delivery_manifest.py verify',
        note='Manifest excludes itself. Current gates validate declared evidence; historical receipts are preserved, not promoted. File identity does not establish independent scientific or bank acceptance.',
        artifacts=artifacts)
    temporary = TARGET.with_suffix('.json.tmp')
    temporary.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    temporary.replace(TARGET)
    print(json.dumps(dict(status='frozen', version='7.0', artifacts=len(artifacts),
                          documents=audit['documents']), indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['check', 'freeze'])
    try:
        if parser.parse_args().command == 'freeze':
            freeze()
        else:
            gates()
            print('Current V7 delivery gates pass.')
    except (ValueError, KeyError, OSError) as error:
        raise SystemExit(str(error))
