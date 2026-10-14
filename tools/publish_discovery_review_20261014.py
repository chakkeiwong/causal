#!/usr/bin/env python3
"""Publish reviewed discovery scholarship and record its bounded author acceptance."""
import argparse
import json
from pathlib import Path
import re

import discovery_design_oracles_20261014 as design
import discovery_screening_value_20261014 as screening
import prepare_reader_repair_20261014 as initial
import review_estimation_validation_20261014 as estimation
import run_program as run
import master_control as core
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-14/l4-completion/v3'
OUT = BASE / 'reader'
PARENT = BASE.parent
OP = 'TEXT.REVIEW.L4'
ORIGINAL = ROOT / 'docs/program/execution/2026-10-13/l2/final-v4/reader'
OUTPUT = ROOT / 'docs/program/comprehensive-v14/work/TEXT.REVIEW.L4/chapter-review.json'


def review():
    assert not OUTPUT.exists() and not (BASE / 'release-source-review.json').exists()
    report = json.loads((OUT / 'build-report.json').read_text())
    audit = json.loads((OUT / 'source-audit.json').read_text())
    index = json.loads((BASE / 'traceability-review.json').read_text())
    prior = json.loads((ORIGINAL / 'source-audit.json').read_text())
    for obj in [report, audit, index, prior, json.loads((BASE / 'prepared-inputs.json').read_text())]:
        verify_bindings(obj)
    assert report['pages'] == 683 and report['cited_records'] == 506
    assert index['status'] == 'pass' and not index['issues']
    assert json.loads((OUT / 'text-layout-review.json').read_text())['status'] == 'pass'
    assert not [w for w in report['warnings'] if 'Underfull' not in w]
    previous = {s['integrated_citation_key']: s for s in prior['sources']}
    current = {s['integrated_citation_key']: s for s in audit['sources']}
    assert len(previous) == 497 and all(current[k] == v for k, v in previous.items())
    assert initial.exact() == json.loads((initial.BASE / 'exact-results.json').read_text())
    assert estimation.exact_oracle() == json.loads((estimation.BASE / 'exact-oracle.json').read_text())
    assert design.serializable(design.calculate()) == json.loads((PARENT / 'exact-results.json').read_text())
    assert screening.calculate() == json.loads((BASE / 'exact-results.json').read_text())
    extracted = re.sub(r'\s+', ' ', (OUT / 'reader.txt').read_text())
    for phrase in ['A correlation screen can discard a nonlinear cause',
                   'Faithfulness can fail even with complete measurements',
                   'An intervention’s value can be calculated before conducting it',
                   '94 of 98', '1.440825', 'Unknown', '1.498585']:
        assert phrase.lower() in extracted.lower(), phrase
    first = json.loads((PARENT / 'depth-review-predecessor.json').read_text())
    second = json.loads((PARENT / 'v2/depth-review-predecessor.json').read_text())
    per_page = [dict(x) for x in first['per_page'] if x['printed_page'] < 373]
    per_page += [dict(x) for x in second['new_page_credit']]
    per_page[-1]['credit'] = 1
    per_page[-1]['rationale'] += ' The final layout adds the nonlinear-screen motivation on the same page.'
    per_page += [{'printed_page': 381, 'credit': 1,
                  'rationale': 'New nonlinear dependence and sign-symmetry derivation, feature intervention distinction, and separate query objective.'},
                 {'printed_page': 382, 'credit': .75,
                  'rationale': 'Exact entropy/decision-value reversal and weak/accurate query calculations; repeated prototype closing discounted.'}]
    assert len(per_page) == 29 and sum(x['credit'] for x in per_page) == 21.5
    state = core.read(ROOT, core.STATE)
    prior_reviews = {k: state['execution_runtime']['results']['PROPOSAL.' + k] for k in ['Q2', 'Q3', 'Q4']}
    source_evidence = [ref(OUT / 'source-audit.json', 'All 506 cited records and compiled sources'),
                       ref(BASE / 'traceability-review.json', 'Exact citation contexts and primary copy identities'),
                       ref(initial.BASE / 'draft-repair-review.json', 'Earlier omissions, target and scorer corrections'),
                       ref(PARENT / 'source-audit.json', 'New primary rereads and explicit model assumptions'),
                       ref(BASE / 'source-audit.json', 'New nonlinear and decision references'),
                       ref(initial.BASE / 'exact-results.json', 'Original L4 and AIPW algebra'),
                       ref(PARENT / 'exact-results.json', 'Exact covariance and full binomial outcomes'),
                       ref(BASE / 'exact-results.json', 'Nonlinear moments and priced query arithmetic'),
                       ref(estimation.BASE / 'primary-review.json', 'Preserved pinned estimation package inspection'),
                       ref(estimation.BASE / 'exact-oracle.json', 'Replayed target and scoring examples'),
                       ref(ROOT / 'docs/program/execution/2026-10-14/servicing-journey/local-review.json', '98-request preserved negative local screen'),
                       ref(ROOT / 'docs/program/execution/2026-10-14/servicing-journey/expectation-correction.json', 'Documented safe error, frozen failed expectation preserved'),
                       ref(ROOT / 'docs/program/execution/2026-10-14/commercial-latent-comparison/author-review.json', 'Reviewed commercial comparison now integrated'),
                       ref(ROOT / 'docs/program/execution/2026-10-14/java-latent/primary-review.json', 'Pinned Java source scope'),
                       ref(ROOT / 'docs/program/execution/2026-10-14/causallearn-reuse/primary-review.json', 'Scoped Python reuse sources'),
                       ref(ROOT / 'docs/program/execution/2026-10-14/execution-labels/evidence-labels.json', 'Actual, static, exact and mock execution distinction')]
    for item in source_evidence:
        verify_bindings(json.loads((ROOT / item['path']).read_text()))
    limitations = ['Author content/source/depth review only; no independent scientific acceptance.',
                   'L4 depth passes; complete MR01, MR02 and MR03 coverage and whole-proposal Q1 remain open.',
                   'No live model, external discovery engine or bank experiment was executed in this continuation.',
                   'Exact examples are declared project laws and planning scenarios; no bank ROI is established.',
                   'Rendered image review remains pending: inherited six-preview allowance is exhausted under /home/ubuntu/AGENTS.md.',
                   'Q5 sponsor reconciliation and exact rendered release acceptance remain open.']
    chapter = {'operation_id': OP, 'status': 'pass', 'reviewer': {'name': 'Codex author/coordinator', 'kind': 'author'},
               'scope': 'L4 discovery chapter in the exact 683-page working reader; content, sources, mathematics and nonduplicate depth',
               'allocation': {'min': 20, 'target': 21, 'max': 22},
               'physical_span': {'first_printed_page': 354, 'last_printed_page': 382, 'pages': 29,
                                 'first_pdf_page': 371, 'last_pdf_page': 399},
               'substantive_page_credit': 21.5,
               'measurement': 'Conservative author page-equivalent review under the unchanged standard typography; partial pages, overlap, generic recaps and already credited L3/software material deducted.',
               'per_page': per_page, 'allocation_exception': None,
               'double_counting': 'Credit belongs only to L4. No credit from added estimation/commercial/integration sections or public-data survey. Shared software and L3 exposition explicitly discounted.',
               'subject_coverage': ['Language-only and retrieval-assisted graph proposals, soft/hard priors, statistical prompting and correlated debate',
                                    'CPDAG/PAG/RFCI meaning, temporal discovery and longitudinal intervention distinctions',
                                    'Numerical alternatives, structural premises, source-specific packages and conditional reuse decisions',
                                    'Two-world coverage/risk limits, cancellation, depth bounds, misleading environment invariance and nonlinear screening',
                                    'Restriction-error sensitivity, actual versus proposed execution, admissible public/generated evaluation',
                                    'Intervention-value calculation, attainable sample information, graph entropy versus decision loss'],
               'findings': [{'issue': '674-page candidate had 20 physical but only 12.75 credited pages.',
                             'resolution': 'Preserved negative review; developed distinct numerical alternatives and exact adverse cases.'},
                            {'issue': '681-page candidate still had only 19.5 credited pages.',
                             'resolution': 'Added nonlinear-screen proof and explicit information-versus-decision query analysis; final credit 21.5.'},
                            {'issue': 'A temporal section was nested under an earlier conclusion.',
                             'resolution': 'Promoted section hierarchy in a preserving source copy.'},
                            {'issue': 'A missing LaTeX escape stopped one build.',
                             'resolution': 'Failed source/log preserved; one escaped brace repaired in a successor and compiled.'}],
               'evidence': [report['pdf'], ref(OUT / 'build-report.json', 'Exact chapter pages and successful compile'),
                            ref(OUT / 'reader.txt', 'Page-level text reviewed'), ref(PARENT / 'depth-review-predecessor.json', 'First negative review'),
                            ref(PARENT / 'v2/depth-review-predecessor.json', 'Second negative review'),
                            ref(BASE / 'build-repair.json', 'Observed build failure and correction')] + source_evidence,
               'limitations': limitations, 'visual_acceptance': False, 'original_gap_qualification': False}
    write(OUTPUT, chapter)
    prior_paths = {x['path']: x for x in prior['tex_files']}
    current_paths = {x['path']: x for x in audit['tex_files']}
    unchanged = [p for p in prior_paths.keys() & current_paths.keys() if prior_paths[p]['sha256'] == current_paths[p]['sha256']]
    source_review = {'status': 'pass', 'issues': [], 'reviewer': chapter['reviewer'],
                    'scope': 'Exact-reader author review of preserved 497-source baseline and nine new records, integrated source conclusions and exact project derivations',
                    'reviewed_reader': report['pdf'], 'prior_reviews': prior_reviews,
                    'unchanged_prior_source_records': 497, 'new_source_records': sorted(current.keys() - previous.keys()),
                    'unchanged_predecessor_compiled_sources': len(unchanged),
                    'scholarly_pdfs': index['scholarly_pdfs'], 'cited_sources': index['cited_sources'],
                    'findings': ['Inherited primary source identities remain unchanged. Nine new records concern pinned software/evidence and explicit project derivations.',
                                 'Fresh primary rereads support NOTEARS optimization scope, LiNGAM model assumptions and invariant-prediction conditions.',
                                 'All added covariance, conditioning, AIPW, target-weight and full-outcome decision calculations reproduce.',
                                 'Commercial comparisons, Java/Python source findings and execution labels now appear in the main reader.',
                                 'The 98-request servicing screen remains negative at 94 expected outcomes; safe corruption rejection is not hidden or relabeled.',
                                 'New financial amounts are stipulated cost/utility scenarios; likelihoods and information-transfer assumptions are explicit.'],
                    'evidence': source_evidence + [ref(OUTPUT, 'Substantive L4 review')],
                    'limitations': limitations, 'visual_acceptance': False, 'bank_ROI_established': False}
    write(BASE / 'release-source-review.json', source_review)
    print(json.dumps({'review': 'pass', 'substantive_L4_pages': 21.5, 'citations': index['cited_sources'],
                      'scholarly_PDFs': index['scholarly_pdfs'], 'unchanged_compiled_sources': len(unchanged)}))


def publish():
    state = core.read(ROOT, core.STATE)
    before = core.sha(ROOT / core.STATE)
    assert state['execution_runtime']['active']['operation'] == OP
    assert state['reader']['path'] == 'docs/causal_proposal_l2_v4_2026-10-13.pdf'
    report = json.loads((OUT / 'build-report.json').read_text())
    audit = json.loads((OUT / 'source-audit.json').read_text())
    reviewed = json.loads((BASE / 'release-source-review.json').read_text())
    verify_bindings(reviewed)
    manifest = {'kind': 'working_monograph', 'final_acceptance': False, 'pdf': report['pdf'], 'pages': report['pages'],
                'supersedes': {k: state['reader'][k] for k in ['path', 'sha256']},
                'build_report': ref(OUT / 'build-report.json', '683-page preserving reader'),
                'source_review': ref(BASE / 'release-source-review.json', 'Scientific/source delta reviewed'),
                'text_layout': ref(OUT / 'text-layout-review.json', 'All-page extracted text and physical bounds'),
                'source_artifacts': audit['tex_files'] + reviewed['evidence'] + [
                    ref(OUT / 'source-audit.json', '506 cited source records'),
                    ref(Path(__file__), 'Review and publication procedure')],
                'visual_acceptance': False, 'mandatory_repairs_closed': [],
                'changes': ['Completed L4 content/depth review with 21.5 nonduplicate page equivalents.',
                            'Integrated previous estimation, commercial-latent, Java/Python and execution-evidence developments.',
                            'Added exact model limits and a decision-valued public prototype argument.'],
                'sponsor_binding': 'Preserved sponsor baseline; Q5 reconciliation remains open.'}
    write(BASE / 'working-release.json', manifest)
    binding = ref(BASE / 'working-release.json', 'Reviewed discovery working release')
    run.ledger.validate_working_release(ROOT, binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader'] = {k: report['pdf'][k] for k in ['path', 'sha256']}
    state['reader'].update(pages=report['pages'], status='Working monograph; Q1/Q5 and whole-repair acceptance open')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT, before, state, {'action': 'publish_discovery_review_working_reader', 'manifest': binding, 'final_acceptance': False})
    graph, _, _ = run.combined(ROOT, state)
    receipt = run.ledger.receipt_template(run.ledger.operation(graph, OP))
    receipt.update(outcome='pass', execution='performed', scope='Author L4 source/content/mathematical/depth review in the 683-page reader',
                   reviewer=reviewed['reviewer'], limitations=reviewed['limitations'],
                   outputs=[ref(OUTPUT, 'Complete chapter review'), binding], nonexecution_reason='', revisit_trigger='',
                   criteria=[{'index': 0, 'verdict': 'pass',
                              'finding': 'All allocated discovery topics, primary methods, alternatives, failures, proposed remedies and banking decision consequences are developed. Mathematical and citation findings are resolved; external performance and unresolved identification are not invented.',
                              'evidence': [ref(OUTPUT, 'Coverage and substantive findings'), ref(BASE / 'release-source-review.json', 'Source and exact-reference review')]},
                             {'index': 1, 'verdict': 'pass',
                              'finding': 'Page-by-page review credits 21.5 substantive equivalents in 29 physical pages, within the 20-22 allocation. Duplicate L3/software exposition, generic framing and partial content are deducted; no exception or public-survey credit is used.',
                              'evidence': [ref(OUTPUT, 'Per-page credit and deductions'), ref(OUT / 'build-report.json', 'Exact physical span')]}])
    write(BASE / 'operation-receipt.json', receipt)
    transition('record', OP, BASE / 'operation-receipt.json')


def renew():
    report = json.loads((OUT / 'build-report.json').read_text())
    review_doc = json.loads((BASE / 'release-source-review.json').read_text())
    findings = {
        'Q2': 'All 497 predecessor source records remain unchanged; nine new records extend the exact reader to 506 citations with genuine local scholarly copies and bound software/project records. Primary rereads support numerical alternatives. The source and text checks pass; L4 duplicate credit is explicitly deducted.',
        'Q3': 'Preserved demonstrations remain scoped. New exact model, screening, restriction and decision examples replay without random draws or external engines. The actual 98-request servicing trial retains 94 expected outcomes and its frozen negative verdict; supported interfaces are not relabeled a policy estimator. No live model or bank demonstration is claimed.',
        'Q4': 'The original investment scenarios are preserved. New exact finite-probe values, including 1.440825 units at 20 probes below the 1.5 perfect-information ceiling, show how prototype evidence could justify a later study. Information-gain and decision-value rankings can differ. Priors, likelihoods, costs and transfer population are stipulated; no measured ROI or price is inferred.'}
    for q, finding in findings.items():
        identifier = 'PROPOSAL.' + q
        state = core.read(ROOT, core.STATE)
        previous = state['execution_runtime']['results'][identifier]
        old = json.loads((ROOT / previous['path']).read_text())
        folder = BASE / q
        folder.mkdir(exist_ok=False)
        evidence = [previous, ref(BASE / 'working-release.json', 'New exact working reader'),
                    ref(BASE / 'release-source-review.json', 'Reviewed source, example and investment delta'),
                    ref(OUTPUT, 'Author L4 chapter review')]
        write(folder / 'reopen.json', {'reason': 'Integrated reader changed; preserve the earlier proposal review and review this exact PDF.',
              'prior_result': previous, 'reviewed_reader': report['pdf'], 'evidence': evidence,
              'next_action': 'Record the reviewed preserving source, demonstration and investment delta.'})
        transition('reopen', identifier, folder / 'reopen.json')
        state = core.read(ROOT, core.STATE)
        graph, _, _ = run.combined(ROOT, state)
        node = run.ledger.operation(graph, identifier)
        attempt = len(state['execution_runtime']['review_history'][identifier])
        output = ROOT / run.review_output_paths(node, state['reader'], attempt)[0]
        limits = list(dict.fromkeys(old['limitations'] + review_doc['limitations']))
        reviewed = {'operation': identifier, 'status': 'pass', 'criterion': node['criteria'][0],
                    'reviewer': review_doc['reviewer'], 'reviewed_reader': report['pdf'], 'review_attempt': attempt,
                    'acceptance_scope': 'proposal_only', 'scope': 'Author exact-reader delta review; proposal evidence only',
                    'findings': [finding], 'evidence': evidence, 'limitations': limits,
                    'visual_acceptance': False, 'bank_ROI_established': False}
        write(output, reviewed)
        receipt = run.ledger.receipt_template(node)
        receipt.update(outcome='pass', execution='performed', scope=reviewed['scope'], reviewer=reviewed['reviewer'],
                       limitations=limits, reviewed_reader=report['pdf'], review_attempt=attempt, acceptance_scope='proposal_only',
                       outputs=[ref(output, 'Exact current-reader ' + q + ' review')], nonexecution_reason='', revisit_trigger='',
                       criteria=[{'index': 0, 'verdict': 'pass', 'finding': finding, 'evidence': evidence}])
        write(folder / 'operation-receipt.json', receipt)
        transition('record', identifier, folder / 'operation-receipt.json')
    print(json.dumps({'exact_reader_reviews': 'Q2-Q4 pass', 'proposal_acceptance': False}))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('action', choices=['review', 'publish', 'renew'])
    {'review': review, 'publish': publish, 'renew': renew}[p.parse_args().action]()
