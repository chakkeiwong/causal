#!/usr/bin/env python3
"""Preserve the recovered reader and integrate the effect/threshold chapter."""
import argparse
from contextlib import redirect_stdout
import json
from pathlib import Path
import re

import audit_reader_traceability_v2_20261013 as trace
import build_java_temporal_engine_20261016 as engine
import prepare_s4_20261017 as work
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT, WORK = work.ROOT, work.BASE
BASE = WORK/'publication'
OUT = BASE/'reader'
OLD = ROOT/'docs/causal_proposal_identification_reviewed_2026-10-17.tex'
PRIOR = work.PRIOR
NAME = 'causal_proposal_effects_2026-10-17'
DRIVER = ROOT/'docs'/(NAME+'.tex')
PDF = DRIVER.with_suffix('.pdf')
LABELS = ['s4','s4-target','s4-remainder','s4-clipping','s4-paths','s4-joint',
          's4-allocation','s4-regret','s4-curvature','s4-fuzzy','s4-support',
          's4-adoption','s4-end']


def expected_driver():
    book = OLD.read_text()
    marker = r'\input{program/execution/2026-10-17/s3/publication-v3/sensitivity.tex}'
    assert book.count(marker) == 1
    book = book.replace(marker,marker+'\n'+r'\input{program/comprehensive-v14/work/TEXT.DRAFT.S4/chapter.tex}')
    pattern = re.compile(r'\\bibliography\{([^}]+)\}')
    assert len(pattern.findall(book)) == 1
    return pattern.sub(lambda m:r'\bibliography{'+m.group(1)+',program/execution/2026-10-17/s4/publication/refs}',book)


def prepare():
    assert not BASE.exists() and not DRIVER.exists()
    for p in ['primary-review.json','mathematics-review.json','source-audit.json','prototype-design.json']:
        verify_bindings(json.loads((WORK/p).read_text()))
    assert work.independent()['status'] == 'pass'
    tex=work.CHAPTER.read_text()
    assert not any(r'\label{' in body for body in re.findall(r'\\\[(.*?)\\\]',tex,re.S)), 'Labels require numbered displays'
    assert ',+' not in tex and tex.count(r'\chapter{') == 1
    cited={k.strip() for match in re.findall(engine.shared.CITE,tex) for k in match.split(',')}
    prior=json.loads(PRIOR.read_text())['sources']
    additions=json.loads((WORK/'source-audit.json').read_text())['sources']
    assert cited <= {s['integrated_citation_key'] for s in prior+additions}
    write(WORK/'draft-author-review.json',dict(status='pass_for_compilation',reviewer=work.REVIEWER,
        findings=['Connected target, influence-function, exact-remainder, joint-action, resource-dual and threshold argument with explicit assumptions and financial units.',
            'Separate author symbolic/moment/dual/witness checks reproduce; selected software claims trace to inspected originals.',
            'Public/generated comparison remains a design. No new upstream runtime, bank ROI, full census or acceptance claim.',
            'Initial unbound draft punctuation typo repaired before source freezing. Depth remains to be assessed on compiled pages.'],
        evidence=[ref(p,'Reviewed draft or bounded evidence') for p in
                  [work.CHAPTER,WORK/'plan.md',WORK/'primary-review.json',WORK/'mathematics-review.json',
                   WORK/'exact-results.json',WORK/'prototype-design.json',Path(__file__)]],
        limitations=work.LIMITS,visual_acceptance=False))
    BASE.mkdir()
    audit=json.loads((WORK/'source-audit.json').read_text())
    write(BASE/'source-audit.json',audit)
    bib=[]
    for s in audit['sources']:
        bib.append('@misc{'+s['integrated_citation_key']+',\n author={{'+engine.shared.escape(s['author'])+
                   '}},\n title={'+engine.shared.escape(s['title'])+'},\n year={'+str(s['year'])+'},\n note={'+
                   engine.shared.escape(s['version_date'])+'}\n}\n')
    (BASE/'refs.bib').write_text('\n'.join(bib))
    DRIVER.write_text(expected_driver())
    write(BASE/'prepared-inputs.json',dict(
        inputs=[ref(p,'Preserved or reviewed input') for p in
                [OLD,PRIOR,work.CHAPTER,WORK/'draft-author-review.json',Path(__file__)]],
        generated=[ref(p,'Successor source') for p in [DRIVER,BASE/'source-audit.json',BASE/'refs.bib']],
        credit_policy='Exclusive S4 depth on actual compiled pages; earlier AIPW, target, ranking, IV and basic RD developments receive no duplicate credit.',
        visual_acceptance=False))
    print(json.dumps(dict(prepared=str(DRIVER.relative_to(ROOT)),new_citations=3)))


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
    report.update(builder=ref(Path(__file__),'Preserving S4 builder'),
        predecessor_pdf=ref(OLD.with_suffix('.pdf'),'Frozen899-page identification reader'),
        effect_sections=sections)
    engine.core.write(OUT/'build-report.json',report)
    audited=trace.audit(DRIVER,OUT/'source-audit.json')
    write(BASE/'traceability-review.json',audited)
    assert report['cited_records']==706 and report['pages']>899
    assert audited['status']=='pass' and not audited['issues'] and audited['scholarly_pdfs']==187
    print(json.dumps(dict(pages=report['pages'],cited_records=706,sections=sections,scholarly_pdfs=187,
        material_warnings=[w for w in report['warnings'] if 'Underfull' not in w])))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('command',choices=['prepare','build'])
    args=parser.parse_args()
    {'prepare':prepare,'build':build}[args.command]()
