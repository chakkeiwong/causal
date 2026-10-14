#!/usr/bin/env python3
"""Compile a preserving reader containing the reviewed L5 workflow development."""
import argparse
import json
from pathlib import Path
import re

import build_native_evaluation_reader_v3_20261014 as engine
import develop_longitudinal_workflow_20261014 as work
import master_control as core

ROOT=core.ROOT
DOCS=ROOT/'docs'
BASE=work.BASE/'publication'
OUT=BASE/'reader'
OLD=DOCS/'causal_proposal_native_evaluation_v3_2026-10-14.tex'
NAME='causal_proposal_longitudinal_workflow_2026-10-14'
DRIVER=DOCS/(NAME+'.tex')
PDF=DRIVER.with_suffix('.pdf')
ref=work.ref


def configure():
    engine.BASE=BASE
    engine.OUT=OUT
    engine.OLD=OLD
    engine.NAME=NAME
    engine.DRIVER=DRIVER
    engine.PDF=PDF
    engine.PRIOR_AUDIT=work.PRIOR


def prepare():
    assert not DRIVER.exists() and not (BASE/'prepared-inputs.json').exists()
    work.verify()
    text=OLD.read_text()
    marker=r'\input{program/repair-v12/work/LA04/chapter-draft.tex}'
    replacement=r'\input{program/comprehensive-v14/work/TEXT.DRAFT.L5/chapter.tex}'
    assert text.count(marker)==1
    text=text.replace(marker,replacement)
    text=re.sub(r'\\bibliography\{([^}]+)\}',lambda m:r'\bibliography{'+m.group(1)+
                ',program/execution/2026-10-14/l5-workflow/refs}',text)
    DRIVER.write_text(text)
    BASE.mkdir(parents=True,exist_ok=True)
    audit=json.loads((work.BASE/'source-audit.json').read_text())
    work.write(BASE/'source-audit.json',audit)
    work.write(BASE/'prepared-inputs.json',{
        'inputs':[ref(p,'Preserved or reviewed source input') for p in
                  [OLD,work.PRIOR,work.CHAPTER,work.ADDITION,work.BASE/'refs.bib',
                   work.BASE/'source-audit.json',work.BASE/'primary-review.json',
                   work.BASE/'exact-oracle.json',work.BASE/'plan-review.json',Path(__file__)]],
        'generated':[ref(DRIVER,'Preserving chapter insertion and bibliography addition'),
                     ref(BASE/'source-audit.json','One new project-source identity')],
        'credit_policy':'Rendered text/content review must deduct generic workflow, architecture, data/code and repeated material; no automatic repair or page credit.',
        'visual_acceptance':False})
    print(json.dumps({'prepared':str(DRIVER.relative_to(ROOT)),'one_additional_source':True}))


def build():
    configure()
    engine.build()
    report=json.loads((OUT/'build-report.json').read_text())
    aux=(OUT/(NAME+'.aux')).read_text()
    def page(label):
        return int(re.search(r'\\newlabel\{'+re.escape(label)+r'\}\{\{[^}]*\}\{(\d+)\}',aux).group(1))
    report.update(builder=ref(Path(__file__),'Preserving L5 builder using unchanged compile/audit engine'),
                  predecessor_pdf=ref(OLD.with_suffix('.pdf'),'Frozen692-page reader'),
                  workflow_sections={name:page('exec14:l5-'+name) for name in
                                     ['servicing','retention','panel','observations','handoffs','development-end']})
    core.write(OUT/'build-report.json',report)
    print(json.dumps({'pages':report['pages'],'cited_records':report['cited_records'],
                      'workflow_sections':report['workflow_sections']}))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('command',choices=['prepare','build'])
    args=parser.parse_args()
    prepare() if args.command=='prepare' else build()
