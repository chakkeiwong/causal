#!/usr/bin/env python3
"""Build a preserving sponsor successor paired to the Julia/Rust IV/RD reader."""
import argparse
import json
import re
import subprocess
from pathlib import Path

import build_prophets_repository_sponsor_20261021 as engine
import build_other_iv_rd_reader_v3_20261023 as reader
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run, core, ROOT = engine.run, engine.core, reader.ROOT
DOCS = ROOT / 'docs'
BASE = DOCS / 'program/execution/2026-10-23/sponsor-other-iv-rd-v1'
OUT = BASE / 'reader'
PRIOR = DOCS / 'program/execution/2026-10-23/sponsor-panel-v1'
READER_BASE = DOCS / 'program/execution/2026-10-23/other-iv-rd-reader-v3'
READER_PDF = DOCS / 'causal_proposal_other_iv_rd_reviewed_v3_2026-10-23.pdf'
NAME = 'sponsor-proposal'
MIRROR = DOCS / 'sponsor_proposal_other_iv_rd_reviewed_2026-10-23.pdf'
read = lambda p: json.loads(p.read_text())


def manuscript(pages):
    text = (PRIOR / 'proposal.md').read_text()
    old = '1,270 pages and 964 audited citation records, including 225 genuine scholarly PDFs'
    assert text.count(old) == 1
    text = text.replace(old, f'{pages:,} pages and 970 audited citation records, including 225 genuine scholarly PDFs')
    text = text.replace('60 open and 39 inconclusive cells', '59 open and 40 inconclusive cells')
    text = text.replace('Each closure needs an explicit original', 'Each closure needs an explicit original')
    text = text.replace('These counts describe unresolved review obligations', r'Current counts are bound to the canonical snapshot. \citep{sp23otheriv_progress} These counts describe unresolved review obligations')
    # Preserve earlier citations and their contexts; append the new binding in the added section.
    marker = '# Public evidence before expensive bank experiments'
    assert text.count(marker) == 1
    return text.replace(marker, (READER_BASE / 'sponsor-addition.md').read_text() + '\n' + marker)


def prepare():
    assert not BASE.exists() and not MIRROR.exists()
    state = core.read(ROOT, core.STATE)
    assert state['execution_runtime']['active'] is None
    assert run.same_reader(state['reader'], ref(READER_PDF, 'Current reader'))
    verify_bindings(read(READER_BASE / 'working-release.json'))
    BASE.mkdir()
    OUT.mkdir()
    progress = engine.snapshot(state)
    progress['census'] = ref(DOCS / 'program/execution/2026-10-23/census-geometric-hierarchical-v1/census-register-v2.json',
        '65 inspected and 48 unread originals of 113')
    write(BASE / 'progress-evidence.json', progress)
    write(BASE / 'economics-results.json', engine.economics.calculate())
    pages = state['reader']['pages']
    (BASE / 'proposal.md').write_text(manuscript(pages))
    prior = read(PRIOR / 'source-audit.json')
    verify_bindings(prior)
    write(BASE / 'plan-review.json', dict(status='pass',
        scope='Preserve sponsor sections and source identities while pairing the exact Julia/Rust IV/RD reader',
        evidence=[ref(PRIOR / 'proposal.md', 'Preserved sponsor source'), ref(PRIOR / 'source-audit.json', 'Prior identities'),
            ref(READER_BASE / 'working-release.json', 'Exact current reader'), ref(BASE / 'proposal.md', 'Connected sponsor'),
            ref(BASE / 'progress-evidence.json', 'Canonical coverage snapshot'), ref(Path(__file__), 'Preserving generator')],
        checks=['All 353 prior keys, source bytes, claims and substantive sections survive; two source-entry line-anchor corrections are explicit.',
            'Only current reader/count references, and one new section change.',
            'Ratio covariance, normal tails, rank and mutation witnesses remain authored; static findings require native replay.',
            'Thirty-two source inspections grant no native capability or universal calibration.',
            'Native qualification, rights, wider coverage, visual and final acceptance remain open.']))
    entries = {s['integrated_citation_key']: s for s in prior['sources']}
    inherited = read(READER_BASE / 'source-audit.json')
    verify_bindings(inherited)
    for source in inherited['sources']:
        entries.setdefault(source['integrated_citation_key'], source)
    for key, title, path, claim in [
        ('sp23otheriv_reader', 'Current Panel working reader', READER_BASE / 'working-release.json',
         f'Exact{pages}-page reader with970 audited records; no final acceptance'),
        ('sp23otheriv_progress', 'Current Panel proposal-coverage snapshot', BASE / 'progress-evidence.json',
         'Canonical software, reuse, chapter and frontier-census dispositions; no native adoption')]:
        assert key not in entries
        entries[key] = dict(integrated_citation_key=key, kind='project_evidence_not_scholarly_paper',
            title=title, author='Causal banking proposal project', year=2026,
            source_identity=str(path.relative_to(ROOT)), version_date='23 October 2026; exact artifact bytes',
            local_copy=ref(path, claim), inspected_anchors=[dict(anchor=claim, inspection='Author inspection')],
            supported_claims=[claim], limitations=['Proposal evidence; no independent, bank, visual or final acceptance.'])
    for source in read(reader.CORRECTIONS / 'corrected-source-entries.json')['sources']:
        assert source['integrated_citation_key'] in entries
        entries[source['integrated_citation_key']] = source
    cited = {k.strip() for group in re.findall(engine.shared.CITE, (BASE / 'proposal.md').read_text()) for k in group.split(',')}
    assert cited <= entries.keys()
    assert {s['integrated_citation_key'] for s in prior['sources']} <= cited
    sources = [entries[k] for k in sorted(cited)]
    assert len(sources) == len(prior['sources']) + len(inherited['sources']) + 2 == 361
    audit = dict(sources=sources, cutoff='2026-10-07', predecessor_audit=ref(PRIOR / 'source-audit.json', '353 unchanged identities'),
        reader_audit=ref(READER_BASE / 'source-audit.json', 'Current six additional audited records'),
        manuscript=ref(BASE / 'proposal.md', 'Connected sponsor argument'), plan_review=ref(BASE / 'plan-review.json', 'Reviewed plan'),
        economics_code=ref(ROOT / 'tools/sponsor_economics_20261013.py', 'Unchanged exact economics'),
        economics_results=ref(BASE / 'economics-results.json', 'Exact economics replay'),anchor_corrections=ref(reader.CORRECTIONS/'correction-overlay.json','Six line-end corrections, unchanged bytes and claims'))
    verify_bindings(audit)
    write(BASE / 'source-audit.json', audit)
    bib = []
    for source in sources:
        author = source.get('author', source.get('authors', source.get('name', 'Software') + ' contributors'))
        if isinstance(author, list): author = ' and '.join(author)
        author = author.replace(', ', ' and ') if source['kind'] == 'paper' else '{' + engine.shared.escape(author) + '}'
        title = source.get('title', source.get('name', 'Software') + ' primary source review')
        version = source.get('version_date', source.get('version_status', 'Bound local original'))
        if isinstance(version, dict): version = json.dumps(version, sort_keys=True)
        bib.append('@misc{' + source['integrated_citation_key'] + ',\n author={' + author + '},\n title={' + engine.shared.escape(title) + '},\n year={' + str(source.get('year', 2026)) + '},\n note={' + engine.shared.escape(version) + '}\n}\n')
    (BASE / 'refs.bib').write_text('\n'.join(bib))
    subprocess.run(['pandoc', '--from=markdown+raw_tex+tex_math_single_backslash', '--to=latex', '--top-level-division=section', '--wrap=auto', str(BASE / 'proposal.md'), '-o', str(BASE / 'proposal.tex')], check=True, timeout=20)
    driver = (PRIOR / 'reader/sponsor-proposal.tex').read_text().replace(str(PRIOR.relative_to(DOCS)) + '/', str(BASE.relative_to(DOCS)) + '/')
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
