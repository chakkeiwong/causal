#!/usr/bin/env python3
"""Verify LA01 source identities and references without executing source code."""
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / 'docs/program/repair-v12/work/LA01'


def read(p):
    return json.loads(p.read_text())


def verify():
    audit = read(WORK/'source-audit.json')
    issues, checked, pages, papers = [], 0, 0, 0
    for source in audit['sources']:
        refs = source.get('local_sources', []) if source['kind'] != 'paper' else [
            {'path': source['local_path'], 'sha256': source['sha256']}]
        for ref in refs:
            p = ROOT/ref['path']
            checked += 1
            if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest() != ref['sha256']:
                issues.append('source hash ' + ref['path'])
        if source['kind'] != 'paper':
            continue
        papers += 1
        p = ROOT/source['local_path']
        expected = f"{source['filename_title']} {source['first_author']}({source['year']}).pdf"
        if p.name != expected or not p.read_bytes().startswith(b'%PDF-'):
            issues.append('paper identity ' + source['id'])
        normalize = lambda s: re.sub(r'[^\w]', '', s).casefold()
        if normalize(source['filename_title']) != normalize(source['title']):
            issues.append('filename/title mismatch ' + source['id'])
        text = (ROOT/source['extracted_text']).read_text()
        if source['arxiv_version'] not in text.split('\f')[0]:
            issues.append('version stamp ' + source['id'])
        info = subprocess.check_output(['pdfinfo', str(p)], text=True)
        n = int(re.search(r'^Pages:\s+(\d+)', info, re.M).group(1))
        pages += n
        if n != source['pages']:
            issues.append('page count ' + source['id'])
        for anchor in source['anchors']:
            if isinstance(anchor, dict) and 'pdf_page' in anchor and not 1 <= anchor['pdf_page'] <= n:
                issues.append('page anchor ' + source['id'])
        date = source.get('version_date', source.get('updated', ''))[:10]
        if not date or date > '2026-10-07':
            issues.append('cutoff ' + source['id'])
    mapping = read(WORK/'literature-map.json')
    contract = read(ROOT/'docs/program/repair-v12/coverage-contract.json')
    if {x['id'] for x in mapping['task_families']} != {x['id'] for x in contract['llm_tasks']}:
        issues.append('family coverage')
    screening = read(WORK/'screening-decisions.json')
    candidates = read(WORK/'screening-candidates.json')
    if len(screening['decisions']) != len(candidates) or len({x['candidate_id'] for x in screening['decisions']}) != len(candidates):
        issues.append('screening identities')
    ids = {x['id'] for x in audit['sources']}
    for row in screening['decisions']:
        if row.get('source_id') and row['source_id'] not in ids:
            issues.append('screening source link')
    for row in mapping['task_families']:
        if not set(row['source_ids']) <= ids:
            issues.append('family source links ' + row['id'])
    for row in read(WORK/'search-ledger.json')['searches']:
        for key in ['receipt', 'local_copy']:
            ref = row.get(key)
            if ref and hashlib.sha256((ROOT/ref['path']).read_bytes()).hexdigest() != ref['sha256']:
                issues.append('search hash ' + row['id'])
    manifest = ROOT/'docs/literature/fetch-manifest.json'
    if hashlib.sha256(manifest.read_bytes()).hexdigest() != 'c86a5ff3f9a4b5ecab80e26698da8ba8a641ffca70a640e5508fca187872533d':
        issues.append('frozen collector manifest')
    out = {'status': 'pass' if not issues else 'fail', 'issues': issues,
           'source_records': len(audit['sources']), 'source_files_hashed': checked,
           'genuine_papers': papers, 'paper_pages': pages, 'task_families': len(mapping['task_families']),
           'screened_candidates': len(screening['decisions']), 'screening_counts': screening['counts'],
           'scope': 'Source bytes, PDF names/version stamps/page ranges, recorded dates, family and screening links. Author review supplies scholarly judgments; no runtime or visual qualification.'}
    (WORK/'verification.json').write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps(out))
    return bool(issues)


if __name__ == '__main__':
    raise SystemExit(verify())
