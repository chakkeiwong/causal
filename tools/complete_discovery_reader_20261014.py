#!/usr/bin/env python3
"""Prepare/build a preserving successor for the substantive discovery review."""
import argparse
import contextlib
import json
from pathlib import Path
import re

import build_integrated_monograph_v12 as shared
import build_java_reader_20261013 as compiler
import discovery_design_oracles_20261014 as examples
import master_control as core

ROOT = core.ROOT
DOCS = ROOT / 'docs'
BASE = DOCS / 'program/execution/2026-10-14/l4-completion'
OUT = BASE / 'reader'
NAME = 'causal_proposal_discovery_review_2026-10-14'
OLD = DOCS / 'causal_proposal_integrated_2026-10-14.tex'
DRIVER = DOCS / (NAME + '.tex')
PDF = DRIVER.with_suffix('.pdf')
PRIOR = DOCS / 'program/execution/2026-10-14/reader-repair'
PRIOR_AUDIT = PRIOR / 'reader/source-audit.json'
ref = shared.ref


def write(path, value):
    assert not path.exists(), path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def prepare():
    assert not DRIVER.exists() and not (BASE / 'prepared-inputs.json').exists()
    exact = examples.serializable(examples.calculate())
    write(BASE / 'exact-results.json', exact)
    rows = exact['finite_information']['rows']
    table = [r'\begin{table}[htbp]', r'\centering',
             r'\caption{Exact information value under the stipulated two-world intervention law.}',
             r'\label{exec14:l4-evsi-table}', r'\begin{tabular}{rrr}', r'\toprule',
             r'Probes $n$ & Success count triggering an offer & Value of sample information\\', r'\midrule']
    for r in rows:
        threshold = min(r['offer_counts'])
        table.append(f"{r['n']} & ${threshold}$ or more & ${r['EVSI_decimal']:.6f}$" + r'\\')
    table += [r'\bottomrule', r'\end{tabular}', r'\end{table}']
    (BASE / 'evsi-table.tex').write_text('\n'.join(table) + '\n')
    temporal = DOCS / 'program/execution/2026-10-13/llm-census/temporal.tex'
    copied = temporal.read_text().replace(r'\subsection{', r'\section{').replace(r'\subsubsection{', r'\subsection{')
    (BASE / 'temporal-hierarchy.tex').write_text(copied)
    wrapper = DOCS / 'program/comprehensive-v14/work/TEXT.DRAFT.L4/chapter-reviewed.tex'
    assembled = wrapper.read_text().replace(str(temporal.relative_to(DOCS)),
                                            str((BASE / 'temporal-hierarchy.tex').relative_to(DOCS)))
    assembled += '\\input{program/execution/2026-10-14/l4-completion/discovery-alternatives.tex}\n'
    (BASE / 'chapter.tex').write_text(assembled)
    book = OLD.read_text()
    marker = '\\input{' + str(wrapper.relative_to(DOCS)) + '}'
    assert book.count(marker) == 1
    book = book.replace(marker, '\\input{' + str((BASE / 'chapter.tex').relative_to(DOCS)) + '}')
    book, n = re.subn(r'\\bibliography\{([^}]+)\}',
                     lambda m: '\\bibliography{' + m[1] + ',program/execution/2026-10-14/l4-completion/refs}', book)
    assert n == 1
    DRIVER.write_text(book)
    key = 'exec14_discovery_design_oracles'
    (BASE / 'refs.bib').write_text('@misc{' + key + ',\n author={{Causal banking proposal}},\n'
                                 ' title={Exact discovery, restriction-error and experiment-value references},\n'
                                 ' year={2026},\n note={Project derivations, 14 October 2026; no live or bank experiment}\n}\n')
    originals = json.loads(PRIOR_AUDIT.read_text())['sources']
    keys = ['notears2018', 'exec13_pydisc_shimizu2006', 'petersicp2016', 'runge2020']
    reinspected = []
    anchors = {'notears2018': 'PDF pp2-4: objective, stationary-point limitation, Theorem 1 and nonnegative trace-power argument',
               'exec13_pydisc_shimizu2006': 'PDF pp1-3, Section 2: linearity, acyclicity, independent non-Gaussian disturbances and no faithfulness premise',
               'petersicp2016': 'PDF pp3-5, equations (1)-(3), Assumption 1; preserved technical review of Section 3: false-inclusion guarantee is conditional on invariant-set testing',
               'runge2020': 'Preserved primary review: Section 3.2, Assumptions 1 and Theorems 1-2; no new experimental or hidden-variable guarantee'}
    for k in keys:
        s = next(s for s in originals if s['integrated_citation_key'] == k)
        local = s.get('local_path') or s['local_copy']['path']
        reinspected.append({'citation_key': k, 'primary_copy': ref(ROOT / local, anchors[k]),
                            'source_identity': s.get('url', s.get('source_identity', s['title'])),
                            'version_date': s.get('version_status', s.get('version_date')),
                            'inspection': 'Current primary reread' if k != 'runge2020' else 'Preserved inspected claim with unchanged scope'})
    sources = [{'integrated_citation_key': key, 'kind': 'project_derivation',
                'title': 'Exact discovery, restriction-error and experiment-value references',
                'author': 'Causal banking proposal', 'year': 2026,
                'source_identity': 'Project-authored explicit Gaussian and finite binary laws',
                'version_date': '2026-10-14', 'local_copy': ref(BASE / 'exact-results.json', 'Exact covariances, search-depth separation, environment law, all finite outcomes and restriction errors'),
                'inspected_anchors': ['Faithfulness triangle/collider equivalence', 'Minimal separator of size two',
                                      'Identical multi-environment laws', 'At-most-k restriction errors and Markov bound',
                                      'Exhaustive binomial information-value sum at seven fixed sample sizes'],
                'claims': ['All numerical examples follow from stated invented laws and reproduce exactly.',
                           'The probabilistic restriction bound needs genuine marginal error bounds; none is supplied for LLMs.',
                           'Finite information values are planning calculations, not a performed experiment.'],
                'records': [{'local_copy': ref(ROOT / 'tools/discovery_design_oracles_20261014.py', 'Independent equations represented as loadings, matrix conditioning and exact finite sums')},
                            {'local_copy': ref(BASE / 'discovery-alternatives.tex', 'Reviewed assumptions, proofs and banking interpretations')}],
                'limitations': ['No random study, external discovery engine, live model or bank experiment executed.']}]
    write(BASE / 'source-audit.json', {'sources': sources, 'cutoff': '2026-10-07',
                                      'prior': ref(PRIOR_AUDIT, 'Preserved 504 source records'),
                                      'additional_primary_support': reinspected})
    credit = [0.25, 0.75, 1, 0.75, 0.5, 1, 1, 0.25, 1, 0.75, 0.5, 0.75, 0.5, 0.5, 0.5, 0.75, 0.5, 1, 0.5, 0]
    reasons = ['Opening repeats L3 and architecture framing.',
               'Language-only and contamination comparison; shared evaluation framing discounted.',
               'Categorical-response variance and exact rejection probability.',
               'Contrasting priors and statistical prompting; shared constraint framing discounted.',
               'Debate and effect union overlap L3; retain procedure-specific coverage premises.',
               'Temporal-method assumptions and longitudinal distinction.',
               'Active mechanism discovery, empirical denominators and computational comparison.',
               'Interface and generic evaluation repeat integration/evaluation chapters.',
               'Augur and CausalCollab source-specific methods and intervention definition.',
               'Constructed labels and style mixture; shared evaluation design discounted.',
               'Restrictions repeat L3; retain two-world report-law argument.',
               'Coverage/risk bound; graph metrics partly repeat earlier comparisons.',
               'Decision arithmetic overlaps L3 EVPI and uncertainty framing.',
               'Refusal denominators and stateful agents overlap L5/L6; retain new application.',
               'ORCA, protected core and formalization overlap census; retain integrated comparison.',
               'Method-specific full package path; shared software findings discounted.',
               'Gaussian proxy calculation substantially overlaps earlier measurement argument.',
               'Full CI-family count and exact false-rejection scope.',
               'Public evaluation application; generic leakage and cost discussion excluded.',
               'Nearly empty closing page; no credit.']
    write(BASE / 'depth-review-predecessor.json', {
        'operation': 'TEXT.REVIEW.L4', 'status': 'negative',
        'reviewed_reader': ref(OLD.with_suffix('.pdf'), 'Preserved 674-page candidate'),
        'allocation': {'min': 20, 'target': 21, 'max': 22}, 'physical_pages': 20,
        'substantive_page_credit': sum(credit),
        'measurement': 'Author fractional standard-typography page equivalents; overlap and incomplete pages explicitly excluded.',
        'per_page': [{'printed_page': 354+i, 'credit': x, 'rationale': reasons[i]} for i, x in enumerate(credit)],
        'findings': ['Physical span alone does not satisfy the substantive allocation.',
                     'Temporal discussion was a subsection of a conclusion; successor promotes it one level.',
                     'Numerical-method choice, cancellation, search-depth consequences, environment validity and attainable information value need fuller development.'],
        'next_action': 'Develop the missing arguments and review the complete successor, preserving this negative finding.',
        'evidence': [ref(PRIOR / 'reader/build-report.json', 'Exact 20-page physical span'),
                     ref(PRIOR / 'reader/reader.txt', 'Page-by-page text review'),
                     ref(DOCS / 'program/comprehensive-v14/work/TEXT.REVIEW.L3/chapter-review.json', 'Previously credited overlapping L3 material')],
        'visual_acceptance': False})
    generated = [DRIVER, BASE / 'source-audit.json', BASE / 'exact-results.json',
                 BASE / 'depth-review-predecessor.json', BASE / 'refs.bib'] + sorted(BASE.glob('*.tex'))
    write(BASE / 'prepared-inputs.json', {
        'inputs': [ref(OLD, 'Preserved candidate driver'), ref(PRIOR_AUDIT, 'Preserved source custody'),
                   ref(wrapper, 'Earlier L4 wrapper'), ref(temporal, 'Temporal source preserved'),
                   ref(Path(__file__), 'Preparation and compilation'),
                   ref(ROOT / 'tools/discovery_design_oracles_20261014.py', 'Exact references')],
        'generated': [ref(p, 'Prepared preserving input') for p in generated]})
    print(json.dumps({'prepared': str(DRIVER.relative_to(ROOT)), 'prior_credit': sum(credit),
                      'new_manuscript_words': len((BASE / 'discovery-alternatives.tex').read_text().split()),
                      'EVSI': [{'n': r['n'], 'value': r['EVSI_decimal']} for r in rows]}))


def build():
    assert not OUT.exists() and not PDF.exists(), 'Preserve attempted output; use a successor for repairs'
    shared.verify_refs(json.loads((BASE / 'prepared-inputs.json').read_text()))
    for key in ['BASE', 'OUT', 'NAME', 'OLD', 'DRIVER', 'PDF', 'PRIOR_AUDIT']:
        setattr(compiler, key, globals()[key])
    OUT.mkdir()
    with (OUT / 'compile-summary.txt').open('x') as log, contextlib.redirect_stdout(log):
        compiler.build()
    report = json.loads((OUT / 'build-report.json').read_text())
    report.pop('java_comparison', None)
    aux = (OUT / (NAME + '.aux')).read_text()
    def page(label):
        return int(re.search(r'\\newlabel\{' + re.escape(label) + r'\}\{\{[^}]*\}\{(\d+)\}', aux)[1])
    report.update(builder=ref(Path(__file__), 'Preserving discovery development builder'),
                  pdf=ref(PDF, 'Integrated discovery-review working monograph'),
                  predecessor_pdf=ref(OLD.with_suffix('.pdf'), 'Preserved 674-page candidate'),
                  reviewed_l4={'start': page('ch:la03-discovery'), 'end': page('exec14:l4-completion-end'),
                               'physical_span': page('exec14:l4-completion-end') - page('ch:la03-discovery') + 1,
                               'new_argument_start': page('exec14:l4-alternatives'),
                               'allocation': [20, 22], 'substantive_acceptance': False},
                  new_sections={k: page(k) for k in ['exec14:l4-alternatives', 'exec14:l4-faithfulness',
                                                    'exec14:l4-depth-example', 'exec14:l4-environments',
                                                    'exec14:l4-restriction-errors', 'exec14:l4-finite-information']})
    core.write(OUT / 'build-report.json', report)
    print(json.dumps({'pages': report['pages'], 'citations': report['cited_records'],
                      'l4': report['reviewed_l4'], 'warning_count': len(report['warnings'])}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['prepare', 'build'])
    prepare() if parser.parse_args().action == 'prepare' else build()
