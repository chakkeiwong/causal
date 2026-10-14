#!/usr/bin/env python3
"""Preserving successor Q4 author review of the 587-page operations reader."""
import copy
from fractions import Fraction as F
import json
from pathlib import Path
import re

import build_integrated_monograph_v12 as shared
import master_control as core
import operation_planning_examples_20261013 as operations
import run_program as run

ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-13/investment-review'
OPS = ROOT / 'docs/program/execution/2026-10-13/operational-adoption'
ref = shared.ref


def main():
    state = core.read(ROOT, core.STATE)
    assert state['execution_runtime']['active']['operation'] == 'PROPOSAL.Q4'
    assert state['reader']['path'] == 'docs/causal_proposal_operations_2026-10-13.pdf'
    reader = ref(ROOT / state['reader']['path'], 'Exact 587-page reader reviewed for proposal Q4')
    assert reader['sha256'] == state['reader']['sha256']
    graph, _, _ = run.combined(ROOT, state)
    node = run.ledger.operation(graph, 'PROPOSAL.Q4')
    attempt = len(state['execution_runtime']['review_history']['PROPOSAL.Q4'])
    assert attempt == 1
    output = ROOT / run.review_output_paths(node, reader, attempt)[0]
    arithmetic_path = BASE / 'operations-arithmetic-review.json'
    receipt_path = BASE / 'operations-operation-receipt.json'
    assert not any(p.exists() for p in (output, arithmetic_path, receipt_path)), 'Preserve immutable evidence'

    prior_path = ROOT / 'docs/program/execution/acceptance/Q4.json'
    previous = core.read(ROOT, str(prior_path.relative_to(ROOT)))
    shared.verify_refs(previous)
    assert previous['status'] == 'pass'
    for name in ('exact-review.json', 'author-review.json', 'working-release.json'):
        evidence = json.loads((OPS / name).read_text())
        shared.verify_refs(evidence)
    # Pure replay plus a distinct 100-request cost account and conditional
    # failure-law calculation. No random trials or prices are inferred.
    actual = operations.serialize(operations.calculate())
    assert actual == json.loads((OPS / 'exact-results.json').read_text())
    full_cost = F(70*10-15*30-100*2-15*20, 100)
    completed_cost = F(70*10-15*30-85*2, 85)
    persistent_success = F(9, 10)*(1-F(1, 10)**3)
    attempts = F(1, 10)*3+F(9, 10)*(1+F(1, 10)+F(1, 100))
    assert full_cost == F(-5, 2) and completed_cost == F(16, 17)
    assert persistent_success == F(8991, 10000) and attempts == F(1299, 1000)
    numerical = {
        'status': 'pass', 'issues': [], 'prior_investment_evidence_unchanged': True,
        'prior_review': ref(prior_path, 'Every prior economics and information-value evidence hash verified unchanged'),
        'prior_arithmetic': ref(BASE / 'arithmetic-review.json', 'Preserved exact reuse and value-of-information checks'),
        'operational_results': ref(OPS / 'exact-results.json', 'Pure calculation replay equals preserved output'),
        'independent_cost_account': {'requests': 100, 'all_attempt_usd': str(full_cost),
            'completed_only_usd': str(completed_cost), 'persistent_success': str(persistent_success),
            'persistent_expected_attempts': str(attempts)},
        'interpretation': 'Failure selection can reverse the sign of a stipulated benefit. Persistent failures invalidate an independent-retry approximation.',
        'empirical_prices': False, 'new_runtime_trials': 0, 'bank_ROI': False,
        'review_code': ref(Path(__file__), 'Successor review and separate finite arithmetic')}
    core.write(arithmetic_path, numerical)

    aux_path = OPS / 'reader/causal_proposal_operations_2026-10-13.aux'
    aux = aux_path.read_text()
    labels = list(previous['printed_page_anchors']) + ['in:operations', 'exec13:operations-end', 'pd15:investment']
    pages = {}
    for label in labels:
        match = re.search(r'\\newlabel\{'+re.escape(label)+r'\}\{\{[^}]*\}\{(\d+)\}', aux)
        assert match, label
        pages[label] = int(match.group(1))
    review = copy.deepcopy(previous)
    review.update(reviewed_reader=reader, review_attempt=attempt, printed_page_anchors=pages,
        supersedes=ref(prior_path, 'Preserved passing Q4 review of earlier 581-page reader'),
        review_method='Verify unchanged prior evidence; inspect the new operating chapter and independently recompute its cost/retry cases; bind successor reader and anchors.')
    review['evidence'] += [
        ref(ROOT / 'docs/program/comprehensive-v14/work/TEXT.DRAFT.I4/chapter.tex', 'Operating costs, failure denominators, persistent retries and qualification limits'),
        ref(arithmetic_path, 'Successor arithmetic and prior evidence identity review'),
        ref(OPS / 'author-review.json', 'Source/implementation and stipulated-example boundaries'),
        ref(OPS / 'working-release.json', 'Preserving 587-page compiled release'),
        ref(aux_path, 'Updated exact-reader printed anchors')]
    review['findings'] += [{'requirement': 'Successor operational costs and reliability', 'verdict': 'pass',
        'finding': 'The all-attempt account is -2.5 USD versus a selected completed-only +16/17 USD under declared assumptions. Persistent-failure success is 0.8991, not the false independent-marginal 0.993141. Retry costs do not become new independent banking opportunities. No measured reliability or prices are asserted.'}]
    core.write(output, review)
    receipt = run.ledger.receipt_template(node)
    receipt.update(outcome='pass', execution='performed',
        scope='Successor exact-reader author review of conditional proposal economics and all-attempt operation costs',
        reviewer=review['reviewer'], reviewed_reader=reader, acceptance_scope='proposal_only', review_attempt=attempt,
        limitations=['All numerical costs, probabilities and values remain stipulated, without measured bank ROI.',
                    'Author Q4 review only; Q1, Q2, Q3, Q5 and independent acceptance remain separate.',
                    'No new runtime experiment, bank experiment or visual acceptance.'],
        outputs=[ref(output, 'Immutable successor Q4 review')], nonexecution_reason='', revisit_trigger='')
    receipt['criteria'] = [{'index': 0, 'verdict': 'pass',
        'finding': 'Unchanged reviewed investment and information-value arguments plus the new whole-cost and persistent-retry cases support a conditional bounded prototype recommendation for this exact reader.',
        'evidence': [ref(output, 'Requirement-by-requirement successor review'),
                     ref(arithmetic_path, 'Preserved economics and new independent arithmetic')]}]
    core.write(receipt_path, receipt)
    print(json.dumps({'status': 'pass', 'review_attempt': attempt, 'reader_pages': 587,
                      'printed_page_anchors': pages, 'receipt': str(receipt_path.relative_to(ROOT))}))


if __name__ == '__main__':
    main()
