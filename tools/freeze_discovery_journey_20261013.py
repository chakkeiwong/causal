#!/usr/bin/env python3
"""Write the reviewed discovery protocol before any final service invocation."""
import json
from pathlib import Path
import sys

import run_program as control
import discovery_journey_20261013 as journey

ROOT, BASE = journey.ROOT, journey.BASE
sys.path.insert(0, str(ROOT / 'src'))
from causalbank.runtime_v12 import execution_identity
from causalbank.artifacts_v12 import ArtifactStore


def main():
    assert not journey.DESIGN.exists(), 'Protocol already frozen'
    assert not (BASE / 'local-journal.json').exists(), 'Final trial already started'
    ref, write = journey.ref, journey.write
    state = control.core.read(ROOT, control.core.STATE)
    graph, _, _ = control.combined(ROOT, state)
    local = control.ledger.operation(graph, 'IN.JOURNEY.LOCAL.discovery')
    design = control.ledger.operation(graph, 'IN.JOURNEY.DESIGN.discovery')
    cases = json.loads((BASE / 'fixtures.json').read_text())['cases']
    store = ArtifactStore(ROOT / '.runtime/discovery-draft-reimport-review')
    value = {'review_only': 'draft_reimport', 'value': 1}
    descriptor = store.put(value, 'review/1', 'review_only')
    (store.folder / (descriptor['artifact_id'] + '.json')).write_text('{}')
    try:
        store.put(value, 'review/1', 'review_only')
        raise AssertionError('Expected the saved draft reimport failure')
    except ValueError as exc:
        write(BASE / 'draft-defect-reproduction.json', {
            'observed_exception': type(exc).__name__, 'message': str(exc),
            'scope': 'Artifact-store-only reproduction; no final workflow invocation',
            'repair': 'Persist the reference before fault injection, and reuse it on restart',
            'original_runner': ref(BASE / 'recovered-draft/discovery_journey_20261013.py',
                                   'run loop called store.put for each phase')})
    write(BASE / 'environment.json', execution_identity())
    inputs = [ROOT / 'tools/discovery_journey_20261013.py', Path(__file__),
              BASE / 'fixtures.json', BASE / 'design-preflight.json', BASE / 'environment.json']
    inputs += [ROOT / 'src/causalbank' / p for p in
               ['artifacts_v12.py', 'operation_contract_v12.py', 'operation_service_v12.py',
                'runtime_v12.py', 'worker_v12.py', 'cli_v12.py', 'mcp_server_v12.py',
                'responses.py', 'causal_workflow.py']]
    inputs += [ROOT / 'docs/program/repair-v12/work/IN02' / p for p in
               ['request-schema.json', 'response-schema.json']]
    evidence = [ref(p, 'Frozen inspected fixture, environment, source or schema') for p in inputs]
    review = {
        'operation_id': local['id'], 'design_approved': True,
        'unresolved_design_blockers': [], 'scope_matches_contract': True,
        'retained_predecessor_failures': True, 'reviewer': {'name': 'Codex author', 'kind': 'author'},
        'review': ref(BASE / 'plan-review.md', 'Steps, independent references, defect repair and claim boundaries'),
        'preflight': ref(BASE / 'design-preflight.json', '23 valid declarations and one intentional cycle'),
        'observed_draft_defect': ref(BASE / 'draft-defect-reproduction.json', 'Second import of corrupted bytes fails'),
        'execution_inputs': evidence,
        'scope': 'Prospective deterministic boundary and restart screen; no discovery-performance or coverage claim'}
    write(BASE / 'argument-review.json', review)
    review_ref = ref(BASE / 'argument-review.json', 'Author review approves the exact design within its boundary')
    protocol = {
        'operation_id': local['id'], 'operation_contract_sha256': control.core.digest_object(local),
        'target': 'Preserve the meaning and refusals of a twelve-month offer effect in USD through fixed local operations.',
        'model': 'Authored DAG, CPDAG/PAG endpoint declarations, moment/artifact failures and elementary quadratic sets.',
        'observation_law': 'Deterministic generated declarations and four timestamp rows; no observational or experimental bank sample.',
        'sampling_unit': 'A fixed request; accounts are the declared scientific unit, dependent months an explicit unsupported case.',
        'method': 'Run all 24 frozen cases via library and CLI, each initially and after re-instantiation/restart, plus two same-key horizon conflicts.',
        'assumptions': ['Supplied graph and causal premises are unverified declarations.',
                        'Finite authored inputs cover only their specified boundary; no general method validity is inferred.',
                        'Fresh operator stores isolate trial state from historical demonstrations.'],
        'uncertainty_claim': 'No new sampling-confidence claim. Preserve qualification and deterministic set topology; do not relabel sensitivity as confidence.',
        'alternatives': ['Analytic graph/path and inequality references', 'Library versus CLI on identical inputs',
                         'Replay versus first execution', 'Explicit unsupported/refused result versus invented point answer'],
        'adverse_cases': [c['id'] for c in cases if c['expected'].get('disposition') in ['unsupported', 'refused', 'unavailable']
                          or 'invocation_error' in c['expected']],
        'metrics': ['all-request expectation agreement', 'semantic parity excluding only request_id',
                    'graph marks, adjustments, set endpoints, qualifiers, hashes, errors and CLI exits',
                    'invocation/active-runner wall time and process high-water RSS'],
        'acceptance_rules': {'pass': 'All 98 slots match frozen expectations and all 24 parity comparisons pass.',
                             'negative': 'Any mismatch; retain full request and response and review the failed boundary.',
                             'execution_failure': 'Checkpoint environmental obstruction; do not omit requests or redraw fixtures.'},
        'replications': 1, 'seed': 26101307, 'seed_role': 'Version identity only; no random draws',
        'stopping_rule': 'fixed_design_no_outcome_stopping',
        'derivation_review': review_ref, 'successor_review': review_ref,
        'screen_operating_characteristics': 'Deterministic conformance on 98 authored slots; no confidence level, power or general false-accept rate.',
        'width_and_availability_rules': 'Retain disconnected/unbounded/empty/singleton outputs. Correct refusals pass conformance but do not count as available effect estimates.',
        'fresh_data_provenance': 'New frozen boundary suite, deterministic authored data, new isolated operator roots; no held-out empirical-performance claim.',
        'execution_inputs': evidence,
        'input_sha256': {x['path']: x['sha256'] for x in evidence},
        'fixtures': ref(BASE / 'fixtures.json', 'All exact contexts, input bodies and expected outputs'),
        'invocation_count': len(cases) * 4 + 2,
        'decision_chain': {
            'business': 'Whether an offer should be proposed for eligible accounts over twelve months',
            'clock': 'event <= available < decision; keep leakage and missing-clock failures',
            'information': 'Declared variables, endpoint marks, causal premises and immutable artifact provenance',
            'identification': 'Selected supplied-DAG back-door route; ambiguous/latent/dependent cases keep their limited dispositions',
            'estimation': 'No full raw-data discovery-to-estimation path is installed by this study; supplied-moment failures test context/custody',
            'uncertainty': 'Preserve class ambiguity and deterministic sensitivity topology; statistical effect calibration remains separate',
            'numerical': 'Independent exact factorizations on four small quadratic cases; no certified general outer-bound solver',
            'financial': 'A conditional expression is not a dollar estimate. Without justified identified uncertainty and costs, hold the action for investigation'},
        'cost_accounting': {
            'measured': 'All invocation time including failed requests/replay and process startup; active runner time including imports into the store and journaling; parent and child RSS maxima',
            'excluded': 'Time between segments, initial interpreter/module startup, simultaneous process-tree memory, author effort and subsequent manuscript/review',
            'unmeasured_workflow': ['data procurement and cleaning', 'graph elicitation/adjudication', 'adapter implementation',
                                    'live-model calls', 'independent review', 'deployment and ongoing operations'],
            'money': 'No price or bank ROI assertion; local measurements are inputs to later scenarios'},
        'evidence_classes': {
            'local_execution': 'This registered library/CLI trial',
            'independent_reference': 'Analytic path blocking, factorization, timestamp ordering and exact context change',
            'contract_double': 'Proposed consumer handling only, not executed here and never an accepted sibling integration',
            'authentic_owner_run': 'Later accepted request/map/clock plus owner trace, fault results and signed disposition; optional for this proposal'},
        'limits': ['No discovery engine installed', 'No live LLM calls', 'No actual sibling execution',
                   'No general PAG/temporal identification or confidence guarantee',
                   'Restart replay is not process-kill, multi-host, or exactly-once crash qualification']}
    write(journey.DESIGN, protocol)
    output = ref(journey.DESIGN, 'Reviewed complete workflow protocol and frozen local trial')
    receipt = control.ledger.receipt_template(design)
    receipt.update(outcome='pass', execution='performed',
                   scope='Reviewed 24-case discovery workflow design; runtime execution is a separate registered operation',
                   reviewer={'name': 'Codex author', 'kind': 'author'}, limitations=protocol['limits'], outputs=[output])
    for i, finding in enumerate([
        'The protocol develops clock, target, information, sampling, identification, uncertainty, decision and full cost categories with all failures retained.',
        'The 24 fixed cases use only the available local service and analytic references; contract doubles and authentic owner cases are separately specified without any sibling execution.']):
        receipt['criteria'][i].update(verdict='pass', finding=finding,
                                      evidence=[output, review_ref, ref(BASE / 'plan-review.md', 'Reviewed assumptions, alternatives and exact execution steps')])
    write(BASE / 'design-receipt.json', receipt)
    print(json.dumps({'frozen_cases': len(cases), 'invocations': protocol['invocation_count'],
                      'protocol': output['path'], 'final_trial_run': False}))


if __name__ == '__main__':
    main()
