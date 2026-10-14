#!/usr/bin/env python3
"""Deterministic feasibility review; no final sampling or protocol registration."""
from fractions import Fraction as F
from itertools import product
import json
import math
from pathlib import Path

from scipy.stats import beta, binom
import master_control as core
from build_integrated_monograph_v12 import ref
from review_temporal_design_20261013 import exact_tail

ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-13/dependent-design'


def main():
    output = BASE / 'calculations.json'
    assert not output.exists(), 'Preserve reviewed calculations'
    original = ROOT / 'docs/program/master/work/R05-v2'
    protocol = json.loads((original / 'protocol.json').read_text())
    results = json.loads((original / 'results.json').read_text())
    rules = protocol['acceptance_rules']
    assert rules == {'minimum_coverage': .95, 'minimum_finite_fraction': .99,
                     'simultaneous_error': .05, 'family': 16, 'bank_width_threshold': None}
    cells = []
    for row in results['cells']:
        cells.append({'design': row['design'], 'methods': {
            name: {k: value[k] for k in ['requests', 'covered', 'finite', 'minimum_95_screen',
                                       'simultaneous_lower95', 'width_quantiles']}
            for name, value in row['methods'].items()}})
    # Re-enumerate the existing authored marginal law. At each date a lag-zero
    # or a finite moving window of independent signs can supply bounded inputs;
    # the rows below assess only this exact marginal law and stipulated d.
    worlds = []
    theta = F(6, 5)
    for x, v, eta, eps in product([-1, 1], repeat=4):
        z = F(3, 10)*x+v
        a = F(4, 5)*z+F(1, 5)*x+eta
        y = theta*a+F(2, 5)*x+eps
        worlds.append((z, a, y, z-F(3, 10)*x, a-F(11, 25)*x, y-F(116, 125)*x))
    bounds = [max(abs(w[j]) for w in worlds) for j in range(3)]
    bz, ba, by = bounds
    q0 = sum(w[3]*w[4] for w in worlds)/16
    m0 = sum(w[3]*w[5] for w in worlds)/16
    assert bounds == [F(13, 10), F(56, 25), F(511, 125)]
    assert (q0, m0) == (F(4, 5), F(24, 25))
    alpha = F(3, 100)
    threshold = F(23, 20)
    margin = m0-threshold*q0
    assert margin == F(1, 25)
    planning = []
    for d in [0, 4, 19]:
        q = d+1
        logterm = math.log(float(4*q/alpha))
        # Strict inequalities: the next integer class size makes the centered
        # denominator positive, or the whole ratio set exceed the action cost.
        need_finite = float((8*bz*ba/q0)**2)*logterm/2
        need_action = float((8*bz*(by+threshold*ba)/margin)**2)*logterm/2
        min_class_finite = math.floor(need_finite)+1
        min_class_action = math.floor(need_action)+1
        for n in [640, 65536, 1048576]:
            nmin = n//q
            tscale = math.sqrt(logterm/(2*nmin))
            wm, wq = float(8*bz*by)*tscale, float(8*bz*ba)*tscale
            ml, mu, ql, qu = float(m0)-wm, float(m0)+wm, float(q0)-wq, float(q0)+wq
            if ql > 0:
                corners = [m/qv for m in [ml, mu] for qv in [ql, qu]]
                effect = [min(corners), max(corners)]
                topology = 'finite_interval'
            elif ml <= 0 <= mu:
                effect, topology = None, 'whole_line'
            else:
                effect, topology = None, 'unbounded_union'
            planning.append({'d': d, 'evaluation_rows': n, 'smallest_residue_class': nmin,
                'oracle_nuisance_errors': [0, 0, 0], 'numerator_radius': wm, 'denominator_radius': wq,
                'centered_topology': topology, 'centered_effect_interval': effect,
                'centered_above_action_threshold': bool(ql > 0 and ml > float(threshold)*qu),
                'minimum_rows_for_centered_positive_denominator': q*min_class_finite,
                'minimum_rows_for_centered_action_above_1_15': q*min_class_action})
        assert float(8*bz*ba)*math.sqrt(logterm/(2*min_class_finite)) < float(q0)
        assert float(8*bz*(by+threshold*ba))*math.sqrt(logterm/(2*min_class_action)) < float(margin)
    assert all(r['centered_topology'] == 'whole_line' for r in planning if r['evaluation_rows'] == 640)
    # Even infinite calibration cannot shrink a noise-unsubtracted loss bound
    # below the irreducible loss for an oracle learner.
    noise_variance = [F(1), F(41, 25), F(2101, 625)]
    assert noise_variance == [sum(w[j+3]**2 for w in worlds)/16 for j in range(3)]
    floor_q = math.sqrt(float(noise_variance[0]*noise_variance[1]))
    floor_m = math.sqrt(float(noise_variance[0]*noise_variance[2]))
    assert floor_q > float(q0) and floor_m > float(m0)
    # Coverage certification is separate from nominal coverage and availability.
    error = F(1, 20)/16
    successes = next(k for k in range(1, 513) if beta.ppf(float(error), k, 513-k) >= .95)
    assert successes == 500
    tail = exact_tail(512, successes, F(19, 20))
    below = exact_tail(512, successes-1, F(19, 20))
    assert tail <= error < below
    power = []
    for p in [F(19, 20), F(97, 100), F(49, 50), F(99, 100), F(1)]:
        exact = exact_tail(512, successes, p)
        assert abs(float(exact)-float(binom.sf(successes-1, 512, float(p)))) < 1e-13
        power.append({'true_coverage': str(p), 'per_cell_pass_probability': float(exact)})
    report = {
        'kind': 'deterministic_design_feasibility_no_final_draws', 'random_draws': 0,
        'predecessor_acceptance': rules, 'predecessor_cells': cells,
        'authored_marginal_law': {'worlds': 16, 'bounds_Z_A_Y': [str(x) for x in bounds],
            'truth': str(theta), 'Q': str(q0), 'M': str(m0),
            'action_threshold': str(threshold), 'decision_moment_margin': str(margin),
            'evaluation_error_allocation': str(alpha)},
        'centered_oracle_planning': planning,
        'planning_limit': 'Moment estimates held at their population centers, e_j=0, known d and all bounds exact. These deterministic width screens are not ex ante coverage/power, a bank sample-size recommendation or the old Gaussian experiment. No actual pilot was fitted.',
        'uncorrected_calibration_floor': {'oracle_squared_losses': [str(v) for v in noise_variance],
            'noise_lower_bound': 0, 'infinite_calibration_product_Q': floor_q,
            'infinite_calibration_product_M': floor_m, 'centered_topology': 'whole_line',
            'limit': 'This worst-case risk certificate stays wide even for exact means; it is not actual nuisance error. Known justified residual-variance lower bounds can reduce this floor in this generated law.'},
        'certification_screen': {'requests': 512, 'family': 16, 'minimum_success_count': successes,
            'tail_at_500_under_p_95': float(tail), 'tail_at_499_under_p_95': float(below),
            'per_cell_power': power, 'finite_availability_rule': 'Raw fraction >= .99; 507/512 suffices.',
            'all_successes_lower_bound': float(beta.ppf(float(error), 512, 1)),
            'joint_power': 'Not calculated from a product; across-cell dependence is unspecified.'},
        'evidence': [ref(original/'protocol.json', 'Frozen actual predecessor law, sample sizes and thresholds'),
            ref(original/'results.json', 'All predecessor methods and adverse cells'),
            ref(ROOT/'docs/program/execution/2026-10-13/dependent-learner/argument-review.json', 'Restricted argument review'),
            ref(ROOT/'docs/program/execution/2026-10-13/dependent-learner/exact-results.json', 'Preserved exact finite law and small references'),
            ref(Path(__file__), 'Rational law enumeration, deterministic bound and exact-binomial calculations'),
            ref(ROOT/'tools/review_temporal_design_20261013.py', 'Reused exact rational binomial tail implementation')]}
    core.write(output, report)
    print(json.dumps({'status': 'pass', 'final_draws': 0, 'coverage_threshold': successes,
        'oracle_center_n640': 'whole_line_for_all_three_d_values',
        'n_iid_centered_finite': planning[0]['minimum_rows_for_centered_positive_denominator'],
        'n_iid_centered_action': planning[0]['minimum_rows_for_centered_action_above_1_15'],
        'noise_uncorrected_calibration': 'nonshrinking_whole_line_at_center'}))


if __name__ == '__main__':
    main()
