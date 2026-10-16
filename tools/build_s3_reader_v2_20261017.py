#!/usr/bin/env python3
"""Preserve the recovered S3 candidate and add full-table IV sensitivity."""
import argparse
from contextlib import redirect_stdout
import json
from pathlib import Path
import re

import audit_reader_traceability_v2_20261013 as trace
import build_java_temporal_engine_20261016 as engine
import build_s3_reader_20261017 as candidate
import prepare_s3_20261017 as work
import s3_sensitivity_20261017 as sensitivity
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT, WORK = work.ROOT, work.BASE
BASE = WORK/'publication-v2'
OUT = BASE/'reader'
OLD = candidate.DRIVER
PRIOR = candidate.OUT/'source-audit.json'
NAME = 'causal_proposal_identification_sensitivity_2026-10-17'
DRIVER = ROOT/'docs'/(NAME+'.tex')
PDF = DRIVER.with_suffix('.pdf')
EXTENSION = sensitivity.BASE/'sensitivity.tex'


def expected_driver():
    book = OLD.read_text()
    marker = r'\input{program/comprehensive-v14/work/TEXT.DRAFT.S3/chapter.tex}'
    assert book.count(marker) == 1
    book = book.replace(marker, marker+'\n'+r'\input{program/execution/2026-10-17/s3/sensitivity/sensitivity.tex}')
    pattern = re.compile(r'\\bibliography\{([^}]+)\}')
    assert len(pattern.findall(book)) == 1
    return pattern.sub(lambda m: r'\bibliography{'+m.group(1)+',program/execution/2026-10-17/s3/publication-v2/refs}', book)


def prepare():
    assert not DRIVER.exists() and not BASE.exists()
    exact = json.loads((sensitivity.BASE/'exact-results.json').read_text())
    assert sensitivity.calculate() == exact
    assert sensitivity.separate_review(exact)['status'] == 'pass'
    for p in [PRIOR, WORK/'depth-review-initial.json', sensitivity.BASE/'mathematics-review.json']:
        verify_bindings(json.loads(p.read_text()))
    BASE.mkdir()
    source = engine.source('exec17_s3_sensitivity',
        'Exact full-table binary-IV bounds and assumption sensitivity',
        'Causal banking proposal', 'project_derivation',
        'Project-authored response-type probability laws and algebra; not empirical evidence',
        '2026-10-17', sensitivity.BASE/'exact-results.json',
        'All eight conditional cells;36 feasible domain vertices; four endpoint laws; two exclusion envelopes',
        ['Under the stated exclusion/randomization class and defier budget<=1/10, the sharp complier effect range is[1/25,9/25].',
         'PopulationATE sharp range remains[-4/25,11/25]; full-cell restrictions sharpen contrast-only outer bounds.',
         'Monotone-receipt exclusion relaxation yields outer envelopes, not asserted sharp full-table ranges.',
         'Stipulated USD100/USD12/USD2 values give randomized encouragement incremental net6/5USD.'],
        [ref(ROOT/'tools/s3_sensitivity_20261017.py', 'Exact type enumeration and separate marginal equations'),
         ref(sensitivity.BASE/'mathematics-review.json', 'Separate author arithmetic and cell review'),
         ref(EXTENSION, 'Analytic feasibility, sharpness, derivative and exclusion derivations'),
         ref(WORK/'sensitivity-plan.md', 'Reviewed depth repair'),
         ref(WORK/'depth-review-initial.json', 'Preserved failed initial6.5-page assessment')])
    write(BASE/'source-audit.json', {'cutoff':'2026-10-07', 'sources':[source],
                                    'prior':ref(PRIOR,'702 preserved candidate source records')})
    bib = '@misc{'+source['integrated_citation_key']+',\n author={{'+engine.shared.escape(source['author'])+'}},\n title={'+engine.shared.escape(source['title'])+'},\n year={2026},\n note={'+engine.shared.escape(source['version_date'])+'}\n}\n'
    (BASE/'refs.bib').write_text(bib)
    DRIVER.write_text(expected_driver())
    write(BASE/'prepared-inputs.json', {
        'inputs':[ref(p,'Preserved input or reviewed extension') for p in
                  [OLD, PRIOR, work.PRIOR, WORK/'depth-review-initial.json',
                   sensitivity.BASE/'exact-results.json', sensitivity.BASE/'mathematics-review.json',
                   EXTENSION, ROOT/'tools/s3_sensitivity_20261017.py', Path(__file__)]],
        'generated':[ref(p,'Successor source') for p in [DRIVER, BASE/'source-audit.json', BASE/'refs.bib']],
        'credit_policy':'Review nonduplicate substantive depth after compilation; no census or product acceptance.',
        'visual_acceptance':False})
    print(json.dumps({'prepared':str(DRIVER.relative_to(ROOT)), 'expected_records':703}))


def build():
    assert not OUT.exists() and not PDF.exists(), 'Preserve any earlier build; use a successor'
    for k,v in {'BASE':BASE,'OUT':OUT,'OLD':OLD,'NAME':NAME,
                'DRIVER':DRIVER,'PDF':PDF,'PRIOR_AUDIT':PRIOR}.items():
        setattr(engine,k,v)
    with (BASE/'compile-summary.log').open('x') as stream:
        with redirect_stdout(stream):
            engine.build()
    report = json.loads((OUT/'build-report.json').read_text())
    aux = (OUT/(NAME+'.aux')).read_text()
    sections = {}
    for label in ['s3','s3-target','s3-adjust','s3-idc','s3-coupling','s3-iv',
                  's3-bounds','s3-numerical','s3-software','s3-design','s3-end',
                  's3-sensitivity','s3-monotone-polytope','s3-defiers','s3-exclusion',
                  's3-sensitivity-decision','s3-sensitivity-end']:
        match = re.search(re.escape('\\newlabel{exec17:'+label+'}{{')+'[^}]*'+re.escape('}{')+'([0-9]+)',aux)
        assert match,label
        sections[label] = int(match.group(1))
    report.update(builder=ref(Path(__file__),'Preserving S3 sensitivity builder'),
                  predecessor_pdf=ref(OLD.with_suffix('.pdf'),'Unpublished894-page candidate retained'),
                  canonical_predecessor_pdf=ref(candidate.OLD.with_suffix('.pdf'),'Published883-page predecessor retained'),
                  identification_sections=sections)
    engine.core.write(OUT/'build-report.json',report)
    audited = trace.audit(DRIVER,OUT/'source-audit.json')
    write(BASE/'traceability-review.json',audited)
    assert report['cited_records']==703 and report['pages']>894
    assert audited['status']=='pass' and not audited['issues'] and audited['scholarly_pdfs']==187
    print(json.dumps({'pages':report['pages'],'cited_records':report['cited_records'],
                      'sections':sections,'scholarly_pdfs':audited['scholarly_pdfs'],
                      'material_warnings':[w for w in report['warnings'] if 'Underfull' not in w]}))


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('command',choices=['prepare','build'])
    args=parser.parse_args()
    {'prepare':prepare,'build':build}[args.command]()
