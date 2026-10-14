#!/usr/bin/env python3
"""Build a preserved-source successor book for the V13.1 execution refresh."""
import argparse
import json
import os
import re
import subprocess
from pathlib import Path

import master_control as core
import build_integrated_monograph_v12 as shared
import build_gap_successor_v13 as prior

ROOT = core.ROOT
DOCS = ROOT/'docs'
BASE = DOCS/'program/gap-execution-v13_1'
OUT = BASE/'reader'
NAME = 'causal_integrated_working_v13_1_2026-10-12'
DRIVER = DOCS/(NAME+'.tex')
PDF = DOCS/(NAME+'.pdf')


def ref(path, anchor):
    return {'path': str(path.relative_to(ROOT)), 'sha256': core.sha(path), 'anchor': anchor}


def new_sources():
    entries = json.loads((BASE/'work/SW01/source-audit.json').read_text())['new_entries']
    entries.append({'kind': 'project_evidence', 'integrated_citation_key': 'v131_project_semantics',
        'name': 'Causal banking project semantic examples', 'source_identity': 'Original project derivations',
        'version_date': '2026-10-12',
        'local_copy': ref(ROOT/'tools/gap_semantic_examples_v13_1.py', 'Deterministic example code'),
        'inspected_anchors': [ref(BASE/'semantic-examples.json', 'All five exact example families'),
            ref(BASE/'chapters/graph-and-uncertainty.tex', 'Orientation, group variance and orthogonal-score derivation'),
            ref(BASE/'chapters/histories-forests-densities.tex', 'Competing-event and density-unit derivations')],
        'supported_claims': ['Stipulated arithmetic and the explicitly conditioned algebraic identities in the two chapters.'],
        'limits': ['Not package execution, a new qualification study, observed bank evidence or ROI.']})
    return entries


def build():
    state = core.read(ROOT, core.STATE)
    if any(x['path'] == str(PDF.relative_to(ROOT)) for x in state['deliveries']):
        raise ValueError('Delivered bytes are frozen; use another successor')
    prior.check(ref(prior.OUT/'build-report.json', 'Preserved V13 build'))
    OUT.mkdir(parents=True, exist_ok=True)
    raw = prior.DRIVER.read_text()
    assert 'Integrated working edition, revision 13' in raw
    raw = raw.replace('Integrated working edition, revision 13', 'Integrated working edition, revision 13.1', 1)
    inputs = '\n'.join('\\input{'+str((BASE/'chapters'/p).relative_to(DOCS))+'}'
                        for p in ['graph-and-uncertainty.tex', 'histories-forests-densities.tex'])
    token = r'\label{integrated:software-end}'
    assert raw.count(token) == 1
    raw = raw.replace(token, inputs+'\n'+token, 1)
    token = 'program/gap-repair-v13/reader/new-refs}'
    assert raw.count(token) == 1
    raw = raw.replace(token, 'program/gap-repair-v13/reader/new-refs,program/gap-execution-v13_1/reader/new-refs}', 1)
    DRIVER.write_text(raw)
    bibliography = []
    for e in new_sources():
        key = e['integrated_citation_key']
        if e['kind'] == 'project_evidence':
            author = '{Causal banking research project}'
            title = 'Exact semantic examples for causal software integration'
            note = 'Original stipulated project calculations; no package or bank qualification'
            url = ''
        else:
            author = '{'+shared.escape(e['name'])+' project}'
            title = shared.escape(e['name']+': inspected dependency paths and semantic limits')
            note = shared.escape('Commit '+e['version_date']['commit']+'; '+e['version_date']['commit_date'][:10]+
                                 '; inspected 12 October 2026. Selected source review, runtime untested')
            url = e['source_identity']
        bibliography.append('@misc{'+key+',\n author={'+author+'},\n title={'+title+'},\n year={2026},\n note={'+note+'}'+
                            (',\n url={'+url+'}' if url else '')+'\n}\n')
    (OUT/'new-refs.bib').write_text('\n'.join(bibliography))
    env = dict(os.environ)
    env['TEXINPUTS'] = str(DOCS)+'//:'+env.get('TEXINPUTS', '')
    env['BIBINPUTS'] = str(DOCS)+'//:'+env.get('BIBINPUTS', '')
    latex = ['pdflatex', '-no-shell-escape', '-interaction=nonstopmode', '-halt-on-error',
             '-output-directory='+str(OUT), str(DRIVER)]
    def run(args, name):
        with (OUT/name).open('w') as stream:
            result = subprocess.run(args, cwd=DOCS, env=env, stdout=stream, stderr=subprocess.STDOUT, timeout=90)
        if result.returncode:
            raise ValueError('Build failed; inspect '+str(OUT/name))
    run(latex, 'pass-1.log')
    run(['bibtex', str((OUT/NAME).relative_to(DOCS))], 'bibtex-pass.log')
    for i in range(2, 6):
        run(latex, f'pass-{i}.log')
        log = (OUT/(NAME+'.log')).read_text(errors='replace')
        if i >= 3 and not any(x in log for x in ['Label(s) may have changed', 'Rerun to get']):
            break
    if any(x in log for x in ['undefined citations', 'undefined references', 'multiply defined', 'Missing character']):
        raise ValueError('Unresolved citation/reference/character warning')
    PDF.write_bytes((OUT/(NAME+'.pdf')).read_bytes())
    files = shared.scan(DRIVER)
    combined = '\n'.join(text for _, text in files)
    labels = re.findall(shared.LABEL, combined)
    assert len(labels) == len(set(labels)), 'Duplicate labels'
    references = set(re.findall(r'\\(?:ref|eqref|cref|Cref)\{([^}]+)\}', combined))
    assert references <= set(labels), 'Unresolved label'
    cited = {k.strip() for group in re.findall(shared.CITE, combined) for k in group.split(',')}
    inherited = json.loads((prior.OUT/'source-audit.json').read_text())
    entries = {e['integrated_citation_key']: e for e in inherited['sources']}
    entries.update({e['integrated_citation_key']: e for e in new_sources()})
    assert cited <= entries.keys(), 'Missing audited citation'
    audit = {'predecessor_audit': ref(prior.OUT/'source-audit.json', 'All inherited V13 sources retained'),
        'sources': [entries[k] for k in sorted(cited)],
        'tex_files': [ref(p, 'Complete integrated source') for p in sorted({p for p, _ in files})],
        'new_bibliography': ref(OUT/'new-refs.bib', 'Eight package and one project records'),
        'survey_audit': ref(BASE/'work/SW01/source-audit.json', 'Scoped primary dependency inspection'),
        'cutoff': '2026-10-07', 'visual_acceptance': False}
    shared.verify_refs(audit)
    core.write(OUT/'source-audit.json', audit)
    subprocess.run(['pdftotext', '-layout', str(PDF), str(OUT/'reader.txt')], check=True, timeout=30)
    info = subprocess.check_output(['pdfinfo', str(PDF)], text=True, timeout=15)
    pages = int(re.search(r'(?m)^Pages:\s+(\d+)', info).group(1))
    aux = (OUT/(NAME+'.aux')).read_text()
    page_labels = {m.group(1): int(m.group(2)) for m in re.finditer(r'\\newlabel\{([^}]+)\}\{\{[^}]*\}\{(\d+)\}', aux)}
    spans = {kind: page_labels['integrated:'+kind+'-end']-page_labels[start]+1
             for kind, start in [('software', 'sw:interfaces'), ('llm', 'la:frontier'), ('integration', 'in:semantics')]}
    chapters = len(re.findall(r'\\contentsline \{chapter\}\{\\numberline', (OUT/(NAME+'.toc')).read_text()))
    warnings = [l for l in log.splitlines() if any(x in l for x in ['Warning', 'Overfull', 'Underfull', 'Missing character'])]
    report = {'status': 'compiled_source_and_text_checked_working_draft', 'pdf': ref(PDF, 'Unified V13.1 working book'),
        'driver': ref(DRIVER, 'Versioned whole-book driver'), 'source_audit': ref(OUT/'source-audit.json', 'Whole-book source audit'),
        'builder': ref(Path(__file__), 'Preserving builder/checker'), 'predecessor_pdf': ref(prior.PDF, 'Preserved 364-page book'),
        'pages': pages, 'numbered_chapters': chapters, 'cited_records': len(cited), 'physical_body_pages': spans,
        'source_files': len(audit['tex_files']), 'warnings': warnings, 'final_release': False, 'mandatory_repairs_closed': [],
        'body_page_status': 'Physical spans only; accepted substantive counts remain pending',
        'visual_review': 'Pending fresh session under exhausted inherited image allowance'}
    core.write(OUT/'build-report.json', report)
    print(json.dumps({k: report[k] for k in ['status', 'pages', 'numbered_chapters', 'cited_records', 'physical_body_pages', 'warnings']}))


def check(binding=None, state=None):
    binding = binding or ref(OUT/'build-report.json', 'Current versioned book')
    core.bound(ROOT, binding)
    report = core.read(ROOT, binding['path'])
    shared.verify_refs(report)
    audit = core.read(ROOT, report['source_audit']['path'])
    shared.verify_refs(audit)
    raw = '\n'.join(t for _, t in shared.scan(ROOT/report['driver']['path']))
    cited = {k.strip() for group in re.findall(shared.CITE, raw) for k in group.split(',')}
    if cited != {e['integrated_citation_key'] for e in audit['sources']}:
        raise ValueError('Citation/audit mismatch')
    info = subprocess.check_output(['pdfinfo', str(ROOT/report['pdf']['path'])], text=True, timeout=15)
    if int(re.search(r'(?m)^Pages:\s+(\d+)', info).group(1)) != report['pages']:
        raise ValueError('PDF page count differs from report')
    state = state if state is not None else core.read(ROOT, core.STATE)
    if state.get('successor_document') == binding or state.get('execution_refresh'):
        for field in ['path', 'sha256']:
            if state['reader'][field] != report['pdf'][field]:
                raise ValueError('Current reader differs from V13.1 report')
        if state['reader']['pages'] != report['pages']:
            raise ValueError('Current reader page count differs from V13.1 report')
    return {'status': 'pass', 'pages': report['pages'], 'cited_records': len(cited), 'final_acceptance': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['build', 'check', 'layout'])
    command = parser.parse_args().command
    if command == 'build':
        build()
    elif command == 'layout':
        import review_gap_reader_v13 as layout
        layout.OUT = OUT
        layout.main()
    else:
        print(json.dumps(check()))
