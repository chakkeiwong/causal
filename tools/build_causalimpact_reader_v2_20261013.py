#!/usr/bin/env python3
"""Preserving CausalImpact integration using the established bounded compiler."""
import argparse
import contextlib
import json
from pathlib import Path

import build_integrated_monograph_v12 as shared
import build_java_reader_20261013 as compiler
import master_control as core
from publish_latent_r_review_v2_20261013 import verify_bindings, write

ROOT = core.ROOT
REVIEW = ROOT/'docs/program/execution/2026-10-13/causalimpact-reuse'
BASE = REVIEW/'final'
OUT = BASE/'reader'
NAME = 'causal_proposal_causalimpact_2026-10-13'
OLD = ROOT/'docs/causal_proposal_commercial_iv_rd_2026-10-13.tex'
DRIVER = ROOT/'docs'/(NAME+'.tex')
PDF = DRIVER.with_suffix('.pdf')
PRIOR_AUDIT = ROOT/'docs/program/execution/2026-10-13/commercial-iv-rd/reader/source-audit.json'
OLD_SOFTWARE = ROOT/'docs/program/execution/2026-10-13/python-discovery/software-preserving.tex'
NEW_SOFTWARE = REVIEW/'software-preserving.tex'
INSERT = r'\input{program/execution/2026-10-13/causalimpact-reuse/decision-v2.tex}'+'\n\n'
ref = shared.ref


def expected_driver():
    text = OLD.read_text()
    marker = str(OLD_SOFTWARE.relative_to(ROOT/'docs'))
    assert text.count(marker) == 1
    text = text.replace(marker, str(NEW_SOFTWARE.relative_to(ROOT/'docs')), 1)
    marker = 'program/execution/2026-10-13/commercial-iv-rd/refs}'
    assert text.count(marker) == 1
    return text.replace(marker, 'program/execution/2026-10-13/commercial-iv-rd/refs,program/execution/2026-10-13/causalimpact-reuse/final/refs}', 1)


def prepare():
    assert not DRIVER.exists()
    assert NEW_SOFTWARE.read_text().replace(INSERT, '', 1) == OLD_SOFTWARE.read_text()
    for name in ['source-audit.json', 'manuscript-review.json', 'decision-proposal.json']:
        verify_bindings(json.loads((REVIEW/name).read_text()))
    BASE.mkdir(exist_ok=False)
    audit = json.loads((REVIEW/'source-audit.json').read_text())
    prior = json.loads(PRIOR_AUDIT.read_text())
    assert not ({s['integrated_citation_key'] for s in audit['sources']} &
                {s['integrated_citation_key'] for s in prior['sources']})
    write(BASE/'source-audit.json', audit)
    (BASE/'refs.bib').write_bytes((REVIEW/'refs.bib').read_bytes())
    DRIVER.write_text(expected_driver())
    write(BASE/'prepared-inputs.json', {'inputs':[ref(p, 'Inspected or preserved manuscript input') for p in
        [OLD, OLD_SOFTWARE, PRIOR_AUDIT, REVIEW/'source-audit.json', REVIEW/'manuscript-review.json', Path(__file__)]],
        'generated':[ref(p, 'Preserving final manuscript input') for p in
            [DRIVER, NEW_SOFTWARE, REVIEW/'decision-v2.tex', BASE/'refs.bib', BASE/'source-audit.json']]})
    print(json.dumps({'prepared':str(DRIVER.relative_to(ROOT)), 'sources':len(audit['sources'])}))


def build():
    assert not PDF.exists(), 'Preserve completed reader'
    OUT.mkdir(exist_ok=False)
    for name in ['BASE','OUT','NAME','OLD','DRIVER','PDF','PRIOR_AUDIT']:
        setattr(compiler, name, globals()[name])
    for suffix in ['.aux','.bbl','.toc','.out']:
        (OUT/(NAME+suffix)).touch(exist_ok=False)
    with (OUT/'compile-summary.txt').open('x') as stream, contextlib.redirect_stdout(stream):
        compiler.build()
    report = json.loads((OUT/'build-report.json').read_text())
    report.pop('java_comparison', None)
    audit = json.loads((OUT/'source-audit.json').read_text())
    prior = json.loads(PRIOR_AUDIT.read_text())
    audit['added_bibliography'] = ref(BASE/'refs.bib', 'CausalImpact primary sources and authored examples')
    audit['additive_anchor_corrections'] = prior.get('additive_anchor_corrections', [])
    core.write(OUT/'source-audit.json', audit)
    aux = (OUT/(NAME+'.aux')).read_text()
    def page(label):
        prefix = chr(92)+'newlabel{'+label+'}{{'
        line = next(x for x in aux.splitlines() if x.startswith(prefix))
        return int(line[len(prefix):].split('}{', 2)[1])
    report.update(builder=ref(Path(__file__), 'Established bounded compiler, preserving manuscript successor'),
        source_audit=ref(OUT/'source-audit.json','Whole-reader source audit'),
        pdf=ref(PDF,'CausalImpact software-survey working reader'),
        predecessor_pdf=ref(OLD.with_suffix('.pdf'),'Preserved642-page commercial-IV/RD reader'),
        causalimpact={'first_printed_page':page('exec13:causalimpact-reuse'),
            'last_printed_page':page('exec13:causalimpact-reuse-end'),
            'choice':'reference','native_execution':False,'integration_allowed':False})
    core.write(OUT/'build-report.json', report)
    print(json.dumps({k:report[k] for k in ['pages','cited_records','causalimpact','warnings']}))


if __name__ == '__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','build']);args=p.parse_args()
    prepare() if args.command=='prepare' else build()
