#!/usr/bin/env python3
"""Recognize preserved nested inspected-anchor schemas without editing evidence."""
import argparse
import json
from pathlib import Path

import audit_reader_traceability_20261013 as prior


def preserved_anchors(source):
    """Only explicit inspected primary records or hash-bound project anchors."""
    anchors = [r['local_copy'] for r in source.get('records', [])
               if r.get('role') == 'inspected_primary_technical_text'
               and isinstance(r.get('local_copy'), dict)
               and all(r['local_copy'].get(k) for k in ['path', 'sha256', 'anchor'])]
    if anchors:
        return 'records[role=inspected_primary_technical_text].local_copy.anchor', anchors
    copy = source.get('local_copy')
    if source.get('kind', '').startswith('project_') and isinstance(copy, dict) and all(
            copy.get(k) for k in ['path', 'sha256', 'anchor']):
        return 'project.local_copy.anchor', [copy]
    return None, None


def audit(driver, source_audit):
    # The original audit verifies all bound paths/hashes before normalization.
    result = prior.audit(driver, source_audit)
    original_issues = list(result['issues'])
    source_by_key = {s['integrated_citation_key']: s
                     for s in json.loads(source_audit.read_text())['sources']}
    repairs = []
    for row in result['records']:
        if 'anchors' not in row['structural_issues']:
            continue
        field, anchors = preserved_anchors(source_by_key[row['citation_key']])
        if not anchors:
            continue
        row.update(anchor_field=field, anchors=anchors)
        row['structural_issues'].remove('anchors')
        repairs.append({'citation_key': row['citation_key'], 'recognized_field': field,
                        'evidence': anchors})
    schema_keys = set(source_by_key)
    result['issues'] = [x for x in original_issues if x.split(': missing ', 1)[0] not in schema_keys]
    for row in result['records']:
        if row['structural_issues']:
            result['issues'].append(row['citation_key'] + ': missing ' + ', '.join(row['structural_issues']))
    result.update(status='pass' if not result['issues'] else 'fail',
                  predecessor_schema_issues=original_issues, recognized_nested_anchors=repairs,
                  normalization_note=result['normalization_note'] +
                  ' Explicit nested primary inspection records and hash-bound project local-copy anchors are also recognized. No record is edited, missing anchor invented, or semantic acceptance awarded.')
    return result


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--driver', type=Path, required=True)
    p.add_argument('--audit', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    result = audit(args.driver.resolve(), args.audit.resolve())
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': result['status'], 'issues': result['issues'],
                      'recognized_nested_records': len(result['recognized_nested_anchors']),
                      'semantic_acceptance': False}))
