#!/usr/bin/env python3
"""Generated counterexamples for population and portfolio composition."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    effects, source, target = [10, -10], [F(4, 5), F(1, 5)], [F(1, 5), F(4, 5)]
    source_effect = sum(p * v for p, v in zip(source, effects))
    target_effect = sum(p * v for p, v in zip(target, effects))
    ratios = [q / p for p, q in zip(source, target)]
    transported = sum(p * w * v for p, w, v in zip(source, ratios, effects))
    assert source_effect == 6 and target_effect == transported == -6
    values = {(f, s): 100 + 20 * f + 15 * s - 30 * f * s for f in [0, 1] for s in [0, 1]}
    interaction = values[1, 1] - values[1, 0] - values[0, 1] + values[0, 0]
    isolated = values[1, 0] + values[0, 1] - 2 * values[0, 0]
    joint = values[1, 1] - values[0, 0]
    assert isolated == 35 and interaction == -30 and joint == isolated + interaction == 5
    # A funding population of 100, servicing population of 60 and overlap20.
    portfolio_direct = 80 * 20 + 40 * 15 + 20 * 5
    portfolio_inclusion = 100 * 20 + 60 * 15 + 20 * interaction
    assert portfolio_direct == portfolio_inclusion == 2300
    assert sum([3, -3]) == 0
    result = {'scope': 'Supplied conditional effects, fixed population memberships and known joint net-value table; no observed bank evidence',
              'code_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'population': {'stratum_effects': effects, 'source_weights': [str(p) for p in source],
                             'target_weights': [str(p) for p in target], 'density_ratios': [str(w) for w in ratios],
                             'source_effect': str(source_effect), 'target_effect': str(target_effect),
                             'transported_effect': str(transported)},
              'joint_actions': {'values': {str(k):v for k,v in values.items()}, 'isolated_sum': isolated,
                                'interaction': interaction, 'joint_effect': joint,
                                'portfolio_total': portfolio_direct, 'naive_portfolio_total': 2900,
                                'funding_count': 100, 'servicing_count': 60, 'overlap_count': 20},
              'internal_transfer': {'branch': 3, 'treasury': -3, 'consolidated': 0}}
    if args.output.exists():
        raise FileExistsError('Preserve evidence; choose a fresh output')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
