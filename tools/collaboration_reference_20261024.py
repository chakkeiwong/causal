#!/usr/bin/env python3
"""Authored exact examples and checks of reported numbers; no upstream code."""
from fractions import Fraction as F
import json


def calculate():
    # A stipulated bank response law, not an estimate from the chess paper.
    states = [dict(h=-1, p0=F(2, 100), p1=F(4, 100)),
              dict(h=1, p0=F(4, 100), p1=F(2, 100))]
    loss = 10000
    advantages = {s['h']: loss * (s['p0'] - s['p1']) for s in states}
    full = sum(max(F(0), v) for v in advantages.values()) / 2
    constant = max(F(0), sum(advantages.values()) / 2)
    typed_bit = sum(max(F(0), advantages[h]) for h in [-1, 1]) / 2
    assert full == typed_bit == 100 and constant == 0
    # Crossed ratings: a shared rater effect and a shared position effect.
    raters, positions = 12, 15
    crossed = F(1, raters) + F(1, positions)
    iid = F(2, raters * positions)
    assert crossed == F(3, 20) and iid == F(1, 90)
    # Neither caption/heading arithmetic nor this example reproduces a run.
    values = dict(
        training_overhead_8b=(F('16.8') - 15) / 15,
        wild_table14_14b=(F(57) + 54 + 60) / 3,
        wild_table18_14b=F(49),
        rationale_table15_14b=(F(44) + F('56.6')) / 2,
        rationale_table18_14b=F('45.8'),
        difficulty_table17_14b=F('0.67'),
        difficulty_table18_14b=F('0.71'),
        verbal_tool_return_tokens=F('2.9') * 150,
        latent_tool_return_tokens=F('1.9') * 182,
        all_judgments_preference=F(130, 180),
        non_tie_preference=F(130, 162),
        full_information_savings=full,
        lossy_summary_savings=constant,
        typed_text_savings=typed_bit,
        crossed_rating_variance=crossed,
        mistaken_iid_rating_variance=iid,
        variance_ratio=crossed / iid,
    )
    assert values['training_overhead_8b'] == F(3, 25)
    assert values['wild_table14_14b'] == 57
    assert values['rationale_table15_14b'] == F('50.3')
    assert values['variance_ratio'] == F('13.5')
    return dict(scope='Authored arithmetic and stipulated examples; not empirical replication',
                exact={k: str(v) for k, v in values.items()},
                decimal={k: float(v) for k, v in values.items()},
                action_advantages={str(k): str(v) for k, v in advantages.items()},
                native_execution=False)


if __name__ == '__main__':
    print(json.dumps(calculate(), indent=2))
