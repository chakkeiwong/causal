#!/usr/bin/env python3
"""Preserve the prior sponsor and pair a reviewed successor to the actual reader."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET

import build_population_attribution_reader_20261020 as reader
import build_integrated_monograph_v12 as shared
import run_program_reviews_v2 as extension
import sponsor_economics_20261013 as economics
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run = extension.base
core = run.core
ROOT = reader.ROOT
DOCS = ROOT/'docs'
BASE = DOCS/'program/execution/2026-10-20/sponsor-population-attribution-v1'
OUT = BASE/'reader'
PRIOR = DOCS/'program/execution/2026-10-19/sponsor-r-effects-v1'
NAME = 'sponsor-proposal'
MIRROR = DOCS/'sponsor_proposal_population_attribution_reviewed_2026-10-20.pdf'


def read(path):
    return json.loads(path.read_text())


def snapshot(state):
    graph, merged, stages = run.combined(ROOT, state)
    results = merged['execution_program']['results']
    groups, bindings = {}, []
    for name, prefix, total in [('software_cells', 'SW.CELL.', 102),
            ('reuse_decisions', 'SW.DECISION.', 115), ('chapter_reviews', 'TEXT.REVIEW.', 22),
            ('llm_task_reviews', 'LL.TASK.', 14), ('integration_requirements', 'IN.REQ.', 12)]:
        selected = {k: v for k, v in results.items() if k.startswith(prefix)}
        groups[name] = dict(Counter(v['outcome'] for v in selected.values()), open=total-len(selected), total=total)
        bindings += list(selected.values())
    assert results['SW.CELL.effects_heterogeneity.R']['outcome'] == 'inconclusive'
    return dict(scope='Effective canonical proposal receipts; no implementation or final acceptance',
        reader=dict(state['reader']), **groups,
        census=ref(DOCS/'program/execution/2026-10-20/census-population-attribution-v1/census-register.json',
                   '51 inspected/62 unread out of 113'),
        evidence=bindings, mandatory_repairs_closed=[], final_acceptance=False)


def manuscript(pages):
    text = (PRIOR/'proposal.md').read_text()
    count = len(read(reader.OUT/'source-audit.json')['sources'])
    papers = read(reader.BASE/'traceability-review.json')['scholarly_pdfs']
    replacements = {
        '1,123 pages and 819 audited citation records, including 208 genuine scholarly PDFs':
            f'{pages:,} pages and {count} audited citation records, including {papers} genuine scholarly PDFs',
        '19 October 2026 working monograph': '20 October 2026 working monograph',
        'The original-candidate census now contains 49 inspected and 64 unread':
            'The original-candidate census now contains 51 inspected and 62 unread',
        'sp20rfx_reader': 'sp20pa_reader', 'sp20rfx_progress': 'sp20pa_progress'}
    for old,new in replacements.items():
        assert old in text,old
        text=text.replace(old,new)
    text=text.replace('sp20pa_reader}', 'sp20pa_reader,sp20rfx_reader}', 1)
    text=text.replace('sp20pa_progress}', 'sp20pa_progress,sp20rfx_progress}', 1)
    marker='# Public evidence before expensive bank experiments'
    assert text.count(marker)==1
    addition=(reader.BASE/'sponsor-addition.md').read_text()
    return text.replace(marker,addition+chr(10)+marker)


def prepare():
    assert not BASE.exists() and not MIRROR.exists()
    state = core.read(ROOT, core.STATE)
    assert run.same_reader(state['reader'], ref(reader.PDF, 'Current reader'))
    verify_bindings(read(reader.BASE/'working-release.json'))
    BASE.mkdir()
    OUT.mkdir()
    write(BASE/'progress-evidence.json', snapshot(state))
    write(BASE/'economics-results.json', economics.calculate())
    pages = state['reader']['pages']
    (BASE/'proposal.md').write_text(manuscript(pages))
    prior = read(PRIOR/'source-audit.json')
    verify_bindings(prior)
    prior_count = len(prior['sources'])
    write(BASE/'plan-review.json', dict(status='pass',
        scope='Preserving population and attribution sponsor reconciliation with dynamically derived citation counts',
        evidence=[ref(PRIOR/'proposal.md', 'Preserved sponsor source'),
            ref(PRIOR/'source-audit.json', f'{prior_count} prior citation identities'),
            ref(reader.BASE/'working-release.json', 'Exact paired reader'),
            ref(BASE/'proposal.md', 'Updated sponsor argument'), ref(BASE/'progress-evidence.json', 'Effective receipts')],
        checks=['Preserve previous substantive sections and all source identities.',
            'Separate population-response fidelity, controlled prompt effects and numerical causal identification.',
            'Keep incomplete coverage and proofs explicit without claiming a working adapter or bank qualification.',
            'Counts derive from actual cited source records; visual acceptance remains open.']))
    entries = {s['integrated_citation_key']: s for s in prior['sources']}
    inherited = read(reader.OUT/'source-audit.json')
    verify_bindings(inherited)
    for source in inherited['sources']:
        entries.setdefault(source['integrated_citation_key'], source)
    progress = read(BASE/'progress-evidence.json')
    for key, title, path, claim in [
        ('sp20pa_reader', 'Current population and attribution working reader', reader.BASE/'working-release.json',
         f'Exact {pages}-page reader with {len(inherited["sources"])} audited citation records; no final acceptance'),
        ('sp20pa_progress', 'Current effective proposal coverage', BASE/'progress-evidence.json',
         'Effective proposal receipts and census 51 inspected and 62 unread; no runtime integration capability')]:
        assert key not in entries
        entries[key] = dict(integrated_citation_key=key, kind='project_evidence_not_scholarly_paper',
            title=title, author='Causal banking proposal project', year=2026,
            source_identity=str(path.relative_to(ROOT)), version_date='20 October 2026; exact artifact bytes',
            local_copy=ref(path, claim), inspected_anchors=[dict(anchor=claim, inspection='Author inspection')],
            supported_claims=[claim], limitations=['Proposal evidence, not independent or bank acceptance.'])
    cited = {k.strip() for group in re.findall(shared.CITE, (BASE/'proposal.md').read_text()) for k in group.split(',')}
    assert cited <= entries.keys() and {s['integrated_citation_key'] for s in prior['sources']} <= cited
    sources = [entries[k] for k in sorted(cited)]
    assert len(sources) > prior_count
    audit = dict(sources=sources, cutoff='2026-10-07',
        predecessor_audit=ref(PRIOR/'source-audit.json', f'{prior_count} unchanged prior identities'),
        reader_audit=ref(reader.OUT/'source-audit.json', 'Current reader citations'),
        manuscript=ref(BASE/'proposal.md', 'Reconciled sponsor narrative'),
        plan_review=ref(BASE/'plan-review.json', 'Reviewed preserving plan'),
        economics_code=ref(ROOT/'tools/sponsor_economics_20261013.py', 'Unchanged exact economics'),
        economics_results=ref(BASE/'economics-results.json', 'Exact replay'))
    verify_bindings(audit)
    write(BASE/'source-audit.json', audit)
    bibliography=[]
    for source in sources:
        author = source['author'] if source['kind']=='paper' else '{'+shared.escape(source['author'])+'}'
        bibliography.append('@misc{'+source['integrated_citation_key']+',\n author={'+author+'},\n title={'+
            shared.escape(source['title'])+'},\n year={'+str(source['year'])+'},\n note={'+
            shared.escape(source['version_date'])+'}\n}\n')
    (BASE/'refs.bib').write_text('\n'.join(bibliography))
    subprocess.run(['pandoc', '--from=markdown+raw_tex+tex_math_single_backslash', '--to=latex',
        '--top-level-division=section', '--wrap=auto', str(BASE/'proposal.md'), '-o', str(BASE/'proposal.tex')],
        check=True, timeout=20)
    driver = (PRIOR/'reader/sponsor-proposal.tex').read_text().replace(
        'program/execution/2026-10-19/sponsor-r-effects-v1/',
        'program/execution/2026-10-20/sponsor-population-attribution-v1/')
    assert r'\usepackage[numbers,square]{natbib}' in driver and r'\bibliographystyle{unsrt}' in driver
    (OUT/(NAME+'.tex')).write_text(driver)
    print(json.dumps(dict(prepared=str(BASE.relative_to(ROOT)), citations=len(cited), paired_pages=pages)))


def build():
    assert not (BASE/'build-report.json').exists() and not MIRROR.exists()
    verify_bindings(read(BASE/'source-audit.json'))
    command = ['pdflatex', '-interaction=nonstopmode', '-halt-on-error', '-no-shell-escape',
               '-output-directory', str(OUT), str(OUT/(NAME+'.tex'))]
    def execute(args, name):
        with (OUT/name).open('x') as stream:
            subprocess.run(args, cwd=DOCS, stdout=stream, stderr=subprocess.STDOUT, check=True, timeout=55)
    execute(command, 'pass-1.log')
    execute(['bibtex', str((OUT/NAME).relative_to(DOCS))], 'bibtex-pass.log')
    for turn in range(2, 5):
        execute(command, f'pass-{turn}.log')
        log = (OUT/(NAME+'.log')).read_text(errors='replace')
        if turn >= 3 and not any(t in log for t in ['Label(s) may have changed', 'Rerun to get']):
            break
    for token in ['undefined citations', 'undefined references', 'multiply defined', 'Missing character', 'Overfull']:
        assert token not in log, token
    pdf = OUT/(NAME+'.pdf')
    info = subprocess.check_output(['pdfinfo', str(pdf)], text=True, timeout=15)
    pages = int(re.search(r'(?m)^Pages:\s+(\d+)', info).group(1))
    subprocess.run(['pdftotext', '-layout', str(pdf), str(BASE/'reader.txt')], check=True, timeout=20)
    subprocess.run(['pdftotext', '-bbox', str(pdf), str(BASE/'reader-bbox.html')], check=True, timeout=20)
    tree = ET.fromstring((BASE/'reader-bbox.html').read_text())
    ns = {'h': 'http://www.w3.org/1999/xhtml'}
    bad, empty = [], []
    for i, page in enumerate(tree.findall('.//h:page', ns), 1):
        words = page.findall('.//h:word', ns)
        if not words:
            empty.append(i)
        for word in words:
            if (float(word.attrib['xMin']) < 0 or float(word.attrib['yMin']) < 0 or
                    float(word.attrib['xMax']) > float(page.attrib['width']) or
                    float(word.attrib['yMax']) > float(page.attrib['height'])):
                bad.append(dict(page=i, word=word.text))
    assert not bad and not empty
    assert read(BASE/'economics-results.json') == economics.calculate()
    MIRROR.write_bytes(pdf.read_bytes())
    report = dict(status='compiled_source_and_text_checked_working_proposal', pages=pages,
        pdf=ref(pdf, 'Sponsor operation output'), reader_copy=ref(MIRROR, 'Exact-byte sponsor delivery'),
        paired_monograph=ref(reader.PDF, 'Actual current working monograph'),
        source_audit=ref(BASE/'source-audit.json', str(len(read(BASE/'source-audit.json')['sources']))+' source records'),
        manuscript=ref(BASE/'proposal.md', 'Preserving sponsor source'),
        compiled_content=ref(BASE/'proposal.tex', 'Compiled source'),
        bibliography=ref(BASE/'refs.bib', 'Complete bibliography'),
        driver=ref(OUT/(NAME+'.tex'), 'Exact sponsor driver'), builder=ref(Path(__file__), 'Preserving bounded builder'),
        cited_records=len(read(BASE/'source-audit.json')['sources']), empty_pages=empty, text_bounds_issues=bad,
        warnings=[line for line in log.splitlines() if 'Warning' in line or 'Underfull' in line],
        visual_acceptance=False, final_proposal_acceptance=False, bank_product_acceptance=False)
    write(BASE/'build-report.json', report)
    print(json.dumps(dict(pages=pages, records=report['cited_records'], pdf=str(MIRROR.relative_to(ROOT)), warnings=report['warnings'])))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['prepare', 'build'])
    {'prepare': prepare, 'build': build}[parser.parse_args().command]()
