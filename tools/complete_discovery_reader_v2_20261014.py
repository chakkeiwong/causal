#!/usr/bin/env python3
"""Preserve the first depth repair and integrate screening/decision distinctions."""
import argparse
import contextlib
import json
from pathlib import Path
import re
import complete_discovery_reader_20261014 as base
import discovery_screening_value_20261014 as exact
import master_control as core

ROOT = core.ROOT
PARENT = base.BASE
BASE = PARENT / 'v2'
OUT = BASE / 'reader'
NAME = 'causal_proposal_discovery_review_v2_2026-10-14'
OLD = base.DRIVER
DRIVER = ROOT / 'docs' / (NAME + '.tex')
PDF = DRIVER.with_suffix('.pdf')
PRIOR_AUDIT = PARENT / 'reader/source-audit.json'
ref, write = base.ref, base.write


def prepare():
    assert not DRIVER.exists() and not BASE.exists()
    BASE.mkdir()
    write(BASE / 'exact-results.json', exact.calculate())
    chapter = '\\input{program/execution/2026-10-14/l4-completion/chapter.tex}\n'
    chapter += '\\input{program/execution/2026-10-14/l4-completion/discovery-screening-value.tex}\n'
    (BASE / 'chapter.tex').write_text(chapter)
    book = OLD.read_text()
    marker = '\\input{program/execution/2026-10-14/l4-completion/chapter.tex}'
    assert book.count(marker) == 1
    book = book.replace(marker, '\\input{program/execution/2026-10-14/l4-completion/v2/chapter.tex}')
    book, n = re.subn(r'\\bibliography\{([^}]+)\}', lambda m: '\\bibliography{' + m[1] + ',program/execution/2026-10-14/l4-completion/v2/refs}', book)
    assert n == 1
    DRIVER.write_text(book)
    key = 'exec14_discovery_screening_value'
    (BASE / 'refs.bib').write_text('@misc{' + key + ',\n author={{Causal banking proposal}},\n'
                                 ' title={Nonlinear screening and information versus decision-value references},\n'
                                 ' year={2026},\n note={Project derivations, 14 October 2026; exact specified laws}\n}\n')
    write(BASE / 'source-audit.json', {'sources': [{
        'integrated_citation_key': key, 'kind': 'project_derivation',
        'title': 'Nonlinear screening and information versus decision-value references',
        'author': 'Causal banking proposal', 'year': 2026,
        'source_identity': 'Project-authored nonlinear Gaussian and finite binary reference problems',
        'version_date': '2026-10-14',
        'local_copy': ref(BASE / 'exact-results.json', 'Gaussian moments, exact posterior decisions and analytic entropy calculations'),
        'inspected_anchors': ['Sign-symmetry proof of zero Spearman correlation despite dependence',
                              'Decision-irrelevant entropy, positive information without action change, and priced accurate query'],
        'claims': ['Correlation screens need not preserve nonlinear causes.',
                   'Query rankings by information and by expected decision utility can differ under a fully specified law.'],
        'records': [{'local_copy': ref(PARENT / 'discovery-screening-value.tex', 'Complete derivations and limitations')},
                    {'local_copy': ref(ROOT / 'tools/discovery_screening_value_20261014.py', 'Exact finite probability and moment reference')}],
        'limitations': ['Analytic authored laws; no package, live model or bank experiment.']}],
        'prior': ref(PRIOR_AUDIT, '505 preserved source records'), 'cutoff': '2026-10-07'})
    write(BASE / 'depth-review-predecessor.json', {
        'status': 'negative', 'operation': 'TEXT.REVIEW.L4',
        'reviewed_reader': ref(OLD.with_suffix('.pdf'), '681-page predecessor retained'),
        'base_credit': 12.75,
        'new_page_credit': [{'printed_page': p, 'credit': c, 'rationale': r} for p, c, r in [
            (373, .5, 'Numerical methods and NOTEARS argument overlap the software/core exposition; credit comparative use in the agent design.'),
            (374, .5, 'Method-assumption and unit-scale selection; exclude repeated package claims and original-method summaries.'),
            (375, 1, 'New triangle/collider equivalence and near-cancellation derivation.'),
            (376, 1, 'Exact search-depth separator and discovery-versus-adjustment consequences.'),
            (377, 1, 'New multi-environment equivalence and structural interpretation of invariance.'),
            (378, 1, 'At-most-k restriction construction, explicit failure and marginal-error bound.'),
            (379, 1, 'Exact finite-sample information experiment and full-outcome decision sum.'),
            (380, .75, 'Numerical information values, transfer and cost interpretation; repeated closing excluded.')]],
        'substantive_page_credit': 19.5, 'minimum_required': 20,
        'findings': ['A second review retains overlap deductions rather than treating 27 physical pages as acceptance.',
                     'Develop nonlinear pre-screen failure and the missing distinction between information gain and decision value.'],
        'evidence': [ref(PARENT / 'depth-review-predecessor.json', 'Base fractional review'),
                     ref(PARENT / 'reader/reader.txt', 'Exact second-candidate pages'),
                     ref(PARENT / 'reader/build-report.json', '27-page physical span')],
        'visual_acceptance': False})
    write(BASE / 'prepared-inputs.json', {
        'inputs': [ref(OLD, 'Preserved 681-page driver'), ref(PRIOR_AUDIT, 'Preserved source records'),
                   ref(Path(__file__), 'Successor preparation/build'),
                   ref(ROOT / 'tools/discovery_screening_value_20261014.py', 'Exact calculator'),
                   ref(PARENT / 'discovery-screening-value.tex', 'Additional substantive arguments')],
        'generated': [ref(p, 'Prepared successor input') for p in [DRIVER, BASE / 'chapter.tex', BASE / 'refs.bib',
                                                               BASE / 'source-audit.json', BASE / 'exact-results.json',
                                                               BASE / 'depth-review-predecessor.json']]})
    print(json.dumps({'prepared': str(DRIVER.relative_to(ROOT)), 'earlier_substantive_credit': 19.5}))


def build():
    for key in ['BASE', 'OUT', 'NAME', 'OLD', 'DRIVER', 'PDF', 'PRIOR_AUDIT']:
        setattr(base, key, globals()[key])
    with (BASE / 'build-summary.txt').open('x') as log, contextlib.redirect_stdout(log):
        base.build()
    report = json.loads((OUT / 'build-report.json').read_text())
    aux = (OUT / (NAME + '.aux')).read_text()
    def page(label):
        return int(re.search(r'\\newlabel\{' + re.escape(label) + r'\}\{\{[^}]*\}\{(\d+)\}', aux)[1])
    report['reviewed_l4'].update(end=page('exec14:l4-final-end'),
                                 physical_span=page('exec14:l4-final-end') - page('ch:la03-discovery') + 1)
    report['new_sections'].update({k: page(k) for k in ['exec14:l4-nonlinear-screen', 'exec14:l4-information-objective']})
    report.update(builder=ref(Path(__file__), 'Preserving substantive discovery successor'),
                  predecessor_pdf=ref(OLD.with_suffix('.pdf'), '681-page predecessor'),
                  pdf=ref(PDF, 'Current integrated working monograph'))
    core.write(OUT / 'build-report.json', report)
    print(json.dumps({'pages': report['pages'], 'citations': report['cited_records'],
                      'l4': report['reviewed_l4'],
                      'warnings_except_underfull': [w for w in report['warnings'] if 'Underfull' not in w]}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['prepare', 'build'])
    prepare() if parser.parse_args().action == 'prepare' else build()
