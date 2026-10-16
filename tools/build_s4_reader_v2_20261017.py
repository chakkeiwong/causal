#!/usr/bin/env python3
"""Preserve the first S4 reader and develop its failed substantive-depth review."""
import argparse
from contextlib import redirect_stdout
import json
from pathlib import Path
import re

import audit_reader_traceability_v2_20261013 as trace
import build_java_temporal_engine_20261016 as engine
import build_s4_reader_20261017 as previous
import s4_extension_20261017 as extension
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT, WORK = previous.ROOT, previous.WORK
BASE = WORK/'publication-v2'
OUT = BASE/'reader'
OLD = previous.DRIVER
CANONICAL_OLD = previous.OLD
PRIOR = previous.OUT/'source-audit.json'
NAME = 'causal_proposal_effects_reviewed_2026-10-17'
DRIVER = ROOT/'docs'/(NAME+'.tex')
PDF = DRIVER.with_suffix('.pdf')
EXTENSION = extension.CHAPTER
LABELS = previous.LABELS + ['s4-common-population','s4-design-criterion',
    's4-robust-allocation','s4-finite-policy','s4-gap-bounds','s4-extension-end']


def expected_driver():
    book = OLD.read_text()
    marker = r'\input{program/comprehensive-v14/work/TEXT.DRAFT.S4/chapter.tex}'
    assert book.count(marker) == 1
    book = book.replace(marker, marker+'\n'+r'\input{'+str(EXTENSION.relative_to(ROOT/'docs'))+'}')
    pattern = re.compile(r'\\bibliography\{([^}]+)\}')
    assert len(pattern.findall(book)) == 1
    return pattern.sub(lambda m:r'\bibliography{'+m.group(1)+',program/execution/2026-10-17/s4/publication-v2/refs}',book)


def prepare():
    assert not BASE.exists() and not DRIVER.exists()
    for p in [previous.BASE/'prepared-inputs.json',previous.OUT/'build-report.json',PRIOR,
              previous.BASE/'traceability-review.json',WORK/'depth-review-initial.json',
              extension.BASE/'mathematics-review.json']:
        verify_bindings(json.loads(p.read_text()))
    exact=json.loads((extension.BASE/'exact-results.json').read_text())
    assert extension.calculate() == exact and extension.separate(exact)['status'] == 'pass'
    tex=EXTENSION.read_text()
    assert ',+' not in tex and r'\chapter{' not in tex
    assert not any(r'\label{' in body for body in re.findall(r'\\\[(.*?)\\\]',tex,re.S))
    cited={k.strip() for match in re.findall(engine.shared.CITE,tex) for k in match.split(',')}
    assert cited <= {s['integrated_citation_key'] for s in json.loads(PRIOR.read_text())['sources']}|{'exec17_s4_extension'}
    BASE.mkdir()
    claims=[
        'Full-population multiarm effects10/6 versus selected-pair effects8/6; twelve-atom score law gives covariance[[128,-48],[-48,60]] and difference variance284.',
        'Cauchy--Schwarz and strict convexity certify the declared iid experiment trace criterion; different precision objectives imply different allocations.',
        'Rectangular sensitivity classes imply explicit maximin and minimax-regret objectives with distinct exact policies and endpoint witnesses.',
        'A complete bounded-score exponential/union proof gives a conditional finite-policy guarantee under independent evaluation and known randomized propensities; numerical bounds are deterministic, not measured coverage.',
        'Two-point score support plus quantitative separate Lipschitz restrictions gives sharp cutoff-effect bounds, linear endpoint witnesses and an explicit information remedy.'
    ]
    source=dict(integrated_citation_key='exec17_s4_extension',
        title='Common-population comparisons, robust allocation and finite-policy and support-gap bounds',
        author='Causal banking proposal',kind='project_derivation',year=2026,
        source_identity='Project-authored complete finite laws, elementary proof and endpoint constructions',
        version_date='2026-10-17; author derivation; inherited primary-source/cutoff limits unchanged',
        local_copy=ref(extension.BASE/'exact-results.json','Five exact authored families'),
        inspected_anchors=claims,supported_claims=claims,
        records=[ref(p,a) for p,a in [
            (EXTENSION,'Complete connected derivations and proofs'),
            (extension.BASE/'mathematics-review.json','Separate atoms, algebra, endpoint and range checks'),
            (ROOT/'tools/s4_extension_20261017.py','Exact calculations and separate verification'),
            (WORK/'depth-extension-plan.md','Reviewed nonduplicate depth repair'),
            (WORK/'primary-review.json','Inherited inspected primary software/paper claims'),
            (Path(__file__),'Preserving preparation and build')]],limitations=extension.work.LIMITS)
    write(BASE/'source-audit.json',dict(cutoff='2026-10-07',sources=[source],
        prior=ref(PRIOR,'706 unchanged candidate source records')))
    (BASE/'refs.bib').write_text('@misc{exec17_s4_extension,\n author={{Causal banking proposal}},\n title={'+
        engine.shared.escape(source['title'])+'},\n year={2026},\n note={'+
        engine.shared.escape(source['version_date'])+'}\n}\n')
    DRIVER.write_text(expected_driver())
    write(BASE/'extension-author-review.json',dict(status='pass_for_compilation',reviewer=extension.REVIEWER,
        findings=claims+[
            'Selected CausalML full-X point mean is explicitly distinguished from the explanatory pair-population mean; no package result of8 is alleged.',
            'The elementary exponential bound is proved here; no uninspected theorem or additional scholarly citation is invented.',
            'Draft comma/plus typo corrected before binding. Equation labels use numbered environments. Actual exclusive depth remains subject to compiled review.'],
        evidence=[ref(p,'Reviewed source or exact evidence') for p in [EXTENSION,
            extension.BASE/'exact-results.json',extension.BASE/'mathematics-review.json',
            WORK/'depth-review-initial.json',WORK/'depth-extension-plan.md',Path(__file__)]],
        limitations=extension.work.LIMITS,visual_acceptance=False))
    write(BASE/'prepared-inputs.json',dict(
        inputs=[ref(p,'Preserved or reviewed input') for p in [OLD,PRIOR,EXTENSION,
            previous.OUT/'build-report.json',BASE/'extension-author-review.json',Path(__file__)]],
        generated=[ref(p,'Preserving successor source') for p in [DRIVER,BASE/'source-audit.json',BASE/'refs.bib']],
        credit_policy='Assess all actual S4 pages; preserve initial8-page failure, discount inherited and generic material, reserve S5/S6 subjects.',
        visual_acceptance=False))
    print(json.dumps(dict(prepared=str(DRIVER.relative_to(ROOT)),expected_records=707,new_project_derivations=1)))


def build():
    assert not OUT.exists() and not PDF.exists()
    assert DRIVER.read_text() == expected_driver()
    for k,v in dict(BASE=BASE,OUT=OUT,OLD=OLD,NAME=NAME,DRIVER=DRIVER,PDF=PDF,PRIOR_AUDIT=PRIOR).items():
        setattr(engine,k,v)
    with (BASE/'compile-summary.log').open('x') as stream:
        with redirect_stdout(stream):engine.build()
    report=json.loads((OUT/'build-report.json').read_text())
    aux=(OUT/(NAME+'.aux')).read_text()
    sections={}
    for label in LABELS:
        match=re.search(re.escape('\\newlabel{exec17:'+label+'}{{')+'[^}]*'+re.escape('}{')+'([0-9]+)',aux)
        assert match,label
        sections[label]=int(match.group(1))
    report.update(pdf=ref(PDF,'Preserving S4 effects, decisions and quasi-experiment working reader'),
        builder=ref(Path(__file__),'Preserving S4 substantive extension builder'),
        predecessor_pdf=ref(OLD.with_suffix('.pdf'),'Preserved unpublished912-page S4 candidate'),
        canonical_predecessor_pdf=ref(CANONICAL_OLD.with_suffix('.pdf'),'Canonical899-page identification reader'),
        effect_sections=sections)
    engine.core.write(OUT/'build-report.json',report)
    audited=trace.audit(DRIVER,OUT/'source-audit.json')
    write(BASE/'traceability-review.json',audited)
    assert report['cited_records']==707 and report['pages']>912
    assert audited['status']=='pass' and not audited['issues'] and audited['scholarly_pdfs']==187
    print(json.dumps(dict(pages=report['pages'],cited_records=707,sections=sections,scholarly_pdfs=187,
        material_warnings=[w for w in report['warnings'] if 'Underfull' not in w])))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=['prepare','build'])
    args=parser.parse_args();{'prepare':prepare,'build':build}[args.command]()
