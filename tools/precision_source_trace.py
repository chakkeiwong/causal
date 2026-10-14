#!/usr/bin/env python3
"""Bind the V10 source-role review without rewriting the preserved V9 receipt."""
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PRIOR = 'docs/literature/calibration-source-review.json'
CLAIMS = 'docs/literature/reconstruction-claims.json'
PRESERVATION = 'docs/program/history/v9-preservation-receipt.json'


def read(name):
    return json.loads((ROOT / name).read_text())


def digest(name):
    with (ROOT / name).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    preservation = read(PRESERVATION)
    require(digest(preservation['archive']) == preservation['sha256'],
            'Changed V9 archive')
    with zipfile.ZipFile(ROOT / preservation['archive']) as archive:
        prior_bytes = archive.read(PRIOR)
        require(prior_bytes == (ROOT / PRIOR).read_bytes(), 'Changed V9 source review')
        prior = json.loads(prior_bytes)
        for name, expected in prior['input_sha256'].items():
            require(hashlib.sha256(archive.read(name)).hexdigest() == expected,
                    'Stale preserved V9 source-review input: ' + name)
            if name != CLAIMS:
                require(digest(name) == expected, 'Changed inherited source input: ' + name)
        inherited = json.loads(archive.read(CLAIMS))
    claims = read(CLAIMS)
    current = [c for c in claims if c['id'].startswith('J-R')]
    require([c for c in claims if not c['id'].startswith('J-R')] == inherited,
            'Inherited claim records changed')
    require({c['id'] for c in current} == {'J-R01', 'J-R02', 'J-R03'} and len(current) == 3,
            'Missing or duplicate V10 claim groups')
    roles = {'J-R01': ['dml2018'], 'J-R02': [], 'J-R03': ['newey1986']}
    require(all(c['sources'] == roles[c['id']] for c in current), 'Changed source roles')
    inspected = prior['inspected']
    for row in inspected:
        require(digest(row['local_path']) == row['sha256'], 'Changed primary source')
    inputs = set(prior['input_sha256']) | {
        PRIOR, PRESERVATION, 'tools/precision_source_trace.py',
        'docs/reconstruction/24_precision_streaming.tex',
        'docs/reviews/precision-source-excerpts/newey1986-6.png',
    }
    result = dict(
        status='pass', issues=[], date='2026-10-10', revision='10.0',
        publication_cutoff='2026-10-07', inspected=inspected,
        inspection_record='DML local primary-text lines 1590--1658 reread; Newey original PDF page 6 rendered and actually viewed during V10 closeout. Anchors and narrow inherited roles above remain applicable.',
        claims=[c['id'] for c in current], inherited_claims_unchanged=len(inherited),
        project_claims=current,
        source_role_limits={
            'J-R01': 'DML supports the orthogonal score and nuisance-product rate premise. QR equivalence and dependent-calendar rates are project derivations, not consequences of the iid DML theorem.',
            'J-R02': 'Coverage, paired comparisons and failures are this project\'s synthetic evidence. No external paper establishes their finite-sample calibration.',
            'J-R03': 'Newey supports the Bartlett covariance alternative and its positive-semidefinite construction. Untapered horizon covariance, streaming equivalence and local cost measurements are project work.',
        },
        prior_review=PRIOR,
        repair='The V9 receipt binds the V9 claim register and remains historical. This separate receipt binds the current V10 register after source-role review; no prior scientific hash or simulation result is replaced.',
        search_scope='Reinspection of two unchanged registered primary works. No new discovery, version, correction or exhaustive literature search is claimed.',
        scope='Author source-role review and identity checks, not independent proof of project derivations or bank validity.',
        input_sha256={name: digest(name) for name in sorted(inputs)},
    )
    target = ROOT / 'docs/literature/precision-source-review.json'
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print('V10 source-role review bound: two primary works, three current claims; V9 review and inherited claims preserved.')


if __name__ == '__main__':
    main()
