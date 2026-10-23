#!/usr/bin/env python3
"""Build a preserving sponsor successor paired to the specialist collaboration provenance/denominator/scoring reader."""
import argparse
import json
import re
import subprocess
from pathlib import Path

import build_prophets_repository_sponsor_20261021 as engine
import build_collaboration_reader_v2_20261024 as reader
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run, core, ROOT = engine.run, engine.core, reader.ROOT
DOCS = ROOT / 'docs'
BASE = DOCS / 'program/execution/2026-10-24/sponsor-collaboration-v1'
OUT = BASE / 'reader'
PRIOR = DOCS / 'program/execution/2026-10-23/sponsor-recon-memory-v1'
READER_BASE = DOCS / 'program/execution/2026-10-24/collaboration-reader-v2'
READER_PDF = DOCS / 'causal_proposal_collaboration_v2_reviewed_2026-10-24.pdf'
NAME = 'sponsor-proposal'
MIRROR = DOCS / 'sponsor_proposal_collaboration_reviewed_2026-10-24.pdf'
read = lambda p: json.loads(p.read_text())


def manuscript(pages):
    text = (PRIOR / 'proposal.md').read_text()
    old = '1,336 pages and 1017 audited citation records, including 234 genuine scholarly PDFs'
    assert text.count(old) == 1
    text = text.replace(old, f'{pages:,} pages and 1019 audited citation records, including 235 genuine scholarly PDFs')
    text = text.replace('This brief accompanies the 23 October 2026 working monograph', 'This brief accompanies the 24 October 2026 working monograph', 1)
    entries = {x['integrated_citation_key']: x for x in read(PRIOR / 'source-audit.json')['sources']}
    keys = ['sp23nt_progress','sp23sc_progress','sp23admission_progress','sp23proof_progress',
            'sp23sensitivity_progress','sp23gist_progress','sp23medflex_progress',
            'sp23controlled_progress','sp23sua_progress','sp23recon_progress']
    paragraphs = text.split(chr(10) * 2)
    for i, para in enumerate(paragraphs):
        if 'inspected' not in para or 'unread' not in para:
            continue
        if para.startswith('Twenty of 22 chapter reviews'):
            para = para.replace('72 inspected and 41 unread', '73 inspected and 40 unread')
            para += ' Current census totals are bound to this release. ' + chr(92) + 'citep{sp24collaboration_progress}'
        else:
            matched = [k for k in keys if k in para]
            if not matched:
                continue
            assert len(matched) == 1
            snapshot = read(ROOT / entries[matched[0]]['local_copy']['path'])
            counts = read(ROOT / snapshot['census']['path'])['counts']
            inspected = counts['inspected_primary_retained_with_limits']
            unread = counts['open_original_not_inspected']
            para, n = re.subn(r'72 inspected and\s*(?:41|43)\s*unread',
                             f'{inspected} inspected and {unread} unread', para)
            assert n == 1, matched[0]
            para = 'At that cited review stage, the following figures apply. ' + para
        paragraphs[i] = para
    text = (chr(10) * 2).join(paragraphs)
    marker = '# Public evidence before expensive bank experiments'
    assert text.count(marker) == 1
    addition = (READER_BASE / 'sponsor-addition.md').read_text()
    addition += ('The current census has 73 inspected and 40 unread originals out of 113, with four crosscutting obligations open. '
                 'The current reuse register has 51 passing proposal dispositions, three inconclusive and 61 open. '
                 + chr(92) + 'citep{sp24collaboration_reader,sp24collaboration_progress}' + chr(10) * 2)
    return text.replace(marker, addition + marker)


def prepare():
    assert not BASE.exists() and not MIRROR.exists()
    state = core.read(ROOT, core.STATE)
    assert state['execution_runtime']['active'] is None
    assert run.same_reader(state['reader'], ref(READER_PDF, 'Current reader'))
    verify_bindings(read(READER_BASE / 'working-release.json'))
    BASE.mkdir()
    OUT.mkdir()
    progress = engine.snapshot(state)
    progress['census'] = ref(DOCS / 'program/execution/2026-10-24/census-language-collaboration-v1/census-register.json',
        '73 inspected and 40 unread originals of 113')
    write(BASE / 'progress-evidence.json', progress)
    write(BASE / 'economics-results.json', engine.economics.calculate())
    pages = state['reader']['pages']
    (BASE / 'proposal.md').write_text(manuscript(pages))
    prior = read(PRIOR / 'source-audit.json')
    verify_bindings(prior)
    write(BASE / 'plan-review.json', dict(status='pass',
        scope='Preserve sponsor sections and source identities while pairing the exact specialist collaboration reader',
        evidence=[ref(PRIOR / 'proposal.md', 'Preserved sponsor source'), ref(PRIOR / 'source-audit.json', 'Prior identities'),
            ref(READER_BASE / 'working-release.json', 'Exact current reader'), ref(BASE / 'proposal.md', 'Connected sponsor'),
            ref(BASE / 'progress-evidence.json', 'Canonical coverage snapshot'), ref(Path(__file__), 'Preserving generator')],
        checks=['All 448 prior source identities and substantive arguments survive; historical census numbers are corrected from their bound snapshots.',
            'Current reader/count references and one new section change; historical census counts are corrected against their exact cited snapshots.',
            'Original proof conditions and reported software claims remain distinct from native verification.',
            'One genuine scholarly original and authored counterexamples and independent witnesses grant no native capability.',
            'Native qualification, rights, wider coverage, visual and final acceptance remain open.']))
    entries = {s['integrated_citation_key']: s for s in prior['sources']}
    inherited = read(READER_BASE / 'source-audit.json')
    verify_bindings(inherited)
    for source in inherited['sources']:
        entries.setdefault(source['integrated_citation_key'], source)
    for key, title, path, claim in [
        ('sp24collaboration_reader', 'Current specialist collaboration working reader', READER_BASE / 'working-release.json',
         f'Exact {pages}-page reader with 1019 audited records; no final acceptance'),
        ('sp24collaboration_progress', 'Current specialist collaboration proposal-coverage snapshot', BASE / 'progress-evidence.json',
         'Canonical software, reuse, chapter and frontier-census dispositions; no native adoption')]:
        assert key not in entries
        entries[key] = dict(integrated_citation_key=key, kind='project_evidence_not_scholarly_paper',
            title=title, author='Causal banking proposal project', year=2026,
            source_identity=str(path.relative_to(ROOT)), version_date='24 October 2026; exact artifact bytes',
            local_copy=ref(path, claim), inspected_anchors=[dict(anchor=claim, inspection='Author inspection')],
            supported_claims=[claim], limitations=['Proposal evidence; no independent, bank, visual or final acceptance.'])
    cited = {k.strip() for group in re.findall(engine.shared.CITE, (BASE / 'proposal.md').read_text()) for k in group.split(',')}
    assert cited <= entries.keys()
    assert {s['integrated_citation_key'] for s in prior['sources']} <= cited
    sources = [entries[k] for k in sorted(cited)]
    assert len(sources) == len(prior['sources']) + len(inherited['sources']) + 2 == 452
    audit = dict(sources=sources, cutoff='2026-10-07', predecessor_audit=ref(PRIOR / 'source-audit.json', '448 unchanged identities'),
        reader_audit=ref(READER_BASE / 'source-audit.json', 'Two additional audited records'),
        manuscript=ref(BASE / 'proposal.md', 'Connected sponsor argument'), plan_review=ref(BASE / 'plan-review.json', 'Reviewed plan'),
        economics_code=ref(ROOT / 'tools/sponsor_economics_20261013.py', 'Unchanged exact economics'),
        economics_results=ref(BASE / 'economics-results.json', 'Exact economics replay'))
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
    (BASE / 'refs.bib').write_text('\n'.join(line.rstrip() for line in '\n'.join(bib).splitlines()) + '\n')
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
