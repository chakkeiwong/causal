#!/usr/bin/env python3
"""Independent finite-law oracles; no NumPyro/JAX imports or upstream execution."""
from fractions import Fraction as F
from itertools import product
from math import factorial
import json


def frac(x):
    return str(x)


def moments(law):
    assert sum(law.values()) == 1
    mean = sum(x * p for x, p in law.items())
    return mean, sum((x - mean) ** 2 * p for x, p in law.items())


def beta_integral(a, b):
    return F(factorial(a - 1) * factorial(b - 1), factorial(a + b - 1))


def calculate():
    # A deliberately confounded supplied structural law, enumerated independently.
    joint = {}
    for u, a in product([0, 1], repeat=2):
        pa = F(3, 4) if a == u else F(1, 4)
        joint[u, a, 2 * a + 4 * u] = F(1, 2) * pa
    conditional = {}
    for a in [0, 1]:
        mass = sum(p for (u, aa, y), p in joint.items() if aa == a)
        conditional[a] = sum(y * p for (u, aa, y), p in joint.items() if aa == a) / mass
    intervened = {a: sum(F(1, 2) * (2 * a + 4 * u) for u in [0, 1]) for a in [0, 1]}
    assert conditional == {0: F(1), 1: F(5)} and intervened == {0: F(2), 1: F(4)}

    # Signal updates a latent servicing type. MAP substitution changes the decision.
    prior = {0: F(2, 3), 1: F(1, 3)}
    likelihood = {0: F(1, 4), 1: F(3, 4)}
    signal_mass = sum(prior[u] * likelihood[u] for u in prior)
    posterior = {u: prior[u] * likelihood[u] / signal_mass for u in prior}
    payoff = {0: F(-200), 1: F(100)}
    posterior_value = sum(posterior[u] * payoff[u] for u in prior)
    prior_value = sum(prior[u] * payoff[u] for u in prior)
    map_state = max(posterior, key=posterior.get)
    map_value = payoff[map_state]
    assert signal_mass == F(5, 12) and posterior[1] == F(3, 5)
    assert (prior_value, posterior_value, map_value) == (F(-100), F(-20), F(100))
    assert posterior_value < 0 < map_value

    # Equal single-world interventional marginals allow different cross-world laws.
    worlds = {'shared': [(0, 0, F(1, 2)), (1, 1, F(1, 2))],
              'flipped': [(0, 1, F(1, 2)), (1, 0, F(1, 2))]}
    cross = {}
    marginals = {}
    for name, law in worlds.items():
        marginals[name] = [sum(p for y0, y1, p in law if [y0, y1][a] == 1) for a in [0, 1]]
        event = sum(p for y0, y1, p in law if y0 == 1)
        cross[name] = sum(p for y0, y1, p in law if y0 == y1 == 1) / event
    assert marginals['shared'] == marginals['flipped'] == [F(1, 2), F(1, 2)]
    assert cross == {'shared': F(1), 'flipped': F(0)}

    # Conjugate benchmark from normalizing integrals, rather than a package formula.
    a, b = 2 + 4, 3 + 1
    z = beta_integral(a, b)
    mean = beta_integral(a + 1, b) / z
    variance = beta_integral(a + 2, b) / z - mean ** 2
    assert mean == F(3, 5) and variance == F(6, 275)

    # An explicit dependence witness, not a claim about a native PRNG failure.
    independent = {}
    for bits in product([0, 1], repeat=4):
        average = F(sum(bits), 4)
        independent[average] = independent.get(average, F(0)) + F(1, 16)
    copied = {F(0): F(1, 2), F(1): F(1, 2)}
    mi, vi = moments(independent)
    mc, vc = moments(copied)
    assert mi == mc == F(1, 2) and vi == F(1, 16) and vc == F(1, 4)
    deterministic_means = [sum(F(x ** power, 2) for x in [1, 2]) for power in [2, 3]]
    assert deterministic_means == [F(5, 2), F(9, 2)]
    return dict(
        kind='Project-owned exact examples, not upstream execution or bank observations',
        confounding=dict(conditional_means=[frac(conditional[a]) for a in [0, 1]],
            intervention_means=[frac(intervened[a]) for a in [0, 1]], association='4', effect='2'),
        latent_signal=dict(signal_probability=frac(signal_mass), posterior_high=frac(posterior[1]),
            prior_value=frac(prior_value), posterior_value=frac(posterior_value), map_state=map_state,
            map_value=frac(map_value), optimal_action_under_mixture=0, action_under_map=1,
            expected_loss_of_map_action=frac(-posterior_value)),
        cross_world=dict(intervention_success=[frac(x) for x in marginals['shared']],
            conditional_shared=frac(cross['shared']), conditional_flipped=frac(cross['flipped'])),
        conjugate=dict(prior=[2, 3], successes=4, failures=1, posterior=[a, b],
            normalizer=frac(z), mean=frac(mean), variance=frac(variance)),
        replication=dict(chains=4, independent_variance=frac(vi), copied_variance=frac(vc),
            variance_ratio=frac(vc / vi)),
        deterministic=dict(stored_square_mean=frac(deterministic_means[0]),
            recomputed_cube_mean=frac(deterministic_means[1])),
        native_execution=False)


if __name__ == '__main__':
    print(json.dumps(calculate(), indent=2))
