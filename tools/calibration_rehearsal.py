#!/usr/bin/env python3
"""Exercise V9 local request identities, consumer qualifications and refusals."""
import json
import numpy as np
from threadpoolctl import threadpool_limits
from calibration_common import ROOT, SPEC, save
from causalbank.dynamic_funding import FundingTarget
from causalbank.funding_calibration import simulate_rows, DECLARATIONS
from causalbank.calibrated_funding_operations import run_request, treasury_report, analyst_report


def main():
    s = json.loads((ROOT/SPEC).read_text())
    base = json.loads((ROOT/s['base']).read_text())
    obs = json.loads((ROOT/s['observation']).read_text())
    target = FundingTarget(horizon=base['horizon'], branches=base['branches'])
    rows, pilot = simulate_rows(base, obs, 720, 911313), simulate_rows(base, obs, 2880, 911317)
    cases = []
    for method in ('joint_ols', 'growing_pilot'):
        kwargs = dict(pilot_rows=pilot if method == 'growing_pilot' else None, declarations=DECLARATIONS)
        for name, counts in [('regular', [950, 800]), ('weak_rank', [500, 500]), ('audit_boundary', [1000, 800])]:
            result = run_request(method, rows, target, counts, [1000, 1000], **kwargs)
            wire = json.loads(json.dumps(result, allow_nan=False))
            assert wire == result
            treasury, analyst = treasury_report(wire), analyst_report(wire)
            assert treasury['status'] == analyst['status'] == result['result']['status']
            assert treasury['qualifications'] == analyst['qualifications'] == result['result']['qualifications']
            assert treasury['request_identity'] == analyst['request_identity'] == result['request_identity']
            if name == 'regular':
                assert treasury['status'] == 'computed'
                assert treasury['monetary_interval'] == analyst['interval']
            else:
                assert treasury['monetary_value'] is analyst['estimate'] is analyst['interval'] is None
            cases.append(dict(method=method, case=name, envelope=wire, treasury=treasury, analyst=analyst))
    first = run_request('joint_ols', rows, target, [950, 800], [1000, 1000], declarations=DECLARATIONS)
    changed = rows.copy();changed[0, 5] += .01
    second = run_request('joint_ols', changed, target, [950, 800], [1000, 1000], declarations=DECLARATIONS)
    assert first['request_identity'] != second['request_identity']
    violations = []
    for method, prior, declarations in [('automatic_best', None, DECLARATIONS), ('growing_pilot', None, DECLARATIONS),
        ('joint_ols', pilot, DECLARATIONS), ('joint_ols', None, None)]:
        try:
            run_request(method, rows, target, [950, 800], [1000, 1000], pilot_rows=prior, declarations=declarations)
        except ValueError as error:
            violations.append(str(error))
    assert len(violations) == 4
    result = dict(status='pass', cases=cases, changed_input_identity=True, rejected_requests=violations,
        scope='Two author-owned local consumers preserve method, uncertainty, unavailable status and qualifications. Not accepted external interfaces or bank adoption.')
    save('docs/reviews/calibration-local-rehearsal.json', result, [SPEC, 'tools/calibration_rehearsal.py',
        'src/causalbank/calibrated_funding_operations.py', 'src/causalbank/funding_pilot_rates.py',
        'src/causalbank/funding_calibration.py', 'src/causalbank/dynamic_funding.py', s['base'], s['observation']])
    print(json.dumps({'status':result['status'], 'consumer_cases':len(cases), 'rejected_requests':len(violations)}))


if __name__ == '__main__':
    with threadpool_limits(limits=1):
        main()
