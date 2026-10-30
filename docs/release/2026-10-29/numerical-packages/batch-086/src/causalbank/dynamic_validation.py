"""Numerical input domain of the selected linked funding experiment.

These checks do not establish independence, causal exclusion, source truth,
representativeness, or the nuisance model's population correctness.
"""
import numpy as np


def validate_target(target):
    target.validate()
    if (not isinstance(target.horizon, (int, np.integer))
            or not isinstance(target.branches, (int, np.integer))):
        raise ValueError('horizon and branches must be integer counts')
    values = [target.discount, target.monthly_margin,
              target.currency_per_balance_unit, target.baseline_per_branch]
    if not np.all(np.isfinite(values)):
        raise ValueError('economic inputs must be finite')
    if (not 0 <= target.discount <= 1 or target.currency_per_balance_unit <= 0
            or target.baseline_per_branch < 0):
        raise ValueError('unsupported discount, currency scale or baseline')


def validate_sample(sample, horizon, name):
    try:
        x, action, outcomes, stratum = [np.asarray(sample[k])
                                       for k in ('x', 'action', 'outcomes', 'stratum')]
    except (KeyError, TypeError) as exc:
        raise ValueError(name + ': missing sample arrays') from exc
    if action.ndim != 1:
        raise ValueError(name + ': action must be a vector')
    n = len(action)
    if (n < 2 or x.shape != (n, 6) or stratum.shape != (n,)
            or outcomes.shape != (n, 2 * (horizon + 1))):
        raise ValueError(name + ': inconsistent sample dimensions')
    if not all(np.all(np.isfinite(a)) for a in (x, action, outcomes, stratum)):
        raise ValueError(name + ': arrays must be finite')
    if not np.all(np.isin(stratum, [0, 1])) or len(np.unique(stratum)) != 2:
        raise ValueError(name + ': both evaluation/pilot strata 0 and 1 are required')
    basic = np.column_stack((np.ones(n), x[:, 1], x[:, 1]**2 - 1))
    expected = np.column_stack((basic, basic * stratum[:, None]))
    if not np.allclose(x, expected, rtol=1e-12, atol=1e-12):
        raise ValueError(name + ': unsupported nuisance basis')
    return x, action, outcomes, stratum


def validate_inputs(brief, pilot, data, strata, correct, penalties, inference, alpha):
    validate_target(brief.target)
    if inference not in ('regular_delta', 'weak_linkage_projection'):
        raise ValueError('unsupported inference procedure')
    if not np.isfinite(alpha) or not 0 < alpha < 1:
        raise ValueError('confidence error must be between zero and one')
    if inference == 'regular_delta' and alpha != .05:
        raise ValueError('regular reference interval is qualified at 95 percent')
    x, action, outcomes, _ = validate_sample(pilot, brief.target.horizon, 'pilot')
    validate_sample(data, brief.target.horizon, 'evaluation')
    if (not isinstance(brief.bandwidth, (int, np.integer))
            or not 0 <= brief.bandwidth < len(data['action'])):
        raise ValueError('bandwidth must be an integer below the calendar length')
    penalties = np.asarray(penalties, dtype=float)
    if penalties.ndim != 1 or not len(penalties) or np.any(~np.isfinite(penalties)) or np.any(penalties < 0):
        raise ValueError('penalties must be a nonempty finite nonnegative vector')
    split = len(x) // 2
    targets = np.column_stack((action, outcomes))
    if (split < x.shape[1] or np.linalg.matrix_rank(x[:split]) < x.shape[1]
            or np.any(np.var(targets[:split], axis=0) <= 0)):
        raise ValueError('pilot training half lacks full basis rank or loss variation')
    strata, correct = np.asarray(strata), np.asarray(correct)
    if (strata.ndim != 1 or correct.shape != strata.shape
            or not np.all(np.isin(strata, [0, 1]))
            or not np.all(np.isin(correct, [0, 1]))):
        raise ValueError('audits require aligned binary stratum and correctness vectors')
    if inference == 'regular_delta' and len(np.unique(strata)) != 2:
        raise ValueError('regular inverse mapping requires audits in both strata')
