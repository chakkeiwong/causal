#!/usr/bin/env python3
"""Extend the preserving L7 successor with two authentic benchmark originals."""
import argparse
import json
from pathlib import Path
import re
import build_l7_benchmarking_20261014 as engine
import build_l7_benchmarking_v2_20261014 as previous
import develop_l7_benchmarking_20261014 as work
import review_l7_frontier_20261014 as frontier
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT=work.ROOT
BASE=work.BASE/'v3'
OUT=BASE/'reader'
OLD,PRIOR=previous.OLD,work.PRIOR
NAME='causal_proposal_benchmarking_v3_2026-10-14'
DRIVER=ROOT/'docs'/(NAME+'.tex')
PDF=DRIVER.with_suffix('.pdf')
CHAPTER=ROOT/'docs/program/comprehensive-v14/work/TEXT.DRAFT.L7/chapter-v3.tex'
BS,NL=chr(92),chr(10)


def prepare():
    assert not DRIVER.exists() and not CHAPTER.exists()
    BASE.mkdir(exist_ok=False)
    sources=json.loads((work.BASE/'source-audit.json').read_text())['sources']
    sources+=json.loads((frontier.BASE/'source-audit.json').read_text())['sources']
    verify_bindings(sources)
    assert frontier.exact()==json.loads((frontier.BASE/'exact-results.json').read_text())
    write(BASE/'source-audit.json',{'cutoff':'2026-10-07','sources':sources,
                                  'prior':ref(PRIOR,'568 inherited records')})
    addition=BASE/'frontier.tex'
    addition.write_text((frontier.BASE/'comparison.template').read_text().replace('§',BS))
    bib=[]
    for s in sources:
        authors=s.get('author') or ' and '.join(s['authors'])
        author=engine.engine.shared.escape(authors)
        if s['kind']!='paper':
            author='{'+author+'}'
        bib.append('@misc{'+s['integrated_citation_key']+','+NL+' author={'+author+'},'+NL+
                   ' title={'+engine.engine.shared.escape(s['title'])+'},'+NL+
                   ' year={'+str(s['year'])+'},'+NL+
                   ' note={'+engine.engine.shared.escape(s['version_date'])+'}'+NL+'}'+NL)
    (BASE/'refs.bib').write_text(NL.join(bib))
    wrapper=previous.CHAPTER.read_text()+BS+'input{'+str(addition.relative_to(ROOT/'docs'))+'}'+NL
    CHAPTER.write_text(wrapper)
    book=previous.DRIVER.read_text()
    old_input=BS+'input{'+str(previous.CHAPTER.relative_to(ROOT/'docs'))+'}'
    new_input=BS+'input{'+str(CHAPTER.relative_to(ROOT/'docs'))+'}'
    assert book.count(old_input)==1
    book=book.replace(old_input,new_input)
    old_bib='program/execution/2026-10-14/l7-benchmarking/v2/refs}'
    assert book.count(old_bib)==1
    book=book.replace(old_bib,'program/execution/2026-10-14/l7-benchmarking/v3/refs}')
    DRIVER.write_text(book)
    write(BASE/'prepared-inputs.json',{
        'inputs':[ref(p,'Preserved reviewed input') for p in [
            previous.DRIVER,previous.CHAPTER,previous.OUT/'build-report.json',PRIOR,
            previous.BASE/'repair-review.json',frontier.BASE/'primary-review.json',
            frontier.BASE/'comparison.template',Path(__file__).resolve()]],
        'generated':[ref(p,'Integrated successor') for p in [
            DRIVER,CHAPTER,addition,BASE/'source-audit.json',BASE/'refs.bib']],
        'visual_acceptance':False,
    })
    print(json.dumps({'prepared':str(DRIVER.relative_to(ROOT)),'new_records':len(sources)}))


def build():
    # Engine validates the preserving original baseline; add the expected source delta.
    for key,value in {'BASE':BASE,'OUT':OUT,'OLD':OLD,'PRIOR':PRIOR,'NAME':NAME,
                      'DRIVER':DRIVER,'PDF':PDF,'CHAPTER':CHAPTER}.items():
        setattr(engine,key,value)
    for key,value in {'BASE':BASE,'OUT':OUT,'OLD':OLD,'PRIOR_AUDIT':PRIOR,'NAME':NAME,
                      'DRIVER':DRIVER,'PDF':PDF}.items():
        setattr(engine.engine,key,value)
    from contextlib import redirect_stdout
    with (BASE/'compile-summary.log').open('x') as stream:
        with redirect_stdout(stream):
            engine.engine.build()
    report=json.loads((OUT/'build-report.json').read_text())
    aux=(OUT/(NAME+'.aux')).read_text()
    def page(label):
        pattern=re.escape(BS+'newlabel{'+label+'}{{')+'[^}]*'+re.escape('}{')+'([0-9]+)'
        return int(re.search(pattern,aux).group(1))
    report.update(builder=ref(Path(__file__).resolve(),'Preserving L7 expanded primary benchmark comparison'),
                  predecessor_pdf=ref(OLD.with_suffix('.pdf'),'Frozen750-page baseline'),
                  chapter_sections={label:page(label) for label in [
                      'la:evaluation','exec14:l7-development','exec14:l7-adjudication','exec14:l7-metamorphic',
                      'exec14:l7-oracles','exec14:l7-development-end','exec14:l7-frontier','exec14:l7-frontier-end','la:economics']})
    engine.engine.core.write(OUT/'build-report.json',report)
    assert report['cited_records']==573 and report['pages']>754
    result=engine.trace.audit(DRIVER,OUT/'source-audit.json')
    write(BASE/'traceability-review.json',result)
    assert result['status']=='pass' and not result['issues'] and result['scholarly_pdfs']==162
    print(json.dumps({'pages':report['pages'],'cited_records':report['cited_records'],
                      'sections':report['chapter_sections'],'scholarly_pdfs':result['scholarly_pdfs'],
                      'material_warnings':[w for w in report['warnings'] if 'Underfull' not in w]}))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('command',choices=['prepare','build'])
    args=parser.parse_args()
    {'prepare':prepare,'build':build}[args.command]()
