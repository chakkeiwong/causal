#!/usr/bin/env python3
"""Independent inverse/covariance and analytic checks of the printed examples."""
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.linalg import expm

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-13/python-discovery'


def ref(p, anchor):
    return {'path': str(p.relative_to(ROOT)), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'anchor': anchor}


def number(v):
    return float(Fraction(v))


def main():
    oracle = BASE/'oracle-results.json'
    d = json.loads(oracle.read_text())
    f = d['funding']
    w = np.array([[number(x) for x in r] for r in f['row_source_W']])
    inverse = np.linalg.inv(np.eye(3)-w)
    np.testing.assert_allclose(inverse[0]*0.25, [0.25, 1, 0.25], atol=1e-14)
    assert np.linalg.inv(np.eye(3)-w.T)[0, 2] == 0
    np.testing.assert_allclose(inverse, [[number(x) for x in r] for r in f['total_row_source']])

    forward = np.array([[0., .6], [0., 0.]])
    reverse = forward.T
    covariances = []
    for a, noise in [(forward, np.diag([1., .64])), (reverse, np.diag([.64, 1.]))]:
        t = np.linalg.inv(np.eye(2)-a)
        covariances.append(t.T@noise@t)
    np.testing.assert_allclose(covariances[0], covariances[1], rtol=0, atol=1e-14)
    assert np.linalg.inv(np.eye(2)-forward)[0, 1] == .6
    assert np.linalg.inv(np.eye(2)-reverse)[0, 1] == 0
    scaling = np.diag([1., 10.])
    scaled_covariance = scaling@covariances[0]@scaling
    for a, expected_loss, expected_l1 in [(forward, 32.5, 6.), (reverse, 50.32, .06)]:
        scaled_a = np.linalg.inv(scaling)@a@scaling
        residual = (np.eye(2)-scaled_a).T@scaled_covariance@(np.eye(2)-scaled_a)
        np.testing.assert_allclose(np.trace(residual)/2, expected_loss, atol=1e-12)
        np.testing.assert_allclose(np.abs(scaled_a).sum(), expected_l1, atol=1e-12)

    cycle = np.array([[0., .005], [.005, 0.]])
    squared = cycle*cycle
    c = d['cyclic']
    computed = {'exponential_h': np.trace(expm(squared))-2,
                'polynomial_h_d2': np.trace(np.linalg.matrix_power(np.eye(2)+squared/2, 2))-2,
                'logdet_h_s1': -np.linalg.slogdet(np.eye(2)-squared)[1]}
    for key, value in computed.items():
        np.testing.assert_allclose(value, c[key], rtol=1e-6, atol=1e-15)
        assert 0 < value < 1e-8
    assert np.all(cycle[[0, 1], [1, 0]] > .001)

    # Reconstruct selected covariance through the orthogonal half-normal basis.
    rotation = np.array([[1., 1.], [1., -1.]])/math.sqrt(2)
    selected = rotation@np.diag([1-2/math.pi, 1.])@rotation.T
    np.testing.assert_allclose(selected[0, 1], d['selection']['selected_covariance'])
    np.testing.assert_allclose(selected[0, 1]/selected[0, 0], d['selection']['selected_correlation'])
    assert round(d['duplicated_rows']['unit_Z'], 3) == .988
    assert round(d['duplicated_rows']['naive_row_Z'], 3) == 3.168

    result = {'status': 'pass', 'scope': 'Independent deterministic checks; no package execution or empirical qualification',
              'methods': ['Matrix inverse versus rational finite path sum', 'Independent-noise covariance reconstruction',
                          'Scaled covariance residual loss', 'SciPy matrix exponential / polynomial / determinant',
                          'Orthogonal-basis selected covariance', 'CI statistic arithmetic'],
              'examples': ref(oracle, 'Exact generated examples under review'),
              'review_code': ref(Path(__file__), 'Independent numerical formulations'),
              'numpy_version': np.__version__, 'matrix_residuals': computed,
              'findings': ['Funding increment USD0.25million and transpose error reproduced.',
                           'Equal observational Gaussian laws and distinct interventions reproduced.',
                           'Scale-dependent losses and small-residual cycle reproduced.',
                           'Selection-induced association and duplicated-row statistic reproduced.']}
    p = BASE/'reproduction-review.json'
    if p.exists():
        assert json.loads(p.read_text()) == result
    else:
        p.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'status': 'pass', 'checks': len(result['methods'])}))


if __name__ == '__main__':
    main()
