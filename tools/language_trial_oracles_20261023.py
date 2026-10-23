#!/usr/bin/env python3
"""Independent finite design calculations. No native engines or random draws."""
from decimal import Decimal, localcontext
from fractions import Fraction as F
from itertools import combinations, permutations, product
import hashlib
import json


def decimal(value):
    with localcontext() as ctx:
        ctx.prec = 40
        return str(Decimal(value.numerator) / Decimal(value.denominator))


def binomial_cdf(n, p, k):
    a, b = p.numerator, p.denominator
    term = (b-a)**n
    total = term if k >= 0 else 0
    for j in range(k):
        numerator = term*(n-j)*a
        denominator = (j+1)*(b-a)
        assert numerator % denominator == 0
        term = numerator // denominator
        total += term
    return F(total, b**n)


def screen(n, ceiling, alternative):
    a, b = ceiling.numerator, ceiling.denominator
    term = (b-a)**n
    total, k = 0, -1
    for j in range(n+1):
        total += term
        if total*480 > b**n:
            break
        k = j
        term = term*(n-j)*a // ((j+1)*(b-a))
    actual = binomial_cdf(n, ceiling, k)
    next_size = binomial_cdf(n, ceiling, k+1)
    power = binomial_cdf(n, alternative, k)
    assert actual <= F(1, 480) < next_size
    assert power >= F(95, 100)
    return dict(N=n, failure_ceiling=str(ceiling), useful_alternative=str(alternative),
                per_screen_alpha='1/480', pass_if_failures_at_most=k,
                exact_null_tail_decimal=decimal(actual), next_count_tail_decimal=decimal(next_size),
                exact_power_decimal=decimal(power),
                exact_probability_digest=hashlib.sha256(
                    ('|'.join(map(str, [actual, next_size, power]))).encode()).hexdigest())


def transpose(x):
    return [list(r) for r in zip(*x)]


def mul(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def inverse(a):
    n = len(a)
    rows = [[F(v) for v in row]+[F(i == j) for j in range(n)] for i, row in enumerate(a)]
    for j in range(n):
        pivot = next(i for i in range(j, n) if rows[i][j])
        rows[j], rows[pivot] = rows[pivot], rows[j]
        q = rows[j][j]
        rows[j] = [x/q for x in rows[j]]
        for i in range(n):
            if i != j:
                q = rows[i][j]
                rows[i] = [x-q*y for x, y in zip(rows[i], rows[j])]
    return [row[n:] for row in rows]


def transfer(n, edges):
    matrix = [[F(i == j) for j in range(n)] for i in range(n)]
    for i, j, value in edges:
        matrix[j][i] -= value
    return inverse(matrix)


def acyclic(n, edges):
    pending = set(range(n))
    while pending:
        roots = {j for j in pending if not any(a in pending and b == j for a, b in edges)}
        if not roots:
            return False
        pending -= roots
    return True


def colliders(edges):
    adjacent = {frozenset(e) for e in edges}
    answer = set()
    for (a, b), (c, d) in combinations(edges, 2):
        if b == d and a != c and frozenset((a, c)) not in adjacent:
            answer.add((min(a, c), b, max(a, c)))
    return answer


def gaussian_class(kind):
    n = 4
    generating = ([(0, 1, F(3, 5)), (1, 2, F(4, 5))] if kind == 'chain'
                  else [(0, 1, F(3, 5)), (2, 1, F(4, 5))])
    t = transfer(n, generating)
    covariance = mul(t, transpose(t))
    original = [(a, b) for a, b, _ in generating]
    skeleton = sorted(tuple(sorted(e)) for e in original)
    models = []
    for choices in product([False, True], repeat=len(skeleton)):
        edges = [(b, a) if reverse else (a, b) for (a, b), reverse in zip(skeleton, choices)]
        if not acyclic(n, edges) or colliders(edges) != colliders(original):
            continue
        fitted, variances = [], []
        for j in range(n):
            parents = [a for a, b in edges if b == j]
            beta = (mul(inverse([[covariance[a][b] for b in parents] for a in parents]),
                        [[covariance[a][j]] for a in parents]) if parents else [])
            fitted.extend((a, j, beta[i][0]) for i, a in enumerate(parents))
            variances.append(covariance[j][j]-sum(beta[i][0]*covariance[a][j] for i, a in enumerate(parents)))
        f = transfer(n, fitted)
        noise = [[variances[i] if i == j else F(0) for j in range(n)] for i in range(n)]
        assert mul(mul(f, noise), transpose(f)) == covariance
        models.append(dict(edges=edges, coefficients=fitted, noise_variances=variances,
                           effect_X0_on_X2=f[2][0]))
    assert len(models) == (3 if kind == 'chain' else 1)
    if kind == 'chain':
        assert sorted(m['effect_X0_on_X2'] for m in models) == [F(0), F(0), F(12, 25)]
    # Every relabeling keeps a bijective coordinate map, including the isolated node.
    permutations_ = [list(p) for p in permutations(range(n))]
    cpdag = []
    for a, b in skeleton:
        if all((a, b) in m['edges'] for m in models):
            marks = ['tail', 'arrow']
        elif all((b, a) in m['edges'] for m in models):
            marks = ['arrow', 'tail']
        else:
            marks = ['tail', 'tail']
        cpdag.append(dict(nodes=[a, b], endpoints=marks))
    return dict(nodes=list(range(n)), covariance=covariance, models=models,
                population_cpdag=cpdag, node_permutations=permutations_)


def bernoulli(p, x):
    return p if x else 1-p


def finite_functions():
    tables = []
    for pu, pa, pm, base, slope in product(
        [F(1, 3), F(1, 2), F(2, 3)],
        [(F(1, 5), F(4, 5)), (F(2, 5), F(3, 5))],
        [(F(1, 4), F(3, 4)), (F(1, 10), F(9, 10))],
        [F(1, 10), F(1, 5)], [F(2, 5), F(1, 2)]):
        law = {(a, m, y): F(0) for a, m, y in product(range(2), repeat=3)}
        for u, a, m, y in product(range(2), repeat=4):
            law[a, m, y] += bernoulli(pu, u)*bernoulli(pa[u], a)*bernoulli(pm[a], m)*bernoulli(base+slope*m+F(1, 5)*u, y)
        assert sum(law.values()) == 1 and min(law.values()) > 0
        def mass(a=None, m=None, y=None):
            return sum(v for (aa, mm, yy), v in law.items()
                       if (a is None or a == aa) and (m is None or m == mm) and (y is None or y == yy))
        functionals = [sum(mass(a=a, m=m)/mass(a=a)*sum(
            mass(a=aa, m=m, y=1)/mass(a=aa, m=m)*mass(a=aa) for aa in range(2)) for m in range(2)) for a in range(2)]
        do_law = [sum(bernoulli(pu, u)*bernoulli(pm[a], m)*(base+slope*m+F(1, 5)*u)
                      for u, m in product(range(2), repeat=2)) for a in range(2)]
        assert functionals == do_law
        tables.append(dict(family='frontdoor', parameters=[pu, pa, pm, base, slope],
            observed={','.join(map(str, k)): v for k, v in law.items()},
            do_means=do_law, independent_functional=functionals))
    assert len(tables) == 48
    for family, slope in [('backdoor', F(2, 5)), ('no_treatment_effect', F(0))]:
        for pu, pa, base in product([F(1, 3), F(1, 2), F(2, 3)],
            [(F(1, 5), F(4, 5)), (F(2, 5), F(3, 5))], [F(1, 10), F(1, 5)]):
            law = {(u, a, y): bernoulli(pu, u)*bernoulli(pa[u], a)*bernoulli(base+slope*a+F(1, 5)*u, y)
                   for u, a, y in product(range(2), repeat=3)}
            functionals = [sum(law[u, a, 1]/sum(law[u, a, y] for y in range(2))*bernoulli(pu, u)
                              for u in range(2)) for a in range(2)]
            do_law = [base+slope*a+F(1, 5)*pu for a in range(2)]
            assert functionals == do_law and min(law.values()) > 0
            tables.append(dict(family=family, parameters=[pu, pa, base, slope],
                observed={','.join(map(str, k)): v for k, v in law.items()},
                do_means=do_law, independent_functional=functionals))
    assert len(tables) == 72
    return dict(laws=tables, variable_permutations=[list(p) for p in permutations(range(3))],
                positive_law_requests=432, intervention_coordinate_evaluations=864)


def forest_moments():
    result = []
    for key, effects, propensities in [('F0', [F(0)]*2, [F(1, 2)]*2),
                                      ('F1', [F(20)]*2, [F(1, 2)]*2),
                                      ('F2', [F(-4), F(12)], [F(1, 5), F(4, 5)])]:
        mean = sum(effects)/2
        effect_variance = sum((t-mean)**2 for t in effects)/2
        noise_variance = sum(F(400)*(1/e+1/(1-e)) for e in propensities)/2
        variance = effect_variance+noise_variance
        result.append(dict(cell=key, population_ATE=mean, effect_variance=effect_variance,
            noise_score_variance=noise_variance, oracle_score_variance=variance,
            n=2000, oracle_mean_variance=variance/2000,
            normal_approximate_full_width_usd=2*1.959963984540054*float(variance/2000)**0.5))
    assert [x['oracle_score_variance'] for x in result] == [1600, 1600, 2564]
    return result


def calculate():
    result = dict(kind='independent_design_oracles_no_engine_execution', random_draws=0,
        screens={name: screen(2000, p0, p1) for name, p0, p1 in [
            ('graph_mismatch', F(1, 10), F(1, 20)),
            ('unavailable_or_useless', F(1, 20), F(1, 50)),
            ('interval_failure', F(3, 40), F(1, 20))]},
        family_error_bound='22/480', gaussian={k: gaussian_class(k) for k in ['chain', 'collider']},
        finite_functions=finite_functions(), forest=forest_moments(),
        limitations=['No engine, adapter, sampling study or bank qualification.',
            'Finite corpus equality does not prove general algorithm completeness.',
            'Binomial screening requires the registered independent replication law.'])
    return json.loads(json.dumps(result, default=str))


if __name__ == '__main__':
    result = calculate()
    print(json.dumps(dict(status='pass_for_design_arithmetic', screens=result['screens'],
        gaussian_models={k: len(v['models']) for k, v in result['gaussian'].items()},
        finite_laws=len(result['finite_functions']['laws']), forest=result['forest']), indent=2))
