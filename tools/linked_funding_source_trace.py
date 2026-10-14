#!/usr/bin/env python3
"""Bind inspected primary copies to narrowly inherited source roles."""
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def digest(p):
    return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()


def main():
    prior_path = 'docs/reviews/weak-audit-sharpening-source-review.json'
    prior = json.loads((ROOT/prior_path).read_text())
    for p,h in prior['input_sha256'].items():
        if digest(p) != h: raise ValueError('Changed inherited source audit: '+p)
    manuscript = 'docs/supplements/linked_funding_2026-10-11.tex'
    citations = re.findall(r'\\cite\{([^}]+)\}',(ROOT/manuscript).read_text())
    if set(citations) != {'dml2018','newey1986'}: raise ValueError('Unreviewed citation')
    sources = prior['cited_primary_works']
    for source in sources:
        p = source['local_path']
        if digest(p) != source['sha256'] or (ROOT/p).read_bytes()[:5] != b'%PDF-':
            raise ValueError('Changed primary PDF: '+p)
    paths = [prior_path, manuscript, 'tools/linked_funding_source_trace.py',
             'docs/literature/sources.json','docs/literature/text/dml2018.txt',
             'docs/reviews/precision-source-excerpts/newey1986-6.png']+[s['local_path'] for s in sources]
    result = dict(status='pass',date='2026-10-11',issues=[],publication_cutoff='2026-10-07',
                  cited_primary_works=sources,
                  inspected_this_continuation=[
                      'DML Section 4.1, equation (4.4), Assumption 4.1(ii), local primary-text extraction lines 1588--1658.',
                      'Newey--West April 1986 original, PDF page 6/printed page 4, Bartlett weights and Theorem 1; scanned source page actually viewed.'],
                  project_claims=[
                      'LF-R01: sampled linked-outcome expectation identity and extension to the selected funding calendar are project derivations.',
                      'LF-R02: diagonal extra audit variance, horizon filtration, fixed-pilot rates and numerical safeguards are conditional project arguments, not the iid DML theorem.',
                      'LF-R03: 4800 fresh paired requests are selected synthetic evidence, not source-derived guarantees.',
                      'LF-R04: wrong-inclusion/label/exogeneity bias and the symbolic precision-price planning boundary are project algebra.'],
                  search_scope='Existing two primary copies reinspected. No new discovery, correction or version search; client cutoff 2026-10-07.',
                  scope='Traceable scholarly claim roles, not independent scientific or bank validation.',
                  input_sha256={p:digest(p) for p in paths})
    (ROOT/'docs/reviews/linked-funding-source-review.json').write_text(json.dumps(result,indent=2)+'\n')
    print('Linked funding source roles verified against two genuine primary PDFs.')


if __name__ == '__main__': main()
