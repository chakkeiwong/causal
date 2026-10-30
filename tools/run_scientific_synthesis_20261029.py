"""Reproduce the prespecified illustrative study; no external software execution."""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json
import time

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/scientific-synthesis/2026-10-29'


def frequency(values):
    x = np.asarray(values, dtype=float)
    p = float(x.mean())
    return dict(rate=p, monte_carlo_se=float(np.sqrt(p * (1-p) / len(x))), count=len(x))


def main():
    start = time.monotonic()
    plan_bytes = (OUT / 'study-plan.json').read_bytes()
    plan = json.loads(plan_bytes)
    spec = plan['scenarios']
    seeds = np.random.SeedSequence(spec['seed']).spawn(
        len(spec['sample_sizes']) * len(spec['propensities_s1']))
    results = []
    index = 0
    for n in spec['sample_sizes']:
        for e1 in spec['propensities_s1']:
            rng = np.random.default_rng(seeds[index])
            index += 1
            own_target = 100 * e1*(1-e1) / (0.25 + e1*(1-e1))
            methods = {'constant_projection': [], 'standardized_strata': []}
            cells = []
            for _ in range(spec['replications']):
                s = rng.integers(0, 2, n)
                e = np.where(s == 0, 0.5, e1)
                a = rng.binomial(1, e)
                y = 50*s + 100*s*a + rng.normal(0, 50, n)
                ar = a-e
                yr = y-(50*s+100*s*e)
                denominator = ar @ ar
                b = float(ar @ yr / denominator)
                se = float(np.sqrt(np.sum((ar*(yr-b*ar))**2)) / denominator)
                methods['constant_projection'].append((b, se))
                groups = [y[(s == j) & (a == k)] for j in (0, 1) for k in (0, 1)]
                cells.append(min(map(len, groups)))
                if min(map(len, groups)) < 2:
                    methods['standardized_strata'].append(None)
                else:
                    b = float(0.5*(groups[1].mean()-groups[0].mean()
                                   + groups[3].mean()-groups[2].mean()))
                    se = float(np.sqrt(0.25*sum(g.var(ddof=1)/len(g) for g in groups)))
                    methods['standardized_strata'].append((b, se))
            summary = dict(n=n, propensity_s1=e1, population_ate=50,
                           offer_cost=40, population_net_value=10,
                           projection_target=own_target,
                           min_cell_observed=min(cells), methods={})
            for method, rows in methods.items():
                available = [r for r in rows if r is not None]
                estimates, ses = np.array(available).T
                target = own_target if method == 'constant_projection' else 50
                coverage_own = np.abs(estimates-target) <= 1.959963984540054*ses
                coverage_ate = np.abs(estimates-50) <= 1.959963984540054*ses
                rejection = estimates <= 40
                summary['methods'][method] = dict(
                    available=len(available), unavailable=len(rows)-len(available),
                    mean_estimate=float(estimates.mean()),
                    bias_own_target=float(estimates.mean()-target),
                    bias_population_ate=float(estimates.mean()-50),
                    rmse_population_ate=float(np.sqrt(np.mean((estimates-50)**2))),
                    mean_standard_error=float(ses.mean()),
                    coverage_own_conditional=frequency(coverage_own),
                    coverage_ate_conditional=frequency(coverage_ate),
                    coverage_ate_unconditional=float(coverage_ate.sum()/len(rows)),
                    reject_profitable_offer_conditional=frequency(rejection),
                    incorrect_or_unavailable_unconditional=float(
                        (rejection.sum()+len(rows)-len(available))/len(rows)),
                    conditional_point_rule_regret=float(10*rejection.mean()))
            results.append(summary)
    exact = {
        'panel': {'treated_cell': str((F(3,4)*2+F(3,4)*4+F(1,4)*10)/(F(3,4)*2+F(1,4))),
                  'group': str(F(3,4)*3+F(1,4)*10),
                  'dynamic': str((F(3,4)*2+F(1,4)*10+4)/2),
                  'calendar': str((2+F(3,4)*4+F(1,4)*10)/2)},
        'projection': {'ate': '50', 'projection_e1_one_tenth': str(F(100)*F(9,100)/(F(1,4)+F(9,100))),
                       'offer_cost': '40', 'net_population_value': '10'},
        'proxy': [{'noise_variance': str(s), 'adjusted_slope': str(-F(1,5)+s/(1+2*s))}
                  for s in [F(0),F(1,10),F(1,3),F(1),F(4)]],
        'graph': {'effects': ['0','12/25'], 'units': 'thousand currency units per percentage point',
                  'action_percentage_points': '1/4', 'cost_currency_units': '60',
                  'gross_value_range': ['0','120'], 'net_value_range': ['-60','60'],
                  'interpretation': 'No sign-robust recommendation under the specified equivalent models'},
    }
    assert exact['panel'] == dict(treated_cell='4',group='19/4',dynamic='4',calendar='15/4')
    assert exact['projection']['projection_e1_one_tenth'] == '450/17'
    assert exact['proxy'][2]['adjusted_slope'] == '0'
    # Independent covariance solution for the Gaussian proxy example.
    for item in exact['proxy']:
        s = float(F(item['noise_variance']))
        covariance = np.array([[2.,1.],[1.,1.+s]])
        cross = np.array([0.6,0.8])
        assert np.isclose(np.linalg.solve(covariance,cross)[0],float(F(item['adjusted_slope'])))
    # All three non-collider chains reproduce the same covariance; intervention
    # effects are compared using the explicit structural coefficient matrices.
    sigma = np.array([[1,.6,.48],[.6,1.36,1.088],[.48,1.088,1.8704]])
    orientations = [[[],[0],[1]],[[1],[],[1]],[[1],[2],[]]]
    effects = []
    for parents in orientations:
        b = np.zeros((3,3)); v = np.zeros(3)
        for j, pa in enumerate(parents):
            if pa:
                coefs = np.linalg.solve(sigma[np.ix_(pa,pa)],sigma[pa,j])
                b[j,pa]=coefs; v[j]=sigma[j,j]-sigma[j,pa]@coefs
            else:
                v[j]=sigma[j,j]
        transform=np.linalg.inv(np.eye(3)-b)
        assert np.all(v>0)
        assert np.allclose(transform@np.diag(v)@transform.T,sigma)
        effects.append(float(transform[2,0]))
    assert np.allclose(effects,[.48,0,0])
    output = dict(plan_sha256=sha256(plan_bytes).hexdigest(),
                  code_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                  numpy_version=np.__version__, replications_per_scenario=spec['replications'],
                  scenarios=results, exact=exact, graph_reconstruction_effects=effects,
                  seconds=round(time.monotonic()-start,3),
                  scope=plan['kind'], package_execution=False)
    (OUT/'study-results.json').write_text(json.dumps(output,indent=2)+'\n')
    rows=[]
    for r in results:
        for name,m in r['methods'].items():
            label='Constant projection' if name=='constant_projection' else 'Stratum standardisation'
            rows.append(f"{r['n']} & {r['propensity_s1']:.2f} & {label} & "
                        f"{m['mean_estimate']:.1f} & {m['coverage_ate_conditional']['rate']:.3f} & "
                        f"{m['reject_profitable_offer_conditional']['rate']:.3f} & {m['unavailable']} "+r'\\')
    table=r'''\begin{table}[htbp]
\centering\small
\begin{tabular}{rrlrrrr}
\toprule
$n$ & $e(1)$ & Method & Mean & ATE cover & Reject & Fail \\
\midrule
'''+ '\n'.join(rows)+r'''
\bottomrule
\end{tabular}
\caption{Project-generated offer study. True population benefit is 50 and
stipulated cost is 40 illustrative USD per customer. Coverage and rejection
frequencies condition on an available estimate; Fail counts unavailable
replications out of 500. These are independent reference calculations,
not outputs from an external causal package.}
\label{scisyn:offer-results}
\end{table}
'''
    (OUT/'offer-results-table.tex').write_text(table)
    print(json.dumps({'scenarios':len(results),'replications':len(results)*spec['replications'],
                      'seconds':output['seconds'],'exact_checks':'pass','results':'docs/scientific-synthesis/2026-10-29/study-results.json'}))


if __name__=='__main__':
    main()
