#!/usr/bin/env python3
"""Validate proposed scientific envelopes; no identification/estimation engine."""
from copy import deepcopy
import hashlib
import json
import math
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'contracts/scientific'
EXAMPLES = BASE / 'examples'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def artifact(record, role=None):
    path = (ROOT / record['path']).resolve()
    if not path.is_relative_to(ROOT) or not path.is_file():
        raise ValueError('Artifact is missing or outside the workspace')
    if digest(path) != record['sha256']:
        raise ValueError('Artifact bytes differ from their declared hash')
    if role is not None and record['role'] != role:
        raise ValueError('Artifact has the wrong scientific role')


def finite_numbers(value):
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError('JSON numerical values must be finite; infinity uses null endpoints')
    if isinstance(value, dict):
        for v in value.values():
            finite_numbers(v)
    if isinstance(value, list):
        for v in value:
            finite_numbers(v)


def validate(request, result, request_path):
    for kind, record in [('request', request), ('result', result)]:
        finite_numbers(record)
        schema = json.loads((BASE / (kind + '.schema.json')).read_text())
        Draft202012Validator.check_schema(schema)
        Draft202012Validator(schema).validate(record)
    if json.loads(request_path.read_text()) != request:
        raise ValueError('Request object differs from bound request file')
    if result['request_sha256'] != digest(request_path):
        raise ValueError('Result has a stale request hash')
    for key in ('request_id', 'operation'):
        if request[key] != result[key]:
            raise ValueError('Result/request mismatch: ' + key)
    for key in ('model', 'observation', 'target', 'sampling'):
        artifact(request[key], key + '_specification')
    identification = result['identification']
    roles = {'identified_functional': 'functional_derivation',
             'identified_set': 'identified_set_derivation',
             'outer_bound': 'outer_bound_derivation',
             'not_identified': 'nonidentification_witness',
             'incompatible_specification': 'contradiction'}
    status = identification['status']
    if status in roles:
        if not identification['assumptions'] or identification['evidence'] is None:
            raise ValueError('Scientific conclusion needs assumptions and explicit evidence')
        artifact(identification['evidence'], roles[status])
    elif identification['evidence'] is not None:
        raise ValueError('Unresolved identification must not carry a conclusion artifact')
    computation = result['computation']['status']
    if result['estimate'] is not None and (status != 'identified_functional' or computation != 'completed'):
        raise ValueError('A point estimate needs an identified functional and completed estimation')
    inference = result['inference']
    requested = request['inference_request']
    if (requested == 'none') != (inference['status'] == 'not_requested'):
        raise ValueError('Inference request and inference state disagree')
    if inference['status'] != 'available':
        if inference['object'] is not None or inference['evidence'] is not None:
            raise ValueError('Unavailable inference must not return an uncertainty object')
        return
    if computation != 'completed' or status not in ('identified_functional', 'identified_set', 'outer_bound'):
        raise ValueError('Available inference requires completed computation and a defined target/set')
    uncertainty = inference['object']
    if uncertainty is None or inference['evidence'] is None:
        raise ValueError('Available inference needs an uncertainty object and inference contract')
    artifact(inference['evidence'], 'inference_contract')
    if uncertainty['kind'] != requested:
        raise ValueError('Confidence and posterior credible sets cannot be interchanged')
    previous = None
    for interval in uncertainty['set']:
        lo, hi = interval['lower'], interval['upper']
        lc, uc = interval['lower_closed'], interval['upper_closed']
        if (lo is None and lc) or (hi is None and uc):
            raise ValueError('Infinite endpoints must be open')
        lower = -math.inf if lo is None else lo
        upper = math.inf if hi is None else hi
        if lower > upper or (lower == upper and not (lc and uc)):
            raise ValueError('Reversed or empty interval component')
        if previous is not None:
            end, end_closed = previous
            if lower < end or (lower == end and (lc or end_closed)):
                raise ValueError('Set components must be ordered and canonically disjoint')
        previous = upper, uc


def save(name, value):
    path = EXAMPLES / name
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')
    return path


def ref(path, role):
    return {'path': str(path.relative_to(ROOT)), 'sha256': digest(path), 'role': role}


def main():
    EXAMPLES.mkdir(parents=True, exist_ok=True)
    specifications = {
        'model': {'assumptions': ['binary encouragement exogeneity', 'exclusion', 'monotonicity'],
                  'scope': 'Schematic IV/compliance model; full machine-readable mathematical language is not implemented'},
        'observation': {'clock': 'baseline X, invitation Z, receipt A, then outcome Y', 'information': 'observed X,Z,A,Y'},
        'target': {'functional': 'declared complier outcome contrast', 'population': 'eligible customers', 'unit': 'USD/customer'},
        'sampling': {'independent_unit': 'customer', 'dependence': 'independent trajectories in this fixture'},
    }
    request = {'schema_version': '0.3.0-proposal', 'request_id': 'illustrative_iv_request',
               'operation': 'encouragement_iv', 'inference_request': 'confidence_set'}
    for key, value in specifications.items():
        request[key] = ref(save(key + '.json', value), key + '_specification')
    request_path = save('request.json', request)
    proof = save('scientific-evidence.json', {
        'scope': 'Protocol fixture only. No estimator, general proof checker or confidence procedure is executed.',
        'functional_derivation': 'Wald ratio under the declared binary-compliance assumptions; see monograph chapter 2.',
        'nonidentification_witness': 'ATE is not determined by unrestricted always/never-taker responses; chapter 2 gives an exact witness.',
        'outer_bound_derivation': 'An enclosing graph-compatible target interval need not be sharp; see chapter 10.',
        'inference_contract': 'Two illustrative rays preserve weak-ratio set topology; coverage is not asserted.'})
    base = {'schema_version': '0.3.0-proposal', 'request_id': request['request_id'],
            'request_sha256': digest(request_path), 'operation': request['operation'],
            'computation': {'status': 'completed', 'reason': 'Protocol fixture, no scientific backend executed'},
            'identification': {'status': 'identified_functional', 'assumptions': ['exogeneity', 'exclusion', 'monotonicity', 'nonzero first stage'],
                               'reason': 'Illustrative conditional functional', 'evidence': ref(proof, 'functional_derivation')},
            'estimate': None,
            'inference': {'status': 'available', 'reason': 'Schematic set topology, no coverage claim',
                          'evidence': ref(proof, 'inference_contract'),
                          'object': {'kind': 'confidence_set', 'level': .95, 'coverage_target': 'scalar_target',
                                     'method': 'illustrative weak-ratio test inversion',
                                     'set': [{'lower': None, 'upper': -2, 'lower_closed': False, 'upper_closed': True},
                                             {'lower': 3, 'upper': None, 'lower_closed': True, 'upper_closed': False}]}},
            'evidence_class': 'schema_fixture'}
    cases = {'disconnected_unbounded': (request, base, request_path)}
    def add(name, fn, change_request=None):
        req, res = deepcopy(request), deepcopy(base)
        if change_request:
            change_request(req)
        req['request_id'] = name
        reqpath = save(name + '-request.json', req)
        res.update(request_id=name, request_sha256=digest(reqpath), operation=req['operation'])
        fn(res)
        cases[name] = req, res, reqpath
    unavailable = {'status': 'unavailable', 'reason': 'No numerical inference requested from an executed backend', 'object': None, 'evidence': None}
    add('identified_only', lambda x: x.update(inference={**unavailable, 'status': 'not_requested'}),
        lambda x: x.update(inference_request='none'))
    add('timeout', lambda x: x.update(computation={'status': 'timeout', 'reason': 'Estimation budget exhausted after identification'}, inference=deepcopy(unavailable)))
    add('unsupported', lambda x: x.update(computation={'status': 'unsupported', 'reason': 'No estimator for identified functional'}, inference=deepcopy(unavailable)))
    ate = ref(save('ate-target.json', {'functional': 'ATE in eligible population', 'unit': 'USD/customer'}), 'target_specification')
    add('nonidentification', lambda x: x.update(identification={**x['identification'], 'status': 'not_identified', 'reason': 'Unrestricted compliance types leave ATE ambiguous', 'evidence': ref(proof, 'nonidentification_witness')}, inference=deepcopy(unavailable)), lambda x: x.update(target=ate))
    graph_target = ref(save('graph-target.json', {'functional': 'effect over a graph equivalence class', 'scope': 'schematic outer bound'}), 'target_specification')
    graph_model = ref(save('graph-model.json', {'graph_class': 'CPDAG', 'edges': ['A-M', 'M-Y'], 'restrictions': ['linear Gaussian SCM', 'causal sufficiency']}), 'model_specification')
    graph_observation = ref(save('graph-observation.json', {'observed': ['A', 'M', 'Y'], 'clock': 'single occasion; orientation unresolved'}), 'observation_specification')
    add('outer_bound', lambda x: x.update(identification={**x['identification'], 'status': 'outer_bound', 'assumptions': ['linear Gaussian SCM', 'causal sufficiency'], 'reason': 'Schematic enclosing set, no sharpness assertion', 'evidence': ref(proof, 'outer_bound_derivation')}, inference=deepcopy(unavailable)), lambda x: x.update(operation='discovery_query', target=graph_target, model=graph_model, observation=graph_observation))
    add('empty_confidence_set', lambda x: x['inference']['object'].update(set=[]))
    add('whole_line', lambda x: x['inference']['object'].update(set=[{'lower': None, 'upper': None, 'lower_closed': False, 'upper_closed': False}]))
    outcomes = []
    for name, (req, res, reqpath) in cases.items():
        validate(req, res, reqpath)
        save(name + '-result.json', res)
        outcomes.append({'case': name, 'status': 'pass'})
    mutations = [
        ('stale_request', lambda x: x.update(request_sha256='0' * 64)),
        ('wrong_operation', lambda x: x.update(operation='adjusted_mean')),
        ('changed_evidence', lambda x: x['identification']['evidence'].update(sha256='0' * 64)),
        ('missing_derivation', lambda x: x['identification'].update(evidence=None)),
        ('unproved_nonidentification', lambda x: x['identification'].update(status='not_identified')),
        ('timeout_with_inference', lambda x: x['computation'].update(status='timeout')),
        ('reversed_endpoint', lambda x: x['inference']['object']['set'][0].update(lower=1, upper=-2)),
        ('closed_infinity', lambda x: x['inference']['object']['set'][0].update(lower_closed=True)),
        ('overlapping_rays', lambda x: x['inference']['object']['set'][1].update(lower=-3)),
        ('posterior_substitution', lambda x: x['inference']['object'].update(kind='posterior_credible_set')),
        ('missing_uncertainty', lambda x: x['inference'].update(object=None)),
        ('nonfinite_number', lambda x: x.update(estimate=float('nan'))),
        ('unresolved_point', lambda x: x.update(estimate=1, identification={'status': 'unresolved', 'assumptions': [], 'reason': 'Search stopped', 'evidence': None})),
    ]
    for name, mutate in mutations:
        candidate = deepcopy(base)
        mutate(candidate)
        try:
            validate(request, candidate, request_path)
        except (ValueError, ValidationError) as error:
            outcomes.append({'case': name, 'status': 'rejected_as_expected', 'reason': str(error)[:300]})
        else:
            raise AssertionError('Accepted invalid contract: ' + name)
    inputs = [Path(__file__).resolve()] + sorted(BASE.rglob('*.json'))
    receipt = {'status': 'pass', 'valid_cases': len(cases), 'invalid_rejected': len(mutations), 'cases': outcomes,
               'input_sha256': {str(p.relative_to(ROOT)): digest(p) for p in inputs},
               'scope': 'Proposed schemas and selected semantic invariants; all fixtures are schematic, no causal engine or backend qualification.'}
    (ROOT / 'docs/reviews/scientific-contract-checks.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({k: receipt[k] for k in ('status', 'valid_cases', 'invalid_rejected', 'scope')}, indent=2))


if __name__ == '__main__':
    main()
