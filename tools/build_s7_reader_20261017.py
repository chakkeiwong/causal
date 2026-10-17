#!/usr/bin/env python3
"""Build a preserving observation/network/transport proposal reader."""
import argparse
from contextlib import redirect_stdout
import json
from pathlib import Path
import re

import audit_reader_traceability_v2_20261013 as trace
import build_java_temporal_engine_20261016 as engine
import prepare_s7_20261017 as work
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT, WORK = work.ROOT, work.BASE
BASE = WORK/'publication-v1'
OUT = BASE/'reader'
OLD = ROOT/'docs/causal_proposal_panels_reviewed_v2_2026-10-17.tex'
PRIOR = work.PRIOR
NAME = 'causal_proposal_observation_reviewed_2026-10-17'
DRIVER = ROOT/'docs'/(NAME+'.tex')
PDF = DRIVER.with_suffix('.pdf')
CHAPTER = work.CHAPTER
LABELS = ['s7', 's7-question', 's7-overlap', 's7-coordination', 's7-topology',
          's7-pooled', 's7-uncertainty', 's7-audit', 's7-allocation',
          's7-software', 's7-prototype', 's7-end']


def read(path):
    return json.loads(path.read_text())


def expected_driver():
    text = OLD.read_text()
    marker = r'\input{program/execution/2026-10-17/s6/publication-v2/chapter.tex}'
    assert text.count(marker) == 1
    text = text.replace(marker, marker+'\n'+r'\input{'+str(CHAPTER.relative_to(ROOT/'docs'))+'}')
    pattern = re.compile(r'\\bibliography\{([^}]+)\}')
    assert len(pattern.findall(text)) == 1
    return pattern.sub(lambda m: r'\bibliography{'+m.group(1)+
                       ',program/execution/2026-10-17/s7/publication-v1/refs}', text)


def verify_exact():
    for name in ['primary-review.json', 'prototype-design.json', 'source-audit.json',
                 'precompile-author-review.json', 'mathematics-review.json']:
        verify_bindings(read(WORK/name))
    exact = read(WORK/'exact-results.json')
    assert work.examples.calculate() == exact and work.examples.separate(exact)['status'] == 'pass'


def prepare():
    assert not BASE.exists() and not DRIVER.exists()
    verify_bindings(read(PRIOR)); verify_exact()
    chapter = CHAPTER.read_text()
    assert chapter.count(r'\chapter{') == 1
    assert not re.search(r'(?<!\\)\\\n', chapter)
    cited = {k.strip() for group in re.findall(engine.shared.CITE, chapter) for k in group.split(',')}
    sources = read(WORK/'source-audit.json')['sources']
    assert len(sources) == 3
    assert cited <= ({s['integrated_citation_key'] for s in read(PRIOR)['sources']} |
                     {s['integrated_citation_key'] for s in sources})
    BASE.mkdir()
    write(BASE/'source-audit.json', dict(sources=sources, cutoff='2026-10-07',
        prior=ref(PRIOR, '717 unchanged audited records')))
    bibliography = []
    for source in sources:
        bibliography.append('@misc{'+source['integrated_citation_key']+',\n author={{'+
            engine.shared.escape(source['author'])+'}},\n title={'+engine.shared.escape(source['title'])+
            '},\n year={2026},\n note={'+engine.shared.escape(source['version_date'])+'}\n}\n')
    (BASE/'refs.bib').write_text('\n'.join(bibliography))
    DRIVER.write_text(expected_driver())
    write(BASE/'prepared-inputs.json', dict(
        inputs=[ref(p, 'Preserved or reviewed input') for p in
            [OLD, PRIOR, CHAPTER, WORK/'plan.md', WORK/'primary-review.json',
             WORK/'prototype-design.json', WORK/'mathematics-review.json',
             WORK/'precompile-author-review.json', Path(__file__)]],
        generated=[ref(p, 'Preserving successor source') for p in
            [DRIVER, BASE/'source-audit.json', BASE/'refs.bib']],
        transformation='Insert one chapter after S6 and append one bibliography; every inherited chapter remains unchanged.',
        credit_policy='Only new joint observation/exposure/transport and audit-design development; inherited generic observation, transport, sensitivity, catalogs and interfaces are excluded.',
        visual_acceptance=False))
    print(json.dumps(dict(prepared=str(DRIVER.relative_to(ROOT)), expected_records=720)))


def build():
    assert not OUT.exists() and not PDF.exists()
    assert DRIVER.read_text() == expected_driver()
    verify_exact()
    for key, value in dict(BASE=BASE, OUT=OUT, OLD=OLD, NAME=NAME, DRIVER=DRIVER,
                           PDF=PDF, PRIOR_AUDIT=PRIOR).items():
        setattr(engine, key, value)
    with (BASE/'compile-summary.log').open('x') as stream:
        with redirect_stdout(stream):
            engine.build()
    report = read(OUT/'build-report.json')
    aux = (OUT/(NAME+'.aux')).read_text()
    sections = {}
    for label in LABELS:
        match = re.search(re.escape('\\newlabel{exec17:'+label+'}{{')+r'[^}]*\}{([0-9]+)', aux)
        assert match, label
        sections[label] = int(match.group(1))
    report.update(pdf=ref(PDF, 'Preserving observation/network/transport working reader'),
        driver=ref(DRIVER, 'Preserving S7 driver'), builder=ref(Path(__file__), 'Preserving bounded builder'),
        predecessor_pdf=ref(OLD.with_suffix('.pdf'), '963-page canonical predecessor'),
        effect_sections=sections)
    engine.core.write(OUT/'build-report.json', report)
    audited = trace.audit(DRIVER, OUT/'source-audit.json')
    write(BASE/'traceability-review.json', audited)
    assert report['cited_records'] == 720 and report['pages'] > 963
    assert audited['status'] == 'pass' and not audited['issues'] and audited['scholarly_pdfs'] == 188
    print(json.dumps(dict(pages=report['pages'], cited_records=720, sections=sections,
        scholarly_pdfs=188, material_warnings=[w for w in report['warnings'] if 'Underfull' not in w])))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('command', choices=['prepare', 'build'])
    args = parser.parse_args(); {'prepare': prepare, 'build': build}[args.command]()
