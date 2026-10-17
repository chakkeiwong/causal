#!/usr/bin/env python3
"""Build a preserving constraint-aware S7 depth successor."""
import argparse
from contextlib import redirect_stdout
import json
from pathlib import Path
import re

import audit_reader_traceability_v2_20261013 as trace
import build_java_temporal_engine_20261016 as engine
import build_s7_reader_20261017 as previous
import s7_depth_extension_20261017 as extension
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

ROOT, WORK = previous.ROOT, previous.WORK
BASE = WORK/'publication-v2'
OUT = BASE/'reader'
OLD = previous.DRIVER
CANONICAL_OLD = previous.OLD
PRIOR = previous.OUT/'source-audit.json'
NAME = 'causal_proposal_observation_reviewed_v2_2026-10-17'
DRIVER = ROOT/'docs'/(NAME+'.tex')
PDF = DRIVER.with_suffix('.pdf')
CHAPTER = BASE/'chapter.tex'
EXTENSION = extension.BASE/'development.tex'
INSERT = r'\input{program/execution/2026-10-17/s7/depth-extension/development.tex}'
LABELS = previous.LABELS+['s7-constraint-design','s7-noisy-pool']


def read(path):
    return json.loads(path.read_text())


def expected_chapter():
    text=previous.CHAPTER.read_text()
    marker=r'\section{Conclusion}'
    assert text.count(marker)==1
    return text.replace(marker,INSERT+'\n\n'+marker)


def expected_driver():
    text=OLD.read_text()
    marker=r'\input{'+str(previous.CHAPTER.relative_to(ROOT/'docs'))+'}'
    assert text.count(marker)==1
    text=text.replace(marker,r'\input{'+str(CHAPTER.relative_to(ROOT/'docs'))+'}')
    pattern=re.compile(r'\\bibliography\{([^}]+)\}')
    assert len(pattern.findall(text))==1
    return pattern.sub(lambda m:r'\bibliography{'+m.group(1)+
        ',program/execution/2026-10-17/s7/publication-v2/refs}',text)


def prepare():
    assert not BASE.exists() and not DRIVER.exists()
    for path in [previous.BASE/'prepared-inputs.json',previous.OUT/'build-report.json',
                 PRIOR,previous.BASE/'traceability-review.json',WORK/'depth-review-initial.json',
                 extension.BASE/'mathematics-review.json']:
        verify_bindings(read(path))
    previous.verify_exact()
    exact=read(extension.BASE/'exact-results.json')
    assert extension.calculate()==exact and extension.separate(exact)['status']=='pass'
    text=EXTENSION.read_text()
    assert not [c for c in text if ord(c)<32 and c not in '\n\t']
    assert not re.search(r'(?<!\\)\\\n',text)
    assert r'\chapter{' not in text
    assert set(re.findall(engine.shared.CITE,text))=={'exec17_s7_extension'}
    BASE.mkdir()
    CHAPTER.write_text(expected_chapter())
    assert CHAPTER.read_text().replace(INSERT+'\n\n','')==previous.CHAPTER.read_text()
    claims=[
        'An exact pooled overlap constraint supplies a family of unbiased linear value estimators with coefficient identity a0-3a1=136.',
        'A weighted absolute-value proof globally minimizes a stated common-one-quarter Bernoulli variance envelope over those estimators and continuous price-constrained allocations.',
        'The envelope optimum is4624*min(c0,c1/9)/C, with single-stratum boundary designs and price-ratio-nine transition; this does not claim actual minimax variance or optimum over arbitrary estimators.',
        'Equal-count700 and price(1,4)/budget1820 examples give envelope1156/1575 and4624/4095, compared with28/25 and52/35 for the earlier two-mean designs.',
        'For a noisy pooled moment, target22-(32/3)*tau-(136/3)*theta1 retains pool variance, stratum variance and8704/9 times their covariance.',
        'Twelve explicit finite Bernoulli audit laws reproduce the unbiased means and actual variance, including zero-sample coefficient-zero boundary designs; no sampled qualification study is inferred.'
    ]
    limits=read(WORK/'primary-review.json')['limitations']+[
        'Known pooled information is shared by all incremental audit comparisons; its original acquisition cost is not measured here.',
        'Envelope optimality is restricted to the stated common-one-quarter relaxation, linear unbiased family, independent truthful audits and continuous allocations; integer examples attain their displayed bounds.',
        'Estimated or systematically wrong pooled information has additional covariance, coverage and bias requirements.'
    ]
    source=dict(integrated_citation_key='exec17_s7_extension',
        title='Constraint-aware graph audits and uncertainty in pooled observation information',
        author='Causal banking proposal',kind='project_derivation',year=2026,
        source_identity='Project-authored linear constraint, Bernoulli audit law and incremental budget comparison',
        version_date='2026-10-17; preserving author depth successor; inherited cutoff retained',
        local_copy=ref(extension.BASE/'exact-results.json','Exact coefficient, allocation, budget and covariance references'),
        inspected_anchors=claims,supported_claims=claims,
        records=[ref(path,anchor) for path,anchor in [
            (EXTENSION,'Connected coefficient derivation, global inequality, monetary comparison and noisy-pool limits'),
            (extension.BASE/'mathematics-review.json','Distinct symbolic and finite-enumeration checks'),
            (ROOT/'tools/s7_depth_extension_20261017.py','Reproducible references and separate author checks'),
            (WORK/'depth-extension-plan.md','Reviewed scope, assumptions and duplicate exclusions'),
            (Path(__file__),'Preserving transformation and bounded compilation')]],limitations=limits)
    write(BASE/'source-audit.json',dict(cutoff='2026-10-07',sources=[source],
        prior=ref(PRIOR,'720 unchanged first-candidate source records')))
    (BASE/'refs.bib').write_text('@misc{exec17_s7_extension,\n author={{Causal banking proposal}},\n title={'+
        engine.shared.escape(source['title'])+'},\n year={2026},\n note={'+
        engine.shared.escape(source['version_date'])+'}\n}\n')
    DRIVER.write_text(expected_driver())
    write(BASE/'extension-author-review.json',dict(status='pass_for_compilation',
        reviewer=dict(name='Codex author/coordinator',kind='author'),findings=claims+[
            'Removing the one inserted input recovers every byte of the first-candidate chapter.',
            'The preserved initial exclusive-depth assessment is7.5, below minimum8; new depth remains subject to rendered assessment.',
            'Only the new constraint-aware estimator, joint envelope design and noisy-pool error argument are proposed for additional credit.'],
        evidence=[ref(path,'Reviewed source, exact evidence or retained failure') for path in
            [CHAPTER,EXTENSION,extension.BASE/'exact-results.json',extension.BASE/'mathematics-review.json',
             WORK/'depth-review-initial.json',WORK/'depth-extension-plan.md',Path(__file__)]],
        limitations=limits,visual_acceptance=False))
    write(BASE/'prepared-inputs.json',dict(
        inputs=[ref(path,'Preserved or reviewed input') for path in
            [OLD,PRIOR,previous.CHAPTER,EXTENSION,previous.OUT/'build-report.json',
             BASE/'extension-author-review.json',Path(__file__)]],
        generated=[ref(path,'Preserving successor source') for path in
            [DRIVER,CHAPTER,BASE/'source-audit.json',BASE/'refs.bib']],
        transformation='Insert one development input before the original conclusion in a copy; preserve the initial candidate and depth failure.',
        credit_policy='Retain initial7.5 exclusive equivalents; assess only new constraint-aware audit design and noisy pooled-information propagation after rendering.',
        visual_acceptance=False))
    progress=WORK/'recovery-depth-progress.json'
    write(progress,dict(finding='Recovered975-page candidate passed source/math/text checks but failed exclusive depth at7.5 of minimum8. A preserving constraint-aware audit extension is prepared and exactly checked.',
        next_action='Compile S7 v2; inspect equations, inherited contexts and exclusive8/9/11 depth. Record and publish warranted results, then continue eligible work.',
        evidence=[ref(path,'Recovery or repair evidence') for path in
            [WORK/'depth-review-initial.json',WORK/'depth-extension-plan.md',
             extension.BASE/'mathematics-review.json',BASE/'prepared-inputs.json']]))
    transition('progress','TEXT.DRAFT.S7',progress)
    print(json.dumps(dict(prepared=str(DRIVER.relative_to(ROOT)),expected_records=721)))


def build():
    assert not OUT.exists() and not PDF.exists()
    assert DRIVER.read_text()==expected_driver() and CHAPTER.read_text()==expected_chapter()
    previous.verify_exact()
    assert extension.calculate()==read(extension.BASE/'exact-results.json')
    for key,value in dict(BASE=BASE,OUT=OUT,OLD=OLD,NAME=NAME,DRIVER=DRIVER,
                          PDF=PDF,PRIOR_AUDIT=PRIOR).items():
        setattr(engine,key,value)
    with (BASE/'compile-summary.log').open('x') as stream:
        with redirect_stdout(stream):engine.build()
    report=read(OUT/'build-report.json')
    aux=(OUT/(NAME+'.aux')).read_text()
    sections={}
    for label in LABELS:
        match=re.search(re.escape('\\newlabel{exec17:'+label+'}{{')+r'[^}]*\}{([0-9]+)',aux)
        assert match,label
        sections[label]=int(match.group(1))
    report.update(pdf=ref(PDF,'Preserving constraint-aware observation working reader'),
        driver=ref(DRIVER,'Preserving S7 v2 driver'),builder=ref(Path(__file__),'Bounded depth-successor builder'),
        predecessor_pdf=ref(OLD.with_suffix('.pdf'),'Unpublished975-page first candidate'),
        canonical_predecessor_pdf=ref(CANONICAL_OLD.with_suffix('.pdf'),'Canonical963-page predecessor'),
        effect_sections=sections)
    engine.core.write(OUT/'build-report.json',report)
    audited=trace.audit(DRIVER,OUT/'source-audit.json')
    write(BASE/'traceability-review.json',audited)
    assert report['cited_records']==721 and report['pages']>975
    assert audited['status']=='pass' and not audited['issues'] and audited['scholarly_pdfs']==188
    print(json.dumps(dict(pages=report['pages'],cited_records=721,sections=sections,
        scholarly_pdfs=188,material_warnings=[w for w in report['warnings'] if 'Underfull' not in w])))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=['prepare','build'])
    args=parser.parse_args();{'prepare':prepare,'build':build}[args.command]()
