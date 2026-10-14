#!/usr/bin/env python3
"""Freeze the reviewed funding protocol without invoking the final study."""
import json
from pathlib import Path
import sys

import run_program as control
import funding_journey_20261013 as journey

ROOT, BASE = journey.ROOT, journey.BASE
sys.path.insert(0, str(ROOT / 'src'))
from causalbank.runtime_v12 import execution_identity


def main():
    assert not journey.DESIGN.exists(), 'Protocol already frozen'
    assert not (BASE / 'local-journal.json').exists(), 'Final study already started'
    ref, write = journey.ref, journey.write
    state = control.core.read(ROOT, control.core.STATE)
    graph, _, _ = control.combined(ROOT, state)
    local = control.ledger.operation(graph, 'IN.JOURNEY.LOCAL.funding')
    design = control.ledger.operation(graph, 'IN.JOURNEY.DESIGN.funding')
    cases = json.loads((BASE / 'fixtures.json').read_text())['cases']
    preflight = json.loads((BASE / 'design-preflight.json').read_text())
    assert preflight['status'] == 'pass' and preflight['final_service_invocations'] == 0
    write(BASE / 'environment.json', execution_identity())
    inputs = [ROOT / 'tools' / name for name in ['funding_journey_20261013.py', 'funding_examples_20261013.py',
                                               'freeze_funding_journey_20261013.py', 'discovery_journey_20261013.py']]
    inputs += [BASE / name for name in ['fixtures.json', 'design-preflight.json', 'environment.json', 'exact-examples.json', 'plan-review.md']]
    inputs += [ROOT / 'src/causalbank' / name for name in ['artifacts_v12.py', 'operation_contract_v12.py', 'operation_service_v12.py',
               'runtime_v12.py', 'worker_v12.py', 'cli_v12.py', 'mcp_server_v12.py', 'responses.py', 'causal_workflow.py']]
    inputs += [ROOT / 'docs/program/repair-v12/work/IN02' / name for name in ['request-schema.json', 'response-schema.json']]
    evidence = [ref(p, 'Frozen reviewed funding fixture, reference, source, environment or schema') for p in inputs]
    review = {'operation_id': local['id'], 'design_approved': True, 'unresolved_design_blockers': [],
              'scope_matches_contract': True, 'retained_predecessor_failures': True,
              'reviewer': {'name': 'Codex author', 'kind': 'author'},
              'review': ref(BASE / 'plan-review.md', 'Full chain, independent derivations, costs, exposed limits and execution sequence'),
              'preflight': ref(BASE / 'design-preflight.json', 'All 29 schemas valid; no final service invocations'),
              'execution_inputs': evidence,
              'scope': 'Deterministic conformance and boundary screen; no random-sampling calibration or automated financial recommendation'}
    write(BASE / 'argument-review.json', review)
    review_ref = ref(BASE / 'argument-review.json', 'Author approval of the exact scoped design')
    protocol = {
        'operation_id': local['id'], 'operation_contract_sha256': control.core.digest_object(local),
        'target': 'Preserve a twelve-month average funding response in million USD per percentage point through supplied-moment inversion, boundaries and replay.',
        'model': 'Authored normal residual inequalities, a nonorthogonal fitted-nuisance example, finite household/inclusion truth and an annual profit scenario.',
        'observation_law': 'Fixed generated summaries and five feature-clock rows. No bank observations or random final draws.',
        'sampling_unit': 'A request slot. The scientific context declares dependent monthly origins; the service does not validate that law. The independent Gaussian toy reference has its own expressly different law.',
        'method': 'All 29 cases via library and CLI, initially and after restart; two changed-horizon conflicts; compare complete outputs with fixed analytic references.',
        'assumptions': ['The ratio is causal only under external identification and normalization premises.',
                        'Covariance, identity/inclusion and local linearity are supplied, unverified declarations.',
                        'Known Gaussian references illustrate arithmetic and a specific variance law, not arbitrary fitted/dependent validity.'],
        'uncertainty_claim': 'Nominal Gaussian supplied-covariance inversion; preserve pointwise versus Bonferroni labels. No empirical coverage study, general joint estimated-nuisance result or decision qualification.',
        'alternatives': ['Fixed versus joint fitted-nuisance covariance under the exact example',
                         'Analytic residual inequalities versus runtime inversion', 'Record versus household units; unweighted versus known-probability HT expectation',
                         'Library versus CLI and restart replay', 'Full effect/profit set versus favorable point answer'],
        'adverse_cases': [c['id'] for c in cases if c['expected']['disposition'] in ['unsupported', 'refused', 'unavailable']]
            + ['weak_denominator_rays', 'no_information_whole', 'incompatible_zero_noise_empty', 'zero_noise_singleton', 'unresolved_link_map', 'unknown_inclusion'],
        'metrics': ['Every attempted slot, expected dispositions/errors and preserved topologies',
                    'Numeric endpoints under absolute 1e-9/relative 1e-10 tolerance',
                    'Exact context, units, sampling labels, assumptions, uncertainty qualifications and all-field parity excluding only request_id',
                    'Invocation and active-runner wall time; separate process high-water RSS'],
        'acceptance_rules': {'pass': 'All 118 slots and 29 four-response parity comparisons match the frozen expectations.',
                             'negative': 'Any mismatch is retained and reviewed; do not change fixtures to match responses.',
                             'execution_failure': 'Preserve checkpoint and all failed attempts; no replacement or favorable-only denominator.'},
        'replications': 1, 'seed': 26101308, 'seed_role': 'Fixture version only; no random sampling',
        'stopping_rule': 'fixed_design_no_outcome_stopping',
        'derivation_review': review_ref, 'successor_review': review_ref,
        'screen_operating_characteristics': 'Fixed authored boundary conformance only; no estimated power, coverage or false-acceptance probability.',
        'width_and_availability_rules': 'Retain empty, singleton, rays and whole-line sets. Refusals are unavailable estimates. Narrow sets on unverified inputs cannot establish useful financial precision.',
        'fresh_data_provenance': 'New deterministic fixtures and isolated library/CLI artifact roots; no empirical held-out claim.',
        'execution_inputs': evidence, 'input_sha256': {x['path']: x['sha256'] for x in evidence},
        'fixtures': ref(BASE / 'fixtures.json', 'Exact input contexts, body errors and independent expected outcomes'),
        'invocation_count': len(cases)*4+2,
        'decision_chain': {
            'business': 'Evaluate a quarter-point deposit-rate increase over the next twelve months.',
            'target': 'Average retained balance, not endpoint balance; one-pp normalization with separate local-linearity premise.',
            'clock': 'Feature event<=available<decision; outcomes have separate later follow-up/censoring requirements.',
            'information': 'Dated household map, inclusion/population, proxy/quote/outcome meanings and covariance provenance.',
            'sampling': 'Monthly dependence and overlapping horizons need joint covariance; supplied labels do not prove its validity.',
            'identification': 'No general continuous/panel identification engine; proxy premises cannot be inferred from moments.',
            'estimation': 'Runtime inverts supplied summaries; fitting and joint fitted-nuisance derivation remain upstream.',
            'uncertainty': 'Preserve disconnected/unbounded sets and distinguish Bonferroni coordinate construction from a general joint result.',
            'numerical': 'Independent factorizations and strict endpoint tolerance; no certified general solver.',
            'decision': 'Proposed consumer reviews premises and maps the complete set through profit; holds when prerequisites fail. This decision layer is not implemented by the local screen.'},
        'cost_accounting': {
            'scenario': 'USD 6500 baseline repricing plus USD 500 workflow; profit=3750*beta-7000 under stated annual balances/spreads.',
            'workflow_USD_assumptions': {'data_identity_preparation': 120, 'integration_amortization': 150, 'scientific_review': 100, 'computation': 30, 'monitoring_recovery': 100},
            'measured': 'Every invocation including worker/CLI startup, replay and failures; active runner import/journal time; separate parent/child peak RSS.',
            'excluded_from_timing': 'Inter-segment idle time, initial interpreter/module startup, author/review/manuscript work and all unexecuted activities.',
            'additional_categories': ['failed requests/retries', 'human adjudication', 'optional live-model acquisition/calls', 'held-out evaluation',
                                      'legal/platform review', 'implementation', 'security', 'deployment', 'ongoing operations'],
            'money': 'Scenario inputs only; no measured bank prices, accepted ROI or cost-per-bank-decision.'},
        'evidence_classes': {'local_execution': 'Registered fixed library/CLI calculation and refusal screen',
            'independent_reference': 'Exact inequalities, covariance/inclusion sums and profit endpoints',
            'contract_double': 'Future explicit consumer boundary with prerequisite checks; not executed here',
            'authentic_owner_run': 'Later owner maps/design/inclusion/follow-up/cost traces and accepted disposition, only if prototype merit warrants expense'},
        'limits': ['No raw-data fitting or joint estimated-nuisance/dependence proof', 'No verified household identity/inclusion or bank observations',
                   'No live model, MCP requalification, language adapter or actual sibling execution',
                   'No empirical nominal-coverage or bank-profit claim', 'Replay/restart is not process-kill or multi-host crash qualification']}
    write(journey.DESIGN, protocol)
    output = ref(journey.DESIGN, 'Reviewed funding workflow and frozen local screen')
    receipt = control.ledger.receipt_template(design)
    receipt.update(outcome='pass', execution='performed',
        scope='Reviewed funding workflow design, exact references and 29 frozen cases; final service execution remains separately registered',
        reviewer=review['reviewer'], limitations=protocol['limits'], outputs=[output])
    findings = ['Full clock/target/information/sampling/covariance/decision chain, negative cases and complete cost categories are declared and reviewed.',
                'The available local service is testable with 29 cases and independent analytic references; unavailable fitting, proposed doubles and authentic owner evidence are separate, with no sibling execution.']
    for index, finding in enumerate(findings):
        receipt['criteria'][index].update(verdict='pass', finding=finding, evidence=[output, review_ref,
            ref(BASE / 'plan-review.md', 'Author review and exact execution sequence')])
    write(BASE / 'design-receipt.json', receipt)
    print(json.dumps({'frozen_cases': len(cases), 'invocations': protocol['invocation_count'], 'protocol': output['path'], 'final_trial_run': False}))


if __name__ == '__main__':
    main()
