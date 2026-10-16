#!/usr/bin/env python3
"""Preserve recovered S6 inputs and compile an audited successor reader."""
import argparse
from contextlib import redirect_stdout
import json
from pathlib import Path
import re

import audit_reader_traceability_v2_20261013 as trace
import build_java_temporal_engine_20261016 as engine
import prepare_s6_20261017 as work
import s6_robust_panels_20261017 as robust
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT, WORK = work.ROOT, work.BASE
BASE = WORK / 'publication-v1'
OUT = BASE / 'reader'
OLD = ROOT / 'docs/causal_proposal_longitudinal_reviewed_v3_2026-10-17.tex'
PRIOR = work.PRIOR
NAME = 'causal_proposal_panels_reviewed_2026-10-17'
DRIVER = ROOT / 'docs' / (NAME + '.tex')
PDF = DRIVER.with_suffix('.pdf')
ORIGINAL = work.CHAPTER
CHAPTER = BASE / 'chapter.tex'
LABELS = ['s6', 's6-event', 's6-curvature', 's6-donor', 's6-sdid',
          's6-calendar', 's6-feedback', 's6-value', 's6-software',
          's6-prototype', 's6-end']
CORRECTIONS = [
    ('For an ex ante gross-tail tolerance $\\varepsilon>0$ and $0<dr<1$,',
     'If $C=0$, the gross tail is zero at every horizon. For $C>0$, an ex ante\n'
     'gross-tail tolerance $\\varepsilon>0$ and $0<dr<1$,'),
    ('forecast 27 periods from an uninformative short history.',
     'forecast 28 periods (indices $0$ through $27$) from an uninformative short history.')
]


def read(path):
    return json.loads(path.read_text())


def expected_chapter():
    tex = ORIGINAL.read_text()
    for old, new in CORRECTIONS:
        assert tex.count(old) == 1
        tex = tex.replace(old, new)
    return tex


def expected_driver():
    tex = OLD.read_text()
    marker = r'\input{program/execution/2026-10-17/s5/revision-v3/chapter.tex}'
    assert tex.count(marker) == 1
    tex = tex.replace(marker, marker + '\n' + r'\input{' +
                      str(CHAPTER.relative_to(ROOT / 'docs')) + '}')
    pattern = re.compile(r'\\bibliography\{([^}]+)\}')
    assert len(pattern.findall(tex)) == 1
    return pattern.sub(lambda m: r'\bibliography{' + m.group(1) +
                       ',program/execution/2026-10-17/s6/publication-v1/refs}', tex)


def verify_exact():
    for name in ['primary-review.json', 'prototype-design.json', 'source-audit.json',
                 'precompile-author-review.json', 'mathematics-review.json',
                 'robust-mathematics-review.json', 'value-checks/mathematics-review.json']:
        verify_bindings(read(WORK / name))
    exact = read(WORK / 'exact-results.json')
    assert work.examples.calculate() == exact
    assert work.examples.separate(exact)['status'] == 'pass'
    assert robust.calculate() == read(WORK / 'robust-results.json')
    assert work.value.calculate() == read(WORK / 'value-checks/exact-results.json')


def prepare():
    assert not BASE.exists() and not DRIVER.exists()
    verify_bindings(read(PRIOR))
    verify_exact()
    tex = expected_chapter()
    assert tex.count(r'\chapter{') == 1
    assert not re.search(r'(?<!\\)\\\n', tex)
    cited = {k.strip() for g in re.findall(engine.shared.CITE, tex) for k in g.split(',')}
    sources = read(WORK / 'source-audit.json')['sources']
    assert len(sources) == 4
    assert cited <= ({s['integrated_citation_key'] for s in read(PRIOR)['sources']} |
                     {s['integrated_citation_key'] for s in sources})
    BASE.mkdir()
    CHAPTER.write_text(tex)
    write(BASE / 'source-audit.json', dict(sources=sources, cutoff='2026-10-07',
        prior=ref(PRIOR, '712 unchanged source records')))
    bib = []
    for s in sources:
        if s['integrated_citation_key'] == 'sun2021':
            continue  # Genuine paper already has its bibliographic entry.
        bib.append('@misc{' + s['integrated_citation_key'] + ',\n author={{' +
                   engine.shared.escape(s['author']) + '}},\n title={' +
                   engine.shared.escape(s['title']) + '},\n year={2026},\n note={' +
                   engine.shared.escape(s['version_date']) + '}\n}\n')
    (BASE / 'refs.bib').write_text('\n'.join(bib))
    DRIVER.write_text(expected_driver())
    write(BASE / 'copy-author-review.json', dict(status='pass_for_compilation',
        reviewer=dict(name='Codex author/coordinator', kind='author'),
        findings=['Preserve the recovered hash-bound chapter and all earlier evidence.',
                  'State C>0 before dividing by C in the logarithmic horizon condition; C=0 has zero gross tail.',
                  'H=27 includes 28 periods, indexed 0 through 27; correct the following prose.',
                  'Reverse the two recorded substitutions to recover the exact original source.'],
        substitutions=[dict(original=a, successor=b) for a, b in CORRECTIONS],
        evidence=[ref(p, 'Reviewed immutable input or preserving copy') for p in
                  [ORIGINAL, CHAPTER, WORK / 'precompile-author-review.json',
                   WORK / 'value-checks/mathematics-review.json', Path(__file__)]],
        visual_acceptance=False, limitations=work.LIMITS))
    write(BASE / 'prepared-inputs.json', dict(
        inputs=[ref(p, 'Preserved and verified input') for p in
                [OLD, PRIOR, ORIGINAL, WORK / 'plan.md', WORK / 'primary-review.json',
                 WORK / 'prototype-design.json', WORK / 'source-audit.json',
                 WORK / 'precompile-author-review.json', BASE / 'copy-author-review.json',
                 Path(__file__)]],
        generated=[ref(p, 'Preserving successor source') for p in
                   [DRIVER, CHAPTER, BASE / 'source-audit.json', BASE / 'refs.bib']],
        credit_policy='Exclusive S6 panel and time-series development; inherited generic DiD, donor balance, panel moments, inference, sensitivity and CLI catalogs receive no duplicate credit.',
        visual_acceptance=False))
    print(json.dumps(dict(prepared=str(DRIVER.relative_to(ROOT)),
                          expected_records=716, expected_scholarly_pdfs=188)))


def build():
    assert not OUT.exists() and not PDF.exists()
    assert DRIVER.read_text() == expected_driver() and CHAPTER.read_text() == expected_chapter()
    for k, v in dict(BASE=BASE, OUT=OUT, OLD=OLD, NAME=NAME, DRIVER=DRIVER,
                     PDF=PDF, PRIOR_AUDIT=PRIOR).items():
        setattr(engine, k, v)
    with (BASE / 'compile-summary.log').open('x') as stream:
        with redirect_stdout(stream):
            engine.build()
    report = read(OUT / 'build-report.json')
    aux = (OUT / (NAME + '.aux')).read_text()
    sections = {}
    for label in LABELS:
        match = re.search(re.escape('\\newlabel{exec17:' + label + '}{{') +
                          r'[^}]*\}{([0-9]+)', aux)
        assert match, label
        sections[label] = int(match.group(1))
    report.update(pdf=ref(PDF, 'Preserving panel and time-series working reader'),
                  driver=ref(DRIVER, 'Preserving S6 driver'),
                  builder=ref(Path(__file__), 'Preserving recovery and build'),
                  predecessor_pdf=ref(OLD.with_suffix('.pdf'), '939-page canonical predecessor'),
                  effect_sections=sections)
    engine.core.write(OUT / 'build-report.json', report)
    audited = trace.audit(DRIVER, OUT / 'source-audit.json')
    write(BASE / 'traceability-review.json', audited)
    assert report['cited_records'] == 716 and report['pages'] > 939
    assert audited['status'] == 'pass' and not audited['issues']
    assert audited['scholarly_pdfs'] == 188
    print(json.dumps(dict(pages=report['pages'], cited_records=716, sections=sections,
                          scholarly_pdfs=188, material_warnings=[w for w in report['warnings']
                                                               if 'Underfull' not in w])))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['prepare', 'build'])
    args = parser.parse_args()
    {'prepare': prepare, 'build': build}[args.command]()
