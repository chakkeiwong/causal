#!/usr/bin/env python3
"""Exact proposal examples; no vendor engine, fitted data or final study."""
import argparse
from fractions import Fraction as F
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / 'docs/program/execution/2026-10-13/commercial-latent/exact-results.json'


def calculate():
    rho = F(3, 5)
    direct_covariance = [[F(1), rho], [rho, rho * rho + F(16, 25)]]
    hidden_covariance = [[rho + F(2, 5), rho], [rho, rho + F(2, 5)]]
    assert direct_covariance == hidden_covariance == [[F(1), rho], [rho, F(1)]]
    # Direct world: A=eA; Y=.6 A+eY. Hidden world: A=U+eA; Y=U+eY.
    effects = {'direct': rho, 'hidden': F(0)}
    monetary = {k: v * F(1, 4) * 1000 for k, v in effects.items()}
    assert monetary == {'direct': F(150), 'hidden': F(0)}

    proxy_cases = []
    # Independent U,eA,eY with unit variances; W=U+eW; Var(eW)=s.
    for s in [F(4), F(1), F(1, 4), F(0)]:
        cov_cond = F(1) - F(1) / (1 + s)
        var_cond = F(2) - F(1) / (1 + s)
        slope = cov_cond / var_cond
        v = s / (1 + s)
        assert slope == v / (1 + v)
        proxy_cases.append({'proxy_noise_variance': s, 'risk_variance_given_proxy': v,
                            'adjusted_association': slope, 'true_effect': F(0)})
    assert proxy_cases[1]['adjusted_association'] == F(1, 3)

    compliance = F(2, 5)
    tau = F(3)
    trials = []
    for direct_offer_effect in [F(0), F(1, 5)]:
        rows = []
        for c in (0, 1):
            for z in (0, 1):
                mass = (compliance if c else 1 - compliance) * F(1, 2)
                d = z * c
                y = 2 + c + tau * d + direct_offer_effect * z
                rows.append({'C': c, 'Z': z, 'D': d, 'Y': y, 'mass': mass})
        assert sum(r['mass'] for r in rows) == 1
        def conditional(field, z):
            return sum(r['mass'] * r[field] for r in rows if r['Z'] == z) / F(1, 2)
        first_stage = conditional('D', 1) - conditional('D', 0)
        itt = conditional('Y', 1) - conditional('Y', 0)
        ratio = itt / first_stage
        assert first_stage == compliance and ratio == tau + direct_offer_effect / compliance
        trials.append({'direct_offer_effect': direct_offer_effect, 'law': rows,
                       'first_stage': first_stage, 'ITT': itt, 'Wald_ratio': ratio,
                       'receipt_effect_for_compliers': tau,
                       'exclusion_holds': direct_offer_effect == 0})
    assert trials[0]['Wald_ratio'] == 3 and trials[1]['Wald_ratio'] == F(7, 2)
    small_probability = 1 / (1 + math.exp(15))
    assert 0 < small_probability < 1e-6
    return {'kind': 'project_derivations_and_deterministic_arithmetic',
            'random_draws': 0, 'commercial_engine_executed': False,
            'gaussian_worlds': {'common_covariance': direct_covariance,
                               'do_effect_Y_per_A': effects,
                               'declared_scale': 'One A unit is1 percentage point; one centered Y unit is1000 currency units.',
                               'change_for_25_basis_points_currency': monetary},
            'proxy_adjustment': {'unadjusted_association': F(1, 2), 'cases': proxy_cases},
            'randomized_offer': {'cases': trials, 'claim': 'Exact finite law, not Mplus output or an empirical trial.'},
            'logit_threshold_15': {'probability': small_probability,
                                  'complement': 1 - small_probability,
                                  'exact_structural_zero': False},
            'limits': ['Stipulated proposal examples, not bank estimates.',
                       'No fitted latent structure, vendor parity, confidence coverage or statistical final study.']}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path, default=DEFAULT)
    args = p.parse_args()
    value = calculate()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.output.exists():
        raise ValueError('Preserve earlier evidence; use a fresh output path')
    args.output.write_text(json.dumps(value, indent=2, default=lambda x: str(x) if isinstance(x, F) else x) + '\n')
    print(json.dumps({'status': 'pass', 'example_groups': 4, 'random_draws': 0, 'output': str(args.output)}))


if __name__ == '__main__':
    main()
