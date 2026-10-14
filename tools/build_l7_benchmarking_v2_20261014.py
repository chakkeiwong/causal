#!/usr/bin/env python3
"""Preserve the first L7 candidate and repair inherited TeX punctuation."""
import argparse
import json
from pathlib import Path
import re

import build_l7_benchmarking_20261014 as previous
import develop_l7_benchmarking_20261014 as work
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = work.ROOT
BASE = work.BASE/'v2'
OUT = BASE/'reader'
OLD, PRIOR = previous.OLD, work.PRIOR
NAME = 'causal_proposal_benchmarking_v2_2026-10-14'
DRIVER = ROOT/'docs'/(NAME+'.tex')
PDF = DRIVER.with_suffix('.pdf')
CHAPTER = ROOT/'docs/program/comprehensive-v14/work/TEXT.DRAFT.L7/chapter-v2.tex'
BS, NL = chr(92), chr(10)
REPAIRS = {
    'program/gap-repair-v13/work/LA07/evaluation-extension.tex':'evaluation-extension.tex',
    'program/execution/2026-10-13/llm-census/evaluation.tex':'census-evaluation.tex',
}


def corrected(path, text):
    if path.endswith('evaluation-extension.tex'):
        assert text.count('95%') == 1
        return text.replace('95%', '95'+BS+'%')
    assert text.count("'"+BS+",'") == 2
    return text.replace("'"+BS+",'", "''")


def prepare():
    assert not DRIVER.exists() and not CHAPTER.exists()
    verify_bindings(json.loads((previous.OUT/'build-report.json').read_text()))
    BASE.mkdir(exist_ok=False)
    originals=[]
    successors=[]
    for old, name in REPAIRS.items():
        source=ROOT/'docs'/old
        dest=BASE/name
        dest.write_text(corrected(old,source.read_text()))
        originals.append(ref(source,'Immutable inherited input'))
        successors.append(ref(dest,'Only escaped percentage or closing quotation repaired'))
    audit=json.loads((work.BASE/'source-audit.json').read_text())
    verify_bindings(audit)
    write(BASE/'source-audit.json',audit)
    (BASE/'development.tex').write_bytes((previous.BASE/'development.tex').read_bytes())
    (BASE/'refs.bib').write_bytes((previous.BASE/'refs.bib').read_bytes())
    inputs=[BS+'input{'+p+'}' for p in work.INHERITED]
    replacement=[BS+'input{'+str((BASE/REPAIRS[p]).relative_to(ROOT/'docs'))+'}'
                 if p in REPAIRS else BS+'input{'+p+'}' for p in work.INHERITED]
    replacement.append(BS+'input{program/execution/2026-10-14/l7-benchmarking/v2/development.tex}')
    CHAPTER.write_text(NL.join(replacement)+NL)
    book=OLD.read_text()
    assert book.count(NL.join(inputs))==1
    book=book.replace(NL.join(inputs),BS+'input{program/comprehensive-v14/work/TEXT.DRAFT.L7/chapter-v2.tex}')
    pattern=re.compile(re.escape(BS+'bibliography{')+'([^}]+)'+re.escape('}'))
    assert len(pattern.findall(book))==1
    book=pattern.sub(lambda m:BS+'bibliography{'+m.group(1)+
                    ',program/execution/2026-10-14/l7-benchmarking/v2/refs}',book)
    DRIVER.write_text(book)
    write(BASE/'repair-review.json',{
        'reviewer':work.REVIEWER,'status':'source_repair_prepared',
        'prior_candidate':ref(previous.OUT/'build-report.json','Unpublished first L7 candidate'),
        'finding':'Unescaped95% hid the percent sign and joined the next line; two inherited closing quotation pairs contained spurious thin spaces.',
        'originals':originals,'successors':successors,
        'scientific_change':'None; all source records and substantive claims preserved.',
        'tooling_failure':'An initial patch-construction call failed on an unescaped JavaScript delimiter before any tool execution. Reissued as two bounded patches; no artifact was overwritten.',
        'visual_acceptance':False,
    })
    write(BASE/'prepared-inputs.json',{
        'inputs':[ref(p,'Preserved reviewed input') for p in [
            OLD,PRIOR,previous.OUT/'build-report.json',work.BASE/'derivation-review.json',
            previous.BASE/'development.tex',previous.BASE/'refs.bib',Path(__file__).resolve()]]+originals,
        'generated':[ref(p,'Successor source') for p in [
            DRIVER,CHAPTER,BASE/'source-audit.json',BASE/'development.tex',BASE/'refs.bib',
            BASE/'repair-review.json']]+successors,
        'visual_acceptance':False,
    })
    print(json.dumps({'prepared':str(DRIVER.relative_to(ROOT)),'repaired_sources':2}))


def build():
    for key,value in {'BASE':BASE,'OUT':OUT,'OLD':OLD,'PRIOR':PRIOR,'NAME':NAME,
                      'DRIVER':DRIVER,'PDF':PDF,'CHAPTER':CHAPTER}.items():
        setattr(previous,key,value)
    previous.build()
    report=json.loads((OUT/'build-report.json').read_text())
    report.update(builder=ref(Path(__file__).resolve(),'Preserving L7 punctuation successor'),
                  repair_review=ref(BASE/'repair-review.json','Observed inherited defects and exact replacements'))
    previous.engine.core.write(OUT/'build-report.json',report)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('command',choices=['prepare','build'])
    args=parser.parse_args()
    {'prepare':prepare,'build':build}[args.command]()
