#!/usr/bin/env python3
"""Independent exact checks for authored graphical and branch-rollout laws."""
from fractions import Fraction as F
import json

import review_commercial_panels_20261018 as panels
import review_dagitty_reuse_20261018 as graphs


def solve(matrix, rhs):
    """Rational Gaussian elimination, separate from the saved FWL calculation."""
    n = len(rhs)
    a = [list(map(F, row)) + [F(value)] for row, value in zip(matrix, rhs)]
    for j in range(n):
        pivot = next(i for i in range(j, n) if a[i][j])
        a[j], a[pivot] = a[pivot], a[j]
        scale = a[j][j]
        a[j] = [v / scale for v in a[j]]
        for i in range(n):
            if i != j:
                scale = a[i][j]
                a[i] = [u - scale * v for u, v in zip(a[i], a[j])]
    return [row[-1] for row in a]


def calculate():
    graph = graphs.reference()
    panel = panels.exact_reference()
    units = ['E1', 'E2', 'L1', 'L2', 'N']
    x, y = [], []
    for i, unit in enumerate(units):
        for t in range(3):
            d = int((unit.startswith('E') and t >= 1) or
                    (unit.startswith('L') and t >= 2))
            effect = 100 if unit.startswith('E') and t == 2 else d
            x.append(list(map(F, [1] + [int(i == j) for j in range(1, 5)] +
                              [int(t == j) for j in (1, 2)] + [d])))
            y.append(F(10*i + 2*t + effect))
    n = len(x[0])
    gram = [[sum(row[j]*row[k] for row in x) for k in range(n)] for j in range(n)]
    rhs = [sum(row[j]*v for row, v in zip(x, y)) for j in range(n)]
    coefficients = solve(gram, rhs)
    assert coefficients[-1] == F(-91, 8)
    residuals = [v - sum(c*r for c, r in zip(coefficients, row)) for row, v in zip(x, y)]
    assert all(sum(row[j]*r for row, r in zip(x, residuals)) == 0 for j in range(n))
    assert panel['TWFE_projection_coefficient']['fraction'] == str(coefficients[-1])
    assert panel['treated_branch_period_ATT']['fraction'] == '34'
    # Recover the treatment weights from the least-squares linear functional.
    # The treatment row of inverse(X'X) is obtained by solving against e_last.
    dual = solve(gram, [int(j == n-1) for j in range(n)])
    observation_weights = [sum(c*r for c, r in zip(dual, row)) for row in x]
    grouped = {}
    for group, t in [('E', 1), ('E', 2), ('L', 2)]:
        grouped[group+str(t)] = sum(observation_weights[i*3+t]
                                   for i, unit in enumerate(units) if unit.startswith(group))
    assert grouped == {'E1': F(5, 8), 'E2': F(-1, 8), 'L2': F(1, 2)}
    assert grouped == {k: F(v['fraction']) for k, v in panel['TWFE_effect_weights'].items()}
    # Direct structural-law calculations, independent of enumerated joint tables.
    adjusted = [sum(F(1, 2)*F(1+2*a+z, 8) for z in (0, 1)) for a in (0, 1)]
    assert list(map(str, adjusted)) == graph['confounding']['risks_adjusting_Z']
    assert adjusted[1] - adjusted[0] == F(1, 4)
    naive = []
    for a in (0, 1):
        p = [F(1, 2)*(F(1+2*z, 4) if a else 1-F(1+2*z, 4)) for z in (0, 1)]
        naive.append(sum(p[z]*F(1+2*a+z, 8) for z in (0, 1))/sum(p))
    assert naive[1]-naive[0] == F(5, 16)
    collider_contrasts, collider_masses = [], []
    for c in (0, 1):
        risks, masses = [], []
        for a in (0, 1):
            weights = [F(1, 2)*(F(1+2*a+2*u, 8) if c else
                               1-F(1+2*a+2*u, 8)) for u in (0, 1)]
            masses.append(sum(weights))
            risks.append(weights[1]/sum(weights))
        collider_contrasts.append(risks[1]-risks[0])
        collider_masses.append(sum(masses)/2)
    assert list(map(str, collider_contrasts)) == graph['collider']['differences_conditioning_C']
    collider_standardized = sum(p*d for p, d in zip(collider_masses, collider_contrasts))
    assert str(collider_standardized) == graph['collider']['standardized_difference'] == '-7/96'
    mediator_risks = []
    for a in (0, 1):
        pm = F(1+2*a, 4)
        mediator_risks.append((1-pm)*F(1+a, 8)+pm*F(3+a, 8))
    assert str(mediator_risks[1]-mediator_risks[0]) == graph['mediator']['total_effect'] == '1/4'
    mediator_fixed = sum(F(1, 2)*(F(2+2*m, 8)-F(1+2*m, 8)) for m in (0, 1))
    assert str(mediator_fixed) == graph['mediator']['difference_standardized_over_marginal_M'] == '1/8'
    assert graph == graphs.read(graphs.BASE/'exact-reference.json')
    assert panel == panels.read(panels.BASE/'exact-reference.json')
    assert F(34000)-10000 == panel['stipulated_net_value']['true_average_net_USD']
    assert 1000*coefficients[-1]-10000 == panel['stipulated_net_value']['invalid_projection_as_value_USD']
    return dict(status='pass', graph=graph, panel=panel,
        independent_checks=dict(panel_method='Rational normal equations and inverse-Gram treatment functional',
            panel_coefficients=list(map(str, coefficients)),
            treatment_weights={k: str(v) for k, v in grouped.items()},
            all_normal_equations_zero=True,
            graph_method='Direct structural conditioning and marginalization, separate from saved joint-table enumeration',
            collider_contrasts=list(map(str, collider_contrasts)),
            collider_masses=list(map(str, collider_masses)),
            collider_standardized=str(collider_standardized),
            mediator_risks=list(map(str, mediator_risks)),
            mediator_fixed_marginal_contrast=str(mediator_fixed)),
        vendor_or_upstream_execution=False, sampling_coverage_claim=False,
        bank_evidence=False, prices='Stipulated example only')


if __name__ == '__main__':
    print(json.dumps(calculate(), indent=2))
