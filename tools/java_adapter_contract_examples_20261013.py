#!/usr/bin/env python3
"""Validate illustrative wire records against the inherited schema and semantics."""
import copy
import hashlib
import json
from pathlib import Path
import sys

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from causalbank.operation_contract_v12 import context_digest, validate_response

BASE = ROOT / 'docs/program/execution/2026-10-13/java-integration'
SCHEMAS = ROOT / 'docs/program/repair-v12/work/IN02'


def artifact(path, identifier, role, schema):
    raw = path.read_bytes()
    return {'artifact_id': identifier, 'sha256': hashlib.sha256(raw).hexdigest(),
            'media_type': 'application/json', 'schema_version': schema,
            'role': role, 'bytes': len(raw), 'custody': 'local_project_reference'}


def main():
    request_schema = json.loads((SCHEMAS / 'request-schema.json').read_text())
    response_schema = json.loads((SCHEMAS / 'response-schema.json').read_text())
    context = {
        'target': {'kind': 'effect_contrast', 'outcome': 'Z', 'treatment': 'X',
                   'contrast': 'one standardized unit increase; retained context, not computed'},
        'population': {'definition': 'Project illustration of eligible funding accounts', 'unit': 'account'},
        'variables': [{'id': x, 'role': role, 'unit': 'standardized'} for x, role in
                      [('X', 'action'), ('Y', 'covariate'), ('Z', 'outcome')]],
        'intervention': {'kind': 'fixed_action', 'value': 'X increases by one standardized unit'},
        'horizon': {'value': 12, 'unit': 'months'}, 'units': ['standardized'],
        'sign_convention': 'higher-minus-lower-X',
        'observation_clock': {'event_time': 'event_at', 'available_time': 'available_at',
                              'decision_time': 'decision_at', 'rule': 'strict_before_decision',
                              'alternative_justification': None},
        'sampling': {'law': 'iid_gaussian_accounts', 'unit': 'account', 'fold_unit': 'account'},
        'assumptions': [{'id': name, 'statement': name, 'status': 'unverified', 'evidence': []}
                        for name in ['acyclicity', 'sufficiency', 'faithfulness', 'IID_Gaussian', 'no_selection']],
        'graph': None, 'source_evidence': []}
    toy = {'kind': 'deterministic_wire_fixture_not_a_statistical_sample', 'columns': ['X', 'Y', 'Z'],
           'rows': [[-2, 1, 0], [-1, -1, 1], [0, 2, 2], [1, 0, -1], [2, 1, 3], [3, -2, 1]],
           'warning': 'No fitted graph or IID sampling validity is claimed for this fixed interface fixture.'}
    (BASE / 'wire-input.json').write_text(json.dumps(toy, indent=2) + '\n')
    config = {'schema_version': 'causalbank.tetrad-config/1.0.0',
              'engine_commit': 'b89afaf952a4fd647df0d85b08102250106c6764',
              'adapter_version': '1.0.0', 'alpha': .05, 'depth': -1,
              'stable': True, 'knowledge': [], 'missing': 'FAIL',
              'shrinkage': 'NONE', 'ridge': 0, 'pseudoinverse': False}
    (BASE / 'wire-configuration.json').write_text(json.dumps(config, indent=2) + '\n')
    request = {'schema_version': 'causalbank.request/1.0.0', 'request_id': 'java-design-example',
               'operation': 'graph.discover',
               'artifact_inputs': [artifact(BASE / 'wire-input.json', 'java-wire-input', 'data', 'project-wire-fixture/1'),
                                   artifact(BASE / 'wire-configuration.json', 'java-wire-config', 'engine_configuration',
                                            'causalbank.tetrad-config/1.0.0')],
               'budget': {'wall_seconds': 20, 'memory_bytes': 1073741824, 'max_output_bytes': 1000000, 'model_calls': 0},
               'parameters': {'algorithm_id': 'tetrad.pc.fisher_z',
                              'algorithm_version': 'b89afaf952a4fd647df0d85b08102250106c6764/adapter-1.0.0'},
               'scientific_context': context, 'idempotency_key': 'java-design-example'}
    graph = {'kind': 'CPDAG', 'nodes': ['X', 'Y', 'Z'],
             'edges': [{'left_node': a, 'right_node': b, 'left_mark': 'tail', 'right_mark': 'tail',
                        'evidence_type': 'assumption', 'evidence_refs': [], 'review_status': 'project_oracle_only'}
                       for a, b in [('X', 'Y'), ('Y', 'Z')]],
             'basis': 'Independent Gaussian population reference; not fitted from wire-input and not a Tetrad result'}
    (BASE / 'wire-graph-reference.json').write_text(json.dumps(graph, indent=2) + '\n')
    notes = {'scope': 'Illustrative response vocabulary; all engine paths remain unexecuted',
             'engine_not_admitted': ['Java environment', 'failure-transparent wrapper', 'graph-class recognizer'],
             'unsupported_alternative': 'Retain repeated account identifiers and use a reviewed panel/temporal profile.',
             'hypothetical_failure': 'A singular conditional covariance must withhold graph publication.'}
    (BASE / 'wire-dispositions.json').write_text(json.dumps(notes, indent=2) + '\n')
    evidence = [artifact(BASE / 'wire-dispositions.json', 'java-wire-dispositions', 'design_evidence', 'project-design/1')]
    response = {'schema_version': 'causalbank.response/1.0.0', 'request_id': request['request_id'],
                'operation': request['operation'], 'status': 'completed', 'disposition': 'unavailable',
                'context_sha256': context_digest(context), 'result': None, 'error': None,
                'evidence': evidence, 'qualification': {'level': 'none', 'evidence': []}}
    cases = [{'label': 'Current design runtime unavailable; no Java attempt', 'request': request, 'response': response}]
    q, r = copy.deepcopy(request), copy.deepcopy(response)
    q['scientific_context']['sampling']['law'] = 'clustered_account_months'
    r.update(disposition='unsupported', context_sha256=context_digest(q['scientific_context']))
    cases.append({'label': 'Hypothetical scoped refusal for dependent data', 'request': q, 'response': r})
    q, r = copy.deepcopy(request), copy.deepcopy(response)
    r.update(status='failed', error={'code': 'CI_NUMERICAL_FAILURE', 'message': 'Illustrative singular covariance; no engine was run.', 'retryable': False})
    cases.append({'label': 'Hypothetical failed invocation with no scientific result', 'request': q, 'response': r})
    q, r = copy.deepcopy(request), copy.deepcopy(response)
    r.update(disposition='computed', result={'kind': 'graph', 'estimate': None, 'coordinate_sets': None,
               'units': [], 'uncertainty': None, 'payload': {'graph_artifact': artifact(BASE / 'wire-graph-reference.json',
                   'java-wire-graph', 'graph_reference', 'project-graph/1')}}, qualification={'level': 'none', 'evidence': []})
    cases.append({'label': 'Illustrative graph response from independent oracle only; not fitted from request', 'request': q, 'response': r})
    for case in cases:
        jsonschema.validate(case['request'], request_schema)
        jsonschema.validate(case['response'], response_schema)
        validate_response(case['request'], case['response'])
    bad = copy.deepcopy(cases[0]);bad['request']['scientific_context']['units'] = ['USD']
    try:
        validate_response(bad['request'], bad['response'])
    except ValueError as exc:
        rejected = str(exc)
    else:
        raise AssertionError('stale scientific identity accepted')
    out = {'status': 'pass', 'kind': 'schema_and_reference_semantic_validation', 'java_executed': False,
           'cases': cases, 'mutation_rejection': rejected,
           'limits': ['These examples validate structure and declared meanings only.',
                      'The generic validator does not enforce every Java admission condition or recognize arbitrary CPDAGs.',
                      'No runtime results or transport interoperability measured.']}
    (BASE / 'wire-examples.json').write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps({'status': 'pass', 'validated_records': len(cases), 'stale_identity_rejected': True, 'java_executed': False}))


if __name__ == '__main__':
    main()
