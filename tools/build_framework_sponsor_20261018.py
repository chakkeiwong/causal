#!/usr/bin/env python3
"""Preserve the prior sponsor and pair a reviewed successor to the actual reader."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET

import build_framework_reader_20261018 as reader
import build_integrated_monograph_v12 as shared
import run_program_reviews_v2 as extension
import sponsor_economics_20261013 as economics
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run = extension.base
core = run.core
ROOT = reader.ROOT
DOCS = ROOT/'docs'
BASE = DOCS/'program/execution/2026-10-18/sponsor-framework-v1'
OUT = BASE/'reader'
PRIOR = DOCS/'program/execution/2026-10-18/sponsor'
NAME = 'sponsor-proposal'
MIRROR = DOCS/'sponsor_proposal_framework_reviewed_2026-10-18.pdf'


def read(path):
    return json.loads(path.read_text())


def snapshot(state):
    graph, merged, stages = run.combined(ROOT, state)
    results = merged['execution_program']['results']
    groups = {}
    bindings = []
    for name, prefix, total in [('software_cells', 'SW.CELL.', 102),
            ('reuse_decisions', 'SW.DECISION.', 115), ('chapter_reviews', 'TEXT.REVIEW.', 22),
            ('llm_task_reviews', 'LL.TASK.', 14), ('integration_requirements', 'IN.REQ.', 12)]:
        selected = {k: v for k, v in results.items() if k.startswith(prefix)}
        counts = Counter(v['outcome'] for v in selected.values())
        groups[name] = dict(counts, open=total-len(selected), total=total)
        bindings += list(selected.values())
    assert groups['software_cells'] == {'pass': 2, 'inconclusive': 21, 'open': 79, 'total': 102}
    assert groups['reuse_decisions'] == {'pass': 15, 'inconclusive': 3, 'open': 97, 'total': 115}
    assert groups['chapter_reviews'] == {'pass': 20, 'inconclusive': 2, 'open': 0, 'total': 22}
    return dict(scope='Exact current-reader proposal snapshot; counts from effective canonical receipts',
        reader=dict(state['reader']), **groups,
        census=ref(reader.BASE/'census-register.json', '42 inspected/71 unread out of113'),
        evidence=bindings, mandatory_repairs_closed=[], final_acceptance=False)


def manuscript(pages):
    text = (PRIOR/'proposal.md').read_text()
    replacements = {
        '1,060 pages and 751 audited citation records, including 197 genuine scholarly PDFs':
            f'{pages:,} pages and 763 audited citation records, including 201 genuine scholarly PDFs',
        '80 open and 20 inconclusive cells': '79 open and 21 inconclusive cells',
        '99 open and one inconclusive decision': '97 open and three inconclusive decisions',
        '40 inspected and 73 unread originals': '42 inspected and 71 unread originals',
        'sp18_reader': 'sp18f_reader', 'sp18_progress': 'sp18f_progress', 'sp18_census': 'sp18f_census',
    }
    for old, new in replacements.items():
        assert old in text, old
        text = text.replace(old, new)
    marker = '## The reusable product and its customer'
    historical = ('The preceding brief and its source and coverage snapshot are the preserved '
        'baseline for these additional comparisons. \\citep{sp18_reader,sp18_progress,sp18_census}\n\n')
    assert text.count(marker) == 1
    text = text.replace(marker, historical+marker)
    marker = '# Public evidence before expensive bank experiments'
    addition = r'''## R identification and framework evaluation

The expanded R comparison distinguishes graphical adjustment, symbolic ID/IDC,
counterfactual identification, restricted sharp bounds and Bayesian causal
queries. These operations answer different questions. In an exact authored
repayment example, a point-identified average effect coexists with a nontrivial
counterfactual interval, while two admissible priors give different posterior
summaries. The supplied assumptions and result type therefore need to survive
any language adapter. Selected pinned sources support the comparison;
native R execution, broader census and complete dependency/rights qualification
remain unresolved. The causaleffect disposition is reference use with
executable integration deferred. \citep{sp18f_r_identification}

Two additional originals help specify a framework comparison. The selected
autonomous-agent survey organizes profile, memory, planning and action, and
discusses prompt fragility, hallucination, information leakage and efficiency.
PromptBench provides a documented modular evaluation design and custom metric
hooks; its historical findings do not show that one prompt is best for every
task. These sources support a proposed evaluator whose references check the
banking target, assumptions and valid nonidentification responses. They do not
establish a qualified causal agent, current model ranking or licensed software
integration. \citep{exec18_framework_agents_survey,exec18_framework_promptbench}

An exact bookkeeping illustration separates completion from correctness. Across
forty fixed requests in twenty paired families, stipulated system A has 22
correct, two wrong and sixteen unanswered requests; B has thirty correct, six
wrong and four unanswered. Accuracy among completed requests favors A, whereas
correct responses per planned request favor B. With assumed value and error
costs, their net-value ranking can reverse. These are authored outcomes and
prices, not observed model or bank performance. A justified scientific refusal
can be a completed correct answer; an execution failure remains in the planned
denominator. The comparison should preserve both distinctions and pairing.
\citep{exec18_framework_reference,sp18f_framework_review}

'''
    assert text.count(marker) == 1
    return text.replace(marker, addition+marker)


def prepare():
    assert not BASE.exists() and not MIRROR.exists()
    state = core.read(ROOT, core.STATE)
    assert run.same_reader(state['reader'], ref(reader.PDF, 'Current exact reader'))
    release = read(reader.BASE/'working-release.json')
    verify_bindings(release)
    BASE.mkdir()
    OUT.mkdir()
    write(BASE/'progress-evidence.json', snapshot(state))
    write(BASE/'economics-results.json', economics.calculate())
    pages = state['reader']['pages']
    (BASE/'proposal.md').write_text(manuscript(pages))
    write(BASE/'plan-review.json', dict(status='pass',
        scope='Preserving exact-reader sponsor reconciliation; no Q5 or final acceptance',
        evidence=[ref(PRIOR/'proposal.md', 'Preserved sponsor source'),
            ref(PRIOR/'source-audit.json', 'Preserved26 citation identities'),
            ref(reader.BASE/'working-release.json', 'Actual paired working monograph'),
            ref(BASE/'proposal.md', 'Reconciled source'), ref(BASE/'progress-evidence.json', 'Effective receipt counts')],
        checks=['Preserve all prior citation records, negative findings, funding/servicing discussion and exact economic section.',
                'Update only current reader/coverage claims and bounded R/framework findings.',
                'Source, compilation, text and arithmetic checks cannot award rendered acceptance.']))
    prior = read(PRIOR/'source-audit.json')
    verify_bindings(prior)
    entries = {s['integrated_citation_key']: s for s in prior['sources']}
    inherited = read(reader.OUT/'source-audit.json')
    verify_bindings(inherited)
    for source in inherited['sources']:
        entries.setdefault(source['integrated_citation_key'], source)
    records = [
        ('sp18f_reader', 'Current framework-evaluation working reader', reader.BASE/'working-release.json',
         f'Exact{pages}-page reader with763 audited citation records and201 genuine scholarly PDFs; no final acceptance'),
        ('sp18f_progress', 'Effective current proposal coverage snapshot', BASE/'progress-evidence.json',
         '79open/21inconclusive software cells;97open/3inconclusive reuse decisions;20passing/2inconclusive chapter reviews'),
        ('sp18f_census', 'Preserving original-candidate census', reader.BASE/'census-register.json',
         '42inspected/71unread out of113; only candidates19/244 changed; no frontier closure'),
        ('sp18f_r_identification', 'Bounded R-identification comparison and reference reuse',
         reader.PREDECESSOR/'release-source-review.json',
         'Adjustment, ID/IDC, counterfactual, sharp bounds and prior-sensitive queries; no native package execution'),
        ('sp18f_framework_review', 'Bounded framework source and exact accounting review',
         reader.BASE/'release-source-review.json',
         'General-source limits, completed versus unanswered results, exact paired counts and conditional assumed economics')]
    for key, title, path, claim in records:
        assert key not in entries
        entries[key] = dict(integrated_citation_key=key, kind='project_evidence_not_scholarly_paper',
            title=title, author='Causal banking proposal project', year=2026,
            source_identity=str(path.relative_to(ROOT)), version_date='Preserved artifact inspected18October2026',
            local_copy=ref(path, claim), inspected_anchors=[dict(anchor=claim, inspection='Author inspection')],
            supported_claims=[claim], limitations=['Author project evidence; no independent or bank acceptance.'])
    cited = {k.strip() for group in re.findall(shared.CITE, (BASE/'proposal.md').read_text()) for k in group.split(',')}
    assert cited <= entries.keys(), cited-entries.keys()
    assert {s['integrated_citation_key'] for s in prior['sources']} <= cited
    sources = [entries[k] for k in sorted(cited)]
    assert len(sources) == 34
    audit = dict(sources=sources, cutoff='2026-10-07',
        predecessor_audit=ref(PRIOR/'source-audit.json', 'All26 unchanged prior citation records'),
        reader_audit=ref(reader.OUT/'source-audit.json', 'Current working monograph citations'),
        manuscript=ref(BASE/'proposal.md', 'Reconciled sponsor narrative'),
        plan_review=ref(BASE/'plan-review.json', 'Reviewed preserving plan'),
        economics_code=ref(ROOT/'tools/sponsor_economics_20261013.py', 'Unchanged exact economics'),
        economics_results=ref(BASE/'economics-results.json', 'Fresh exact replay'))
    verify_bindings(audit)
    write(BASE/'source-audit.json', audit)
    bib = []
    for source in sources:
        author = source['author'] if source['kind'] == 'paper' else '{'+shared.escape(source['author'])+'}'
        bib.append('@misc{'+source['integrated_citation_key']+',\n author={'+author+'},\n title={'+
            shared.escape(source['title'])+'},\n year={'+str(source['year'])+'},\n note={'+
            shared.escape(source['version_date'])+'}\n}\n')
    (BASE/'refs.bib').write_text('\n'.join(bib))
    subprocess.run(['pandoc', '--from=markdown+raw_tex+tex_math_single_backslash', '--to=latex',
        '--top-level-division=section', '--wrap=auto', str(BASE/'proposal.md'), '-o', str(BASE/'proposal.tex')],
        check=True, timeout=20)
    driver = (PRIOR/'reader/sponsor-proposal.tex').read_text().replace(
        'program/execution/2026-10-18/sponsor/', 'program/execution/2026-10-18/sponsor-framework-v1/')
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
        source_audit=ref(BASE/'source-audit.json', '34 source records'),
        manuscript=ref(BASE/'proposal.md', 'Preserving sponsor source'),
        compiled_content=ref(BASE/'proposal.tex', 'Compiled source'),
        bibliography=ref(BASE/'refs.bib', 'Complete bibliography'),
        driver=ref(OUT/(NAME+'.tex'), 'Exact sponsor driver'), builder=ref(Path(__file__), 'Preserving bounded builder'),
        cited_records=34, empty_pages=empty, text_bounds_issues=bad,
        warnings=[line for line in log.splitlines() if 'Warning' in line or 'Underfull' in line],
        visual_acceptance=False, final_proposal_acceptance=False, bank_product_acceptance=False)
    write(BASE/'build-report.json', report)
    print(json.dumps(dict(pages=pages, records=34, pdf=str(MIRROR.relative_to(ROOT)), warnings=report['warnings'])))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['prepare', 'build'])
    {'prepare': prepare, 'build': build}[parser.parse_args().command]()
