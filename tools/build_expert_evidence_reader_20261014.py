#!/usr/bin/env python3
"""Integrate expert evidence without changing any earlier reader inputs."""
import argparse
from contextlib import redirect_stdout
import json
from pathlib import Path
import re
import subprocess

import audit_reader_traceability_v2_20261013 as trace
import build_native_evaluation_reader_v3_20261014 as engine
import review_expert_evidence_20261014 as work
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings

ROOT=work.ROOT
DOCS=ROOT/'docs'
BASE=work.BASE/'publication'
OUT=BASE/'reader'
OLD=DOCS/'causal_proposal_software_lifecycle_2026-10-14.tex'
NAME='causal_proposal_expert_evidence_2026-10-14'
DRIVER=DOCS/(NAME+'.tex')
PDF=DRIVER.with_suffix('.pdf')
PRIOR=DOCS/'program/execution/2026-10-14/causalnex-reuse/publication/reader/source-audit.json'


def prepare():
    assert not DRIVER.exists() and not (BASE/'prepared-inputs.json').exists()
    primary=json.loads((work.BASE/'primary-review.json').read_text())
    audit=json.loads((work.BASE/'source-audit.json').read_text())
    for obj in [primary,audit]:verify_bindings(obj)
    assert work.calculate()==json.loads((work.BASE/'exact-oracle.json').read_text())
    BASE.mkdir(exist_ok=True)
    subprocess.run(['pandoc','--from=markdown+raw_tex+tex_math_dollars','--to=latex','--wrap=auto',
        str(work.SYN),'-o',str(BASE/'development.tex')],check=True,timeout=20)
    write(BASE/'source-audit.json',audit)
    bib=[]
    for source in audit['sources']:
        author=engine.shared.escape(source['author'])
        if source['kind']!='paper':author='{'+author+'}'
        bib.append('@misc{'+source['integrated_citation_key']+',\n author={'+author+'},\n title={'+
            engine.shared.escape(source['title'])+'},\n year={'+str(source['year'])+'},\n note={'+
            engine.shared.escape(source['version_date'])+'}\n}\n')
    (BASE/'refs.bib').write_text('\n'.join(bib))
    text=OLD.read_text()
    marker=r'\input{program/execution/2026-10-13/llm-census/measurement.tex}'
    assert text.count(marker)==1
    text=text.replace(marker,marker+'\n'+r'\input{program/execution/2026-10-14/expert-evidence/publication/development.tex}')
    text=re.sub(r'\\bibliography\{([^}]+)\}',lambda m:r'\bibliography{'+m.group(1)+
        ',program/execution/2026-10-14/expert-evidence/publication/refs}',text)
    DRIVER.write_text(text)
    write(BASE/'prepared-inputs.json',{'inputs':[ref(p,'Preserved or reviewed input') for p in
        [OLD,PRIOR,work.SYN,work.BASE/'primary-review.json',work.BASE/'source-audit.json',
         work.BASE/'exact-oracle.json',work.BASE/'candidate-reassessment.json',Path(__file__)]],
        'generated':[ref(p,'Successor source') for p in [DRIVER,BASE/'development.tex',BASE/'refs.bib',BASE/'source-audit.json']],
        'credit_policy':'No automatic substantive-page credit; repeated background must be deducted at Q1.',
        'visual_acceptance':False})
    print(json.dumps({'prepared':str(DRIVER.relative_to(ROOT)),'new_sources':4,'new_authentic_papers':2}))


def build():
    for name,value in {'BASE':BASE,'OUT':OUT,'OLD':OLD,'NAME':NAME,'DRIVER':DRIVER,'PDF':PDF,'PRIOR_AUDIT':PRIOR}.items():
        setattr(engine,name,value)
    with (BASE/'compile-summary.log').open('x') as stream:
        with redirect_stdout(stream):engine.build()
    report=json.loads((OUT/'build-report.json').read_text())
    aux=(OUT/(NAME+'.aux')).read_text()
    report.update(builder=ref(Path(__file__),'Preserving expert-evidence builder'),
        predecessor_pdf=ref(OLD.with_suffix('.pdf'),'Frozen705-page working reader'),
        expert_sections={name:int(re.search(r'\\newlabel\{exec14:'+name+r'\}\{\{[^}]*\}\{(\d+)\}',aux).group(1))
                         for name in ['expert-evidence','expert-evidence-end']})
    engine.core.write(OUT/'build-report.json',report)
    result=trace.audit(DRIVER,OUT/'source-audit.json')
    write(BASE/'traceability-review.json',result)
    assert result['status']=='pass' and not result['issues']
    print(json.dumps({'pages':report['pages'],'cited_records':report['cited_records'],
        'sections':report['expert_sections'],'scholarly_pdfs':result['scholarly_pdfs'],
        'material_warnings':[w for w in report['warnings'] if 'Underfull' not in w]}))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('command',choices=['prepare','build'])
    args=parser.parse_args()
    prepare() if args.command=='prepare' else build()
