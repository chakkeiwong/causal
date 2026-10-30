"""Exact authored witnesses for source contracts; never executes vendor code."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/release/2026-10-29/source-delegates-015'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def orientation():
    # The two-point, unit-cost hard-margin optimum has dual weights 1/2.
    # We stipulate that optimum, then reconstruct the inspected label transport
    # and DTRlearn2 coefficient/bias algebra. This is not a solver run.
    records = []
    for rows in [[-1, 1], [1, -1]]:
        y = list(map(F, rows))
        x = y[:]
        first_class = y[0]
        internal_labels = [first_class * v for v in y]
        dual = [F(1, 2)] * 2
        coefficients = [a * label for a, label in zip(dual, internal_labels)]
        weight = sum(v * c for v, c in zip(x, coefficients))
        assert sum(coefficients) == 0 and abs(weight) == 1
        assert all(label * weight * value == 1 for label, value in zip(internal_labels, x))
        # These satisfy the exact dual/primal stationary equations and margins.
        reconstructed_dual = [c / label for c, label in zip(coefficients, y)]
        fitted = [weight * value for value in x]
        residual = [label - value for label, value in zip(y, fitted)]
        middle = [i for i, a in enumerate(reconstructed_dual) if 0 < a < 1]
        if middle:
            bias = sum(residual[i] for i in middle) / len(middle)
        else:
            up = [residual[i] for i, a in enumerate(reconstructed_dual) if (a < 0 and y[i] == -1) or (a > 1 and y[i] == 1)]
            low = [residual[i] for i, a in enumerate(reconstructed_dual) if (a < 0 and y[i] == 1) or (a > 1 and y[i] == -1)]
            bias = (min(up) + max(low)) / 2
        predictions = [1 if value + bias > 0 else -1 for value in fitted]
        assert predictions == ([int(-v) for v in y] if first_class == -1 else rows)
        records.append(dict(rows=rows, factor_codes=[1 if v == -1 else 2 for v in y],
                            native_positive_class=str(first_class),
                            stipulated_coefficients=list(map(str, coefficients)),
                            reconstructed_weight=str(weight), reconstructed_bias=str(bias),
                            predictions=predictions, matches_original_labels=predictions == rows))
    return records


def clustering():
    a = (F(9, 10), F(1, 10))
    b = (F(3, 5), F(3, 5))
    correct = [a[0] * a[1], b[0] * b[1]]
    stationary = [a[0] ** 2, b[0] ** 2]
    posterior = lambda v: [x / sum(v) for x in v]
    assert posterior(correct) == [F(1, 5), F(4, 5)]
    assert posterior(stationary) == [F(9, 13), F(4, 13)]
    prior = [F(9, 10), F(1, 10)]
    likelihood = [F(2, 5), F(4, 5)]
    weighted = [a * b for a, b in zip(prior, likelihood)]
    assert likelihood.index(max(likelihood)) == 1 and weighted.index(max(weighted)) == 0
    return dict(transition_likelihoods=[list(map(str, a)), list(map(str, b))],
                correct_posterior=list(map(str, posterior(correct))),
                stationary_posterior=list(map(str, posterior(stationary))),
                prior=list(map(str, prior)), likelihood=list(map(str, likelihood)),
                mixture_products=list(map(str, weighted)),
                likelihood_only_choice=1, prior_weighted_choice=0)


def main():
    files = sorted((ROOT / 'docs/literature/raw').glob('rel15_*.txt'))
    result = dict(status='pass', scope='Exact project-authored finite witnesses for inspected source contracts. No installed R/Java execution, stochastic convergence, runtime qualification or bank evidence.',
                  orientation=orientation(), clustering=clustering(),
                  bindings={str(p.relative_to(ROOT)): sha(p) for p in files},
                  verifier_sha256=sha(Path(__file__)))
    output = OUT / 'exact-witnesses.json'
    assert not output.exists(), 'Do not overwrite frozen witness evidence'
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
