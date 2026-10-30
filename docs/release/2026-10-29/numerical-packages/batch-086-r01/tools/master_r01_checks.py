#!/usr/bin/env python3
"""Exact conditional expectation and independent dense algebra fixtures."""
import json
from pathlib import Path
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
from causalbank.linked_funding import pseudo_rows
from causalbank.funding_calibration import pilot_data
from causalbank.streaming_pilot import train_streaming_pilot
from causalbank.replicated_funding import control_score
from master_experiment import atomic


def main():
    results = {}
    for assumed in (.2, .5):
        total = 0.
        for v, pv in [(0., 2/3), (-np.sqrt(3), 1/6), (np.sqrt(3), 1/6)]:
            for correct in (0, 1):
                for audited, pr in [(0, .8), (1, .2)]:
                    focal, companion = 2*v+3, -v+5
                    first, second = (focal, companion) if correct else (companion, focal)
                    rows = np.array([[0, v-.2, 1, 0, -1, first, second]])
                    audit = (np.array([audited]), np.array([float(correct) if audited else np.nan]), np.array([assumed]))
                    coefficient = np.zeros((6, 2)); coefficient[0, 1] = 7.
                    score = control_score(rows, audit, 0, np.ones(1), coefficient, 17.)[0]
                    total += pv*.5*pr*score
                    swapped = rows.copy(); swapped[:, 5:] = rows[:, 5:][:, ::-1]
                    relabel = (audit[0], np.where(audit[0], 1-audit[1], np.nan), audit[2])
                    assert np.allclose(control_score(swapped, relabel, 0, np.ones(1), coefficient, 17.), [score])
        results[f'exact_mean_assumed_q_{assumed}'] = total
    assert abs(results['exact_mean_assumed_q_0.2']-2) < 1e-12
    assert abs(results['exact_mean_assumed_q_0.5']-1.1) < 1e-12
    rng = np.random.default_rng(77819)
    n = 240
    rows = np.column_stack((rng.integers(0, 2, n), rng.normal(size=n), np.ones(n), rng.normal(size=(n, 2)), rng.normal(size=(n, 4))))
    info = (np.ones(n, dtype=int), np.ones(n), np.ones(n))
    data = pseudo_rows(rows, *info, 1)
    fit = train_streaming_pilot(data, [0., 1., 10.], 17)
    train, test = pilot_data(data[:120]), pilot_data(data[120:])
    yt, yv = np.column_stack((train['action'], train['outcomes'])), np.column_stack((test['action'], test['outcomes']))
    losses = []
    for penalty in [0., 1., 10.]:
        reg = np.diag([0.]+[np.sqrt(penalty)]*5)
        c = np.linalg.lstsq(np.vstack((train['x'], reg)), np.vstack((yt, np.zeros((6, 3)))), rcond=None)[0]
        losses.append(float(np.mean((yv-test['x']@c)**2/yt.var(axis=0))))
    assert np.allclose(losses, fit['validation_losses'], rtol=1e-12, atol=1e-12)
    full = pilot_data(data); yf = np.column_stack((full['action'], full['outcomes']))
    reg = np.diag([0.]+[np.sqrt(fit['penalty'])]*5)
    reference = np.linalg.lstsq(np.vstack((full['x'], reg)), np.vstack((yf, np.zeros((6, 3)))), rcond=None)[0]
    assert np.allclose(reference, fit['coefficient'], atol=1e-12)
    results.update(status='pass', dense_coefficient_max_error=float(abs(reference-fit['coefficient']).max()),
                   scope='Exact discrete expectation, label permutation and independent dense chronological pilot; no coverage calibration data used.')
    atomic(ROOT/'docs/program/master/work/R01/fixtures.json', results)
    print(json.dumps(results))


if __name__ == '__main__':
    main()
