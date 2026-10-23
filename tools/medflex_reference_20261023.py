#!/usr/bin/env python3
"""Independent exact examples; no upstream R code imported or executed."""
from fractions import Fraction as F
import json


def calculate():
    p = {0: F(1, 5), 1: F(3, 5)}
    def outcome(x, m):
        return 10 + 2*x + 5*m + 4*x*m
    mu = {(x, a): (1-p[a])*outcome(x, 0) + p[a]*outcome(x, 1)
          for x in [0, 1] for a in [0, 1]}
    pnde = mu[1, 0] - mu[0, 0]
    tnie = mu[1, 1] - mu[1, 0]
    pnie = mu[0, 1] - mu[0, 0]
    tnde = mu[1, 1] - mu[0, 1]
    total = mu[1, 1] - mu[0, 0]
    assert pnde + tnie == pnie + tnde == total == F(32, 5)
    assert pnde != tnde and pnie != tnie
    original_scores = [F(-1), F(1)]
    replicated_scores = [x for x in original_scores for _ in range(2)]
    subject_variance = sum(x*x for x in original_scores) / len(original_scores)**2
    naive_variance = sum(x*x for x in replicated_scores) / len(replicated_scores)**2
    assert subject_variance == F(1, 2) and naive_variance == F(1, 4)
    # A inverse first row is (1,2); B is [[1,1/2],[1/2,1]].
    full_variance_factor = 1 + 2*2*F(1, 2) + 4
    assert full_variance_factor == 7
    return dict(kind='project_owned_exact_reference', native_execution=False,
        nested_means={str(x)+str(a): str(v) for (x,a),v in mu.items()},
        effects=dict(pure_direct=str(pnde), total_indirect=str(tnie), pure_indirect=str(pnie),
            total_direct=str(tnde), total=str(total)),
        original_subject_score_variance=str(subject_variance), naive_expanded_row_variance=str(naive_variance),
        joint_score_variance_factor=str(full_variance_factor), frozen_nuisance_variance_factor='1',
        mediator_probability_ratios=dict(event=str(p[1]/p[0]), nonevent=str((1-p[1])/(1-p[0]))),
        stipulated_economics=dict(value_per_unit='10', total_policy_cost='50',
            total_net=str(10*total-50), direct_component_minus_same_cost=str(10*pnde-50)),
        limitations=['The nested mean law is stipulated, not estimated or identified from bank data.',
            'Natural-effect components have different cross-world definitions and do not each specify an implementable policy.',
            'Score covariance examples illustrate dependence/nuisance propagation, not a medflex numerical result or coverage study.',
            'No external package or downloaded code executed.'])


if __name__ == '__main__':
    print(json.dumps(calculate(), indent=2))
