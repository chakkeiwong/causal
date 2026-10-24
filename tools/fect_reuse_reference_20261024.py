#!/usr/bin/env python3
"""Independent exact arithmetic for a bounded fect source review; no imports of fect."""
from fractions import Fraction as F
import json


def calculate():
    effects = [F(2), F(4), F(10)]
    weights = [F(1), F(1), F(4)]
    cell = sum(effects) / len(effects)
    unit = ((effects[0] + effects[1]) / 2 + effects[2]) / 2
    weighted = sum(a*b for a, b in zip(effects, weights)) / sum(weights)
    assert (cell, unit, weighted) == (F(16, 3), F(13, 2), F(23, 3))
    treatment = [0, 1, 0, 0, 1, 0]
    marked = list(treatment)
    for t, d in enumerate(treatment):
        if d and t + 1 < len(treatment) and not treatment[t + 1]:
            marked[t + 1] = 2
    assert marked == [0, 1, 2, 0, 1, 2]
    means = [F(6, 5), F(1), F(11, 10)]
    ses = [F(0), F(3, 10), F(0)]
    best = min(range(3), key=lambda i: means[i])
    one_se = next(i for i in range(3) if means[i] <= means[best]+ses[best])
    one_pct = next(i for i in range(3) if means[i] <= means[best]*F(101, 100))
    assert (best, one_se, one_pct) == (1, 0, 1)
    # A diagonal 2 by 2 matrix avoids numerical SVD and isolates scaling.
    singular = [F(12), F(4)]
    lam = F(3, 2)
    normalized = [s/4 for s in singular]
    shrunk = [4*max(s-lam, F(0)) for s in normalized]
    assert shrunk == [F(6), F(0)]
    theta = F(10)
    null_quantiles = [F(-1), F(1)]  # type-7 .25/.75 of [-2,-1,0,1,2]
    unshifted = [2*theta-null_quantiles[1], 2*theta-null_quantiles[0]]
    shifted = [theta-null_quantiles[1], theta-null_quantiles[0]]
    assert unshifted == [F(19), F(21)] and shifted == [F(9), F(11)]
    fold_mean = (F(1)+F(9))/2
    pooled_mean = (100*F(1)+F(9))/101
    assert fold_mean == 5 and pooled_mean == F(109,101) and pooled_mean < 3 < fold_mean
    conditional_iterations = len(range(501))
    cap_warning = conditional_iterations >= 5000
    assert conditional_iterations == 501 and not cap_warning
    return {
        'provenance': 'Authored exact finite arithmetic; no downloaded code, native trial or coverage guarantee',
        'targets': {'effects_thousand_USD': list(map(str, effects)),
                    'treated_cell': str(cell), 'equal_unit': str(unit),
                    'weights': list(map(str, weights)), 'weighted_cell': str(weighted)},
        'carryover': {'treatment': treatment, 'one_step_marked': marked,
                      'claim': 'Synthetic regular-clock status coding, not a carryover identification proof'},
        'validation': {'fold_sizes': [100, 1], 'A_fold_mspe': [1, 9],
                       'A_equal_fold_mean': str(fold_mean), 'A_pooled_cell_mean': str(pooled_mean),
                       'B_fold_mspe': [3, 3], 'B_equal_fold_mean': '3',
                       'B_pooled_cell_mean': '3',
                       'minimum_index': best, 'one_se_index': one_se, 'one_pct_index': one_pct,
                       'candidate_means': list(map(str, means)), 'candidate_se': list(map(str, ses)),
                       'clock': {'sampled_unit_train': [1, 2], 'buffer': [3],
                                 'holdout': [4, 5], 'future_drop': [6],
                                 'unsampled_unit_train': [1, 2, 3, 4, 5, 6]}},
        'shrinkage': {'shape': [2, 2], 'diagonal': [12, 4], 'lambda': str(lam),
                      'normalized_singular_values': list(map(str, normalized)),
                      'soft_thresholded_diagonal': list(map(str, shrunk))},
        'basic_interval': {'theta': str(theta), 'null_draws': [-2, -1, 0, 1, 2],
                           'alpha': '1/2', 'unshifted': list(map(str, unshifted)),
                           'shifted': list(map(str, shifted)),
                           'claim': 'Arithmetic of location centering; no calibration inference'},
        'iteration_guard': {'requested_max': 5000, 'helper_hard_cap': 500,
                            'possible_iterations_if_never_converged': conditional_iterations,
                            'wrapper_cap_warning': cap_warning,
                            'claim': 'Conditional source control-flow witness, not observed package failure'},
        'costs': {'illustrative_USD': 4800, 'requested': 240, 'finite': 200, 'accepted': 160,
                  'per_request': str(F(4800, 240)), 'per_finite': str(F(4800, 200)),
                  'per_accepted': str(F(4800, 160))},
        'native_execution': False}


if __name__ == '__main__':
    print(json.dumps(calculate(), indent=2) + '\n')
