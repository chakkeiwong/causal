#!/usr/bin/env python3
"""Bind the reviewed servicing boundary protocol before service invocations."""
import json
from pathlib import Path

import run_program as control
import servicing_journey_20261014 as journey
from causalbank.runtime_v12 import execution_identity


def main():
    root, base = journey.ROOT, journey.BASE
    ref, write = journey.ref, journey.write
    assert not journey.DESIGN.exists() and not (base / 'local-journal.json').exists()
    graph, _, _ = control.combined(root, control.core.read(root, control.core.STATE))
    local = control.ledger.operation(graph, 'IN.JOURNEY.LOCAL.servicing')
    design = control.ledger.operation(graph, 'IN.JOURNEY.DESIGN.servicing')
    cases = json.loads((base / 'fixtures.json').read_text())['cases']
    preflight = json.loads((base / 'design-preflight.json').read_text())
    assert preflight['status'] == 'pass' and preflight['final_service_invocations'] == 0
    write(base / 'environment.json', execution_identity())
    inputs = [Path(__file__), root / 'tools/servicing_journey_20261014.py',
              root / 'tools/discovery_journey_20261013.py', root / 'tools/servicing_observed_examples_20261013.py']
    inputs += [base / n for n in ['fixtures.json', 'design-preflight.json', 'plan-review.md', 'environment.json']]
    inputs += [root / 'src/causalbank' / n for n in ['artifacts_v12.py', 'operation_contract_v12.py',
        'operation_service_v12.py', 'runtime_v12.py', 'worker_v12.py', 'cli_v12.py', 'mcp_server_v12.py',
        'responses.py', 'causal_workflow.py']]
    inputs += [root / 'docs/program/repair-v12/work/IN02' / n for n in ['request-schema.json', 'response-schema.json']]
    inputs += [root / 'docs/program/execution/2026-10-13/servicing' / n for n in
               ['exact-results.json', 'source-audit.json', 'argument-author-review.json',
                'SCI.ARGUMENT.R03S.receipt.json', 'SCI.DESIGN.R03S.receipt.json']]
    inputs += [root / 'docs/program/comprehensive-v14/work/SCI.ARGUMENT.R03S/argument-and-counterexamples.md',
               root / 'docs/program/comprehensive-v14/work/SCI.DESIGN.R03S/successor-review.json',
               root / 'docs/program/public-data-v15/studies/P4/design.json']
    evidence = [ref(p, 'Frozen servicing fixture, code, environment, review or preserved scientific evidence') for p in inputs]
    review = {'operation_id': local['id'], 'design_approved': True, 'unresolved_design_blockers': [],
        'scope_matches_contract': True, 'retained_predecessor_failures': True,
        'reviewer': {'name': 'Codex author/coordinator', 'kind': 'author'},
        'review': ref(base / 'plan-review.md', 'Scientific chain, boundary cases, independent formulas, cost scope and sequential plan'),
        'preflight': ref(base / 'design-preflight.json', '24 valid authored declarations; no final service invocation'),
        'execution_inputs': evidence,
        'scope': 'Conformance to explicit installed/unsupported behavior, not approval of the negative R03S sampling study'}
    write(base / 'argument-review.json', review)
    review_ref = ref(base / 'argument-review.json', 'Author-approved bounded conformance design; scientific predecessor failures retained')
    protocol = {
        'operation_id': local['id'], 'operation_contract_sha256': control.core.digest_object(local),
        'target': 'Preserve the target, clock, uncertainty meaning and refusals of a two-period servicing policy request.',
        'model': 'Fixed authored contexts, declared assumptions, timestamps and supplied scalar inequalities; exact finite-state reference separate.',
        'observation_law': 'Deterministic generated requests. No new customer sampling, public-data fit or bank observations.',
        'sampling_unit': 'One request for conformance; whole independent customer trajectory for the separate scientific argument.',
        'method': '24 fixtures through library and CLI, each initial/restart, plus two changed-horizon conflicts; 98 calls; replay preserved exact reference separately.',
        'assumptions': ['Scientific premises in request contexts are declarations, not verified truths.',
                        'The current service has no servicing estimator; policy requests must preserve unsupported/refused results.',
                        'Ordinary restart replay is tested on fresh isolated operator roots; no multi-host recovery claim.'],
        'uncertainty_claim': 'No new sampling-confidence or coverage claim. Supplied inequality sets are sensitivity; exact generated values are arithmetic references.',
        'alternatives': ['Independent path-sum versus backward recursion and prefix change of measure',
                         'Library versus CLI and initial versus restart',
                         'Supplied versus estimated logger, fixed versus training-selected versus unknown optimum requests',
                         'Retained refusals versus unjustified numeric output'],
        'adverse_cases': [c['id'] for c in cases if c['expected']['disposition'] != 'computed'] + ['clock_leakage', 'idempotency_drift'],
        'metrics': ['98-slot all-request expectation agreement', '24 complete semantic parity comparisons',
                    'Qualification, contexts, graph marks, set topology, error and CLI exit preservation',
                    'Invocation wall, active runner wall, separate exact-reference wall, parent/child peak RSS'],
        'acceptance_rules': {'pass': 'All 98 slots and all 24 four-way parity comparisons match frozen expectations; preserved exact reference matches in full.',
                             'negative': 'Any scientific/semantic/transport expectation mismatch; retain all inputs and outputs.',
                             'inconclusive': 'An execution obstruction prevents completing the fixed suite; retain completed slots and exact recovery action.'},
        'replications': 1, 'seed': 26101401, 'seed_role': 'Fixed suite identity; no random draws',
        'stopping_rule': 'fixed_design_no_outcome_stopping',
        'derivation_review': review_ref, 'successor_review': review_ref,
        'screen_operating_characteristics': 'Deterministic 98-call conformance screen; no general error rate, power or empirical validity qualification.',
        'width_and_availability_rules': 'Unknown/refused is unavailable, not zero or empty. Empty/disconnected/unbounded sensitivity is preserved. [-4,4] is a supplied single-policy range, not contrast confidence. Existing broad width failure remains.',
        'fresh_data_provenance': 'New authored immutable boundary fixtures and isolated operator roots; preserved exact examples explicitly replayed, not called fresh qualification data.',
        'execution_inputs': evidence, 'input_sha256': {r['path']: r['sha256'] for r in evidence},
        'fixtures': ref(base / 'fixtures.json', 'Exact cases, context, input artifact bodies and expected behavior'),
        'invocation_count': 98,
        'decision_chain': {
            'business': 'Compare assistance with ordinary collection for the original eligible cohort',
            'clock': 'History available before action; retention then reward/next history; stop observed score at absorbing dropout',
            'target': 'V(realized policy)-V(never-assist), independent of evaluation; no unknown optimum claim',
            'information': 'Sufficient observable dated histories, action/retention law, policy split and feasible actions; private state and truth are not inferred from interface declarations',
            'sampling': 'Independent whole customer trajectories; common calendar dependence is outside the restricted proof',
            'identification': 'Consistency, exchangeability, noninformative observation and support are necessary; identical observed laws with differing values remain explicit counterexamples',
            'estimation': 'Finite-table nuisance argument is inherited project work; no installed policy estimator is tested or fabricated',
            'uncertainty': 'Finite-table bound is conservative and too wide in the preserved example; no P4 or general hidden-state calibration',
            'numerical': 'Exact path/recursion/observed-prefix calculations separately reproduced; simple quadratic topology checked analytically',
            'decision': 'Conditional generated-law reward and full-workflow planning scenarios; a consumer must preserve scientific limitations before an investment recommendation'},
        'cost_accounting': {
            'scenario': '1000 generated customers, assumed USD100/utility; contrast 5/8 gives USD62500 incremental reward; assistance already deducted.',
            'workflow_USD_assumptions': {'data_rights_cleaning': 1500, 'fitting_selection': 1000, 'integration_allocation': 2000,
                'human_review': 2000, 'compute_storage_recovery': 500, 'monitoring_operations': 1000, 'evaluation_privacy_governance': 2000},
            'scenario_net_USD': 52500, 'break_even_workflow_USD': 62500,
            'high_cost_sensitivity': {'assumed_workflow_USD': 75000, 'scenario_net_USD': -12500},
            'measured': 'Every invocation including failed/replayed requests and worker/CLI startup; active import/journal wall; exact reference wall separately; individual parent/child high-water RSS.',
            'excluded': 'Initial interpreter/module startup, intersegment idle, authoring/review/manuscript time, simultaneous tree memory and unexecuted workflow components.',
            'additional_categories': ['optional live-model calls', 'licenses', 'external data acquisition', 'training/evaluation',
                'human adjudication', 'fault/retry handling', 'implementation and maintenance', 'deployment and authentic study'],
            'money': 'All currency inputs stipulated; no measured bank prices or ROI.'},
        'evidence_classes': {'local_execution': 'Frozen library/CLI behavior and exact-reference replay',
            'independent_reference': 'Different arithmetic formulas under generated truth; not independent institutional review',
            'contract_double': 'Proposed consumer prerequisites and interpretation only; no executed consumer double',
            'authentic_owner_run': 'Later dated cohorts, truth/design/split, real costs, owner trace and accepted disposition if justified by prototype merit'},
        'limits': ['No servicing policy estimator implemented in the canonical service',
                   'No general hidden-state, unknown-optimum, dependence or unbounded-reward inference',
                   'No new sampling study or coverage/useful-width acceptance; R03S negative review retained',
                   'No MCP requalification, foreign-language bridge, sibling execution or live model call',
                   'No authentic bank data, prices, independent acceptance or adoption',
                   'Restart replay is not process-kill, exactly-once or multi-host qualification']}
    write(journey.DESIGN, protocol)
    output = ref(journey.DESIGN, 'Reviewed servicing workflow and exact prospective local protocol')
    receipt = control.ledger.receipt_template(design)
    receipt.update(outcome='pass', execution='performed', reviewer=review['reviewer'],
        scope='Reviewed servicing chain, preserved negative scientific decisions and frozen 98-call local boundary screen',
        limitations=protocol['limits'], outputs=[output])
    for i, finding in enumerate([
        'Full decision/clock/target/information/sampling/identification/uncertainty/financial chain, failures and workflow cost categories are explicit and reviewed.',
        'Available local operations, arithmetic references, proposed consumer contracts and authentic owner evidence are separate; no adapter or sibling execution prerequisite.']):
        receipt['criteria'][i].update(verdict='pass', finding=finding, evidence=[output, review_ref, review['review']])
    write(base / 'design-receipt.json', receipt)
    print(json.dumps({'frozen_cases': len(cases), 'invocations': 98, 'protocol': output['path'], 'final_trial_run': False}))


if __name__ == '__main__':
    main()
