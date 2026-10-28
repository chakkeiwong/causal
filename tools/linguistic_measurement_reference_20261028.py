"""Exact authored stochastic-proxy witness; no external package or bank data."""
from fractions import Fraction as F


def calculate():
    delta, error = [F(20), F(-10)], [F(9, 20), F(0)]
    cells = []
    for s in range(2):
        for real in range(2):
            for proxy in range(2):
                prob = F(1, 4) * (1 - error[s] if real == proxy else error[s])
                cells.append((s, real, proxy, prob, 100 + delta[s] * real))
    assert sum(x[3] for x in cells) == 1
    accuracy = sum(p for _, r, t, p, _ in cells if r == t)
    contrasts = []
    for s in range(2):
        means = []
        for t in range(2):
            selected = [x for x in cells if x[0] == s and x[2] == t]
            means.append(sum(x[3] * x[4] for x in selected) / sum(x[3] for x in selected))
        contrasts.append(means[1] - means[0])
    algebra = [(1 - 2 * error[s]) * delta[s] for s in range(2)]
    assert contrasts == algebra == [F(2), F(-10)]
    true_effect, proxy_contrast = sum(delta) / 2, sum(contrasts) / 2
    assert (accuracy, true_effect, proxy_contrast) == (F(31, 40), F(5), F(-4))
    return dict(model='Authored randomized latent perception with stochastic symmetric stratum-specific measurement',
                probabilities_sum=str(sum(x[3] for x in cells)),
                stratum_effects_usd=list(map(str, delta)), flip_probabilities=list(map(str, error)),
                accuracy=str(accuracy), proxy_contrasts_usd=list(map(str, contrasts)),
                true_effect_usd=str(true_effect), proxy_contrast_usd=str(proxy_contrast),
                accounts=10000, true_portfolio_effect_usd=str(10000 * true_effect),
                proxy_portfolio_contrast_usd=str(10000 * proxy_contrast),
                enumeration=[dict(stratum=s, perception=r, proxy=t, mass=str(p), outcome_usd=str(y))
                             for s, r, t, p, y in cells],
                native_execution=False, textcause_replication=False, bank_evidence=False)


if __name__ == '__main__':
    import json
    print(json.dumps(calculate(), indent=2))
