#!/usr/bin/env python3
"""Freeze the reviewed observation journey before any final service call."""
import json
from pathlib import Path
import sys

import observations_journey_20261013 as journey
import run_program as control

ROOT, BASE = journey.ROOT, journey.BASE
ref, write = journey.ref, journey.write
sys.path.insert(0, str(ROOT / 'src'))
from causalbank.runtime_v12 import execution_identity


def main():
    assert not journey.DESIGN.exists() and not (BASE / 'local-journal.json').exists()
    s = control.core.read(ROOT, control.core.STATE)
    graph, _, _ = control.combined(ROOT, s)
    local = control.ledger.operation(graph, 'IN.JOURNEY.LOCAL.observations')
    design = control.ledger.operation(graph, 'IN.JOURNEY.DESIGN.observations')
    cases = json.loads((BASE / 'fixtures.json').read_text())['cases']
    preflight = json.loads((BASE / 'design-preflight.json').read_text())
    assert preflight['status'] == 'pass' and preflight['final_service_invocations'] == 0
    assert len(cases) == 26
    write(BASE / 'environment.json', execution_identity())
    inputs = [ROOT / 'tools' / n for n in ['observations_journey_20261013.py', 'observations_examples_20261013.py',
              'freeze_observations_journey_20261013.py', 'funding_journey_successor_20261013.py', 'discovery_journey_20261013.py']]
    inputs += [BASE / n for n in ['fixtures.json', 'exact-examples.json', 'design-preflight.json', 'environment.json', 'plan-review.md']]
    inputs += [ROOT / 'src/causalbank' / n for n in ['artifacts_v12.py', 'operation_contract_v12.py', 'operation_service_v12.py',
               'runtime_v12.py', 'worker_v12.py', 'cli_v12.py', 'mcp_server_v12.py', 'responses.py', 'causal_workflow.py']]
    inputs += [ROOT / 'docs/program/repair-v12/work/IN02' / n for n in ['request-schema.json', 'response-schema.json']]
    evidence = [ref(p, 'Frozen reviewed observation code, environment, schema or input') for p in inputs]
    review = {'operation_id': local['id'], 'design_approved': True, 'unresolved_design_blockers': [],
              'scope_matches_contract': True, 'retained_predecessor_failures': True,
              'reviewer': {'name': 'Codex author/coordinator', 'kind': 'author'},
              'review': ref(BASE / 'plan-review.md', 'Reviewed complete chain, independent references and exposed boundaries'),
              'execution_inputs': evidence,
              'pre_registration_repair': 'Draft recovery-amount variable replaced by a coherent binary-event/probability context before any final invocation; preserved draft remains available.',
              'scope': 'Deterministic boundary screen; no raw-data measurement correction, sampling coverage or bank validation'}
    write(BASE / 'argument-review.json', review)
    reviewed = ref(BASE / 'argument-review.json', 'Author approval of frozen observation design')
    protocol = {
        'operation_id': local['id'], 'operation_contract_sha256': control.core.digest_object(local),
        'target': 'Preserve origin, feature/outcome clock, inclusion and label uncertainty when framing a twelve-month contact decision.',
        'model': 'Authored finite sampling and bijective identity laws, two binary misclassification worlds, generic sensitivity polynomials and distinct supplied Gaussian summaries.',
        'observation_law': 'Generated feature and follow-up rows, missing/duplicate/false-label records, fixed summaries and exact source artifacts; no bank data or new random draws.',
        'sampling_unit': 'A request slot for runtime conformance. The proposed scientific unit is a borrower origin with household/map dependence; declared labels do not verify that law.',
        'method': '26 cases through library and CLI, initial and restarted invocation, then two changed-horizon conflicts; independently review complete responses and saved prefix identities.',
        'assumptions': ['Timestamps, identity, inclusion probabilities and label truth are separate declarations.',
                        'The binary label relation assumes the stated homogeneous sensitivity/false-positive law and target population.',
                        'Fitted audit uncertainty needs its own joint expansion and sampling law; the supplied moment service does not derive it.',
                        'Prevalence, measurement correction and intervention effect are distinct targets.'],
        'uncertainty_claim': 'Exact illustrative laws; deterministic sensitivity has no coverage level. Supplied Gaussian moments retain only their nominal conditional interpretation, with no finite-sample or general sampling guarantee.',
        'alternatives': ['Independent versus shared inclusion with identical marginals', 'Two bijective origin maps preserving totals',
                         'Accurate versus noisy labels; known versus unidentified measurement law',
                         'Fixed-nuisance versus full joint score covariance', 'Local library versus CLI/restart',
                         'Selected truth or positive point decision versus retained ambiguity and missing-information result'],
        'adverse_cases': [c['id'] for c in cases if c['id'] != 'clock_valid'],
        'metrics': ['106 planned slots with all errors, refusals, unsupported outputs and replays retained',
                    '26 complete-response parity comparisons excluding only request_id',
                    'Exact clock failure indices, row counts, evidence/context hashes, units and qualifications',
                    'Independent set topology/endpoints with absolute 1e-9 and relative 1e-10 tolerance',
                    'Invocation and active-runner wall time, separate parent/child high-water RSS'],
        'acceptance_rules': {'pass': 'All 106 slots and 26 semantic parity comparisons match the frozen scoped references.',
                             'negative': 'Retain any mismatch; do not repair expectations to fit observed behavior.',
                             'scientific_boundary': 'Passing conformance does not qualify identity/label truth, an empty audit, automatic audit-to-estimator gating or complete trustworthy-observation reconstruction.'},
        'replications': 1, 'seed': 26101309, 'seed_role': 'Fixture identity, no random sampling',
        'stopping_rule': 'fixed_design_no_outcome_stopping',
        'derivation_review': reviewed, 'successor_review': reviewed,
        'screen_operating_characteristics': 'No empirical coverage, power or false-acceptance estimate; finite authored boundary cases only.',
        'width_and_availability_rules': 'Empty, whole-line, disconnected and finite sets remain distinct. Physical prevalence bounds and decision mapping are separate proposed operations. Refusals are unavailable estimates; clock passes alone cannot admit effects.',
        'fresh_data_provenance': 'New deterministic cases and separate unused local operator roots. No bank or empirical held-out claim.',
        'execution_inputs': evidence, 'input_sha256': {x['path']: x['sha256'] for x in evidence},
        'fixtures': ref(BASE / 'fixtures.json', 'Frozen coherent contexts, artifact mutations and expected outcomes'),
        'invocation_count': 106,
        'decision_chain': {
            'business': 'Contact decision before twelve-month adverse event under a separately justified intervention model.',
            'clock': 'Feature event<=available<decision; follow-up outcome horizon/ascertainment/censoring separate.',
            'information': 'Origin maps, source/version/custody, selection and labeling declarations; retain rejections and alternatives.',
            'sampling': 'Borrower/household/map and audit dependence; marginal probabilities alone do not identify joint variance.',
            'identification': 'q=f+(s-f)p needs measurement information; equal reported laws can leave different prevalence and decisions.',
            'estimation': 'Proposed weighted measurement fit; present runtime only accepts supplied summaries and algebraic sensitivity.',
            'uncertainty': 'Joint score includes nuisance and cross terms; invert a justified joint region near singular measurement laws.',
            'decision': 'Retain full feasible values and resolve consequential ambiguity before deployment; no automated consumer gate claimed.'},
        'cost_accounting': {'measured': 'All invocation/replay/failure wall time plus active runner import/journaling and process high-water RSS.',
             'excluded_from_timing': 'Inter-segment idle time, initial interpreter startup, author/review time and unexecuted activities.',
             'unknown_prices': ['source acquisition/rights', 'identity and audit adjudication', 'nuisance fitting', 'integration',
                                'scientific review', 'storage', 'monitoring/recovery', 'failed work', 'optional live models', 'bank validation'],
             'scenario_only': 'USD 1000 event loss, USD 200 contact cost, stipulated one-half prevention conditional on baseline event; not an estimated causal efficacy or bank ROI.'},
        'evidence_classes': {'local_execution': 'Registered library/CLI artifact, clock, qualifier and replay screen',
             'independent_reference': 'Exact finite-law enumeration, label relation, polynomials and illustrative value calculations',
             'contract_double': 'Proposed consumer nonempty/relevant-audit and remaining-assumption policy; not run here',
             'authentic_owner_run': 'Later owned population/history/inclusion and independent label evidence, when prototype merit justifies expense'},
        'limits': ['No bank, sibling, live-model or foreign-engine execution', 'No raw-data measurement estimation or truthful-origin/label qualification',
                   'No automatic observation-audit prerequisite enforcement', 'No empirical coverage or financial-decision qualification',
                   'Restart replay is not exactly-once, process-kill or multi-host recovery qualification']}
    write(journey.DESIGN, protocol)
    output = ref(journey.DESIGN, 'Frozen reviewed observation workflow and prospective local screen')
    receipt = control.ledger.receipt_template(design)
    receipt.update(outcome='pass', execution='performed', reviewer=review['reviewer'],
                   scope='Complete observation workflow design and 26 fixed local cases; final runtime trial requires separate registration',
                   limitations=protocol['limits'], outputs=[output])
    for i, finding in enumerate([
        'Clock, target, identity/selection/label law, joint uncertainty, decision mapping, all failures and full workflow cost categories are declared and reviewed.',
        'Local fixed methods have independent references and schema preflight; consumer doubles and authentic owner evidence remain separate. No sibling or unavailable adapter is required.']):
        receipt['criteria'][i].update(verdict='pass', finding=finding, evidence=[output, reviewed, ref(BASE / 'plan-review.md', 'Detailed author review')])
    write(BASE / 'design-receipt.json', receipt)
    print(json.dumps({'frozen_cases': 26, 'invocations': 106, 'protocol': output['path'], 'final_trial_executed': False}))


if __name__ == '__main__':
    main()
