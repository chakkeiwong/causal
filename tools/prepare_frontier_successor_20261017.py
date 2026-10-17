#!/usr/bin/env python3
"""Preserve the first census reader and repair two inspected wording defects."""
import argparse
import json
from pathlib import Path

import audit_reader_traceability_v2_20261013 as trace
import build_frontier_census_20261017 as previous
import build_java_temporal_engine_20261016 as engine
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = previous.ROOT
BASE = previous.BASE / 'publication-v2'
OUT = BASE / 'reader'
NAME = 'causal_proposal_frontier_census_reviewed_v2_2026-10-17'
DRIVER = ROOT / 'docs' / (NAME + '.tex')
PDF = DRIVER.with_suffix('.pdf')
EXTENSION = BASE / 'frontier.tex'
REPAIRS = [
    ('Substitution of the three rounded rows in Table 4',
     'Substitution for three selected rounded rows in Table 4'),
    ('USD 5, minusUSD 5 or', 'USD 5, minus USD 5 or'),
]


def read(path):
    return json.loads(path.read_text())


def corrected_extension():
    text = previous.EXTENSION.read_text()
    for before, after in REPAIRS:
        assert text.count(before) == 1
        text = text.replace(before, after)
    return text


def expected_driver():
    return previous.DRIVER.read_text().replace(
        str(previous.EXTENSION.relative_to(ROOT / 'docs')),
        str(EXTENSION.relative_to(ROOT / 'docs')))


def prepare():
    assert not BASE.exists() and not DRIVER.exists() and not PDF.exists()
    BASE.mkdir()
    write(BASE / 'candidate-review.json', dict(
        status='revision_required', reviewed_reader=read(previous.OUT / 'build-report.json')['pdf'],
        findings=[
            'Table 4 has five model rows. The exact reference checks three selected rows; the reader must describe that selection explicitly.',
            'Separate minus and USD in the hypothetical value example.'],
        scientific_calculations='Exact values reproduce; no source experiment or denominator is reconstructed.',
        evidence=[ref(previous.EXTENSION, 'Preserved initial text'),
                  ref(previous.BASE / 'candidate137-page-8.txt', 'Five rows of original Table 4'),
                  ref(previous.BASE / 'exact-results.json', 'Three selected rounding checks')],
        final_acceptance=False, visual_acceptance=False))
    EXTENSION.write_text(corrected_extension())
    DRIVER.write_text(expected_driver())
    # Reuse identical audited source records and bibliography; add no citation claim.
    write(BASE / 'source-audit.json', read(previous.BASE / 'source-audit.json'))
    write(BASE / 'prepared-inputs.json', dict(
        inputs=[ref(p, 'Preserved reviewed input') for p in [
            previous.BASE / 'prepared-inputs.json', previous.OUT / 'build-report.json',
            previous.OUT / 'source-audit.json', previous.BASE / 'traceability-review.json',
            previous.BASE / 'primary-review.json', previous.BASE / 'exact-results.json',
            previous.BASE / 'census-register.json', previous.BASE / 'task-map.json',
            previous.BASE / 'citation-chains.json', previous.BASE / 'search-observations.json',
            previous.EXTENSION, BASE / 'candidate-review.json', Path(__file__)]],
        generated=[ref(p, 'Corrected successor input') for p in [DRIVER, EXTENSION, BASE / 'source-audit.json']],
        repairs=REPAIRS, census_closed=False, depth_acceptance=False, visual_acceptance=False))
    print(json.dumps(dict(prepared=str(DRIVER.relative_to(ROOT)), expected_records=735, scholarly_pdfs=191)))


def build():
    verify_bindings(read(BASE / 'prepared-inputs.json'))
    assert DRIVER.read_text() == expected_driver()
    assert EXTENSION.read_text() == corrected_extension()
    assert previous.exact.serial(previous.exact.calculate()) == read(previous.BASE / 'exact-results.json')
    assert not OUT.exists() and not PDF.exists()
    engine.BASE=BASE;engine.OUT=OUT;engine.NAME=NAME;engine.DRIVER=DRIVER;engine.PDF=PDF
    engine.OLD=previous.OLD;engine.PRIOR_AUDIT=previous.PRIOR
    engine.build()
    report=read(OUT / 'build-report.json')
    assert report['cited_records']==735
    index=trace.audit(DRIVER,OUT / 'source-audit.json')
    write(BASE / 'traceability-review.json',index)
    assert index['status']=='pass' and not index['issues'] and index['scholarly_pdfs']==191
    print(json.dumps(dict(pages=report['pages'],records=735,scholarly_pdfs=191,
                          traceability='pass',visual_acceptance=False)))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('command',choices=['prepare','build'])
    args=parser.parse_args()
    {'prepare':prepare,'build':build}[args.command]()
