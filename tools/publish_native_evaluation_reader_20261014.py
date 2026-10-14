#!/usr/bin/env python3
"""Review and publish the preserving native/reuse/evaluation working reader."""
import argparse
import json
from pathlib import Path
import re

import build_native_evaluation_reader_v3_20261014 as build
import master_control as core
import review_causalml_reuse_20261014 as causalml
import review_cxx_latent_20261014 as native
import review_evaluation_cost_20261014 as evaluation
import run_program as run
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

ROOT = core.ROOT
BASE = build.BASE
OUT = build.OUT
REVIEWER = {'name': 'Codex author/coordinator', 'kind': 'author'}
LIMITS = [
    'Author content/source delta review; no independent scientific acceptance.',
    'Whole-manuscript coverage/depth, all mandatory repairs and proposal Q1 remain open.',
    'Native source coverage is inconclusive; MIIC convention and methodological originals remain unresolved.',
    'No upstream engine, live model evaluation or bank experiment was executed by this publication.',
    'Project examples and prices are stipulated; no measured bank ROI or provider price is established.',
    'Rendered visual acceptance remains pending: the inherited six-preview allowance is exhausted under /home/ubuntu/AGENTS.md.',
    'Sponsor reconciliation and Q5 exact-release acceptance remain open.',
]


def review():
    assert not (BASE / 'release-source-review.json').exists()
    report = json.loads((OUT / 'build-report.json').read_text())
    audit = json.loads((OUT / 'source-audit.json').read_text())
    prior = json.loads(build.PRIOR_AUDIT.read_text())
    index = json.loads((BASE / 'traceability-review.json').read_text())
    for obj in [report, audit, prior, index,
                json.loads((BASE / 'prepared-inputs.json').read_text())]:
        verify_bindings(obj)
    assert report['pages'] == 692 and report['cited_records'] == 514
    assert index['status'] == 'pass' and not index['issues']
    assert json.loads((OUT / 'text-layout-review.json').read_text())['status'] == 'pass'
    assert not [w for w in report['warnings'] if 'Underfull' not in w]
    previous = {s['integrated_citation_key']: s for s in prior['sources']}
    current = {s['integrated_citation_key']: s for s in audit['sources']}
    assert len(previous) == 506 and len(current) == 514
    assert all(current[k] == v for k, v in previous.items())
    old_files = {r['path']: r for r in prior['tex_files']}
    new_files = {r['path']: r for r in audit['tex_files']}
    inherited = set(old_files) - {str(build.OLD.relative_to(ROOT))}
    assert all(p in new_files and old_files[p]['sha256'] == new_files[p]['sha256'] for p in inherited)
    assert native.exact() == json.loads((native.BASE / 'exact-oracle.json').read_text())
    assert causalml.exact_examples() == json.loads((causalml.BASE / 'oracle-results.json').read_text())
    assert evaluation.calculate() == json.loads((evaluation.BASE / 'exact-oracle.json').read_text())
    extracted = re.sub(r'\s+', ' ', (OUT / 'reader.txt').read_text())
    for phrase in ['Native discovery when important borrower variables are hidden',
                   'A restricted CausalML route for heterogeneous offer effects',
                   'What published evaluations establish and how to reuse them',
                   'Full cost and the investment threshold', '2,952', '78.75%']:
        assert phrase.lower() in extracted.lower(), phrase
    evidence = [ref(OUT / 'source-audit.json', '514 exact-reader citation identities'),
                ref(BASE / 'traceability-review.json', '153 genuine scholarly PDFs and all citation contexts'),
                ref(OUT / 'reader.txt', 'Reviewed added sections in the compiled reader'),
                ref(OUT / 'text-layout-review.json', 'All-page extraction and physical bounds'),
                ref(BASE / 'prepared-inputs.json', 'Preserving source and generated-input identities'),
                ref(BASE / 'preparation-repair.json', 'Observed preparation repair')]
    for module in [native, causalml, evaluation]:
        for name in ['primary-review.json', 'author-review.json']:
            obj = json.loads((module.BASE / name).read_text())
            verify_bindings(obj)
            evidence.append(ref(module.BASE / name, 'Scoped primary/source and author findings'))
    evidence += [ref(native.BASE / 'exact-oracle.json', 'Nine endpoint pairs and observationally equal worlds'),
                 ref(native.BASE / 'omissions-register.json', 'Incomplete native coverage and exact revisit actions'),
                 ref(causalml.BASE / 'oracle-results.json', 'Targets, policy value and rare-arm resampling'),
                 ref(evaluation.BASE / 'exact-oracle.json', 'Request denominators, costs and precision'),
                 ref(evaluation.BASE / 'prospective-inputs.json', 'Unexecuted future study requirements'),
                 ref(BASE.parent / 'v2/build-failure-review.json', 'Preserved failed candidate and math-mode repair'),
                 ref(Path(__file__), 'Publication and exact-reader review procedure')]
    state = core.read(ROOT, core.STATE)
    write(BASE / 'release-source-review.json', {
        'status': 'pass', 'issues': [], 'reviewer': REVIEWER,
        'scope': 'Exact working-reader author delta review of native software, optional CausalML reuse, primary evaluations and full-cost scenarios',
        'reviewed_reader': report['pdf'],
        'prior_reviews': {q: state['execution_runtime']['results']['PROPOSAL.' + q] for q in ['Q2', 'Q3', 'Q4']},
        'unchanged_source_records': 506, 'new_source_records': sorted(set(current) - set(previous)),
        'unchanged_inherited_compiled_sources': len(inherited),
        'cited_sources': 514, 'scholarly_pdfs': index['scholarly_pdfs'],
        'findings': [
            'All predecessor source records and compiled chapter bytes remain unchanged; eight citation records bind the added material.',
            'Native graph marks, complete-case selection, dependency notices and unresolved MIIC export semantics are differentiated; source coverage remains inconclusive.',
            'CausalML target averaging, multi-arm variance populations, row resampling and learned-policy limitations are explicitly scoped; admission is deferred.',
            'Seven primary evaluations retain their actual tasks, subsets, denominators, model settings and adverse evidence; no bank productivity claim is inferred.',
            'Three independent exact-reference families replay: graph conversion/hidden worlds, stratified targets/policy, and full-cost/request/precision arithmetic.',
            'The illustrative cost comparison changes from 1000 to 5000 break-even requests under the stated error loss and becomes negative under the larger error scenario.',
            'All new sections are integrated within the relevant main chapters; no automatic substantive-page credit or repair completion is awarded.',
        ], 'evidence': evidence, 'limitations': LIMITS,
        'visual_acceptance': False, 'bank_ROI_established': False,
    })
    print(json.dumps({'review': 'pass', 'pages': 692, 'citations': 514, 'scholarly_pdfs': index['scholarly_pdfs']}))


def publish():
    state = core.read(ROOT, core.STATE)
    before = core.sha(ROOT / core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path'] == str(build.OLD.with_suffix('.pdf').relative_to(ROOT))
    report = json.loads((OUT / 'build-report.json').read_text())
    audit = json.loads((OUT / 'source-audit.json').read_text())
    reviewed = json.loads((BASE / 'release-source-review.json').read_text())
    verify_bindings(reviewed)
    manifest = {'kind': 'working_monograph', 'final_acceptance': False,
        'pdf': report['pdf'], 'pages': report['pages'],
        'supersedes': {k: state['reader'][k] for k in ['path', 'sha256']},
        'build_report': ref(OUT / 'build-report.json', '692-page compiled successor'),
        'source_review': ref(BASE / 'release-source-review.json', 'Content, source and exact-reference delta review'),
        'text_layout': ref(OUT / 'text-layout-review.json', 'All-page text and bounds review'),
        'source_artifacts': audit['tex_files'] + reviewed['evidence'],
        'visual_acceptance': False, 'mandatory_repairs_closed': [],
        'changes': ['Added native latent discovery and restricted CausalML comparison.',
                    'Integrated primary evaluation findings, denominator accounting and full-cost scenarios.'],
        'sponsor_binding': 'Preserved sponsor baseline; Q5 reconciliation remains open.'}
    write(BASE / 'working-release.json', manifest)
    binding = ref(BASE / 'working-release.json', 'Reviewed native/reuse/evaluation working release')
    run.ledger.validate_working_release(ROOT, binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader'] = {k: report['pdf'][k] for k in ['path', 'sha256']}
    state['reader'].update(pages=692, status='Working monograph; Q1/Q5 and whole-repair acceptance open')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT, before, state, {'action': 'publish_native_evaluation_working_reader',
                                  'manifest': binding, 'final_acceptance': False})
    print(json.dumps({'published': state['reader'], 'final_acceptance': False}))


def renew():
    report = json.loads((OUT / 'build-report.json').read_text())
    review_doc = json.loads((BASE / 'release-source-review.json').read_text())
    findings = {
        'Q2': 'All 506 predecessor records and inherited chapter bytes are retained. Eight new records bind 514 cited sources, 153 genuine scholarly PDFs, pinned original software and explicitly declared project derivations. Whole-reader traceability passes; native census completeness remains inconclusive and receives no completion waiver.',
        'Q3': 'Earlier executed demonstrations and negative verdicts remain unchanged. Three added exact-reference families reproduce endpoint information loss, two equal observational laws, distinct ATE/ATT/ATC targets, rare-arm failure and request denominators. These are stipulated examples. Static engines, benchmark reuse, future live-model study and bank outcomes are not relabeled as executed demonstrations.',
        'Q4': 'Preserved banking investment scenarios are supplemented by USD31 versus18.50 illustrative request costs. Explicit error-loss sensitivity changes fixed-cost break-even from1000 to5000 requests and can eliminate positive variable value. Primary studies motivate a narrow public/generated-data prototype; mechanism-level precision, actual prices and later bank loss remain explicit inputs. No measured ROI is asserted.'}
    for q, finding in findings.items():
        identifier = 'PROPOSAL.' + q
        state = core.read(ROOT, core.STATE)
        assert state['reader']['sha256'] == report['pdf']['sha256']
        previous = state['execution_runtime']['results'][identifier]
        old = json.loads((ROOT / previous['path']).read_text())
        folder = BASE / q
        folder.mkdir(exist_ok=False)
        evidence = [previous, ref(BASE / 'working-release.json', 'Exact successor working reader'),
                    ref(BASE / 'release-source-review.json', 'Content/source/example/investment delta')]
        write(folder / 'reopen.json', {'reason': 'Working reader changed; retain and renew the earlier exact-reader proposal review.',
            'prior_result': previous, 'reviewed_reader': report['pdf'], 'evidence': evidence,
            'next_action': 'Record the author review of the exact native/reuse/evaluation successor.'})
        transition('reopen', identifier, folder / 'reopen.json')
        state = core.read(ROOT, core.STATE)
        graph, _, _ = run.combined(ROOT, state)
        node = run.ledger.operation(graph, identifier)
        attempt = len(state['execution_runtime']['review_history'][identifier])
        output = ROOT / run.review_output_paths(node, state['reader'], attempt)[0]
        limits = list(dict.fromkeys(old['limitations'] + LIMITS))
        scope = 'Author exact-reader delta review; proposal evidence only'
        write(output, {'operation': identifier, 'status': 'pass', 'criterion': node['criteria'][0],
            'reviewer': REVIEWER, 'reviewed_reader': report['pdf'], 'review_attempt': attempt,
            'acceptance_scope': 'proposal_only', 'scope': scope, 'findings': [finding],
            'evidence': evidence, 'limitations': limits, 'visual_acceptance': False, 'bank_ROI_established': False})
        receipt = run.ledger.receipt_template(node)
        receipt.update(outcome='pass', execution='performed', scope=scope, reviewer=REVIEWER,
            limitations=limits, reviewed_reader=report['pdf'], review_attempt=attempt,
            acceptance_scope='proposal_only', outputs=[ref(output, 'Exact current-reader ' + q + ' review')],
            nonexecution_reason='', revisit_trigger='',
            criteria=[{'index': 0, 'verdict': 'pass', 'finding': finding, 'evidence': evidence}])
        write(folder / 'operation-receipt.json', receipt)
        transition('record', identifier, folder / 'operation-receipt.json')
    print(json.dumps({'exact_reader_reviews': 'Q2-Q4 pass', 'proposal_acceptance': False}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['review', 'publish', 'renew'])
    {'review': review, 'publish': publish, 'renew': renew}[parser.parse_args().action]()
