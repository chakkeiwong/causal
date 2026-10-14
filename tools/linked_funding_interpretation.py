#!/usr/bin/env python3
"""Check the population bias and symbolic precision planning calculations."""
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
from scipy.stats import norm

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from causalbank.dynamic_funding import FundingTarget


def main():
    spec = json.loads((ROOT/'docs/studies/dynamic-funding-spec.json').read_text())
    obs = json.loads((ROOT/'docs/studies/dynamic-observation-spec.json').read_text())
    target = FundingTarget(horizon=spec['horizon'],branches=spec['branches'])
    scale = float(target.weights() @ spec['rho']**np.arange(target.horizon+1))
    focal, companion = spec['beta'], obs['decoy_beta']
    baseline = .5*(focal+companion)
    # Enumerate inclusion and label flips to recover both population moments.
    cases = {}
    for name,qa,qd,e in [('correct',.25,.25,0.),('wrong_inclusion',.1,.25,0.),('noisy_labels',.25,.25,.15)]:
        aug, ipw = 0., 0.
        for selected in (0,1):
            for flipped in (0,1):
                probability = (qa if selected else 1-qa)*(e if flipped else 1-e)
                apparent = companion if flipped else focal
                aug += probability*(baseline+selected/qd*(apparent-baseline))
                ipw += probability*selected/qd*apparent
        expected = (1-e)*focal+e*companion
        assert np.isclose(aug,baseline+qa/qd*(expected-baseline))
        assert np.isclose(ipw,qa/qd*expected)
        cases[name] = dict(augmented_coefficient=aug,ipw_coefficient=ipw,
                          augmented_population_bias=(aug-focal)*scale,
                          ipw_population_bias=(ipw-focal)*scale)
    # Both sides of the width inversion agree on a deterministic grid.
    checked = 0
    for omega in (1.,5.,20.):
        for k in (.2,2.,10.):
            for limit in (omega,omega+1.,omega+100.):
                threshold = k/(limit-omega+k)
                for q in (threshold,1.,max(.001,threshold/2)):
                    assert (omega+(1/q-1)*k <= limit+1e-10) == (q >= threshold-1e-12)
                    checked += 1
    result = dict(status='pass',date='2026-10-11',issues=[],
                  monetary_response_scale=scale,direct_cost=target.direct_cost(),
                  exogeneity_population_bias=spec['common_noise_sd']*.5*scale,
                  audit_law_cases=cases,precision_inequality_cases=checked,
                  scope='Post-study deterministic interpretation checks. No new outcomes or bank price/precision assumption.',
                  input_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in
                    ['tools/linked_funding_interpretation.py','src/causalbank/dynamic_funding.py',
                     'docs/studies/dynamic-funding-spec.json','docs/studies/dynamic-observation-spec.json']})
    (ROOT/'docs/reviews/linked-funding-interpretation-checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status='pass',exogeneity_shift=result['exogeneity_population_bias'],audit_laws=cases),indent=2))


if __name__ == '__main__': main()
