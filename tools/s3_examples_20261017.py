#!/usr/bin/env python3
"""Exact authored laws for S3; no external causal engine or bank observations."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-17/s3'


def bitlaw(p):
    return [(0, 1-p), (1, p)]


def net(effect):
    return 100*effect-12


def encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {k: encode(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [encode(v) for v in value]
    return value


def calculate():
    adjustment = []
    for c in [0, 1]:
        for a, pa in bitlaw([F(1, 5), F(4, 5)][c]):
            py = [F(1, 10), F(3, 5)][c]+F(a, 10)
            for y, qy in bitlaw(py):
                adjustment.append({'C': c, 'A': a, 'Y': y, 'p': F(1, 2)*pa*qy})
    raw = [sum(r['p']*r['Y'] for r in adjustment if r['A'] == a) /
           sum(r['p'] for r in adjustment if r['A'] == a) for a in [0, 1]]
    adjusted = [sum(F(1, 2)*([F(1, 10), F(3, 5)][c]+F(a, 10))
                    for c in [0, 1]) for a in [0, 1]]
    observed = {(a, y): sum(r['p'] for r in adjustment if (r['A'], r['Y']) == (a, y))
                for a, y in product([0, 1], repeat=2)}
    # Enumerate full exogenous laws. A fair U remains random after intervening.
    conditional = []
    for world in [0, 1]:
        laws = {}
        for action in [None, 0, 1]:
            rows = []
            for u, pu in bitlaw(F(1, 2)):
                a = u if action is None else action
                for e, pe in bitlaw(F(1, 4)):
                    z = (u if world == 0 else a) ^ e
                    for y, py in bitlaw(F(1, 5)+F(3, 5)*z):
                        rows.append({'A': a, 'Z': z, 'Y': y, 'p': pu*pe*py})
            law = {}
            for a, z, y in product([0, 1], repeat=3):
                p = sum(r['p'] for r in rows if (r['A'], r['Z'], r['Y']) == (a, z, y))
                if p:
                    law[f'{a}{z}{y}'] = p
            laws['observed' if action is None else f'do_A_{action}'] = law
        means, conditional_means = [], []
        for a in [0, 1]:
            law = laws[f'do_A_{a}']
            means.append(sum(p for key, p in law.items() if key[2] == '1'))
            conditional_means.append([
                sum(p for key, p in law.items() if key[1:] == f'{z}1') /
                sum(p for key, p in law.items() if key[1] == str(z)) for z in [0, 1]])
        conditional.append({'world': world, 'laws': laws, 'Y_means_do_A': means,
                            'effect': means[1]-means[0], 'conditional_Y_given_Z': conditional_means})
    assert conditional[0]['laws']['observed'] == conditional[1]['laws']['observed']
    assert min(conditional[0]['laws']['observed'].values()) > 0
    coupling = []
    for t in [F(0), F(1, 5), F(2, 5)]:
        law = {'00': t, '01': F(3, 5)-t, '10': F(2, 5)-t, '11': t}
        assert sum(law.values()) == 1 and min(law.values()) >= 0
        coupling.append({'t': t, 'response_type_law': law,
                         'ATE': law['01']-law['10'],
                         'benefit': law['01'], 'harm': law['10'],
                         'attribution_given_treated_success': law['01']/F(3, 5)})
    iv = []
    for missing_never_y1, missing_always_y0 in product([F(0), F(1)], repeat=2):
        rows = []
        for name, mass, d0, d1, p0, p1 in [
            ('never', F(3, 10), 0, 0, F(1, 5), missing_never_y1),
            ('complier', F(2, 5), 0, 1, F(3, 10), F(1, 2)),
            ('always', F(3, 10), 1, 1, missing_always_y0, F(2, 5))]:
            for y0, py0 in bitlaw(p0):
                for y1, py1 in bitlaw(p1):
                    for z, pz in bitlaw(F(1, 2)):
                        d = [d0, d1][z]
                        rows.append({'stratum': name, 'Z': z, 'D': d, 'Y': [y0, y1][d],
                                     'Y0': y0, 'Y1': y1, 'p': mass*py0*py1*pz})
        observable = {f'{z}{d}{y}': sum(r['p'] for r in rows if (r['Z'], r['D'], r['Y']) == (z, d, y))
                      for z, d, y in product([0, 1], repeat=3)}
        dmeans = [2*sum(r['p']*r['D'] for r in rows if r['Z'] == z) for z in [0, 1]]
        ymeans = [2*sum(r['p']*r['Y'] for r in rows if r['Z'] == z) for z in [0, 1]]
        ate = sum(r['p']*(r['Y1']-r['Y0']) for r in rows)
        iv.append({'missing_never_Y1': missing_never_y1, 'missing_always_Y0': missing_always_y0,
                   'observable_ZDY': observable, 'receipt_means': dmeans, 'outcome_means': ymeans,
                   'first_stage': dmeans[1]-dmeans[0], 'ITT': ymeans[1]-ymeans[0],
                   'LATE': (ymeans[1]-ymeans[0])/(dmeans[1]-dmeans[0]),
                   'population_ATE': ate, 'universal_receipt_net_USD': net(ate)})
    assert all(r['observable_ZDY'] == iv[0]['observable_ZDY'] for r in iv)
    completions = []
    cells = list(observed)
    for missing in product([0, 1], repeat=4):
        ey = [F(0), F(0)]
        for (a, y), other in zip(cells, missing):
            pair = [None, None]; pair[a] = y; pair[1-a] = other
            for action in [0, 1]:
                ey[action] += observed[(a, y)]*pair[action]
        completions.append({'missing_responses': list(missing), 'EY0': ey[0], 'EY1': ey[1],
                            'ATE': ey[1]-ey[0]})
    bounds = [min(r['ATE'] for r in completions), max(r['ATE'] for r in completions)]
    def envelope(d):
        n, eps = F(3, 5)*d, F(1, 10000000)
        q = [(n-eps)/(d+eps), (n+eps)/(d-eps)]
        return {'denominator': d, 'numerator': n, 'certified_absolute_error': eps,
                'ratio_interval': q, 'incremental_net_USD': [net(v-F(2, 5)) for v in q]}
    return encode({
        'status': 'exact_authored_laws_not_empirical_data',
        'prices': {'success_USD': 100, 'receipt_USD': 12},
        'adjustment': {'rows': adjustment, 'raw_means': raw, 'adjusted_means': adjusted,
                       'raw_contrast': raw[1]-raw[0], 'ATE': adjusted[1]-adjusted[0],
                       'raw_net_USD': net(raw[1]-raw[0]), 'causal_net_USD': net(adjusted[1]-adjusted[0]),
                       'linear_mediation': {'M_A_slope': 1, 'Y_A_direct_slope': 2,
                                            'Y_M_slope': 3, 'total_effect': 5, 'controlled_direct_effect': 2}},
        'conditional_identification': conditional,
        'coupling': {'examples': coupling, 'benefit_bounds': [F(1, 5), F(3, 5)],
                     'harm_bounds': [F(0), F(2, 5)], 'attribution_bounds': [F(1, 3), F(1)],
                     'average_net_USD': net(F(1, 5))},
        'iv': {'completions': iv, 'ATE_bounds': [min(r['population_ATE'] for r in iv), max(r['population_ATE'] for r in iv)],
               'receipt_net_bounds_USD': [min(r['universal_receipt_net_USD'] for r in iv), max(r['universal_receipt_net_USD'] for r in iv)],
               'complier_net_USD': net(F(1, 5)), 'encouragement_net_USD': F(2, 5)*net(F(1, 5)),
               'encouragement_net_with_2_USD_direct_cost': F(2, 5)*net(F(1, 5))-2,
               'fixed_denominator_error_examples': [
                   {'first_stage': d, 'numerator_error': F(1, 1000), 'ratio_error': F(1, 1000)/d,
                    'USD_error': 100*F(1, 1000)/d} for d in [F(2, 5), F(1, 50)]]},
        'consistency_bounds': {'observable_AY': {f'{a}{y}': p for (a, y), p in observed.items()},
                               'completions': completions, 'ATE_bounds': bounds,
                               'net_bounds_USD': [net(v) for v in bounds]},
        'numerical': {'rare': envelope(F(1, 1000000)), 'common': envelope(F(1, 10)),
                      'nominal_incremental_net_USD': net(F(1, 5)),
                      'four_decimal_rounded_rare_n_and_d': ['0.0000', '0.0000']}
    })


if __name__ == '__main__':
    result = calculate()
    path = BASE / 'exact-results.json'
    with path.open('x') as stream:
        json.dump(result, stream, indent=2, ensure_ascii=False); stream.write('\n')
    print(json.dumps({'exact_families': 6, 'output': str(path.relative_to(ROOT))}))
