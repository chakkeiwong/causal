#!/usr/bin/env python3
"""Preserve earlier audits and admit explicitly identified versioned originals.

All bytes, canonical names and resolved locations remain checked. This adds
only docs/papers/versions/arxiv-IDvN/ for an explicitly matched source identity.
"""
from pathlib import Path
import re
import audit_reader_traceability_v2_20261013 as previous

shared = previous.prior.shared
ROOT, DOCS = shared.ROOT, shared.DOCS


def verify_refs(value):
    if isinstance(value, dict):
        name = value.get('local_path', value.get('path'))
        if not name and isinstance(value.get('local_copy'), str):
            name = value['local_copy']
        if name and value.get('sha256'):
            path = ROOT / name
            if not path.is_file() or shared.sha(path) != value['sha256']:
                raise ValueError('Source bytes changed or unavailable: ' + str(path))
        if value.get('kind') == 'paper' and value.get('local_path'):
            path = ROOT / value['local_path']
            papers = (DOCS / 'papers').resolve()
            resolved = path.resolve()
            assert resolved.is_relative_to(papers), path
            relative = resolved.relative_to(papers)
            if len(relative.parts) != 1:
                assert len(relative.parts) == 3 and relative.parts[0] == 'versions', path
                folder = relative.parts[1]
                assert re.fullmatch(r'arxiv-[0-9]{4}\.[0-9]{4,5}v[1-9][0-9]*', folder), path
                version = folder.removeprefix('arxiv-')
                assert value.get('source_identity') in {
                    'https://arxiv.org/abs/' + version,
                    'https://arxiv.org/pdf/' + version,
                }, 'Version directory requires exact original identity'
                assert version in value.get('version_date', ''), 'Version date must name selected original'
            assert path.read_bytes().startswith(b'%PDF-'), path
            assert path.name == f"{value['filename_title']} {value['first_author']}({value['year']}).pdf", path
        for child in value.values():
            verify_refs(child)
    elif isinstance(value, list):
        for child in value:
            verify_refs(child)


def audit(driver, source_audit):
    original = shared.verify_refs
    shared.verify_refs = verify_refs
    try:
        result = previous.audit(driver, source_audit)
    finally:
        shared.verify_refs = original
    result['versioned_original_policy'] = {
        'location': 'docs/papers/versions/arxiv-IDvN/Title FirstAuthorSurname(year).pdf',
        'requirements': ['Full SHA-256', 'Resolved containment', 'Canonical basename',
                         'Exact arXiv identity/version', 'Genuine PDF header'],
        'earlier_versions_preserved': True,
        'semantic_or_visual_acceptance': False,
    }
    return result
