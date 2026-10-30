#!/usr/bin/env python3
"""Independent dense and exact-binomial challenges for the weak-audit design."""
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
from scipy.stats import binom
from threadpoolctl import threadpool_limits

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from causalbank.dynamic_funding import FundingTarget
from causalbank.funding_calibration import DECLARATIONS, pilot_data, simulate_rows
from causalbank.linkage_sets import binomial_interval, pair_projection
from causalbank.streaming_pilot import train_streaming_pilot
from causalbank.weak_audit_projection import (
    audit_interval, fit_weak_audit_projection, observable_scores,
)


def digest(name):
    return hashlib.sha256((ROOT / name).read_bytes()).hexdigest()


def main():
    spec = json.loads((ROOT / 'docs/studies/weak-audit-projection-spec.json').read_text())
    base = json.loads((ROOT / spec['base']).read_text())
    observation = json.loads((ROOT / spec['observation']).read_text())
    target = FundingTarget(horizon=base['horizon'], branches=base['branches'])
    checks = []
    error = spec['audit_error_total'] / 2
    for n in range(1, 16):
        intervals = [audit_interval(k, n, error) for k in range(n + 1)]
        for p in np.linspace(0, 1, 101):
            mass = sum(float(binom.pmf(k, n, p)) for k, (lo, hi) in enumerate(intervals)
                       if lo <= p <= hi)
            assert mass + 1e-12 >= 1 - error, (n, p, mass)
        for k in (0, n // 2, n):
            old = binomial_interval(k, n, error)
            new = intervals[k]
            assert max(abs(new[0] - old[0]), abs(new[1] - old[1])) < 1e-8
    checks.append('exact_binomial_enumeration_and_inherited_inversion')

    assert pair_projection((0., 2.), (1., 3.), (.49, .51)) == [(-float('inf'), float('inf'))]
    disconnected = pair_projection((0., 1.), (2., 3.), (.49, .51))
    assert len(disconnected) == 2 and disconnected[0][0] == -float('inf') and disconnected[1][1] == float('inf')
    checks.append('whole_line_and_disconnected_rank_one_projection')

    for name in ('baseline_1200', 'near_rank_1200'):
        design = next(d for d in spec['designs'] if d['name'] == name)
        law = dict(base, rho=design.get('rho', base['rho']))
        obs = dict(observation, correct_pair_probability=design['probability'])
        rows = simulate_rows(law, obs, 1200, [spec['seed'], 717, 0 if name == 'baseline_1200' else 1])
        prior = simulate_rows(law, obs, 4800, [spec['seed'], 718, 0 if name == 'baseline_1200' else 1])
        check = observable_scores(prior, rows, target, base['penalties'], spec['pilot_chunk_size'])
        assert check['status'] == 'computed', check
        fit = train_streaming_pilot(prior, base['penalties'], spec['pilot_chunk_size'])
        data = pilot_data(rows)
        predicted = data['x'] @ fit['coefficient']
        action = data['action'] - predicted[:, 0]
        residual = data['outcomes'] - predicted[:, 1:]
        h = target.horizon + 1
        weighted = np.column_stack((residual[:, :h] @ target.weights(),
                                    residual[:, h:] @ target.weights()))
        n = len(rows)
        dense_slopes = np.zeros((2, 2))
        dense_score = np.zeros((n, 4))
        for s in (0, 1):
            keep = data['stratum'] == s
            qsum = action[keep] @ action[keep]
            dense_slopes[s] = action[keep] @ weighted[keep] / qsum
            dense_score[keep, 2 * s:2 * s + 2] = (
                n * action[keep, None] *
                (weighted[keep] - action[keep, None] * dense_slopes[s]) / qsum)
        variance = []
        for j in range(4):
            x = dense_score[:, j] - dense_score[:, j].mean()
            raw = x @ x + 2 * sum(x[k:] @ x[:-k] for k in range(1, target.horizon + 1))
            variance.append(raw / n**2)
        assert np.allclose(check['candidate_financial_means'], dense_slopes.ravel(), rtol=1e-12, atol=1e-6)
        assert np.allclose(check['candidate_financial_variances'], variance, rtol=1e-12, atol=1e-4)
        counts = [int(round(design['audit'] * p)) for p in design['probability']]
        result = fit_weak_audit_projection(prior, rows, target, counts,
                                            [design['audit']] * 2, base['penalties'],
                                            declarations=DECLARATIONS)
        assert result['status'] in ('computed_set', 'empty_projection')
        checks.append(name + '_dense_candidate_score_and_projection')

    for mutation in ('counts', 'declarations', 'dimensions', 'nonfinite'):
        changed_rows, changed_counts, declarations = rows.copy(), counts.copy(), DECLARATIONS
        if mutation == 'counts':
            changed_counts[0] = -1
        elif mutation == 'declarations':
            declarations = {}
        elif mutation == 'dimensions':
            changed_rows = rows[:, :-1]
        else:
            changed_rows[0, 1] = float('nan')
        try:
            fit_weak_audit_projection(prior, changed_rows, target, changed_counts,
                                       [design['audit']] * 2, base['penalties'],
                                       declarations=declarations)
        except ValueError:
            checks.append('reject_' + mutation)
        else:
            raise AssertionError('Accepted invalid ' + mutation)

    inputs = [
        'tools/weak_audit_checks.py', 'src/causalbank/weak_audit_projection.py',
        'src/causalbank/funding_calibration.py', 'src/causalbank/streaming_pilot.py',
        'src/causalbank/linkage_sets.py', 'docs/studies/weak-audit-projection-spec.json',
        spec['base'], spec['observation'],
    ]
    receipt = dict(status='pass', date='2026-10-11', checks=checks, issues=[],
                   scope='Independent dense arithmetic and exact-binomial enumeration under selected synthetic fixtures; no general coverage proof.',
                   input_sha256={name: digest(name) for name in sorted(inputs)})
    path = ROOT / 'docs/reviews/weak-audit-projection-checks.json'
    path.write_text(json.dumps(receipt, indent=2) + '\n')
    print(f'Weak-audit independent checks: {len(checks)} pass.')


if __name__ == '__main__':
    with threadpool_limits(limits=1):
        main()
