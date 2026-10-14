#!/usr/bin/env python3
"""Review final-study feasibility without drawing or relabeling study data."""
from fractions import Fraction as F
from math import comb, sqrt
import hashlib
import json
from pathlib import Path

from scipy.stats import beta, binom, chi2
import run_program as control

ROOT = control.core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-13/temporal-design'


def ref(p, anchor):
    return {'path': str(p.relative_to(ROOT)), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'anchor': anchor}


def exact_tail(n, k, p):
    return sum((F(comb(n, j))*p**j*(1-p)**(n-j) for j in range(k, n+1)), F(0))


def main():
    assert not (BASE / 'calculations.json').exists(), 'Preserve reviewed calculations'
    BASE.mkdir(parents=True, exist_ok=True)
    original = ROOT / 'docs/program/master/work/R04-v3'
    protocol = json.loads((original / 'protocol.json').read_text())
    results = json.loads((original / 'results.json').read_text())
    rules = protocol['acceptance_rules']
    assert rules == {'minimum_coverage': .95, 'minimum_finite_fraction': .99,
                     'simultaneous_error': .05, 'family': 16, 'bank_width_threshold': None}
    cells = []
    for c in results['cells']:
        d = c['design']; r = c['methods']['class_union']
        ratio = F(r['finite'], r['requests'])
        cells.append({'name': d['name'], 'adverse': d.get('adverse', False),
                      'requests': r['requests'], 'covered': r['covered'], 'retained': r['true_class_retained'],
                      'finite': r['finite'], 'finite_fraction_exact': str(ratio),
                      'raw_99_percent_availability_pass': ratio >= F(99, 100),
                      'coverage_screen_pass': r['minimum_95_screen'], 'width_quantiles': r['width_quantiles']})
    by_name = {c['name']: c for c in cells}
    assert by_name['persistent']['raw_99_percent_availability_pass']
    assert not by_name['weak_relevance']['raw_99_percent_availability_pass']
    assert not by_name['observational']['raw_99_percent_availability_pass']
    # Exact binomial upper tail supplies a second, independently expressed
    # check of the beta-quantile coverage certification threshold.
    family = 16; alpha = F(1, 20); error = alpha/family
    threshold = next(k for k in range(1, 513) if beta.ppf(float(error), k, 513-k) >= .95)
    assert threshold == 500
    boundary = exact_tail(512, threshold, F(19, 20))
    below = exact_tail(512, threshold-1, F(19, 20))
    assert boundary <= error < below
    power = []
    for p in [F(19, 20), F(97, 100), F(49, 50), F(99, 100), F(1)]:
        exact = exact_tail(512, threshold, p)
        scipy = float(binom.sf(threshold-1, 512, float(p)))
        assert abs(float(exact)-scipy) < 1e-13
        power.append({'true_per_cell_coverage': str(p), 'pass_probability': float(exact)})
    planning = []
    for m in [200, 268, 400]:
        nu = 2*m-2
        b2 = F(nu, nu-2)/F(3, 100)
        half2 = b2*100/(2*m*F(1, 2)**2)
        width = sqrt(float(half2))
        planning.append({'episodes_per_arm': m, 'assumed_reported_pooled_variance': 100,
                         'squared_halfwidth_exact': str(half2), 'halfwidth': width,
                         'net_lower_USD_at_effect20_cost15_cohort3000': 3000*(20-width-15)})
    assert planning[0]['net_lower_USD_at_effect20_cost15_cohort3000'] < 0
    assert planning[1]['net_lower_USD_at_effect20_cost15_cohort3000'] > 0
    # These quantiles are a development diagnostic, not certified interval
    # arithmetic and not a prospective registered study result.
    nu = 239; a = .02/9
    multipliers = [nu/chi2.ppf(1-a/2, nu), nu/chi2.ppf(a/2, nu)]
    report = {'kind': 'deterministic_design_review_no_final_draws', 'random_draws': 0,
        'predecessor_cells': cells,
        'availability_correction': {
            'observed': '507/512 = 0.990234375 is above 0.99; persistent cell passes the frozen raw finite-fraction criterion.',
            'finite_fraction_lower_bound_if_newly_required': float(beta.ppf(float(error),507,6)),
            'new_lower_bound_not_old_criterion': True,
            'all_successes_lower_bound': float(beta.ppf(float(error),512,1)),
            'warning': 'Do not retroactively add a 99-percent lower confidence-bound criterion; even 512/512 would have lower bound below .99 at this family size.'},
        'continuous_lag_bound': {'directions': 9, 'relative_tolerance': '1/4', 'error_probability': '1/50',
            'minimum_df': 14400, 'minimum_transitions': 14401, 'predecessor_transitions': 240,
            'untruncated_union_bound_at_predecessor': str(F(18,239)/F(1,4)**2),
            'n240_fallback': 'whole_line_bound_insufficient',
            'law': 'Stationary common scalar lag, iid Gaussian innovations, known graph family; no generic temporal graph proof.'},
        'coverage_certification_screen': {'requests_per_cell': 512, 'family': 16, 'family_error': .05,
            'minimum_coverage': .95, 'minimum_success_count': threshold,
            'exact_tail_at_500': float(boundary), 'exact_tail_at_499': float(below),
            'per_cell_pass_probabilities': power,
            'joint_pass_power': 'Not inferred by multiplying cells; no across-cell independence supplied.'},
        'intervention_planning': planning,
        'planning_limit': 'Pooled variance and estimated effect are held at supplied scenario values; these arithmetic thresholds are not prospective trial power or a recommended bank sample size.',
        'sharper_pivot_development_only': {'df':nu,'direction_error':a,'variance_multiplier_interval':list(map(float,multipliers)),
            'certified_quantiles':False,'purpose':'Numerical diagnostic supporting a tighter-pivot implementation route; no final performance claim.'},
        'evidence': [ref(original/'protocol.json','Unchanged R04-v3 thresholds and 512-request design'),
                     ref(original/'results.json','All predecessor cell counts and widths'),
                     ref(ROOT/'tools/master_experiment_v2.py','summary: beta lower-bound coverage and raw finite counts'),
                     ref(Path(__file__),'Independent exact-binomial and rational planning calculations')]}
    control.core.write(BASE/'calculations.json',report)
    print(json.dumps({'status':'pass','random_draws':0,'persistent_raw_availability_pass':True,
        'coverage_success_threshold':threshold,'minimum_transitions_for_displayed_bound':14401,
        'chi_square_variance_multipliers_development':multipliers}))


if __name__ == '__main__':
    main()
