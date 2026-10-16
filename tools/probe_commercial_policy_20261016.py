#!/usr/bin/env python3
"""Bounded actual local capability observations, with no vendor calls."""
import json
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'src'), str(ROOT/'tests')]
from causalbank.operation_service_v12 import OperationService, REQUEST_SCHEMA
from test_operation_service_v12 import context, request
from publish_latent_r_review_v2_20261013 import ref, write


def main():
    with tempfile.TemporaryDirectory(prefix='commercial-policy-', dir=ROOT/'.runtime') as tmp:
        service = OperationService(Path(tmp)); observations = []
        cap_request = request('capabilities.describe', {}, ctx=None)
        capabilities = service.invoke(cap_request)
        for method in ['fixed-history-policy', 'learned-policy-validation', 'static-assignment-value']:
            req = request('estimate.effect', {'engine_id': 'proposed-policy-reference', 'estimator_id': method}, ctx=context())
            res = service.invoke(req)
            assert res['disposition'] == 'unsupported' and res['result'] is None
            observations.append({'request': req, 'response': res})
    write(ROOT/'docs/program/execution/2026-10-16/commercial-policy/local-probe.json', {
        'status': 'observed', 'scope': 'Actual local reference dispatcher; no vendor, policy learner or history evaluator executed.',
        'capability_request': cap_request, 'capability_response': capabilities,
        'operation_enum': REQUEST_SCHEMA['properties']['operation']['enum'], 'policy_method_probes': observations,
        'evidence': [ref(ROOT/'src/causalbank/operation_service_v12.py', 'SUPPORTED, _capabilities and _estimate guard'),
                     ref(ROOT/'tests/test_operation_service_v12.py', 'Valid request/context constructors'),
                     ref(Path(__file__), 'Three schema-valid proposed method identifiers')],
        'limits': ['These three refusal observations do not establish that the repository has no policy research modules.',
                   'Source-inspected history_inference.py and controlled.py remain distinct from this common service.']})
    print(json.dumps({'local_policy_method_probes': 3, 'disposition': 'unsupported', 'vendor_execution': False}))


if __name__ == '__main__':
    main()
