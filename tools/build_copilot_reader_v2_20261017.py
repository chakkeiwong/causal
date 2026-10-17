#!/usr/bin/env python3
"""Build an immutable, preserving Copilot-source working reader."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess

import audit_reader_traceability_v2_20261013 as trace
import copilot_reference_20261017 as exact
import build_integrated_monograph_v12 as shared
import review_gap_reader_v13 as layout
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT/'docs'
WORK = DOCS/'program/execution/2026-10-17/census-recovery/copilot-v1'
BASE = WORK/'publication-v2'
OUT = BASE/'reader'
PREDECESSOR = WORK.parent/'benchmark-v1'
OLD = DOCS/'causal_proposal_benchmark_sources_reviewed_2026-10-17.tex'
PRIOR = PREDECESSOR/'reader/source-audit.json'
NAME = 'causal_proposal_copilot_reviewed_v2_2026-10-17'
DRIVER = DOCS/(NAME+'.tex')
PDF = DRIVER.with_suffix('.pdf')
EXTENSION = WORK/'copilot.tex'


def read(path):
    return json.loads(path.read_text())


def expected_driver():
    text = OLD.read_text()
    marker = r'\input{program/execution/2026-10-14/iid-discovery/publication/development.tex}'
    assert text.count(marker) == 1
    text = text.replace(marker, marker+'\n'+r'\input{'+str(EXTENSION.relative_to(DOCS))+'}')
    return re.sub(r'\\bibliography\{([^}]+)\}',
        lambda m: r'\bibliography{'+m.group(1)+','+str((BASE/'refs').relative_to(DOCS))+'}', text)


def prepare():
    assert not DRIVER.exists() and not PDF.exists() and not OUT.exists()
    audit = read(WORK/'source-audit.json')
    verify_bindings(audit)
    assert exact.serial(exact.calculate()) == read(WORK/'exact-results.json')
    bib = []
    for source in audit['sources']:
        author = shared.escape(source['author'])
        if source['integrated_citation_key'] == 'exec17_copilot_paper':
            assert len(author.split(' and ')) == 13
        else:
            author = '{'+author+'}'
        bib.append('@misc{'+source['integrated_citation_key']+',\n author={'+author+
            '},\n title={'+shared.escape(source['title'])+'},\n year={'+str(source['year'])+
            '},\n note={'+shared.escape(source['version_date'])+'}\n}\n')
    (BASE/'refs.bib').write_text('\n'.join(bib))
    DRIVER.write_text(expected_driver())
    write(BASE/'prepared-inputs.json', dict(
        inputs=[ref(p, 'Reviewed preserving input') for p in [OLD, PRIOR,
            WORK/'source-audit.json', WORK/'primary-review.json', WORK/'exact-results.json',
            WORK/'citation-chain-register.json', WORK/'git-byte-validation.json', WORK/'recovery-review.json', WORK.parent/'copilot-plan.md',
            ROOT/'tools/copilot_reference_20261017.py', EXTENSION, BASE/'repair-plan.json',
            WORK/'prepared-inputs.json', WORK/'reader/source-audit.json', WORK/'traceability-review.json', Path(__file__)]],
        generated=[ref(DRIVER, 'Preserving integrated driver'), ref(BASE/'refs.bib', 'Four added references')],
        previous_records=738, added_records=4, expected_scholarly_pdfs=194,
        census_closed=False, depth_acceptance=False, visual_acceptance=False))
    print(json.dumps(dict(prepared=str(DRIVER.relative_to(ROOT)), expected_records=742)))


def build():
    verify_bindings(read(BASE/'prepared-inputs.json'))
    assert DRIVER.read_text() == expected_driver()
    assert exact.serial(exact.calculate()) == read(WORK/'exact-results.json')
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
        assert result.returncode == 0, 'Build failure preserved in '+str(OUT/name)

    execute(command, 'pass-1.log')
    execute(['bibtex', str((OUT/NAME).relative_to(DOCS))], 'bibtex-pass.log')
    for turn in range(2, 6):
        execute(command, f'pass-{turn}.log')
        log = (OUT/(NAME+'.log')).read_text(errors='replace')
        if turn >= 3 and not any(t in log for t in ['Label(s) may have changed', 'Rerun to get']):
            break
    for token in ['undefined citations', 'undefined references', 'multiply defined', 'Missing character']:
        assert token not in log, token
    files = shared.scan(DRIVER)
    joined = '\n'.join(text for _, text in files)
    labels = re.findall(shared.LABEL, joined)
    assert len(labels) == len(set(labels)), 'Duplicate labels'
    cited = {key.strip() for group in re.findall(shared.CITE, joined) for key in group.split(',')}
    entries = {}
    for path in [PRIOR, WORK/'source-audit.json']:
        audit = read(path)
        verify_bindings(audit)
        for source in audit['sources']:
            key = source['integrated_citation_key']
            assert key not in entries or entries[key] == source
            entries[key] = source
    assert cited <= entries.keys(), cited-entries.keys()
    assert len(cited) == 742
    PDF.write_bytes((OUT/(NAME+'.pdf')).read_bytes())
    audit = dict(sources=[entries[k] for k in sorted(cited)],
        tex_files=[ref(p, 'Compiled source') for p in sorted({p for p, _ in files})],
        source_audits=[ref(p, 'Preserved audited input') for p in [PRIOR, WORK/'source-audit.json']],
        cutoff='2026-10-07', visual_acceptance=False)
    write(OUT/'source-audit.json', audit)
    subprocess.run(['pdftotext', '-layout', str(PDF), str(OUT/'reader.txt')], check=True, timeout=30)
    info = subprocess.check_output(['pdfinfo', str(PDF)], text=True, timeout=15)
    pages = int(re.search(r'(?m)^Pages:\s+(\d+)', info).group(1))
    aux = (OUT/(NAME+'.aux')).read_text()
    section_pages = {}
    for suffix in ['development', 'development-end']:
        label = 'exec17:copilot-'+suffix
        match = re.search(r'\\newlabel\{'+re.escape(label)+r'\}\{\{[^}]*\}\{(\d+)\}', aux)
        assert match, label
        section_pages[suffix] = int(match.group(1))
    report = dict(status='compiled_source_and_text_checked_working_draft', pages=pages,
        pdf=ref(PDF, 'Integrated Copilot-source working successor'),
        driver=ref(DRIVER, 'Preserving driver'), builder=ref(Path(__file__), 'Exact Copilot reader builder'),
        predecessor_pdf=ref(OLD.with_suffix('.pdf'), 'Preserved1025-page benchmark working reader'),
        source_audit=ref(OUT/'source-audit.json', '742 audited citation records'),
        cited_records=len(cited), added_section_printed_pages=section_pages,
        warnings=[line for line in log.splitlines() if any(t in line for t in ['Warning', 'Overfull', 'Underfull', 'Missing character'])],
        final_acceptance=False, mandatory_repairs_closed=[], visual_acceptance=False,
        visual_review='Pending fresh session under exhausted inherited image allowance')
    write(OUT/'build-report.json', report)
    layout.OUT = OUT
    layout.main()
    assert read(OUT/'text-layout-review.json')['status'] == 'pass'
    index = trace.audit(DRIVER, OUT/'source-audit.json')
    write(BASE/'traceability-review.json', index)
    assert index['status'] == 'pass' and not index['issues'] and index['scholarly_pdfs'] == 194
    print(json.dumps(dict(pages=pages, records=742, scholarly_pdfs=194,
        section_pages=section_pages, warnings=report['warnings'], visual_acceptance=False)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['prepare', 'build'])
    {'prepare': prepare, 'build': build}[parser.parse_args().command]()
