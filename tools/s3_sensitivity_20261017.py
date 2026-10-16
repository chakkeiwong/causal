#!/usr/bin/env python3
"""Exact authored full-table IV sensitivity references; no package or bank trial."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

from publish_latent_r_review_v2_20261013 import ref, write

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-17/s3/sensitivity'
TABLE = [F(13, 25), F(9, 50), F(9, 50), F(3, 25),
         F(6, 25), F(3, 50), F(19, 50), F(8, 25)]
OBS = {''.join(map(str, t)): p for t, p in zip(product([0, 1], repeat=3), TABLE)}


def encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {k: encode(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [encode(v) for v in value]
    return value


def model(f, h0, h1, n, b):
    """Product-couple response margins within each receipt principal stratum.

    h0/h1 are defier success masses. n/b are the missing never-Y1 and
    always-Y0 success masses, not conditional means.
    """
    assert 0 <= f <= F(1, 10)
    assert 0 <= h0 <= min(f, F(3, 50)) and 0 <= h1 <= f
    assert 0 <= n <= F(3, 10)-f and 0 <= b <= F(3, 10)-f
    strata = [((0, 0), F(3, 10)-f, F(3, 50)-h0, n),
              ((0, 1), F(2, 5)+f, F(3, 25)+h0, F(1, 5)+h1),
              ((1, 0), f, h0, h1),
              ((1, 1), F(3, 10)-f, b, F(3, 25)-h1)]
    law = {}
    for (d0, d1), mass, s0, s1 in strata:
        assert 0 <= s0 <= mass and 0 <= s1 <= mass
        for y0, y1 in product([0, 1], repeat=2):
            p = ((s0 if y0 else mass-s0)*(s1 if y1 else mass-s1)/mass
                 if mass else F(0))
            law[f'{d0}{d1}{y0}{y1}'] = p
    assert sum(law.values()) == 1 and min(law.values()) >= 0
    observed = {}
    for z, d, y in product([0, 1], repeat=3):
        observed[f'{z}{d}{y}'] = sum(p for k, p in law.items()
                                    if int(k[z]) == d and int(k[2+d]) == y)
    assert observed == OBS
    c_mass = sum(p for k, p in law.items() if k[:2] == '01')
    c_effect = sum(p*(int(k[3])-int(k[2])) for k, p in law.items() if k[:2] == '01')/c_mass
    ate = sum(p*(int(k[3])-int(k[2])) for k, p in law.items())
    assert c_mass == F(2, 5)+f
    assert c_effect == (F(2, 25)+h1-h0)/(F(2, 5)+f)
    assert ate == F(7, 50)+h1-h0+n-b
    return {'f': f, 'h0': h0, 'h1': h1, 'missing_never_Y1_mass': n,
            'missing_always_Y0_mass': b, 'response_type_masses_D0D1Y0Y1': law,
            'observed_DY_given_Z': observed, 'complier_mass': c_mass,
            'complier_effect': c_effect, 'population_ATE': ate}


def calculate():
    # Enumerate vertices of the piecewise polyhedral domain, including both
    # unobserved response margins. Positive C mass makes each fractional
    # extremum attainable at a vertex; manuscript supplies derivative proof.
    vertices = []
    for f in [F(0), F(3, 50), F(1, 10)]:
        for h0, h1, n, b in product(sorted({F(0), min(f, F(3, 50))}),
                                    sorted({F(0), f}),
                                    [F(0), F(3, 10)-f], [F(0), F(3, 10)-f]):
            vertices.append(model(f, h0, h1, n, b))
    c_bounds = [min(r['complier_effect'] for r in vertices), max(r['complier_effect'] for r in vertices)]
    ate_bounds = [min(r['population_ATE'] for r in vertices), max(r['population_ATE'] for r in vertices)]
    assert c_bounds == [F(1, 25), F(9, 25)]
    assert ate_bounds == [F(-4, 25), F(11, 25)]
    endpoints = {
        'monotone_population_lower': model(F(0), F(0), F(0), F(0), F(3, 10)),
        'monotone_population_upper': model(F(0), F(0), F(0), F(3, 10), F(0)),
        'bounded_defier_complier_lower': model(F(1, 10), F(3, 50), F(0), F(0), F(0)),
        'bounded_defier_complier_upper': model(F(1, 10), F(0), F(1, 10), F(0), F(0))}
    direct = []
    for g in [F(1, 50), F(1, 25)]:
        outer = [max(F(-1), (F(2, 25)-g)/F(2, 5)),
                 min(F(1), (F(2, 25)+g)/F(2, 5))]
        direct.append({'Gamma_budget': g, 'complier_effect_outer_envelope': outer,
                       'receipt_net_outer_USD': [100*v-12 for v in outer],
                       'sharp_for_full_table': False})
    result = {
        'kind': 'authored_exact_probability_laws_not_empirical',
        'response_type_order': 'D0,D1,Y0,Y1; exclusion and randomized encouragement',
        'observed_DY_given_Z': OBS, 'vertices': vertices, 'vertex_count': len(vertices),
        'endpoint_models': endpoints,
        'bounded_defier_complier_sharp_range': c_bounds,
        'bounded_defier_complier_net_USD': [100*v-12 for v in c_bounds],
        'population_ATE_sharp_range_both_classes': ate_bounds,
        'population_receipt_net_USD': [100*v-12 for v in ate_bounds],
        'first_stage_and_ITT_only_outer_complier_range': [F(-1, 25), F(9, 25)],
        'exclusion_sensitivity': direct,
        'encouragement': {'receipt_first_stage': F(2, 5), 'outcome_ITT': F(2, 25),
                          'net_before_encouragement_cost_USD': F(16, 5),
                          'encouragement_cost_USD': 2, 'incremental_net_USD': F(6, 5)}}
    return encode(result)


def separate_review(saved):
    """Direct stratum marginal equations, separate from response enumeration."""
    assert saved['observed_DY_given_Z'] == {k: str(v) for k, v in OBS.items()}
    for row in saved['vertices']:
        f, h0, h1, n, b = [F(row[k]) for k in
                           ['f', 'h0', 'h1', 'missing_never_Y1_mass', 'missing_always_Y0_mass']]
        # Eight cells reconstructed without calling model or using its types.
        weights = [F(3, 10)-f, F(2, 5)+f, f, F(3, 10)-f]
        means0 = [F(3, 50)-h0, F(3, 25)+h0, h0, b]
        means1 = [n, F(1, 5)+h1, h1, F(3, 25)-h1]
        for z in [0, 1]:
            zero = [0, 1] if z == 0 else [0, 2]
            one = [2, 3] if z == 0 else [1, 3]
            s0, m0 = sum(means0[i] for i in zero), sum(weights[i] for i in zero)
            s1, m1 = sum(means1[i] for i in one), sum(weights[i] for i in one)
            assert [m0-s0, s0, m1-s1, s1] == TABLE[z*4:z*4+4]
        # Analytic envelope inequalities for each piecewise vertex.
        c = (F(2, 25)+h1-h0)/(F(2, 5)+f)
        assert F(1, 25) <= c <= F(9, 25)
        assert F(-4, 25) <= F(7, 50)+h1-h0+n-b <= F(11, 25)
    assert F(saved['endpoint_models']['bounded_defier_complier_lower']['complier_effect']) == F(1, 25)
    assert F(saved['endpoint_models']['bounded_defier_complier_upper']['complier_effect']) == F(9, 25)
    assert 100*F(2, 25)-12*F(2, 5)-2 == F(6, 5)
    return {'status': 'pass', 'method': 'Separate author marginal mixing and analytic envelope review; not independent acceptance.',
            'checked': ['Nonnegative16-type masses and all eight observable conditional cells',
                        'Piecewise-domain vertices and attainable sharp endpoints',
                        'Complier and population target distinction',
                        'Exclusion outer envelopes and randomized encouragement value'],
            'evidence': [ref(BASE/'exact-results.json', 'Exact rational constructions'),
                         ref(Path(__file__), 'Separate marginal recomputation and reference code')],
            'limitations': ['Sensitivity budgets are stipulated, not learned from the observed law.',
                            'Exclusion envelopes are outer, not asserted sharp for the complete table.',
                            'No upstream execution, sampling calibration, bank truth or ROI result.']}


if __name__ == '__main__':
    BASE.mkdir(exist_ok=False)
    saved = calculate()
    write(BASE/'exact-results.json', saved)
    write(BASE/'mathematics-review.json', separate_review(saved))
    print(json.dumps({k: saved[k] for k in ['vertex_count', 'bounded_defier_complier_sharp_range',
                                          'population_ATE_sharp_range_both_classes', 'encouragement']}))
