#!/usr/bin/env python3
"""Independent rational witnesses; never imports acquired upstream code."""
from fractions import Fraction as F
import json

def calculate():
    labels = ['A', 'B', 'C', 'D']
    rows = labels.copy()
    selected = []
    n0 = len(rows) - 1
    for i in range(n0 - 1):
        rows[i], rows[-1] = rows[-1], rows[i]
        selected.append(rows[-1])
    rows[0], rows[-1] = rows[-1], rows[0]
    selected.append(rows[-1])
    assert selected == ['A', 'B', 'D']
    def variance(xs):
        mean = sum(xs, F(0)) / len(xs)
        return sum((x - mean)**2 for x in xs) / (len(xs) - 1)
    effects = dict(A=F(2), B=F(4), C=F(6), D=F(10))
    subset = variance([effects[x] for x in selected])
    full = variance(list(effects.values()))
    assert subset == F(52, 3) and full == F(35, 3)
    # Identical pre-period donor values leave all simplex weights optimal.
    fits = []
    for a in [F(0), F(1, 2), F(1)]:
        pre = a * 100 + (1-a) * 100
        post = a * 100 + (1-a) * 200
        fits.append(dict(weight=str(a), pre_loss=str((100-pre)**2),
                         counterfactual=str(post), effect=str(150-post)))
    # Example denominator arithmetic, without a calibrated probability claim.
    finite_rank = F(1, 3)
    all_requested_bounds = [F(1, 5), F(3, 5)]
    # R's na.rm row sum ignores missing elements; this witnesses only the guard.
    network_row = [None, F(1)]
    observed_sum = sum((x for x in network_row if x is not None), F(0))
    assert observed_sum == 1
    # Stated hypothetical costs for three distinct denominators.
    costs = {str(n): str(F(15000, n)) for n in [500, 300, 250]}
    assert costs == {'500': '30', '300': '50', '250': '60'}
    return dict(placebo_labels=selected, omitted_label='C',
                selected_variance=str(subset), full_variance=str(full),
                indistinguishable_prefit=fits, finite_rank=str(finite_rank),
                all_requested_rank_bounds=list(map(str, all_requested_bounds)),
                zero_effect_without_se_fitted_predicate=False,
                missing_network_row_guard_sum=str(observed_sum),
                hypothetical_costs_usd=costs, native_execution=False,
                scientific_calibration_claim=False)

if __name__ == '__main__':
    print(json.dumps(calculate(), indent=2))
