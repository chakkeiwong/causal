#!/usr/bin/env python3
"""Audit the active foundations draft without requalifying withdrawn deliveries."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads((ROOT / path).read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inspect_receipt(name, issues):
    receipt = read(name)
    if receipt.get('status') != 'pass' or not receipt.get('input_sha256'):
        issues.append('Missing passing verification/input manifest: ' + name)
    for path, expected in receipt.get('input_sha256', {}).items():
        file = ROOT / path
        if not file.is_file() or digest(file) != expected:
            issues.append('Stale verification input: ' + name + '/' + path)
    return {'path': name, 'sha256': digest(ROOT / name),
            'input_sha256': receipt.get('input_sha256', {}),
            'scope': receipt.get('scope')}


def main():
    issues = []
    sources = {x['id']: x for x in read('docs/literature/sources.json')}
    notes = read('docs/literature/reading-notes.json')
    claims = read('docs/literature/reconstruction-claims.json')
    matrix = read('docs/literature/source-question-matrix.json')
    revision = read('docs/program/state.json').get('revision')
    checks = read('docs/reviews/precision-exact-replay.json' if revision == '10.0-precision-streaming' else 'docs/reviews/calibration-exact-replay.json' if revision == '9.0-calibration-completion' else 'docs/reviews/reliability-exact-replay.json' if revision == '8.0-reliability-extension' else 'docs/reconstruction/checks.json')
    files = [ROOT / 'docs/causal_foundations.tex'] + sorted((ROOT / 'docs/reconstruction').glob('*.tex'))
    sponsor = ROOT / 'docs/sponsor_reconstruction.tex'
    if sponsor.is_file():
        files.append(sponsor)
    # Generated tables carry labels too. Follow actual local TeX inputs instead
    # of mistaking their valid references for unresolved manuscript anchors.
    seen = set(files)
    for path in files:
        raw = re.sub(r'(?m)(?<!\\)%.*$', '', path.read_text())
        for name in re.findall(r'\\(?:input|include)\{([^}]+)\}', raw):
            included = ROOT / 'docs' / (name if name.endswith('.tex') else name+'.tex')
            if included.is_file() and included not in seen:
                seen.add(included)
                files.append(included)
    revision = read('docs/program/state.json').get('revision')
    verification_names = ('docs/reviews/precision-verification.json',) if revision == '10.0-precision-streaming' else ('docs/reviews/calibration-verification.json',) if revision == '9.0-calibration-completion' else ('docs/reviews/reliability-verification.json',) if revision == '8.0-reliability-extension' else ('docs/reviews/closure-verification.json',) if revision == '7.0-gap-closure' else (
        'docs/reviews/revision-verification.json',
        'docs/reviews/scientific-contract-checks.json',
        'docs/reviews/scientific-completion-verification.json',
        'docs/reviews/scope-verification.json',
        'docs/reviews/dynamic-verification.json',
        'docs/reviews/linkage-verification.json')
    verification = [inspect_receipt(name, issues) for name in verification_names]
    build_receipt = inspect_receipt('docs/reviews/reconstruction-build.json', issues)
    for document in read('docs/reviews/reconstruction-build.json')['documents']:
        if digest(ROOT / document['path']) != document['sha256']:
            issues.append('Built PDF bytes changed: ' + document['path'])
    verified_inputs = {}
    for receipt in verification:
        verified_inputs.update(receipt['input_sha256'])
        verified_inputs[receipt['path']] = receipt['sha256']
    cited, labels, refs = set(), set(), set()
    document_citations = {'causal_foundations': set(), 'sponsor_reconstruction': set()}
    occurrences = []
    for path in files:
        raw = re.sub(r'(?m)(?<!\\)%.*$', '', path.read_text())
        labels.update(re.findall(r'\\label\{([^}]+)\}', raw))
        refs.update(re.findall(r'\\(?:ref|eqref)\{([^}]+)\}', raw))
        for match in re.finditer(r'\\cite\w*\*?(?:\[[^\]]*\])*\{([^}]+)\}', raw):
            for key in match.group(1).split(','):
                key = key.strip()
                cited.add(key)
                document_citations['sponsor_reconstruction' if path == sponsor else 'causal_foundations'].add(key)
                occurrences.append({'id': key, 'path': str(path.relative_to(ROOT)),
                                    'line': raw[:match.start()].count('\n') + 1})
    if refs - labels:
        issues.append('Unresolved manuscript labels: ' + str(sorted(refs - labels)))
    trace = []
    mapped = set()
    for claim in claims:
        if claim['manuscript_anchor'] not in labels:
            issues.append('Missing claim anchor: ' + claim['id'])
        mapped.update(claim['sources'])
        for name in claim.get('checks', []):
            if name not in checks['checks']:
                issues.append('Missing named check: ' + claim['id'] + '/' + name)
        artifact_evidence = []
        for path in claim.get('artifacts', []):
            file = ROOT / path
            if not file.is_file():
                issues.append('Missing claim artifact: ' + claim['id'] + '/' + path)
                continue
            actual = digest(file)
            if path not in verified_inputs or verified_inputs[path] != actual:
                issues.append('Claim artifact lacks current verification binding: ' + claim['id'] + '/' + path)
            artifact_evidence.append({'path': path, 'sha256': actual,
                                      'verification_receipts': [r['path'] for r in verification
                                          if path == r['path'] or path in r['input_sha256']]})
        trace.append({**claim, 'artifact_evidence': artifact_evidence, 'source_evidence': [
            {k: sources[s][k] for k in ('id', 'local_path', 'sha256', 'version_status', 'inspected', 'limits')}
            for s in claim['sources'] if s in sources]})
    if cited - mapped:
        issues.append('Citations without reconstruction claim mapping: ' + str(sorted(cited - mapped)))
    copies = []
    for key in sorted(cited | mapped):
        if key not in sources:
            issues.append('Unregistered source: ' + key)
            continue
        s = sources[key]
        p = ROOT / s['local_path']
        if not p.is_file() or digest(p) != s['sha256']:
            issues.append('Missing or changed source copy: ' + key)
            continue
        if s['kind'] == 'paper':
            expected = f"{s['filename_title']} {s['first_author']}({s['year']}).pdf"
            if p.parent != ROOT / 'docs/papers' or p.name != expected or p.read_bytes()[:5] != b'%PDF-':
                issues.append('Paper filename/content mismatch: ' + key)
            if s['inspected'] != notes[key]['inspected']:
                issues.append('Catalog has stale inspection notes: ' + key)
        if s['kind'] == 'software':
            snapshot = json.loads(p.read_text())
            for a in snapshot['artifacts']:
                nested = ROOT / a['path']
                if not nested.is_file() or digest(nested) != a['sha256']:
                    issues.append('Software artifact changed: ' + key + '/' + a['path'])
            qualification = snapshot.get('scientific_qualification')
            if not qualification:
                issues.append('Software lacks mathematical qualification: ' + key)
            else:
                if qualification['runtime_status'] != 'not_run':
                    issues.append('Unexpected runtime promotion in document-only review: ' + key)
                for e in qualification['evidence']:
                    nested = ROOT / e['path']
                    if not nested.is_file() or digest(nested) != e['sha256']:
                        issues.append('Software inspection copy changed: ' + key)
                        continue
                    first, last = e['lines']
                    excerpt = '\n'.join(nested.read_text().splitlines()[first-1:last])
                    if hashlib.sha256(excerpt.encode()).hexdigest() != e['excerpt_sha256']:
                        issues.append('Software inspection anchor changed: ' + key)
                    receipt = e.get('retrieval_receipt')
                    if receipt and digest(ROOT / receipt['path']) != receipt['sha256']:
                        issues.append('Software retrieval receipt changed: ' + key)
        if not s['inspected'] or not s['claims']:
            issues.append('Empty source inspection/claim record: ' + key)
        if s['kind'] == 'documentation':
            for artifact in s.get('artifacts', []):
                nested = ROOT / artifact['path']
                if not nested.is_file() or digest(nested) != artifact['sha256']:
                    issues.append('Installed documentation/source copy changed: ' + key + '/' + artifact['path'])
        copies.append({'id': key, 'path': s['local_path'], 'sha256': s['sha256']})
    if [r['id'] for r in matrix['domains']] != list(range(1, 15)):
        issues.append('Theory matrix does not cover 14 ordered domains')
    for row in matrix['domains']:
        for source in row['sources']:
            if source['id'] not in sources:
                issues.append('Matrix source is unregistered: ' + source['id'])
        if not row['remaining']:
            issues.append('Missing domain limitations: ' + str(row['id']))

    for path, expected in checks['input_sha256'].items():
        if digest(ROOT / path) != expected:
            issues.append('Exact-check input changed: ' + path)
    if checks['status'] != 'pass':
        issues.append('Exact checks failed')
    documents = []
    for stem, expected_keys in document_citations.items():
        if stem == 'sponsor_reconstruction' and not sponsor.is_file():
            continue
        build = ROOT / 'docs/build' / stem
        aux = build.with_suffix('.aux').read_text()
        bibkeys = set(re.findall(r'\\bibitem(?:\[[^]]*\])?\{([^}]+)\}', build.with_suffix('.bbl').read_text()))
        auxkeys = {k.strip() for block in re.findall(r'\\citation\{([^}]+)\}', aux) for k in block.split(',')}
        if bibkeys != expected_keys or auxkeys != expected_keys:
            issues.append('Compiled bibliography and manuscript citation sets differ: ' + stem)
        findings = re.findall(r'(?m)^.*(?:Overfull|LaTeX Warning|Package \S+ Warning|Class \S+ Warning|undefined).*$',
                              build.with_suffix('.log').read_text())
        issues.extend(stem + ': ' + finding for finding in findings)
        blg = build.with_suffix('.blg').read_text()
        if 'Warning--' in blg or 'error message' in blg:
            issues.append('BibTeX warning or error: ' + stem)
        document = ROOT / 'docs' / (stem + '.pdf')
        info = subprocess.run(['pdfinfo', str(document)], check=True, text=True, capture_output=True).stdout
        documents.append({'path': str(document.relative_to(ROOT)), 'sha256': digest(document),
                          'pages': int(re.search(r'(?m)^Pages:\s+(\d+)', info).group(1))})
    pdf = ROOT / 'docs/causal_foundations.pdf'
    info = subprocess.run(['pdfinfo', str(pdf)], check=True, text=True, capture_output=True).stdout
    pages = int(re.search(r'(?m)^Pages:\s+(\d+)', info).group(1))
    acquisition = []
    for key in ('pearl2009', 'angrist1996', 'grf2018', 'rlearner2020', 'drlearner2023', 'snm2014', 'id2006',
                'targeted2018', 'staiger1994', 'hall2005', 'zhang2008', 'perkovic2018',
                'sarkka2013', 'kalouptsidi2021', 'imai2009',
                'pearltransport2014', 'petersicp2016', 'howard2021', 'imbens2002',
                'roysland2024', 'rytgaard2021', 'ryalen2026',
                'blundellbond2023', 'rohekar2023', 'slawski2025', 'zhangprox2024',
                'wei2026', 'casini2025', 'ran2026', 'kleibergen2021', 'gerhardus2021'):
        s = sources[key]
        row = {'id': key, 'original_path': s['original_path'], 'copy': s['local_path'],
               'sha256': s['sha256'], 'accessed': s['accessed']}
        origin = Path(s['original_path'])
        if origin.is_file() and digest(origin) != s['sha256']:
            issues.append('Original differs from preserved new source: ' + key)
        receipt = origin.with_suffix('.receipt.json')
        if receipt.is_file():
            r = json.loads(receipt.read_text())
            if r.get('status') != 'saved' or r.get('sha256') != s['sha256']:
                issues.append('Acquisition receipt mismatch: ' + key)
            row['receipt'] = str(receipt.relative_to(ROOT))
            row['receipt_sha256'] = digest(receipt)
        acquisition.append(row)

    # Keep old claim and delivery audits historical; write scoped current artifacts.
    (ROOT / 'docs/literature/reconstruction-source-trace.json').write_text(json.dumps(
        {'date': read('docs/program/state.json')['updated'], 'claims': trace, 'citation_occurrences': occurrences,
         'new_acquisitions': acquisition, 'verification_receipts': verification,
         'build_receipt': build_receipt}, ensure_ascii=False, indent=2) + '\n')
    lines = ['# Source-to-question matrix', '',
             '9 October 2026. Publication cutoff: 7 October 2026.', '', matrix['scope'], '',
             'Full source identity, preserved path and hashes: [source register](sources.json). '
             'Current claim/anchor trace: [reconstruction-source-trace.json](reconstruction-source-trace.json).', '']
    for row in matrix['domains']:
        lines += [f"## {row['id']}. {row['domain']}", '', row['question'], '',
                  '| Source key | Inspected anchor | Current inspection status |', '|---|---|---|']
        lines += [f"| {s['id']} | {s['anchors']} | {s['inspection']} |" for s in row['sources']]
        lines += ['', '**Draft anchors:** ' + (row['draft'] or 'Not yet reconstructed'), '',
                  '**Remaining scholarship:** ' + row['remaining'], '']
    (ROOT / 'docs/literature/source-question-matrix.md').write_text('\n'.join(lines))
    claimlines = ['# Foundations claim trace', '',
                  'These records separate inherited results, project derivations, finite examples and proposed product behavior. '
                  'They do not certify scholarly sufficiency.', '',
                  '| Claim | Manuscript anchor | Evidence class | Sources / exact checks |', '|---|---|---|---|']
    for c in claims:
        claimlines.append(f"| {c['id']}: {c['claim']} | {c['manuscript_anchor']} | {c['evidence_class']} | "
                          + ', '.join(c['sources'] + c.get('checks', [])) + ' |')
    (ROOT / 'docs/literature/reconstruction-claims.md').write_text('\n'.join(claimlines) + '\n')
    current_receipts = [json.loads(p.read_text()) for p in sorted((ROOT / 'docs/literature/raw').glob('r3*.receipt.json'))]
    (ROOT / 'docs/literature/reconstruction-request-ledger.json').write_text(json.dumps(
        {'date': '2026-10-09', 'records': current_receipts,
         'retry_history': [{'id': 'r3_npiv_metadata', 'initial_status': 'HTTP 429',
                            'subsequent_status': 'saved', 'record_scope': 'The collector overwrote the initial receipt; the initial error is retained as a session observation, not an independently hashed response.'}]},
        indent=2) + '\n')
    result = {'status': 'pass' if not issues else 'fail', 'date': read('docs/program/state.json')['updated'],
              'document': {'path': str(pdf.relative_to(ROOT)), 'sha256': digest(pdf), 'pages': pages},
              'documents': documents,
              'cited_works': len(cited), 'claims': len(claims), 'source_copies': copies,
              'new_preserved_sources': len(acquisition), 'domains_mapped': len(matrix['domains']),
              'exact_checks': checks['status'], 'issues': issues,
              'verification_receipts': [{'path': r['path'], 'sha256': r['sha256']} for r in verification],
              'build_receipt': {'path': build_receipt['path'], 'sha256': build_receipt['sha256']},
              'scope': 'Citation/byte/claim/label/build closure, exact-example and study/component/protocol input receipts; not completeness, general proof verification, independent review or bank qualification.'}
    (ROOT / 'docs/reviews/foundations-audit.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'source_copies'}, indent=2))
    raise SystemExit(bool(issues))


if __name__ == '__main__':
    main()
