#!/usr/bin/env python3
"""Preserve the prior sponsor and pair a reviewed successor to the actual reader."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET

import build_evaluation_code_reader_20261019 as reader
import build_integrated_monograph_v12 as shared
import run_program_reviews_v2 as extension
import sponsor_economics_20261013 as economics
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run = extension.base
core = run.core
ROOT = reader.ROOT
DOCS = ROOT/'docs'
BASE = DOCS/'program/execution/2026-10-19/sponsor-evaluation-code-v1'
OUT = BASE/'reader'
PRIOR = DOCS/'program/execution/2026-10-19/sponsor-java-identification-v1'
NAME = 'sponsor-proposal'
MIRROR = DOCS/'sponsor_proposal_evaluation_code_reviewed_2026-10-19.pdf'


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
    assert groups['software_cells'] == {'pass': 2, 'inconclusive': 24, 'open': 76, 'total': 102}
    assert groups['reuse_decisions'] == {'pass': 17, 'inconclusive': 3, 'open': 95, 'total': 115}
    assert groups['chapter_reviews'] == {'pass': 20, 'inconclusive': 2, 'open': 0, 'total': 22}
    return dict(scope='Exact current-reader proposal snapshot; counts from effective canonical receipts',
        reader=dict(state['reader']), **groups,
        census=ref(reader.BASE/'census-register.json', '46 inspected/67 unread out of113'),
        evidence=bindings, mandatory_repairs_closed=[], final_acceptance=False)


def manuscript(pages):
    text=(PRIOR/'proposal.md').read_text()
    replacements={
        '18 October 2026 working monograph':'19 October 2026 working monograph',
        '1,087 pages and 788 audited citation records, including 203 genuine scholarly PDFs':f'{pages:,} pages and 791 audited citation records, including 205 genuine scholarly PDFs',
        '44 inspected and 69 unread':'46 inspected and 67 unread',
        'sp19ji_reader':'sp19ec_reader','sp19ji_progress':'sp19ec_progress'}
    for old,new in replacements.items():
        assert old in text,old
        text=text.replace(old,new)
    marker='## The reusable product and its customer'
    historical='The preceding Java identification brief and its exact-reader coverage snapshot remain the preserved baseline for this evaluation comparison. '+chr(92)+'citep{sp19ji_reader,sp19ji_progress}\n\n'
    text=text.replace(marker,historical+marker)
    text=text.replace('sp19ec_progress,sp18ar_census','sp19ec_progress,sp19ec_census,sp18ar_census')
    marker='# Public evidence before expensive bank experiments'
    addition=r'''## Evaluate accepted causal outputs and all-request cost

Two inspected historical surveys organize evaluation by task, benchmark and
protocol, and code generation by its data, workflow and evaluation lifecycle.
Their compiled model scores and framework discussions remain secondary evidence
for the constituent systems. Evaluation must separately test contamination,
prompt robustness, human disagreement and model-judge bias; a dynamically
generated benchmark does not establish novelty by itself. The code survey's
June 2024 initial-version identity is retained alongside its conflicting
September 2024 template footer and distinct later discovery record.
\citep{exec19_surveys_evaluation,exec19_surveys_code}

The code survey's finite-pool pass-at-k formula and its description of the
successful-count variable conflict. Our exact illustration resolves the
counting convention explicitly: among ten candidates with three test passes,
a uniformly drawn pair contains a pass with probability 8/15. Choosing one
candidate uniformly gives only 3/10. Incorrectly substituting the success count
inside the selected pair produces 16/135. Turning at-least-one success into
output success therefore requires a qualified selector, whose errors and costs
must also be measured. Even correct tests do not establish the causal target.
\citep{exec19_surveys_code,exec19_surveys_reference}

In a separate stipulated workflow, twenty requests yield sixteen runnable
outputs, twelve test passes, seven target-valid results and five fully accepted
outputs. The runnable test-pass rate is 75 percent, while all-attempt acceptance
is 25 percent. Assumed generation and harness costs of USD 3 per attempt and
review costs of USD 5 per test pass total USD 120, or USD 24 per accepted output.
At an assumed USD 30 benefit per accepted output, net value is USD 30, or
USD 1.50 per attempt. Treating every test pass as accepted overstates total net
value by USD 210. These are illustrative assumptions, not observed performance,
provider prices or bank ROI. The proposed public/synthetic trial must retain
all attempts, retries, failures, abstentions, scientific adjudication and costs.
\citep{exec19_surveys_reference}

'''
    assert text.count(marker)==1
    return text.replace(marker,addition+marker)


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
            ref(PRIOR/'source-audit.json', 'Preserved70 citation identities'),
            ref(reader.BASE/'working-release.json', 'Actual paired working monograph'),
            ref(BASE/'proposal.md', 'Reconciled source'), ref(BASE/'progress-evidence.json', 'Effective receipt counts')],
        checks=['Use numeric natbib and standard unsrt to avoid the preserved plainnat suffix overflow; keep original source identities and dates.',
                'Preserve all70 prior citation records, negative findings, funding/servicing discussion and exact economic section.',
                'Update reader/software counts and critical survey findings and46/67 census; preserve Java, DuckDB, causal-agent, Python, R, graph/panel and economic arguments.',
                'Source, compilation, text and arithmetic checks cannot award rendered acceptance.']))
    prior = read(PRIOR/'source-audit.json')
    verify_bindings(prior)
    entries = {s['integrated_citation_key']: s for s in prior['sources']}
    inherited = read(reader.OUT/'source-audit.json')
    verify_bindings(inherited)
    for source in inherited['sources']:
        entries.setdefault(source['integrated_citation_key'], source)
    records = [
        ('sp19ec_reader', 'Current evaluation and code-generation working reader', reader.BASE/'working-release.json',
         f'Exact{pages}-page reader with791 audited citation records and205 genuine scholarly PDFs; no final acceptance'),
        ('sp19ec_progress', 'Effective current proposal coverage snapshot', BASE/'progress-evidence.json',
         '76open/24inconclusive software cells;95open/3inconclusive reuse decisions;20passing/2inconclusive chapter reviews'),
        ('sp19ec_census','Preserving original-candidate census',reader.BASE/'census-register.json','46 inspected and67 unread of113 originals; only candidates18/20 changed')]
    for key, title, path, claim in records:
        assert key not in entries
        entries[key] = dict(integrated_citation_key=key, kind='project_evidence_not_scholarly_paper',
            title=title, author='Causal banking proposal project', year=2026,
            source_identity=str(path.relative_to(ROOT)), version_date='Preserved artifact inspected19October2026',
            local_copy=ref(path, claim), inspected_anchors=[dict(anchor=claim, inspection='Author inspection')],
            supported_claims=[claim], limitations=['Author project evidence; no independent or bank acceptance.'])
    cited = {k.strip() for group in re.findall(shared.CITE, (BASE/'proposal.md').read_text()) for k in group.split(',')}
    assert cited <= entries.keys(), cited-entries.keys()
    assert {s['integrated_citation_key'] for s in prior['sources']} <= cited
    sources = [entries[k] for k in sorted(cited)]
    assert len(sources) == 76
    audit = dict(sources=sources, cutoff='2026-10-07',
        predecessor_audit=ref(PRIOR/'source-audit.json', 'All70 unchanged prior citation records'),
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
        'program/execution/2026-10-19/sponsor-java-identification-v1/',
        'program/execution/2026-10-19/sponsor-evaluation-code-v1/')
    assert r'\usepackage[numbers,square]{natbib}' in driver
    assert r'\bibliographystyle{unsrt}' in driver
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
        source_audit=ref(BASE/'source-audit.json', '76 source records'),
        manuscript=ref(BASE/'proposal.md', 'Preserving sponsor source'),
        compiled_content=ref(BASE/'proposal.tex', 'Compiled source'),
        bibliography=ref(BASE/'refs.bib', 'Complete bibliography'),
        driver=ref(OUT/(NAME+'.tex'), 'Exact sponsor driver'), builder=ref(Path(__file__), 'Preserving bounded builder'),
        cited_records=76, empty_pages=empty, text_bounds_issues=bad,
        warnings=[line for line in log.splitlines() if 'Warning' in line or 'Underfull' in line],
        visual_acceptance=False, final_proposal_acceptance=False, bank_product_acceptance=False)
    write(BASE/'build-report.json', report)
    print(json.dumps(dict(pages=pages, records=76, pdf=str(MIRROR.relative_to(ROOT)), warnings=report['warnings'])))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['prepare', 'build'])
    {'prepare': prepare, 'build': build}[parser.parse_args().command]()
