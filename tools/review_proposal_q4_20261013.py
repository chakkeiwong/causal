#!/usr/bin/env python3
"""Exact-reader author acceptance review of proposal economics, not bank ROI."""
from fractions import Fraction as F
import json
from pathlib import Path
import re

import build_integrated_monograph_v12 as shared
import master_control as core
import proposal_economics_example
import run_program as run
import sponsor_economics_20261013

ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-13/investment-review'
ref = shared.ref


def main():
    BASE.mkdir(exist_ok=True)
    state = core.read(ROOT, core.STATE)
    assert state['reader']['path'] == 'docs/causal_proposal_active_experiments_2026-10-13.pdf'
    reader = ref(ROOT / state['reader']['path'], 'Exact 581-page working reader reviewed for Q4 only')
    assert reader['sha256'] == state['reader']['sha256']
    output = ROOT / 'docs/program/execution/acceptance/Q4.json'
    assert not output.exists(), 'Preserve earlier acceptance review'
    economic_design = ROOT / 'docs/program/comprehensive-v14/work/ECON.DESIGN/cost-design.json'
    design = json.loads(economic_design.read_text()); shared.verify_refs(design)
    assert not design['actual_bank_prices_received'] and not design['bank_ROI_established']
    assert all(x['actual_unit_price'] is None and x['actual_price_source'] is None for x in design['price_ledger'])
    # Independent exact recomputation of the three-year reuse account.
    old = json.loads((ROOT / 'docs/derivations/economics.json').read_text())
    annuity = sum(F(10, 11)**t for t in range(1, 4))
    threshold = (3/annuity+F(6, 5))/F(9, 100)
    assert abs(float(threshold)-old['constant_annual_study_threshold']) < 1e-10
    rows = []
    table = (ROOT / 'docs/derivations/reuse_economics.tex').read_text()
    for case in old['scenarios']:
        n = case['completed_studies']
        expert = 1+sum((F(3, 5)+F(15, 100)*volume)*F(10, 11)**t for t, volume in enumerate(n, 1))
        product = 4+sum((F(9, 5)+F(6, 100)*volume)*F(10, 11)**t for t, volume in enumerate(n, 1))
        saving = expert-product
        extra = max(F(0), -saving/annuity)
        values = {'expert_present_cost': expert, 'platform_present_cost': product,
                  'platform_cost_saving': saving,
                  'additional_constant_annual_decision_benefit_to_break_even': extra}
        assert all(abs(float(value)-case[key]) < 1e-10 for key, value in values.items())
        for value in [expert, product, saving]: assert f'{float(value):.3f}' in table
        rows.append({'scenario': case['scenario'], 'annual_studies': n,
                     **{key: {'exact': str(value), 'usd_millions': float(value)} for key, value in values.items()}})
    assert abs(float(2*threshold)-old['sensitivity']['half_per_study_saving_threshold']) < 1e-10
    shared_cost_case = (3/annuity+2)/F(9, 100)
    assert abs(float(shared_cost_case)-old['sensitivity']['annual_shared_gap_2m_threshold']) < 1e-10
    tranche = (6*6*25000+50000)*F(6, 5)
    assert tranche == 1140000 == old['pilot_budget']['total_usd']
    # Re-run the prior proposal calculator through its pure function, leaving
    # the original receipt-bound JSON untouched.
    replay = proposal_economics_example.calculate()
    assert replay == json.loads((ROOT / 'docs/program/comprehensive-v14/work/ECON.DESIGN/illustration.json').read_text())
    exact_sponsor = sponsor_economics_20261013.calculate()
    assert exact_sponsor['EVSI'] == '5200' and exact_sponsor['EVPI'] == '36000'
    assert exact_sponsor['net_information_value_at_8000'] == '-2800'
    assert exact_sponsor['net_information_value_at_3000'] == '2200'
    # Separate CNY information example; no currency aggregation with USD.
    gross_cny = F(1, 2)*F(9, 10)*100-F(1, 2)*F(1, 10)*300
    assert gross_cny == 30 and gross_cny-10 == 20 and F(50000, 20) == 2500
    assert F(1, 2)*100 == 50
    current = ROOT / 'docs/program/execution/2026-10-13/active-experiments'
    active_review = json.loads((current / 'exact-review.json').read_text())
    assert active_review['status'] == 'pass'; shared.verify_refs(active_review)
    numerical = {'status': 'pass', 'issues': [], 'kind': 'author_assumption_arithmetic_not_empirical_ROI',
        'three_year_reuse': {'currency': 'USD million', 'annuity': str(annuity),
            'annual_study_threshold': str(threshold), 'scenarios': rows,
            'half_saving_threshold': str(2*threshold), 'shared_premium_2m_threshold': str(shared_cost_case),
            'first_tranche_usd': str(tranche), 'tranche_in_initial_capital_not_added_twice': True},
        'prior_proposal_calculator_replay': replay, 'exact_sponsor_replay': exact_sponsor,
        'separate_cny_example': {'gross_information_value': '30', 'net_value': '20',
            'perfect_information_value': '50', 'fixed_cost_break_even_decisions': '2500'},
        'active_acquisition_review': ref(current / 'exact-review.json', 'Independent stopping/all-attempt verification'),
        'empirical_prices': False, 'bank_ROI': False,
        'review_code': ref(Path(__file__), 'Independent rational reuse account plus preserved calculator replays')}
    core.write(BASE / 'arithmetic-review.json', numerical)
    aux = (current / 'reader/causal_proposal_active_experiments_2026-10-13.aux').read_text()
    labels = ['r3:investment', 'r3:cost-model', 'r3:incremental-value', 'r3:adoption-experiment',
              'r3:investment-sequence', 'r3:commercial-product', 'la:economics',
              'exec13:active-experiments', 'exec13:active-experiments-end']
    pages = {}
    for label in labels:
        match = re.search(r'\\newlabel\{'+re.escape(label)+r'\}\{\{[^}]*\}\{(\d+)\}', aux)
        assert match, label
        pages[label] = int(match.group(1))
    paths = ['docs/reconstruction/21_investment.tex', 'docs/derivations/economics.json',
             'docs/derivations/reuse_economics.tex', 'docs/program/repair-v12/work/LA07/economics-chapter.tex',
             'docs/program/public-data-v15/survey.md', 'docs/program/public-data-v15/survey.tex',
             'docs/program/comprehensive-v14/work/ECON.DESIGN/argument.md',
             'docs/program/comprehensive-v14/work/ECON.DESIGN/cost-design.json',
             'docs/program/comprehensive-v14/work/ECON.DESIGN/illustration.json',
             'tools/proposal_economics_example.py', 'tools/sponsor_economics_20261013.py',
             'docs/program/execution/2026-10-13/active-experiments/chapter.tex',
             'docs/program/execution/2026-10-13/active-experiments/author-review.json',
             'docs/program/execution/2026-10-13/active-experiments/traceability-review.json',
             'docs/program/execution/2026-10-13/active-experiments/reader/source-audit.json']
    evidence = [ref(ROOT / p, 'Inspected investment account, exact source or claim limit') for p in paths]
    evidence += [ref(BASE / 'arithmetic-review.json', 'Independent exact arithmetic review')]
    findings = [
        {'requirement': 'Fair baseline', 'verdict': 'pass',
         'finding': 'Capable expert composition with the same methods, information, reusable templates, scientific output and review is the comparator. No product premium is justified by withholding tools from that baseline.'},
        {'requirement': 'Complete cost categories and units', 'verdict': 'pass',
         'finding': 'Initial/shared/marginal costs, unsuccessful work, adoption timing, review, data, compute, integration, recovery and institutional participation are distinct. Missing actual prices remain null. USD, USD-million and CNY examples are separate.'},
        {'requirement': 'Negative cases and sensitivity', 'verdict': 'pass',
         'finding': 'Low/moderate reuse and the adoption ramp lose under the assumed account. Marginal savings and shared-cost sensitivities, harmful decisions, correlated tasks, unsupported causal truth and hard constraints are explicit.'},
        {'requirement': 'Value of information', 'verdict': 'pass',
         'finding': 'EVSI compares the best action before/after information and subtracts information cost separately. The 8000-cost study has negative assumed net value; failure denominators, irrelevant information, correlated answers and finite stopping are developed.'},
        {'requirement': 'Conditional next experiment', 'verdict': 'pass',
         'finding': 'Start with matched public/generated tasks and explicit acquisition/compute budgets; compare fixed/random/numerical and optional model-assisted decisions, including clean and failed cases. Bank measurement follows only if prototype evidence reveals a decision-changing unresolved variable and plausible positive net information value.'},
        {'requirement': 'Proposal claim boundary', 'verdict': 'pass',
         'finding': 'No measured bank ROI, adoption, labor substitution, vendor quotation or calibrated bank signal likelihood is asserted. Runtime measurements are explicitly separated from labor value.'}]
    review = {'operation': 'PROPOSAL.Q4', 'status': 'pass', 'issues': [], 'acceptance_scope': 'proposal_only',
        'reviewer': {'name': 'Codex author/coordinator', 'kind': 'author'}, 'reviewed_reader': reader,
        'printed_page_anchors': pages, 'findings': findings, 'evidence': evidence,
        'recommendation': 'The economic argument supports evaluating a bounded prototype under declared scenarios. It does not authorize a bank investment or claim positive empirical ROI.',
        'remaining_conditional_inputs': ['Actual task mix, adoption, review effort and fully priced institutional work',
            'Empirical loss, signal calibration, transport and feasible intervention information for a particular later bank study',
            'A prospectively registered sampled protocol before any final study claim'],
        'not_awarded': ['Q1 manuscript depth', 'Q2 full semantic source acceptance', 'Q3 all demonstration claims',
                        'Q5 sponsor/rendered release coherence', 'independent acceptance', 'bank/product qualification'],
        'visual_acceptance': False, 'bank_ROI_established': False}
    core.write(output, review)
    graph, _, _ = run.combined(ROOT, state)
    node = run.ledger.operation(graph, 'PROPOSAL.Q4')
    receipt = run.ledger.receipt_template(node)
    receipt.update(outcome='pass', execution='performed', scope='Exact current-reader author review of proposal economics and conditional experimentation',
        reviewer=review['reviewer'], reviewed_reader=reader, acceptance_scope='proposal_only', review_attempt=0,
        limitations=['All numerical price, value, prevalence and signal inputs are author assumptions; no empirical ROI.',
                     'Review is author-only and specific to the current reader; other acceptance gates remain separate.',
                     'Future final studies need their actual frozen protocols; later bank inputs depend on a justified question.'],
        outputs=[ref(output, 'Completed exact-reader Q4 review')], nonexecution_reason='', revisit_trigger='')
    receipt['criteria'] = [{'index': 0, 'verdict': 'pass',
        'finding': 'Developed equivalent-output baseline, complete cost categories, adverse/sensitivity cases, exact VOI calculations and a conditional public/generated-first next experiment satisfy the proposal criterion without bank ROI claims.',
        'evidence': [ref(output, 'Requirement-by-requirement review'), ref(BASE / 'arithmetic-review.json', 'Independent arithmetic'),
                     ref(current / 'chapter.tex', 'Conditional next experiment and acquisition failure cases')]}]
    core.write(BASE / 'operation-receipt.json', receipt)
    print(json.dumps({'review': 'pass', 'scope': 'proposal_only', 'reader_pages': state['reader']['pages'],
                      'page_anchors': pages, 'bank_ROI': False}))


if __name__ == '__main__':
    main()
