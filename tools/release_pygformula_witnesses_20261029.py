"""Exact authored fitting-population laws; never imports downloaded software."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import math

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/release/2026-10-29/source-pygformula-025'


def main():
    target = OUT / 'exact-witnesses.json'
    assert not target.exists(), 'Single-use witness: retain the prior result.'
    rows = []
    for x in [0, 1]:
        rows.extend(dict(x=x, eligible=1, z=int(i < 8), time=1) for i in range(10))
        rows.extend(dict(x=x, eligible=0, z=0, time=1) for _ in range(10))
    fit_sets = {'restricted': [r for r in rows if r['eligible']], 'unrestricted': rows}
    fits = {}
    for name, subset in fit_sets.items():
        probabilities = [F(sum(r['z'] for r in subset if r['x'] == x),
                           sum(r['x'] == x for r in subset)) for x in [0, 1]]
        assert probabilities[0] == probabilities[1]
        q = probabilities[0]
        # Both intercept and slope scores vanish at this constant fitted q.
        scores = [sum((F(r['z'])-q)*(1 if j == 0 else r['x']) for r in subset)
                  for j in [0, 1]]
        assert scores == [0, 0]
        # The two predictor cells each contain both binary outcomes. Thus
        # the binomial log-likelihood is strictly concave at a finite fit.
        information = [[sum(q*(1-q)*(1 if j == 0 else r['x'])*(1 if k == 0 else r['x'])
                            for r in subset) for k in [0, 1]] for j in [0, 1]]
        determinant = information[0][0]*information[1][1]-information[0][1]**2
        assert determinant > 0
        portfolio_mean = F(1, 2)*q
        fits[name] = dict(n=len(subset), conditional_probabilities=list(map(str, probabilities)),
                          intercept=math.log(float(q/(1-q))), slope=0, scores=list(map(str, scores)),
                          information_determinant=str(determinant),
                          portfolio_mean=str(portfolio_mean), contingent_receipt='100', account_cost='30',
                          net=str(100*portfolio_mean-30))
    assert fits['restricted']['net'] == '10' and fits['unrestricted']['net'] == '-10'

    # This describes the documented list/string membership contract using
    # inert labels; it does not evaluate callbacks or execute upstream code.
    restrictions = [['Z', {'E': 'equals one'}, 0]]
    fitting_names = [restrictions[0] for _ in restrictions]
    simulation_names = [r[0] for r in restrictions]
    membership = dict(fitting_recognizes_name='Z' in fitting_names,
                      simulation_recognizes_name='Z' in simulation_names)
    assert membership == dict(fitting_recognizes_name=False, simulation_recognizes_name=True)

    outcomes = [1]*8 + [0]*72 + [None]*20
    observed = [v for v in outcomes if v is not None]
    observed_risk = F(sum(observed), len(observed))
    zero_risk = F(sum(v or 0 for v in outcomes), len(outcomes))
    bounds = [zero_risk, F(sum(observed)+20, len(outcomes))]
    censoring = dict(accounts=100, observed_defaults=8, observed_nondefaults=72, missing_outcomes=20,
                     observed_risk=str(observed_risk), zero_encoded_risk=str(zero_risk),
                     finite_population_bounds=list(map(str, bounds)),
                     payout='10000', premium='900',
                     observed_model_margin=str(10000*observed_risk-900),
                     zero_encoded_margin=str(10000*zero_risk-900))
    assert [censoring['observed_model_margin'], censoring['zero_encoded_margin']] == ['100', '-100']
    q = F(20, 100)
    p = F(8, 80)
    competing = dict(prepayments=20, defaults=8, no_event=72,
                     prepayment_hazard=str(q), default_given_no_prepayment=str(p),
                     default_incidence=str((1-q)*p),
                     double_counted_incidence=str((1-q)*F(8, 100)),
                     two_period_incidence=str((1-q)*p*(1+(1-q)*(1-p))),
                     eliminated_prepayment_incidence=str(1-(1-p)**2))
    assert [competing[k] for k in ['default_incidence', 'double_counted_incidence',
                                  'two_period_incidence', 'eliminated_prepayment_incidence']] == [
        '2/25', '8/125', '86/625', '19/100']
    identities = {}
    for name in ['authenticated-files.json', 'authenticated-retained-files.json']:
        for row in json.loads((OUT/name).read_text()):
            path = ROOT/row['local_path']
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            assert digest == row['sha256']
            identities[row['local_path']] = digest
    report = dict(status='pass', scope='Exact authored likelihood and finite-law calculations. No upstream import, native runtime, causal-effect estimate, empirical coverage or bank observations.',
                  restrictions=dict(records=rows, fits=fits, source_schema_membership=membership),
                  censoring=censoring, competing=competing, source_bindings=identities)
    target.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ['source_bindings', 'restrictions']}))


if __name__ == '__main__':
    main()
