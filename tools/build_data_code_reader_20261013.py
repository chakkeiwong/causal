#!/usr/bin/env python3
"""Preserving reader successor for the data/code agent synthesis."""
import argparse
import contextlib
import json
from pathlib import Path

import build_integrated_monograph_v12 as shared
import build_java_reader_20261013 as compiler
import master_control as core
from publish_latent_r_review_v2_20261013 import verify_bindings, write

ROOT=core.ROOT
REVIEW=ROOT/'docs/program/execution/2026-10-13/data-code'
BASE=REVIEW/'final'
OUT=BASE/'reader'
NAME='causal_proposal_data_code_2026-10-13'
OLD=ROOT/'docs/causal_proposal_causalimpact_2026-10-13.tex'
DRIVER=ROOT/'docs'/(NAME+'.tex')
PDF=DRIVER.with_suffix('.pdf')
PRIOR_AUDIT=ROOT/'docs/program/execution/2026-10-13/causalimpact-reuse/final/reader/source-audit.json'
ref=shared.ref

def expected_driver():
    text=OLD.read_text()
    marker=r'\input{program/execution/2026-10-13/agent-architecture/architecture.tex}'
    assert text.count(marker)==1
    text=text.replace(marker,marker+'\n'+r'\input{program/execution/2026-10-13/data-code/chapter.tex}',1)
    marker='program/execution/2026-10-13/causalimpact-reuse/final/refs}'
    assert text.count(marker)==1
    return text.replace(marker,'program/execution/2026-10-13/causalimpact-reuse/final/refs,program/execution/2026-10-13/data-code/final/refs}',1)

def prepare():
    assert not DRIVER.exists()
    for p in ['source-audit-v2.json','review-v2.json','findings.json']:
        verify_bindings(json.loads((REVIEW/p).read_text()))
    BASE.mkdir(exist_ok=False)
    audit=json.loads((REVIEW/'source-audit-v2.json').read_text())
    prior=json.loads(PRIOR_AUDIT.read_text())
    assert not ({s['integrated_citation_key'] for s in audit['sources']} &
                {s['integrated_citation_key'] for s in prior['sources']})
    write(BASE/'source-audit.json',audit)
    (BASE/'refs.bib').write_bytes((REVIEW/'refs.bib').read_bytes())
    DRIVER.write_text(expected_driver())
    write(BASE/'prepared-inputs.json',{'inputs':[ref(p,'Inspected or preserved input') for p in
        [OLD,PRIOR_AUDIT,REVIEW/'chapter.tex',REVIEW/'source-audit-v2.json',REVIEW/'review-v2.json',Path(__file__)]],
        'generated':[ref(p,'Preserving reader input') for p in [DRIVER,BASE/'refs.bib',BASE/'source-audit.json']]})
    print(json.dumps({'prepared':str(DRIVER.relative_to(ROOT)),'source_records':len(audit['sources'])}))

def build():
    assert not PDF.exists()
    OUT.mkdir(exist_ok=False)
    for name in ['BASE','OUT','NAME','OLD','DRIVER','PDF','PRIOR_AUDIT']:
        setattr(compiler,name,globals()[name])
    for suffix in ['.aux','.bbl','.toc','.out']:
        (OUT/(NAME+suffix)).touch(exist_ok=False)
    with (OUT/'compile-summary.txt').open('x') as stream,contextlib.redirect_stdout(stream):
        compiler.build()
    report=json.loads((OUT/'build-report.json').read_text());report.pop('java_comparison',None)
    audit=json.loads((OUT/'source-audit.json').read_text());prior=json.loads(PRIOR_AUDIT.read_text())
    audit['added_bibliography']=ref(BASE/'refs.bib','Data/code primary sources and local oracle')
    audit['additive_anchor_corrections']=prior.get('additive_anchor_corrections',[])
    core.write(OUT/'source-audit.json',audit)
    aux=(OUT/(NAME+'.aux')).read_text()
    def page(label):
        prefix=chr(92)+'newlabel{'+label+'}{{'
        line=next(x for x in aux.splitlines() if x.startswith(prefix))
        return int(line[len(prefix):].split('}{',2)[1])
    report.update(builder=ref(Path(__file__),'Bounded preserving LLM data/code compiler'),
        source_audit=ref(OUT/'source-audit.json','Whole-reader source audit'),
        pdf=ref(PDF,'Data/code agent working reader'),
        predecessor_pdf=ref(OLD.with_suffix('.pdf'),'Preserved647-page CausalImpact reader'),
        data_code={'first_printed_page':page('exec13:data-code-agents'),'live_model_calls':0,'bank_truth':False})
    core.write(OUT/'build-report.json',report)
    print(json.dumps({k:report[k] for k in ['pages','cited_records','data_code']}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','build']);args=p.parse_args()
    prepare() if args.command=='prepare' else build()
