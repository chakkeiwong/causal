#!/usr/bin/env python3
"""Exact subject-level event covariance and sequential-TV witness for S5."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-17/s5'

def serial(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {k: serial(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [serial(v) for v in value]
    return value


def calculate():
    d, p = F(3, 25), F(3, 5)
    no_event = 1 - d - p
    one_period = {'D': d, 'P': p, 'N': no_event}
    paths = {}
    means = [F(0), F(0), F(0)]
    second = [[F(0) for _ in range(3)] for __ in range(3)]
    for first, later in product(one_period, repeat=2):
        probability = one_period[first] * one_period[later]
        active = F(2 if first == 'N' else 1)
        default = F(first == 'D' or (first == 'N' and later == 'D'))
        prepayment = F(first == 'P' or (first == 'N' and later == 'P'))
        x = [active, default, prepayment]
        paths[first + later] = dict(probability=probability,
            active_periods=active, default=default, prepayment=prepayment)
        means = [a + probability * b for a, b in zip(means, x)]
        second = [[second[i][j] + probability * x[i] * x[j]
                   for j in range(3)] for i in range(3)]
    covariance = [[second[i][j] - means[i] * means[j]
                   for j in range(3)] for i in range(3)]
    coefficients = [F(20), F(-1000), F(-50)]
    value_mean = sum(c * m for c, m in zip(coefficients, means)) - 3
    value_variance = sum(coefficients[i] * covariance[i][j] * coefficients[j]
                         for i in range(3) for j in range(3))
    diagonal_only = sum(coefficients[i] ** 2 * covariance[i][i]
                        for i in range(3))
    assert means == [F(32, 25), F(96, 625), F(96, 125)]
    assert covariance == [
        [F(126, 625), F(-147, 15625), F(-147, 3125)],
        [F(-147, 15625), F(50784, 390625), F(-9216, 78125)],
        [F(-147, 3125), F(-9216, 78125), F(2784, 15625)]]

    # Maximal coupling of kernels with uniform TV error epsilon, recursively.
    eps, horizon, margin, terminal = F(1, 50), 3, F(20), F(1000)
    divergence = [F(0)]
    for _ in range(horizon):
        divergence.append(divergence[-1] + (1 - divergence[-1]) * eps)
    sharp_error = sum(margin * q for q in divergence[:-1]) + terminal * divergence[-1]
    loose_divergence = [F(i) * eps for i in range(horizon + 1)]
    loose_error = sum(margin * q for q in loose_divergence[:-1]) + terminal * loose_divergence[-1]
    # The approximation enters an absorbing failure state with probability eps
    # at each still-matched transition; the reference never does.
    states = {'matched': F(1), 'diverged': F(0)}
    witness = [F(0)]
    for _ in range(horizon):
        matched, diverged = states['matched'], states['diverged']
        states = {'matched': matched * (1 - eps),
                  'diverged': diverged + matched * eps}
        witness.append(states['diverged'])
    assert witness == divergence
    assert sharp_error == F(60) and loose_error == F(306, 5)
    return serial(dict(status='exact_authored_reference',
        event_law=dict(period_default=d, period_prepayment=p,
                       period_no_event=no_event, horizons=2, path_probabilities=paths),
        vector=['restricted_active_periods','default_by_horizon','prepayment_by_horizon'],
        mean=means, covariance=covariance,
        monetary_coefficients=coefficients, net_mean_USD=value_mean,
        net_variance_USD_squared=value_variance,
        diagonal_only_variance_USD_squared=diagonal_only,
        diagonal_minus_full_variance_USD_squared=diagonal_only-value_variance,
        independent_subject_mean_variance=dict(n_subjects=1000,
            net_USD_squared=value_variance/F(1000)),
        tv=dict(horizon=horizon,epsilon=eps,sharp_history_divergence=divergence,
            additive_history_bound=loose_divergence,
            sharp_running_terminal_total_error_USD=sharp_error,
            additive_running_terminal_total_error_USD=loose_error,
            constructed_absorbing_divergence_witness=witness)))


def separate(saved):
    assert calculate() == saved
    # Re-derive the covariance using indicator identities, without path products.
    s, fd, fp = F(7, 25), F(96, 625), F(96, 125)
    cov = [list(map(F, row)) for row in saved['covariance']]
    assert cov[0][0] == s * (1-s)
    assert cov[0][1] == -F(3,25) * s**2
    assert cov[0][2] == -F(3,5) * s**2
    assert cov[1][1] == fd * (1-fd)
    assert cov[2][2] == fp * (1-fp)
    assert cov[1][2] == -fd * fp
    c = list(map(F, saved['monetary_coefficients']))
    reconstructed = sum(c[i]*cov[i][j]*c[j] for i in range(3) for j in range(3))
    assert reconstructed == F(saved['net_variance_USD_squared'])
    # Reconstruct the maximal-coupling error as probabilities of first split.
    eps = F(1,50)
    q = [F(0)]
    for t in range(3):
        first_split = (1-q[t])*eps
        q.append(q[t]+first_split)
    assert list(map(str,q)) == saved['tv']['sharp_history_divergence']
    return dict(status='pass',method='Independent indicator covariance identities and first-split coupling recursion.',
        off_diagonal_terms_required=True,variance_identity='c^T Sigma c',
        history_coupling='d_next=d+(1-d)epsilon; absorbing witness attains every step',
        limitations=['Author algebra and constructed laws; not an upstream, empirical or bank study.'])


def main():
    out=BASE/'covariance-results.json'
    data=calculate()
    assert not out.exists()
    out.write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(separate(data)))


if __name__ == '__main__':
    main()
