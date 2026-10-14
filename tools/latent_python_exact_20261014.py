#!/usr/bin/env python3
"""Exact authored borrower-readiness counterexample for the Python latent cell."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/program/execution/2026-10-14/latent-python/exact-results.json'


def law_direct():
    joint = {(a, y): F(0) for a, y in product((0, 1), repeat=2)}
    for a, e in product((0, 1), repeat=2):
        p = F(1, 2) * (F(1, 5) if e else F(4, 5))
        joint[(a, a ^ e)] += p
    return joint


def law_hidden():
    joint = {(a, y): F(0) for a, y in product((0, 1), repeat=2)}
    for u, ea, ey in product((0, 1), repeat=3):
        p = F(1, 2)
        p *= F(1, 10) if ea else F(9, 10)
        p *= F(1, 8) if ey else F(7, 8)
        joint[(u ^ ea, u ^ ey)] += p
    return joint


def main():
    direct, hidden = law_direct(), law_hidden()
    assert direct == hidden == {(0, 0): F(2, 5), (0, 1): F(1, 10),
                                  (1, 0): F(1, 10), (1, 1): F(2, 5)}
    # In the first law Y=A xor noise(1/5); in the second Y depends on U only.
    effects = {'direct': F(3, 5), 'hidden': F(0)}
    value = {name: 100 * (effect * 100 - 10) for name, effect in effects.items()}
    assert value == {'direct': F(5000), 'hidden': F(-1000)}
    result = {
        'status': 'pass', 'kind': 'authored synthetic exact construction',
        'variables': {'A': 'early relief offer', 'Y': '30-day repayment indicator',
                      'U': 'unobserved borrower readiness in hidden law'},
        'law_direct': 'A~Bernoulli(1/2); E~Bernoulli(1/5); Y=A xor E',
        'law_hidden': 'U~Bernoulli(1/2); EA~Bernoulli(1/10); EY~Bernoulli(1/8); A=U xor EA; Y=U xor EY',
        'observed_joint': {f'A{a}Y{y}': str(p) for (a, y), p in direct.items()},
        'observed_conditional_repayment': {'A1': '4/5', 'A0': '1/5'},
        'interventional_effects': {k: str(v) for k, v in effects.items()},
        'stipulated_economics': {'eligible_accounts': 100,
                                 'value_per_extra_repayment_usd': 100,
                                 'offer_cost_per_account_usd': 10,
                                 'incremental_net_usd': {k: str(v) for k, v in value.items()}},
        'interpretation': 'The same positive observed association supports opposite offer choices under two distinct structural laws. No bank data or package runtime is used.'}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open('x') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print(json.dumps({'observed_joint': result['observed_joint'],
                      'incremental_net_usd': result['stipulated_economics']['incremental_net_usd']}))


if __name__ == '__main__':
    main()
