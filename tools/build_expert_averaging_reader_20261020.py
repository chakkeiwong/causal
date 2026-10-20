#!/usr/bin/env python3
"""Build a preserving expert-guided discovery proposal successor with dynamically derived audit counts."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess

import audit_reader_traceability_v2_20261013 as trace
import build_integrated_monograph_v12 as shared
import expert_averaging_reference_20261020 as exact
import review_gap_reader_v13 as layout
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT/'docs'
BASE = DOCS/'program/execution/2026-10-20/census-expert-averaging-v1'
OUT = BASE/'reader'
PREDECESSOR = DOCS/'program/execution/2026-10-20/census-validity-v1'
OLD = DOCS/'causal_proposal_validity_measurement_reviewed_2026-10-20.tex'
PRIOR = PREDECESSOR/'reader/source-audit.json'
NAME = 'causal_proposal_expert_averaging_reviewed_2026-10-20'
DRIVER = DOCS/(NAME+'.tex')
PDF = DRIVER.with_suffix('.pdf')
DEVELOPMENT = BASE/'development.tex'
LABELS = ['exec20:expert-'+x for x in ['scope','semantics','votes','majority','cycle','evidence','budget','identification','worlds','effects']]
read = lambda p: json.loads(p.read_text())


def sources():
    entries = {}
    for path in [PRIOR, BASE/'source-audit.json']:
        audit = read(path)
        verify_bindings(audit)
        for source in audit['sources']:
            key = source['integrated_citation_key']
            assert key not in entries or entries[key] == source
            entries[key] = source
    return entries


def expected_driver():
    text = OLD.read_text()
    marker = r'\input{program/execution/2026-10-14/iid-discovery/publication/development.tex}'
    assert text.count(marker) == 1
    text = text.replace(marker, marker+'\n'+r'\input{program/execution/2026-10-20/census-expert-averaging-v1/development.tex}')
    return re.sub(r'\\bibliography\{([^}]+)\}',
        lambda m: r'\bibliography{'+m.group(1)+','+str((BASE/'refs').relative_to(DOCS))+'}', text)


def prepare():
    assert not DRIVER.exists() and not PDF.exists() and not OUT.exists()
    for name in ['source-audit.json', 'primary-review.json', 'review.json', 'reconciliation-review.json']:
        verify_bindings(read(BASE/name))
    assert exact.calculate() == read(BASE/'exact-results.json')
    entries = sources()
    prior_count = len(read(PRIOR)['sources'])
    papers = read(PREDECESSOR/'traceability-review.json')['scholarly_pdfs']+1
    write(BASE/'manuscript-plan-review.json', dict(status='pass',
        scope='Preserve predecessor and integrate expert-guided discovery with graph and intervention limits',
        evidence=[ref(DEVELOPMENT, 'Connected discovery argument'), ref(BASE/'review.json', 'Primary review')],
        checks=['Preserve all previous citations, contexts and compiled inputs.',
                'Integrate into the discovery chapter; no duplicate depth credit.',
                'Distinguish primary reported experiments, printed specification traces and project counterexamples.',
                'Separate conditional candidate use, executable reuse, graph validity and identified intervention effects.']))
    write(BASE/'mathematical-review.json', dict(status='pass_for_scoped_project_argument', issues=[],
        evidence=[ref(ROOT/'tools/expert_averaging_reference_20261020.py', 'Exact reference'),
                  ref(BASE/'exact-results.json', 'Exact outputs'), ref(DEVELOPMENT, 'Explicit laws and graph constructions')],
        findings=['Eleven independent3/4-correct votes have majority correctness1012581/1048576; identical votes retain3/4.',
                  'Three acyclic two-edge graphs give2/3 support to each edge of a directed3-cycle.',
                  'Printed existence-query branch permits3 rejections with budget1 and counter0; exhausted orientation has no terminal fallback.',
                  'Independent structural Gaussian errors give common covariance[[1,3/5],[3/5,1]] but intervention slopes3/5 and0.',
                  'Stipulated value100 and cost40 give compatible margins20,-40; an unjustified9/10 vote weight yields14.',
                  'No native code defect, calibrated posterior, universal recovery or bank profit is established.'],
        native_execution=False, empirical_coverage=False, all_source_theorems_independently_verified=False))
    write(BASE/'copyedit-review.json', dict(status='pass', evidence=[ref(DEVELOPMENT, 'Connected argument')],
        findings=['Keep ancestry, adjacency, orientation and clock restrictions distinct.',
                  'Include real-model appendix, cached answers, exclusions and adverse domain results.',
                  'Describe printed discrepancies as unresolved implementation questions.',
                  'Do not transfer a two-variable unclocked example to a known bank time order.',
                  'Keep process records out of the product narrative.'], rendered_review=False))
    bibliography=[]
    for source in read(BASE/'source-audit.json')['sources']:
        author = source['author'] if source['kind']=='paper' else '{'+shared.escape(source['author'])+'}'
        bibliography.append('@misc{'+source['integrated_citation_key']+',\n author={'+author+
            '},\n title={'+shared.escape(source['title'])+'},\n year={'+str(source['year'])+
            '},\n note={'+shared.escape(source['source_identity']+'; '+source['version_date'])+'}\n}\n')
    (BASE/'refs.bib').write_text('\n'.join(bibliography))
    DRIVER.write_text(expected_driver())
    paths=[OLD, PRIOR, DEVELOPMENT, Path(__file__), ROOT/'tools/expert_averaging_reference_20261020.py']
    paths += [BASE/n for n in ['source-audit.json','primary-review.json','review.json','omissions-register.json',
        'mathematical-review.json','copyedit-review.json','manuscript-plan-review.json','exact-results.json']]
    write(BASE/'prepared-inputs.json',dict(inputs=[ref(p,'Reviewed preserving input') for p in paths],
        generated=[ref(DRIVER,'Preserving driver'),ref(BASE/'refs.bib','Added audited citations')],
        prior_cited_records=prior_count,expected_cited_records=len(entries),expected_scholarly_pdfs=papers,
        visual_acceptance=False))
    print(json.dumps(dict(prepared=str(DRIVER.relative_to(ROOT)),expected_records=len(entries),scholarly_pdfs=papers)))

def build():
    prepared = read(BASE/'prepared-inputs.json')
    verify_bindings(prepared)
    assert DRIVER.read_text() == expected_driver()
    assert exact.calculate() == read(BASE/'exact-results.json')
    assert not OUT.exists() and not PDF.exists()
    OUT.mkdir()
    env = dict(os.environ)
    for name in ['TEXINPUTS', 'BIBINPUTS']:
        env[name] = str(DOCS)+':'+env.get(name, '')
    command = ['pdflatex', '-no-shell-escape', '-interaction=nonstopmode', '-halt-on-error',
        '-output-directory='+str(OUT), str(DRIVER)]

    def execute(args, name):
        with (OUT/name).open('x') as stream:
            result = subprocess.run(args, cwd=DOCS, env=env, stdout=stream, stderr=subprocess.STDOUT, timeout=120)
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
    entries = sources()
    assert cited == entries.keys() and len(cited) == prepared['expected_cited_records']
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
        pdf=ref(PDF, 'Population and attribution working successor'), driver=ref(DRIVER, 'Preserving driver'),
        builder=ref(Path(__file__), 'Exact builder'), predecessor_pdf=ref(OLD.with_suffix('.pdf'), 'Preserved preceding reader'),
        source_audit=ref(OUT/'source-audit.json', f'{len(cited)} audited citation records'),
        cited_records=len(cited), added_anchors=anchors,
        warnings=[line for line in log.splitlines() if any(t in line for t in ['Warning', 'Overfull', 'Underfull', 'Missing character'])],
        final_acceptance=False, mandatory_repairs_closed=[], visual_acceptance=False,
        visual_review='Pending fresh image allowance; inherited session allowance exhausted')
    write(OUT/'build-report.json', report)
    layout.OUT = OUT
    layout.main()
    assert read(OUT/'text-layout-review.json')['status'] == 'pass'
    index = trace.audit(DRIVER, OUT/'source-audit.json')
    write(BASE/'traceability-review.json', index)
    assert index['status'] == 'pass' and not index['issues']
    assert index['scholarly_pdfs'] == prepared['expected_scholarly_pdfs']
    print(json.dumps(dict(pages=pages, records=len(cited), scholarly_pdfs=index['scholarly_pdfs'],
        anchors=anchors, warnings=report['warnings'], visual_acceptance=False)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['prepare', 'build'])
    {'prepare': prepare, 'build': build}[parser.parse_args().command]()
