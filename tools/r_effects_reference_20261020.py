#!/usr/bin/env python3
"""Exact authored laws for target, missing-treatment and dose-unit contracts."""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
import json


def integral(coeff, upper=F(2)):
    return sum(c*upper**(i+1)/F(i+1) for i, c in enumerate(coeff))/upper


def calculate():
    # Two equally probable baseline groups; conditional slopes1and3,
    # conditional treatment variances1and4. A common PLR score reweights them.
    average_slope = (F(1)+F(3))/2
    pooled_slope = (F(1)*F(1)+F(4)*F(3))/(F(1)+F(4))
    # R indicates that the treatment label is observed. R and randomized A are
    # independent fair coins. In R=1 both worlds have Y(a)=a. In R=0 the second
    # world has Y(a)=1-a. Observed Y distributions agree after erasing that label.
    worlds = []
    for reverse in [False, True]:
        observed = defaultdict(F)
        ate = F(0)
        for r, a in product([0, 1], repeat=2):
            y0, y1 = ((1, 0) if reverse and r == 0 else (0, 1))
            observed[(r, a if r else None, y1 if a else y0)] += F(1, 4)
            ate += F(y1-y0, 4)
        worlds.append((observed, ate))
    assert worlds[0][0] == worlds[1][0]
    # W~Uniform[0,2] in thousands of dollars; Y(w)=20w^2-5w dollars.
    ew, ew2 = integral([F(0), F(1)]), integral([F(0), F(0), F(1)])
    ey = integral([F(0), F(-5), F(20)])
    ewy = integral([F(0), F(0), F(-5), F(20)])
    slope = (ewy-ew*ey)/(ew2-ew*ew)
    assert slope == F(35)
    # Location-scale GPS: both residuals0, scales1and2, same residual density k.
    # True f(W|X)=k/s versus the unscaled residual density k. With numerator k,
    # correct stabilized weights1and2 become1and1 if scale is omitted.
    correct_mean = (F(1)*0+F(2)*100)/(F(1)+F(2))
    wrong_mean = (F(1)*0+F(1)*100)/(F(1)+F(1))
    assert correct_mean-wrong_mean == F(50, 3)
    result = dict(
        scope='Authored exact population laws; no R package execution or bank observations',
        target_weighting=dict(average_conditional_slope=str(average_slope),
            pooled_partial_linear_slope=str(pooled_slope),
            formula='E[var(W|X)*slope(X)] / E[var(W|X)]'),
        missing_treatment=dict(observed_laws_equal=True,
            law=[dict(R=r, recorded_A=a, Y=y, probability=str(p))
                for (r, a, y), p in worlds[0][0].items()],
            ATE_worlds=[str(x[1]) for x in worlds],
            assumed_100USD_outcome_scale_effects=[str(100*x[1]) for x in worlds],
            restriction='Treatment randomization holds; observation positivity fails for R=0; no transport restriction granted.'),
        continuous_response=dict(exposure_unit='USD1000 of incremental limit',
            outcome_unit='USD stipulated margin', support='W uniform on [0,2]',
            response='20W^2-5W', projection_slope=str(slope),
            derivative_at_zero='-5', contrast_zero_to_one='15',
            false_slope_prediction_zero_to_one=str(slope),
            slope_per_exposure_dollar=str(slope/1000)),
        density_scale=dict(scales=['1','2'], correct_weights=['1','2'], unscaled_weights=['1','1'],
            correct_weighted_mean=str(correct_mean), unscaled_weighted_mean=str(wrong_mean),
            difference=str(correct_mean-wrong_mean),
            constant_unit_change='Both numerator and denominator densities divide by the same positive unit factor; their ratio is unchanged.',
            scope_limit='Two-row algebra illustration, not a causal effect estimate or measured package discrepancy.'),
        bootstrap_order_statistics=dict(replicates_20_lower_index=0,
            replicates_40_lower_index=1, formula='floor(0.025*B)',
            limitation='Index algebra only; actual R return shape and bootstrap validity unexecuted.'))
    assert average_slope == 2 and pooled_slope == F(13, 5)
    assert [x[1] for x in worlds] == [F(1), F(0)]
    return result


if __name__ == '__main__':
    print(json.dumps(calculate(), indent=2))
