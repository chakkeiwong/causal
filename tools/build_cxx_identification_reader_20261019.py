#!/usr/bin/env python3
"""Build a preserving working reader from a bounded native identification and counterfactual source review."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess

import audit_reader_traceability_v2_20261013 as trace
import build_integrated_monograph_v12 as shared
import cxx_identification_reference_20261019 as exact
import review_gap_reader_v13 as layout
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT/'docs'
BASE = DOCS/'program/execution/2026-10-19/cxx-identification-v1'
OUT = BASE/'reader'
PREDECESSOR = DOCS/'program/execution/2026-10-19/commercial-synthetic-controls-v1'
OLD = DOCS/'causal_proposal_commercial_synthetic_reviewed_2026-10-19.tex'
PRIOR = PREDECESSOR/'reader/source-audit.json'
NAME = 'causal_proposal_cxx_identification_reviewed_2026-10-19'
DRIVER = DOCS/(NAME+'.tex')
PDF = DRIVER.with_suffix('.pdf')
DEVELOPMENT = BASE/'development.tex'
LABELS = ['exec19:cxxid-'+suffix for suffix in ['scope','recursion','abduction','coupling','joint','contract']]


def read(path):
    return json.loads(path.read_text())


def expected_driver():
    text = OLD.read_text()
    marker = r'\input{program/execution/2026-10-19/commercial-synthetic-controls-v1/development.tex}'
    assert text.count(marker) == 1
    text = text.replace(marker, marker+'\n'+r'\input{program/execution/2026-10-19/cxx-identification-v1/development.tex}')
    return re.sub(r'\\bibliography\{([^}]+)\}',
        lambda m: r'\bibliography{'+m.group(1)+','+str((BASE/'refs').relative_to(DOCS))+'}', text)


def prepare():
    assert not DRIVER.exists() and not PDF.exists() and not OUT.exists()
    for path in [PRIOR, BASE/'source-audit.json', BASE/'review.json', BASE/'omissions-register.json']:
        verify_bindings(read(path))
    assert exact.calculate() == read(BASE/'exact-results.json')
    write(BASE/'manuscript-plan-review.json',dict(status='pass',scope='Preserve prior reader and integrate bounded native identification and joint-abduction critique',evidence=[ref(BASE/'plan-review.json','Reviewed program'),ref(DEVELOPMENT,'Connected banking argument'),ref(BASE/'review.json','Pinned source findings')],checks=['Preserve all795 predecessor citation identities and contexts.','Separate static code, proof obligations and native execution.','Keep complete candidate coverage and counterfactual coupling unresolved.']))
    write(BASE/'mathematical-review.json',dict(status='pass',issues=[],evidence=[ref(ROOT/'tools/cxx_identification_reference_20261019.py','Exact finite enumeration'),ref(BASE/'exact-results.json','Reproduced rational outcomes'),ref(DEVELOPMENT,'Explained structural models')],findings=['Stable/switch worlds share observed and intervention marginals but profile counterfactuals are1and0.','Joint posterior roots are equal with probability1; product marginals yield1/2.','Assumed100USD payoff less20USD cost gives80,-20and30USD.','No native behavior or actual bank performance inferred.'],empirical_performance=False))
    write(BASE/'copyedit-review.json',dict(status='pass',evidence=[ref(DEVELOPMENT,'Connected native-source critique')],findings=['Multi-conditioning and accumulated-kernel observations remain qualification obligations, not asserted bugs.','Source tests are inspected, not run; incomplete search remains unknown.','Counterfactual conditional values are distinguished from incremental ROI.'],rendered_review=False))
    bib=[]
    for source in read(BASE/'source-audit.json')['sources']:
        author=source['author']
        if source['kind']!='paper': author='{'+shared.escape(author)+'}'
        note=source['source_identity']+'; '+source['version_date']
        bib.append('@misc{'+source['integrated_citation_key']+',\n author={'+author+'},\n title={'+shared.escape(source['title'])+'},\n year={'+str(source['year'])+'},\n note={'+shared.escape(note)+'}\n}\n')
    (BASE/'refs.bib').write_text('\n'.join(bib))
    DRIVER.write_text(expected_driver())
    paths=[OLD,PRIOR,DEVELOPMENT,BASE/'source-audit.json',BASE/'review.json',BASE/'omissions-register.json',BASE/'mathematical-review.json',BASE/'copyedit-review.json',BASE/'manuscript-plan-review.json',BASE/'exact-results.json',ROOT/'tools/cxx_identification_reference_20261019.py',Path(__file__)]
    write(BASE/'prepared-inputs.json',dict(inputs=[ref(p,'Reviewed preserving input') for p in paths],generated=[ref(DRIVER,'Preserving native identification driver'),ref(BASE/'refs.bib','Two-record bibliography')],expected_cited_records=797,expected_scholarly_pdfs=205,visual_acceptance=False))
    print(json.dumps(dict(prepared=str(DRIVER.relative_to(ROOT)),expected_records=797)))


def build():
    verify_bindings(read(BASE/'prepared-inputs.json'))
    assert DRIVER.read_text() == expected_driver()
    assert exact.calculate() == read(BASE/'exact-results.json')
    assert not OUT.exists() and not PDF.exists()
    OUT.mkdir()
    env = dict(os.environ)
    env['TEXINPUTS'] = str(DOCS)+'//:'+env.get('TEXINPUTS', '')
    env['BIBINPUTS'] = str(DOCS)+'//:'+env.get('BIBINPUTS', '')
    command = ['pdflatex', '-no-shell-escape', '-interaction=nonstopmode', '-halt-on-error',
               '-output-directory='+str(OUT), str(DRIVER)]

    def execute(args, name):
        with (OUT/name).open('x') as stream:
            result = subprocess.run(args, cwd=DOCS, env=env, stdout=stream,
                                    stderr=subprocess.STDOUT, timeout=120)
        assert result.returncode == 0, 'Failure preserved in '+str(OUT/name)

    execute(command, 'pass-1.log')
    execute(['bibtex', str((OUT/NAME).relative_to(DOCS))], 'bibtex-pass.log')
    for turn in range(2, 6):
        execute(command, f'pass-{turn}.log')
        log = (OUT/(NAME+'.log')).read_text(errors='replace')
        if turn >= 3 and not any(t in log for t in ['Label(s) may have changed', 'Rerun to get']):
            break
    for token in ['undefined citations', 'undefined references', 'multiply defined', 'Missing character', 'Overfull']:
        assert token not in log, token
    files = shared.scan(DRIVER)
    joined = '\n'.join(text for _, text in files)
    labels = re.findall(shared.LABEL, joined)
    assert len(labels) == len(set(labels))
    cited = {key.strip() for group in re.findall(shared.CITE, joined) for key in group.split(',')}
    entries = {}
    for path in [PRIOR, BASE/'source-audit.json']:
        audit = read(path)
        verify_bindings(audit)
        for source in audit['sources']:
            key = source['integrated_citation_key']
            assert key not in entries or entries[key] == source
            entries[key] = source
    assert cited <= entries.keys(), cited-entries.keys()
    assert len(cited) == 797
    PDF.write_bytes((OUT/(NAME+'.pdf')).read_bytes())
    write(OUT/'source-audit.json', dict(sources=[entries[k] for k in sorted(cited)],
        tex_files=[ref(p, 'Compiled source') for p in sorted({p for p, _ in files})],
        source_audits=[ref(p, 'Preserved audited input') for p in [PRIOR, BASE/'source-audit.json']],
        cutoff='2026-10-07', visual_acceptance=False))
    subprocess.run(['pdftotext', '-layout', str(PDF), str(OUT/'reader.txt')], check=True, timeout=30)
    info = subprocess.check_output(['pdfinfo', str(PDF)], text=True, timeout=15)
    pages = int(re.search(r'(?m)^Pages:\s+(\d+)', info).group(1))
    aux = (OUT/(NAME+'.aux')).read_text()
    anchors = {}
    for label in LABELS:
        match = re.search(r'\\newlabel\{'+re.escape(label)+r'\}\{\{([^}]+)\}\{(\d+)\}', aux)
        assert match, label
        anchors[label] = dict(number=match.group(1), printed_page=int(match.group(2)))
    report = dict(status='compiled_source_and_text_checked_working_draft', pages=pages,
        pdf=ref(PDF, 'Preserving native identification and counterfactual working successor'),
        driver=ref(DRIVER, 'Preserving driver'), builder=ref(Path(__file__), 'Exact preserving builder'),
        predecessor_pdf=ref(OLD.with_suffix('.pdf'), 'Preserved1094-page commercial synthetic-control reader'),
        source_audit=ref(OUT/'source-audit.json', '797 audited citation records'),
        cited_records=len(cited), added_anchors=anchors,
        warnings=[line for line in log.splitlines() if any(t in line for t in ['Warning', 'Overfull', 'Underfull', 'Missing character'])],
        final_acceptance=False, mandatory_repairs_closed=[], visual_acceptance=False,
        visual_review='Pending fresh session; inherited image allowance exhausted')
    write(OUT/'build-report.json', report)
    layout.OUT = OUT
    layout.main()
    assert read(OUT/'text-layout-review.json')['status'] == 'pass'
    index = trace.audit(DRIVER, OUT/'source-audit.json')
    write(BASE/'traceability-review.json', index)
    assert index['status'] == 'pass' and not index['issues'] and index['scholarly_pdfs'] == 205
    print(json.dumps(dict(pages=pages, records=797, scholarly_pdfs=205,
        anchors=anchors, warnings=report['warnings'], visual_acceptance=False)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['prepare', 'build'])
    {'prepare': prepare, 'build': build}[parser.parse_args().command]()
