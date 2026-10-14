#!/usr/bin/env python3
"""Exact finite examples of conditional support and noncommuting aggregation."""
from fractions import Fraction as F
import json


def main():
    numerator = (F(3, 1000), F(5, 1000))
    denominator = (F(6, 1000), F(14, 1000))
    ratio = (numerator[0] / denominator[1], numerator[1] / denominator[0])
    assert numerator[1] <= denominator[0]
    assert ratio == (F(3, 14), F(5, 6))
    group_probabilities = (F(1, 5), F(1, 2))
    mean_probability = sum(group_probabilities) / 2
    mean_odds = sum(p / (1 - p) for p in group_probabilities) / 2
    assert mean_probability == F(7, 20)
    assert mean_odds / (1 + mean_odds) == F(5, 13)
    result = {
        "kind": "exact_generated_numerical_examples", "random_draws": 0,
        "ratio": {"numerator_interval": numerator, "denominator_interval": denominator,
                  "ratio_interval": ratio, "point_ratio": F(4, 1000) / F(10, 1000)},
        "noncommuting_odds": {"mean_probability": mean_probability,
                              "odds_of_mean": mean_probability / (1 - mean_probability),
                              "mean_odds": mean_odds,
                              "probability_from_mean_odds": mean_odds / (1 + mean_odds)},
    }
    print(json.dumps(result, default=str, indent=2))


if __name__ == '__main__':
    main()
