#!/usr/bin/env python3
"""Exact authored witnesses, not native package output or calibration evidence."""
from fractions import Fraction as F
import json


def calculate():
    clean = F(80, 2) + F(120, 2)
    contaminated = F(80, 2) + F(140, 2)
    ratios = [4, 4, 1]
    inclusive = [F(sum(x >= r for x in ratios), len(ratios)) for r in ratios]
    effects = [F(0), F(2)]
    mean = sum(effects) / len(effects)
    ss = sum((x - mean) ** 2 for x in effects)
    accepted_grid = [F(0), F(2)]
    return {
        'donor_spillover': dict(clean_counterfactual=str(clean), contaminated_counterfactual=str(contaminated), clean_gap=str(120-clean), contaminated_gap=str(120-contaminated)),
        'tied_placebos': dict(ratios=ratios, ordered_rank=[str(F(i+1,3)) for i in range(3)], inclusive_tail=[str(x) for x in inclusive]),
        'failed_draws': dict(requested=19, finite=10, missing=9, exceedances=2, finite_frequency=str(F(2,10)), all_request_lower=str(F(2,19)), all_request_upper=str(F(11,19)), interpretation='Unknown failed-draw classifications; bounds on exceedance frequency, not calibrated p-values.'),
        'resampling_support': dict(iid_zero_exceedance_raw='0', iid_plus_one=str(F(1,20)), cyclic_five_unique_max=str(F(1,5))),
        'jackknife_population': dict(full_n=4, selected_m=2, replicate_effects=[str(x) for x in effects], squared_deviations=str(ss), full_n_scale=str(F(3,4)*ss), selected_m_scale=str(F(1,2)*ss), interpretation='Different formulas; neither establishes valid sampling-law inference.'),
        'grid_hull': dict(accepted=[str(x) for x in accepted_grid], rejected_inside='1', hull=[str(min(accepted_grid)),str(max(accepted_grid))], empty_grid='No finite interval; explicit refusal required.'),
        'solver_boundary': dict(sigfig=5, requested=5, break_predicate=5>=5, converged_predicate=5>5, native_execution=False),
        'cost': dict(total_usd=9000, attempted=300, conformant=240, useful=150, per_attempt=str(F(9000,300)), per_conformant=str(F(9000,240)), per_useful=str(F(9000,150)), observed=False),
    }


if __name__ == '__main__':
    print(json.dumps(calculate(), indent=2))
