#!/usr/bin/env python3
"""Preserve the S8 depth/typography failure and build its reviewed successor."""
import argparse
from contextlib import redirect_stdout
import json
from pathlib import Path
import re

import audit_reader_traceability_v2_20261013 as trace
import build_java_temporal_engine_20261016 as engine
import build_s8_reader_20261017 as previous
import s8_residency_20261017 as extension
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write

ROOT,WORK=previous.ROOT,previous.WORK
BASE=WORK/'publication-v2'
OUT=BASE/'reader'
OLD=previous.DRIVER
PRIOR=previous.OUT/'source-audit.json'
CANONICAL_OLD=previous.OLD
NAME='causal_proposal_commercial_gap_reviewed_v2_2026-10-17'
DRIVER=ROOT/'docs'/(NAME+'.tex')
PDF=DRIVER.with_suffix('.pdf')
CHAPTER=BASE/'chapter.tex'
EXTENSION=extension.BASE/'development.tex'
REPLACEMENTS={
 'Temporal/interventional discovery &':'Temporal and intervention discovery &',
 'Identification/counterfactual &':'Identification and counterfactuals &',
 'Mediation/sensitivity &':'Mediation and sensitivity &',
 'Effects/heterogeneity &':'Effects and heterogeneity &',
 'Longitudinal/survival &':'Longitudinal and survival &',
 'Networks/interference &':'Networks and interference &',
 'Transport/missingness &':'Transport and missingness &',
 'Computation/integration &':'Computation and integration &',
 'For independent jobs and a nonpreemptive\nschedule, the makespan is':
 'For independent jobs all available at time zero and a nonpreemptive\nschedule, the makespan is',
 'a graph-class intervention query, a weak-IV set, a competing-event\nrow conversion and a fixed-history policy value.':
 'a graph-class intervention query for discovery, a weak-IV funding set, a\ncompeting-event servicing conversion and an observation identity/clock map.\nInclude a fixed-history policy value as an additional servicing case.',
 'All nine\nsignal-contingent pairs of routes give the same optimum under separate\nenumeration':
 'Separate enumeration of all nine\nsignal-contingent pairs of routes confirms this optimum'
}
INSERT=r'\input{program/execution/2026-10-17/s8/residency-extension/development.tex}'


def read(path):return json.loads(path.read_text())


def expected_chapter():
    text=previous.CHAPTER.read_text()
    for old,new in REPLACEMENTS.items():
        assert text.count(old)==1,old
        text=text.replace(old,new)
    marker=r'\section{Exact hypothetical cost and route choice}'
    assert text.count(marker)==1
    return text.replace(marker,INSERT+'\n\n'+marker)


def expected_driver():
    text=OLD.read_text()
    assert text.count(previous.INSERT)==1
    text=text.replace(previous.INSERT,r'\input{program/execution/2026-10-17/s8/publication-v2/chapter.tex}')
    pat=re.compile(r'\\bibliography\{([^}]+)\}')
    return pat.sub(lambda m:r'\bibliography{'+m.group(1)+',program/execution/2026-10-17/s8/publication-v2/refs}',text)


def verify_exact():
    previous.verify_exact()
    exact=read(extension.BASE/'exact-results.json')
    assert extension.calculate()==exact and extension.separate(exact)['status']=='pass'
    verify_bindings(read(extension.BASE/'mathematics-review.json'))


def prepare():
    assert not BASE.exists() and not DRIVER.exists() and not PDF.exists()
    verify_bindings(read(PRIOR));previous.verify_exact()
    failure=read(WORK/'depth-review-initial.json');assert failure['substantive_page_credit']==6.25
    # Fail before writing if the copy edits no longer describe the preserved draft.
    chapter=expected_chapter();driver=expected_driver()
    exact=extension.calculate(); checked=extension.separate(exact)
    write(extension.BASE/'exact-results.json',exact)
    write(extension.BASE/'mathematics-review.json',dict(checked,
        reviewer=dict(name='Codex author/coordinator',kind='author'),
        evidence=[ref(p,'Source-specific exact residency evidence') for p in
            [EXTENSION,extension.BASE/'exact-results.json',ROOT/'tools/s8_residency_20261017.py',
             WORK/'residency-extension-plan.md',WORK/'primary-review.json']],
        limitations=['Empty initial residency; serial nonoverlapping load/inference; instantaneous eviction; fixed immutable model identities.',
                    'Known batch oracle and online policies have different information;729-path law is stipulated, not sampled.',
                    'Capacity prices and time charges are hypothetical; no actual license, engine, latency, workload or bank benefit is established.']))
    BASE.mkdir();CHAPTER.write_text(chapter);DRIVER.write_text(driver)
    source=dict(integrated_citation_key='exec17_s8_residency',
        title='Loaded-model residency, known-batch and online acquisition references',
        author='Causal banking proposal',kind='project_derivation',year=2026,
        source_identity='Project finite residency recurrence, exhaustive path enumeration and conditional capacity decision',
        version_date='2026-10-17; inherited Bayesia source and2026-10-07 cutoff limits retained',
        local_copy=ref(extension.BASE/'exact-results.json','Exact loads, times,729-path means and hypothetical prices'),
        inspected_anchors=['capacity','uniform_workload','known_batch_costs','assumptions'],
        supported_claims=['Known-batch loads6/4/3 and times36/26/21 differ from LRU loads6/6/3.',
                          'Uniform six-request means13/3,769/243,665/243 agree by full enumeration and marginal probability calculations.',
                          'Known-batch cost chooses two slots, expected IID online cost chooses one, and a worst-support30-unit deadline requires three under stated assumptions.'],
        records=[ref(p,'Reviewed exact or primary input') for p in
                 [EXTENSION,extension.BASE/'mathematics-review.json',WORK/'primary-review.json',WORK/'residency-extension-plan.md']],
        limitations=previous.work.LIMITS)
    write(BASE/'source-audit.json',dict(sources=[source],cutoff='2026-10-07',prior=ref(PRIOR,'724 unchanged initial-candidate records')))
    (BASE/'refs.bib').write_text('@misc{exec17_s8_residency,\n author={{Causal banking proposal}},\n title={Loaded-model residency, known-batch and online acquisition references},\n year={2026},\n note={Authored hypothetical laws; inherited cutoff and source limits retained}\n}\n')
    write(BASE/'extension-author-review.json',dict(status='pass_for_compilation',
        reviewer=dict(name='Codex author/coordinator',kind='author'),
        findings=['Correct eight overflowing table labels, explicit release-time assumption, observation journey case and ambiguous enumeration wording.',
                  'Residency recurrence has sufficient state under stipulated immutable models and serial processing; delaying eviction is without loss here.',
                  'Two-slot lower bound and trace prove four loads; LRU six-load failure is retained, not relabeled as a runtime trial.',
                  'All729 uniform sequences agree with independent mean-load formulas; expected and worst-deadline choices differ for explicit objectives.',
                  'Shared annual capacity allocation, license connectivity, identity updates and adaptive requests remain separate from hypothetical timing.',
                  'Initial6.25-page depth and typography failure preserved; successor exclusive depth remains to be measured.'],
        evidence=[ref(p,'Reviewed new or preserved input') for p in
            [CHAPTER,EXTENSION,WORK/'depth-review-initial.json',WORK/'residency-extension-plan.md',
             extension.BASE/'mathematics-review.json',WORK/'primary-review.json',BASE/'source-audit.json']],
        visual_acceptance=False,limitations=previous.work.LIMITS))
    write(BASE/'prepared-inputs.json',dict(inputs=[ref(p,'Preserved or reviewed input') for p in
        [OLD,PRIOR,previous.CHAPTER,CHAPTER,EXTENSION,WORK/'depth-review-initial.json',WORK/'residency-extension-plan.md',
         extension.BASE/'mathematics-review.json',BASE/'extension-author-review.json',Path(__file__)]],
        generated=[ref(p,'Preserving successor source') for p in [DRIVER,BASE/'refs.bib',BASE/'source-audit.json']],
        replacements=REPLACEMENTS,insert=INSERT,
        transformation='Explicit S8 text repairs plus residency section; every canonical S7 chapter remains unchanged.',
        visual_acceptance=False))
    print(json.dumps(dict(prepared=str(DRIVER.relative_to(ROOT)),expected_records=725)))


def build():
    assert not OUT.exists() and not PDF.exists()
    assert CHAPTER.read_text()==expected_chapter() and DRIVER.read_text()==expected_driver()
    verify_exact();verify_bindings(read(BASE/'prepared-inputs.json'))
    for k,v in dict(BASE=BASE,OUT=OUT,OLD=OLD,NAME=NAME,DRIVER=DRIVER,PDF=PDF,PRIOR_AUDIT=PRIOR).items():setattr(engine,k,v)
    with (BASE/'compile-summary.log').open('x') as log:
        with redirect_stdout(log):engine.build()
    report=read(OUT/'build-report.json');aux=(OUT/(NAME+'.aux')).read_text();sections={}
    for label in previous.LABELS+['s8-residency','s8-resident-workload']:
        m=re.search(re.escape(r'\newlabel{exec17:'+label+r'}{{')+r'[^}]*\}{([0-9]+)',aux)
        assert m,label
        sections[label]=int(m.group(1))
    report.update(pdf=ref(PDF,'Preserving commercial acquisition working reader'),
        driver=ref(DRIVER,'S8 residency successor driver'),builder=ref(Path(__file__),'Preserving builder'),
        predecessor_pdf=ref(OLD.with_suffix('.pdf'),'Preserved993-page initial candidate'),commercial_sections=sections)
    engine.core.write(OUT/'build-report.json',report)
    audited=trace.audit(DRIVER,OUT/'source-audit.json');write(BASE/'traceability-review.json',audited)
    assert report['pages']>993 and report['cited_records']==725
    assert audited['status']=='pass' and not audited['issues'] and audited['scholarly_pdfs']==188
    print(json.dumps(dict(pages=report['pages'],cited_records=725,sections=sections,
        scholarly_pdfs=188,material_warnings=[w for w in report['warnings'] if 'Underfull' not in w])))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=['prepare','build'])
    args=parser.parse_args();{'prepare':prepare,'build':build}[args.command]()
