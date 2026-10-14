#!/usr/bin/env python3
"""Preserving reader integration for commercial IV/RD and learner design findings."""
import argparse
import contextlib
import json
from pathlib import Path

import build_integrated_monograph_v12 as shared
import build_java_reader_20261013 as compiler
import master_control as core
from publish_latent_r_review_v2_20261013 import verify_bindings, write

ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-13/commercial-iv-rd'
OUT = BASE / 'reader'
NAME = 'causal_proposal_commercial_iv_rd_2026-10-13'
OLD = ROOT / 'docs/causal_proposal_observations_2026-10-13.tex'
DRIVER = ROOT / 'docs' / (NAME + '.tex')
PDF = DRIVER.with_suffix('.pdf')
PRIOR_AUDIT = ROOT / 'docs/program/execution/2026-10-13/observations-journey/reader/source-audit.json'
ref = shared.ref


def expected_driver():
    text = OLD.read_text()
    for marker, extra in [
        (r'\input{program/execution/2026-10-13/commercial-heterogeneity/comparison.tex}',
         r'\input{program/execution/2026-10-13/commercial-iv-rd/comparison.tex}'),
        (r'\input{program/execution/2026-10-13/dependent-learner/chapter.tex}',
         r'\input{program/execution/2026-10-13/commercial-iv-rd/dependent-feasibility.tex}')]:
        assert text.count(marker) == 1
        text = text.replace(marker, marker+'\n'+extra, 1)
    marker = 'program/execution/2026-10-13/observations-journey/refs}'
    assert text.count(marker) == 1
    return text.replace(marker, 'program/execution/2026-10-13/observations-journey/refs,program/execution/2026-10-13/commercial-iv-rd/refs}', 1)


def prepare():
    assert not DRIVER.exists()
    for name in ['source-audit.json', 'manuscript-review.json']:
        verify_bindings(json.loads((BASE/name).read_text()))
    DRIVER.write_text(expected_driver())
    write(BASE/'prepared-inputs.json', {'inputs':[ref(p,'Preserved or inspected manuscript input') for p in
        [OLD,PRIOR_AUDIT,BASE/'source-audit.json',BASE/'manuscript-review.json',Path(__file__)]],
        'generated':[ref(p,'New preserving manuscript or bibliography') for p in
        [DRIVER,BASE/'comparison.tex',BASE/'dependent-feasibility.tex',BASE/'refs.bib']]})
    print(json.dumps({'driver':str(DRIVER.relative_to(ROOT)),'added_sources':12}))


def build():
    assert not PDF.exists(), 'Preserve completed reader'
    for name in ['BASE','OUT','NAME','OLD','DRIVER','PDF','PRIOR_AUDIT']:
        setattr(compiler,name,globals()[name])
    OUT.mkdir(exist_ok=False)
    for suffix in ['.aux','.bbl','.toc','.out']:
        (OUT/(NAME+suffix)).touch(exist_ok=False)
    with (OUT/'compile-summary.txt').open('x') as stream, contextlib.redirect_stdout(stream):
        compiler.build()
    report=json.loads((OUT/'build-report.json').read_text());report.pop('java_comparison',None)
    audit=json.loads((OUT/'source-audit.json').read_text())
    prior=json.loads(PRIOR_AUDIT.read_text())
    audit['added_bibliography']=ref(BASE/'refs.bib','Inspected commercial IV/RD and learner design sources')
    audit['additive_anchor_corrections']=prior.get('additive_anchor_corrections',[])
    core.write(OUT/'source-audit.json',audit)
    aux=(OUT/(NAME+'.aux')).read_text()
    def page(label):
        prefix=chr(92)+'newlabel{'+label+'}{{'
        line=next(line for line in aux.splitlines() if line.startswith(prefix))
        return int(line[len(prefix):].split('}{',2)[1])
    report.update(builder=ref(Path(__file__),'Bounded preserving IV/RD reader compiler'),
        source_audit=ref(OUT/'source-audit.json','Whole-reader source audit and preserved corrections'),
        pdf=ref(PDF,'Commercial IV/RD and dependent-design working monograph'),
        predecessor_pdf=ref(OLD.with_suffix('.pdf'),'Preserved635-page observation reader'),
        commercial_iv_rd={'first_printed_page':page('exec13:commercial-iv-rd'),
            'last_printed_page':page('exec13:commercial-iv-rd-end'),'commercial_families_inspected':6,
            'essential_candidates_unresolved':3,'native_execution':False},
        dependent_design={'first_printed_page':page('exec13:dependent-design-review'),
            'last_printed_page':page('exec13:dependent-design-review-end'),'final_study_approved':False})
    core.write(OUT/'build-report.json',report)
    print(json.dumps({k:report[k] for k in ['pages','cited_records','commercial_iv_rd','dependent_design']}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','build']);args=p.parse_args()
    prepare() if args.command=='prepare' else build()
