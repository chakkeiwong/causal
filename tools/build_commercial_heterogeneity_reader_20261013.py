#!/usr/bin/env python3
"""Preserving commercial effects comparison and temporal design clarification."""
import argparse
import json
from pathlib import Path
import re
import build_integrated_monograph_v12 as shared
import build_java_reader_20261013 as inherited
import master_control as core

ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-13/commercial-heterogeneity'
OUT=BASE/'reader'
NAME='causal_proposal_commercial_effects_2026-10-13'
OLD=ROOT/'docs/causal_proposal_funding_2026-10-13.tex'
DRIVER=ROOT/'docs'/(NAME+'.tex')
PDF=DRIVER.with_suffix('.pdf')
PRIOR_AUDIT=ROOT/'docs/program/execution/2026-10-13/funding-journey/reader/source-audit.json'
MASTER=ROOT/'docs/program/repair-v12/integrated-reader/chapters/master_execution.tex'
ref=shared.ref

def configure():
    for key in ['BASE','OUT','NAME','OLD','DRIVER','PDF','PRIOR_AUDIT']:setattr(inherited,key,globals()[key])

def expected_driver():
    book=OLD.read_text()
    for marker,extra in [(r'\input{program/execution/2026-10-13/commercial-identification/comparison-final.tex}',r'\input{program/execution/2026-10-13/commercial-heterogeneity/comparison.tex}'),(r'\input{program/execution/2026-10-13/temporal-graphs/chapter.tex}',r'\input{program/execution/2026-10-13/commercial-heterogeneity/temporal-clarification.tex}')]:
        assert book.count(marker)==1
        book=book.replace(marker,marker+'\n'+extra,1)
    old=r'\input{program/repair-v12/integrated-reader/chapters/master_execution.tex}'
    assert book.count(old)==1
    book=book.replace(old,r'\input{program/execution/2026-10-13/commercial-heterogeneity/master-execution-preserving.tex}',1)
    old='program/execution/2026-10-13/funding-journey/refs}'
    assert book.count(old)==1
    return book.replace(old,'program/execution/2026-10-13/funding-journey/refs,program/execution/2026-10-13/commercial-heterogeneity/refs}',1)

def prepare():
    configure();inherited.guard()
    audit=json.loads((BASE/'source-audit.json').read_text());shared.verify_refs(audit)
    assert json.loads((BASE/'exact-review.json').read_text())['status']=='pass'
    book=MASTER.read_text()
    old='The finite-availability screen fails despite conservative coverage. Such sets identify ambiguity, not decision-useful precision.'
    assert book.count(old)==1
    new=r'''The overall finite-availability screen fails because the weak-relevance and unrestricted latent cells never return finite sets. The persistent cell itself passes its original raw-fraction rule: $507/512=.990234375$ exceeds $.99$. Its five whole-line outcomes remain visible, and none of these availability counts establishes decision-useful precision or a confidence lower bound of $.99$. Section~\ref{exec13:temporal-design-review} explains the distinction and the successor design requirements \cite{exec13_temporal_design}.'''
    (BASE/'master-execution-preserving.tex').write_text(book.replace(old,new,1))
    DRIVER.write_text(expected_driver())
    (BASE/'refs.bib').write_text('\n'.join('@misc{'+s['integrated_citation_key']+',\n author={{'+shared.escape(s['author'])+'}},\n title={'+shared.escape(s['title'])+'},\n year={'+str(s['year'])+'},\n note={'+shared.escape(s['version_date'])+'}\n}\n' for s in audit['sources']))
    review={'status':'pass','issues':[],'reviewer':{'name':'Codex author/coordinator','kind':'author'},'scope':'Substantive comparison, separate arithmetic review and temporal design clarification','findings':['All seventeen families retained; only ten complete new technical documents used.','Raw acquisition times and exit codes not invented; exact-cutoff identity remains qualified.','Stata target homogeneity assumption distinguished from the authored coarsening counterexample.','JMP Uplift and Causal Treatment have distinct version and method scopes; image-only equations are not inferred.','DataRobot overview is not promoted to inspected notebook or native CATE evidence.','Separate finite-population arithmetic verifies targets, policy costs, clipping and selection examples.','Temporal persistent count passes raw availability; lower-bound coverage screen and unknown-law limits remain distinct.','No vendor, bank, independent-review or visual-acceptance claim.'],'evidence':[ref(BASE/p,p) for p in ['plan-review.md','comparison.tex','temporal-clarification.tex','source-audit.json','exact-review.json','omissions-register.json']],'visual_acceptance':False,'independent_review':False}
    core.write(BASE/'manuscript-review.json',review)
    core.write(BASE/'prepared-inputs.json',{'inputs':[ref(p,'Preserved/reviewed input') for p in [OLD,MASTER,PRIOR_AUDIT,BASE/'comparison.tex',BASE/'temporal-clarification.tex',BASE/'source-audit.json',BASE/'manuscript-review.json',Path(__file__)]],'generated':[ref(p,'New preserving reader input') for p in [DRIVER,BASE/'master-execution-preserving.tex',BASE/'refs.bib']]})
    print(json.dumps({'prepared':str(DRIVER.relative_to(ROOT)),'new_citations':len(audit['sources'])}))

def build():
    configure();OUT.mkdir(exist_ok=True)
    for suffix in ['.aux','.bbl','.toc','.out']:
        p=OUT/(NAME+suffix)
        if not p.exists():p.write_text('')
    inherited.build()
    audit=json.loads((OUT/'source-audit.json').read_text());audit['added_bibliography']=ref(BASE/'refs.bib','Commercial heterogeneity and temporal feasibility sources');core.write(OUT/'source-audit.json',audit)
    report=json.loads((OUT/'build-report.json').read_text());report.pop('java_comparison',None)
    aux=(OUT/(NAME+'.aux')).read_text()
    def page(label):return int(re.search(r'\\newlabel\{'+re.escape(label)+r'\}\{\{[^}]*\}\{(\d+)\}',aux).group(1))
    report.update(builder=ref(Path(__file__),'Preserving commercial heterogeneity builder'),compile_routine=ref(ROOT/'tools/build_java_reader_20261013.py','Unchanged bounded compiler'),pdf=ref(PDF,'Working commercial effects successor'),predecessor_pdf=ref(OLD.with_suffix('.pdf'),'Preserved 601-page funding reader'),source_audit=ref(OUT/'source-audit.json','Whole-reader audit'),commercial_heterogeneity={'first_printed_page':page('exec13:commercial-heterogeneity'),'last_printed_page':page('exec13:commercial-heterogeneity-end'),'coverage_acceptance':False},temporal_design={'first_printed_page':page('exec13:temporal-design-review'),'last_printed_page':page('exec13:temporal-design-review-end'),'final_study_approved':False})
    core.write(OUT/'build-report.json',report)
    print(json.dumps({k:report[k] for k in ['pages','cited_records','commercial_heterogeneity','temporal_design']}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','build']);a=p.parse_args();prepare() if a.command=='prepare' else build()
