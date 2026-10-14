#!/usr/bin/env python3
"""Record the substantive L5 review and preserve exact-reader continuity."""
import argparse
import json
from pathlib import Path
import re

import complete_l5_depth_20261014 as work
import master_control as core
import publish_longitudinal_workflow_reader_20261014 as predecessor
import run_program as run
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

ROOT = core.ROOT
BASE = work.BASE
OUT = work.OUT
REVIEWER = {'name': 'Codex author/coordinator', 'kind': 'author'}
LIMITS = [
    'Author content/source/depth review; no independent scientific or bank acceptance.',
    'The fixed-nuisance bias calculation is a restricted project identity, not a general SDR theorem or fitted coverage study.',
    'The conditional panel and monetary values use stipulated truth and costs, not bank observations or measured ROI.',
    'Known-law planning arithmetic does not select a trial size or establish achieved precision.',
    'No upstream longitudinal/panel estimator, live model or bank experiment was executed by this addition.',
    'L5 allocation passes; whole MR01/MR02/MR03 coverage and proposal Q1 remain open.',
    'Rendered review requires a fresh session under the exhausted six-preview allowance in /home/ubuntu/AGENTS.md; Q5 remains open.',
]
REVIEW = ROOT / 'docs/program/comprehensive-v14/work/TEXT.REVIEW.L5/chapter-review.json'


def review():
    report = json.loads((OUT / 'build-report.json').read_text())
    audit = json.loads((OUT / 'source-audit.json').read_text())
    prior = json.loads(work.PRIOR.read_text())
    index = json.loads((BASE / 'traceability-review.json').read_text())
    previous_index = json.loads((predecessor.BASE / 'traceability-review.json').read_text())
    prepared = json.loads((BASE / 'prepared-inputs.json').read_text())
    for item in [report, audit, prior, index, prepared]:
        verify_bindings(item)
    assert index['status'] == 'pass' and index['issues'] == []
    assert index['scholarly_pdfs'] == 153
    assert json.loads((OUT / 'text-layout-review.json').read_text())['status'] == 'pass'
    assert not [w for w in report['warnings'] if 'Underfull' not in w]
    old = {s['integrated_citation_key']: s for s in prior['sources']}
    current = {s['integrated_citation_key']: s for s in audit['sources']}
    assert len(old) == 515 and len(current) == 516
    assert all(current[k] == v for k, v in old.items())
    assert set(current) - set(old) == {'exec14_workflow_remainder'}
    files = {r['path']: r for r in audit['tex_files']}
    inherited = [r for r in prior['tex_files'] if r['path'] != str(work.OLD.relative_to(ROOT))]
    assert all(files[r['path']]['sha256'] == r['sha256'] for r in inherited)
    old_contexts = {r['citation_key']: r for r in previous_index['records']}
    new_contexts = {r['citation_key']: r for r in index['records']}
    changed = [k for k, r in old_contexts.items()
               if r['citation_contexts'] != new_contexts[k]['citation_contexts']]
    assert set(changed) == {'sequentialdr2018', 'callaway2021'}
    oracle = work.calculate()
    assert oracle == json.loads((BASE / 'exact-oracle.json').read_text())
    text = re.sub(r'\s+', ' ', (OUT / 'reader.txt').read_text())
    for phrase in ['How estimated components can change a sequential value',
                   'Conditional panel comparisons must preserve cohort composition',
                   '92.8', '4007', 'not a claimed achieved confidence interval']:
        assert phrase in text, phrase
    evidence = [ref(p, anchor) for p, anchor in [
        (OUT / 'build-report.json', 'Exact 702-page candidate and PDF hash'),
        (OUT / 'source-audit.json', '516 source records and compiled chapter identities'),
        (OUT / 'reader.txt', 'Inspected physical pages 427–430; printed 409–412'),
        (OUT / 'text-layout-review.json', 'All-page text and physical bounds; not visual acceptance'),
        (BASE / 'traceability-review.json', 'Complete citation contexts and 153 genuine scholarly PDFs'),
        (BASE / 'prepared-inputs.json', 'Preserved inputs and derivation identities'),
        (BASE / 'depth-review-predecessor.json', 'Preserved 8.5-page depth shortfall'),
        (BASE / 'plan-review.json', 'Reviewed derivation and composition repair'),
        (BASE / 'exact-oracle.json', 'Independent enumeration, exact algebra and planning arithmetic'),
        (work.ADDITION, 'Two connected substantive additions'),
        (predecessor.BASE / 'release-source-review.json', 'Preserved core coverage and mathematics review'),
        (ROOT / 'docs/program/execution/2026-10-14/l5-workflow/primary-review.json',
         'Primary longitudinal, panel and observation anchors'),
        (Path(__file__), 'Immutable review and publication procedure'),
    ]]
    findings = [
        'Fixed-component conditioning and independent observational enumeration agree on the exact bias identity; the example gives bias −2 and augmented mean 92.8 rather than 94.8.',
        'Correct assignment probabilities at both stages or correct outcome components at both stages restore 94.8. Neither a point-treatment loop nor sample splitting supplies the missing general theorem or rates.',
        'The Cauchy–Schwarz diagnostic and known-law planning size 4007 are conditional mathematical constructions. Increasing sample size does not remove the fixed bias.',
        'Conditional ATT 7 differs from pooled DiD 11. Standardization and cohort-odds weighting both yield control change 8; missing support changes the admissible target.',
        'The stipulated cost 6 leaves margin 1, while the naive contrast suggests 5; scientific targets precede investment interpretation.',
        'Reread Luedtke Definitions 1–3 (saved text lines 185–235) and Callaway/Sant’Anna Assumptions 3–6 (320–405); inherited primary representations remain bound. New numeric statements are explicitly project derivations.',
        'All 515 preceding source records and inherited chapter bytes are preserved; only two existing citation keys acquire new contexts.',
    ]
    write(BASE / 'release-source-review.json', {
        'status': 'pass', 'issues': [], 'reviewer': REVIEWER,
        'scope': 'Exact-reader L5 source, derivation, banking and nonduplicate-depth review',
        'reviewed_reader': report['pdf'], 'findings': findings, 'evidence': evidence,
        'unchanged_source_records': 515, 'new_source_records': ['exec14_workflow_remainder'],
        'changed_existing_context_keys': changed,
        'unchanged_inherited_compiled_sources': len(inherited),
        'limits': LIMITS, 'visual_acceptance': False, 'bank_ROI_established': False,
    })
    initial = json.loads((BASE / 'depth-review-predecessor.json').read_text())
    per_page = [dict(r) for r in initial['per_page']]
    assert sum(p['credit'] for p in per_page) == 8.5
    per_page[-1]['credit'] = .75
    per_page[-1]['rationale'] += ' New error-ratio setup adds only 0.25 credit.'
    per_page.extend([
        {'printed_page': 410, 'credit': 1, 'rationale': 'New exact remainder, counterexample, error-product bound and conditional inference obligations.'},
        {'printed_page': 411, 'credit': 1, 'rationale': 'New conditional panel composition, target, standardization and weighted representation.'},
        {'printed_page': 412, 'credit': .25, 'rationale': 'Partial page: missing-support target change and monetary consequence. Architecture continuation excluded.'},
    ])
    credit = sum(p['credit'] for p in per_page)
    assert credit == 11 and 10 <= credit <= 12
    write(REVIEW, {
        'operation_id': 'TEXT.REVIEW.L5', 'status': 'pass', 'reviewer': REVIEWER,
        'scope': 'L5 identification/estimation/longitudinal/panel/observation pathways in the exact 702-page working candidate',
        'allocated_title': 'Agents across identification, estimation and longitudinal decisions',
        'allocation': {'min': 10, 'target': 11, 'max': 12},
        'physical_span': {'first_printed_page': 396, 'last_printed_page': 425,
                          'first_pdf_page': 414, 'last_pdf_page': 443, 'pages': 30},
        'substantive_page_credit': credit,
        'measurement': 'Conservative fractional standard-typography page equivalents from source and extracted pages; physical chapter span does not determine credit.',
        'per_page': per_page,
        'excluded': 'Architecture/data/code/validation continuation on printed 412–425; excluded from L5. Generic framework, permission, recovery and repeated framing are also discounted.',
        'double_counting': 'Credit belongs only to L5; no software, adjacent LLM or integration page credit is inferred.',
        'allocation_exception': None, 'reviewed_reader': report['pdf'],
        'findings': findings,
        'subject_coverage': ['Business target and history translation; identification and estimator handoff',
            'Fixed sequential policies, feedback, retention, recursive scores and nuisance-error diagnostics',
            'Panel adoption targets, heterogeneous comparisons, composition, overlap and counterfactual ambiguity',
            'Observation frames, label inversion, dependence and uncertainty limitations',
            'Assistant roles, restricted ltmle interface reuse and matched analyst alternatives'],
        'evidence': evidence + [ref(BASE / 'release-source-review.json', 'Actual exact-reader semantic delta review')],
        'limitations': LIMITS, 'visual_acceptance': False, 'original_gap_qualification': False,
    })
    print(json.dumps({'review': 'pass', 'substantive_pages': credit, 'sources': 516,
                      'pages': report['pages'], 'visual_acceptance': False}))


def record_review():
    reviewed = json.loads(REVIEW.read_text())
    verify_bindings(reviewed)
    state = core.read(ROOT, core.STATE)
    assert state['execution_runtime']['active']['operation'] == 'TEXT.REVIEW.L5'
    graph, _, _ = run.combined(ROOT, state)
    node = run.ledger.operation(graph, 'TEXT.REVIEW.L5')
    receipt = run.ledger.receipt_template(node)
    evidence = [ref(REVIEW, 'Actual chapter content and depth review'),
                ref(BASE / 'release-source-review.json', 'Exact source/mathematics delta')]
    facts = ['Allocated longitudinal/panel/observation pathways and matched alternatives are developed; exact references and primary-source contexts have been inspected.',
             'Conservative review credits 11 substantive pages against allocation 10/11/12, excluding repetition and adjacent architecture/data/code material.']
    receipt.update(outcome='pass', execution='performed', scope=reviewed['scope'],
                   reviewer=REVIEWER, limitations=LIMITS, outputs=[ref(REVIEW, 'Reviewed L5 allocation')],
                   nonexecution_reason='', revisit_trigger='',
                   criteria=[{'index': i, 'verdict': 'pass', 'finding': fact, 'evidence': evidence}
                             for i, fact in enumerate(facts)])
    write(BASE / 'operation-receipt.json', receipt)
    transition('record', 'TEXT.REVIEW.L5', BASE / 'operation-receipt.json')


def publish():
    state = core.read(ROOT, core.STATE)
    before = core.sha(ROOT / core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path'] == str(work.OLD.with_suffix('.pdf').relative_to(ROOT))
    assert 'TEXT.REVIEW.L5' in state['execution_program']['results']
    report = json.loads((OUT / 'build-report.json').read_text())
    audit = json.loads((OUT / 'source-audit.json').read_text())
    review = json.loads((BASE / 'release-source-review.json').read_text())
    verify_bindings(review)
    manifest = {'kind': 'working_monograph', 'final_acceptance': False,
        'pdf': report['pdf'], 'pages': report['pages'],
        'supersedes': {k: state['reader'][k] for k in ['path', 'sha256']},
        'build_report': ref(OUT / 'build-report.json', '702-page preserving L5 successor'),
        'source_review': ref(BASE / 'release-source-review.json', 'Reviewed source/mathematics/depth delta'),
        'text_layout': ref(OUT / 'text-layout-review.json', 'All-page text/bounds review'),
        'source_artifacts': audit['tex_files'] + review['evidence'] + [ref(REVIEW, 'L5 depth receipt')],
        'visual_acceptance': False, 'mandatory_repairs_closed': [],
        'changes': ['Derive sequential nuisance-error bias and diagnostic products.',
                    'Develop conditional panel composition, supported target and monetary consequence.',
                    'Meet L5 allocation with 11 nonduplicate substantive pages.'],
        'sponsor_binding': 'Preserved sponsor baseline; Q5 reconciliation remains open.'}
    write(BASE / 'working-release.json', manifest)
    binding = ref(BASE / 'working-release.json', 'Reviewed longitudinal depth successor')
    run.ledger.validate_working_release(ROOT, binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader'] = {k: report['pdf'][k] for k in ['path', 'sha256']}
    state['reader'].update(pages=report['pages'], status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT, before, state, {'action': 'publish_l5_depth_successor',
                                   'manifest': binding, 'final_acceptance': False})
    print(json.dumps({'published': state['reader'], 'proposal_accepted': False}))


def renew():
    # Reuse the previously inspected exact-reader transition contract. Its
    # source bytes and historical receipts remain unchanged.
    predecessor.BASE = BASE
    predecessor.OUT = OUT
    predecessor.LIMITS = LIMITS
    predecessor.renew()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['review', 'record', 'publish', 'renew'])
    args = parser.parse_args()
    {'review': review, 'record': record_review, 'publish': publish, 'renew': renew}[args.command]()
