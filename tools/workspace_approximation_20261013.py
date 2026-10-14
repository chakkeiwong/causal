#!/usr/bin/env python3
"""Finite exact reference for mapping provider approximation into value.

Two declared probabilities are illustrative inputs, not BayesFilter output.
"""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    low, high = F(3, 5), F(9, 10)
    exact_p, approximate_p = F(2, 5), F(1, 2)
    exact_mean = low * (1 - exact_p) + high * exact_p
    approximate_mean = low * (1 - approximate_p) + high * approximate_p
    tv = (abs(exact_p - approximate_p) + abs((1 - exact_p) - (1 - approximate_p))) / 2
    error_bound = (high - low) * tv
    assert exact_mean == F(18, 25) and approximate_mean == F(3, 4)
    assert abs(exact_mean - approximate_mean) == error_bound == F(3, 100)
    # A direct common-uniform coupling also attains the TV error bound:
    # common mass .4 high, .5 low; mismatched mass .1.
    coupled_error = F(1, 10) * abs(high - low)
    assert coupled_error == error_bound
    scale = 100000 * sum(.25 / 1.04 ** (q / 4) for q in range(1, 5))
    result = {'scope': 'Supplied two-state distributions; no actual filter execution or error certification',
              'code_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'exact_mean_coefficient': str(exact_mean),
              'approximate_mean_coefficient': str(approximate_mean),
              'total_variation_distance': str(tv), 'coefficient_error_bound': str(error_bound),
              'exact_conditional_value_usd': scale * float(exact_mean) - 40000,
              'approximate_conditional_value_usd': scale * float(approximate_mean) - 40000,
              'absolute_value_error_bound_usd': scale * float(error_bound),
              'two_sided_outer_value_range_usd': [scale * float(approximate_mean - error_bound) - 40000,
                                                 scale * float(approximate_mean + error_bound) - 40000]}
    if args.output.exists():
        raise FileExistsError('Preserve earlier result; choose a fresh output path')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
