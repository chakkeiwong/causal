"""Exact authored mediation targets and nonidentification witnesses."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


def calculate():
    # Zero-mean independent disturbances may be added without changing these means.
    mediator = lambda a: F(2 + 3*a)
    outcome = lambda a, m: 5 + 4*a + 2*m + a*m
    mu = {str(a)+str(b): outcome(a, mediator(b)) for a, b in product([0, 1], repeat=2)}
    effects = dict(total=mu['11']-mu['00'], pure_direct=mu['10']-mu['00'],
        total_indirect=mu['11']-mu['10'], pure_indirect=mu['01']-mu['00'],
        total_direct=mu['11']-mu['01'])
    assert effects['total'] == effects['pure_direct'] + effects['total_indirect']
    assert effects['total'] == effects['total_direct'] + effects['pure_indirect']

    # Observed A and U are independent fair bits. Both worlds yield M=A xor U,Y=A.
    observed, nested = {}, {}
    for world in ['direct', 'mediated']:
        def y(a, m, u):
            return a if world == 'direct' else m ^ u
        law = {}
        for a, u in product([0, 1], repeat=2):
            m = a ^ u
            key = str((a, m, y(a, m, u)))
            law[key] = law.get(key, F(0)) + F(1, 4)
        observed[world] = {k: str(v) for k, v in sorted(law.items())}
        means = {str(a)+str(b): sum(F(y(a, b ^ u, u), 2) for u in [0, 1])
            for a, b in product([0, 1], repeat=2)}
        nested[world] = {k: str(v) for k, v in means.items()}
    assert observed['direct'] == observed['mediated']
    assert nested['direct']['10'] == '1' and nested['mediated']['10'] == '0'

    # A nonlinear conditional-mean effect depends on the target covariate population.
    effect_at = lambda x: F(1, 10) + F(1, 10)*x*x
    average = sum(effect_at(x) for x in [-1, 1])/2
    at_mean = effect_at(0)

    # Residual correlated-error sensitivity: b_OLS = b + rho*sigma_e/sigma_u.
    a, b_observed, sigma_e_over_u = F(2), F(3), F(2)
    rho_values = [F(-1, 2), F(0), F(1, 2)]
    sensitivity = {str(r): str(a*(b_observed-r*sigma_e_over_u)) for r in rho_values}
    return dict(
        linear_interaction=dict(
            law='M(a)=2+3a+U; Y(a,m)=5+4a+2m+am+V; E(U)=E(V)=0 and independent for the stated causal model',
            means={k: str(v) for k, v in mu.items()},
            effects={k: str(v) for k, v in effects.items()},
            controlled_direct={str(m): str(outcome(1, F(m))-outcome(0, F(m))) for m in [0, 2, 5]},
            joint_program_fee10_margin=str(effects['total']-10),
            no_interaction_product='6'),
        observational_equivalence=dict(
            law='A,U independent fair bits; M(a)=a XOR U. Direct world Y(a,m)=a; mediated world Y(a,m)=m XOR U.',
            observed=observed, nested_means=nested,
            main_event_value100_fee20_total_margin='80',
            mediator_only_set1_vs0_effect='0',
            mediator_only_value100_fee20_margin='-20',
            interpretation='Randomized A and observed mediator overlap do not identify natural components; no assertion against a qualified vendor model.'),
        covariate_population=dict(
            law='P(Y=1|do(a),do(m),X=x)=1/5+a*(1/10+x^2/10), X is equally likely -1 or1; m has no role.',
            average_effect=str(average), at_mean_effect=str(at_mean),
            value100_fee15_average_margin=str(100*average-15),
            value100_fee15_at_mean_margin=str(100*at_mean-15)),
        inconsistent_mediation=dict(
            law='M(a)=a; Y(a,m)=3a-2m',
            total='1', pure_direct='3', total_indirect='-2', proportion='-2'),
        residual_sensitivity=dict(
            law='M=a*A+u;Y=c*A+b*M+e; A independent errors; Var(u)>0; rho=Corr(u,e)',
            identity='b_OLS=b+rho*sigma_e/sigma_u',
            illustrative_a='2',illustrative_b_OLS='3',assumed_sigma_e_over_u='2',
            scenarios=sensitivity, effect_range=['4','8'], point_assumption='6',
            value100_fee500_margin_range=['-100','300'],
            identification='Scenario set is not a confidence or credible interval; residual scale ratio is assumed, not identified from fitted residual SD alone.'),
        limits=['Exact authored constructions; no vendor executable, source-code port or bank data run.',
            'Natural-effect assumptions, controlled interventions, standardization and sensitivity scenarios are separate targets.',
            'Generated laws support no general interval-calibration or market-completeness claim.'])


if __name__ == '__main__':
    target = Path(__file__).resolve().parents[1]/'docs/program/execution/2026-10-20/mediation-commercial-v1/exact-results.json'
    assert not target.exists()
    target.write_text(json.dumps(calculate(), indent=2)+'\n')
    print(json.dumps(dict(status='exact_references_reproduced',output=str(target))))
