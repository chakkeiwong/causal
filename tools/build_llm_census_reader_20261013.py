#!/usr/bin/env python3
"""Integrate inspected frontier evidence into four existing LLM chapters."""
import argparse
import json
from pathlib import Path
import re
import subprocess

import build_java_reader_20261013 as inherited
import build_integrated_monograph_v12 as shared
import master_control as core

ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-13/llm-census'
OUT = BASE / 'reader'
NAME = 'causal_proposal_census_2026-10-13'
OLD = ROOT / 'docs/causal_proposal_reuse_2026-10-13.tex'
DRIVER = ROOT / 'docs' / (NAME + '.tex')
PDF = DRIVER.with_suffix('.pdf')
PRIOR_AUDIT = ROOT / 'docs/program/execution/2026-10-13/tetrad-reuse/reader/source-audit.json'
PARTS = {
    'measurement': 'program/execution/2026-10-13/formulation.tex',
    'temporal': 'program/repair-v12/work/LA03/chapter-draft.tex',
    'agents': 'program/repair-v12/work/LA04/chapter-draft.tex',
    'evaluation': 'program/gap-repair-v13/work/LA07/evaluation-extension.tex',
}
ref = shared.ref


def configure():
    for key in ['BASE','OUT','NAME','OLD','DRIVER','PDF','PRIOR_AUDIT']:
        setattr(inherited, key, globals()[key])


def prepare():
    configure()
    inherited.guard()
    audit = json.loads((BASE / 'source-audit.json').read_text())
    shared.verify_refs(audit)
    book = OLD.read_text()
    for part, location in PARTS.items():
        subprocess.run(['pandoc','--from=markdown+raw_tex+tex_math_single_backslash','--to=latex',
                        '--wrap=auto',str(BASE / (part + '.md')),'-o',str(BASE / (part + '.tex'))],
                       check=True,timeout=20)
        marker = r'\input{' + location + '}'
        assert book.count(marker)==1
        book = book.replace(marker,marker + '\n' + r'\input{program/execution/2026-10-13/llm-census/' + part + '.tex}',1)
    marker = 'program/execution/2026-10-13/tetrad-reuse/refs}'
    assert book.count(marker)==1
    book = book.replace(marker,'program/execution/2026-10-13/tetrad-reuse/refs,program/execution/2026-10-13/llm-census/refs}',1)
    DRIVER.write_text(book)
    prior_keys = {s['integrated_citation_key'] for s in json.loads(PRIOR_AUDIT.read_text())['sources']}
    bib = []
    for s in audit['sources']:
        if s['integrated_citation_key'] in prior_keys:
            continue
        bib.append('@misc{' + s['integrated_citation_key'] + ',\n author={{' + shared.escape(s['author']) +
                   '}},\n title={' + shared.escape(s['title']) + '},\n year={' + str(s['year']) +
                   '},\n note={' + shared.escape(s['version_date']) + '}\n}\n')
    (BASE / 'refs.bib').write_text('\n'.join(bib))
    core.write(BASE / 'prepared-inputs.json',{
        'inputs':[ref(p,'Reviewed preserving input') for p in [OLD,PRIOR_AUDIT,BASE/'source-audit.json',
                  BASE/'exact-examples.json',BASE/'substantive-review.md',Path(__file__),
                  *[BASE/(part+'.md') for part in PARTS]]],
        'outputs':[ref(p,'Generated source') for p in [DRIVER,BASE/'refs.bib',*[BASE/(part+'.tex') for part in PARTS]]]})
    print(json.dumps({'prepared':str(DRIVER.relative_to(ROOT)),'new_primary_citations':len(bib),'existing_chapters_extended':len(PARTS)}))


def build():
    configure()
    inherited.build()
    report = json.loads((OUT / 'build-report.json').read_text())
    audit = json.loads((OUT / 'source-audit.json').read_text())
    audit['added_bibliography'] = ref(BASE/'refs.bib','Ten newly inspected originals; two prior source records preserved')
    core.write(OUT / 'source-audit.json',audit)
    aux = (OUT / (NAME + '.aux')).read_text()
    def page(label):
        return int(re.search(r'\\newlabel\{' + re.escape(label) + r'\}\{\{[^}]*\}\{(\d+)\}',aux).group(1))
    report.update(builder=ref(Path(__file__),'Preserving LLM census integration'),
                  compile_routine=ref(ROOT/'tools/build_java_reader_20261013.py','Inherited bounded compiler'),
                  predecessor_pdf=ref(OLD.with_suffix('.pdf'),'Frozen 477-page reader'),
                  pdf=ref(PDF,'Working integrated census successor'),
                  source_audit=ref(OUT/'source-audit.json','Whole-reader source identities'))
    report['llm_census_additions'] = {part:{'first_printed_page':page('exec13:census-'+part),
                                           'last_printed_page':page('exec13:census-'+part+'-end')}
                                     for part in PARTS}
    report['census_closed'] = False
    report['candidate_originals_still_open'] = 101
    core.write(OUT/'build-report.json',report)
    print(json.dumps({'pages':report['pages'],'citations':report['cited_records'],
                      'additions':report['llm_census_additions'],'visual_acceptance':False}))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('command',choices=['prepare','build'])
    args=parser.parse_args()
    prepare() if args.command=='prepare' else build()
