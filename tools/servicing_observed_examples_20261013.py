#!/usr/bin/env python3
"""Exact path references for a restricted servicing argument; no random draws."""
from fractions import Fraction as F
from itertools import product
import json
from math import log, sqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'docs/program/execution/2026-10-13/servicing/exact-results.json'


def bern(p, value):
    return p if value else 1 - p


def action_probability(s):
    return F(3, 10) + F(2, 5) * s


def retention(s, a):
    return F(9, 10) - F(1, 10) * (s + a)


def transition(s, a):
    return F(1, 5) + F(1, 2) * s - F(3, 20) * a


def reward(s_next, a):
    return 2 - 3 * s_next - F(1, 4) * a


POLICIES = {'none': lambda s: 0, 'all': lambda s: 1, 'stressed': lambda s: s}


def backward_value(policy):
    values = [F(0), F(0)]
    for _ in range(2):
        values = [sum(bern(transition(s, policy(s)), sn) *
                      (reward(sn, policy(s)) + values[sn]) for sn in [0, 1])
                  for s in [0, 1]]
    return sum(values) / 2


def enumerate_values(policy, fitted=False):
    """Enumerate full latent paths but construct observed scores only until dropout."""
    result = {k: F(0) for k in ['observed_mass', 'intervention_mass', 'truth',
                                'prefix_score', 'current_only', 'changed_law_score']}
    for s0, a0, s1, a1, s2 in product([0, 1], repeat=5):
        states, actions = [s0, s1, s2], [a0, a1]
        observed_prob = F(1, 2)
        target_prob = F(1, 2)
        ratios, cumulative = [], F(1)
        for t in range(2):
            s, a = states[t], actions[t]
            ep, gp = action_probability(s), retention(s, a)
            eh = ep + F(1, 25) if fitted else ep
            gh = gp - F(3, 100) if fitted else gp
            assert F(1, 4) <= eh <= F(3, 4) and F(13, 20) <= gh <= 1
            observed_prob *= bern(ep, a) * bern(transition(s, a), states[t+1])
            target_prob *= int(a == policy(s)) * bern(transition(s, a), states[t+1])
            cumulative *= bern(ep, a) / bern(eh, a) * gp / gh
            ratios.append(cumulative)
        result['intervention_mass'] += target_prob
        result['truth'] += target_prob * sum(reward(states[t+1], actions[t]) for t in range(2))
        result['changed_law_score'] += target_prob * sum(
            ratios[t] * reward(states[t+1], actions[t]) for t in range(2))
        for c0, c1 in product([0, 1], repeat=2):
            cs = [c0, c1]
            probability = observed_prob
            for t in range(2):
                probability *= bern(retention(states[t], actions[t]), cs[t])
            result['observed_mass'] += probability
            weight, score, shortcut, visible = F(1), F(0), F(0), True
            for t in range(2):
                # Later potential C values only enumerate the full law; they are
                # never available to this observed-data score after dropout.
                if not visible:
                    break
                s, a = states[t], actions[t]
                ep = action_probability(s) + (F(1, 25) if fitted else 0)
                gp = retention(s, a) - (F(3, 100) if fitted else 0)
                ratio = F(int(a == policy(s)), 1) / bern(ep, a) * cs[t] / gp
                weight *= ratio
                visible = bool(cs[t])
                if visible:
                    score += weight * reward(states[t+1], a)
                    shortcut += ratio * reward(states[t+1], a)
            result['prefix_score'] += probability * score
            result['current_only'] += probability * shortcut
    assert result['observed_mass'] == result['intervention_mass'] == 1
    assert result['prefix_score'] == result['changed_law_score']
    assert result['truth'] == backward_value(policy)
    if not fitted:
        assert result['prefix_score'] == result['truth']
    return result


def hidden_worlds():
    experimental = {(a, y): F(0) for a, y in product([0, 1], repeat=2)}
    hidden = experimental.copy()
    for a, y in experimental:
        experimental[a, y] = F(1, 2) * (F(4, 5) if y == a else F(1, 5))
        for u in [0, 1]:
            hidden[a, y] += F(1, 2) * bern(F(1, 5) + F(3, 5) * u, a) * int(y == u)
    assert hidden == experimental
    ipw = sum(p * a * y / F(1, 2) for (a, y), p in hidden.items())
    assert ipw == F(4, 5)
    return {'observed_law': {str(k): str(v) for k, v in hidden.items()},
            'experimental_intervention_values': ['1/5', '4/5'],
            'hidden_intervention_values': ['1/2', '1/2'],
            'observed_logger_ipw': str(ipw), 'same_observed_law': True}


def missing_worlds():
    worlds = []
    for missing_y in [0, 1]:
        full = {(1, 0): F(1, 4), (1, 1): F(1, 4), (0, missing_y): F(1, 2)}
        observed = {}
        for (c, y), p in full.items():
            key = (c, y if c else None)
            observed[key] = observed.get(key, F(0)) + p
        worlds.append((observed, sum(y * p for (c, y), p in full.items())))
    assert worlds[0][0] == worlds[1][0]
    assert [w[1] for w in worlds] == [F(1, 4), F(3, 4)]
    return {'same_observed_law': True, 'cohort_means': ['1/4', '3/4'],
            'complete_case_mean': '1/2'}


def calculate():
    ce, cg, de, dg = F(1, 4), F(13, 20), F(1, 25), F(3, 100)
    growth = (1 + de / ce) * (1 + dg / cg)
    envelope = sum(2 * (growth ** (t+1) - 1) for t in range(2))
    maximum = sum(2 / (ce * cg) ** (t+1) for t in range(2))
    rows = []
    for name, policy in POLICIES.items():
        true = enumerate_values(policy)
        fitted = enumerate_values(policy, fitted=True)
        bias = fitted['prefix_score'] - fitted['truth']
        assert abs(bias) <= envelope
        rows.append({'policy': name, 'true': {k: str(v) for k, v in true.items()},
                     'fitted': {k: str(v) for k, v in fitted.items()},
                     'value': float(true['truth']), 'fitted_bias': float(bias),
                     'bias_inside_envelope': True})
    assert any(r['true']['current_only'] != r['true']['truth'] for r in rows)
    n = 1000
    radius = float(maximum) * sqrt(2 * log(2 / .025) / n)
    # Exact binomial coverage of a training-cell interval for small, fully
    # enumerated samples; this checks the count rule, not a final study.
    from math import comb
    binomial_cases = []
    for count in [0, 1, 4, 12, 32]:
        for p in [F(1, 5), F(1, 2), F(4, 5)]:
            eps = 1 if count == 0 else min(1, sqrt(log(2 / .05) / (2 * count)))
            coverage = sum(F(comb(count, k)) * p**k * (1-p)**(count-k)
                           for k in range(count+1)
                           if abs((k/count if count else .5) - float(p)) <= eps)
            assert float(coverage) >= .95
            binomial_cases.append({'n': count, 'p': str(p), 'coverage': float(coverage)})
    return {'kind': 'deterministic_exact_reference_not_final_study', 'random_draws': 0,
            'independent_formula_checks': ['path sums versus backward recursion',
                                          'observed prefixes versus intervention density change'],
            'policies': rows, 'bias_envelope': float(envelope), 'score_bound': float(maximum),
            'n_eval': n, 'alpha_eval': .025, 'evaluation_radius': radius,
            'total_radius_with_illustrative_errors': radius + float(envelope),
            'declared_value_range': [-4, 4], 'hidden_confounding': hidden_worlds(),
            'informative_observation': missing_worlds(), 'binomial_enumerations': binomial_cases,
            'qualification_claim': False}


if __name__ == '__main__':
    result = calculate()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': 'pass', 'policies': [(r['policy'], r['value']) for r in result['policies']],
                      'evaluation_radius': result['evaluation_radius'], 'random_draws': 0}))
