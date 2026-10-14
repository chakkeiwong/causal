#!/usr/bin/env python3
"""Review and publish the corrected latent-language comparison."""
import argparse
import json
from pathlib import Path
import re

import build_other_latent_reader_v2_20261014 as build
import master_control as core
import review_other_latent_20261014 as work
import run_program as run
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

ROOT, BASE, OUT = work.ROOT, build.BASE, build.OUT
LIMITS = ['Author review only; no independent scientific or bank acceptance.',
          'Six selected families and36 source blobs; no executed upstream engine or measured causal performance.',
          'Broader census, missing scholarly originals and dependency/rights/runtime qualification remain open.',
          'No automatic substantive-page or mandatory-repair credit; Q1 remains open.',
          'The six-preview allowance is exhausted under /home/ubuntu/AGENTS.md; visual acceptance and Q5 remain open.']
NEW_KEYS = {'exec14_olatent_'+k for k in work.SPECS} | {
    'exec14_olatent_rcd_paper', 'exec14_olatent_search', 'exec14_olatent_oracle'}


def review():
    report = json.loads((OUT/'build-report.json').read_text())
    audit = json.loads((OUT/'source-audit.json').read_text())
    prior = json.loads(build.PRIOR.read_text())
    index = json.loads((BASE/'traceability-review.json').read_text())
    for obj in [report, audit, prior, index, json.loads((BASE/'prepared-inputs.json').read_text())]:
        verify_bindings(obj)
    assert index['status'] == 'pass' and not index['issues'] and index['scholarly_pdfs'] == 156
    assert json.loads((OUT/'text-layout-review.json').read_text())['status'] == 'pass'
    assert not [w for w in report['warnings'] if 'Underfull' not in w]
    old = {r['integrated_citation_key']: r for r in prior['sources']}
    new = {r['integrated_citation_key']: r for r in audit['sources']}
    assert len(old) == 522 and len(new) == 531 and new.keys()-old.keys() == NEW_KEYS
    assert all(new[k] == row for k, row in old.items())
    compiled = {r['path']: r for r in audit['tex_files']}
    inherited = [r for r in prior['tex_files'] if r['path'] != str(build.OLD.relative_to(ROOT))]
    assert all(compiled[r['path']]['sha256'] == r['sha256'] for r in inherited)
    prev = json.loads((ROOT/'docs/program/execution/2026-10-14/expert-evidence/publication/traceability-review.json').read_text())
    contexts = {r['citation_key']: r['citation_contexts'] for r in index['records']}
    assert all(contexts[r['citation_key']] == r['citation_contexts'] for r in prev['records'])
    assert work.exact() == json.loads((work.BASE/'exact-oracle.json').read_text())
    original = work.SYN.read_text()
    corrected = build.SYN.read_text()
    assert corrected == original.replace("``confidence''", 'confidence').replace("``latent effects''", 'latent effects')
    tex = (BASE/'comparison.tex').read_text()
    assert r'\texttt{confidence' not in tex
    text = re.sub(r'\s+', ' ', (OUT/'reader.txt').read_text())
    for phrase in ['Latent discovery beyond the principal language interfaces',
                   'USD 70', 'minus USD 30', 'squared norm two',
                   'proper MAG and PAG validation', 'first twenty of 640 and 74']:
        assert phrase.lower() in text.lower(), phrase
    findings = [
        'Julia raw endpoint direction, keyword-stage discrepancy,100-path caps and missing bidirected plotting branch match the selected pinned implementation; no upstream runtime is asserted.',
        'The authentic RCD original differs from the inspected Rust path. Its substantive coefficient invariant and heuristic confidence limitations are explained without presenting the path as a validated port.',
        'L-MARVEL skeleton/unresolved-state and CI settings, GIN contrast/default-order/rights gaps, OCT Tetrad delegation/selected MAG/row folds and DAGitty validation/conversion limits are distinguished.',
        'Exact hidden-risk, selection, null-contrast and endpoint diagnostics replay. The null contrast is nonzero; floating-point SVD behavior remains unobserved.',
        'Five queries,137 retained identities and six selected families are bounded; outstanding search pages, primary originals and environment/rights reviews remain explicit.',
        'The quotation conversion defect is repaired in a preserved successor. Physical pages266-270 and surrounding extracted text were inspected; whole-reader bounds checks pass, with visual acceptance pending.',
        'All522 earlier source records, contexts and compiled chapter bytes remain unchanged; nine new records yield531 records and156 authentic scholarly PDFs.',
    ]
    evidence = [ref(p, a) for p, a in [
        (OUT/'build-report.json', 'Exact corrected successor PDF'), (OUT/'source-audit.json', '531 source records'),
        (OUT/'reader.txt', 'Inspected comparative text and equations'), (OUT/'text-layout-review.json', 'Every-page text and bounds'),
        (BASE/'traceability-review.json', '156 genuine scholarly originals and citation contexts'),
        (BASE/'prepared-inputs.json', 'Corrected and preserving manuscript inputs'),
        (work.BASE/'v2/repair-review.json', 'Recorded conversion defect and successor repair'),
        (work.BASE/'primary-review.json', '36 inspected pinned blobs'),
        (work.BASE/'exact-oracle.json', 'Independent exact mechanisms'),
        (work.BASE/'omissions-register.json', 'Unwaived limitations'),
        (build.SYN, 'Corrected connected manuscript'), (Path(__file__), 'Actual review procedure'),
    ]]
    write(BASE/'release-source-review.json', {'status': 'pass', 'issues': [], 'reviewer': work.REVIEWER,
        'reviewed_reader': report['pdf'], 'findings': findings, 'evidence': evidence,
        'unchanged_source_records': 522, 'new_source_records': sorted(NEW_KEYS),
        'unchanged_inherited_compiled_sources': len(inherited), 'unchanged_inherited_citation_contexts': True,
        'limitations': LIMITS, 'visual_acceptance': False, 'bank_ROI_established': False})
    prior_build = work.BASE/'publication/reader/build-report.json'
    write(BASE/'superseded-attempt.json', {'status': 'rejected_for_publication',
        'prior_build': ref(prior_build, 'Successful compile with observed quotation typography defect'),
        'reason': 'Markdown parsed TeX quotation syntax as a cross-phrase code span.',
        'successor': report['pdf'], 'scientific_change': False, 'review': ref(BASE/'release-source-review.json', 'Corrected source/text review')})
    receipt = json.loads((work.BASE/'operation-receipt.json').read_text())
    extra = [ref(BASE/'release-source-review.json', 'Current corrected-reader review'),
             ref(BASE/'superseded-attempt.json', 'Preserved rejected attempt and repair')]
    for criterion in receipt['criteria']:
        criterion['evidence'] += extra
    receipt['limitations'] += ['Visual acceptance remains pending; initial quotation defect preserved and repaired.']
    write(BASE/'coverage-operation-receipt.json', receipt)
    print(json.dumps({'review': 'pass', 'pages': report['pages'], 'cited_records': 531, 'cell_coverage': 'inconclusive'}))


def publish():
    state = core.read(ROOT, core.STATE)
    before = core.sha(ROOT/core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path'] == str(build.OLD.with_suffix('.pdf').relative_to(ROOT))
    assert 'SW.CELL.discovery_latent.other_relevant' in state['execution_program']['results']
    report = json.loads((OUT/'build-report.json').read_text())
    audit = json.loads((OUT/'source-audit.json').read_text())
    review = json.loads((BASE/'release-source-review.json').read_text())
    verify_bindings(review)
    manifest = {'kind': 'working_monograph', 'final_acceptance': False, 'pdf': report['pdf'], 'pages': report['pages'],
        'supersedes': {k: state['reader'][k] for k in ['path', 'sha256']},
        'build_report': ref(OUT/'build-report.json', 'Preserving corrected latent-language reader'),
        'source_review': ref(BASE/'release-source-review.json', 'Source, mathematical and text review'),
        'text_layout': ref(OUT/'text-layout-review.json', 'All-page text and bounds'),
        'source_artifacts': audit['tex_files']+review['evidence'], 'visual_acceptance': False,
        'mandatory_repairs_closed': [],
        'changes': ['Integrate six latent-language software pathways and concrete reuse limitations.',
                    'Develop exact hidden-risk, selection, nonzero-null-contrast and endpoint diagnostics.'],
        'sponsor_binding': 'Preserved sponsor baseline; Q5 reconciliation remains open.'}
    write(BASE/'working-release.json', manifest)
    binding = ref(BASE/'working-release.json', 'Reviewed latent-language successor')
    run.ledger.validate_working_release(ROOT, binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader'] = {k: report['pdf'][k] for k in ['path', 'sha256']}
    state['reader'].update(pages=report['pages'], status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT, before, state, {'action': 'publish_latent_language_reader', 'manifest': binding, 'final_acceptance': False})
    print(json.dumps({'published': state['reader'], 'proposal_accepted': False}))


def renew():
    report = json.loads((OUT/'build-report.json').read_text())
    findings = {
        'Q2': 'All522 earlier citation records/contexts and manuscript inputs are preserved. Nine new records bind36 selected primary blobs, complete cutoff trees, one authentic RCD original, bounded discovery and exact diagnostics:531 records and156 scholarly PDFs. Missing originals, rights and runtime closure are explicit.',
        'Q3': 'The previous demonstration portfolio is unchanged. Exact hidden-risk, selection, null-contrast and conversion mechanisms reproduce; no upstream execution, package failure rate, theorem or empirical model qualification is asserted.',
        'Q4': 'The imposed banking mechanism distinguishes associational net70USD from causal net minus30USD. Concrete adaptation/defer/reject decisions and inexpensive exact-oracle comparisons explain what to establish before bank spending. No bank price, superiority or ROI has been inferred.',
    }
    verify_bindings(json.loads((BASE/'release-source-review.json').read_text()))
    for q, finding in findings.items():
        identifier = 'PROPOSAL.'+q
        state = core.read(ROOT, core.STATE)
        assert state['reader']['sha256'] == report['pdf']['sha256']
        previous = state['execution_runtime']['results'][identifier]
        old = json.loads((ROOT/previous['path']).read_text())
        folder = BASE/q
        folder.mkdir(exist_ok=False)
        evidence = [previous, ref(BASE/'working-release.json', 'Exact current reader'),
                    ref(BASE/'release-source-review.json', 'Reviewed source and mathematics delta'),
                    ref(Path(__file__), 'Current review findings')]
        write(folder/'reopen.json', {'reason': 'Reader changed; preserve and renew the earlier review.',
            'prior_result': previous, 'reviewed_reader': report['pdf'], 'evidence': evidence,
            'next_action': 'Record reviewed latent-language findings against the new reader.'})
        transition('reopen', identifier, folder/'reopen.json')
        state = core.read(ROOT, core.STATE)
        graph, _, _ = run.combined(ROOT, state)
        node = run.ledger.operation(graph, identifier)
        attempt = len(state['execution_runtime']['review_history'][identifier])
        output = ROOT/run.review_output_paths(node, state['reader'], attempt)[0]
        limits = list(dict.fromkeys(old['limitations']+LIMITS))
        scope = 'Author exact-reader delta review; proposal evidence only'
        write(output, {'operation': identifier, 'status': 'pass', 'criterion': node['criteria'][0],
            'reviewer': work.REVIEWER, 'reviewed_reader': report['pdf'], 'review_attempt': attempt,
            'acceptance_scope': 'proposal_only', 'scope': scope, 'findings': [finding],
            'evidence': evidence, 'limitations': limits, 'visual_acceptance': False})
        receipt = run.ledger.receipt_template(node)
        receipt.update(outcome='pass', execution='performed', scope=scope, reviewer=work.REVIEWER,
            limitations=limits, reviewed_reader=report['pdf'], review_attempt=attempt,
            acceptance_scope='proposal_only', outputs=[ref(output, 'Current-reader '+q+' review')],
            nonexecution_reason='', revisit_trigger='',
            criteria=[{'index': 0, 'verdict': 'pass', 'finding': finding, 'evidence': evidence}])
        write(folder/'operation-receipt.json', receipt)
        transition('record', identifier, folder/'operation-receipt.json')
    print(json.dumps({'exact_reader_reviews': 'Q2-Q4 pass', 'proposal_accepted': False}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['review', 'publish', 'renew'])
    args = parser.parse_args()
    {'review': review, 'publish': publish, 'renew': renew}[args.command]()
