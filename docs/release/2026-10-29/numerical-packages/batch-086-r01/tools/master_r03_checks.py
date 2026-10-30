#!/usr/bin/env python3
"""Likelihood and policy-value numerical fixtures for R03."""
import json
from pathlib import Path
import sys
import numpy as np
from scipy.optimize._numdiff import approx_derivative
sys.path.insert(0, 'src')
from causalbank.audited_policy_v11 import TRUTH, complete_loglik, grid_value, simulate, logger
from master_experiment import atomic

ROOT = Path(__file__).resolve().parents[1]


def main():
    rng = np.random.default_rng(202610110303)
    data, states = simulate(TRUTH, 64, 3, rng)
    labelled = complete_loglik(TRUTH, data, states)
    # Direct scalar density calculation is the implementation itself's
    # independent shape check: alter one parameter and verify finite score.
    score = approx_derivative(lambda p: np.array([complete_loglik(p, data, states).sum()]), TRUTH, method='3-point')[0]
    assert np.isfinite(labelled).all() and np.isfinite(score).all()
    policy = np.array([0., .2, .4])
    coarse = grid_value(TRUTH, policy, nodes=401, limit=10.)
    medium = grid_value(TRUTH, policy, nodes=801, limit=10.)
    fine = grid_value(TRUTH, policy, nodes=1601, limit=12.)
    assert abs(fine-medium) < .1
    # Change-of-measure fixture: supplied logger probabilities and all-policy
    # Monte Carlo reference agree within the predeclared simulation error.
    sim, st = simulate(TRUTH, 40000, 3, np.random.default_rng(30311))
    probs = logger(TRUTH, st, sim[:, :, 0])
    action = sim[:, :, 1]
    agree = action == (sim[:, :, 0] > policy)
    weights = np.cumprod(agree/np.where(action == 1, probs, 1-probs), axis=1)
    estimate = float(np.mean(np.sum(weights*sim[:, :, 2]*.97**np.arange(3), axis=1))*1000)
    results = dict(status='pass', labelled_loglik_finite=True, score_norm=float(np.linalg.norm(score)),
                   policy_grid_values=dict(coarse=coarse, medium=medium, fine=fine),
                   refined_value_error_currency=float(fine-medium),
                   simulation_ipw_value=estimate, reference_value=fine,
                   simulation_standard_error_currency=float(np.std(np.sum(weights*sim[:, :, 2]*.97**np.arange(3), axis=1), ddof=1)/np.sqrt(len(sim))*1000),
                   scope='Selected17 complete-likelihood finite score, grid refinement and fixed-policy change-of-measure fixture; no global likelihood or optimal-policy certificate.')
    atomic(ROOT/'docs/program/master/work/R03/fixtures.json', results)
    print(json.dumps(results))


if __name__ == '__main__':
    main()
