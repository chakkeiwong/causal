#!/usr/bin/env python3
"""Preserve the current monograph while integrating the Java temporal review."""
import argparse
from contextlib import redirect_stdout
import json
from pathlib import Path
import re

import audit_reader_traceability_v2_20261013 as trace
import build_native_evaluation_reader_v3_20261014 as engine
import review_java_temporal_20261015 as work
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = work.ROOT
BASE = work.BASE / 'publication-v2'
OUT = BASE / 'reader'
OLD = ROOT / 'docs/causal_proposal_latent_temporal_2026-10-15.tex'
PRIOR = work.AUDIT
NAME = 'causal_proposal_java_temporal_v2_2026-10-15'
DRIVER = ROOT / 'docs' / (NAME + '.tex')
PDF = DRIVER.with_suffix('.pdf')
BS, NL = chr(92), chr(10)


def prepare():
    assert not DRIVER.exists() and not BASE.exists()
    BASE.mkdir()
    audit = json.loads((work.BASE/'source-audit.json').read_text())
    verify_bindings(audit)
    verify_bindings(json.loads((work.BASE/'author-review.json').read_text()))
    assert work.exact() == json.loads((work.BASE/'exact-results.json').read_text())
    write(BASE/'source-audit.json', audit)
    chapter=(work.BASE/'development.tex').read_text()
    chapter=chapter.replace('.'+BS+'citep', '.~'+BS+'citep')
    for old,new in [('USD20','USD 20'),('USD8','USD 8'),('USD2','USD 2'),('USD$','USD $'),('a common date shock of variance four','independent common date shocks of variance four')]:
        chapter=chapter.replace(old,new)
    assert BS+'section{Java temporal discovery:' in chapter
    (BASE/'development.tex').write_text(chapter)
    bib=[]
    for s in audit['sources']:
        author=engine.shared.escape(s['author'])
        if s['kind']!='paper':author='{'+author+'}'
        bib.append('@misc{'+s['integrated_citation_key']+','+NL+' author={'+author+'},'+NL+
            ' title={'+engine.shared.escape(s['title'])+'},'+NL+' year={'+str(s['year'])+'},'+NL+
            ' note={'+engine.shared.escape(s['version_date'])+'}'+NL+'}'+NL)
    (BASE/'refs.bib').write_text(NL.join(bib))
    book=OLD.read_text()
    marker=BS+'input{program/execution/2026-10-14/python-temporal/v3/development.tex}'
    new=BS+'input{program/execution/2026-10-15/java-temporal/publication-v2/development.tex}'
    assert book.count(marker)==1
    book=book.replace(marker,marker+NL+new)
    pattern=re.compile(re.escape(BS+'bibliography{')+'([^}]+)'+re.escape('}'))
    assert len(pattern.findall(book))==1
    book=pattern.sub(lambda m:BS+'bibliography{'+m.group(1)+',program/execution/2026-10-15/java-temporal/publication-v2/refs}',book)
    DRIVER.write_text(book)
    write(BASE/'prepared-inputs.json',{'inputs':[ref(p,'Reviewed preserving input') for p in
        [OLD,PRIOR,work.BASE/'development.template',work.BASE/'author-review.json',Path(__file__)]],
        'generated':[ref(p,'Successor source') for p in [DRIVER,BASE/'development.tex',BASE/'source-audit.json',BASE/'refs.bib']],
        'credit_policy':'No automatic chapter depth or mandatory repair completion','visual_acceptance':False})
    print(json.dumps({'prepared':str(DRIVER.relative_to(ROOT)),'added_records':len(audit['sources'])}))


def build():
    for name,value in {'BASE':BASE,'OUT':OUT,'OLD':OLD,'NAME':NAME,'DRIVER':DRIVER,'PDF':PDF,'PRIOR_AUDIT':PRIOR}.items():
        setattr(engine,name,value)
    with (BASE/'compile-summary.log').open('x') as stream:
        with redirect_stdout(stream):engine.build()
    report=json.loads((OUT/'build-report.json').read_text());aux=(OUT/(NAME+'.aux')).read_text()
    def page(label):
        pattern=re.escape(BS+'newlabel{'+label+'}{{')+'[^}]*'+re.escape('}{')+'([0-9]+)'
        return int(re.search(pattern,aux).group(1))
    report.update(builder=ref(Path(__file__),'Preserving Java temporal reader builder'),
        predecessor_pdf=ref(OLD.with_suffix('.pdf'),'Frozen799-page reader'),
        java_temporal_sections={label:page('exec15:'+label) for label in ['java-temporal','java-temporal-end']})
    engine.core.write(OUT/'build-report.json',report)
    result=trace.audit(DRIVER,OUT/'source-audit.json');write(BASE/'traceability-review.json',result)
    assert report['cited_records']==634 and report['pages']>799
    assert result['status']=='pass' and not result['issues'] and result['scholarly_pdfs']==175
    print(json.dumps({'pages':report['pages'],'cited_records':report['cited_records'],'sections':report['java_temporal_sections'],
        'scholarly_pdfs':result['scholarly_pdfs'],'material_warnings':[w for w in report['warnings'] if 'Underfull' not in w]}))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=['prepare','build']);args=parser.parse_args()
    {'prepare':prepare,'build':build}[args.command]()
