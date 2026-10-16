#!/usr/bin/env python3
"""Build a preserving S5 longitudinal/survival successor reader."""
import argparse
from contextlib import redirect_stdout
import json
from pathlib import Path
import re

import audit_reader_traceability_v2_20261013 as trace
import build_java_temporal_engine_20261016 as engine
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
WORK = DOCS / 'program/execution/2026-10-17/s5'
BASE = WORK / 'publication-v2'
OUT = BASE / 'reader'
OLD = DOCS / 'causal_proposal_effects_reviewed_2026-10-17.tex'
PRIOR = DOCS / 'program/execution/2026-10-17/s4/publication-v2/reader/source-audit.json'
NAME = 'causal_proposal_longitudinal_reviewed_v2_2026-10-17'
DRIVER = DOCS / (NAME + '.tex')
PDF = DRIVER.with_suffix('.pdf')
CHAPTER = WORK / 'revision-v2/chapter.tex'
PRIMARY = WORK / 'primary-review.json'
DESIGN = WORK / 'prototype-design.json'
MATH = WORK / 'mathematics-review.json'
PLAN = WORK / 'plan.md'
LABELS = ['s5', 's5-horizon', 's5-selection', 's5-ordered', 's5-natural',
          's5-pushforward', 's5-software', 's5-uncertainty', 's5-error',
          's5-derivative', 's5-joint', 's5-adoption', 's5-end']


def expected_driver():
    book = OLD.read_text()
    marker = r'\input{program/execution/2026-10-17/s4/depth-extension/development.tex}'
    assert book.count(marker) == 1
    book = book.replace(marker, marker + '\n' +
                        r'\input{program/execution/2026-10-17/s5/revision-v2/chapter.tex}')
    pattern = re.compile(r'\\bibliography\{([^}]+)\}')
    assert len(pattern.findall(book)) == 1
    return pattern.sub(lambda m: r'\bibliography{' + m.group(1) +
                       ',program/execution/2026-10-17/s5/publication-v2/refs}', book)


def read(path):
    return json.loads(path.read_text())


def prepare():
    assert not BASE.exists() and not DRIVER.exists()
    prior = read(PRIOR)
    verify_bindings(prior)
    for p in [WORK / 'primary-review.json', WORK / 'prototype-design.json',
              WORK / 'mathematics-review.json', WORK / 'exact-results.json',
              WORK / 'publication-v1/prepared-inputs.json',
              WORK / 'revision-v2/mathematics-review.json']:
        verify_bindings(read(p))
    import s5_examples_20261017 as examples
    exact = read(WORK / 'exact-results.json')
    assert examples.calculate() == exact
    assert examples.separate(exact)['status'] == 'pass'
    import s5_covariance_20261017 as joint
    covariance = read(WORK / 'covariance-results.json')
    assert joint.calculate() == covariance
    assert joint.separate(covariance)['status'] == 'pass'
    tex = CHAPTER.read_text()
    assert r'\chapter{' in tex and tex.count(r'\chapter{') == 1
    assert ',+' not in tex and 'finaladoption' not in tex
    cited = {key.strip() for match in re.findall(engine.shared.CITE, tex)
             for key in match.split(',')}
    prior_keys = {s['integrated_citation_key'] for s in prior['sources']}
    allowed = prior_keys | {'exec17_s5_math', 'exec17_s5_paths', 'exec17_s5_design',
                            'exec17_s5_joint_error'}
    assert cited <= allowed, sorted(cited - allowed)
    BASE.mkdir(parents=True)
    current = read(WORK / 'source-audit.json')
    assert len(current['sources']) == 3
    additions = read(WORK / 'revision-v2/source-audit.json')['sources']
    assert len(additions) == 1
    sources = current['sources'] + additions
    write(BASE / 'source-audit.json', dict(sources=sources,
        prior=ref(PRIOR, '707 preserved source records'), cutoff='2026-10-07'))
    bib = []
    for source in sources:
        bib.append('@misc{' + source['integrated_citation_key'] + ',\n author={{' +
                   engine.shared.escape(source['author']) + '}},\n title={' +
                   engine.shared.escape(source['title']) + '},\n year={' +
                   str(source['year']) + '},\n note={' +
                   engine.shared.escape(str(source['version_date'])) + '}\n}\n')
    (BASE / 'refs.bib').write_text('\n'.join(bib))
    DRIVER.write_text(expected_driver())
    write(BASE / 'prepared-inputs.json', dict(
        inputs=[ref(p, 'Preserved or reviewed input') for p in
                [OLD, PRIOR, CHAPTER, PLAN, PRIMARY, DESIGN, MATH,
                 WORK / 'exact-results.json', WORK / 'covariance-results.json',
                 WORK / 'revision-v2/mathematics-review.json',
                 WORK / 'revision-v2/source-audit.json',
                 WORK / 'draft-review-v1.json',
                 WORK / 'publication-v1/prepared-inputs.json', Path(__file__)]],
        generated=[ref(p, 'Successor source') for p in
                   [DRIVER, BASE / 'source-audit.json', BASE / 'refs.bib']],
        credit_policy='Exclusive S5 longitudinal/survival depth; earlier fixed-policy, basic competing-event, longitudinal-state and software-census material receives no duplicate credit.',
        visual_acceptance=False))
    write(BASE / 'draft-author-review.json', dict(status='pass_for_compilation',
        reviewer={'name': 'Codex author/coordinator', 'kind': 'author'},
        findings=['Connected event-clock, survival, competing-event, modified-policy, support, software-semantics and uncertainty argument.',
                  'Eight original exact families plus joint-event covariance and sharp transition-coupling references reproduce with separate author checks.',
                  'The original uncompiled candidate and its defects are preserved; source and package-semantic corrections occur only in this successor.',
                  'Selected primary source excerpts support software and LMTP claims; package version, rights, runtime and bank qualification limits remain explicit.',
                  'This is proposal evidence and a prospective public/generated design, not an external-estimator or bank experiment.'],
        evidence=[ref(p, 'Reviewed S5 evidence') for p in
                  [CHAPTER, PLAN, PRIMARY, DESIGN, MATH, WORK / 'exact-results.json',
                   WORK / 'covariance-results.json',
                   WORK / 'revision-v2/mathematics-review.json',
                   Path(__file__)]],
        limitations=read(PRIMARY).get('limitations', []), visual_acceptance=False))
    print(json.dumps(dict(prepared=str(DRIVER.relative_to(ROOT)), new_citations=4,
                          original_exact_families=8, added_exact_families=2)))


def build():
    assert not OUT.exists() and not PDF.exists()
    assert DRIVER.read_text() == expected_driver()
    for key, value in dict(BASE=BASE, OUT=OUT, OLD=OLD, NAME=NAME,
                            DRIVER=DRIVER, PDF=PDF, PRIOR_AUDIT=PRIOR).items():
        setattr(engine, key, value)
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
    report.update(pdf=ref(PDF, 'Preserving S5 longitudinal/survival working reader'),
                  driver=ref(DRIVER, 'Preserving S5 driver'),
                  builder=ref(Path(__file__), 'Bounded S5 source/audit builder'),
                  predecessor_pdf=ref(OLD.with_suffix('.pdf'), 'Frozen917-page S4 reader'),
                  effect_sections=sections)
    engine.core.write(OUT / 'build-report.json', report)
    audited = trace.audit(DRIVER, OUT / 'source-audit.json')
    write(BASE / 'traceability-review.json', audited)
    assert audited['status'] == 'pass' and not audited['issues']
    assert report['pages'] > 917 and report['cited_records'] == 711
    assert audited['scholarly_pdfs'] == 187
    print(json.dumps(dict(pages=report['pages'], cited_records=711,
                          sections=sections, scholarly_pdfs=187,
                          material_warnings=[w for w in report['warnings']
                                             if 'Underfull' not in w])))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['prepare', 'build'])
    args = parser.parse_args()
    {'prepare': prepare, 'build': build}[args.command]()
