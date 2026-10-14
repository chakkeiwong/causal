#!/usr/bin/env python3
"""Exact generated reference examples; no fitted model or bank observation."""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/program/execution/2026-10-13/llm-census/exact-examples.json'


def number(x):
    return {'exact': str(x), 'decimal': float(x)}


def main():
    tau = F(-1, 5)
    rows = []
    for noise in [F(0), F(1, 4), F(1), F(4)]:
        # Independent centered Gaussian U, e_A, e_Y have variance one;
        # e_W has variance noise. A=U+e_A; W=U+e_W; Y=tau*A+U+e_Y.
        va, vw, caw = F(2), 1 + noise, F(1)
        cay, cwy = 2 * tau + 1, tau + 1
        denominator = va * vw - caw * caw
        assert denominator > 0
        beta_covariance = (cay * vw - cwy * caw) / denominator
        residual_variance = noise / (1 + noise)
        beta_residual = tau + residual_variance / (1 + residual_variance)
        formula = tau + noise / (1 + 2 * noise)
        assert beta_covariance == beta_residual == formula
        rows.append({'text_noise_variance': number(noise), 'true_effect': number(tau),
                     'adjusted_population_coefficient': number(formula),
                     'bias': number(formula - tau),
                     'checks': ['covariance normal equation', 'residual variance decomposition', 'closed form']})
    mixtures = []
    for q in [F(0), F(1, 2), F(1)]:
        response = (1 - q) * F(1, 5) + q * F(4, 5)
        effect = response - F(1, 10)
        assert effect == F(1, 10) + F(3, 5) * q
        mixtures.append({'probability_of_second_message': number(q),
                         'response_probability': number(response), 'effect_vs_reference': number(effect)})
    out = {'kind': 'project_generated_exact_reference_examples', 'status': 'pass',
           'scope': 'Exact rational population calculations under stated illustrative laws. No public empirical fit, LLM call, causal package execution or bank calibration.',
           'script': {'path': str(Path(__file__).relative_to(ROOT)), 'sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
           'measurement_error': rows,
           'no_information_limit': number(tau + F(1, 2)),
           'text_versions': {'assumptions': 'Two messages share one style label but have stipulated response probabilities 1/5 and 4/5; reference is 1/10. The policy must specify their mixture.', 'rows': mixtures},
           'repeated_call_design': {'mechanisms': 100, 'calls_each': 5, 'within_mechanism_correlation': 1,
                                    'design_effect': 5, 'effective_independent_units': 100},
           'paper_table_arithmetic': {'DDI_F1_gain_points': number(F('87.9') - F('67.4')),
                                      'ORCA_rounded_completion_gain_points': number(100 * (F('.83') - F('.75'))),
                                      'ORCA_rounded_reported_CI_metric_gain_points': number(100 * (F('.50') - F('.083'))),
                                      'CausalSmith_catalog_acceptance_fraction': number(F(14, 144))}}
    OUT.write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps({'status': 'pass', 'measurement_regimes': len(rows), 'text_policies': len(mixtures), 'empirical_study': False}))


if __name__ == '__main__':
    main()
