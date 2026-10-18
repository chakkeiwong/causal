#!/usr/bin/env python3
"""Preserve the prior sponsor and pair a reviewed successor to the actual reader."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET

import build_graph_panel_reader_v2_20261018 as reader
import build_integrated_monograph_v12 as shared
import run_program_reviews_v2 as extension
import sponsor_economics_20261013 as economics
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run = extension.base
core = run.core
ROOT = reader.ROOT
DOCS = ROOT/'docs'
BASE = DOCS/'program/execution/2026-10-18/sponsor-graph-panel-v1'
OUT = BASE/'reader'
PRIOR = DOCS/'program/execution/2026-10-18/sponsor-framework-v1'
NAME = 'sponsor-proposal'
MIRROR = DOCS/'sponsor_proposal_graph_panels_reviewed_2026-10-18.pdf'


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
    assert groups['software_cells'] == {'pass': 2, 'inconclusive': 22, 'open': 78, 'total': 102}
    assert groups['reuse_decisions'] == {'pass': 16, 'inconclusive': 3, 'open': 96, 'total': 115}
    assert groups['chapter_reviews'] == {'pass': 20, 'inconclusive': 2, 'open': 0, 'total': 22}
    return dict(scope='Exact current-reader proposal snapshot; counts from effective canonical receipts',
        reader=dict(state['reader']), **groups,
        census=ref(reader.PREDECESSOR/'census-register.json', '42 inspected/71 unread out of113'),
        evidence=bindings, mandatory_repairs_closed=[], final_acceptance=False)


def manuscript(pages):
    text = (PRIOR/'proposal.md').read_text()
    replacements = {
        '1,068 pages and 763 audited citation records, including 201 genuine scholarly PDFs':
            f'{pages:,} pages and 772 audited citation records, including 201 genuine scholarly PDFs',
        '79 open and 21 inconclusive cells': '78 open and 22 inconclusive cells',
        '97 open and three inconclusive decisions': '96 open and three inconclusive decisions',
        'sp18f_reader': 'sp18gp_reader', 'sp18f_progress': 'sp18gp_progress',
        'uninspected panel, synthetic-control, transport and latent-discovery scope':
            'unresolved additional panel vendors, synthetic-control, transport and latent-discovery scope',
    }
    for old, new in replacements.items():
        assert old in text, old
        text = text.replace(old, new)
    marker = '## The reusable product and its customer'
    historical = ('The preceding R/framework brief and its exact-reader coverage snapshot '
        'remain the preserved baseline for the following graph and panel additions. '
        '\\citep{sp18f_reader,sp18f_progress}\n\n')
    assert text.count(marker) == 1
    text = text.replace(marker, historical+marker)
    marker = '# Public evidence before expensive bank experiments'
    addition = r'''## Graph adjustment and staggered panel comparisons

A pinned DAGitty R-wrapper is now a scoped reference-reuse choice for a supplied
observed DAG and one total-effect adjustment query. Invalid questions, a valid
empty covariate set, no returned adjustment set and an incomplete capped search
need different result types. Failure of adjustment need not imply failure of
all identification methods. The inspected wrapper and JavaScript entry point
also differ when exposure or outcome is omitted. A future adapter must validate
the question before interpreting a Boolean. This remains a source-reviewed
proposal: no R, Node, browser or upstream test was executed. The selected
components have distinct GPL/MIT declarations, and the dependency resolution
and intended distribution still need a complete rights review.
\citep{exec18_gp_dagitty}

Exact authored repayment laws show why preserving the graph is consequential.
One gives an adjusted effect of one quarter versus an unadjusted five sixteenths;
a second introduces a spurious negative contrast by conditioning on documentation
completion, a collider; and a third changes the total-effect target by adjusting
for subsequent engagement. These are stipulated structural examples, not
DAGitty trial results or empirical bank effects. They provide concrete positive
and negative references for a proposed conversion test.
\citep{exec18_gp_graph_reference}

The commercial panel comparison now has four inspected Stata manuals and an
EViews introduction. Stata distinguishes scalar DID from heterogeneous
cohort-time effects, repeated cross-sections from panels, never-treated from
not-yet-treated controls, and alternative base periods and aggregation weights.
Its inspected postestimation restrictions also make interval and aggregation
options estimator-specific. The EViews introduction is a narrower capability
lead. These public snapshots do not establish licensed edition parity, precise
cutoff-era bytes or executable compatibility; SAS, SPSS, MATLAB and additional
commercial frontends remain unresolved for this specific comparison.
\citep{exec18_gp_stata_did,exec18_gp_stata_hdid,exec18_gp_stata_xthdid,
exec18_gp_stata_post,exec18_gp_eviews}

An exact five-branch, three-date rollout makes the target distinction concrete.
All stipulated treatment effects are positive and the treated-period average
is USD 34,000, but the scalar two-way fixed-effects projection is minus
USD 11,375 because one cohort-time effect receives negative weight. Separate
rational calculations reproduce both quantities. Exact preperiod equality also
fails to identify an untreated postperiod shock. No commercial engine,
confidence-coverage study or bank rollout was executed. The saved dependent-panel
request to the local common dispatcher returned unsupported; other panel
research code is not ruled out. Build a declared cohort-time request with cells,
weights and compatible inference options before proposing a matched licensed
comparison. \citep{exec18_gp_panel_reference,exec18_gp_dispatch}

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
            ref(PRIOR/'source-audit.json', 'Preserved34 citation identities'),
            ref(reader.BASE/'working-release.json', 'Actual paired working monograph'),
            ref(BASE/'proposal.md', 'Reconciled source'), ref(BASE/'progress-evidence.json', 'Effective receipt counts')],
        checks=['Preserve all prior citation records, negative findings, funding/servicing discussion and exact economic section.',
                'Update only current reader/coverage claims and bounded DAGitty/panel findings; retain R/framework treatment.',
                'Source, compilation, text and arithmetic checks cannot award rendered acceptance.']))
    prior = read(PRIOR/'source-audit.json')
    verify_bindings(prior)
    entries = {s['integrated_citation_key']: s for s in prior['sources']}
    inherited = read(reader.OUT/'source-audit.json')
    verify_bindings(inherited)
    for source in inherited['sources']:
        entries.setdefault(source['integrated_citation_key'], source)
    records = [
        ('sp18gp_reader', 'Current graph and panel working reader', reader.BASE/'working-release.json',
         f'Exact{pages}-page reader with772 audited citation records and201 genuine scholarly PDFs; no final acceptance'),
        ('sp18gp_progress', 'Effective current proposal coverage snapshot', BASE/'progress-evidence.json',
         '78open/22inconclusive software cells;96open/3inconclusive reuse decisions;20passing/2inconclusive chapter reviews')]
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
    assert len(sources) == 45
    audit = dict(sources=sources, cutoff='2026-10-07',
        predecessor_audit=ref(PRIOR/'source-audit.json', 'All34 unchanged prior citation records'),
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
        'program/execution/2026-10-18/sponsor-framework-v1/', 'program/execution/2026-10-18/sponsor-graph-panel-v1/')
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
        source_audit=ref(BASE/'source-audit.json', '45 source records'),
        manuscript=ref(BASE/'proposal.md', 'Preserving sponsor source'),
        compiled_content=ref(BASE/'proposal.tex', 'Compiled source'),
        bibliography=ref(BASE/'refs.bib', 'Complete bibliography'),
        driver=ref(OUT/(NAME+'.tex'), 'Exact sponsor driver'), builder=ref(Path(__file__), 'Preserving bounded builder'),
        cited_records=45, empty_pages=empty, text_bounds_issues=bad,
        warnings=[line for line in log.splitlines() if 'Warning' in line or 'Underfull' in line],
        visual_acceptance=False, final_proposal_acceptance=False, bank_product_acceptance=False)
    write(BASE/'build-report.json', report)
    print(json.dumps(dict(pages=pages, records=45, pdf=str(MIRROR.relative_to(ROOT)), warnings=report['warnings'])))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['prepare', 'build'])
    {'prepare': prepare, 'build': build}[parser.parse_args().command]()
