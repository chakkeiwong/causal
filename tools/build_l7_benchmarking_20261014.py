#!/usr/bin/env python3
"""Preserve and integrate L7 benchmarking analysis in a working reader."""
import argparse
from contextlib import redirect_stdout
import json
from pathlib import Path
import re

import audit_reader_traceability_v2_20261013 as trace
import build_native_evaluation_reader_v3_20261014 as engine
import develop_l7_benchmarking_20261014 as work
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = work.ROOT
BASE = work.BASE/'publication'
OUT = BASE/'reader'
OLD = ROOT/'docs/causal_proposal_failure_recovery_2026-10-14.tex'
PRIOR = work.PRIOR
NAME = 'causal_proposal_benchmarking_2026-10-14'
DRIVER = ROOT/'docs'/(NAME+'.tex')
PDF = DRIVER.with_suffix('.pdf')
CHAPTER = ROOT/'docs/program/comprehensive-v14/work/TEXT.DRAFT.L7/chapter.tex'
BS, NL = chr(92), chr(10)


def prepare():
    assert not DRIVER.exists() and not CHAPTER.exists()
    BASE.mkdir(exist_ok=False)
    audit = json.loads((work.BASE/'source-audit.json').read_text())
    verify_bindings(audit)
    verify_bindings(json.loads((work.BASE/'derivation-review.json').read_text()))
    assert work.calculate() == json.loads((work.BASE/'exact-results.json').read_text())
    write(BASE/'source-audit.json', audit)
    content = (work.BASE/'development.template').read_text().replace('§', BS)
    assert '§' not in content
    (BASE/'development.tex').write_text(content)
    bib = []
    for s in audit['sources']:
        bib.append('@misc{'+s['integrated_citation_key']+','+NL+
                   ' author={{'+engine.shared.escape(s['author'])+'}},'+NL+
                   ' title={'+engine.shared.escape(s['title'])+'},'+NL+
                   ' year={2026},'+NL+' note={'+s['version_date']+'}'+NL+'}'+NL)
    (BASE/'refs.bib').write_text(NL.join(bib))
    inputs = [BS+'input{'+p+'}' for p in work.INHERITED]
    addition = BS+'input{program/execution/2026-10-14/l7-benchmarking/publication/development.tex}'
    CHAPTER.parent.mkdir(exist_ok=True)
    CHAPTER.write_text(NL.join(inputs+[addition])+NL)
    book = OLD.read_text()
    block = NL.join(inputs)
    assert book.count(block) == 1
    wrapper = BS+'input{program/comprehensive-v14/work/TEXT.DRAFT.L7/chapter.tex}'
    book = book.replace(block, wrapper)
    pattern = re.compile(re.escape(BS+'bibliography{')+'([^}]+)'+re.escape('}'))
    assert len(pattern.findall(book)) == 1
    book = pattern.sub(lambda m: BS+'bibliography{'+m.group(1)+
                       ',program/execution/2026-10-14/l7-benchmarking/publication/refs}', book)
    DRIVER.write_text(book)
    write(BASE/'prepared-inputs.json',{
        'inputs':[ref(p,'Reviewed preserving input') for p in
                  [OLD,PRIOR,work.BASE/'development.template',work.BASE/'derivation-review.json',
                   work.BASE/'primary-review.json',Path(__file__).resolve()]],
        'generated':[ref(p,'Successor source') for p in
                     [DRIVER,CHAPTER,BASE/'source-audit.json',BASE/'development.tex',BASE/'refs.bib']],
        'credit_policy':'Review each substantive page after excluding repeats and adjacent-chapter credit.',
        'visual_acceptance':False,
    })
    print(json.dumps({'prepared':str(DRIVER.relative_to(ROOT)),'new_records':len(audit['sources'])}))


def build():
    for key, value in {'BASE':BASE,'OUT':OUT,'OLD':OLD,'NAME':NAME,'DRIVER':DRIVER,
                       'PDF':PDF,'PRIOR_AUDIT':PRIOR}.items():
        setattr(engine,key,value)
    with (BASE/'compile-summary.log').open('x') as stream:
        with redirect_stdout(stream):
            engine.build()
    report=json.loads((OUT/'build-report.json').read_text())
    aux=(OUT/(NAME+'.aux')).read_text()
    def page(label):
        pattern=re.escape(BS+'newlabel{'+label+'}{{')+'[^}]*'+re.escape('}{')+'([0-9]+)'
        return int(re.search(pattern,aux).group(1))
    report.update(
        builder=ref(Path(__file__).resolve(),'Preserving L7 reader builder'),
        predecessor_pdf=ref(OLD.with_suffix('.pdf'),'Frozen750-page reader'),
        chapter_sections={label:page(label) for label in [
            'la:evaluation','exec14:l7-development','exec14:l7-adjudication',
            'exec14:l7-metamorphic','exec14:l7-oracles','exec14:l7-development-end','la:economics']},
    )
    engine.core.write(OUT/'build-report.json',report)
    assert report['cited_records']==570 and report['pages']>750
    result=trace.audit(DRIVER,OUT/'source-audit.json')
    write(BASE/'traceability-review.json',result)
    assert result['status']=='pass' and not result['issues']
    print(json.dumps({'pages':report['pages'],'cited_records':report['cited_records'],
                      'sections':report['chapter_sections'],'scholarly_pdfs':result['scholarly_pdfs'],
                      'material_warnings':[w for w in report['warnings'] if 'Underfull' not in w]}))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('command',choices=['prepare','build'])
    args=parser.parse_args()
    {'prepare':prepare,'build':build}[args.command]()
