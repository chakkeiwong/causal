"""Independent finite witnesses; never imports or executes acquired source."""
from collections import Counter
from fractions import Fraction


def calculate():
    x = (0, 0, 1, 1)
    z = x
    shuffled = (1, 1, 0, 0)
    alternating = (0, 1, 0, 1)
    assert Counter(x) == Counter(shuffled) == Counter(alternating)
    mean = lambda a: sum(map(Fraction, a)) / len(a)
    covariance = lambda a, b: mean([u*v for u, v in zip(a, b)]) - mean(a)*mean(b)
    loss = lambda a, b: mean([(u-v)**2 for u, v in zip(a, b)])
    agreement = lambda a: Fraction(sum(a[i] == a[i-1] for i in range(1, len(a))), len(a)-1)
    assert covariance(x, z) == Fraction(1, 4)
    assert covariance(shuffled, z) == Fraction(-1, 4)
    assert loss(x, z) == 0 and loss(shuffled, z) == 1
    assert agreement(x) == Fraction(2, 3) and agreement(alternating) == 0
    # U is a fair exogenous binary variable: X=U, Z=U. do(X) leaves Z=U.
    effect = mean(z) - mean(z)
    assert effect == 0
    return dict(
        status='pass', evidence_type='authored exact finite witness',
        original=list(x), unchanged_target=list(z), shuffled=list(shuffled),
        marginal_multiset_preserved=True, joint_distribution_preserved=False,
        covariance_before=str(covariance(x, z)), covariance_after=str(covariance(shuffled, z)),
        fitted_predictor='f(X)=X; no refit', loss_before=str(loss(x,z)), loss_after=str(loss(shuffled,z)),
        confounded_structural_example='X=U,Z=U; U fair Bernoulli; no X-to-Z structural edge',
        intervention_effect=str(effect), alternating=list(alternating),
        adjacent_agreement_before=str(agreement(x)), adjacent_agreement_after=str(agreement(alternating)),
        limitation='A witness against universal distribution preservation and causal interpretation; not an empirical failure rate or reproduction of a selected paper.')


if __name__ == '__main__':
    import json
    print(json.dumps(calculate(), indent=2))
