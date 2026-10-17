#!/usr/bin/env python3
"""Reorder one misplaced bootstrap paragraph in a preserving S9 successor."""
import argparse
import json
import re
from pathlib import Path

import audit_reader_traceability_v2_20261013 as trace
import build_java_temporal_engine_20261016 as engine
import s9_successor_v2_20261017 as v2
from build_integrated_monograph_v12 import ref
from publish_latent_r_review_v2_20261013 import verify_bindings, write

ROOT=Path(__file__).resolve().parents[1];DOCS=ROOT/'docs'
BASE=DOCS/'program/execution/2026-10-17/s9';V1=BASE/'publication-v1';V2=BASE/'publication-v2'
PUB=BASE/'publication-v3';OUT=PUB/'reader'
OLD=DOCS/'causal_proposal_language_reuse_reviewed_2026-10-17.tex'
NAME='causal_proposal_language_reuse_reviewed_v3_2026-10-17'
DRIVER=DOCS/(NAME+'.tex');PDF=DRIVER.with_suffix('.pdf')
CHAPTER=PUB/'chapter.tex';SOURCE_AUDIT=PUB/'source-audit.json'
PRIOR=V1/'reader/source-audit.json'
INSERT=r'\input{program/execution/2026-10-17/s9/publication-v3/chapter.tex}'
FAILED=("Failed resamples are part of that contract. A bootstrap sample can omit a\n"
"treatment arm; deleting those replicates changes the conditional law from the\n"
"declared row bootstrap. Stratifying by arm also changes the law and may be\n"
"useful only as a declared procedure. The comparison needs all planned\n"
"replicates, valid-result indicators, diagnostics and aggregation rules.\n"
"A port that returns an interval from a selected successful subset may look\n"
"more reliable than a source that exposes failure, while answering a different\n"
"question. The proposed acquisition decision is to preserve the original\n"
"resampling path first and qualify any new dependent-data method separately.\n")
FAILED_RE=re.compile(r'Failed resamples are part of that contract\..*?dependent-data method separately\.\n',re.S)


def read(p):return json.loads(Path(p).read_text())


def prepare():
    assert not PUB.exists() and not DRIVER.exists() and not PDF.exists()
    PUB.mkdir(parents=True)
    raw=(BASE/'development.tex').read_text()
    match=FAILED_RE.search(raw); assert match
    failed=match.group(0)
    raw=raw[:match.start()]+raw[match.end():]
    marker=r'\section{Endpoint types and stable identities}'
    assert raw.count(marker)==1
    raw=raw.replace(marker,failed+'\n'+marker,1)
    extension=v2.EXTENSION
    CHAPTER.write_text(raw.rstrip()+'\n'+extension)
    audit=read(V2/'source-audit.json');write(SOURCE_AUDIT,audit)
    (PUB/'refs.bib').write_text((V2/'refs.bib').read_text())
    old=OLD.read_text();marker=r'\input{program/execution/2026-10-17/s9/development.tex}'
    assert old.count(marker)==1
    driver=old.replace(marker,INSERT)
    driver=re.sub(r'\\bibliography\{([^}]+)\}',lambda m:r'\bibliography{'+m.group(1)+',program/execution/2026-10-17/s9/publication-v3/refs}',driver)
    DRIVER.write_text(driver)
    write(PUB/'prepared-inputs.json',dict(inputs=[ref(OLD,'Preserved S9 v1 driver'),ref(PRIOR,'S9 v1 729-record audit'),
        ref(BASE/'development.tex','Preserved S9 v1 source'),ref(V2/'chapter.tex','Reviewed joint-law successor source'),
        ref(V2/'law-results.json','Exact law and decision-boundary example'),ref(SOURCE_AUDIT,'Preserved source audit'),
        ref(BASE/'plan.md','Reviewed plan'),ref(Path(__file__),'Preserving structural-repair builder')],
        generated=[ref(DRIVER,'S9 v3 preserving driver'),ref(CHAPTER,'S9 v3 chapter'),ref(PUB/'refs.bib','Bibliography copy')],
        repair='Moves the failed-resample paragraph from after the banking conclusion back into the bootstrap section; preserves the joint-law extension.',
        prior_records=729,added_records=1,visual_acceptance=False))
    print(json.dumps({'prepared':str(DRIVER.relative_to(ROOT)),'content_change':'one paragraph reordered','source_records':4}))


def build():
    assert PUB.exists() and not OUT.exists() and not PDF.exists()
    verify_bindings(read(PUB/'prepared-inputs.json'))
    engine.BASE=PUB;engine.OUT=OUT;engine.OLD=OLD;engine.NAME=NAME;engine.DRIVER=DRIVER;engine.PDF=PDF;engine.PRIOR_AUDIT=PRIOR
    engine.build()
    report=read(OUT/'build-report.json');assert report['cited_records']==730 and report['pages']>1007
    assert not [w for w in report['warnings'] if 'Underfull' not in w]
    idx=trace.audit(DRIVER,OUT/'source-audit.json');write(PUB/'traceability-review.json',idx)
    assert idx['status']=='pass' and not idx['issues'] and idx['scholarly_pdfs']==188
    write(PUB/'build-review.json',dict(status='pass',reviewer={'name':'Codex author/coordinator','kind':'author'},
        reader=report['pdf'],pages=report['pages'],cited_records=730,prior_records_preserved=729,new_records=1,
        scholarly_pdfs=188,material_warnings=[],visual_acceptance=False,
        repair='Restored the failed-resample paragraph to the row-bootstrap section before endpoint and banking sections; all v1/v2 evidence retained.'))
    print(json.dumps({'pages':report['pages'],'cited_records':730,'traceability':'pass','scholarly_pdfs':188}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','build']);a=p.parse_args();{'prepare':prepare,'build':build}[a.command]()
