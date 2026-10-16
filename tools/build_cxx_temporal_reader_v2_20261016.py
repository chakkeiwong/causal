#!/usr/bin/env python3
"""Preserving integration of the reviewed native temporal comparison."""
import argparse
from contextlib import redirect_stdout
import json
from pathlib import Path
import re
import audit_reader_traceability_v2_20261013 as trace
import build_java_temporal_engine_20261016 as engine
import review_cxx_temporal_20261016 as work
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT, WORK = work.ROOT, work.BASE
BASE = WORK/'publication-v2'; OUT = BASE/'reader'
OLD = ROOT/'docs/causal_proposal_longitudinal_policy_2026-10-16.tex'
PRIOR = work.PRIOR
NAME = 'causal_proposal_cxx_temporal_v2_2026-10-16'
DRIVER = ROOT/'docs'/(NAME+'.tex'); PDF = DRIVER.with_suffix('.pdf')


def expected_driver():
    book = OLD.read_text()
    marker = r'\input{program/execution/2026-10-15/java-temporal/publication-v3/development.tex}'
    assert book.count(marker) == 1
    book = book.replace(marker, marker+'\n'+r'\input{program/execution/2026-10-16/cxx-temporal/publication-v2/development.tex}')
    pat = re.compile(r'\\bibliography\{([^}]+)\}')
    assert len(pat.findall(book)) == 1
    return pat.sub(lambda m: r'\bibliography{'+m.group(1)+',program/execution/2026-10-16/cxx-temporal/publication-v2/refs}', book)


def prepare():
    assert not DRIVER.exists() and not (BASE/'prepared-inputs.json').exists()
    BASE.mkdir(exist_ok=True)
    audit = json.loads((WORK/'source-audit.json').read_text())
    verify_bindings(audit); verify_bindings(json.loads((WORK/'author-review.json').read_text()))
    write(BASE/'source-audit.json', audit)
    bib = []
    for s in audit['sources']:
        bib.append('@misc{'+s['integrated_citation_key']+',\n author={{'+engine.shared.escape(s['author'])+
            '}},\n title={'+engine.shared.escape(s['title'])+'},\n year={'+str(s['year'])+'},\n note={'+
            engine.shared.escape(s['version_date'])+'}\n}\n')
    (BASE/'refs.bib').write_text('\n'.join(bib))
    DRIVER.write_text(expected_driver())
    write(BASE/'prepared-inputs.json', {
        'inputs': [ref(p, 'Reviewed preserving input') for p in
                   [OLD, PRIOR, WORK/'author-review.json', BASE/'development.tex', BASE/'repair.json', Path(__file__)]],
        'generated': [ref(p, 'Successor source') for p in [DRIVER, BASE/'source-audit.json', BASE/'refs.bib']],
        'credit_policy': 'No automatic census, chapter-depth or product acceptance', 'visual_acceptance': False})
    print(json.dumps({'prepared': str(DRIVER.relative_to(ROOT)), 'new_citations': 7}))


def build():
    for k, v in {'BASE': BASE, 'OUT': OUT, 'OLD': OLD, 'NAME': NAME, 'DRIVER': DRIVER, 'PDF': PDF, 'PRIOR_AUDIT': PRIOR}.items():
        setattr(engine, k, v)
    with (BASE/'compile-summary.log').open('x') as stream:
        with redirect_stdout(stream): engine.build()
    report = json.loads((OUT/'build-report.json').read_text()); aux = (OUT/(NAME+'.aux')).read_text()
    sections = {}
    for label in ['cxx-temporal', 'cxx-temporal-end']:
        m = re.search(re.escape('\\newlabel{exec16:'+label+'}{{')+'[^}]*'+re.escape('}{')+'([0-9]+)', aux)
        assert m, label
        sections[label] = int(m.group(1))
    report.update(builder=ref(Path(__file__), 'Preserving C++ temporal comparison builder'),
                  predecessor_pdf=ref(OLD.with_suffix('.pdf'), 'Frozen827-page reader'), cxx_temporal_sections=sections)
    engine.core.write(OUT/'build-report.json', report)
    audited = trace.audit(DRIVER, OUT/'source-audit.json'); write(BASE/'traceability-review.json', audited)
    assert report['cited_records'] == 656 and report['pages'] > 827
    assert audited['status'] == 'pass' and not audited['issues'] and audited['scholarly_pdfs'] == 175
    print(json.dumps({'pages': report['pages'], 'cited_records': report['cited_records'], 'sections': sections,
                      'scholarly_pdfs': audited['scholarly_pdfs'],
                      'material_warnings': [w for w in report['warnings'] if 'Underfull' not in w]}))


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('command', choices=['prepare', 'build']); args = p.parse_args()
    {'prepare': prepare, 'build': build}[args.command]()
