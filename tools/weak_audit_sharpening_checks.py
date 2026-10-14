#!/usr/bin/env python3
"""Dense covariance, set geometry and observational-equivalence witnesses."""
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
from scipy.signal import lfilter
from threadpoolctl import threadpool_limits

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from causalbank.dynamic_funding import FundingTarget
from causalbank.funding_calibration import DECLARATIONS, pilot_data, simulate_rows
from causalbank.linkage_sets import sum_difference_projection
from causalbank.streaming_pilot import train_streaming_pilot
from causalbank.weak_audit_sharpening import fit_transformed_projection, transformed_scores

SPEC = 'docs/studies/weak-audit-sharpening-spec.json'


def digest(name):
    return hashlib.sha256((ROOT / name).read_bytes()).hexdigest()


def main():
    spec = json.loads((ROOT / SPEC).read_text())
    base = json.loads((ROOT / spec['base']).read_text())
    obs = json.loads((ROOT / spec['observation']).read_text())
    target = FundingTarget(horizon=base['horizon'], branches=base['branches'])
    tests, differences = [], []
    transform = np.kron(np.eye(2), np.array([[.5, .5], [.5, -.5]]))
    for cell, design in enumerate(spec['designs'][:5]):
        law = dict(base, rho=design.get('rho', base['rho']))
        observation = dict(obs, correct_pair_probability=design['probability'])
        correlation = design.get('innovation_correlation', 0.)
        data = simulate_rows(law, observation, 1200, [spec['seed'], 811, cell], correlation)
        prior = simulate_rows(law, observation, 4800, [spec['seed'], 812, cell], correlation)
        result = transformed_scores(prior, data, target, base['penalties'], 4096)
        assert result['status'] == 'computed', result
        fit = train_streaming_pilot(prior, base['penalties'], 4096)
        prepared = pilot_data(data)
        predictions = prepared['x'] @ fit['coefficient']
        action = prepared['action'] - predictions[:, 0]
        residual = prepared['outcomes'] - predictions[:, 1:]
        width = target.horizon + 1
        monetary = np.column_stack((residual[:, :width] @ target.weights(),
                                     residual[:, width:] @ target.weights()))
        means, scores = np.zeros(4), np.zeros((len(data), 4))
        for s in (0, 1):
            keep = prepared['stratum'] == s
            q = action[keep] @ action[keep]
            slope = action[keep] @ monetary[keep] / q
            means[2*s:2*s+2] = slope
            scores[keep, 2*s:2*s+2] = len(data)*action[keep, None]*(monetary[keep]-action[keep, None]*slope)/q
        scores -= scores.mean(axis=0)
        covariance = scores.T @ scores
        for lag in range(1, target.horizon+1):
            cross = scores[lag:].T @ scores[:-lag]
            covariance += cross + cross.T
        covariance /= len(data)**2
        expected_means = transform @ means
        expected_variances = np.diag(transform @ covariance @ transform.T)
        assert np.allclose(result['transformed_means'], expected_means, rtol=2e-12, atol=1e-6)
        assert np.allclose(result['transformed_variances'], expected_variances, rtol=2e-12, atol=1e-4)
        differences.append(float(np.max(np.abs(np.array(result['transformed_variances'])-expected_variances)/np.maximum(1., np.abs(expected_variances)))))
        tests.append(design['name']+'_full_covariance_transform')
    assert sum_difference_projection((1,2),(-1,1),(.49,.51)) == [(-float('inf'),float('inf'))]
    pieces = sum_difference_projection((1,2),(1,2),(.49,.51))
    assert len(pieces) == 2 and pieces[0][0] == -float('inf') and pieces[1][1] == float('inf')
    assert sum_difference_projection((1,2),(1,2),(.5,.5)) == []
    tests.append('whole_line_disconnected_and_empty_exact_rank')

    # Force equal candidate residuals: their difference score has zero variance.
    duplicate_prior, duplicate_data = prior.copy(), data.copy()
    duplicate_prior[:, 5+width:] = duplicate_prior[:, 5:5+width]
    duplicate_data[:, 5+width:] = duplicate_data[:, 5:5+width]
    raw = transformed_scores(duplicate_prior, duplicate_data, target, base['penalties'],4096)
    # Exact arithmetic has zero variance; fitted floating point can leave a
    # tiny positive remnant. The fitted route itself must now refuse it.
    assert raw['status'] == 'unavailable_response_variance', raw
    from causalbank.funding_calibration import LagAccumulator
    zero = LagAccumulator(target.horizon)
    zero.add(np.zeros(len(data)))
    assert zero.variance_of_mean() == 0
    tests.append('zero_score_variance_not_qualified')

    # Coupled exact observational laws: c != 0 in the first, independent error
    # and shifted causal response plus adjusted nuisance mean in the second.
    rng = np.random.default_rng([spec['seed'],813])
    n = 2000
    driver = rng.normal(size=n)
    e, z, branch = rng.normal(size=(3,n))
    action_mean = .5*driver+.2*(driver**2-1)
    nuisance = 1.2*driver+.4*(driver**2-1)
    action = action_mean + e
    sigma, c, beta = base['common_noise_sd'], .5, base['beta']
    shift = sigma*c
    noise = sigma*np.sqrt(1-c*c)*z + base['branch_noise_sd']/np.sqrt(base['branches'])*branch
    forcing_original = beta*action+nuisance+shift*e+noise
    forcing_alternative = (beta+shift)*action+(nuisance-shift*action_mean)+noise
    original = lfilter([1.], [1.,-base['rho']],forcing_original)
    alternative = lfilter([1.], [1.,-base['rho']],forcing_alternative)
    assert np.allclose(original,alternative,rtol=1e-13,atol=1e-12)
    response_shift = shift * base['rho']**np.arange(target.horizon+1)
    financial_shift = float(target.weights()@response_shift)
    tests.append('observational_equivalence_with_different_causal_value')
    receipt = dict(status='pass',date='2026-10-11',issues=[],tests=tests,
                   maximum_scaled_variance_difference=max(differences),
                   zero_difference_fixture=raw['status'],
                   observational_equivalence=dict(coefficient_shift=shift,
                       maximum_path_difference=float(np.max(np.abs(original-alternative))),
                       financial_target_difference=financial_shift,
                       scope='Constructed laws permitting an adjusted nuisance mean have identical observational paths but different interventions; not an impossibility claim under every restriction.'),
                   input_sha256={name:digest(name) for name in [SPEC,spec['base'],spec['observation'],
                       'tools/weak_audit_sharpening_checks.py','src/causalbank/weak_audit_sharpening.py',
                       'src/causalbank/weak_audit_projection.py','src/causalbank/funding_calibration.py',
                       'src/causalbank/streaming_pilot.py','src/causalbank/linkage_sets.py']})
    (ROOT/'docs/reviews/weak-audit-sharpening-checks.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(dict(status='pass',tests=len(tests),scaled_variance_difference=max(differences),
                          identical_observations_causal_value_difference=financial_shift,
                          zero_difference_fixture=raw['status']),indent=2))


if __name__ == '__main__':
    with threadpool_limits(limits=1):
        main()
