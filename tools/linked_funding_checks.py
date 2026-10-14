#!/usr/bin/env python3
"""Independent audit enumeration and dense estimator checks before final draws."""
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
from threadpoolctl import threadpool_limits

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
from causalbank.dynamic_funding import FundingTarget
from causalbank.linkage_sets import decode_set
from causalbank.linked_funding import (LINKED_DECLARATIONS, fit_linked_funding,
                                       pseudo_rows, simulate_linked)


def read(name):
    return json.loads((ROOT/name).read_text())


def digest(name):
    with (ROOT/name).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def dense(pilot, rows, target, pilot_audit, audit, penalties, augment):
    def reduce(source, info):
        mask, labels, q = info
        h = target.horizon+1
        a, b = source[:, 5:5+h], source[:, 5+h:]
        baseline = (a+b)/2 if augment else np.zeros_like(a)
        z = []
        for t in range(len(source)):
            y = baseline[t].copy()
            if mask[t]:
                focal = a[t] if labels[t] == 1 else b[t]
                y += (focal-baseline[t])/q[t]
            z.append(y)
        x = np.c_[source[:, 2:5], source[:, 2:5]*source[:, 0, None]]
        return x, np.c_[source[:, 1], z]
    x, y = reduce(pilot, pilot_audit)
    cut = len(x)//2
    scale = y[:cut].var(axis=0)
    def fit(a, b, penalty):
        reg = np.diag([0.]+[np.sqrt(penalty)]*5)
        return np.linalg.lstsq(np.r_[a, reg], np.r_[b, np.zeros((6, b.shape[1]))], rcond=None)[0]
    losses = [np.mean((y[cut:]-x[cut:]@fit(x[:cut], y[:cut], p))**2/scale) for p in penalties]
    penalty = penalties[int(np.argmin(losses))]
    coefficient = fit(x, y, penalty)
    x, y = reduce(rows, audit)
    residual = y-x@coefficient
    v, outcome = residual[:, 0], residual[:, 1:]@target.weights()
    n = len(rows)
    slopes, scores = [], np.empty(n)
    for s in (0, 1):
        keep = rows[:, 0] == s
        q = np.dot(v[keep], v[keep])
        slope = np.dot(v[keep], outcome[keep])/q
        slopes.append(slope)
        scores[keep] = .5*n*v[keep]*(outcome[keep]-slope*v[keep])/q
    centered = scores-scores.mean()
    variance = (centered@centered+2*sum(centered[j:]@centered[:-j]
                for j in range(1, target.horizon+1)))/n**2
    return .5*sum(slopes)-target.direct_cost(), variance, penalty


def main():
    tests = []
    # Conditional identities use complete outcomes, not any fitted model.
    f, b, v, q = np.array([3., -2.]), np.array([1., 4.]), np.array([.7, -1.2]), np.array([.2, .6])
    delta = v*(f-b)
    errors, weights = [], []
    for r0 in (0, 1):
        for r1 in (0, 1):
            r = np.array([r0, r1])
            errors.append(delta*(r/q-1))
            weights.append(np.prod(np.where(r, q, 1-q)))
    errors, weights = np.array(errors), np.array(weights)
    assert np.allclose(weights@errors, 0, atol=1e-14)
    covariance = errors.T@(weights[:, None]*errors)
    assert np.allclose(covariance, np.diag((1/q-1)*delta**2), atol=1e-13)
    tests += ['conditional_audit_mean_identity', 'diagonal_added_variance_and_zero_cross_date_covariance']
    base, obs = read('docs/studies/dynamic-funding-spec.json'), read('docs/studies/dynamic-observation-spec.json')
    obs = dict(obs, correct_pair_probability=[.5, .5])
    target = FundingTarget(horizon=base['horizon'], branches=base['branches'])
    rows, audit = simulate_linked(base, obs, 240, [811, 1], [811, 3], inclusion=.4)
    pilot, pa = simulate_linked(base, obs, 960, [811, 2], [811, 4], inclusion=.4)
    differences = []
    for aug in (True, False):
        expected, variance, penalty = dense(pilot, rows, target, pa, audit, base['penalties'], aug)
        for chunk in (1, 17, 1000):
            actual = fit_linked_funding(pilot, rows, target, pa, audit, base['penalties'],
                        augmentation=aug, chunk_size=chunk, declarations=LINKED_DECLARATIONS)
            assert actual['status'] == 'computed_set'
            assert np.array_equal(decode_set(actual['financial_set']), [actual['interval']])
            differences += [abs(actual['estimate']-expected)/max(1, abs(expected)),
                            abs(actual['calendar_variance']-variance)/max(1, abs(variance))]
            assert actual['pilot_penalty'] == penalty
    assert max(differences) < 2e-10
    tests.append('independent_dense_tuning_slopes_and_calendar_covariance_across_chunks')
    tests.append('shared_financial_set_serialization_round_trip')
    permuted = dict(obs, correct_pair_probability=[.95, .7])
    swapped, sa = simulate_linked(base, permuted, 240, [811, 1], [811, 3], inclusion=.4)
    assert np.array_equal(pseudo_rows(rows, *audit, target.horizon),
                          pseudo_rows(swapped, *sa, target.horizon))
    tests.append('invariance_to_candidate_swap_probabilities_including_exact_rank')
    full, fa = simulate_linked(base, obs, 240, [812, 1], [812, 2], inclusion=1.)
    truth, _ = simulate_linked(base, dict(obs, correct_pair_probability=[1., 1.]),
                             240, [812, 1], [812, 2], inclusion=1.)
    for augment in (True, False):
        assert np.allclose(pseudo_rows(full, *fa, target.horizon, augmentation=augment)[:, 5:],
                           truth[:, 5:5+target.horizon+1], rtol=1e-14, atol=1e-14)
    tests.append('full_audit_reduces_to_observed_focal_outcomes')
    invalid = [(*audit[:2], np.zeros(len(rows))),
               (audit[0], np.zeros(len(rows)), audit[2]),
               (audit[0], np.where(audit[0], 2., np.nan), audit[2])]
    for info in invalid:
        try:
            pseudo_rows(rows, *info, target.horizon)
        except ValueError:
            pass
        else:
            raise AssertionError('Invalid audit input accepted')
    tests.append('invalid_probability_unsampled_label_leakage_and_untruthful_label_codes_rejected')
    none = (np.zeros(len(rows), bool), np.full(len(rows), np.nan), audit[2])
    missing = fit_linked_funding(pilot, rows, target, pa, none, base['penalties'], declarations=LINKED_DECLARATIONS)
    assert missing['status'] == 'unavailable_outcome_audit'
    tests.append('absent_outcome_audits_refused')
    # Fully observed deterministic linear responses must not become tiny normal bands.
    deterministic = []
    infos = []
    for source in (pilot.copy(), rows.copy()):
        source[:, 5:] = source[:, 1, None]*np.linspace(1., 2., source.shape[1]-5)
        deterministic.append(source)
        infos.append((np.ones(len(source), bool), np.ones(len(source)), np.ones(len(source))))
    constant = fit_linked_funding(deterministic[0], deterministic[1], target, infos[0], infos[1],
                                 [0.], declarations=LINKED_DECLARATIONS)
    assert constant['status'] == 'unavailable_response_variance', constant
    tests.append('deterministic_fitted_score_roundoff_not_a_normal_band')
    paths = ['tools/linked_funding_checks.py', 'src/causalbank/linked_funding.py',
             'src/causalbank/funding_calibration.py', 'src/causalbank/streaming_pilot.py',
             'src/causalbank/dynamic_funding.py', 'docs/program/linked-funding-plan-2026-10-11.md',
             'docs/studies/linked-funding-spec.json', 'docs/studies/dynamic-funding-spec.json',
             'docs/studies/dynamic-observation-spec.json']
    result = dict(status='pass', date='2026-10-11', issues=[], tests=tests,
                  maximum_relative_dense_difference=max(differences),
                  deterministic_fixture=constant['status'],
                  scope='Independent algebra and numerical fixtures, not statistical or bank validation.',
                  input_sha256={name:digest(name) for name in paths})
    (ROOT/'docs/reviews/linked-funding-checks.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status', 'tests', 'maximum_relative_dense_difference')}, indent=2))


if __name__ == '__main__':
    with threadpool_limits(limits=1):
        main()
