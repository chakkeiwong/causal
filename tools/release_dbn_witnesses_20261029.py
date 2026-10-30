"""Exact authored temporal-contract laws; never import or run upstream code."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/release/2026-10-29/source-dbn-019/exact-witnesses.json'


def compute():
    prior = [F(3, 4), F(1, 4)]
    likelihood = [F(1, 5), F(4, 5)]
    kernels = {
        'A': [[F(9, 10), F(1, 10)], [F(1, 5), F(4, 5)]],
        'B': [[F(3, 5), F(2, 5)], [F(1, 10), F(9, 10)]],
    }
    outcomes = {}
    for name, kernel in kernels.items():
        assert all(sum(row) == 1 for row in kernel)
        # Enumerate every latent transition and observed flag contribution.
        masses = [sum(prior[i] * kernel[i][j] * likelihood[j]
                      for i in range(2)) for j in range(2)]
        posterior = masses[1] / sum(masses)
        outcomes[name] = dict(
            forecast=str(sum(prior[i] * kernel[i][1] for i in range(2))),
            flag_probability=str(sum(masses)), posterior=str(posterior),
            stipulated_action_net=str(14 * posterior - 10))
    assert outcomes['A']['posterior'] == '44/73'
    assert outcomes['B']['posterior'] == '84/103'
    assert outcomes['A']['stipulated_action_net'] == '-114/73'
    assert outcomes['B']['stipulated_action_net'] == '146/103'
    # Randomized assignment, equally likely response types, deterministic
    # outcome-dependent cleaning. Each joint state has probability 1/4.
    records = []
    for u, a in product(range(2), repeat=2):
        y = 100 + 100 * u * a
        records.append(dict(type=u, action=a, y=y, retained=y <= 150,
                            probability='1/4'))
    means = {}
    for a in range(2):
        rows = [r for r in records if r['action'] == a and r['retained']]
        means[a] = sum(F(r['probability']) * r['y'] for r in rows) / sum(
            F(r['probability']) for r in rows)
    effect = F(1, 2) * (100 - 100) + F(1, 2) * (200 - 100)
    selected = means[1] - means[0]
    assert (effect, selected, effect - 20, selected - 20) == (50, 0, 30, -20)
    return dict(status='pass', provenance='Project-authored exact laws; no upstream execution or bank measurements.',
                transition=dict(prior=list(map(str, prior)),
                                likelihood=list(map(str, likelihood)),
                                kernels={k: [list(map(str, r)) for r in v] for k, v in kernels.items()},
                                outcomes=outcomes,
                                scope='Quantifies substituting kernel A for intended B with identical variable identities; does not predict every pointer-lifetime or concurrency outcome.'),
                cleaning=dict(records=records, population_effect=str(effect),
                              retained_contrast=str(selected), cost='20',
                              population_net=str(effect-20), retained_net=str(selected-20),
                              scope='Correct, treatment-responsive outcomes deliberately flagged; missingness is created by cleaning. No claim that every filter or threshold produces this example.'),
                ternary=dict(probabilities=['1/5', '3/10', '1/2'],
                             boolean_images=[0, 1, 1], pushed_mass=['1/5', '4/5'],
                             scope='Noninjective Boolean-literal encoding; no predicted CUDD return for invalid nonbinary inputs.'),
                dummy=dict(sequence_count=40000, positive_iterations=10,
                           per_sequence_return=1, inferred_last_iteration_sum=40000,
                           scope='Source-path arithmetic if the shown loops complete; no timing, fitted likelihood or native-execution result.'))


if __name__ == '__main__':
    assert not OUT.exists(), 'Preserve the original witness; use compute for later checks.'
    result = compute()
    OUT.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))
