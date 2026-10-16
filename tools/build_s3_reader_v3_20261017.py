#!/usr/bin/env python3
"""Preserve S3 candidates and number the labeled sensitivity displays correctly."""
import argparse
from contextlib import redirect_stdout
import json
from pathlib import Path
import re

import audit_reader_traceability_v2_20261013 as trace
import build_java_temporal_engine_20261016 as engine
import build_s3_reader_v2_20261017 as previous
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT, WORK = previous.ROOT, previous.WORK
BASE = WORK/'publication-v3'
OUT = BASE/'reader'
OLD = previous.DRIVER
PRIOR = previous.OUT/'source-audit.json'
CANONICAL_OLD = previous.candidate.OLD
NAME = 'causal_proposal_identification_reviewed_2026-10-17'
DRIVER = ROOT/'docs'/(NAME+'.tex')
PDF = DRIVER.with_suffix('.pdf')
EXTENSION = BASE/'sensitivity.tex'


def corrected_extension():
    old = previous.EXTENSION.read_text()
    count = 0
    def number(match):
        nonlocal count
        body = match.group(1)
        if r'\label{' not in body:
            return match.group(0)
        count += 1
        return '\\begin{equation}'+body+'\\end{equation}'
    new = re.sub(r'\\\[(.*?)\\\]', number, old, flags=re.S)
    assert count == 5
    return new


def expected_driver():
    book = OLD.read_text()
    old = r'\input{'+str(previous.EXTENSION.relative_to(ROOT/'docs'))+'}'
    new = r'\input{'+str(EXTENSION.relative_to(ROOT/'docs'))+'}'
    assert book.count(old) == 1
    return book.replace(old, new)


def prepare():
    assert not BASE.exists() and not DRIVER.exists()
    for p in [previous.OUT/'build-report.json', PRIOR, previous.BASE/'traceability-review.json']:
        verify_bindings(json.loads(p.read_text()))
    BASE.mkdir()
    EXTENSION.write_text(corrected_extension())
    DRIVER.write_text(expected_driver())
    write(BASE/'source-audit.json', {'cutoff':'2026-10-07', 'sources':[],
        'prior':ref(PRIOR,'703 unchanged scholarly, software and project records')})
    write(BASE/'notation-repair.json', {
        'status':'repaired',
        'finding':'Labels in five unnumbered sensitivity displays inherit section numbers; the product-coupling references therefore point to a section instead of an equation.',
        'repair':'Convert only the five labeled display environments to numbered equation environments. All formula bodies, claims and citations are byte-preserved.',
        'review':'Numbered equation environments are the appropriate LaTeX construct; no mathematical or citation change is needed.',
        'evidence':[ref(previous.EXTENSION,'Preserved original sensitivity derivation'),
                    ref(EXTENSION,'Only five display environments corrected'),
                    ref(previous.OUT/'build-report.json','Preserved 899-page candidate'),
                    ref(Path(__file__),'Exact deterministic transformation')],
        'visual_acceptance':False})
    write(BASE/'prepared-inputs.json', {
        'inputs':[ref(p,'Preserved predecessor or exact notation repair') for p in
                  [OLD, PRIOR, previous.BASE/'prepared-inputs.json', previous.OUT/'build-report.json',
                   previous.BASE/'traceability-review.json', BASE/'notation-repair.json', Path(__file__)]],
        'generated':[ref(p,'Successor source') for p in [DRIVER,EXTENSION,BASE/'source-audit.json']],
        'credit_policy':'Review exclusive substantive pages on the final reader, excluding repeated arguments.',
        'visual_acceptance':False})
    print(json.dumps({'prepared':str(DRIVER.relative_to(ROOT)), 'expected_records':703,'numbered_displays':5}))


def build():
    assert not OUT.exists() and not PDF.exists()
    assert EXTENSION.read_text() == corrected_extension()
    assert DRIVER.read_text() == expected_driver()
    for k,v in {'BASE':BASE,'OUT':OUT,'OLD':OLD,'NAME':NAME,
                'DRIVER':DRIVER,'PDF':PDF,'PRIOR_AUDIT':PRIOR}.items():
        setattr(engine,k,v)
    with (BASE/'compile-summary.log').open('x') as stream:
        with redirect_stdout(stream):
            engine.build()
    report = json.loads((OUT/'build-report.json').read_text())
    aux = (OUT/(NAME+'.aux')).read_text()
    labels = list(json.loads((previous.OUT/'build-report.json').read_text())['identification_sections'])
    sections = {}
    for label in labels:
        match = re.search(re.escape('\\newlabel{exec17:'+label+'}{{')+'[^}]*'+re.escape('}{')+'([0-9]+)',aux)
        assert match, label
        sections[label] = int(match.group(1))
    for label in ['product-coupling','defier-feasible','defier-ratio','defier-sharp','exclusion-outer']:
        match = re.search(re.escape('\\newlabel{exec17:s3-'+label+'}{{')+r'([^}]+)',aux)
        assert match and re.fullmatch(r'20\.\d+',match.group(1)) and int(match.group(1).split('.')[1]) < 13
    report.update(builder=ref(Path(__file__),'Preserving equation-reference repair builder'),
        predecessor_pdf=ref(OLD.with_suffix('.pdf'),'899-page sensitivity candidate preserved'),
        canonical_predecessor_pdf=ref(CANONICAL_OLD.with_suffix('.pdf'),'Published 883-page predecessor preserved'),
        identification_sections=sections)
    engine.core.write(OUT/'build-report.json',report)
    audited=trace.audit(DRIVER,OUT/'source-audit.json')
    write(BASE/'traceability-review.json',audited)
    assert report['cited_records']==703 and report['pages']>=899
    assert audited['status']=='pass' and not audited['issues'] and audited['scholarly_pdfs']==187
    print(json.dumps({'pages':report['pages'],'cited_records':703,'sections':sections,
        'scholarly_pdfs':187,'material_warnings':[w for w in report['warnings'] if 'Underfull' not in w]}))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('command',choices=['prepare','build'])
    args=parser.parse_args()
    {'prepare':prepare,'build':build}[args.command]()
