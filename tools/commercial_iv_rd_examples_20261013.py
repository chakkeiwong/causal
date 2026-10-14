#!/usr/bin/env python3
"""Exact authored banking counterexamples; no vendor or downloaded engine execution."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


def calculate():
    # Same first-stage and reduced-form means, different exclusion assumptions.
    threshold_worlds = []
    for effect, direct, baseline in [(F(50), F(0), F(80)), (F(30), F(8), F(84))]:
        p0, p1 = F(1, 5), F(3, 5)
        means = [baseline+effect*p0, baseline+effect*p1+direct]
        assert means == [F(90), F(110)]
        threshold_worlds.append({'causal_effect': str(effect), 'direct_assignment_jump': str(direct),
            'baseline': str(baseline), 'outcome_means': [str(v) for v in means],
            'action_probabilities': [str(p0), str(p1)], 'wald_summary_ratio': '50',
            'value_if_cost40': str(effect-40)})
    # Exogenous instrument signs with direct effects proportional to relevance:
    # every population instrument moment fits coefficient 40, while do(A) is 30.
    moments = [F(0), F(0)]
    for z1, z2, v, u in product([-1, 1], repeat=4):
        a = z1+2*z2+v
        y = 30*a+10*(z1+2*z2)+u
        for j, z in enumerate([z1, z2]):
            moments[j] += F(z*(y-40*a), 16)
    assert moments == [0, 0]
    # Discrete scores have no observations arbitrarily close to zero. A
    # quadratic factor is zero at -2,-1 and one at the missing cutoff.
    def untreated(x, delta):
        return 100+10*x+delta*(x+1)*(x+2)/2
    rd_worlds = []
    for delta in [F(0), F(40)]:
        observed = [untreated(F(x), delta) if x < 0 else 120+10*x for x in [-2, -1, 1, 2]]
        assert observed == [F(80), F(90), F(130), F(140)]
        effect_at_zero = 120-untreated(F(0), delta)
        rd_worlds.append({'delta': str(delta), 'observed_means': [str(x) for x in observed],
            'smooth_untreated_limit_at_zero': str(untreated(F(0), delta)),
            'smooth_treated_limit_at_zero': '120', 'effect_at_zero': str(effect_at_zero)})
    # A narrow numeric grid can miss both pieces of a valid supplied set.
    probes = [F(k, 10) for k in range(-50, 51)]
    hits = [str(t) for t in probes if (max(F(1), min(-t/2, t/2)) <= min(F(2), max(-t/2, t/2)))]
    assert hits and all(abs(F(t)) >= 2 for t in hits)
    assert not any(abs(t) <= 1 for t in probes if str(t) in hits)
    return {'kind': 'project_exact_iv_rd_examples', 'random_draws': 0,
        'threshold_worlds': threshold_worlds,
        'threshold_limit': 'Identical two first-stage and two reduced-form means, not a claim of equal complete distributions. Constant effect and direct-effect restrictions are stipulated.',
        'overidentification': {'law': 'Z1,Z2,V,U independent fair signs; A=Z1+2Z2+V; Y=30A+10(Z1+2Z2)+U',
            'population_instrument_moments_at_40': [str(x) for x in moments],
            'controlled_causal_effect': 30, 'all_moment_fitting_coefficient': 40,
            'limit': 'Population moments only; no finite-sample test output or automatic IV diagnosis.'},
        'discrete_score': {'support': [-2, -1, 1, 2], 'worlds': rd_worlds,
            'limit': 'Both response functions are smooth, but continuity alone does not determine the missing limit on a support with a gap. A curvature bound, specified functional model or new score information changes the conclusion.'},
        'weak_projection': {'numerator': [1, 2], 'denominator': ['-1/2', '1/2'],
            'exact_set': [[None, -2], [2, None]], 'grid_on_minus1_plus1_has_no_points': True,
            'membership_checks': len(probes), 'limit': 'Supplied deterministic rectangle; not a Stata AR/CLR run or a sampling-coverage guarantee.'},
        'vendor_execution': False, 'bank_prices': False}


if __name__ == '__main__':
    dest = Path(__file__).resolve().parents[1] / 'docs/program/execution/2026-10-13/commercial-iv-rd/exact-results.json'
    assert not dest.exists()
    dest.write_text(json.dumps(calculate(), indent=2)+'\n')
    print(json.dumps({'exact_examples': 'pass', 'random_draws': 0, 'vendor_execution': False}))
