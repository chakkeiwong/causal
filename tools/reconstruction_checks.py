#!/usr/bin/env python3
"""Exact finite witnesses for the foundations draft; no bank-performance claims."""
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def prob(value, p):
    return p if value else 1 - p


def static():
    cells = {}
    for u, a, y in product(range(2), repeat=3):
        p = F(1, 5) + F(3, 5) * u
        cells[a, y] = cells.get((a, y), 0) + F(1, 2) * prob(a, p) * prob(y, p)
    other = {(a, y): F(1, 2) * prob(y, F(8, 25) + F(9, 25) * a)
             for a, y in product(range(2), repeat=2)}
    assert cells == other
    collider = {(a, v): F(1, 4) for a, v in product(range(2), repeat=2)}
    selected = {k: p for k, p in collider.items() if k[0] == k[1]}
    assert sum(p * v for (a, v), p in selected.items() if a) / sum(
        p for (a, v), p in selected.items() if a) == 1
    return {"observed_cells": {str(k): str(v) for k, v in sorted(cells.items())},
            "ate_models": [0, 0.36], "consistency_bounds": [-0.32, 0.68],
            "collider_true_effect": 0, "collider_selected_contrast": 1}


def instrument():
    strata = [(F(2, 5), (0, 1), [(0, 1), (0, 1)]),
              (F(3, 10), (1, 1), [(1, 1), (0, 1)]),
              (F(3, 10), (0, 0), [(0, 0), (0, 1)])]
    laws, ates = [], []
    for model in range(2):
        law = {}
        ate = F(0)
        for p, action, outcome in strata:
            ate += p * (outcome[model][1] - outcome[model][0])
            for z in range(2):
                a = action[z]
                k = (z, a, outcome[model][a])
                law[k] = law.get(k, 0) + p / 2
        laws.append(law)
        ates.append(ate)
    assert laws[0] == laws[1] and ates == [F(2, 5), F(1)]
    means = {z: [sum(2 * p * k[j] for k, p in laws[0].items() if k[0] == z)
                 for j in [1, 2]] for z in range(2)}
    first = means[1][0] - means[0][0]
    reduced = means[1][1] - means[0][1]
    assert reduced / first == 1
    return {"first_stage": float(first), "reduced_form": float(reduced),
            "late": 1, "ate_completions": [float(v) for v in ates],
            "direct_effect_bias": {"pi_0.4": float(F(1, 50) / F(2, 5)),
                                   "pi_0.02": float(F(1, 50) / F(1, 50))}}


def learning():
    p = {}
    e = {0: F(1, 4), 1: F(3, 4)}
    m = {(0, 0): F(1, 5), (0, 1): F(1, 2),
         (1, 0): F(2, 5), (1, 1): F(4, 5)}
    eh = {0: F(2, 5), 1: F(3, 5)}
    mh = {k: v + F(1, 20) * (1 if k[1] else -1) for k, v in m.items()}
    for x, a, y in product(range(2), repeat=3):
        p[x, a, y] = F(1, 2) * prob(a, e[x]) * prob(y, m[x, a])

    def phi(x, a, y, ee, mm):
        return (mm[x, 1] - mm[x, 0] + a / ee[x] * (y - mm[x, 1])
                - (1 - a) / (1 - ee[x]) * (y - mm[x, 0]))

    theta = sum(m[x, 1] - m[x, 0] for x in range(2)) / 2
    bias = sum(v * phi(*k, eh, mh) for k, v in p.items()) - theta
    remainder = sum((eh[x] - e[x]) * ((mh[x, 1] - m[x, 1]) / eh[x]
                     + (mh[x, 0] - m[x, 0]) / (1 - eh[x])) for x in range(2)) / 2
    assert bias == remainder
    for ee, mm in [(e, mh), (eh, m)]:
        assert sum(v * phi(*k, ee, mm) for k, v in p.items()) == theta

    # Perturb the complete finite law; compare a functional derivative to E[phi S].
    raw = {k: F(2 * k[0] - k[1] + 3 * k[2] + k[0] * k[1]) for k in p}
    mean = sum(p[k] * raw[k] for k in p)
    score = {k: raw[k] - mean for k in p}
    eps = F(1, 100000)

    def functional(t):
        pt = {k: v * (1 + t * score[k]) for k, v in p.items()}
        total = F(0)
        for x in range(2):
            px = sum(v for k, v in pt.items() if k[0] == x)
            conditional = []
            for a in range(2):
                mass = sum(v for k, v in pt.items() if k[:2] == (x, a))
                conditional.append(sum(v * k[2] for k, v in pt.items()
                                       if k[:2] == (x, a)) / mass)
            total += px * (conditional[1] - conditional[0])
        return total

    numeric = (functional(eps) - functional(-eps)) / (2 * eps)
    gradient = sum(v * (phi(*k, e, m) - theta) * score[k] for k, v in p.items())
    assert abs(float(numeric - gradient)) < 1e-8
    projection = F(99, 10000) * 10 / (F(1, 4) + F(99, 10000))
    return {"aipw_exact_bias": str(bias), "derived_remainder": str(remainder),
            "double_robustness_cases": "both passed exactly",
            "functional_derivative": float(numeric), "gradient_inner_product": float(gradient),
            "derivative_error": abs(float(numeric - gradient)),
            "heterogeneous_ate": 5, "constant_r_projection": float(projection)}


def longitudinal():
    def e0(l):
        return F(1, 5) + F(3, 5) * l

    def l1p(l, a):
        return F(1, 10) + F(1, 2) * l + F(1, 5) * a

    def e1(l, a, m):
        return F(3, 20) + F(1, 2) * m + F(1, 10) * a

    def y(l, a, m, b):
        return F(20 + 3 * a + 4 * b + 10 * m + 6 * l)

    cells = {(l, a, m, b): F(1, 2) * prob(a, e0(l)) * prob(m, l1p(l, a))
             * prob(b, e1(l, a, m)) for l, a, m, b in product(range(2), repeat=4)}
    assert sum(cells.values()) == 1
    regime = {}
    for action in range(2):
        gformula = sum(F(1, 2) * prob(m, l1p(l, action)) * y(l, action, m, action)
                       for l, m in product(range(2), repeat=2))
        ipw = sum(p * y(l, a, m, b) / prob(a, e0(l)) / prob(b, e1(l, a, m))
                  for (l, a, m, b), p in cells.items() if a == b == action)
        assert gformula == ipw
        regime[action] = gformula
    moment0 = sum(p * (a - e0(l)) * (y(l, a, m, b) - 4 * b - 5 * a)
                  for (l, a, m, b), p in cells.items())
    moment1 = sum(p * (b - e1(l, a, m)) * (y(l, a, m, b) - 4 * b)
                  for (l, a, m, b), p in cells.items())
    wrong = sum(p * (a - e0(l)) * (y(l, a, m, b) - 4 * b - 3 * a)
                for (l, a, m, b), p in cells.items())
    assert moment0 == moment1 == 0 and wrong != 0

    g0 = lambda l: F(9, 20) + F(1, 10) * l
    g1 = lambda l, a, m: F(13, 20) - F(1, 5) * m
    eh0 = lambda l: F(3, 10) + F(2, 5) * l
    eh1 = lambda l, a, m: F(1, 4) + F(7, 20) * m + F(1, 20) * a
    q1 = {(l, a, m, b): y(l, a, m, b) for l, a, m, b in cells}
    v1 = {(l, a, m): sum(prob(b, g1(l, a, m)) * q1[l, a, m, b] for b in range(2))
          for l, a, m in product(range(2), repeat=3)}
    q0 = {(l, a): sum(prob(m, l1p(l, a)) * v1[l, a, m] for m in range(2))
          for l, a in product(range(2), repeat=2)}
    target = sum(F(1, 2) * prob(a, g0(l)) * q0[l, a] for l, a in q0)
    qh0 = {k: v + F(7, 10) - F(1, 5) * k[0] + F(1, 10) * k[1]
           for k, v in q0.items()}
    qh1 = {k: v + F(1, 2) - F(1, 4) * k[2] + F(1, 10) * k[3]
           for k, v in q1.items()}

    def augmented(qzero, qone, ezero, eone):
        vone = {(l, a, m): sum(prob(b, g1(l, a, m)) * qone[l, a, m, b]
                               for b in range(2)) for l, a, m in v1}
        vzero = {l: sum(prob(a, g0(l)) * qzero[l, a] for a in range(2)) for l in range(2)}
        val = F(0)
        for (l, a, m, b), p in cells.items():
            w0 = prob(a, g0(l)) / prob(a, ezero(l))
            w1 = w0 * prob(b, g1(l, a, m)) / prob(b, eone(l, a, m))
            val += p * (vzero[l] + w0 * (vone[l, a, m] - qzero[l, a])
                        + w1 * (y(l, a, m, b) - qone[l, a, m, b]))
        return val

    assert augmented(qh0, qh1, e0, e1) == target
    assert augmented(q0, q1, eh0, eh1) == target
    rem0 = sum(F(1, 2) * prob(a, g0(l)) * (1 - prob(a, e0(l)) / prob(a, eh0(l)))
               * (qh0[l, a] - q0[l, a]) for l, a in q0)
    rem1 = F(0)
    for (l, a, m, b), p in cells.items():
        w0 = prob(a, g0(l)) / prob(a, eh0(l))
        rem1 += p * w0 * sum(prob(c, g1(l, a, m))
                             * (1 - prob(c, e1(l, a, m)) / prob(c, eh1(l, a, m)))
                             * (qh1[l, a, m, c] - q1[l, a, m, c]) for c in range(2))
    bias = augmented(qh0, qh1, eh0, eh1) - target
    assert bias == rem0 + rem1
    return {"never": float(regime[0]), "always": float(regime[1]),
            "effect": float(regime[1] - regime[0]), "gformula_ipw_equal": True,
            "snmm_moments": [str(moment0), str(moment1)], "wrong_early_blip_moment": str(wrong),
            "fixed_policy_value": float(target), "dr_remainder": str(bias),
            "two_period_remainder_equal": True}


def filtering():
    mu = [F(1, 2), F(1, 2)]
    q = [F(1, 5), F(4, 5)]
    pstate = [[F(4, 5), F(1, 5)], [F(3, 10), F(7, 10)]]
    signal = [F(1, 4), F(3, 4)]
    reward = [[F(1, 5), F(2, 5)], [F(3, 5), F(4, 5)]]
    # Observe action=1, reward=1, signal=1; enumerate the latent path directly.
    joint = {(s, sp): mu[s] * q[s] * pstate[s][sp] * reward[s][sp] * signal[sp]
             for s, sp in product(range(2), repeat=2)}
    likelihood = sum(joint.values())
    posterior = [sum(p for (s, sp), p in joint.items() if sp == j) / likelihood
                 for j in range(2)]
    action_mass = sum(mu[s] * q[s] for s in range(2))
    updated = [mu[s] * q[s] / action_mass for s in range(2)]
    forward = [signal[j] * sum(updated[s] * pstate[s][j] * reward[s][j]
                              for s in range(2)) for j in range(2)]
    normalizer = sum(forward)
    assert [v / normalizer for v in forward] == posterior
    assert action_mass * normalizer == likelihood
    selected = [F(1, 5), F(4, 5)]
    obs_mean = sum(selected[s] * (F(1, 5) + F(3, 5) * s) for s in range(2))
    intervention_mean = sum(mu[s] * (F(1, 5) + F(3, 5) * s) for s in range(2))
    assert obs_mean == F(17, 25) and intervention_mean == F(1, 2)
    return {"enumerated_likelihood": str(likelihood),
            "forward_likelihood_equal": True, "posterior": [str(v) for v in posterior],
            "private_logger_observed_mean_a1": float(obs_mean),
            "intervention_mean_a1": float(intervention_mean)}


def inverse_proxies():
    # Work with complete finite laws, not fitted coefficients or source code outputs.
    rows = [[F(1, 2), F(1, 2), F(0)], [F(0), F(1, 2), F(1, 2)]]
    h, alternate = [1, 2, 3], [2, 1, 4]
    assert [sum(x * y for x, y in zip(r, h)) for r in rows] == [
        sum(x * y for x, y in zip(r, alternate)) for r in rows]
    weights = [F(1, 4), F(1, 2), F(1, 4)]
    assert sum(x * y for x, y in zip(weights, h)) == sum(
        x * y for x, y in zip(weights, alternate)) == 2
    law = {}
    for u, a, z, w in product(range(2), repeat=4):
        law[u, a, z, w] = F(1, 2) * prob(a, F(1, 5) + F(3, 5) * u) * prob(
            z, F(3, 10) + F(2, 5) * u) * prob(w, F(1, 10) + F(4, 5) * u)
    assert sum(law.values()) == 1
    outcome_bridge = lambda w, a: 2 * a - F(3, 8) + F(15, 4) * w
    # Solve observed bridge equations, with rational 2x2 inverses.
    recovered, tbridge, determinants = {}, {}, {}
    for a in range(2):
        matrix, rhs = [], []
        for z in range(2):
            part = {k: p for k, p in law.items() if k[1:3] == (a, z)}
            mass = sum(part.values())
            matrix.append([sum(p for k, p in part.items() if k[3] == w) / mass for w in range(2)])
            rhs.append(sum(p * (2 * a + 3 * k[0]) for k, p in part.items()) / mass)
        det = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        determinants[a] = str(det)
        recovered[a] = [(rhs[0] * matrix[1][1] - rhs[1] * matrix[0][1]) / det,
                        (matrix[0][0] * rhs[1] - matrix[1][0] * rhs[0]) / det]
        assert recovered[a] == [outcome_bridge(w, a) for w in range(2)]
        # Treatment bridge: E[1{A=a} q(Z) | W=w] = 1.
        matrix = []
        for w in range(2):
            pw = sum(p for k, p in law.items() if k[3] == w)
            matrix.append([sum(p for k, p in law.items() if k[1:] == (a, z, w)) / pw
                           for z in range(2)])
        det = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        tbridge[a] = [(matrix[1][1] - matrix[0][1]) / det,
                      (matrix[0][0] - matrix[1][0]) / det]
    means = []
    remainders = []
    for a in range(2):
        theta = 2 * a + F(3, 2)
        means.append(float(sum(p * outcome_bridge(k[3], a) for k, p in law.items())))
        for correct_h, correct_q in product([False, True], repeat=2):
            val = rem = F(0)
            for (u, received, z, w), p in law.items():
                dh = F(0) if correct_h else F(1, 5) + F(1, 10) * w
                dq = F(0) if correct_q else F(1, 3) - F(1, 6) * z
                hb = outcome_bridge(w, a) + dh
                qb = tbridge[a][z] + dq
                val += p * (hb + (received == a) * qb * (2 * received + 3 * u - hb))
                rem -= p * (received == a) * dh * dq
            assert val - theta == rem
            if correct_h or correct_q:
                assert val == theta
            else:
                remainders.append(str(rem))
    raw = []
    for a in range(2):
        mass = sum(p for k, p in law.items() if k[1] == a)
        raw.append(sum(p * (2 * a + 3 * k[0]) for k, p in law.items() if k[1] == a) / mass)
    assert raw[1] - raw[0] == F(19, 5) and means[1] - means[0] == 2
    return {"nonunique_response_identified_average": 2,
            "unidentified_equal_weight_averages": [2, str(F(7, 3))],
            "raw_contrast": float(raw[1] - raw[0]), "proximal_means": means,
            "recovered_bridges": {str(a): [str(v) for v in h] for a, h in recovered.items()},
            "operator_determinants": determinants,
            "both_wrong_remainders": remainders, "all_bridge_remainders_exact": True}


def longer_horizon():
    horizon = 3

    def policy(h):
        t = (len(h) - 1) // 2
        return F(7, 20) + F(3, 20) * h[-1] - F(1, 20) * t + F(1, 40) * sum(h[1::2])

    law = {}
    for k in product(range(2), repeat=2 * horizon + 1):
        p = prob(k[0], F(2, 5))
        for t in range(horizon):
            h, a, l = k[:2 * t + 1], k[2 * t + 1], k[2 * t + 2]
            e = F(1, 5) + F(1, 10) * t + F(1, 5) * h[-1] + F(1, 20) * sum(h[1::2])
            p *= prob(a, e) * prob(l, F(1, 10) + F(1, 10) * t + F(1, 5) * h[-1] + F(3, 20) * a)
        law[k] = p

    def reconstruct(p):
        mass = {(): sum(p.values())}
        for length in range(1, 2 * horizon + 2):
            for k, v in p.items():
                prefix = k[:length]
                mass[prefix] = mass.get(prefix, F(0)) + v
        q, v, e = {}, {k: F(k[-1]) for k in p}, {}
        for t in reversed(range(horizon)):
            for h in product(range(2), repeat=2 * t + 1):
                for a in range(2):
                    ha = h + (a,)
                    e[ha] = mass[ha] / mass[h]
                    q[ha] = sum(mass[ha + (l,)] / mass[ha] * v[ha + (l,)] for l in range(2))
                v[h] = sum(prob(a, policy(h)) * q[h + (a,)] for a in range(2))
        target = sum(mass[(l,)] * v[(l,)] for l in range(2))
        return mass, q, v, e, target

    mass, q, v, e, target = reconstruct(law)

    def score(k, qq, ee):
        val = sum(prob(a, policy(k[:1])) * qq[k[:1] + (a,)] for a in range(2))
        weight = F(1)
        for t in range(horizon):
            h, ha = k[:2 * t + 1], k[:2 * t + 2]
            weight *= prob(ha[-1], policy(h)) / ee[ha]
            next_h = k[:2 * t + 3]
            next_v = F(k[-1]) if t == horizon - 1 else sum(
                prob(a, policy(next_h)) * qq[next_h + (a,)] for a in range(2))
            val += weight * (next_v - qq[ha])
        return val

    phi = {k: score(k, q, e) - target for k in law}
    assert sum(law[k] * phi[k] for k in law) == 0
    qbad = {h: x + F(1, 20) - F(1, 100) * sum(h) for h, x in q.items()}
    ebad = {h: F(1, 2) for h in e}
    bias = sum(p * score(k, qbad, ebad) for k, p in law.items()) - target
    rem = F(0)
    for k, p in law.items():
        prev = F(1)
        for t in range(horizon):
            h, ha = k[:2 * t + 1], k[:2 * t + 2]
            rem += p * prev * sum(prob(a, policy(h)) * (1 - e[h + (a,)] / ebad[h + (a,)])
                                  * (qbad[h + (a,)] - q[h + (a,)]) for a in range(2))
            prev *= prob(ha[-1], policy(h)) / ebad[ha]
    assert bias == rem
    for choices in product([False, True], repeat=horizon):
        qq = {h: (q[h] if choices[(len(h) - 2) // 2] else qbad[h]) for h in q}
        ee = {h: (ebad[h] if choices[(len(h) - 2) // 2] else e[h]) for h in e}
        assert sum(p * score(k, qq, ee) for k, p in law.items()) == target
    raw = {k: F(k[0] - 2 * k[1] + 3 * k[4] + k[1] * k[5]) for k in law}
    center = sum(law[k] * raw[k] for k in law)
    s = {k: raw[k] - center for k in law}
    eps = F(1, 100000)
    plus = reconstruct({k: p * (1 + eps * s[k]) for k, p in law.items()})[-1]
    minus = reconstruct({k: p * (1 - eps * s[k]) for k, p in law.items()})[-1]
    numeric = (plus - minus) / (2 * eps)
    inner = sum(law[k] * phi[k] * s[k] for k in law)
    assert abs(float(numeric - inner)) < 1e-8
    variance = sum(p * phi[k] ** 2 for k, p in law.items())
    parts = sum(mass[(l,)] * (v[(l,)] - target) ** 2 for l in range(2))
    for k, p in law.items():
        weight = F(1)
        for t in range(horizon):
            h, ha, hn = k[:2 * t + 1], k[:2 * t + 2], k[:2 * t + 3]
            weight *= prob(ha[-1], policy(h)) / e[ha]
            parts += p * weight ** 2 * (v[hn] - q[ha]) ** 2
    assert variance == parts
    return {"horizon": horizon, "cells": len(law), "value": float(target),
            "general_remainder": str(bias), "remainder_exact": True,
            "timewise_correctness_patterns": 8, "all_patterns_unbiased": True,
            "gradient_inner_product": float(inner), "directional_derivative": float(numeric),
            "derivative_error": abs(float(numeric - inner)),
            "score_variance": float(variance), "variance_decomposition_exact": True}


def weak_sets():
    # Known-covariance Gaussian inversion; equivalent direct test and quadratic.
    z = 1.959963984540054
    cases = [(0.2, 0.5, "bounded"), (0.2, 0.01, "disconnected"),
             (0.001, 0.01, "all_real")]
    results = []
    for nvalue, kvalue, expected in cases:
        vnn, vkk, vnk = 0.01, 0.01, 0.0
        aa = kvalue ** 2 - z ** 2 * vkk
        bb = -2 * nvalue * kvalue + 2 * z ** 2 * vnk
        cc = nvalue ** 2 - z ** 2 * vnn
        disc = bb ** 2 - 4 * aa * cc
        roots = sorted([(-bb - math.sqrt(disc)) / (2 * aa),
                        (-bb + math.sqrt(disc)) / (2 * aa)]) if disc >= 0 else []
        kind = "bounded" if aa > 0 and disc > 0 else (
            "disconnected" if aa < 0 and disc > 0 else "all_real")
        assert kind == expected
        for b in [-1e6, -100, -1, 0, 0.5, 1, 100, 1e6]:
            direct = (nvalue - b * kvalue) ** 2 <= z ** 2 * (vnn - 2 * b * vnk + b ** 2 * vkk)
            assert direct == (aa * b ** 2 + bb * b + cc <= 0)
        results.append({"N": nvalue, "kappa": kvalue, "set": kind, "boundary": roots})
    return {"known_covariance": [[0.01, 0], [0, 0.01]], "confidence": 0.95,
            "examples": results, "quadratic_and_direct_tests_agree": True}


def panels_time():
    """Independent finite projections and covariance identities for temporal claims."""
    d = [[F(x) for x in row] for row in ((0, 1, 1, 1), (0, 0, 0, 1), (0, 0, 0, 0))]
    rows = [sum(row) / 4 for row in d]
    cols = [sum(d[i][t] for i in range(3)) / 3 for t in range(4)]
    grand = sum(rows) / 3
    residual = [[d[i][t] - rows[i] - cols[t] + grand for t in range(4)] for i in range(3)]
    assert all(sum(row) == 0 for row in residual)
    assert all(sum(residual[i][t] for i in range(3)) == 0 for t in range(4))
    treated = [(i, t) for i in range(3) for t in range(4) if d[i][t]]
    denom = sum(residual[i][t] for i, t in treated)
    assert denom == sum(x * x for row in residual for x in row)
    weights = [residual[i][t] / denom for i, t in treated]
    effects = [F(1), F(1), F(20), F(1)]
    beta = sum(w * tau for w, tau in zip(weights, effects))
    assert weights == [F(3, 10), F(3, 10), -F(1, 10), F(1, 2)]
    assert beta == -F(9, 10) and sum(effects) / 4 == F(23, 4)

    # Rademacher innovations integrate the dynamic regression moments exactly.
    rho = F(7, 10)
    numerator = denominator = F(0)
    for u1, u2 in product((-1, 1), repeat=2):
        y0, y1, y2 = F(0), F(u1), rho * u1 + u2
        dx, dy = y1 - y0, y2 - y1
        numerator += dx * dy / 4
        denominator += dx * dx / 4
    assert numerator / denominator == rho - 1

    # Propagate basis innovations, not the stated aggregate recursion.
    # Test the identity for every coordinate of its linear input vector.
    for initial, *eps in ([int(i == j) for i in range(7)] for j in range(7)):
        x = [F(initial)]
        for e in eps:
            x.append(rho * x[-1] + e)
        s_prev, s_now = x[1] + x[2], x[3] + x[4]
        v = rho * eps[1] + (1 + rho) * eps[2] + eps[3]
        assert s_now - rho ** 2 * s_prev == v
    v_prev = {0: rho, 1: 1 + rho, 2: F(1)}
    v_now = {2: rho, 3: 1 + rho, 4: F(1)}
    cov = sum(v_prev.get(k, 0) * v_now.get(k, 0) for k in range(5))
    assert cov == rho
    coarse = [(r ** 2, 1 + r ** 2) for r in (rho, -rho)]
    assert coarse[0] == coarse[1] == (F(49, 100), F(149, 100))
    theta, sigma2 = F(2), F(3)
    gamma = [(1 + theta ** 2) * sigma2, theta * sigma2, F(0)]
    reverse = [(1 + 1 / theta ** 2) * theta ** 2 * sigma2,
               (1 / theta) * theta ** 2 * sigma2, F(0)]
    assert gamma == reverse and theta != 1 / theta

    # Sum the whole covariance matrix for a 3 by 4 crossed score array.
    variance = sum(F(i == j, 1) * 2 + F(t == s, 1) * 3 + F(i == j and t == s, 1) * 5
                   for i, t, j, s in product(range(3), range(4), range(3), range(4))) / 144
    assert variance == F(2, 3) + F(3, 4) + F(5, 12)
    return {"twfe_weights": list(map(str, weights)), "twfe": str(beta),
            "treated_cell_att": str(sum(effects) / 4), "short_panel_coefficient": str(numerator / denominator),
            "aggregate_linear_identity": True, "aggregate_noise_lag_covariance": str(cov),
            "subsampled_ar": list(map(str, coarse[0])), "ma_observed_autocovariances": list(map(str, gamma)),
            "ma_distinct_unit_impacts": [str(theta), str(1 / theta)], "crossed_score_mean_variance": str(variance)}


def discovery_observation():
    # Covariances computed from structural error loadings for three distinct DAGs.
    half = F(1, 2)
    models = [
        ([[1, 0, 0], [half, 1, 0], [F(1, 4), half, 1]], [1, F(3, 4), F(3, 4)]),
        ([[1, half, 0], [0, 1, 0], [0, half, 1]], [F(3, 4), 1, F(3, 4)]),
        ([[1, half, F(1, 4)], [0, 1, half], [0, 0, 1]], [F(3, 4), F(3, 4), 1])]
    covariances = [[[sum(F(a[i][k]) * variances[k] * a[j][k] for k in range(3))
                     for j in range(3)] for i in range(3)] for a, variances in models]
    assert all(c == covariances[0] for c in covariances)
    assert covariances[0][0][2] - covariances[0][0][1] * covariances[0][1][2] == 0
    # Full observed law, including the missingness indicator, agrees at the endpoints.
    recorded = []
    means = []
    for missing_success in (F(0), F(1)):
        obs, mean = {}, F(0)
        for r, y in product(range(2), repeat=2):
            p = half * prob(y, half if r else missing_success)
            obs[r, r * y] = obs.get((r, r * y), F(0)) + p
            mean += p * y
        recorded.append(obs)
        means.append(mean)
    assert recorded[0] == recorded[1] and means == [F(1, 4), F(3, 4)]
    # Enumerate the misclassified randomized experiment independently of inversion.
    matrix = [[F(4, 5), F(1, 5)], [F(1, 5), F(4, 5)]]
    observed = [[F(0) for y in range(2)] for w in range(2)]
    truth = [[half * prob(y, F(1, 5) + F(3, 5) * a) for y in range(2)] for a in range(2)]
    for a, w, y in product(range(2), repeat=3):
        observed[w][y] += truth[a][y] * matrix[w][a]
    inverse = [[F(4, 3), -F(1, 3)], [-F(1, 3), F(4, 3)]]
    recovered = [[sum(inverse[a][w] * observed[w][y] for w in range(2)) for y in range(2)] for a in range(2)]
    assert recovered == truth
    raw_effect = observed[1][1] / sum(observed[1]) - observed[0][1] / sum(observed[0])
    assert raw_effect == F(9, 25)
    return {"three_dag_common_covariance": [[str(v) for v in row] for row in covariances[0]],
            "effects_by_graph": ["1/4", "0", "0"], "missingness_same_recorded_law": True,
            "missing_outcome_mean_endpoints": list(map(str, means)),
            "misclassified_contrast": str(raw_effect), "corrected_randomized_effect": "3/5",
            "known_measurement_matrix_recovers_true_joint": True}


def controlled_choice():
    e = [[F(4, 5), F(1, 5)], [F(1, 5), F(4, 5)]]
    left = [[F(4, 3), -F(1, 3)], [-F(1, 3), F(4, 3)]]
    mu = [F(3, 5), F(2, 5)]
    transitions = [[[F(4, 5), F(1, 5)], [F(3, 10), F(7, 10)]],
                   [[F(3, 5), F(2, 5)], [F(1, 10), F(9, 10)]]]
    observed_matrices = []
    marked_errors = []
    for action, tmat in enumerate(transitions):
        joint = [[sum(mu[s] * e[o][s] * tmat[s][sp] * e[op][sp]
                      for s, sp in product(range(2), repeat=2)) for op in range(2)] for o in range(2)]
        recovered = [[sum(left[s][o] * joint[o][op] * left[sp][op]
                          for o, op in product(range(2), repeat=2)) / mu[s]
                      for sp in range(2)] for s in range(2)]
        assert recovered == tmat
        observed_matrices.append([[str(v) for v in row] for row in joint])
        category_recoveries = []
        for reward in (0, 1):
            marked = [[sum(mu[s] * e[o][s] * tmat[s][sp] * e[op][sp]
                           * prob(reward, F(1, 10) + F(1, 5)*action + F(3, 20)*s + F(1, 4)*sp)
                           for s, sp in product(range(2), repeat=2))
                       for op in range(2)] for o in range(2)]
            recovered_mark = [[sum(left[s][o] * marked[o][op] * left[sp][op]
                                   for o, op in product(range(2), repeat=2)) / mu[s]
                               for sp in range(2)] for s in range(2)]
            reference = [[tmat[s][sp] * prob(reward, F(1, 10) + F(1, 5)*action
                                            + F(3, 20)*s + F(1, 4)*sp)
                          for sp in range(2)] for s in range(2)]
            marked_errors.append(max(abs(recovered_mark[s][sp] - reference[s][sp])
                                     for s, sp in product(range(2), repeat=2)))
            assert recovered_mark == reference
            category_recoveries.append(recovered_mark)
        assert [[sum(k[s][sp] for k in category_recoveries) for sp in range(2)]
                for s in range(2)] == tmat
    # Identical state/transition/signal/mean-reward summaries can lose policy information.
    reward_information_values = []
    for informative in (False, True):
        law = {}
        for s, o, sign in product(range(2), range(2), (-1, 1)):
            reward = sign * (s + 1 if informative else 1)
            law[s, o, reward] = F(1, 4) * e[o][s]
        assert all(sum(mass * reward for (state, o, reward), mass in law.items()
                       if state == s) == 0 for s in range(2))
        value = sum(max(sum(mass for (s, oo, rr), mass in law.items()
                            if (oo, rr, s) == (o, reward, action)) for action in range(2))
                    for o, reward in {(o, r) for s, o, r in law})
        reward_information_values.append(value)
    assert reward_information_values == [F(4, 5), F(1)]
    # Value iteration is independent of the analytic scalar-root calculation in the text.
    def solve_ddc(utilities, trans):
        value = [0.0, 0.0]
        for _ in range(500):
            action_values = [[utilities[s] + 0.5 * sum(trans[a][s][sp] * value[sp] for sp in range(2))
                              for a in range(2)] for s in range(2)]
            updated = [max(v) + math.log(sum(math.exp(x - max(v)) for x in v)) for v in action_values]
            error = max(abs(updated[s] - value[s]) for s in range(2))
            value = updated
            if error < 1e-13:
                break
        else:
            raise AssertionError("DDC solver did not converge")
        probabilities = []
        for s in range(2):
            av = [utilities[s] + 0.5 * sum(trans[a][s][sp] * value[sp] for sp in range(2)) for a in range(2)]
            probabilities.append(1 / (1 + math.exp(av[0] - av[1])))
        return value, probabilities
    identity = [[1, 0], [0, 1]]
    baseline = [solve_ddc(u, [identity, identity]) for u in ([0, 0], [0, 1])]
    assert baseline[0][1] == baseline[1][1] == [0.5, 0.5]
    assert max(abs(baseline[1][0][s] - baseline[0][0][s] - [0, 2][s]) for s in range(2)) < 1e-12
    changed = [solve_ddc(u, [identity, [[0, 1], [0, 1]]]) for u in ([0, 0], [0, 1])]
    z = (1 + math.sqrt(1 + 8 * math.e)) / 2
    assert abs(changed[1][1][0] - (1 - 1 / z)) < 1e-12
    assert changed[0][1][0] == 0.5 and changed[1][1][0] > 0.5
    return {"randomized_observation_matrices": observed_matrices, "recovered_transitions_exactly": True,
            "marked_reward_kernel_maximum_errors": [str(v) for v in marked_errors],
            "same_mean_reward_different_information_values": [str(v) for v in reward_information_values],
            "historical_choice_probabilities": [x[1] for x in baseline],
            "changed_transition_choice_probabilities": [x[1] for x in changed],
            "analytic_and_iterated_choice_probability_agree": True}


def policy_transport():
    # Front-door: enumerate the latent SCM, then use only its observed law.
    observed = {}
    for u, a, m, y in product(range(2), repeat=4):
        mass = (F(1, 2) * prob(a, F(1, 5) + F(3, 5) * u)
                * prob(m, F(1, 10) + F(7, 10) * a)
                * prob(y, F(1, 10) + F(1, 2) * m + F(1, 5) * u))
        observed[a, m, y] = observed.get((a, m, y), 0) + mass
    pa = {a: sum(v for (aa, m, y), v in observed.items() if aa == a) for a in range(2)}
    pam = {(a, m): sum(v for (aa, mm, y), v in observed.items() if (aa, mm) == (a, m))
           for a, m in product(range(2), repeat=2)}
    ym = {(a, m): observed[a, m, 1] / pam[a, m] for a, m in pam}
    frontdoor = {a: sum(pam[a, m] / pa[a] * sum(pa[b] * ym[b, m] for b in range(2))
                        for m in range(2)) for a in range(2)}
    intervened = {a: sum(F(1, 2) * prob(m, F(1, 10) + F(7, 10) * a)
                         * (F(1, 10) + F(1, 2) * m + F(1, 5) * u)
                         for u, m in product(range(2), repeat=2)) for a in range(2)}
    naive = {a: sum(v * y for (aa, m, y), v in observed.items() if aa == a) / pa[a]
             for a in range(2)}
    assert frontdoor == intervened == {0: F(1, 4), 1: F(3, 5)}
    assert naive[1] - naive[0] == F(47, 100)

    # Directional derivatives under perturbations of the complete observed law.
    p = {(x, a, y): F(1, 2) * prob(a, F(1, 4) + F(1, 2) * x)
         * prob(y, F(1, 10) + F(1, 5) * x + F(3, 10) * a)
         for x, a, y in product(range(2), repeat=3)}

    def components(law):
        px = {x: sum(v for (xx, a, y), v in law.items() if xx == x) for x in range(2)}
        xa = {(x, a): sum(v for (xx, aa, y), v in law.items() if (xx, aa) == (x, a))
              for x, a in product(range(2), repeat=2)}
        ee = {x: xa[x, 1] / px[x] for x in px}
        mm = {(x, a): law[x, a, 1] / xa[x, a] for x, a in xa}
        return px, ee, mm

    def target(law, mode):
        px, ee, mm = components(law)
        if mode == 'incremental':
            delta = F(3, 2)
            return sum(px[x] * (delta * ee[x] * mm[x, 1] + (1-ee[x]) * mm[x, 0])
                       / (1+(delta-1)*ee[x]) for x in px)
        return sum(px[x] * (ee[x] * mm[x, 0] + (1-ee[x]) * mm[x, 1]) for x in px)

    px, ee, mm = components(p)
    raw = {k: F(2*k[0] - k[1] + 3*k[2] + k[0]*k[1]) for k in p}
    center = sum(p[k]*raw[k] for k in p)
    score = {k: raw[k]-center for k in p}
    eps = F(1, 10**6)
    plus = {k: v*(1+eps*score[k]) for k, v in p.items()}
    minus = {k: v*(1-eps*score[k]) for k, v in p.items()}
    derivative_errors = {}
    for mode in ('incremental', 'modified'):
        theta = target(p, mode)
        gradient = {}
        for (x, a, y) in p:
            if mode == 'incremental':
                delta = F(3, 2)
                den = 1+(delta-1)*ee[x]
                value = (delta*ee[x]*mm[x, 1]+(1-ee[x])*mm[x, 0])/den
                phi = ((delta*a+1-a)/den*(y-mm[x, a])+value-theta
                       +delta*(mm[x, 1]-mm[x, 0])*(a-ee[x])/den**2)
            else:
                ratio = prob(1-a, ee[x])/prob(a, ee[x])
                phi = ratio*(y-mm[x, a])+mm[x, 1-a]-theta
            gradient[x, a, y] = phi
        assert sum(p[k]*gradient[k] for k in p) == 0
        numeric = (target(plus, mode)-target(minus, mode))/(2*eps)
        analytic = sum(p[k]*score[k]*gradient[k] for k in p)
        derivative_errors[mode] = abs(float(numeric-analytic))
        assert derivative_errors[mode] < 1e-9
    observed_mean = sum(v*y for (x, a, y), v in p.items())
    for (x, a, y) in p:
        value = ee[x]*mm[x, 1]+(1-ee[x])*mm[x, 0]
        phi_one = y-mm[x, a]+value-observed_mean+(mm[x, 1]-mm[x, 0])*(a-ee[x])
        assert phi_one == y-observed_mean

    # Pooled source/target experiment: outcome only exists in source records.
    law = {(0, x, -1, -1): F(2, 5)*prob(x, F(4, 5)) for x in range(2)}
    law.update({(1, x, a, y): F(3, 5)*prob(x, F(1, 5))
                * prob(a, F(1, 4)+F(1, 2)*x)
                * prob(y, F(1, 10)+F(1, 5)*x+F(3, 10)*a)
                for x, a, y in product(range(2), repeat=3)})

    def transport_parts(dist):
        target_mass = sum(v for (s, x, a, y), v in dist.items() if s == 0)
        sx = {(s, x): sum(v for (ss, xx, a, y), v in dist.items() if (ss, xx) == (s, x))
              for s, x in product(range(2), repeat=2)}
        ax = {x: sum(v for (s, xx, a, y), v in dist.items() if s == 1 and xx == x and a == 1)
              for x in range(2)}
        mx = {x: dist[1, x, 1, 1]/ax[x] for x in range(2)}
        theta = sum(sx[0, x]*mx[x] for x in range(2))/target_mass
        return theta, target_mass, sx, ax, mx

    theta, q, sx, ax, mx = transport_parts(law)
    raw_t = {k: F(2*k[0]+3*k[1]+k[2]-k[3]+k[0]*k[1]) for k in law}
    center_t = sum(law[k]*raw_t[k] for k in law)
    st = {k: raw_t[k]-center_t for k in law}
    phi_t = {}
    for s, x, a, y in law:
        if not s:
            phi_t[s, x, a, y] = (mx[x]-theta)/q
        else:
            phi_t[s, x, a, y] = sx[0, x]/(q*sx[1, x])*a/(ax[x]/sx[1, x])*(y-mx[x])
    assert sum(law[k]*phi_t[k] for k in law) == 0
    tp = {k: v*(1+eps*st[k]) for k, v in law.items()}
    tm = {k: v*(1-eps*st[k]) for k, v in law.items()}
    derivative_errors['transport'] = abs(float(
        (transport_parts(tp)[0]-transport_parts(tm)[0])/(2*eps)
        - sum(law[k]*phi_t[k]*st[k] for k in law)))
    assert derivative_errors['transport'] < 1e-9

    # Independently enumerate intervention paths and retained observed paths.
    direct, weighted = F(0), F(0)
    for x, a0, l1, a1, c1, c2 in product(range(2), repeat=6):
        e0, e1 = F(1, 5)+F(1, 2)*x, F(3, 10)+F(2, 5)*l1
        keep0, keep1 = F(4, 5)-F(1, 5)*a0+F(1, 10)*x, F(3, 5)+F(1, 5)*l1-F(1, 10)*a1
        g0, g1 = F(1, 2), F(1, 4)+F(1, 2)*l1
        transition = prob(l1, F(1, 5)+F(3, 10)*x+F(1, 5)*a0)
        y = 2+3*a0+4*a1+5*l1+x
        if c1 == c2 == 1:
            mass = F(1, 2)*prob(a0, e0)*transition*prob(a1, e1)*keep0*keep1
            weight = prob(a0, g0)/prob(a0, e0)*prob(a1, g1)/prob(a1, e1)/keep0/keep1
            weighted += mass*weight*y
        if c1 == c2 == 0:  # sum full intervention paths exactly once
            direct += F(1, 2)*prob(a0, g0)*transition*prob(a1, g1)*y
    assert direct == weighted
    incidence = [d+(1-d-p2)*d for d, p2 in [(F(1, 10), F(7, 10)), (F(2, 25), F(1, 50))]]
    assert incidence == [F(3, 25), F(19, 125)]
    proxy_reweighted = F(1, 5)*10+F(4, 5)*30
    proxy_true = F(1, 2)*10+F(1, 2)*30
    assert (proxy_reweighted, proxy_true) == (26, 20)
    covariate_effects = [sum(prob(x, prevalence)*(10+20*x) for x in range(2))
                         for prevalence in (F(1, 5), F(4, 5))]
    assert covariate_effects == [14, 26]
    mediator_natural = sum(F(1, 2)*l*l for l in range(2))
    mediator_fresh = sum(F(1, 4)*l*m for l, m in product(range(2), repeat=2))
    assert (mediator_natural, mediator_fresh) == (F(1, 2), F(1, 4))
    return {'frontdoor_means': {str(k): float(v) for k, v in frontdoor.items()},
            'frontdoor_effect': .35, 'unadjusted_effect': .47,
            'gradient_directional_errors': derivative_errors,
            'delta_one_gradient_is_observed_mean_gradient': True,
            'censoring_weighted_and_intervened_mean': str(direct),
            'two_period_default_incidence': [float(v) for v in incidence],
            'covariate_shift_source_target_effects': [float(v) for v in covariate_effects],
            'proxy_shift_true_reweighted_effects': [float(proxy_true), float(proxy_reweighted)],
            'natural_vs_independent_mediator_means': [float(mediator_natural), float(mediator_fresh)]}


def adaptive_randomization():
    # Finite adaptive tree verifies conditional mean and mixture inequalities.
    rho = 1.0
    nodes = [(1.0, 0.0, 0.0, 0)]  # probability, centered sum, intrinsic time, previous outcome
    max_mean_error, max_mixture_excess = 0.0, 0.0

    def mixture(s, v):
        return math.sqrt(rho/(rho+v))*math.exp(s*s/(2*(rho+v)))

    for t in range(8):
        y0, y1 = [(0, 1), (1, 1), (0, 0), (1, 0)][t % 4]
        tau = y1-y0
        children = []
        for mass, s, v, last_y in nodes:
            p = .75 if last_y else .25
            width = 1/(p*(1-p))
            next_v = v+width**2/4
            dz = [-y0/(1-p)-tau, y1/p-tau]
            max_mean_error = max(max_mean_error, abs((1-p)*dz[0]+p*dz[1]))
            mixed_next = (1-p)*mixture(s+dz[0], next_v)+p*mixture(s+dz[1], next_v)
            max_mixture_excess = max(max_mixture_excess, mixed_next-mixture(s, v))
            for a, aa, yy in [(0, 1-p, y0), (1, p, y1)]:
                children.append((mass*aa, s+dz[a], next_v, yy))
        nodes = children
    assert max_mean_error < 1e-12 and max_mixture_excess < 1e-12

    # Exact dynamic program for repeated individually valid binomial tests.
    # Each test rejects only in two tails of probability <= 0.025 each.
    survivors = {0: 1}
    crossing = {}
    for t in range(1, 201):
        cumulative, critical = 0, -1
        for k in range(t//2+1):
            cumulative += math.comb(t, k)
            if 40*cumulative <= 2**t:
                critical = k
            else:
                break
        next_survivors = {}
        for k, count in survivors.items():
            for next_k in (k, k+1):
                if next_k <= critical or next_k >= t-critical:
                    continue
                next_survivors[next_k] = next_survivors.get(next_k, 0)+count
        survivors = next_survivors
        if t in (20, 50, 100, 200):
            crossing[str(t)] = float(1-F(sum(survivors.values()), 2**t))
    assert crossing['200'] > .1
    return {'adaptive_tree_depth': 8, 'conditional_mean_max_error': max_mean_error,
            'mixture_supermartingale_max_excess': max_mixture_excess,
            'repeated_exact_005_binomial_test_crossing_probability': crossing,
            'scope': 'Finite score/mixture checks and exact optional-testing example; not general coverage simulation.'}


def sensitivity_controls():
    # Known hidden law gives an independently computable long and short ATE.
    law = {(u, a, y): F(1, 2)*prob(a, F(1, 5)+F(3, 5)*u)
           * prob(y, F(1, 5)+F(3, 5)*u)
           for u, a, y in product(range(2), repeat=3)}
    pa = {a: sum(p for (u, aa, y), p in law.items() if aa == a) for a in range(2)}
    gs = {a: sum(p*y for (u, aa, y), p in law.items() if aa == a)/pa[a] for a in range(2)}
    long_effect = F(0)
    short_effect = gs[1]-gs[0]
    product_residual, norm_g, norm_alpha = F(0), F(0), F(0)
    for (u, a, y), mass in law.items():
        eu = F(1, 5)+F(3, 5)*u
        g = eu
        alpha = a/eu-(1-a)/(1-eu)
        alpha_s = a/pa[1]-(1-a)/pa[0]
        product_residual += mass*(g-gs[a])*(alpha-alpha_s)
        norm_g += mass*(g-gs[a])**2
        norm_alpha += mass*(alpha-alpha_s)**2
    assert product_residual == long_effect-short_effect == -F(9, 25)
    assert norm_g*norm_alpha == product_residual**2 == F(81, 625)
    # Control-rank example: all factual points obey A=Z+V>=V.
    for z, v in product([F(i, 10) for i in range(11)], repeat=2):
        a = z+v
        assert a+v == a+v+int(a<v)
    # Under do(A=a), missing ranks have exact uniform probability 1-a.
    a = F(1, 5)
    baseline_mean = a+F(1, 2)
    changed_mean = baseline_mean+(1-a)
    assert changed_mean-baseline_mean == F(4, 5)
    # Distinct restriction sets imply distinct population identification sets.
    pre, post, restriction = -F(1), F(3), F(1, 2)
    relative_delta = [-restriction*abs(pre), restriction*abs(pre)]
    smooth_delta = [-pre-restriction, -pre+restriction]
    relative_effect = sorted(post-x for x in relative_delta)
    smooth_effect = sorted(post-x for x in smooth_delta)
    assert relative_effect == [F(5, 2), F(7, 2)]
    assert smooth_effect == [F(3, 2), F(5, 2)]
    return {'long_ate': float(long_effect), 'short_ate': float(short_effect),
            'signed_projection_product': str(product_residual),
            'squared_bias_and_bound': str(norm_g*norm_alpha),
            'control_function_intervention_means_c1': [str(baseline_mean), str(changed_mean)],
            'trend_relative_M_half': [str(x) for x in relative_effect],
            'trend_smooth_M_half': [str(x) for x in smooth_effect]}


def continuous_events():
    import numpy as np
    from scipy.integrate import quad, quad_vec
    from scipy.linalg import expm

    # Two distinct structural drifts produce the same exact sampled law.
    J = np.array([[0., -1.], [1., 0.]])
    drifts = [-np.eye(2), -np.eye(2) + 2*math.pi*J]
    transitions = [expm(g) for g in drifts]
    covariance = [quad_vec(lambda s: expm(g*s) @ expm(g.T*s), 0, 1)[0]
                  for g in drifts]
    controls = [quad_vec(lambda s: expm(g*s) @ np.array([1., 0.]), 0, 1)[0]
                for g in drifts]
    assert np.max(np.abs(transitions[0]-transitions[1])) < 1e-12
    assert np.max(np.abs(covariance[0]-covariance[1])) < 1e-12
    assert np.max(np.abs(covariance[0]-(1-math.exp(-2))/2*np.eye(2))) < 1e-12
    expected = (1-math.exp(-1))/(1+4*math.pi**2)*np.array([1., 2*math.pi])
    assert np.max(np.abs(controls[1]-expected)) < 1e-12
    assert np.linalg.norm(controls[0]-controls[1]) > .5

    # Uniformization independently integrates the killed-state likelihood.
    Q = np.array([[-.3, .3], [.2, -.2]])
    rates = np.array([.1, 1.])
    killed = Q-np.diag(rates)
    nu = float(max(-np.diag(killed)))
    transition = np.eye(2)+killed/nu
    def uniformized(dt):
        answer = np.zeros((2, 2))
        power = np.eye(2)
        mass = math.exp(-nu*dt)
        for n in range(80):
            answer += mass*power
            power = power@transition
            mass *= nu*dt/(n+1)
        return answer
    dt = .8
    uniformization_error = float(np.max(np.abs(uniformized(dt)-expm(killed*dt))))
    assert uniformization_error < 1e-12
    prior = np.array([.5, .5])
    no_event = prior*np.exp(-rates)
    posterior = no_event/no_event.sum()
    at_event = no_event*rates
    at_event /= at_event.sum()
    assert abs(posterior[1]-1/(1+math.exp(.9))) < 1e-14
    assert abs(at_event[1]-1/(1+.1*math.exp(.9))) < 1e-14
    p = np.array([.4, .6])
    h = 1e-6
    def normalized(t):
        a = p@expm(killed*t)
        return a/a.sum()
    numeric = (normalized(h)-normalized(-h))/(2*h)
    theoretical = p@Q-p*(rates-p@rates)
    filter_derivative_error = float(np.max(np.abs(numeric-theoretical)))
    assert filter_derivative_error < 1e-9

    # Poisson sums evaluate both the correct and missing-waiting-time weights.
    masses = [math.exp(-1)/math.factorial(n) for n in range(60)]
    correct = [math.exp(-1)*2**n for n in range(60)]
    mean_w = sum(p*w for p,w in zip(masses,correct))
    mean_wn = sum(n*p*w for n,(p,w) in enumerate(zip(masses,correct)))
    incorrect = sum(p*2**n for n,p in enumerate(masses))
    assert abs(mean_w-1) < 1e-12 and abs(mean_wn-2) < 1e-12
    assert abs(incorrect-math.e) < 1e-12

    # Stochastic-integral expression equals the mean gradient path by path.
    hazard, horizon = .7, 2.
    errors = []
    for event_time in (.1, .4, 1., 1.9, None):
        stop = horizon if event_time is None else event_time
        integral = quad(lambda t: hazard*math.exp(-hazard*(horizon-t)), 0, stop)[0]
        if event_time is not None:
            integral -= math.exp(-hazard*(horizon-event_time))
        expected_score = int(event_time is None)-math.exp(-hazard*horizon)
        errors.append(abs(integral-expected_score))
    assert max(errors) < 1e-12
    b,c = F(2),F(1,2)
    equilibrium = [(u/(1+b*c),-c*u/(1+b*c)) for u in range(-2,3)]
    observational = (equilibrium[-1][0]-equilibrium[0][0])/(equilibrium[-1][1]-equilibrium[0][1])
    assert observational == -1/c == -2
    return {"sampled_transition_max_difference": float(np.max(np.abs(transitions[0]-transitions[1]))),
            "sampled_covariance_max_difference": float(np.max(np.abs(covariance[0]-covariance[1]))),
            "sustained_action_means": [v.tolist() for v in controls],
            "uniformization_likelihood_error": uniformization_error,
            "normalized_filter_derivative_error": filter_derivative_error,
            "distress_after_silence": float(posterior[1]),
            "distress_after_silence_and_report": float(at_event[1]),
            "distress_ignoring_silence": 1/1.1,
            "correct_weight_mean": mean_w, "weighted_event_count": mean_wn,
            "weight_mean_without_integral": incorrect,
            "survival_gradient_path_error": max(errors),
            "equilibrium_rule_response": str(b/(1+b*c)),
            "clamped_rate_response": str(b), "observed_equilibrium_slope": str(observational),
            "scope": "Analytic constructions checked numerically; no fitted bank model, general SDE identification or general TMLE coverage."}


def recent_methods():
    """Independent finite constructions underlying contemporary-method comparisons."""
    import numpy as np
    from scipy.optimize import linprog

    history_cells = {(h,a): F(1,2)*prob(a,F(1,5)+F(3,5)*h)
                     for h,a in product(range(2),repeat=2)}
    mean_y = {a: sum(p*(a+h) for (h,aa),p in history_cells.items() if aa == a)
              /sum(p for (h,aa),p in history_cells.items() if aa == a) for a in range(2)}
    contrast = mean_y[1]-mean_y[0]
    assert contrast == F(8,5)
    balance_law = {a: {0: sum(p for (h,aa),p in history_cells.items() if aa == a)}
                   for a in range(2)}
    assert balance_law[0] == balance_law[1]
    simulation = {}
    for action in (0,1,2):
        paths = [action-1,action+1]
        exact = sum(F(l*l,2) for l in paths)
        mean_path = F(sum(paths),2)**2
        assert exact-mean_path == 1
        simulation[str(action)] = [float(exact),float(mean_path)]
    panel_paths = [np.array([0.,2.]),np.array([10.,12.])]
    demeaned = [x-x.mean() for x in panel_paths]
    transformed = [x*x-(x*x).mean() for x in panel_paths]
    assert np.array_equal(demeaned[0],demeaned[1])
    assert np.array_equal(transformed[0],[-2,2])
    assert np.array_equal(transformed[1],[-22,22])

    # Reconstruct both observational laws, then Bayes-update on all cell-count
    # compositions for sample size six, rather than plugging in a posterior formula.
    latent = {(a,y): sum(F(1,2)*prob(a,F(1,5)+F(3,5)*u)
                         *prob(y,F(1,5)+F(3,5)*u) for u in range(2))
              for a,y in product(range(2),repeat=2)}
    direct = {(a,y): F(1,2)*prob(y,F(8,25)+F(9,25)*a)
              for a,y in product(range(2),repeat=2)}
    assert latent == direct
    prior = F(3,10)
    posteriors = []
    cells = list(latent)
    for c0 in range(7):
        for c1 in range(7-c0):
            for c2 in range(7-c0-c1):
                counts = (c0,c1,c2,6-c0-c1-c2)
                l0,l1 = F(1),F(1)
                for cell,count in zip(cells,counts):
                    l0 *= latent[cell]**count
                    l1 *= direct[cell]**count
                posteriors.append(prior*l1/((1-prior)*l0+prior*l1))
    assert set(posteriors) == {prior}

    # Proxy cardinality exceeds latent cardinality, yet its measurement map
    # has duplicated columns and misses a latent contrast.
    latent_states = list(product(range(2),repeat=2))
    proxy_states = list(product(range(2),repeat=5))
    measurement = np.array([[math.prod(.8 if bit == u1 else .2 for bit in z)
                             for u1,u2 in latent_states] for z in proxy_states])
    rank = int(np.linalg.matrix_rank(measurement))
    invisible = np.array([-1.,1.,-1.,1.])
    assert rank == 2 and np.max(np.abs(measurement@invisible)) < 1e-14
    assert np.max(np.abs(measurement.sum(axis=0)-1)) < 1e-14

    # Conditioning on treatment can couple the two latent coordinates.
    # Assignment uses independent noise and both U coordinates, so proxy
    # noise remains independent. Center within (U1,A), not merely A.
    conditional_null_max = F(0)
    conditional_nonzero = []
    for a in range(2):
        assignment = {(u1,u2):prob(a,F(1,5)+F(u1,5)+F(2*u2,5))
                      for u1,u2 in latent_states}
        centered = {}
        for u1 in range(2):
            mu = assignment[u1,1]/sum(assignment[u1,u2] for u2 in range(2))
            for u2 in range(2):
                centered[u1,u2] = u2-mu
        conditional_nonzero.extend(centered.values())
        for z in proxy_states:
            joint = {(u1,u2):F(1,4)*assignment[u1,u2]*
                     math.prod(F(4,5) if bit == u1 else F(1,5) for bit in z)
                     for u1,u2 in latent_states}
            residual = sum(joint[u]*centered[u] for u in latent_states)/sum(joint.values())
            conditional_null_max = max(conditional_null_max,abs(residual))
    assert conditional_null_max == 0 and all(conditional_nonzero)

    # Enumerate complete action paths under the history-dependent logger.
    # The two models differ only in the first continue transition.
    path_results = {}
    for horizon in (3,5,8):
        laws = [{},{}]
        no_reset = F(0)
        for actions in product(range(3),repeat=horizon-1):
            mass, memory = F(1),None
            lanes = [None,None]
            for t,action in enumerate(actions):
                if t == 0:
                    action_probs = [F(1,3)]*3
                elif memory is None:
                    action_probs = [F(2,3),F(1,6),F(1,6)]
                elif memory == 0:
                    action_probs = [F(1,6),F(2,3),F(1,6)]
                else:
                    action_probs = [F(1,6),F(1,6),F(2,3)]
                mass *= action_probs[action]
                for theta in range(2):
                    if action == 0 and t == 0:
                        lanes[theta] = theta
                    elif action:
                        lanes[theta] = action-1
                if action:
                    memory = action-1
            if memory is None:
                no_reset += mass
            for theta in range(2):
                for reward in range(2):
                    laws[theta][actions+(reward,)] = mass*prob(
                        reward,F(1,4)+F(1,2)*lanes[theta])
        expected = F(1,3)*F(2,3)**(horizon-2)
        assert no_reset == expected
        assert all(sum(law.values()) == 1 for law in laws)
        kl = sum(float(p)*math.log(float(p/laws[1][key])) for key,p in laws[0].items())
        kl_expected = float(expected)*math.log(3)/2
        assert abs(kl-kl_expected) < 1e-13
        path_results[str(horizon)] = {"informative_probability":str(expected),
                                      "full_path_kl":kl,"reduced_kl":kl_expected}

    # Optimize local probability polytopes directly, then compare a backward
    # recursion with exhaustive globally compatible kernel choices.
    m = np.array([.2,.4])
    local_min = linprog([0.,1.],A_eq=[[1.,1.]],b_eq=[1.],
                        bounds=list(zip(m,m+.4)),method="highs")
    local_max = linprog([0.,-1.],A_eq=[[1.,1.]],b_eq=[1.],
                        bounds=list(zip(m,m+.4)),method="highs")
    assert local_min.success and local_max.success
    assert abs(local_min.fun-.4) < 1e-12 and abs(-local_max.fun-.8) < 1e-12
    global_values = [(1-p)*q0+p*q1 for p,q0,q1 in
                     product((F(1,5),F(3,5)),(F(1,10),F(2,5)),(F(3,5),F(9,10)))]
    lower = min((1-p)*F(1,10)+p*F(3,5) for p in (F(1,5),F(3,5)))
    upper = max((1-p)*F(2,5)+p*F(9,10) for p in (F(1,5),F(3,5)))
    assert (min(global_values),max(global_values)) == (lower,upper) == (F(1,5),F(7,10))
    coupled = [u+(1-u) for u in (F(0),F(1,2),F(1))]
    rectangular = [c0+c1 for c0,c1 in product(range(2),repeat=2)]
    assert set(coupled) == {1} and (min(rectangular),max(rectangular)) == (0,2)
    return {"balanced_constant_representation_contrast":str(contrast),
            "true_effect":1,"nonlinear_simulation":[simulation],
            "demeaned_quadratic": [v.tolist() for v in transformed],
            "equivalent_model_posterior":str(prior),
            "all_sample_count_compositions_checked":len(posteriors),
            "proxy_map_shape":list(measurement.shape),"proxy_map_rank":rank,
            "proxy_treatment_conditional_null_max":str(conditional_null_max),
            "rare_informative_paths":path_results,
            "local_polytope_bounds":[float(local_min.fun),float(-local_max.fun)],
            "rectangular_recursion_bounds":[str(lower),str(upper)],
            "coupled_cashflow_bounds":[1,1],"marginal_envelope_bounds":[0,2],
            "scope":"Finite constructed witnesses and a primary-paper path enumeration; not a neural-method replication, full POMDP coverage proof or bank estimate."}


def software_contracts():
    # These are mathematical adapter witnesses, not executions of packages.
    unit_mean = (F(1)*0+F(9)*10)/10
    cluster_mean = (F(0)+10)/2
    assert (unit_mean,cluster_mean) == (9,5)
    # Exact polynomial moments under Uniform[-1,1].
    continuous_projection = F(1,5)/F(1,3)
    assert continuous_projection == F(3,5)
    untruncated = sum(p*l*l for p,l in
                      [(F(1,4),-2),(F(1,2),0),(F(1,4),2)])
    clipped = sum(p*max(-1,min(1,l))**2 for p,l in
                  [(F(1,4),-2),(F(1,2),0),(F(1,4),2)])
    assert (untruncated,clipped) == (2,F(1,2))
    e = F(1,5)
    policy_rows = []
    for delta in (F(1,2),F(1),F(2)):
        keep = delta if delta <= 1 else 1/delta
        replacement = 0 if delta <= 1 else 1
        # Enumerate natural action and independent retention coin.
        q_enum = sum(prob(a,e)*prob(retain,keep)*
                     (a if retain else replacement)
                     for a,retain in product(range(2),repeat=2))
        q = delta*e if delta <= 1 else 1-(1-e)/delta
        odds = delta*e/(1-e+delta*e)
        assert q_enum == q
        policy_rows.append({"delta":str(delta),"retention_policy":str(q),
                            "odds_policy":str(odds)})
    assert [r["retention_policy"] for r in policy_rows] == ["1/10","1/5","3/5"]

    # Check the propensity-dependent one-step gradient by perturbing the
    # complete observed law, not just the final formula.
    law = {(h,a,y):prob(h,F(2,5))*prob(a,F(1+h,5))*
           prob(y,F(1+h+2*a,5)) for h,a,y in product(range(2),repeat=3)}
    tilt = {key:F(2*key[0]-key[1]+3*key[2],7) for key in law}
    tilt_mean = sum(law[k]*tilt[k] for k in law)
    score = {k:tilt[k]-tilt_mean for k in law}

    def target(p, f):
        result = 0
        for h in range(2):
            ph = sum(v for (hh,a,y),v in p.items() if hh == h)
            pa = [sum(p[h,a,y] for y in range(2)) for a in range(2)]
            m = [p[h,a,1]/pa[a] for a in range(2)]
            q = f(pa[1]/ph)
            result += ph*((1-q)*m[0]+q*m[1])
        return result

    gradient_errors = []
    eps = 1e-6
    for delta in (F(1,2),F(1),F(2)):
        transforms = [
            (lambda x,d=delta:d*x if d <= 1 else 1-(1-x)/d,
             lambda x,d=delta:d if d <= 1 else 1/d),
            (lambda x,d=delta:d*x/(1-x+d*x),
             lambda x,d=delta:d/(1+(d-1)*x)**2)]
        for f,df in transforms:
            theta = target(law,f)
            influence = {}
            for h,a,y in law:
                ph = sum(v for (hh,aa,yy),v in law.items() if hh == h)
                pa = [sum(law[h,aa,yy] for yy in range(2)) for aa in range(2)]
                prop = pa[1]/ph
                means = [law[h,aa,1]/pa[aa] for aa in range(2)]
                q = f(prop)
                influence[h,a,y] = (a*q/prop*(y-means[1])+
                    (1-a)*(1-q)/(1-prop)*(y-means[0])+
                    df(prop)*(means[1]-means[0])*(a-prop)+
                    (1-q)*means[0]+q*means[1]-theta)
            assert sum(law[k]*influence[k] for k in law) == 0
            if delta == 1:
                assert all(influence[k] == k[2]-theta for k in law)
            inner = sum(law[k]*influence[k]*score[k] for k in law)
            plus = {k:float(v)*(1+eps*float(score[k])) for k,v in law.items()}
            minus = {k:float(v)*(1-eps*float(score[k])) for k,v in law.items()}
            numerical = (target(plus,f)-target(minus,f))/(2*eps)
            error = abs(float(inner)-float(numerical))
            assert error < 1e-9
            gradient_errors.append(error)
    scores = [1,1,-1,-1]
    row_meat = sum(x*x for x in scores)
    cluster_meat = sum(sum(scores[i] for i in ids)**2 for ids in ((0,1),(2,3)))
    # Worker partitions cross statistical clusters.
    partials = [[("a",1),("b",-1)],[("a",1),("b",-1)]]
    regrouped = {c:sum(x for part in partials for key,x in part if key == c)
                 for c in ("a","b")}
    assert sum(x*x for x in regrouped.values()) == cluster_meat == 8
    assert row_meat == 4
    return {"customer_branch_means":[str(unit_mean),str(cluster_mean)],
            "continuous_projection":str(continuous_projection),
            "derivative_at_zero":0,
            "untruncated_clipped_second_moment":[str(untruncated),str(clipped)],
            "incremental_probability_transforms":policy_rows,
            "policy_gradient_max_error":max(gradient_errors),
            "policy_gradients_checked":len(gradient_errors),
            "row_cluster_meat":[row_meat,cluster_meat],
            "scope":"Project algebra and finite-law directional derivatives; no third-party package execution or adapter implementation."}


def product_contracts():
    # A fixed many-to-one transform O=(Z,W) -> Z, target E[Z].
    # Verify the pushforward score and its pulled-back gradient in a
    # basis spanning every mean-zero score on this four-cell law.
    cells=list(product(range(2),repeat=2))
    law=dict(zip(cells,[F(1,6),F(1,2),F(1,4),F(1,12)]))
    pz={z:sum(p for (zz,w),p in law.items() if zz==z) for z in range(2)}
    mean=pz[1]
    errors=[]
    for selected in cells[:-1]:
        score={o:F(o==selected)-law[selected] for o in cells}
        reduced={z:sum(law[o]*score[o] for o in cells if o[0]==z)/pz[z] for z in range(2)}
        direct=sum(law[o]*o[0]*score[o] for o in cells)
        via_reduced=sum(pz[z]*(z-mean)*reduced[z] for z in range(2))
        pulled=sum(law[o]*(o[0]-mean)*score[o] for o in cells)
        assert direct==via_reduced==pulled
        errors.append(str(direct-pulled))
    # Persistent ambiguity does not permit independently choosing a model
    # at each date. This tests the value-set algebra, not model discovery.
    rewards=[[0,1],[1,0]]
    persistent=min(sum(r) for r in rewards)
    rectangular=sum(min(r[t] for r in rewards) for t in range(2))
    assert persistent==1 and rectangular==0
    return {'pushforward_score_directions':3,'exact_gradient_errors':errors,
            'persistent_rectangular_worst_values':[persistent,rectangular],
            'scope':'Finite checks of the new product derivations; no adapter or backend qualification.'}


def main():
    checks = {"static": static(), "iv": instrument(), "learning": learning(),
              "longitudinal": longitudinal(), "filtering": filtering(),
              "inverse_proxies": inverse_proxies(), "longer_horizon": longer_horizon(),
              "weak_sets": weak_sets(), "panels_time": panels_time(),
              "discovery_observation": discovery_observation(), "controlled_choice": controlled_choice(),
              "policy_transport": policy_transport(), "adaptive_randomization": adaptive_randomization(),
              "sensitivity_controls": sensitivity_controls(), "continuous_events": continuous_events(),
              "recent_methods": recent_methods(),
              "software_contracts": software_contracts(),
              "product_contracts": product_contracts()}
    inputs = [Path(__file__).resolve(), ROOT / 'docs/causal_foundations.tex']
    inputs.extend(sorted((ROOT / 'docs/reconstruction').glob('*.tex')))
    result = {"status": "pass", "date": "2026-10-09", "checks": checks,
              "input_sha256": {str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
                               for p in inputs},
              "scope": "Finite algebraic/likelihood identities, counterexamples, several finite-law directional derivatives and an exact repeated-testing distribution. Not general proof verification, general coverage validation, bank evidence or scholarly completeness."}
    dest = ROOT / 'docs/reconstruction/checks.json'
    dest.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
