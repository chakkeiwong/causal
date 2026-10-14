#!/usr/bin/env python3
"""Prepare a concrete execution queue and preserved-state publication candidate."""
import copy
import json
from pathlib import Path

import master_control as core
import causal_program_v13_1 as control
import build_gap_successor_v13_1 as book

ROOT = core.ROOT
BASE = ROOT/control.BASE


def ref(path, anchor):
    return {'path': str(path.relative_to(ROOT)), 'sha256': core.sha(path), 'anchor': anchor}


def main():
    before = ROOT/core.STATE
    prior = core.read(ROOT, core.STATE)
    if 'execution_refresh' in prior or (BASE/'predecessor-state.json').exists():
        raise ValueError('Refresh already prepared or published; preserve it')
    (BASE/'predecessor-state.json').write_bytes(before.read_bytes())
    def unit(name, parents, lane, status, action, evidence, stop):
        return {'id': name, 'parents': parents, 'lane': lane, 'status': status,
                'next_action': action, 'completion_evidence': evidence, 'stop_condition': stop,
                'owner': 'Authorized local author until an authentic external owner is supplied'}
    units = [
        unit('SW-H1', ['SW01'], 'known_local', 'completed_scoped_inspection',
             'Use the eight versioned dossiers as source evidence; retain their unresolved downstream paths.',
             ['work/SW01/source-audit.json', 'work/SW01/dossiers.md'], 'No full package, cell or SW01 completion claimed.'),
        unit('EX-H1', ['SW01','LA07'], 'known_local', 'completed_stipulated_examples',
             'Use the five exact example families with their explicit assumptions and no empirical claim.',
             ['semantic-examples.json', 'chapters/graph-and-uncertainty.tex', 'chapters/histories-forests-densities.tex'], 'These examples do not test vendor runtimes.'),
        unit('SW-H2', ['SW01'], 'known_local', 'ready',
             'Trace CausalGPS downstream matching/weighting and counterfactual-dose uses; inspect pygformula output/history paths; prepare isolated reproduction protocols for the scale and failed-bootstrap findings.',
             ['New pinned technical-body audit', 'Separate source-level versus reproduced findings', 'Explicit adopt/defer decision and alternatives'],
             'Pause an affected claim if the original or required runtime is unavailable; preserve the finding without calling it reproduced.'),
        unit('SW-C1', ['SW01'], 'known_local', 'ready',
             'Review the 102-cell register individually, beginning with saved R panel/DiD/sensitivity paths and Java/C++ graph paths; complete each two-pass search with alternatives and omissions before claiming closure.',
             ['Versioned search ledger with providers, queries and cutoff', 'Individual primary anchors for admitted candidates or justified bounded no-candidate disposition', 'Coverage matrix and omissions'],
             'An essential inaccessible source blocks its claim; search failure never establishes absent capability.'),
        unit('SW-V1', ['SW01','SW06'], 'known_route_missing_source_evidence', 'preparation_ready',
             'Prepare edition-specific commercial matrices, identify original manual/acquisition routes and compare every verified claim to implemented, conditional, proposed or absent project capability.',
             ['Versioned original vendor manual and provenance', 'Edition/license/pricing status', 'Claim-by-claim capability comparison'],
             'Collector host restrictions and unavailable originals remain explicit; review a successor acquisition route rather than silently expanding permissions.'),
        unit('LA-W1', ['LA07'], 'known_local', 'ready',
             'Expand the eight allocated chapters in order of missing task coverage: translation/measurement, evidence/diagrams, discovery and the remaining workflow; develop a case, adverse case, alternatives and source-supported remedy per task.',
             ['14-task coverage map', 'Primary literature/package audit', '96–112 substantive-page review without duplicate credit', 'Contradictory-findings review'],
             'Uninspected or missing originals block claims; offline fixtures cannot support live performance.'),
        unit('SW-D1', ['SW02','SW03','SW04','SW05','SW06','SW07'], 'known_local_dependency_gated', 'prepare_now_final_receipts_wait',
             'Use accessible SW01 dossiers for common-target comparisons; after SW01 passes record subject receipts, then commercial and reuse decisions.',
             ['Matched estimands, sampling laws and uncertainty', 'Commercial evidence', 'License, maintenance, alternative and revisit rationale'],
             'Do not bypass SW01 or claim a complete comparison from selected helpers.'),
        unit('IN-X1', ['IN03','SW08','IN05'], 'known_engineering_dependency_gated', 'awaits_SW07',
             'After SW07, implement representative R/Python/Java/C++ paths within causal, register matched qualification, and execute parity, refusal/topology, custody, resume/cancel and fault trials.',
             ['Executed language-path evidence', 'Frozen benchmark and full failure denominator', 'Consumer-owned trial receipts when available'],
             'Do not modify or execute sibling repositories; missing real consumers/platform stop authentic trials.'),
        unit('R-ARG', ['R02S','R03S','R04S','R05S'], 'unresolved_scientific_argument', 'argument_work_ready_final_studies_blocked',
             'Follow the four precise unresolved arguments in the refreshed plan and retained successor reviews. Derive feasible regions or score-specific bounds and compare every predecessor failure before requesting design approval.',
             ['Approved argument with scope comparison', 'Information requirements', 'Screen power and useful width/availability', 'Fresh registered protocol'],
             'No identification, nuisance/dependence bound or separating information means no final qualification campaign.'),
        unit('X-E1', ['LA06S','E01S','X01','X02','X03','X04','F01'], 'known_route_missing_external_evidence', 'awaits_authentic_inputs',
             'Use the twelve X00 packets when authentic records and owners are supplied; verify custody/identity, then follow declared package dependencies and exact-release review.',
             ['Twelve authentic input categories as applicable', 'Live calls and real prices for live qualification', 'Independent review, bank/platform/consumer and economics receipts'],
             'Author fixtures, invented prices and unsigned owner declarations cannot satisfy these gates.'),
        unit('BOOK-I1', ['SW09','LA07','IN06','I02'], 'known_editorial_dependency_gated', 'working_successor_delivered_final_open',
             'Continue the 22 allocated chapters, review all required coverage, complete substantive-page accounting and inspect rendered pages in a fresh session before author-release receipts.',
             ['Continuous main PDF/source audit', 'No missing chapter/task/cell coverage', 'Numerical, editorial and rendered-page review', 'Revised sponsor proposal'],
             'Coverage, scholarship or visual findings keep I02 open even when PDF compilation passes.')]
    obligations = {
        'D01': ('Truthful linked identity/audit collection and validation', 'Persistent-sampling uncertainty; counts-only nonidentification', ['bank_truth','pilot_and_prices']),
        'D02': ('Identified observed-history policy development and independent evaluation', 'Hidden-state identification, logger error and selected/optimal-policy uncertainty', ['bank_truth']),
        'D03': ('Graph/query/set contracts and exact small references', 'Separating information and feasible unknown-temporal-parameter regions', ['bank_truth']),
        'D04': ('Owned assignment, inclusion, timing and audit validation', 'Scientific truth is not inferable from declarations alone', ['bank_truth','independent_review']),
        'D05': ('Compare independent calendars/audits and derive joint regions', 'Feasible useful joint dependence construction in prior failed regimes', ['bank_truth','pilot_and_prices']),
        'D06': ('Contribution interfaces, selected adapters and workload trials', 'Learner-specific remainder/rate and dependence control', ['platform','consumers','workflow']),
        'D07': ('Target resource, fault, resume/cancel and recovery protocol', 'No general unknown theorem claimed; actual platform evidence is absent', ['platform','consumers','workflow']),
        'D08': ('Independent scientific, bank and consumer acceptance workflow', 'Author cannot supply independent institutional acceptance', ['independent_review','bank_truth','consumers','sponsor_decision']),
        'D09': ('Separate coverage, availability, precision and certification power', 'No universal repair; valid output may be unbounded or unusable', ['bank_truth','pilot_and_prices']),
        'D10': ('Matched workflow value and full-cost measurement', 'No general mathematical blocker claimed; actual economics and decision ownership absent', ['pilot_and_prices','workflow','sponsor_decision'])}
    gaps = [{'id': k, 'known_work': v[0], 'unresolved_or_noncomputable': v[1], 'external_inputs': v[2]} for k,v in obligations.items()]
    queue = {'execution_revision': control.EXECUTION_REVISION, 'date': '2026-10-12', 'contract_revision': prior['revision'],
        'units': units, 'gaps': gaps, 'research_final_designs_approved': [],
        'external_packets': ref(ROOT/'docs/program/gap-repair-v13/work/X00/intake-packets.json', 'Twelve prepared, unfilled authentic-input packets'),
        'next_local': ['SW-H2', 'SW-C1', 'LA-W1'], 'qualification_changes': [],
        'rule': 'Unit progress is not package completion; original dependencies and acceptance obligations remain authoritative.'}
    core.write(BASE/'execution-queue.json', queue)
    chapter = copy.deepcopy(json.loads((ROOT/'docs/program/gap-repair-v13/reader/chapter-progress.json').read_text()))
    report = json.loads((book.OUT/'build-report.json').read_text())
    chapter['scope'] = 'All 22 original allocations retained. New software development is shared material, not duplicate accepted page credit.'
    chapter['main_pdf'] = report['pdf']; chapter['physical_body_pages'] = report['physical_body_pages']
    chapter['predecessor'] = ref(ROOT/'docs/program/gap-repair-v13/reader/chapter-progress.json', 'Preserved 22-allocation map')
    for row in chapter['chapters']:
        if row['id'] in ['S2','S3','S4','S5','S7','S10']:
            row['execution_refresh_development'] = ['v131:graph-uncertainty','v131:histories-forests']
            row['accepted_substantive_pages'] = None
    core.write(book.OUT/'chapter-progress.json', chapter)
    paths = {
        'plan': ROOT/'docs/program/master-program-v13_1.md', 'plan_pdf': ROOT/'docs/program/master-program-v13_1.pdf',
        'plan_builder': ROOT/'tools/build_gap_program_pdf_v13_1.py', 'plan_layout': BASE/'program-pdf/text-layout-review.json',
        'queue': BASE/'execution-queue.json', 'review': BASE/'review.md', 'continuation': BASE/'continuation.md',
        'controller': ROOT/'tools/causal_program_v13_1.py', 'preparer': Path(__file__),
        'publisher': ROOT/'tools/publish_execution_refresh_v13_1.py', 'tests': ROOT/'tests/test_gap_execution_v13_1.py',
        'software_audit': BASE/'work/SW01/source-audit.json', 'software_coverage': BASE/'work/SW01/coverage-matrix.json',
        'software_catalog_delta': BASE/'work/SW01/catalog-delta.json', 'software_dossiers': BASE/'work/SW01/dossiers.md',
        'source_reviewer': ROOT/'tools/inspect_gap_helpers_v13_1.py', 'examples': BASE/'semantic-examples.json',
        'example_code': ROOT/'tools/gap_semantic_examples_v13_1.py', 'acquisition_review': BASE/'acquisition-review.md',
        'acquisition_dispositions': BASE/'acquisition-dispositions.json',
        'book_report': book.OUT/'build-report.json', 'book_layout': book.OUT/'text-layout-review.json',
        'book_audit': book.OUT/'source-audit.json', 'book_builder': ROOT/'tools/build_gap_successor_v13_1.py',
        'chapter_progress': book.OUT/'chapter-progress.json'}
    state = copy.deepcopy(prior)
    documents = {k: ref(v, 'V13.1 execution evidence: '+k) for k,v in paths.items()}
    state['execution_refresh'] = {'revision': control.EXECUTION_REVISION,
        'predecessor': ref(BASE/'predecessor-state.json', 'Complete preserved published V13 state'), 'documents': documents}
    state['gap_execution']['plan'] = documents['plan']
    state['gap_execution']['documents'].update({'execution_refresh_'+k:v for k,v in documents.items()})
    state['successor_document'] = documents['book_report']
    state['reader'] = {'path': report['pdf']['path'], 'sha256': report['pdf']['sha256'], 'pages': report['pages'],
        'status': 'Working V13.1 book; all three substantive repairs and final visual review remain open; not I02'}
    state['deliveries'].append(dict(state['reader']))
    issues = control.validate_state(ROOT, state)
    if issues:
        raise ValueError(str(issues))
    book.check(state['successor_document'], state)
    core.write(BASE/'proposed-state.json', state)
    print(json.dumps({'prepared': True, 'units': len(units), 'gaps': len(gaps), 'unchanged_contracts': len(prior['work_packages']),
                      'unchanged_results': len(prior['results']), 'pages': report['pages']}))


if __name__ == '__main__':
    main()
