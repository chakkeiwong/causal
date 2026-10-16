#!/usr/bin/env python3
"""Build a preserving S6 joint-weight and full-controller depth successor."""
import argparse
from contextlib import redirect_stdout
import json
from pathlib import Path
import re

import audit_reader_traceability_v2_20261013 as trace
import build_java_temporal_engine_20261016 as engine
import build_s6_reader_20261017 as previous
import s6_depth_extension_20261017 as extension
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

ROOT, WORK = previous.ROOT, previous.WORK
BASE = WORK / 'publication-v2'
OUT = BASE / 'reader'
OLD = previous.DRIVER
CANONICAL_OLD = previous.OLD
PRIOR = previous.OUT / 'source-audit.json'
NAME = 'causal_proposal_panels_reviewed_v2_2026-10-17'
DRIVER = ROOT / 'docs' / (NAME + '.tex')
PDF = DRIVER.with_suffix('.pdf')
CHAPTER = BASE / 'chapter.tex'
EXTENSION = extension.BASE / 'development.tex'
INSERT = r'\input{program/execution/2026-10-17/s6/depth-extension/development.tex}'
LABELS = previous.LABELS + ['s6-joint','s6-full-rule','s6-rule-boundaries','s6-rule-value']


def read(path):
    return json.loads(path.read_text())


def expected_chapter():
    tex = previous.CHAPTER.read_text()
    marker = r'\section{Conclusion}'
    assert tex.count(marker) == 1
    return tex.replace(marker, INSERT + '\n\n' + marker)


def expected_driver():
    book = OLD.read_text()
    marker = r'\input{' + str(previous.CHAPTER.relative_to(ROOT/'docs')) + '}'
    assert book.count(marker) == 1
    book = book.replace(marker, r'\input{' + str(CHAPTER.relative_to(ROOT/'docs')) + '}')
    pattern = re.compile(r'\\bibliography\{([^}]+)\}')
    assert len(pattern.findall(book)) == 1
    return pattern.sub(lambda m:r'\bibliography{' + m.group(1) +
                       ',program/execution/2026-10-17/s6/publication-v2/refs}',book)


def prepare():
    assert not BASE.exists() and not DRIVER.exists()
    for p in [previous.BASE/'prepared-inputs.json',previous.OUT/'build-report.json',
              PRIOR,previous.BASE/'traceability-review.json',WORK/'depth-review-initial.json',
              extension.BASE/'mathematics-review.json']:
        verify_bindings(read(p))
    exact=read(extension.BASE/'exact-results.json')
    assert extension.calculate()==exact and extension.separate(exact)['status']=='pass'
    tex=EXTENSION.read_text()
    assert not [c for c in tex if ord(c)<32 and c not in '\n\t']
    assert not re.search(r'(?<!\\)\\\n',tex)
    assert r'\chapter{' not in tex
    assert set(re.findall(engine.shared.CITE,tex))=={'exec17_s6_extension'}
    BASE.mkdir()
    CHAPTER.write_text(expected_chapter())
    assert CHAPTER.read_text().replace(INSERT+'\n\n','')==previous.CHAPTER.read_text()
    claims=[
        'A known-factor nine-cell law has joint risk(2-a)^2(2-b)^2+sQ(a)Q(b), with a conditional optimizer and exact global sum-of-squares certificate.',
        'For0<s<=1/2 feasible zero-square roots attain9s/(1+s); at s1/8 two asymmetric optima have risk1, versus1.5 nonnegative,1.125 one-axis exact and4.5 both-axis exact.',
        'Full feedback-rule replacement from a nonzero state must retain old and new action costs; finite values and exact paired-regime tails differ from within-regime innovation values.',
        'The supplied beta[1,2] old-law-equivalent class has robust state stability(-.55,.45) and a separate discounted quadratic-cost boundary; rule.47 can have convergent benefits and divergent adverse costs.',
        'Analytic finite/infinite derivative bounds locate the adverse beta1 world for rules.42/.44; the latter has52.7002USD worst infinite value but-5.4812USD through H20 with200USD setup cost.',
        'A four-term absolute tail bound is4.3531689459USD at H80 uniformly across those two rules and the supplied class; direct structural recursions verify finite values and exact remainders.'
    ]
    limits=read(WORK/'primary-review.json')['limitations']+[
        'The oracle factor table and independent-cell noise do not qualify fitted upstream weights or shared-shock inference.',
        'Beta[1,2] is supplied sensitivity information; no probability, confidence coverage or empirical identification of that range is claimed.',
        'Policy feasibility, structural invariance, initial exposure and monetary inputs are stipulated, not authentic bank evidence.'
    ]
    source=dict(integrated_citation_key='exec17_s6_extension',
        title='Joint panel weights and whole-controller replacement under observational equivalence',
        author='Causal banking proposal',kind='project_derivation',year=2026,
        source_identity='Project-authored nine-cell factor law and continuous structural-controller class',
        version_date='2026-10-17; preserving author depth successor; inherited cutoff retained',
        local_copy=ref(extension.BASE/'exact-results.json','Exact symbolic/rational risks, controller values and tails'),
        inspected_anchors=claims,supported_claims=claims,
        records=[ref(p,a) for p,a in [
            (EXTENSION,'Connected algebra, global proof, stability boundaries and dollar comparisons'),
            (extension.BASE/'mathematics-review.json','Cell enumeration, derivative bounds and direct structural recursion'),
            (ROOT/'tools/s6_depth_extension_20261017.py','Reproducible exact references and distinct authored checks'),
            (WORK/'depth-extension-plan.md','Reviewed scope, duplication exclusions and assumptions'),
            (Path(__file__),'Preserving source transformation and compilation')]],limitations=limits)
    write(BASE/'source-audit.json',dict(cutoff='2026-10-07',sources=[source],
        prior=ref(PRIOR,'716 unchanged first-candidate source records')))
    (BASE/'refs.bib').write_text('@misc{exec17_s6_extension,\n author={{Causal banking proposal}},\n title={'+
        engine.shared.escape(source['title'])+'},\n year={2026},\n note={'+
        engine.shared.escape(source['version_date'])+'}\n}\n')
    DRIVER.write_text(expected_driver())
    write(BASE/'extension-author-review.json',dict(status='pass_for_compilation',
        reviewer=dict(name='Codex author/coordinator',kind='author'),findings=claims+[
            'Removing the single inserted input recovers every byte of the preserving first chapter.',
            'Only exclusive joint optimization and complete controller replacement are proposed for new S6 depth.',
            'The4.33USD development assertion failed before freeze; the exact uniform envelope4.3531689459USD requires the corrected4.36USD bound.'],
        evidence=[ref(p,'Reviewed source, exact evidence or preserved failure') for p in
            [CHAPTER,EXTENSION,extension.BASE/'exact-results.json',
             extension.BASE/'mathematics-review.json',WORK/'depth-review-initial.json',
             WORK/'depth-extension-plan.md',Path(__file__)]],limitations=limits,visual_acceptance=False))
    write(BASE/'prepared-inputs.json',dict(
        inputs=[ref(p,'Preserved or reviewed input') for p in
            [OLD,PRIOR,previous.CHAPTER,EXTENSION,previous.OUT/'build-report.json',
             BASE/'extension-author-review.json',Path(__file__)]],
        generated=[ref(p,'Preserving successor source') for p in
            [DRIVER,CHAPTER,BASE/'source-audit.json',BASE/'refs.bib']],
        transformation='Insert one development input before the original conclusion; removing it recovers the exact first-candidate chapter.',
        credit_policy='Retain10.25 initial exclusive equivalents; assess joint-weight optimization and full replacement-controller value after rendering, excluding generic optimization and control framing.',
        visual_acceptance=False))
    progress=WORK/'recovery-depth-progress.json'
    write(progress,dict(finding='The recovered957-page candidate passed integrity and exact references but failed exclusive depth at10.25 of minimum14. Preserving extension prepared with exact checks.',
        next_action='Compile S6 v2; inspect rendered text/equations, preserved contexts and exclusive depth. Publish only warranted outcomes, then continue eligible work.',
        evidence=[ref(p,'Recovery or repair evidence') for p in
            [WORK/'depth-review-initial.json',WORK/'depth-extension-plan.md',
             extension.BASE/'mathematics-review.json',BASE/'prepared-inputs.json']]))
    transition('progress','TEXT.DRAFT.S6',progress)
    print(json.dumps(dict(prepared=str(DRIVER.relative_to(ROOT)),expected_records=717)))


def build():
    assert not OUT.exists() and not PDF.exists()
    assert DRIVER.read_text()==expected_driver() and CHAPTER.read_text()==expected_chapter()
    for k,v in dict(BASE=BASE,OUT=OUT,OLD=OLD,NAME=NAME,DRIVER=DRIVER,
                    PDF=PDF,PRIOR_AUDIT=PRIOR).items():
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
    report.update(pdf=ref(PDF,'Preserving joint-weight and controller-value working reader'),
        driver=ref(DRIVER,'Preserving S6 v2 driver'),builder=ref(Path(__file__),'Preserving depth builder'),
        predecessor_pdf=ref(OLD.with_suffix('.pdf'),'Unpublished957-page initial candidate'),
        canonical_predecessor_pdf=ref(CANONICAL_OLD.with_suffix('.pdf'),'Canonical939-page predecessor'),
        effect_sections=sections)
    engine.core.write(OUT/'build-report.json',report)
    audited=trace.audit(DRIVER,OUT/'source-audit.json')
    write(BASE/'traceability-review.json',audited)
    assert report['cited_records']==717 and report['pages']>957
    assert audited['status']=='pass' and not audited['issues'] and audited['scholarly_pdfs']==188
    print(json.dumps(dict(pages=report['pages'],cited_records=717,sections=sections,
        scholarly_pdfs=188,material_warnings=[w for w in report['warnings'] if 'Underfull' not in w])))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=['prepare','build'])
    args=parser.parse_args();{'prepare':prepare,'build':build}[args.command]()
