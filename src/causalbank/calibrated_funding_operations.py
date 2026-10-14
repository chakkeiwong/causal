"""Local request/report boundary for the two explicit V9 funding procedures."""
from dataclasses import asdict
import hashlib
import json
import numpy as np
from .funding_calibration import fit_funding, DECLARATIONS
from .funding_pilot_rates import fit_growing_pilot


def array_digest(rows):
    values = np.asarray(rows)
    digest = hashlib.sha256(json.dumps({'shape': values.shape, 'dtype': str(values.dtype)}).encode())
    for start in range(0, len(values), 4096):
        digest.update(np.ascontiguousarray(values[start:start+4096]).tobytes())
    return digest.hexdigest()


def run_request(method, rows, target, successes, sizes, *, pilot_rows=None,
                covariance='innovation_horizon', declarations=None, penalties=(0., 1., 10., 100.)):
    if method not in ('joint_ols', 'growing_pilot'):
        raise ValueError('Explicit supported funding method required')
    if method == 'growing_pilot' and pilot_rows is None:
        raise ValueError('Growing-pilot operation requires independent pilot histories')
    if method == 'joint_ols' and pilot_rows is not None:
        raise ValueError('Joint regression does not consume an external pilot')
    identity = dict(recipe='funding-calibration-v1', method=method, target=asdict(target),
        evaluation_sha256=array_digest(rows), audit_successes=list(successes), audit_sizes=list(sizes),
        pilot_sha256=array_digest(pilot_rows) if pilot_rows is not None else None,
        covariance=covariance, declarations=declarations,
        penalties=list(penalties) if method == 'growing_pilot' else None)
    key = hashlib.sha256(json.dumps(identity, sort_keys=True, allow_nan=False).encode()).hexdigest()
    if method == 'joint_ols':
        result = fit_funding(rows, target, successes, sizes, covariance=covariance, declarations=declarations)
        limitation = 'A retained 720-date synthetic comparison under-covers; this is conditional asymptotic inference, not general calibration.'
    else:
        result = fit_growing_pilot(pilot_rows, rows, target, successes, sizes, penalties,
            covariance=covariance, declarations=declarations)
        result.pop('coefficient', None)
        limitation = 'Independent invariant pilot history must grow at least fourfold; calibration evidence remains conditional and its extra acquisition is unpriced.'
    result['qualifications'].append(limitation)
    return dict(schema='funding-calibration-v1', request_identity=key, request=identity, result=result)


def treasury_report(envelope):
    result = envelope['result']
    available = result['status'] == 'computed'
    return dict(request_identity=envelope['request_identity'], status=result['status'],
        monetary_value=result.get('estimate') if available else None,
        monetary_interval=result.get('interval') if available else None,
        qualifications=list(result['qualifications']))


def analyst_report(envelope):
    result = envelope['result']
    available = result['status'] == 'computed'
    return dict(request_identity=envelope['request_identity'], method=envelope['request']['method'],
        status=result['status'], estimate=result.get('estimate') if available else None,
        standard_error=result.get('standard_error') if available else None,
        interval=result.get('interval') if available else None,
        audit_intervals=result['audit_intervals'], qualifications=list(result['qualifications']))
