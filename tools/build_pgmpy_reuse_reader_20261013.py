#!/usr/bin/env python3
"""Preserve the commercial effects reader and integrate the pgmpy decision."""
import argparse
import contextlib
import json
from pathlib import Path
import re
import build_integrated_monograph_v12 as shared
import build_java_reader_20261013 as inherited
import master_control as core

ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-13/pgmpy-reuse'
OUT=BASE/'reader'
NAME='causal_proposal_pgmpy_2026-10-13'
OLD=ROOT/'docs/causal_proposal_commercial_effects_2026-10-13.tex'
DRIVER=ROOT/'docs'/(NAME+'.tex')
PDF=DRIVER.with_suffix('.pdf')
PRIOR_AUDIT=ROOT/'docs/program/execution/2026-10-13/commercial-heterogeneity/reader/source-audit.json'
ref=shared.ref

def configure():
    for key in ['BASE','OUT','NAME','OLD','DRIVER','PDF','PRIOR_AUDIT']:setattr(inherited,key,globals()[key])

def expected_driver():
    book=OLD.read_text();marker=r'\input{program/execution/2026-10-13/pcalg-reuse/decision.tex}'
    assert book.count(marker)==1
    book=book.replace(marker,marker+'\n'+r'\input{program/execution/2026-10-13/pgmpy-reuse/decision.tex}',1)
    marker='program/execution/2026-10-13/commercial-heterogeneity/refs}'
    assert book.count(marker)==1
    return book.replace(marker,'program/execution/2026-10-13/commercial-heterogeneity/refs,program/execution/2026-10-13/pgmpy-reuse/refs}',1)

def prepare():
    configure();inherited.guard()
    audit=json.loads((BASE/'source-audit.json').read_text());shared.verify_refs(audit)
    assert json.loads((BASE/'decision-review.json').read_text())['status']=='pass'
    DRIVER.write_text(expected_driver())
    (BASE/'refs.bib').write_text('\n'.join('@misc{'+s['integrated_citation_key']+',\n author={{'+shared.escape(s['author'])+'}},\n title={'+shared.escape(s['title'])+'},\n year={'+str(s['year'])+'},\n note={'+shared.escape(s['version_date'])+'}\n}\n' for s in audit['sources']))
    review={'status':'pass','issues':[],'reviewer':{'name':'Codex author/coordinator','kind':'author'},'scope':'Restricted reuse decision, implementation boundaries and exact references','findings':['Known observed-DAG candidate path is selected; graph truth, numerical effects and uncertainty are not awarded by that choice.','Static source trace distinguishes role-presence checking from complete adjustment validation; no upstream execution claimed.','Source minimum-variance branch is unimplemented; minimal is not minimum-cardinality.','PDAG conversion warning/arbitrary fallback is preserved as a refusal boundary.','Two separate graph references agree on26064 finite queries; exact mediated total effect6 and adjusted slope0 are generated.','MIT permission, dependency declarations, upgrade obligations and actual runtime prerequisites remain distinct.'],'evidence':[ref(BASE/p,p) for p in ['source-selection.json','source-followup.json','primary-review.json','oracle-results.json','adapter-contract.json','decision-review.json','source-audit.json','decision.tex']],'visual_acceptance':False,'independent_review':False}
    core.write(BASE/'manuscript-review.json',review)
    core.write(BASE/'prepared-inputs.json',{'inputs':[ref(p,'Reviewed preserving input') for p in [OLD,PRIOR_AUDIT,BASE/'decision.tex',BASE/'source-audit.json',BASE/'manuscript-review.json',Path(__file__)]],'generated':[ref(DRIVER,'Preserving reader driver'),ref(BASE/'refs.bib','New audited citations')]})
    print(json.dumps({'prepared':str(DRIVER.relative_to(ROOT)),'new_citations':2}))

def build():
    configure();OUT.mkdir(exist_ok=True)
    for suffix in ['.aux','.bbl','.toc','.out']:
        p=OUT/(NAME+suffix)
        if not p.exists():p.write_text('')
    with (OUT/'compile-summary.txt').open('w') as output,contextlib.redirect_stdout(output):inherited.build()
    audit=json.loads((OUT/'source-audit.json').read_text());audit['added_bibliography']=ref(BASE/'refs.bib','Pinned pgmpy source and exact reference citations');core.write(OUT/'source-audit.json',audit)
    report=json.loads((OUT/'build-report.json').read_text());report.pop('java_comparison',None)
    aux=(OUT/(NAME+'.aux')).read_text()
    def page(label):return int(re.search(r'\\newlabel\{'+re.escape(label)+r'\}\{\{[^}]*\}\{(\d+)\}',aux).group(1))
    report.update(builder=ref(Path(__file__),'Preserving pgmpy integration builder'),compile_routine=ref(ROOT/'tools/build_java_reader_20261013.py','Unchanged bounded compiler'),pdf=ref(PDF,'Working pgmpy reuse successor'),predecessor_pdf=ref(OLD.with_suffix('.pdf'),'Preserved608-page commercial effects reader'),source_audit=ref(OUT/'source-audit.json','Whole-reader traceability'),pgmpy_reuse={'first_printed_page':page('exec13:pgmpy-reuse'),'last_printed_page':page('exec13:pgmpy-reuse-end'),'engine_executed':False})
    core.write(OUT/'build-report.json',report)
    print(json.dumps({k:report[k] for k in ['pages','cited_records','pgmpy_reuse']}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','build']);a=p.parse_args();prepare() if a.command=='prepare' else build()
