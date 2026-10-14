#!/usr/bin/env python3
"""Integrate bounded commercial survival comparison, preserving all earlier text."""
import argparse
from contextlib import redirect_stdout
import json
from pathlib import Path
import re
import audit_reader_traceability_v2_20261013 as trace
import build_native_evaluation_reader_v3_20261014 as engine
import commercial_survival_examples_20261014 as exact
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT=engine.ROOT
BASE=ROOT/'docs/program/execution/2026-10-14/commercial-survival/v2'
OUT=BASE/'reader'
OLD=ROOT/'docs/causal_proposal_banking_economics_v3_2026-10-14.tex'
PRIOR=ROOT/'docs/program/execution/2026-10-14/l8-economics/v3/reader/source-audit.json'
NAME='causal_proposal_commercial_survival_2026-10-15'
DRIVER=ROOT/'docs'/(NAME+'.tex')
PDF=DRIVER.with_suffix('.pdf')
BS,NL=chr(92),chr(10)


def prepare():
    assert not DRIVER.exists() and not (BASE/'prepared-inputs.json').exists()
    audit=json.loads((BASE/'source-audit.json').read_text());verify_bindings(audit)
    assert exact.calculate()==json.loads((BASE/'exact-results.json').read_text())
    bib=[]
    for s in audit['sources']:
        bib.append('@misc{'+s['integrated_citation_key']+','+NL+
            ' author={{'+engine.shared.escape(s['author'])+'}},'+NL+
            ' title={'+engine.shared.escape(s['title'])+'},'+NL+
            ' year={'+str(s['year'])+'},'+NL+
            ' note={'+engine.shared.escape(s['version_date'])+'}'+NL+'}'+NL)
    (BASE/'refs.bib').write_text(NL.join(bib))
    book=OLD.read_text();marker=BS+'input{program/execution/2026-10-13/commercial-iv-rd/comparison.tex}'
    assert book.count(marker)==1
    book=book.replace(marker,marker+NL+BS+'input{'+str((BASE/'comparison.tex').relative_to(ROOT/'docs'))+'}')
    pattern=re.compile(re.escape(BS+'bibliography{')+'([^}]+)'+re.escape('}'))
    assert len(pattern.findall(book))==1
    book=pattern.sub(lambda m:BS+'bibliography{'+m.group(1)+','+str((BASE/'refs').relative_to(ROOT/'docs'))+'}',book)
    DRIVER.write_text(book)
    write(BASE/'prepared-inputs.json',{'prepared_on':'2026-10-15 Asia/Shanghai',
        'inputs':[ref(p,'Preserved input') for p in [OLD,PRIOR,BASE/'source-audit.json',BASE/'primary-review.json',
            BASE/'derivation-review.json',BASE/'exact-results.json',BASE/'omissions-register.json',Path(__file__).resolve()]],
        'generated':[ref(p,'Integrated successor source') for p in [DRIVER,BASE/'comparison.tex',BASE/'refs.bib']],
        'transport_failure':'First combined TeX patch contained unescaped template-string delimiters and did not execute. Two smaller escaped patches succeeded; no bound original changed.',
        'scientific_scope':'Eight inspected families and one unavailable; exact scenarios, no vendor execution or bank evidence.',
        'visual_acceptance':False})
    print(json.dumps({'prepared':str(DRIVER.relative_to(ROOT)),'added_citation_records':len(audit['sources'])}))


def build():
    for key,value in {'BASE':BASE,'OUT':OUT,'OLD':OLD,'PRIOR_AUDIT':PRIOR,'NAME':NAME,'DRIVER':DRIVER,'PDF':PDF}.items():
        setattr(engine,key,value)
    with (BASE/'compile-summary.log').open('x') as stream:
        with redirect_stdout(stream):engine.build()
    report=json.loads((OUT/'build-report.json').read_text());aux=(OUT/(NAME+'.aux')).read_text()
    def page(label):return int(re.search(re.escape(BS+'newlabel{'+label+'}{{')+'[^}]*'+re.escape('}{')+'([0-9]+)',aux).group(1))
    report.update(builder=ref(Path(__file__).resolve(),'Preserving commercial survival builder'),
        predecessor_pdf=ref(OLD.with_suffix('.pdf'),'Frozen780-page economics reader'),
        sections={label:page(label) for label in ['exec15:commercial-survival','exec15:commercial-survival-end']})
    engine.core.write(OUT/'build-report.json',report)
    audited=trace.audit(DRIVER,OUT/'source-audit.json');write(BASE/'traceability-review.json',audited)
    assert audited['status']=='pass' and not audited['issues'] and audited['scholarly_pdfs']==172
    assert report['cited_records']==614
    print(json.dumps({'pages':report['pages'],'cited_records':report['cited_records'],'sections':report['sections'],
        'scholarly_pdfs':audited['scholarly_pdfs'],'material_warnings':[w for w in report['warnings'] if 'Underfull' not in w]}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','build']);a=p.parse_args()
    {'prepare':prepare,'build':build}[a.command]()
