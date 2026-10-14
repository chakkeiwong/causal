#!/usr/bin/env python3
"""Integrate grf design into a preserving working reader with bounded compilation."""
import argparse
import json
from pathlib import Path
import re
import subprocess

import build_java_reader_20261013 as inherited
import build_integrated_monograph_v12 as shared
import master_control as core

ROOT = core.ROOT
BASE = ROOT/'docs/program/execution/2026-10-13/grf-cxx'
OUT = BASE/'reader'
NAME = 'causal_proposal_native_forest_2026-10-13'
OLD = ROOT/'docs/causal_proposal_python_discovery_2026-10-13.tex'
DRIVER = ROOT/'docs'/(NAME+'.tex')
PDF = DRIVER.with_suffix('.pdf')
PRIOR_AUDIT = ROOT/'docs/program/execution/2026-10-13/python-discovery/reader/source-audit.json'
ref = shared.ref


def configure():
    for key in ['BASE','OUT','NAME','OLD','DRIVER','PDF','PRIOR_AUDIT']:
        setattr(inherited,key,globals()[key])


def prepare():
    configure()
    inherited.guard()
    audit=json.loads((BASE/'source-audit.json').read_text())
    shared.verify_refs(audit)
    subprocess.run(['pandoc','--from=markdown+raw_tex+tex_math_single_backslash','--to=latex','--wrap=auto',
                    str(BASE/'adapter.md'),'-o',str(BASE/'adapter.tex')],check=True,timeout=20)
    book=OLD.read_text()
    marker=r'\input{program/execution/2026-10-13/java-integration/adapter.tex}'
    assert book.count(marker)==1
    book=book.replace(marker,marker+'\n'+r'\input{program/execution/2026-10-13/grf-cxx/adapter.tex}',1)
    marker='program/execution/2026-10-13/python-discovery/refs}'
    assert book.count(marker)==1
    book=book.replace(marker,'program/execution/2026-10-13/python-discovery/refs,program/execution/2026-10-13/grf-cxx/refs}',1)
    DRIVER.write_text(book)
    entries=[]
    for s in audit['sources']:
        entries.append('@misc{'+s['integrated_citation_key']+',\n author={{'+shared.escape(s['author'])+
                       '}},\n title={'+shared.escape(s['title'])+'},\n year={'+str(s['year'])+
                       '},\n note={'+shared.escape(s['version_date'])+'}\n}\n')
    (BASE/'refs.bib').write_text('\n'.join(entries))
    core.write(BASE/'prepared-inputs.json',{'inputs':[ref(p,'Preserved build input') for p in
        [OLD,PRIOR_AUDIT,BASE/'source-audit.json',BASE/'adapter.md',BASE/'wire-examples.json',
         BASE/'reproduction-review.json',Path(__file__),ROOT/'tools/build_java_reader_20261013.py']],
        'generated':[ref(p,'Prepared source') for p in [DRIVER,BASE/'adapter.tex',BASE/'refs.bib']]})
    print(json.dumps({'prepared':str(DRIVER.relative_to(ROOT))}))


def build():
    configure()
    OUT.mkdir(exist_ok=True)
    for suffix in ['.aux','.bbl','.toc','.out']:
        p=OUT/(NAME+suffix)
        if not p.exists():p.write_text('')
    inherited.build()
    report=json.loads((OUT/'build-report.json').read_text())
    audit=json.loads((OUT/'source-audit.json').read_text())
    audit['added_bibliography']=ref(BASE/'refs.bib','grf primary-source and project bibliography')
    core.write(OUT/'source-audit.json',audit)
    aux=(OUT/(NAME+'.aux')).read_text()
    def page(label):
        return int(re.search(r'\\newlabel\{'+re.escape(label)+r'\}\{\{[^}]*\}\{(\d+)\}',aux).group(1))
    first,last=page('exec13:grf-adapter'),page('exec13:grf-adapter-end')
    report.update(builder=ref(Path(__file__),'Preserving grf integration builder'),
                  compile_routine=ref(ROOT/'tools/build_java_reader_20261013.py','Inherited bounded compiler'),
                  predecessor_pdf=ref(OLD.with_suffix('.pdf'),'Frozen505-page predecessor'),
                  pdf=ref(PDF,'Integrated native forest design working reader'),
                  source_audit=ref(OUT/'source-audit.json','Whole-reader sources'),
                  grf_adapter={'first_printed_page':first,'last_printed_page':last,'span':last-first+1,
                               'engine_execution':False,'chapter_depth_acceptance':False})
    core.write(OUT/'build-report.json',report)
    print(json.dumps({'pages':report['pages'],'citations':report['cited_records'],'grf_adapter':report['grf_adapter']}))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=['prepare','build'])
    args=parser.parse_args()
    prepare() if args.command=='prepare' else build()
