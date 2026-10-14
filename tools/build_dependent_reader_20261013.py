#!/usr/bin/env python3
"""Integrate the reviewed discovery exercise and dependent-learning argument."""
import argparse
import json
from pathlib import Path
import re

import build_java_reader_20261013 as inherited
import build_integrated_monograph_v12 as shared
import master_control as core

ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-13/dependent-learner'
OUT=BASE/'reader'
NAME='causal_proposal_dependent_learning_2026-10-13'
OLD=ROOT/'docs/causal_proposal_native_discovery_2026-10-13.tex'
DRIVER=ROOT/'docs'/(NAME+'.tex')
PDF=DRIVER.with_suffix('.pdf')
PRIOR_AUDIT=ROOT/'docs/program/execution/2026-10-13/cxx-discovery/reader/source-audit.json'
ref=shared.ref


def configure():
    for key in ['BASE','OUT','NAME','OLD','DRIVER','PDF','PRIOR_AUDIT']:
        setattr(inherited,key,globals()[key])


def prepare():
    configure();inherited.guard()
    audit=json.loads((BASE/'source-audit.json').read_text());shared.verify_refs(audit)
    book=OLD.read_text()
    marker=r'\label{integrated:integration-end}'
    assert book.count(marker)==1
    book=book.replace(marker,r'\input{program/execution/2026-10-13/discovery-journey/section.tex}'+'\n\n'+marker,1)
    marker=r'\input{program/execution/2026-10-13/temporal-graphs/chapter.tex}'
    assert book.count(marker)==1
    book=book.replace(marker,marker+'\n'+r'\input{program/execution/2026-10-13/dependent-learner/chapter.tex}',1)
    marker='program/execution/2026-10-13/cxx-discovery/refs}'
    assert book.count(marker)==1
    book=book.replace(marker,'program/execution/2026-10-13/cxx-discovery/refs,program/execution/2026-10-13/dependent-learner/refs}',1)
    marker=r"\addcontentsline{toc}{chapter}{Reader's contract}"
    assert book.count(marker)==1
    book=book.replace(marker,marker+'\n\n'+
        r'Chapter~\ref{exec13:dependent-pilot} derives a restricted independent-pilot'+ '\n'+
        'learning construction with explicit nuisance error, finite dependent evaluation\n'+
        'and weak-instrument sets. Exact references support the derivation; useful\n'+
        'precision and a fresh qualification study remain open.\n'+
        r'Section~\ref{exec13:discovery-journey} reports 98 registered local workflow'+ '\n'+
        'calls, preserving graph ambiguity, refusals, artifact failures and restart\n'+
        'identity. This does not install a discovery engine or establish live-model performance.\n',1)
    DRIVER.write_text(book)
    entries=[]
    for s in audit['sources']:
        entries.append('@misc{'+s['integrated_citation_key']+',\n author={{'+shared.escape(s['author'])+
                       '}},\n title={'+shared.escape(s['title'])+'},\n year={2026},\n note={'+shared.escape(s['version_date'])+'}\n}\n')
    (BASE/'refs.bib').write_text('\n'.join(entries))
    inputs=[OLD,PRIOR_AUDIT,Path(__file__),BASE/'source-audit.json',BASE/'argument-review.json',
            BASE/'chapter.tex',BASE/'exact-results.json',
            ROOT/'docs/program/execution/2026-10-13/discovery-journey/section.tex']
    core.write(BASE/'prepared-inputs.json',{'inputs':[ref(p,'Reviewed preserving input') for p in inputs],
               'generated':[ref(DRIVER,'Preserving driver'),ref(BASE/'refs.bib','New project source records')]})
    print(json.dumps({'prepared':str(DRIVER.relative_to(ROOT))}))


def build():
    configure();OUT.mkdir(exist_ok=True)
    for suffix in ['.aux','.bbl','.toc','.out']:
        p=OUT/(NAME+suffix)
        if not p.exists():p.write_text('')
    inherited.build()
    audit=json.loads((OUT/'source-audit.json').read_text())
    audit['added_bibliography']=ref(BASE/'refs.bib','Derived and registered project evidence')
    core.write(OUT/'source-audit.json',audit)
    report=json.loads((OUT/'build-report.json').read_text());aux=(OUT/(NAME+'.aux')).read_text()
    def page(label):
        return int(re.search(r'\\newlabel\{'+re.escape(label)+r'\}\{\{[^}]*\}\{(\d+)\}',aux).group(1))
    report.pop('java_comparison',None)
    report.update(builder=ref(Path(__file__),'Preserving discovery and dependent-learner builder'),
                  compile_routine=ref(ROOT/'tools/build_java_reader_20261013.py','Inherited bounded compiler'),
                  predecessor_pdf=ref(OLD.with_suffix('.pdf'),'Frozen 553-page predecessor'),
                  pdf=ref(PDF,'Integrated working reader with reviewed discovery and learning additions'),
                  source_audit=ref(OUT/'source-audit.json','Whole-reader source audit'))
    for name,label in [('discovery_journey','exec13:discovery-journey'),('dependent_learning','exec13:dependent-pilot')]:
        first,last=page(label),page(label+'-end')
        report[name]={'first_printed_page':first,'last_printed_page':last,'physical_span':last-first+1,
                      'mandatory_repair_acceptance':False}
    core.write(OUT/'build-report.json',report)
    print(json.dumps({k:report[k] for k in ['pages','cited_records','discovery_journey','dependent_learning','warnings']}))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=['prepare','build']);args=parser.parse_args()
    prepare() if args.command=='prepare' else build()
