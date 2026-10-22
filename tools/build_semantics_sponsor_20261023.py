#!/usr/bin/env python3
"""Preserve the sponsor and pair semantic findings with the exact current reader."""
import argparse
import json
from pathlib import Path
import re
import subprocess

import build_prophets_repository_sponsor_20261021 as engine
import build_semantics_reader_v4_20261023 as reader
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run, core = engine.run, engine.core
ROOT = reader.ROOT
DOCS = ROOT / 'docs'
BASE = DOCS / 'program/execution/2026-10-23/sponsor-semantics-v1'
OUT = BASE / 'reader'
PRIOR = DOCS / 'program/execution/2026-10-22/sponsor-workflow-v1'
NAME = 'sponsor-proposal'
MIRROR = DOCS / 'sponsor_proposal_semantics_reviewed_2026-10-23.pdf'
read = lambda p: json.loads(p.read_text())


def manuscript(pages):
    text = (PRIOR / 'proposal.md').read_text()
    count = len(read(reader.OUT / 'source-audit.json')['sources'])
    papers = read(reader.BASE / 'traceability-review.json')['scholarly_pdfs']
    replacements = {
        '22 October 2026 working monograph': '23 October 2026 working monograph',
        '1,240 pages and 932 audited citation records, including 221 genuine scholarly PDFs':
            f'{pages:,} pages and {count} audited citation records, including {papers} genuine scholarly PDFs',
        '81 open and three inconclusive decisions': '79 open and three inconclusive decisions',
        '61 inspected and 52 unread originals': '63 inspected and 50 unread originals',
    }
    for old, new in replacements.items():
        assert text.count(old) == 1, old
        text = text.replace(old, new)
    text = text.replace('sp22wf_reader', 'sp23sm_reader').replace('sp22wf_progress', 'sp23sm_progress')
    text = text.replace('sp23sm_reader,', 'sp23sm_reader,sp22wf_reader,', 1)
    text = text.replace('sp23sm_progress,', 'sp23sm_progress,sp22wf_progress,', 1)
    marker = '# Public evidence before expensive bank experiments'
    assert text.count(marker) == 1
    return text.replace(marker, (reader.BASE / 'sponsor-addition.md').read_text() + '\n' + marker)


def prepare():
    assert not BASE.exists() and not MIRROR.exists()
    state = core.read(ROOT, core.STATE)
    assert state['execution_runtime']['active'] is None
    assert run.same_reader(state['reader'], ref(reader.PDF, 'Current reader'))
    assert {q['id']: q['status'] for q in run.status(ROOT, state)['proposal_gaps']} == dict(
        Q1='open', Q2='pass', Q3='pass', Q4='pass', Q5='open')
    verify_bindings(read(reader.BASE / 'working-release.json'))
    BASE.mkdir(parents=True)
    OUT.mkdir()
    progress = engine.snapshot(state)
    progress['census'] = ref(reader.CENSUS / 'census-register.json', '63 inspected/50 unread out of113')
    write(BASE / 'progress-evidence.json', progress)
    write(BASE / 'economics-results.json', engine.economics.calculate())
    pages = state['reader']['pages']
    (BASE / 'proposal.md').write_text(manuscript(pages))
    prior = read(PRIOR / 'source-audit.json')
    verify_bindings(prior)
    write(BASE / 'plan-review.json', dict(status='pass',
        scope='Preserve sponsor sources and reconcile exact reader, intervention semantics and current coverage',
        evidence=[ref(PRIOR / 'proposal.md', 'Prior source'), ref(PRIOR / 'source-audit.json', 'Preserved identities'),
            ref(reader.BASE / 'working-release.json', 'Exact reader'), ref(BASE / 'proposal.md', 'Updated sponsor'),
            ref(BASE / 'progress-evidence.json', 'Effective receipts'), ref(Path(__file__), 'Preserving builder')],
        checks=['All earlier substantive sections and citation identities survive.',
            'Only current reader/count/coverage paragraphs and the new substantive section change.',
            'Twins, conflict critique and software choices retain source/rights/execution limits.',
            'Public/generated prototype merit precedes costly bank trials; visual and final acceptance remain open.']))
    entries = {s['integrated_citation_key']: s for s in prior['sources']}
    inherited = read(reader.OUT / 'source-audit.json')
    verify_bindings(inherited)
    for source in inherited['sources']:
        entries.setdefault(source['integrated_citation_key'], source)
    for key, title, path, claim in [
        ('sp23sm_reader', 'Current integrated causal and software semantics working reader', reader.BASE / 'working-release.json',
         f'Exact{pages}-page reader with{len(inherited["sources"])} audited records; not final acceptance'),
        ('sp23sm_progress', 'Current effective proposal coverage', BASE / 'progress-evidence.json',
         'Effective software/reuse/chapter receipts and census63/50; no native capability')]:
        assert key not in entries
        entries[key] = dict(integrated_citation_key=key, kind='project_evidence_not_scholarly_paper',
            title=title, author='Causal banking proposal project', year=2026, source_identity=str(path.relative_to(ROOT)),
            version_date='23 October 2026; exact artifact bytes', local_copy=ref(path, claim),
            inspected_anchors=[dict(anchor=claim, inspection='Author inspection')], supported_claims=[claim],
            limitations=['Proposal evidence, not independent or bank acceptance.'])
    cited = {k.strip() for group in re.findall(engine.shared.CITE, (BASE / 'proposal.md').read_text()) for k in group.split(',')}
    assert cited <= entries.keys() and {s['integrated_citation_key'] for s in prior['sources']} <= cited
    sources = [entries[k] for k in sorted(cited)]
    assert len(sources) == len(prior['sources']) + len(read(reader.BASE / 'source-audit.json')['sources']) + 2
    audit = dict(sources=sources, cutoff='2026-10-07', predecessor_audit=ref(PRIOR / 'source-audit.json', 'Unchanged prior sources'),
        reader_audit=ref(reader.OUT / 'source-audit.json', 'Current integrated citations'),
        manuscript=ref(BASE / 'proposal.md', 'Reconciled sponsor'), plan_review=ref(BASE / 'plan-review.json', 'Plan review'),
        economics_code=ref(ROOT / 'tools/sponsor_economics_20261013.py', 'Unchanged exact economics'),
        economics_results=ref(BASE / 'economics-results.json', 'Exact replay'))
    verify_bindings(audit)
    write(BASE / 'source-audit.json', audit)
    bib = []
    for s in sources:
        author = s.get('author', s.get('authors', s.get('name', 'Software') + ' contributors'))
        if isinstance(author, list):
            author = ' and '.join(author)
        author = author.replace(', ', ' and ') if s['kind'] == 'paper' else '{' + engine.shared.escape(author) + '}'
        title = s.get('title', s.get('name', 'Software') + ' primary source review')
        version = s.get('version_date', s.get('version_status', 'Bound local original'))
        if isinstance(version, dict):
            version = json.dumps(version, sort_keys=True)
        bib.append('@misc{' + s['integrated_citation_key'] + ',\n author={' + author + '},\n title={' +
            engine.shared.escape(title) + '},\n year={' + str(s.get('year', 2026)) + '},\n note={' +
            engine.shared.escape(version) + '}\n}\n')
    (BASE / 'refs.bib').write_text('\n'.join(bib))
    subprocess.run(['pandoc', '--from=markdown+raw_tex+tex_math_single_backslash', '--to=latex',
        '--top-level-division=section', '--wrap=auto', str(BASE / 'proposal.md'), '-o', str(BASE / 'proposal.tex')], check=True, timeout=20)
    driver = (PRIOR / 'reader/sponsor-proposal.tex').read_text().replace(
        str(PRIOR.relative_to(DOCS)) + '/', str(BASE.relative_to(DOCS)) + '/').replace('22 October 2026', '23 October 2026')
    (OUT / (NAME + '.tex')).write_text(driver)
    print(json.dumps(dict(prepared=str(BASE.relative_to(ROOT)), citations=len(cited), paired_pages=pages)))


def build():
    for name in ['ROOT', 'DOCS', 'BASE', 'OUT', 'PRIOR', 'NAME', 'MIRROR', 'reader']:
        setattr(engine, name, globals()[name])
    engine.build()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['prepare', 'build'])
    {'prepare': prepare, 'build': build}[parser.parse_args().command]()
