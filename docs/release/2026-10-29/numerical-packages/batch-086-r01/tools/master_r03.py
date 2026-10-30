"""Audited fixed-policy study with declared and concealed failures."""
import numpy as np
from causalbank.audited_policy_v11 import TRUTH, simulate, logger, policy_estimate


def request(spec, cell, index):
    d = spec['designs'][cell]; p = TRUTH.copy()
    p[4] = d.get('log_emission_variance', p[4])
    p[5] = d.get('logger_intercept', p[5])
    n, h = d.get('audits', 800), spec['horizon']
    rng = np.random.default_rng([spec['seed'], cell, index])
    data, states = simulate(p, n, h, rng, misspecification=d.get('transition_misspecification', False))
    probs = logger(p, states, data[:, :, 0])
    declared = probs
    if d.get('wrong_logger'):
        declared = np.full_like(probs, .5)
    primary = policy_estimate(data, declared, spec['policy'], alpha=spec['alpha'],
                              selection='evaluation' if d.get('leakage') else 'independent')
    challenger = policy_estimate(data, declared, spec['policy'], alpha=.05,
                                 selection='evaluation' if d.get('leakage') else 'independent')
    return dict(truth=d['reference_value'], methods=dict(audited_policy99=primary, audited_policy95=challenger),
                labels=n*h, history_rows=n*h, audited_trajectories=n,
                reference_error_diagnostic=d['reference_difference'])
