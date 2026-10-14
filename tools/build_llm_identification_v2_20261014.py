#!/usr/bin/env python3
"""Preserving reader integration of a scoped LLM identification reuse decision."""
import argparse
from contextlib import redirect_stdout
import json
from pathlib import Path
import re

import audit_reader_traceability_v2_20261013 as trace
import build_native_evaluation_reader_v3_20261014 as engine
import review_llm_identification_20261014 as work
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write

ROOT=work.ROOT
BASE=work.BASE/'v2'
OUT=BASE/'reader'
OLD=ROOT/'docs/causal_proposal_causalpy_contracts_2026-10-14.tex'
PRIOR=work.AUDIT
NAME='causal_proposal_llm_identification_v2_2026-10-14'
DRIVER=ROOT/'docs'/(NAME+'.tex')
PDF=DRIVER.with_suffix('.pdf')
BS=chr(92)
NL=chr(10)

def prepare():
    assert not DRIVER.exists()and not(BASE/'prepared-inputs.json').exists()
    BASE.mkdir(exist_ok=True)
    audit=json.loads((work.BASE/'source-audit.json').read_text())
    verify_bindings(audit);verify_bindings(json.loads((work.BASE/'author-review.json').read_text()))
    write(BASE/'source-audit.json',audit)
    template=(work.BASE/'development.template').read_text()
    text=template.replace('§',BS).replace('.'+BS+'citep','.'+' '+BS+'citep')
    assert BS+'section{From language' in text and '§'not in text
    (BASE/'development.tex').write_text(text)
    bib=[]
    for s in audit['sources']:
        authors=s.get('author') or (' and '.join(s['authors']) if isinstance(s.get('authors'),list) else s['authors'])
        author=engine.shared.escape(authors)
        if s.get('kind')!='paper':author='{'+author+'}'
        version=s.get('version_date',s.get('arxiv_version','2026-10-14'))
        bib.append('@misc{'+s['integrated_citation_key']+','+NL+' author={'+author+'},'+NL+
            ' title={'+engine.shared.escape(s['title'])+'},'+NL+' year={'+str(s['year'])+'},'+NL+
            ' note={'+engine.shared.escape(version)+'}'+NL+'}'+NL)
    (BASE/'refs.bib').write_text(NL.join(bib))
    book=OLD.read_text()
    marker=BS+'input{program/execution/2026-10-14/l4-completion/v3/chapter.tex}'
    new=BS+'input{program/execution/2026-10-14/llm-identification/v2/development.tex}'
    assert book.count(marker)==1;book=book.replace(marker,marker+NL+new)
    pattern=re.compile(re.escape(BS+'bibliography{')+'([^}]+)'+re.escape('}'))
    assert len(pattern.findall(book))==1
    book=pattern.sub(lambda m:BS+'bibliography{'+m.group(1)+',program/execution/2026-10-14/llm-identification/v2/refs}',book)
    assert book.count(new)==1
    DRIVER.write_text(book)
    write(BASE/'prepared-inputs.json',{'inputs':[ref(p,'Preserved reviewed input')for p in
        [OLD,PRIOR,work.BASE/'development.template',work.BASE/'author-review.json',Path(__file__)]],
        'generated':[ref(p,'Successor source')for p in[DRIVER,BASE/'source-audit.json',BASE/'development.tex',BASE/'refs.bib']],
        'credit_policy':'No automatic mandatory-repair completion or substantive-page credit.','visual_acceptance':False})
    print(json.dumps({'prepared':str(DRIVER.relative_to(ROOT)),'new_records':len(audit['sources'])}))

def build():
    for name,value in{'BASE':BASE,'OUT':OUT,'OLD':OLD,'NAME':NAME,'DRIVER':DRIVER,'PDF':PDF,'PRIOR_AUDIT':PRIOR}.items():setattr(engine,name,value)
    with(BASE/'compile-summary.log').open('x')as stream:
        with redirect_stdout(stream):engine.build()
    report=json.loads((OUT/'build-report.json').read_text());aux=(OUT/(NAME+'.aux')).read_text()
    def page(label):
        pattern=re.escape(BS+'newlabel{'+label+'}{{')+'[^}]*'+re.escape('}{')+'([0-9]+)'
        return int(re.search(pattern,aux).group(1))
    report.update(builder=ref(Path(__file__),'Preserving LLM identification reader builder'),predecessor_pdf=ref(OLD.with_suffix('.pdf'),'Frozen738-page reader'),
        identification_sections={label:page('exec14:'+label)for label in['llm-identification','llm-identification-end']})
    engine.core.write(OUT/'build-report.json',report)
    assert report['cited_records']==558 and report['pages']>738
    result=trace.audit(DRIVER,OUT/'source-audit.json');write(BASE/'traceability-review.json',result)
    assert result['status']=='pass'and not result['issues']
    print(json.dumps({'pages':report['pages'],'cited_records':report['cited_records'],'sections':report['identification_sections'],
        'scholarly_pdfs':result['scholarly_pdfs'],'material_warnings':[w for w in report['warnings']if 'Underfull'not in w]}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','build']);a=p.parse_args()
    {'prepare':prepare,'build':build}[a.command]()
