#!/usr/bin/env python3
"""Check and bind the author-reviewed V8 delivery, including its stated limits."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / 'docs/program/reconstruction-delivery-manifest.json'
REVIEW = 'docs/reviews/reliability-author-review.json'
VISUAL = 'docs/reviews/reconstruction-visual-inspection.json'
RECEIPTS = (
    'docs/reviews/reliability-verification.json',
    'docs/reviews/reliability-exact-replay.json',
    'docs/reviews/reliability-independent-algebra.json',
    'docs/reviews/reliability-local-rehearsal.json',
    'docs/reviews/reliability-table-generation.json',
    'docs/literature/reliability-source-review.json',
    'docs/reviews/reconstruction-build.json',
)


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


def receipt(name, status='pass', bound=True):
    result = read(name)
    require(result.get('status') == status, 'Failed receipt: ' + name)
    require(not result.get('issues'), 'Unresolved issues: ' + name)
    if bound:
        require(result.get('input_sha256'), 'Missing receipt inputs: ' + name)
    check_hashes(result.get('input_sha256', {}), name)
    return result


def gates():
    state = read('docs/program/state.json')
    require(state['revision'] == '8.0-reliability-extension', 'Not the V8 revision')
    current = {f'E{i:02d}' for i in range(8)}
    phases = {p['id']: p for p in state['phases']}
    require(len(phases) == len(state['phases']), 'Duplicate phase IDs')
    require({p for p in phases if p.startswith('E')} == current, 'Missing E phases')
    for name, phase in phases.items():
        require(phase['status'] == ('complete' if name in current else 'historical'),
                'Incorrect phase status: ' + name)
        if name in current:
            require(phase['evidence'] and all((ROOT / p).is_file() for p in phase['evidence']),
                    'Missing phase evidence: ' + name)
            require(set(phase['depends']) <= current and
                    all(phases[p]['status'] == 'complete' for p in phase['depends']),
                    'Incomplete phase prerequisites: ' + name)
    require(state['author_review'] == 'docs/reviews/reliability-author-review.md' and
            state['gap_review'] == 'docs/reviews/remaining-gaps-v8-2026-10-10.md',
            'Stale program review pointers')
    consistency = receipt('docs/program/consistency-check.json', bound=False)
    require(consistency['phases'] == len(phases) and
            consistency['completed_phases'] == len(current) and
            consistency['historical_phases'] == len(phases) - len(current),
            'Stale consistency counts')
    dashboard = (ROOT / 'docs/mission-control.md').read_text()
    require(state['status'] in dashboard and state['next_action'] in dashboard,
            'Stale Mission Control')

    for name in RECEIPTS:
        receipt(name)
    audit = receipt('docs/reviews/foundations-audit.json', bound=False)
    for row in audit['verification_receipts'] + [audit['build_receipt']] + audit['source_copies']:
        check_hashes({row['path']: row['sha256']}, 'Source/build audit')
    sources = read('docs/literature/sources.json')
    check_hashes({s['local_path']: s['sha256'] for s in sources}, 'Registered sources')
    require(consistency['registered_works'] == len(sources), 'Stale source count')

    review = receipt(REVIEW, 'author_reviewed_with_stated_limits')
    require(review['revision'] == '8.0', 'Stale author review')
    require(not review['blocking_findings'], 'Blocking author findings')
    require(set(review['gap_dispositions']) == {f'G{i}' for i in range(1, 7)},
            'Missing gap dispositions')
    for gap in review['gap_dispositions'].values():
        require(all(gap.get(k) for k in ('scholarly', 'capability', 'remaining')),
                'Missing separate scholarly/capability judgment')

    visual = receipt(VISUAL)
    require(visual['revision'] == '8.0' and not visual['blocking_findings'],
            'Stale or blocked visual review')
    check_hashes(visual['image_sha256'], 'Actually inspected images')
    rendered_rows = read('docs/reviews/foundations-render-receipt.json')
    rendered = {d['pdf']: d for d in rendered_rows}
    inspected = {d['pdf']: d for d in visual['documents']}
    reviewed = {d['path']: d for d in review['final_documents']}
    built_rows = read('docs/reviews/reconstruction-build.json')['documents']
    built = {d['path']: d for d in built_rows}
    expected = {'docs/causal_foundations.pdf', 'docs/sponsor_reconstruction.pdf'}
    require(set(rendered) == set(inspected) == set(reviewed) == set(built) ==
            {d['path'] for d in audit['documents']} == expected,
            'Missing delivered document')
    require(all(len(rows) == len(expected) for rows in
                (rendered_rows, visual['documents'], review['final_documents'],
                 built_rows, audit['documents'])), 'Duplicate document identity')
    viewed_images = set()
    for document in audit['documents']:
        name = document['path']
        seen, render, authored = inspected[name], rendered[name], reviewed[name]
        require(digest(name) == document['sha256'] == seen['sha256'] ==
                render['sha256'] == authored['sha256'] == built[name]['sha256'],
                'PDF identity differs across gates: ' + name)
        require(document['pages'] == seen['pages'] == render['pages'] == authored['pages'],
                'Page count mismatch: ' + name)
        require(seen['contact_sheets_viewed'] and
                len(seen['contact_sheets_viewed']) == len(set(seen['contact_sheets_viewed'])) and
                set(seen['contact_sheets_viewed']) == set(render['contact_sheets']),
                'Uninspected or duplicate contact sheet: ' + name)
        pages, images = seen['detail_pages_viewed'], seen['detail_images_viewed']
        require(pages and len(pages) == len(images) == len(set(pages)) and
                len(images) == len(set(images)) and
                all(isinstance(p, int) and 1 <= p <= document['pages'] for p in pages) and
                not seen['blocking_findings'], 'Incomplete detail review: ' + name)
        viewed_images.update(seen['contact_sheets_viewed'] + images)
    require(viewed_images == set(visual['image_sha256']), 'Unbound inspected image')

    preservation = receipt('docs/program/history/v7-preservation-receipt.json', bound=False)
    require(preservation['version'] == '7.0', 'Wrong preservation revision')
    check_hashes({preservation['archive']: preservation['sha256']}, 'Preserved V7')
    check_hashes({r['path']: r['sha256'] for r in preservation['existing_immutable_archives']},
                 'Historical immutable archives')
    with zipfile.ZipFile(ROOT / preservation['archive']) as archive:
        original = archive.read('docs/program/reconstruction-delivery-manifest.json')
        require(hashlib.sha256(original).hexdigest() == preservation['manifest_sha256'],
                'Preserved manifest identity mismatch')
        require(len(json.loads(original)['artifacts']) == preservation['preserved_artifacts'],
                'Preserved artifact count mismatch')
    return state, audit, sources, review


def freeze():
    state, audit, sources, review = gates()
    paths = set()
    for pattern in ('README.md', 'AGENTS.md', 'pyproject.toml', '.gitignore',
                    'tools/**/*.py', 'src/**/*.py', 'contracts/**/*', 'security/**/*', 'docs/**/*'):
        paths.update(p for p in ROOT.glob(pattern) if p.is_file()
                     and '__pycache__' not in p.parts and p.suffix not in ('.pyc', '.tmp'))
    paths.discard(TARGET)
    artifacts = [dict(path=str(p.relative_to(ROOT)), sha256=digest(p), bytes=p.stat().st_size)
                 for p in sorted(paths)]
    manifest = dict(
        version='8.0', status='author_reviewed_reliability_extension_with_stated_limits',
        date='2026-10-10', publication_cutoff='2026-10-07', documents=audit['documents'],
        review=review['review'], author_review_receipt=REVIEW,
        program_state='docs/program/state.json', rendered_review=VISUAL,
        source_trace='docs/literature/reconstruction-source-trace.json',
        current_source_review='docs/literature/reliability-source-review.json',
        deferred_obligations='docs/program/deferred-gaps-2026-10-10.md',
        gap_review='docs/reviews/remaining-gaps-v8-2026-10-10.md',
        external_protocol='docs/program/external-validation-v8.md',
        source_closure=dict(registered_works=len(sources),
                            scholarly_pdfs=sum(s['kind'] == 'paper' for s in sources),
                            active_cited_works=audit['cited_works'], claims=audit['claims']),
        scope=state['completion_scope'],
        verification='python3 tools/delivery_manifest.py verify',
        gate_verification='python3 tools/reliability_delivery.py check',
        note='Manifest excludes itself. Current gates bind declared evidence; historical receipts remain historical. Author completion and file identity do not establish general calibration, independent scientific review, bank validity or adoption.',
        artifacts=artifacts)
    temporary = TARGET.with_suffix('.json.tmp')
    temporary.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    temporary.replace(TARGET)
    print(json.dumps(dict(status='frozen', version='8.0', artifacts=len(artifacts),
                          documents=audit['documents']), indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['check', 'freeze'])
    try:
        if parser.parse_args().command == 'freeze':
            freeze()
        else:
            gates()
            print('Current V8 delivery gates pass; scientific and external limits remain.')
    except (ValueError, KeyError, OSError, zipfile.BadZipFile) as error:
        raise SystemExit(str(error))
