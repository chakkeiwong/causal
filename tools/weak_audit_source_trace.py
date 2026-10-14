#!/usr/bin/env python3
"""Trace the two inherited primary roles in the new research supplement."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRIOR = 'docs/literature/precision-source-review.json'
TARGET = 'docs/reviews/weak-audit-source-review.json'


def read(name):
    return json.loads((ROOT / name).read_text())


def digest(name):
    return hashlib.sha256((ROOT / name).read_bytes()).hexdigest()


def main():
    prior = read(PRIOR)
    if prior['status'] != 'pass' or any(digest(name) != value for name, value in prior['input_sha256'].items()):
        raise ValueError('Historical V10 source-role binding changed')
    registered = {s['id']: s for s in read('docs/literature/sources.json')}
    rows = []
    for source in prior['inspected']:
        item = registered[source['id']]
        path = source['local_path']
        expected_name = f"{item['filename_title']} {item['first_author']}({item['year']}).pdf"
        if (item['local_path'] != path or item['sha256'] != source['sha256']
                or digest(path) != source['sha256'] or Path(path).name != expected_name
                or (ROOT / path).read_bytes()[:5] != b'%PDF-'):
            raise ValueError('Missing or changed original PDF: ' + source['id'])
        rows.append(dict(id=source['id'], title=source['title'], version_status=source['version_status'],
                         local_path=path, sha256=source['sha256'], inspected_anchor=source['anchor'],
                         supported=source['supported'], limit=source['limit']))
    if {row['id'] for row in rows} != {'dml2018', 'newey1986'}:
        raise ValueError('Wrong primary-source set')
    inputs = [PRIOR, 'docs/literature/sources.json',
              'docs/supplements/weak_audit_projection_2026-10-11.tex',
              'tools/weak_audit_source_trace.py'] + [row['local_path'] for row in rows]
    result = dict(status='pass', date='2026-10-11', publication_cutoff='2026-10-07',
                  cited_primary_works=rows,
                  project_claims=[
                      dict(id='WA-R01', evidence='The V9/V10 dependent score and nuisance-rate argument is project work; DML supplies only the inspected orthogonal-score and nuisance-product premise.'),
                      dict(id='WA-R02', evidence='The inherited Bartlett alternative traces to the inspected Newey--West original; the fixed-horizon scalar covariance is project work.'),
                      dict(id='WA-R03', evidence='Exact audit inversion, set projection and rank-one behavior are project derivations and numerical checks, not claims borrowed from the two papers.'),
                      dict(id='WA-R04', evidence='The 3,000-request coverage, width and availability comparisons are newly registered synthetic results, not primary-paper findings.')],
                  search_scope='No new discovery, version or correction search. Reuses and verifies two already inspected original technical copies under their narrow source roles.',
                  scope='Source identity and claim roles for this supplement; not independent proof of the new inference design.',
                  input_sha256={name: digest(name) for name in sorted(inputs)})
    (ROOT / TARGET).write_text(json.dumps(result, indent=2) + '\n')
    print('Supplement source roles: two exact primary PDF copies, four project claim groups.')


if __name__ == '__main__':
    main()
