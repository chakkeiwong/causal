#!/usr/bin/env python3
"""Preserving integrated reader for the recovered three-paper frontier tranche."""
import argparse
import json
import re
from pathlib import Path
import audit_reader_traceability_v2_20261013 as trace
import build_java_temporal_engine_20261016 as engine
import frontier_census_exact_20261017 as exact
from build_integrated_monograph_v12 import escape
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT=Path(__file__).resolve().parents[1];DOCS=ROOT/'docs'
BASE=DOCS/'program/execution/2026-10-17/census-recovery/tranche-v1'
OUT=BASE/'reader'
PREDECESSOR=DOCS/'program/execution/2026-10-17/s9/publication-v4'
OLD=DOCS/'causal_proposal_language_reuse_reviewed_v4_2026-10-17.tex'
PRIOR=PREDECESSOR/'reader/source-audit.json'
NAME='causal_proposal_frontier_census_reviewed_2026-10-17'
DRIVER=DOCS/(NAME+'.tex');PDF=DRIVER.with_suffix('.pdf')
EXTENSION=BASE/'frontier.tex'

def read(p):return json.loads(p.read_text())

def expected_driver():
    book=OLD.read_text()
    marker=r'\input{program/comprehensive-v14/work/TEXT.DRAFT.L1/chapter.tex}'
    assert book.count(marker)==1
    book=book.replace(marker,marker+'\n'+r'\input{'+str(EXTENSION.relative_to(DOCS))+'}')
    return re.sub(r'\\bibliography\{([^}]+)\}',lambda m:r'\bibliography{'+m.group(1)+','+str((BASE/'refs').relative_to(DOCS))+'}',book)

def prepare():
    assert not DRIVER.exists() and not PDF.exists() and not OUT.exists()
    audit=read(BASE/'source-audit.json');verify_bindings(audit)
    assert exact.serial(exact.calculate())==read(BASE/'exact-results.json')
    bib=[]
    for s in audit['sources']:
        bib.append('@misc{'+s['integrated_citation_key']+',\n author={{'+escape(s['author'])+
            '}},\n title={'+escape(s['title'])+'},\n year={2026},\n note={'+escape(s['version_date'])+'}\n}\n')
    (BASE/'refs.bib').write_text('\n'.join(bib))
    DRIVER.write_text(expected_driver())
    write(BASE/'prepared-inputs.json',dict(inputs=[ref(p,'Reviewed preserving input') for p in [
        OLD,PRIOR,BASE/'source-audit.json',BASE/'primary-review.json',BASE/'exact-results.json',
        BASE/'census-register.json',BASE/'task-map.json',BASE/'citation-chains.json',
        BASE/'search-observations.json',BASE.parent/'tranche-plan.md',EXTENSION,
        ROOT/'tools/audit_frontier_census_20261017.py',ROOT/'tools/frontier_census_exact_20261017.py',Path(__file__)]],
        generated=[ref(DRIVER,'Preserving integrated driver'),ref(BASE/'refs.bib','Four added references')],
        previous_records=731,added_records=4,depth_acceptance=False,census_closed=False,visual_acceptance=False))
    print(json.dumps(dict(prepared=str(DRIVER.relative_to(ROOT)),records=735,scholarly_pdfs=191)))

def build():
    verify_bindings(read(BASE/'prepared-inputs.json'))
    assert DRIVER.read_text()==expected_driver()
    assert exact.serial(exact.calculate())==read(BASE/'exact-results.json')
    assert not OUT.exists() and not PDF.exists()
    engine.BASE=BASE;engine.OUT=OUT;engine.OLD=OLD;engine.NAME=NAME
    engine.DRIVER=DRIVER;engine.PDF=PDF;engine.PRIOR_AUDIT=PRIOR
    engine.build()
    report=read(OUT/'build-report.json');assert report['cited_records']==735
    index=trace.audit(DRIVER,OUT/'source-audit.json')
    write(BASE/'traceability-review.json',index)
    assert index['status']=='pass' and not index['issues'] and index['scholarly_pdfs']==191
    print(json.dumps(dict(pages=report['pages'],records=735,scholarly_pdfs=191,traceability='pass',visual_acceptance=False)))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','build']);a=p.parse_args()
    {'prepare':prepare,'build':build}[a.command]()
