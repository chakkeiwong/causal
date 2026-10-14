#!/usr/bin/env python3
"""Check source identities and index citation contexts; never award Q2 acceptance."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re

import build_integrated_monograph_v12 as shared

ROOT = shared.ROOT


def first(record, fields):
    return next(((field, record[field]) for field in fields if record.get(field)), (None, None))


def bindings(value):
    found = []
    if isinstance(value, dict):
        name = value.get('local_path') or value.get('path')
        if not name and isinstance(value.get('local_copy'), str):
            name = value['local_copy']
        if name and value.get('sha256'):
            found.append({'path': name, 'sha256': value['sha256']})
        for item in value.values():
            found.extend(bindings(item))
    elif isinstance(value, list):
        for item in value:
            found.extend(bindings(item))
    return found


def audit(driver, source_audit):
    sources = json.loads(source_audit.read_text())
    shared.verify_refs(sources)
    files = shared.scan(driver)
    contexts = {}
    for path, tex in files:
        for match in re.finditer(shared.CITE, tex):
            for key in match.group(1).split(','):
                key = key.strip()
                contexts.setdefault(key, []).append({
                    'path': str(path.relative_to(ROOT)),
                    'line': tex.count('\n', 0, match.start()) + 1,
                    'context': tex[max(0, match.start()-550):match.end()+220]})
    keys = [s['integrated_citation_key'] for s in sources['sources']]
    issues = []
    if len(keys) != len(set(keys)):
        issues.append('Duplicate source audit keys')
    for key in sorted(set(contexts) - set(keys)):
        issues.append('Cited but unaudited: ' + key)
    records = []
    for source in sources['sources']:
        key = source['integrated_citation_key']
        anchor_field, anchors = first(source, ['inspected_anchors', 'inspected', 'anchors'])
        claim_field, claims = first(source, ['supported_claims', 'claims'])
        version_field, version = first(source, ['version_status', 'version_date', 'observed_version',
                                               'arxiv_version', 'commit_date', 'updated'])
        identity_field, identity = first(source, ['source_identity', 'url', 'origin', 'id', 'title'])
        label_field, label = first(source, ['title', 'name', 'repository', 'source_identity', 'url', 'id'])
        refs = bindings(source)
        missing = [name for name, value in [('source_label', label),
                                           ('identity', identity), ('version_date', version),
                                           ('hash_bound_copy', refs), ('anchors', anchors),
                                           ('claims', claims)] if not value]
        if source['kind'] == 'paper' and not source.get('title'):
            missing.append('scholarly_title')
        if missing:
            issues.append(key + ': missing ' + ', '.join(missing))
        records.append({'citation_key': key, 'kind': source['kind'], 'label_field': label_field,
                        'source_label': label,
                        'source_identity_field': identity_field, 'source_identity': identity,
                        'version_field': version_field, 'version_date': version,
                        'local_copies': refs, 'anchor_field': anchor_field, 'anchors': anchors,
                        'claim_field': claim_field, 'supported_claims': claims,
                        'limits': source.get('limits', source.get('adverse_findings_and_limits')),
                        'citation_contexts': contexts.get(key, []),
                        'structural_issues': missing,
                        'semantic_review': 'not_awarded_by_this_check'})
    paper_count = sum(s['kind'] == 'paper' for s in sources['sources'])
    return {'scope': 'Exact-driver source identity, PDF naming/hash, anchor/claim-field presence and citation context index only',
            'status': 'pass' if not issues else 'fail', 'issues': issues,
            'driver': shared.ref(driver, 'Exact reviewed driver'),
            'pdf': shared.ref(driver.with_suffix('.pdf'), 'Exact current compiled reader'),
            'source_audit': shared.ref(source_audit, 'Whole-book source records'),
            'cited_sources': len(contexts), 'audit_records': len(records),
            'scholarly_pdfs': paper_count, 'nonpaper_records': len(records)-paper_count,
            'compiled_files': len({path for path, _ in files}),
            'kind_counts': dict(Counter(s['kind'] for s in sources['sources'])),
            'normalization_note': 'Inherited anchor schemas inspected, inspected_anchors and anchors are equivalent field roles. Software names/repository coordinates and official document URLs are valid identity labels; only scholarly papers require a scholarly title. Project title/id/local copies establish identity without an external URL.',
            'records': records, 'proposal_q2_acceptance': False,
            'limits': ['Field presence and file integrity do not establish that every nearby scientific claim follows from a primary passage.',
                       'No automatic scholarly, implementation, independence, visual or proposal acceptance.',
                       'Literature cutoff and source-specific limitations remain those of each preserved audit.']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--driver', type=Path, required=True)
    parser.add_argument('--audit', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.driver.resolve(), args.audit.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({k: result[k] for k in ['status', 'issues', 'cited_sources', 'scholarly_pdfs',
                                           'nonpaper_records', 'compiled_files', 'proposal_q2_acceptance']}))
