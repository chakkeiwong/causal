#!/usr/bin/env python3
"""Integrate the Python comparison while preserving every released artifact."""
import argparse
import json
from pathlib import Path
import re

import build_java_reader_20261013 as inherited
import build_integrated_monograph_v12 as shared
import master_control as core

ROOT = core.ROOT
BASE = ROOT/'docs/program/execution/2026-10-13/python-discovery'
OUT = BASE/'reader'
NAME = 'causal_proposal_python_discovery_2026-10-13'
OLD = ROOT/'docs/causal_proposal_interfaces_2026-10-13.tex'
DRIVER = ROOT/'docs'/(NAME+'.tex')
PDF = DRIVER.with_suffix('.pdf')
PRIOR_AUDIT = ROOT/'docs/program/execution/2026-10-13/interfaces/reader/source-audit.json'
SOFTWARE = ROOT/'docs/program/execution/2026-10-13/java-discovery/software-preserving.tex'
ref = shared.ref


def configure():
    for key in ['BASE', 'OUT', 'NAME', 'OLD', 'DRIVER', 'PDF', 'PRIOR_AUDIT']:
        setattr(inherited, key, globals()[key])


def prepare():
    configure()
    inherited.guard()
    audit = json.loads((BASE/'source-audit.json').read_text())
    shared.verify_refs(audit)
    body = SOFTWARE.read_text()
    marker = r'\section{Symbolic identification and numerical evaluation}'
    assert body.count(marker) == 1
    body = body.replace(marker, r'\input{program/execution/2026-10-13/python-discovery/comparison.tex}'+'\n\n'+marker, 1)
    (BASE/'software-preserving.tex').write_text(body)
    book = OLD.read_text()
    marker = r'\input{program/execution/2026-10-13/java-discovery/software-preserving.tex}'
    assert book.count(marker) == 1
    book = book.replace(marker, r'\input{program/execution/2026-10-13/python-discovery/software-preserving.tex}', 1)
    marker = 'program/execution/2026-10-13/interfaces/refs}'
    assert book.count(marker) == 1
    book = book.replace(marker, 'program/execution/2026-10-13/interfaces/refs,program/execution/2026-10-13/python-discovery/refs}', 1)
    marker = '\\addcontentsline{toc}{chapter}{Reader\'s contract}'
    assert book.count(marker) == 1
    book = book.replace(marker, marker+'\n\n'+r'Section \ref{exec13:python-discovery} compares nine Python discovery families,'+'\n'+
                        'with exact funding-direction, observational-equivalence, numerical and selection examples.\n'+
                        'These are primary-source comparisons and project calculations; downloaded engines\n'+
                        'were not executed, and broader search and delegated-wrapper gaps remain explicit.\n', 1)
    DRIVER.write_text(book)
    entries = []
    for source in audit['sources']:
        author = source['author'].replace(r'\u00e4', 'ä')
        entries.append('@misc{'+source['integrated_citation_key']+',\n author={{'+shared.escape(author)+
                       '}},\n title={'+shared.escape(source['title'])+'},\n year={'+str(source['year'])+
                       '},\n note={'+shared.escape(source['version_date'])+'}\n}\n')
    (BASE/'refs.bib').write_text('\n'.join(entries))
    core.write(BASE/'prepared-inputs.json', {'inputs': [ref(p, 'Preserving reader input') for p in
               [OLD, PRIOR_AUDIT, SOFTWARE, BASE/'comparison.tex', BASE/'source-audit.json',
                BASE/'oracle-results.json', BASE/'reproduction-review.json', Path(__file__)]],
               'outputs': [ref(p, 'Prepared manuscript source') for p in [DRIVER, BASE/'software-preserving.tex', BASE/'refs.bib']]})
    print(json.dumps({'prepared': str(DRIVER.relative_to(ROOT))}))


def build():
    configure()
    OUT.mkdir(exist_ok=True)
    # Avoid accidentally loading auxiliaries from a preserved historical attempt.
    for suffix in ['.aux', '.bbl', '.toc', '.out']:
        p = OUT/(NAME+suffix)
        if not p.exists():
            p.write_text('')
    inherited.build()
    report = json.loads((OUT/'build-report.json').read_text())
    audit = json.loads((OUT/'source-audit.json').read_text())
    audit['added_bibliography'] = ref(BASE/'refs.bib', 'Python discovery source and project bibliography')
    core.write(OUT/'source-audit.json', audit)
    aux = (OUT/(NAME+'.aux')).read_text()

    def page(label):
        return int(re.search(r'\\newlabel\{'+re.escape(label)+r'\}\{\{[^}]*\}\{(\d+)\}', aux).group(1))

    first, last = page('exec13:python-discovery'), page('exec13:python-discovery-end')
    report.update(builder=ref(Path(__file__), 'Preserving Python discovery builder'),
                  compile_routine=ref(ROOT/'tools/build_java_reader_20261013.py', 'Inherited bounded compiler'),
                  predecessor_pdf=ref(OLD.with_suffix('.pdf'), 'Frozen496-page predecessor'),
                  pdf=ref(PDF, 'Integrated Python discovery working reader'),
                  source_audit=ref(OUT/'source-audit.json', 'Whole-book source identities'),
                  python_discovery={'first_printed_page': first, 'last_printed_page': last,
                                    'physical_span': last-first+1, 'candidate_families': 9,
                                    'coverage_acceptance': False, 'engine_execution': False})
    core.write(OUT/'build-report.json', report)
    print(json.dumps({'pages': report['pages'], 'citations': report['cited_records'],
                      'python_discovery': report['python_discovery'], 'visual_acceptance': False}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['prepare', 'build'])
    args = parser.parse_args()
    prepare() if args.command == 'prepare' else build()
