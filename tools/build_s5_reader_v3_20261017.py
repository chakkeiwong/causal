#!/usr/bin/env python3
"""Develop the preserved S5 depth failure without changing its frozen inputs."""
import argparse
from contextlib import redirect_stdout
import json
from pathlib import Path
import re

import audit_reader_traceability_v2_20261013 as trace
import build_java_temporal_engine_20261016 as engine
import build_s5_reader_v2_20261017 as previous
import s5_occupied_error_20261017 as extension
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

ROOT, WORK = previous.ROOT, previous.WORK
BASE = WORK/'publication-v3'
OUT = BASE/'reader'
OLD = previous.DRIVER
CANONICAL_OLD = previous.OLD
PRIOR = previous.OUT/'source-audit.json'
NAME = 'causal_proposal_longitudinal_reviewed_v3_2026-10-17'
DRIVER = ROOT/'docs'/(NAME+'.tex')
PDF = DRIVER.with_suffix('.pdf')
CHAPTER = WORK/'revision-v3/chapter.tex'
EXTENSION = extension.BASE/'development.tex'
INSERT = r'\input{program/execution/2026-10-17/s5/depth-extension/development.tex}'
LABELS = previous.LABELS + ['s5-occupied','s5-transport','s5-validation']


def read(path):
    return json.loads(path.read_text())


def expected_chapter():
    tex = previous.CHAPTER.read_text()
    marker = r'\section{Conclusion}'
    assert tex.count(marker) == 1
    return tex.replace(marker, INSERT+'\n\n'+marker)


def expected_driver():
    book = OLD.read_text()
    marker = r'\input{'+str(previous.CHAPTER.relative_to(ROOT/'docs'))+'}'
    assert book.count(marker) == 1
    book = book.replace(marker,r'\input{'+str(CHAPTER.relative_to(ROOT/'docs'))+'}')
    pattern = re.compile(r'\\bibliography\{([^}]+)\}')
    assert len(pattern.findall(book)) == 1
    return pattern.sub(lambda m:r'\bibliography{'+m.group(1)+',program/execution/2026-10-17/s5/publication-v3/refs}',book)


def prepare():
    assert not BASE.exists() and not DRIVER.exists() and not CHAPTER.exists()
    for p in [previous.BASE/'prepared-inputs.json', previous.OUT/'build-report.json',
              PRIOR, previous.BASE/'traceability-review.json', WORK/'depth-review-initial.json',
              extension.BASE/'mathematics-review.json']:
        verify_bindings(read(p))
    exact=read(extension.BASE/'exact-results.json')
    assert extension.calculate() == exact and extension.separate(exact)['status'] == 'pass'
    tex=EXTENSION.read_text()
    assert not [c for c in tex if ord(c)<32 and c not in '\n\t']
    assert not re.search(r'(?<!\\)\\\n',tex)
    assert r'\chapter{' not in tex
    assert set(re.findall(engine.shared.CITE,tex)) == {'exec17_s5_occupied'}
    BASE.mkdir()
    CHAPTER.parent.mkdir()
    CHAPTER.write_text(expected_chapter())
    assert CHAPTER.read_text().replace(INSERT+'\n\n','') == previous.CHAPTER.read_text()
    claims=[
        'An exact finite-horizon signed continuation-residual identity uses reference occupancy and approximate continuation values under common policy, rewards and initial law.',
        'A three-period competing-event mass shift preserves survival but changes value by20.805USD; full occupied, restricted-support and uniform envelopes are21.05,20.805 and30.299USD.',
        'Validation-law residual transport needs support and an explicit occupancy/L2 factor; a rare-history witness gives1USD validation error versus90USD policy error.',
        'Known occupancies and separately fixed continuation values with genuine independent reference-row draws imply the stated simultaneous finite validation interval.',
        'The longitudinal sum-of-radii budget objective has a conditional continuous2/3-power allocation; feasible integer rounding reduces the stipulated unequal-cost radius from35.1783 to31.4016USD.'
    ]
    limits=read(WORK/'primary-review.json')['limitations']+[
        'Reference occupancy, support restrictions and independent reference transitions are explicit premises, not established bank facts.',
        'The validation intervals are prospective designs; no new sample or measured coverage is reported.',
        'Continuous optimality does not imply exact integer optimality or actual bank validation cost.'
    ]
    source=dict(integrated_citation_key='exec17_s5_occupied',
        title='Occupied-history competing-event error, validation transport and longitudinal audit allocation',
        author='Causal banking proposal',kind='project_derivation',year=2026,
        source_identity='Project-authored finite transition laws and elementary conditional proofs',
        version_date='2026-10-17; author depth-repair successor; inherited cutoff limits retained',
        local_copy=ref(extension.BASE/'exact-results.json','Exact paths, values, envelopes and allocation references'),
        inspected_anchors=claims,supported_claims=claims,
        records=[ref(p,a) for p,a in [
            (EXTENSION,'Connected derivations, conditional interval and examples'),
            (extension.BASE/'mathematics-review.json','Separate geometric/backward/transport/KKT checks'),
            (ROOT/'tools/s5_occupied_error_20261017.py','Exact rational references and separate author checks'),
            (WORK/'depth-extension-plan.md','Reviewed overlap restrictions and sampling premises'),
            (Path(__file__),'Preserving source transformation and build')]],limitations=limits)
    write(BASE/'source-audit.json',dict(cutoff='2026-10-07',sources=[source],
        prior=ref(PRIOR,'711 unchanged candidate source records')))
    (BASE/'refs.bib').write_text('@misc{exec17_s5_occupied,\n author={{Causal banking proposal}},\n title={'+
        engine.shared.escape(source['title'])+'},\n year={2026},\n note={'+
        engine.shared.escape(source['version_date'])+'}\n}\n')
    DRIVER.write_text(expected_driver())
    write(BASE/'extension-author-review.json',dict(status='pass_for_compilation',
        reviewer=dict(name='Codex author/coordinator',kind='author'),findings=claims+[
            'Original v2 chapter bytes remain recoverable exactly by removing one inserted input command from the new copy.',
            'The old conclusion follows the extension; original cited mathematics and source claims are unchanged.',
            'Concentration and generic resource-allocation principles already credited elsewhere receive no duplicate depth.',
            'Three missing TeX row terminators were corrected before this source was frozen.'],
        evidence=[ref(p,'Reviewed source or exact evidence') for p in
            [CHAPTER,EXTENSION,extension.BASE/'exact-results.json',
             extension.BASE/'mathematics-review.json',WORK/'depth-review-initial.json',
             WORK/'depth-extension-plan.md',Path(__file__)]],
        limitations=limits,visual_acceptance=False))
    write(BASE/'prepared-inputs.json',dict(
        inputs=[ref(p,'Preserved or reviewed input') for p in
                [OLD,PRIOR,previous.CHAPTER,EXTENSION,previous.OUT/'build-report.json',
                 BASE/'extension-author-review.json',Path(__file__)]],
        generated=[ref(p,'Preserving successor source') for p in
                   [DRIVER,CHAPTER,BASE/'source-audit.json',BASE/'refs.bib']],
        transformation='Insert one extension input before the original conclusion; remove it to recover exact v2 source.',
        credit_policy='Retain10.75 initial exclusive credits; assess new occupied-history, transport and conditional-validation depth, discount generic concentration/allocation framing.',
        visual_acceptance=False))
    progress=WORK/'recovery-depth-progress.json'
    write(progress,dict(finding='Crash-recovered934-page candidate passed integrity/math/text review but failed exclusive depth at10.75 of minimum14; preserving substantive repair prepared.',
        next_action='Compile the prepared S5 v3 successor, inspect all new extracted pages/equations, assess exclusive depth, publish if warranted, and continue the queue.',
        evidence=[ref(p,'Recovery or repair evidence') for p in
                  [WORK/'depth-review-initial.json',WORK/'depth-extension-plan.md',
                   extension.BASE/'mathematics-review.json',BASE/'prepared-inputs.json']]))
    transition('progress','TEXT.DRAFT.S5',progress)
    print(json.dumps(dict(prepared=str(DRIVER.relative_to(ROOT)),expected_records=712)))


def build():
    assert not OUT.exists() and not PDF.exists()
    assert DRIVER.read_text() == expected_driver() and CHAPTER.read_text() == expected_chapter()
    for k,v in dict(BASE=BASE,OUT=OUT,OLD=OLD,NAME=NAME,DRIVER=DRIVER,PDF=PDF,PRIOR_AUDIT=PRIOR).items():
        setattr(engine,k,v)
    with (BASE/'compile-summary.log').open('x') as stream:
        with redirect_stdout(stream):
            engine.build()
    report=read(OUT/'build-report.json')
    aux=(OUT/(NAME+'.aux')).read_text()
    sections={}
    for label in LABELS:
        match=re.search(re.escape('\\newlabel{exec17:'+label+'}{{')+r'[^}]*\}{([0-9]+)',aux)
        assert match,label
        sections[label]=int(match.group(1))
    report.update(pdf=ref(PDF,'Preserving longitudinal/survival working reader'),
        builder=ref(Path(__file__),'Preserving occupied-history depth extension builder'),
        predecessor_pdf=ref(OLD.with_suffix('.pdf'),'Preserved unpublished934-page candidate'),
        canonical_predecessor_pdf=ref(CANONICAL_OLD.with_suffix('.pdf'),'Canonical917-page S4 reader'),
        effect_sections=sections)
    engine.core.write(OUT/'build-report.json',report)
    audited=trace.audit(DRIVER,OUT/'source-audit.json')
    write(BASE/'traceability-review.json',audited)
    assert report['cited_records'] == 712 and report['pages'] > 934
    assert audited['status'] == 'pass' and not audited['issues'] and audited['scholarly_pdfs'] == 187
    print(json.dumps(dict(pages=report['pages'],cited_records=712,sections=sections,
        scholarly_pdfs=187,material_warnings=[w for w in report['warnings'] if 'Underfull' not in w])))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('command',choices=['prepare','build'])
    args=parser.parse_args()
    {'prepare':prepare,'build':build}[args.command]()
