#!/usr/bin/env python3
"""Preserving S8 successor with explicit cold-recovery purchasing conditions."""
import argparse
from contextlib import redirect_stdout
import json
from pathlib import Path
import re

import audit_reader_traceability_v2_20261013 as trace
import build_java_temporal_engine_20261016 as engine
import build_s8_reader_v2_20261017 as previous
import s8_availability_20261017 as extension
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write

ROOT,WORK=previous.ROOT,previous.WORK
BASE=WORK/'publication-v3'
OUT=BASE/'reader'
OLD=previous.DRIVER
PRIOR=previous.OUT/'source-audit.json'
CANONICAL_OLD=previous.CANONICAL_OLD
NAME='causal_proposal_commercial_gap_reviewed_v3_2026-10-17'
DRIVER=ROOT/'docs'/(NAME+'.tex')
PDF=DRIVER.with_suffix('.pdf')
CHAPTER=BASE/'chapter.tex'
EXTENSION=extension.BASE/'development.tex'
INSERT=r'\input{program/execution/2026-10-17/s8/availability-extension/development.tex}'


def read(path):return json.loads(path.read_text())


def expected_chapter():
    text=previous.CHAPTER.read_text();assert text.count(previous.INSERT)==1
    return text.replace(previous.INSERT,previous.INSERT+'\n'+INSERT)


def expected_driver():
    text=OLD.read_text()
    old=r'\input{program/execution/2026-10-17/s8/publication-v2/chapter.tex}'
    assert text.count(old)==1
    text=text.replace(old,r'\input{program/execution/2026-10-17/s8/publication-v3/chapter.tex}')
    pat=re.compile(r'\\bibliography\{([^}]+)\}')
    return pat.sub(lambda m:r'\bibliography{'+m.group(1)+',program/execution/2026-10-17/s8/publication-v3/refs}',text)


def verify_exact():
    previous.verify_exact()
    exact=read(extension.BASE/'exact-results.json')
    assert extension.calculate()==exact and extension.separate(exact)['status']=='pass'
    verify_bindings(read(extension.BASE/'mathematics-review.json'))


def prepare():
    assert not BASE.exists() and not DRIVER.exists() and not PDF.exists()
    verify_bindings(read(PRIOR));previous.verify_exact()
    assert read(WORK/'depth-review-v2.json')['substantive_page_credit']==9.25
    exact=extension.calculate();checked=extension.separate(exact)
    write(extension.BASE/'exact-results.json',exact)
    write(extension.BASE/'mathematics-review.json',dict(checked,
        reviewer=dict(name='Codex author/coordinator',kind='author'),
        evidence=[ref(p,'Cold-recovery exact or primary input') for p in
            [EXTENSION,extension.BASE/'exact-results.json',ROOT/'tools/s8_availability_20261017.py',
             WORK/'availability-extension-plan.md',WORK/'primary-review.json']],
        limitations=exact['limitations']))
    BASE.mkdir();CHAPTER.write_text(expected_chapter());DRIVER.write_text(expected_driver())
    source=dict(integrated_citation_key='exec17_s8_availability',
        title='Shared validation dependencies and conditional cold-recovery capacity',
        author='Causal banking proposal',kind='project_derivation',year=2026,
        source_identity='Authored finite shared/local readiness law and capacity ceiling',
        version_date='2026-10-17; inherited Bayesia source and2026-10-07 cutoff limits retained',
        local_copy=ref(extension.BASE/'exact-results.json','Exact joint-event readiness probabilities'),
        inspected_anchors=['success','ceiling','target','limitations'],
        supported_claims=['Under stipulated independence, cold-recovery readiness is(1-q)(1-p^m).',
                          'With p0.1 and q0.02, readiness0.882/0.9702/0.97902 and ceiling0.98 cannot meet0.99.',
                          'This law does not describe interruption of already loaded engines or observed vendor availability.'],
        records=[ref(p,'Reviewed derivation, source or plan') for p in
                 [EXTENSION,extension.BASE/'mathematics-review.json',WORK/'primary-review.json',WORK/'availability-extension-plan.md']],
        limitations=previous.previous.work.LIMITS)
    write(BASE/'source-audit.json',dict(sources=[source],cutoff='2026-10-07',prior=ref(PRIOR,'725 unchanged v2 records')))
    (BASE/'refs.bib').write_text('@misc{exec17_s8_availability,\n author={{Causal banking proposal}},\n title={Shared validation dependencies and conditional cold-recovery capacity},\n year={2026},\n note={Authored hypothetical law; no observed vendor availability}\n}\n')
    write(BASE/'extension-author-review.json',dict(status='pass_for_compilation',
        reviewer=dict(name='Codex author/coordinator',kind='author'),
        findings=['Source establishes launch-validation and residency distinctions, not loaded-engine interruption behavior.',
                  'Conditional event law, finite joint enumeration and common-dependency ceiling agree.',
                  'Necessary q bound, unattainable finite boundary for p>0 and perfectly common local failures are derived explicitly.',
                  'Hot/cold preparation and instance occupancy must enter a matched purchase; actual rights/runtime remain open.',
                  'Preserve both failed depth reviews; final exclusive credit remains to be measured.'],
        evidence=[ref(p,'Reviewed or preserved input') for p in
            [CHAPTER,EXTENSION,WORK/'depth-review-v2.json',WORK/'availability-extension-plan.md',
             extension.BASE/'mathematics-review.json',WORK/'primary-review.json',BASE/'source-audit.json']],
        limitations=previous.previous.work.LIMITS,visual_acceptance=False))
    write(BASE/'prepared-inputs.json',dict(inputs=[ref(p,'Preserved or reviewed input') for p in
        [OLD,PRIOR,previous.CHAPTER,CHAPTER,EXTENSION,WORK/'depth-review-v2.json',WORK/'availability-extension-plan.md',
         extension.BASE/'mathematics-review.json',BASE/'extension-author-review.json',Path(__file__)]],
        generated=[ref(p,'Preserving successor source') for p in [DRIVER,BASE/'refs.bib',BASE/'source-audit.json']],
        transformation='One availability input after preserved residency input; every prior chapter byte recoverable.',
        insert=INSERT,visual_acceptance=False))
    print(json.dumps(dict(prepared=str(DRIVER.relative_to(ROOT)),expected_records=726)))


def build():
    assert not OUT.exists() and not PDF.exists()
    assert CHAPTER.read_text()==expected_chapter() and DRIVER.read_text()==expected_driver()
    verify_exact();verify_bindings(read(BASE/'prepared-inputs.json'))
    for k,v in dict(BASE=BASE,OUT=OUT,OLD=OLD,NAME=NAME,DRIVER=DRIVER,PDF=PDF,PRIOR_AUDIT=PRIOR).items():setattr(engine,k,v)
    with (BASE/'compile-summary.log').open('x') as log:
        with redirect_stdout(log):engine.build()
    report=read(OUT/'build-report.json');aux=(OUT/(NAME+'.aux')).read_text();sections={}
    for label in previous.previous.LABELS+['s8-residency','s8-resident-workload','s8-availability']:
        m=re.search(re.escape(r'\newlabel{exec17:'+label+r'}{{')+r'[^}]*\}{([0-9]+)',aux);assert m,label
        sections[label]=int(m.group(1))
    report.update(pdf=ref(PDF,'Preserving commercial acquisition working reader'),
        driver=ref(DRIVER,'S8 cold-recovery successor driver'),builder=ref(Path(__file__),'Preserving builder'),
        predecessor_pdf=ref(OLD.with_suffix('.pdf'),'Preserved997-page candidate'),commercial_sections=sections)
    engine.core.write(OUT/'build-report.json',report)
    audited=trace.audit(DRIVER,OUT/'source-audit.json');write(BASE/'traceability-review.json',audited)
    assert report['pages']>997 and report['cited_records']==726
    assert audited['status']=='pass' and not audited['issues'] and audited['scholarly_pdfs']==188
    print(json.dumps(dict(pages=report['pages'],cited_records=726,sections=sections,
        scholarly_pdfs=188,material_warnings=[w for w in report['warnings'] if 'Underfull' not in w])))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=['prepare','build'])
    args=parser.parse_args();{'prepare':prepare,'build':build}[args.command]()
