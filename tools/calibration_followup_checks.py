#!/usr/bin/env python3
"""Bind the new growing-pilot operation to independent inherited matrix algebra."""
import json
import numpy as np
from threadpoolctl import threadpool_limits
from calibration_common import ROOT, SPEC, save
from causalbank.dynamic_funding import FundingTarget, train_pilot
from causalbank.funding_calibration import simulate_rows, pilot_data, DECLARATIONS
from causalbank.funding_pilot_rates import fit_growing_pilot
from causalbank.linked_observation import linked_response
from calibration_study import primitives, covariance, regular


def main():
    s = json.loads((ROOT/SPEC).read_text())
    base = json.loads((ROOT/s['base']).read_text())
    obs = json.loads((ROOT/s['observation']).read_text())
    target = FundingTarget(horizon=base['horizon'], branches=base['branches'])
    errors = []
    for n in (240, 720):
        prior = simulate_rows(base, obs, 4*n, [911073, 1, n])
        data = simulate_rows(base, obs, n, [911073, 2, n])
        fit = train_pilot(pilot_data(prior), base['penalties'])
        counts, sizes = [950, 800], [1000, 1000]
        direct = linked_response(pilot_data(data), fit, counts, sizes, target, int(2*n**.2))
        new = fit_growing_pilot(prior, data, target, counts, sizes, base['penalties'], covariance='bartlett', declarations=DECLARATIONS)
        assert new['status'] == direct['status'] == 'computed'
        errors.extend([abs(new['estimate']-direct['financial_value']), abs(new['standard_error']-direct['financial_se'])])
        horizon = fit_growing_pilot(prior, data, target, counts, sizes, base['penalties'], declarations=DECLARATIONS)
        m, scores = primitives(data, fit['coefficient'], target)
        reference = regular(m, covariance(scores, 'innovation_horizon', target.horizon), np.array(counts)/sizes, 1000, target)
        errors.extend([abs(horizon['estimate']-reference['estimate']), abs(horizon['standard_error']-reference['standard_error'])])
        assert np.max(abs(np.asarray(new['coefficient'])-fit['coefficient'])) == 0
    assert max(errors) < 1e-6
    try:
        fit_growing_pilot(prior[:-1], data, target, counts, sizes, base['penalties'], declarations=DECLARATIONS)
    except ValueError as error:
        assert 'four pilot' in str(error)
    else:
        raise AssertionError('Undersized pilot accepted')
    result = dict(status='pass', maximum_monetary_difference=max(errors),
        equal_pilot_fits=True, insufficient_pilot_refused=True,
        scope='Independent inherited full-matrix Bartlett and primitive direct-lag comparisons; no finite-sample calibration theorem.')
    save('docs/reviews/calibration-followup-checks.json', result, [SPEC,
        'docs/studies/calibration-followup-spec.json', 'tools/calibration_followup_checks.py',
        'tools/calibration_study.py', 'src/causalbank/funding_pilot_rates.py',
        'src/causalbank/funding_calibration.py', 'src/causalbank/dynamic_funding.py',
        'src/causalbank/linked_observation.py', 'src/causalbank/responses.py', s['base'], s['observation']])
    print(json.dumps({k:v for k,v in result.items() if k!='input_sha256'}))


if __name__ == '__main__':
    with threadpool_limits(limits=1):
        main()
