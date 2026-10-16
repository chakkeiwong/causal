#!/usr/bin/env python3
"""Exact authored S4 laws; no external estimator or bank observations."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-17/s4'


def serial(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {k: serial(v) for k, v in x.items()}
    if isinstance(x, (tuple, list)):
        return [serial(v) for v in x]
    return x


def weighted(w, x):
    return sum((a*b for a, b in zip(w, x)), F(0))


def target(w, h, tau):
    return weighted(w, [a*b for a, b in zip(h, tau)])/weighted(w, h)


def weighting():
    p = [F(1, 4), F(1, 2), F(1, 4)]
    e = [F(1, 10), F(1, 2), F(9, 10)]
    q = [F(1, 5), F(1, 2), F(4, 5)]
    t = list(map(F, [-4, 4, 20])); m0 = list(map(F, [30, 50, 70]))
    m1 = [a+b for a, b in zip(m0, t)]
    h = [a*(1-a) for a in e]
    hq = [a*(1-a) for a in q]
    corrected = [a+(b-c)**2 for a, b, c in zip(h, q, e)]
    ipw = weighted(p, [a/b*c-(1-a)/(1-b)*d for a, b, c, d in zip(e, q, m1, m0)])
    ess = {}
    for name, fitted in [('true', e), ('clipped', q)]:
        ew = weighted(p, [a/b for a, b in zip(e, fitted)])
        ew2 = weighted(p, [a/b**2 for a, b in zip(e, fitted)])
        ess[name] = dict(mean_weight=ew, second_moment=ew2, ess_fraction=ew**2/ew2)
    # Enumerate observed X,A,Y cells for influence-function path checks.
    direction = [F(1, 20), F(-1, 10), F(1, 20)]
    paths = {}
    for name, hw, hp in [('ATT', e, [F(1)]*3), ('overlap', h, [1-2*a for a in e])]:
        H = weighted(p, hw); theta = target(p, hw, t)
        means = [F(0)]*2; variances = [F(0)]*2; covariances = [F(0)]*2
        for j, a, sign in product(range(3), [0, 1], [-1, 1]):
            mass = p[j]*(e[j] if a else 1-e[j])/2
            residual = F(2*sign)
            fixed = hw[j]/H*(t[j]-theta+(a/e[j]-(1-a)/(1-e[j]))*residual)
            full = fixed+hp[j]/H*(a-e[j])*(t[j]-theta)
            score = direction[j]*(a-e[j])/(e[j]*(1-e[j]))
            for k, phi in enumerate([fixed, full]):
                means[k] += mass*phi
                variances[k] += mass*phi**2
                covariances[k] += mass*phi*score
        derivative = weighted(p, [a*b*(c-theta) for a, b, c in zip(hp, direction, t)])/H
        assert means == [0, 0] and covariances == [0, derivative]
        paths[name] = dict(target=theta, direction=direction, exact_target_derivative=derivative,
                           mean_phi=means, fixed_and_full_variance=variances,
                           fixed_and_full_score_covariance=covariances)
    # Exact overlap estimating equation under simultaneous nuisance error.
    d1 = [F(1), F(-2), F(3)]; d0 = [F(-1), F(1), F(2)]
    numerator = denominator = F(0)
    for j, a in product(range(3), [0, 1]):
        mass = p[j]*(e[j] if a else 1-e[j])
        mhat1, mhat0 = m1[j]+d1[j], m0[j]+d0[j]
        yy = m1[j] if a else m0[j]
        D = a*(1-q[j])**2+(1-a)*q[j]**2
        N = D*(mhat1-mhat0)+a*(1-q[j])*(yy-mhat1)-(1-a)*q[j]*(yy-mhat0)
        numerator += mass*N; denominator += mass*D
    theta = target(p, h, t)
    remainder = weighted(p, [(b-a)**2*(c-theta)+(b-a)*(b*u+(1-b)*v)
                             for a, b, c, u, v in zip(e, q, t, d1, d0)])
    assert numerator-theta*denominator == remainder
    return dict(masses=p, propensities=e, clipped_propensities=q, effects_USD=t,
                baseline_USD=m0, ATE=weighted(p, t), ATT=target(p, e, t),
                ATC=target(p, [1-a for a in e], t), overlap=theta,
                H=weighted(p, h), trimmed_target=F(4),
                clipped_IPW=ipw, augmented_with_true_outcomes=weighted(p, t),
                frozen_overlap_with_q=target(p, hq, t),
                corrected_overlap_with_true_outcomes=target(p, corrected, t),
                corrected_overlap_bias=target(p, corrected, t)-theta,
                ess=ess, influence_paths=paths,
                overlap_remainder=dict(outcome_errors=[d1, d0], numerator=numerator,
                    denominator=denominator, unnormalized_error=remainder,
                    normalized_error=remainder/denominator))


def multiarm():
    p = [F(1, 2), F(1, 4), F(1, 4)]
    rows = []
    for a, noise in product(range(3), [-2, 2]):
        phi = [F(noise)*((1 if a == j else 0)/p[j]-(1 if a == 0 else 0)/p[0])
               for j in [1, 2]]
        rows.append((p[a]/2, phi))
    cov = [[sum(m*v[j]*v[k] for m, v in rows) for k in range(2)] for j in range(2)]
    contrast = sum(m*(v[0]-v[1])**2 for m, v in rows)
    assert cov == [[24, 8], [8, 24]] and contrast == 32
    return dict(propensities=p, conditional_noise_variance=4, covariance=cov,
                difference_variance=contrast, incorrectly_independent_difference_variance=48,
                interpretation='Population influence covariance; divide by n for an iid mean, not an empirical standard error.')


def allocation():
    p = [F(2, 5), F(3, 10), F(1, 5), F(1, 10)]
    effects = list(map(F, [4, 9, 15, 25])); costs = list(map(F, [1, 3, 7, 14]))
    g = [a-b for a, b in zip(effects, costs)]; r = list(map(F, [1, 1, 2, 4])); B = F(1, 2)
    vertices = {}
    # Every vertex of one budget halfspace intersected with a box has at
    # most one non-bound coordinate; enumerate all such candidates.
    for bits in product([F(0), F(1)], repeat=4):
        candidates = [bits]
        for j in range(4):
            d = list(bits)
            d[j] = (B-sum(p[k]*r[k]*d[k] for k in range(4) if k != j))/(p[j]*r[j])
            candidates.append(tuple(d))
        for d in candidates:
            used = sum(p[k]*r[k]*d[k] for k in range(4))
            if all(0 <= x <= 1 for x in d) and used <= B:
                vertices[d] = sum(p[k]*g[k]*d[k] for k in range(4))
    optimum = max(vertices.values()); best = [d for d, v in vertices.items() if v == optimum]
    greedy = [F(0), F(0), F(1, 4), F(1)]
    greedy_value = sum(p[k]*g[k]*greedy[k] for k in range(4))
    lam = F(4); dual = lam*B+sum(p[k]*max(F(0), g[k]-lam*r[k]) for k in range(4))
    assert best == [(F(0), F(1), F(1, 2), F(0))] and optimum == dual == F(13, 5)
    return dict(masses=p, gross_USD=effects, costs_USD=costs, net_USD=g,
                resource_units=r, budget=B, vertices_checked=len(vertices),
                optimal_fractions=best[0], optimal_value_USD=optimum,
                effect_rank_fractions=greedy, effect_rank_value_USD=greedy_value,
                lost_value_USD=optimum-greedy_value, dual_price_USD_per_unit=lam, dual_bound_USD=dual)


def threshold():
    # Exact normal equations for uniform one-sided local-linear projection.
    G = [[F(1), F(1, 2)], [F(1, 2), F(1, 3)]]
    inv = [[F(4), F(-6)], [F(-6), F(12)]]
    assert [[sum(G[i][k]*inv[k][j] for k in range(2)) for j in range(2)] for i in range(2)] == [[1, 0], [0, 1]]
    intercept = 4*F(1, 3)-6*F(1, 4)
    assert intercept == F(-1, 6)
    cases = []
    for dA, h in product([F(1, 2), F(1, 50)], [F(1, 2), F(1, 4)]):
        theta = F(8); dY = theta*dA
        bY, bA = -12*h**2/6, -F(1, 2)*h**2/6
        fitted = (dY+bY)/(dA+bA)
        assert fitted-theta == (bY-theta*bA)/(dA+bA)
        cases.append(dict(receipt_jump=dA, recovery_jump_USD=dY, bandwidth=h,
                          outcome_bias=bY, receipt_bias=bA, projected_receipt_jump=dA+bA,
                          projected_ratio_USD=fitted, ratio_bias_USD=fitted-theta))
    epsilon = [F(1, 10), F(1, 100), F(1, 1000)]
    return dict(moment_matrix=G, inverse=inv, curvature_coefficient=intercept,
                equivalent_kernel=dict(integral=F(4)-6*F(1, 2), first_moment=4*F(1, 2)-6*F(1, 3),
                                       second_moment=4*F(1, 3)-6*F(1, 4), sign_change=F(2, 3)),
                fuzzy_projection=cases,
                finite_epsilon=[dict(epsilon=x, cutoff_effect_USD=8,
                                     contrast_USD=8+8*x+12*x*x, approximation_error_USD=8*x+12*x*x)
                                for x in epsilon],
                discrete_models=[dict(model='constant causal effect', observed_Y=[10, 14], cutoff_effect=4),
                                 dict(model='score trend only', observed_Y=[10, 14], cutoff_effect=0)],
                transport=dict(cutoff_effect_USD=8, target_scores=[F(-1, 2), F(1, 2)],
                               target_masses=[F(1, 2), F(1, 2)], lipschitz_USD_per_score=6,
                               expected_absolute_score=F(1, 2), sharp_effect_bounds_USD=[5, 11],
                               cost_USD=7, sharp_net_bounds_USD=[-2, 4]))


def calculate():
    return serial(dict(status='exact_authored_examples_not_empirical', weighting=weighting(),
                       multiarm=multiarm(), allocation=allocation(), threshold=threshold()))


if __name__ == '__main__':
    from publish_latent_r_review_v2_20261013 import write
    result = calculate()
    write(BASE/'exact-results.json', result)
    print(json.dumps(dict(status='pass', families=['target weights and influence paths', 'overlap remainder',
        'multiarm covariance', 'resource allocation', 'threshold approximation', 'discrete support', 'transport bounds'])))
