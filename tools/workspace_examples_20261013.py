#!/usr/bin/env python3
"""Exact generated examples for I3, without importing any sibling project.

These are transparent mathematical references, not consumer adapter trials,
statistical qualification, or observations of a bank.
"""
import argparse
from fractions import Fraction as F
import hashlib
from itertools import product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def number(x):
    return {'exact': str(x), 'decimal': float(x)}


def funding():
    balance, action_bp, rate, cost = 100_000_000, -10, .04, 40_000
    accrual = sum(.25 / (1 + rate) ** (t / 4) for t in range(1, 5))
    scale = -balance * action_bp / 10_000 * accrual
    values = [scale * theta - cost for theta in [.6, .75, .9]]
    # Independent cash-flow construction in dollars and in millions.
    for theta, value in zip([.6, .75, .9], values):
        flows = [-balance * (action_bp / 10_000) * theta / 4] * 4
        direct = sum(c / (1 + rate) ** (t / 4) for t, c in enumerate(flows, 1)) - cost
        in_millions = sum((c / 1e6) / (1 + rate) ** (t / 4)
                          for t, c in enumerate(flows, 1)) - cost / 1e6
        assert abs(direct - value) < 1e-8
        assert abs(in_millions * 1e6 - value) < 1e-8
    return {'balance_usd': balance, 'action_bp': action_bp,
            'annual_effective_discount_rate': rate, 'quarters': 4,
            'implementation_cost_usd': cost, 'assumed_coefficient_range': [.6, .9],
            'discounted_accrual_years': accrual, 'scale_usd': scale,
            'net_value_usd': values, 'break_even_coefficient': cost / scale,
            'double_counted_annual_accrual_value_usd': 4 * scale * .75 - cost,
            'unit_invariance_error_bound_usd': 1e-8,
            'meaning': 'Fixed-exposure conditional scenario; coefficient range is not an estimated confidence interval.'}


def bernoulli(p, value):
    return p if value else 1 - p


def servicing():
    def p_l(x, a1):
        return F(1, 5) + F(x, 5) + F(a1, 5)

    def p_y(x, a1, ell, a2):
        return F(1, 10) + F(x, 5) + F(3 * ell, 10) + F(a2, 5) + F(a1, 10)

    def policy(name, x, ell):
        return (0, 0) if name == 'never' else (1 - x, 1 - ell)

    answers = {}
    for name in ['never', 'adaptive']:
        gvalue = F(0)
        for x, ell in product([0, 1], repeat=2):
            a1, a2 = policy(name, x, ell)
            mass = F(1, 2) * bernoulli(p_l(x, a1), ell)
            gvalue += mass * (100 * p_y(x, a1, ell, a2) - 6 * a1 - 4 * a2)
        # Enumerate the complete observed law with behavior propensities,
        # including requests whose observed actions differ from the policy.
        observed_mass, weighted = F(0), F(0)
        for x, a1, ell, a2, y in product([0, 1], repeat=5):
            e2 = F(1, 4) if ell else F(3, 4)
            mass = (F(1, 2) * F(1, 2) * bernoulli(p_l(x, a1), ell)
                    * bernoulli(e2, a2) * bernoulli(p_y(x, a1, ell, a2), y))
            observed_mass += mass
            d1, d2 = policy(name, x, ell)
            weight = F(int(a1 == d1 and a2 == d2), 1) / (F(1, 2) * bernoulli(e2, a2))
            weighted += mass * weight * (100 * y - 6 * a1 - 4 * a2)
        assert observed_mass == 1 and weighted == gvalue
        answers[name] = {'g_computation': number(gvalue), 'observed_law_weighting': number(weighted),
                         'observed_cells': 32, 'probability_mass': number(observed_mass)}
    difference = F(answers['adaptive']['g_computation']['exact']) - F(answers['never']['g_computation']['exact'])
    return {'policies': answers, 'contrast_usd_per_account': number(difference),
            'cash_horizon': 'two decisions then terminal payment, zero discount in this example',
            'interpretation': 'Known generated structural law, no fitted policy or longitudinal adapter.'}


def graphs():
    forward, reverse = {}, {}
    for a, y in product([0, 1], repeat=2):
        forward[str((a, y))] = F(1, 2) * bernoulli(F(1, 5) + F(3 * a, 5), y)
        reverse[str((a, y))] = F(1, 2) * bernoulli(F(1, 5) + F(3 * y, 5), a)
    assert forward == reverse and sum(forward.values()) == 1
    effects = [F(0), F(3, 5)]
    return {'common_joint_law': {k: number(v) for k, v in forward.items()},
            'candidate_effects': [number(v) for v in effects],
            'benefit_per_success_usd': 100, 'cost_per_intervention_usd': 20,
            'net_value_set_usd_per_person': [number(100 * e - 20) for e in effects],
            'interpretation': 'Two fully specified causal models with exactly equal observed laws; not a confidence region.'}


def observations():
    values = [20, 40, 60, 80]
    inclusion = [F(1, 2), F(1), F(1, 4), F(1, 2)]
    expected_ht, expected_unweighted, mass = F(0), F(0), F(0)
    second_ht = F(0)
    for take in product([0, 1], repeat=4):
        prob = F(1)
        for p, r in zip(inclusion, take):
            prob *= bernoulli(p, r)
        if prob == 0:
            continue
        estimate = sum(F(r * y, 1) / p for r, y, p in zip(take, values, inclusion)) / 4
        raw = F(sum(r * y for r, y in zip(take, values)), sum(take))
        mass += prob
        expected_ht += prob * estimate
        second_ht += prob * estimate ** 2
        expected_unweighted += prob * raw
    direct_var = sum((1 - p) / p * y ** 2 for y, p in zip(values, inclusion)) / 16
    assert mass == 1 and expected_ht == 50
    assert second_ht - expected_ht ** 2 == direct_var
    # If the third origin is never observed, changing only its value preserves
    # the full observed law while changing the population mean.
    unseen_worlds = [[20, 40, 60, 80], [20, 40, 100, 80]]
    assert [w[:2] + w[3:] for w in unseen_worlds][0] == [w[:2] + w[3:] for w in unseen_worlds][1]
    return {'population_values': values, 'inclusion_probabilities': [str(p) for p in inclusion],
            'true_mean': 50, 'expected_ht_mean': number(expected_ht),
            'expected_unweighted_observed_mean': number(expected_unweighted),
            'variance_ht_mean': number(direct_var), 'enumerated_selections': 16,
            'zero_inclusion_population_means': [sum(w) / 4 for w in unseen_worlds],
            'shared_mapping_variance_sum': 400, 'independent_mapping_variance_sum': 200,
            'interpretation': 'Finite generated population with declared independent selection and truthful known origin identities.'}


def clocks():
    # Lexicographic (UTC time, sequence) ordering is essential for ties.
    decision = (100, 4)
    cutoff = (100, 3)
    candidates = {'available_before_cutoff': (99, 9), 'tie_allowed': (100, 3),
                  'late_same_timestamp': (100, 5), 'future_arrival': (101, 0)}
    result = {k: v <= cutoff < decision for k, v in candidates.items()}
    assert result == {'available_before_cutoff': True, 'tie_allowed': True,
                      'late_same_timestamp': False, 'future_arrival': False}
    return {'decision': decision, 'cutoff': cutoff, 'availability': candidates,
            'admitted': result, 'note': 'Illustrative admission rule, not execution of a FinMarketing validator.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = {'scope': 'Exact generated I3 examples; no sibling execution or bank evidence',
              'code_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'funding': funding(), 'servicing': servicing(), 'graphs': graphs(),
              'observations': observations(), 'clocks': clocks(),
              'accounting': {'historical': 900, 'perfect_execution': 1100,
                             'card_target': -200, 'feasible_policy_value': 980,
                             'feasible_policy_contrast': 80, 'negated_card_target': 200}}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.output.exists():
        raise FileExistsError('Choose a fresh output; preserve prior evidence')
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': 'pass', 'output': str(args.output),
                      'families': ['funding', 'servicing', 'graphs', 'observations', 'clocks', 'accounting']}))


if __name__ == '__main__':
    main()
