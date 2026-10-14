#!/usr/bin/env python3
"""Preserve the 596-page monograph and integrate the funded decision example."""
import argparse
import json
import math
from pathlib import Path
import re

import build_integrated_monograph_v12 as shared
import build_java_reader_20261013 as inherited
import master_control as core

ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-13/funding-journey'
OUT = BASE / 'reader'
NAME = 'causal_proposal_funding_2026-10-13'
OLD = ROOT / 'docs/causal_proposal_other_discovery_2026-10-13.tex'
DRIVER = ROOT / 'docs' / (NAME+'.tex')
PDF = DRIVER.with_suffix('.pdf')
PRIOR_AUDIT = ROOT / 'docs/program/execution/2026-10-13/other-discovery/reader/source-audit.json'
ref = shared.ref


def configure():
    for key in ['BASE', 'OUT', 'NAME', 'OLD', 'DRIVER', 'PDF', 'PRIOR_AUDIT']:
        setattr(inherited, key, globals()[key])


def expected_driver():
    book = OLD.read_text()
    marker = r'\input{program/execution/2026-10-13/discovery-journey/section.tex}'
    assert book.count(marker) == 1
    book = book.replace(marker, marker+'\n'+r'\input{program/execution/2026-10-13/funding-journey/section.tex}', 1)
    marker = 'program/execution/2026-10-13/other-discovery/reader-input/refs}'
    assert book.count(marker) == 1
    return book.replace(marker, 'program/execution/2026-10-13/other-discovery/reader-input/refs,program/execution/2026-10-13/funding-journey/refs}', 1)


def prepare():
    configure(); inherited.guard()
    assert not (BASE / 'source-audit.json').exists(), 'Preserve prior audit'
    review = json.loads((BASE / 'local-review.json').read_text())
    assert review['status'] == 'pass' and review['matching_slots'] == 118 and review['failed_harness_launches'] == 2
    shared.verify_refs(review)
    law = {'law': 'Known Gaussian independent nuisance example from exact-examples.json',
           'correct_known_variance_coverage': math.erf(2/math.sqrt(2)),
           'omitted_nuisance_coverage': math.erf(2/(3*math.sqrt(2))),
           'weak_ray_profit_image_USD': [[None, -10750], [-3250, None]],
           'derivation': 'Standardize N(0,9/n) at half-width 2/sqrt(n), giving critical 2/3. Profit is the increasing affine map 3750*beta-7000.',
           'claims': 'Exact toy-law probabilities, not Monte Carlo or empirical package coverage; scenario financial image only.'}
    assert round(law['correct_known_variance_coverage'], 5) == .95450
    assert round(law['omitted_nuisance_coverage'], 5) == .49501
    core.write(BASE / 'supplementary-mathematical-review.json', law)
    def source(key, title, kind, records, claims, limits):
        local = [ref(ROOT / p, anchor) for p, anchor in records]
        return {'id': key, 'integrated_citation_key': key, 'kind': kind, 'title': title,
                'author': 'Causal banking research project', 'authors': ['Causal banking research project'],
                'year': 2026, 'version_date': '13 October 2026; project evidence after the literature cutoff, explicitly dated',
                'source_identity': 'Local project construction, inspected source and frozen amended execution',
                'local_records': local, 'inspected_anchors': [x['anchor'] for x in local],
                'supported_claims': claims, 'limits': limits}
    rel = str(BASE.relative_to(ROOT))+'/'
    sources = [
        source('exec13_funding_exact', 'Funding decision: exact nuisance, identity, inclusion and profit examples',
               'project_derivation_and_exact_examples', [
                   (rel+'exact-examples.json', 'Independent Gaussian nuisance variance nine versus one; four inclusion states and financial endpoints'),
                   (rel+'supplementary-mathematical-review.json', 'Analytic 0.95450 versus 0.49501 Gaussian coverage and affine images of weak rays'),
                   ('tools/funding_examples_20261013.py', 'Exact rational calculations; no fitted bank data'),
                   (rel+'plan-review.md', 'Model, target units, population, decision and cost assumptions')],
               ['The specified independent Gaussian estimator has variance 9/n; omitting nuisance contributes only 1/n.',
                'Truth-known household mean and expected HT estimate are three; record and selected-sample means differ.',
                'Under the authored profit function, the two supplied intervals map to [125,875] and [-625,1625] USD.'],
               ['No arbitrary learner/dependence theorem, observed individual treatment effects, measured prices or bank ROI.']),
        source('exec13_funding_runtime', 'Funding workflow: amended local library and CLI boundary execution',
               'project_executed_examples', [
                   (rel+'local-review.json', '118 fixed slots, 29 parity comparisons, 451 independent rational checks, two retained failed launches'),
                   (rel+'local-journal.json', 'Every exact request and response, preserved prefixes, timing and replay'),
                   (rel+'launch-amendment.json', 'Import correction recorded before any final service call'),
                   (rel+'completion-amendment.json', 'Copied fixture-selector correction recorded before final two checks'),
                   ('docs/program/comprehensive-v14/work/IN.JOURNEY.DESIGN.funding/workflow-protocol.json', 'Initial prospective protocol and fixed expectations'),
                   ('docs/program/comprehensive-v14/work/IN.JOURNEY.LOCAL.funding/local-results.json', 'Final service-slot results and measurement scope'),
                   ('tools/funding_journey_20261013.py', 'Frozen original runner, including both retained harness defects'),
                   ('tools/funding_journey_successor_20261013.py', 'Preserved completion executable with two reviewed source changes'),
                   ('tools/review_funding_journey_20261013.py', 'Independent roots, membership, all-request and amendment review')],
               ['All 118 slots and 29 parity comparisons matched after two disclosed harness repairs; original unamended execution failed.',
                'The 48 computed outputs include diagnostics and uninformative effect sets; 40 input failures, eight refusals, twenty unsupported operations and two conflicts remain.',
                'Invocation times sum to approximately 56.46 seconds under the declared scope.'],
               ['No empirical coverage, global reliability, complete workflow cost, MCP requalification or actual sibling/bank result.']),
        source('exec13_funding_service', 'Local reference funding service and scientific-context boundaries',
               'project_software_source', [
                   ('src/causalbank/operation_service_v12.py', '_estimate uses supplied Gaussian moment inversion; _audit checks strict feature clocks only; contradicted premises refused'),
                   ('src/causalbank/responses.py', 'quadratic_sublevel and moment_test_sets; shared denominator and Bonferroni critical'),
                   ('src/causalbank/operation_contract_v12.py', 'validate_context, validate_set and validate_response preserve declared meanings'),
                   ('src/causalbank/runtime_v12.py', 'Runtime artifact custody and idempotency conflict logic'),
                   (rel+'fixtures.json', 'Unknown identity/inclusion cases and supported versus unsupported methods')],
               ['Supplied-covariance inversion retains exact interval topology and conditional qualifications.',
                'Unverified identity/inclusion and sampling labels are not automatically validated; the proposed decision prerequisite layer remains separate.',
                'The two-outcome construction uses a Bonferroni rectangle at the expressly chosen nominal level.'],
               ['Inspected source and bounded execution do not qualify general statistical, financial or platform behavior.'])]
    audit = {'cutoff': '2026-10-07', 'project_evidence_date': '2026-10-13', 'sources': sources,
             'scholarly_originals_added': 0, 'visual_acceptance': False}
    shared.verify_refs(audit)
    core.write(BASE / 'source-audit.json', audit)
    author = {'status': 'pass', 'issues': [], 'reviewer': {'name': 'Codex author', 'kind': 'author'},
              'scope': 'New funding narrative, derivations, proposal implications and amended local results',
              'findings': ['Target is twelve-month average balance; quote normalization and local linearity are separate premises.',
                           'Feature clocks are distinguished from future-outcome follow-up.',
                           'All law, cost and truth assumptions are explicit; Gaussian coverage statements concern only the exact independent toy law.',
                           'The full 118-slot denominator and two harness failures are disclosed; original unamended completion is not claimed.',
                           'Consumer, owner, MCP, arbitrary learner and bank claims remain excluded from demonstrated scope.'],
              'evidence': [ref(BASE / n, n) for n in ['section.tex', 'source-audit.json', 'local-review.json', 'exact-examples.json',
                           'supplementary-mathematical-review.json', 'plan-review.md']],
              'visual_acceptance': False, 'independent_review': False}
    core.write(BASE / 'manuscript-review.json', author)
    DRIVER.write_text(expected_driver())
    (BASE / 'refs.bib').write_text('\n'.join('@misc{'+s['integrated_citation_key']+',\n author={{'+shared.escape(s['author'])
        +'}},\n title={'+shared.escape(s['title'])+'},\n year={2026},\n note={'+shared.escape(s['version_date'])+'}\n}\n' for s in sources))
    core.write(BASE / 'prepared-inputs.json', {
        'inputs': [ref(p, 'Reviewed preserving input') for p in [OLD, PRIOR_AUDIT, BASE / 'section.tex', BASE / 'source-audit.json',
                   BASE / 'manuscript-review.json', Path(__file__)]],
        'generated': [ref(DRIVER, 'Preserving funding driver'), ref(BASE / 'refs.bib', 'Project source identities')]})
    print(json.dumps({'prepared': str(DRIVER.relative_to(ROOT)), 'new_sources': len(sources)}))


def build():
    configure(); OUT.mkdir(exist_ok=True)
    for suffix in ['.aux', '.bbl', '.toc', '.out']:
        p = OUT / (NAME+suffix)
        if not p.exists(): p.write_text('')
    inherited.build()
    audit = json.loads((OUT / 'source-audit.json').read_text())
    audit['added_bibliography'] = ref(BASE / 'refs.bib', 'Funding example, execution and local-source identities')
    core.write(OUT / 'source-audit.json', audit)
    report = json.loads((OUT / 'build-report.json').read_text()); report.pop('java_comparison', None)
    aux = (OUT / (NAME+'.aux')).read_text()
    def page(label):
        return int(re.search(r'\\newlabel\{'+re.escape(label)+r'\}\{\{[^}]*\}\{(\d+)\}', aux).group(1))
    report.update(builder=ref(Path(__file__), 'Funding preserving integration builder'),
        compile_routine=ref(ROOT / 'tools/build_java_reader_20261013.py', 'Unchanged bounded compiler'),
        pdf=ref(PDF, 'Working monograph with complete funding decision journey'),
        predecessor_pdf=ref(OLD.with_suffix('.pdf'), 'Preserved 596-page predecessor'),
        source_audit=ref(OUT / 'source-audit.json', 'Whole-reader source identities'),
        funding_journey={'first_printed_page': page('exec13:funding-journey'), 'last_printed_page': page('exec13:funding-journey-end'),
                         'service_slots': 118, 'failed_harness_launches': 2, 'financial_qualification': False})
    core.write(OUT / 'build-report.json', report)
    print(json.dumps({k: report[k] for k in ['pages', 'cited_records', 'funding_journey']}))


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('command', choices=['prepare', 'build']); args = p.parse_args()
    prepare() if args.command == 'prepare' else build()
