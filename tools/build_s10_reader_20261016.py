#!/usr/bin/env python3
"""Integrate reviewed qualification chapter without rewriting the inherited book."""
import argparse
from contextlib import redirect_stdout
import json
from pathlib import Path
import re

import audit_reader_traceability_v2_20261013 as trace
import build_java_temporal_engine_20261016 as engine
import prepare_s10_20261016 as work
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write

ROOT=work.ROOT
BASE=work.BASE/'publication'
OUT=BASE/'reader'
OLD=ROOT/'docs/causal_proposal_topology_2026-10-16.tex'
PRIOR=ROOT/'docs/program/execution/2026-10-16/topology/publication/reader/source-audit.json'
NAME='causal_proposal_qualification_2026-10-16'
DRIVER=ROOT/'docs'/(NAME+'.tex')
PDF=DRIVER.with_suffix('.pdf')
BS,NL=chr(92),chr(10)


def prepare():
    assert not DRIVER.exists() and not BASE.exists()
    BASE.mkdir()
    audit=json.loads((work.BASE/'source-audit.json').read_text())
    verify_bindings(audit);verify_bindings(json.loads((work.BASE/'draft-author-review.json').read_text()))
    assert work.examples.calculate()==json.loads((work.BASE/'exact-results.json').read_text())
    write(BASE/'source-audit.json',audit)
    bib=[]
    for s in audit['sources']:
        bib.append('@misc{'+s['integrated_citation_key']+','+NL+
          ' author={{'+engine.shared.escape(s['author'])+'}},'+NL+
          ' title={'+engine.shared.escape(s['title'])+'},'+NL+' year={'+str(s['year'])+'},'+NL+
          ' note={'+engine.shared.escape(s['version_date'])+'}'+NL+'}'+NL)
    (BASE/'refs.bib').write_text(NL.join(bib))
    book=OLD.read_text()
    marker=BS+'label{integrated:software-end}'
    assert book.count(marker)==1
    book=book.replace(marker,BS+'input{program/comprehensive-v14/work/TEXT.DRAFT.S10/chapter.tex}'+NL+marker)
    pattern=re.compile(re.escape(BS+'bibliography{')+'([^}]+)'+re.escape('}'))
    assert len(pattern.findall(book))==1
    book=pattern.sub(lambda m:BS+'bibliography{'+m.group(1)+',program/execution/2026-10-16/s10/publication/refs}',book)
    DRIVER.write_text(book)
    write(BASE/'prepared-inputs.json',{'inputs':[ref(p,'Reviewed preserving input') for p in
      [OLD,PRIOR,work.BASE/'draft-author-review.json',work.CHAPTER,Path(__file__)]],
      'generated':[ref(p,'Successor source') for p in [DRIVER,BASE/'source-audit.json',BASE/'refs.bib']],
      'credit_policy':'No automatic coverage/depth completion or product qualification','visual_acceptance':False})
    print(json.dumps({'prepared':str(DRIVER.relative_to(ROOT)),'new_citation_records':2}))


def build():
    for key,value in {'BASE':BASE,'OUT':OUT,'OLD':OLD,'NAME':NAME,'DRIVER':DRIVER,'PDF':PDF,'PRIOR_AUDIT':PRIOR}.items():
        setattr(engine,key,value)
    with (BASE/'compile-summary.log').open('x') as stream:
        with redirect_stdout(stream):engine.build()
    report=json.loads((OUT/'build-report.json').read_text());aux=(OUT/(NAME+'.aux')).read_text()
    def page(label):
        pattern=re.escape(BS+'newlabel{'+label+'}{{')+'[^}]*'+re.escape('}{')+'([0-9]+)'
        return int(re.search(pattern,aux).group(1))
    report.update(builder=ref(Path(__file__),'Preserving qualification chapter builder'),
      predecessor_pdf=ref(OLD.with_suffix('.pdf'),'Frozen809-page reader'),
      qualification_sections={label:page('exec16:'+label) for label in ['s10','s10-end']})
    engine.core.write(OUT/'build-report.json',report)
    audited=trace.audit(DRIVER,OUT/'source-audit.json');write(BASE/'traceability-review.json',audited)
    assert report['cited_records']==641 and report['pages']>809
    assert audited['status']=='pass' and not audited['issues'] and audited['scholarly_pdfs']==175
    print(json.dumps({'pages':report['pages'],'cited_records':report['cited_records'],'sections':report['qualification_sections'],
      'scholarly_pdfs':audited['scholarly_pdfs'],'material_warnings':[w for w in report['warnings'] if 'Underfull' not in w]}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','build']);args=p.parse_args()
    {'prepare':prepare,'build':build}[args.command]()
