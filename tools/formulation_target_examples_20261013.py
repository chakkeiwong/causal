#!/usr/bin/env python3
"""Exact target-change example; no fitted estimator or model performance claim."""
from fractions import Fraction as F
import json
from pathlib import Path


def calculate():
    population = [F(1, 2), F(3, 10), F(1, 5)]
    propensity = [F(1, 20), F(1, 2), F(4, 5)]
    effects = [F(0), F(2), F(8)]
    keep = [F(1, 10) <= e <= F(9, 10) for e in propensity]

    def average(weights):
        mass = sum(p * w for p, w in zip(population, weights))
        return sum(p * w * tau for p, w, tau in zip(population, weights, effects)) / mass

    ate = average([F(1)] * 3)
    trimmed = average(keep)
    ato = average([e * (1 - e) for e in propensity])
    att = average(propensity)
    assert (ate, trimmed, ato, att) == (F(11, 5), F(22, 5), F(1624, 523), F(316, 67))
    return {'evidence_kind': 'exact_project_calculation', 'runtime_model_or_package_run': False,
            'law': {'strata': [0, 1, 2], 'population_mass': list(map(float, population)),
                    'propensity': list(map(float, propensity)), 'conditional_effect': list(map(float, effects)),
                    'intervention': 'binary invitation, 1 versus 0', 'units': 'thousand_currency_units',
                    'scope': 'Known generated population law; true propensities, not fitted scores'},
            'targets': {k: {'fraction': str(v), 'value': float(v)} for k, v in
                        [('ATE', ate), ('trimmed_ATE', trimmed), ('overlap_weighted_ATO', ato), ('ATT', att)]},
            'trimming': {'bounds': [0.1, 0.9], 'retained_strata': [1, 2], 'retained_population_mass': 0.5},
            'interpretation': 'Changing eligibility or weights changes the target. These differences are not estimator errors.',
            'limitations': ['No bank data or live model score', 'Estimated trimming introduces additional randomness and an explicit learned selection rule']}


if __name__ == '__main__':
    out = Path(__file__).resolve().parents[1] / 'docs/program/execution/2026-10-13/formulation-targets.json'
    value = calculate()
    out.write_text(json.dumps(value, indent=2) + '\n')
    print(json.dumps(value['targets'], indent=2))
