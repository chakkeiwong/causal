#!/usr/bin/env python3
"""Independent population, path, partial-regression and lag witnesses for V9."""
import itertools
import json
import numpy as np
from numpy.polynomial.hermite import hermgauss
from threadpoolctl import threadpool_limits
from calibration_common import ROOT, SPEC, save
from causalbank.dynamic_funding import FundingTarget
from causalbank.funding_calibration import (simulate_rows, stationary_nuisance,
    conditional_pilot_responses, fit_funding, fit_dense, LagAccumulator, DECLARATIONS)


def checks():
    spec = json.loads((ROOT/SPEC).read_text())
    base = json.loads((ROOT/spec['base']).read_text())
    obs = json.loads((ROOT/spec['observation']).read_text())
    target = FundingTarget(horizon=base['horizon'], branches=base['branches'])
    oracle = stationary_nuisance(base, obs)
    rng = np.random.default_rng(910607)
    # Independent infinite-past sum, rather than the implementation recurrence.
    curves = []
    j = np.arange(-2000, base['horizon']+1)
    for beta in (base['beta'], obs['decoy_beta']):
        value = np.zeros((3, base['horizon']+1))
        for h in range(base['horizon']+1):
            selected = j[j <= h]
            value[1, h] = (.5*beta+1.2)*np.sum(base['rho']**(h-selected)*base['driver_rho']**abs(selected))
            value[2, h] = (.2*beta+.4)*np.sum(base['rho']**(h-selected)*base['driver_rho']**(2*abs(selected)))
        curves.append(value)
    direct = []
    for p in obs['correct_pair_probability']:
        direct.append(np.column_stack(([0., .5, .2], p*curves[0]+(1-p)*curves[1],
            (1-p)*curves[0]+p*curves[1])))
    oracle_error = float(np.max(abs(oracle-np.vstack((direct[0], direct[1]-direct[0])))))
    assert oracle_error < 1e-12
    # Gaussian quadrature directly integrates residual products over W and e.
    coefficient = oracle+rng.normal(0, .2, oracle.shape)
    predicted = conditional_pilot_responses(base, obs, coefficient)
    nodes, weights = hermgauss(24)
    values = np.sqrt(2)*nodes
    weights /= np.sqrt(np.pi)
    integral = []
    for group, probability in enumerate(obs['correct_pair_probability']):
        true = direct[group]
        fitted = coefficient[:3]+group*coefficient[3:]
        focal = base['beta']*base['rho']**np.arange(target.horizon+1)
        decoy = obs['decoy_beta']*base['rho']**np.arange(target.horizon+1)
        theta = np.r_[probability*focal+(1-probability)*decoy, (1-probability)*focal+probability*decoy]
        numerator, denominator = np.zeros(len(theta)), 0.
        for w, ww in zip(values, weights):
            x = np.array([1., w, w*w-1])
            for e, we in zip(values, weights):
                action = x@true[:, 0]+e
                outcome_mean = x@true[:, 1:]+theta*e
                v = action-x@fitted[:, 0]
                numerator += ww*we*v*(outcome_mean-x@fitted[:, 1:])
                denominator += ww*we*v*v
        integral.append(numerator/denominator)
    bias_identity_error = float(np.max(abs(predicted-integral)))
    assert bias_identity_error < 1e-11

    # Reconstruct the generated law through literal branch recursions. The
    # orthogonal branch noises plus their independent mean have iid Gaussian law.
    n, seed = 171, 910619
    raw = simulate_rows(base, obs, n, seed)
    total = n+base['burn']+base['horizon']+1
    random = np.random.default_rng(seed)
    dw, e, common, average = [random.normal(size=total) for _ in range(4)]
    w, action = np.zeros(total), np.zeros(total)
    for t in range(1, total):
        w[t] = base['driver_rho']*w[t-1]+np.sqrt(1-base['driver_rho']**2)*dw[t]
        action[t] = .5*w[t]+.2*(w[t]*w[t]-1)+e[t]
    branches = base['branches']
    individual = rng.normal(size=(total, branches))
    individual = base['branch_noise_sd']*(individual-individual.mean(axis=1, keepdims=True)+average[:, None]/np.sqrt(branches))
    origin = np.arange(base['burn']+1, base['burn']+n+1)
    bank = []
    for beta in (base['beta'], obs['decoy_beta']):
        paths = np.zeros((total, branches))
        for t in range(1, total):
            paths[t] = (base['rho']*paths[t-1]+beta*np.linspace(.6, 1.4, branches)*action[t]
                +1.2*w[t]+.4*(w[t]*w[t]-1)+base['common_noise_sd']*common[t]+individual[t])
        aggregate = paths.mean(axis=1)
        bank.append(np.column_stack([aggregate[origin+h] for h in range(target.horizon+1)]))
    strata = random.integers(0, 2, n)
    correct = random.random(n) < np.asarray(obs['correct_pair_probability'])[strata]
    literal = np.column_stack((strata, action[origin], np.ones(n), w[origin], w[origin]**2-1,
        np.where(correct[:, None], bank[0], bank[1]), np.where(correct[:, None], bank[1], bank[0])))
    path_error = float(np.max(abs(literal-raw)))
    assert path_error < 1e-11

    lag_errors = []
    for length in (1, 2, 19, 113):
        score = rng.normal(size=length)+3.7
        for lag in (0, min(6, length-1)):
            for size in (1, 2, 7, 53):
                accumulator = LagAccumulator(lag)
                for start in range(0, length, size):
                    accumulator.add(score[start:start+size])
                # Actual serialization/read-back of bounded accumulator state.
                state = json.loads(json.dumps({k:(v.tolist() if isinstance(v, np.ndarray) else v) for k, v in accumulator.__dict__.items()}))
                restored = LagAccumulator(lag)
                restored.__dict__.update({k:(np.array(v) if k in ('products', 'first', 'tail') else v) for k, v in state.items()})
                for bartlett in (True, False):
                    centered = score-score.mean()
                    direct_var = centered@centered
                    for k in range(1, lag+1):
                        direct_var += 2*(1-k/(lag+1) if bartlett else 1)*(centered[k:]@centered[:-k])
                    error = abs(restored.variance_of_mean(bartlett)-direct_var/length**2)
                    lag_errors.append(error)
    assert max(lag_errors) < 1e-12

    # Finite enumeration illustrates the filtration argument for a linear law.
    shocks = np.array(list(itertools.product([-1., 1.], repeat=10)))
    def score_at(t):
        h = 2
        coefficients = np.array([.6**(t+h-j) if j <= t+h and j != t else 0. for j in range(10)])
        return shocks[:, t]*(shocks@coefficients)
    finite_covariances = [float(np.mean(score_at(3)*score_at(3+k))) for k in range(1, 5)]
    assert finite_covariances[0] > 0 and max(abs(v) for v in finite_covariances[2:]) < 1e-12

    data = simulate_rows(base, obs, 431, 910627)
    errors = []
    for features in ((0, 1, 2), (0, 1)):
        for rule in ('innovation_horizon', 'bartlett'):
            dense = fit_dense(data, target, [900, 850], [1000, 1000], features=features, covariance=rule, declarations=DECLARATIONS)
            for size in (1, 7, 59, 500):
                streamed = fit_funding(data, target, [900, 850], [1000, 1000], features=features,
                    covariance=rule, chunk_size=size, declarations=DECLARATIONS)
                assert dense['status'] == streamed['status'] == 'computed'
                errors.append(max(abs(dense[k]-streamed[k]) for k in ('estimate', 'standard_error')))
    assert max(errors) < 1e-6
    assert fit_funding(data, target, [500, 500], [1000, 1000], declarations=DECLARATIONS)['status'] == 'unavailable_mapping_rank'
    assert fit_funding(data, target, [1000, 850], [1000, 1000], declarations=DECLARATIONS)['status'] == 'unavailable_audit_boundary'
    invalid = []
    for kwargs in ({'declarations': None}, {'declarations': DECLARATIONS, 'chunk_size': 0}):
        try:
            fit_funding(data, target, [900, 850], [1000, 1000], **kwargs)
        except ValueError:
            invalid.append(True)
    assert len(invalid) == 2
    receipt = dict(status='pass', stationary_nuisance_error=oracle_error,
        conditional_pilot_integral_error=bias_identity_error, literal_branch_path_error=path_error,
        centered_lag_and_state_error=max(lag_errors), finite_toy_covariances=finite_covariances,
        dense_svd_qr_maximum_monetary_error=max(errors), rank_boundary_and_declaration_refusals=True,
        scope='Independent finite/population/algebra witnesses and declared refusals; the general filtration and rate arguments require the accompanying derivation.')
    save('docs/reviews/calibration-independent-checks.json', receipt, [SPEC,
        'tools/calibration_checks.py', 'src/causalbank/funding_calibration.py',
        'src/causalbank/dynamic_funding.py', spec['base'], spec['observation']])
    print(json.dumps(receipt), flush=True)


if __name__ == '__main__':
    with threadpool_limits(limits=1):
        checks()
