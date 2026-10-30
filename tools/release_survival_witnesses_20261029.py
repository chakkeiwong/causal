"""Project-owned exact survival contracts; no acquired implementation executes."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import math

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/release/2026-10-29/source-survival-022'


def main():
    rows = [(F(4), F(5), 1), (F(4), F(6), 0)]
    events = sum(r[2] for r in rows)
    exposure = sum(t-l for l, t, _ in rows)
    naive_exposure = sum(t for _, t, _ in rows)
    entry_rate, naive_rate = F(events)/exposure, F(events)/naive_exposure
    assert (entry_rate, naive_rate) == (F(1, 3), F(1, 11))
    entry = dict(records=[[str(l), str(t), e] for l,t,e in rows],
                 event_count=events, conditional_exposure=str(exposure),
                 origin_exposure=str(naive_exposure),
                 conditional_rate=str(entry_rate), origin_rate=str(naive_rate),
                 next_month_loss=[100 * -math.expm1(-float(x))
                                  for x in [entry_rate, naive_rate]],
                 interpretation='Exponential right-censor likelihood conditioned on survival to entry; independent entry/censoring assumed. A project example, not a Julia fit.')

    # c1 = exp(x alpha), c2 = exp(x beta - x alpha). Use rational
    # multipliers and integer covariates so the entire witness is exact.
    shape, scale = 2, F(5)
    parameters = [(F(1), F(3)), (F(2), F(3, 2))]
    evaluations = []
    for x in [0, 1, 2]:
        for t in [F(1), F(3), F(7)]:
            values = []
            for a, b in parameters:
                c1, c2 = a**x, (b/a)**x
                H = (t*c1/scale)**shape*c2
                hazard = F(shape)*t**(shape-1)/scale**shape*(a**(shape-1)*b)**x
                values.append((H, hazard))
            assert values[0] == values[1]
            evaluations.append(dict(x=x,t=str(t),H=str(values[0][0]),hazard=str(values[0][1])))
    # Independent exponential AH cancellation across time-scale multipliers.
    ah = [(F(3)*a/F(5))/a for a in [F(1, 2), F(1), F(7)]]
    assert len(set(ah)) == 1 and ah[0] == F(3, 5)
    ridge = dict(shape=shape, scale=str(scale),
                 exp_alpha_beta=[[str(a),str(b)] for a,b in parameters],
                 shared_covariate=True, identified_combination='(k-1)*alpha+beta',
                 evaluations=evaluations, exponential_ah_H=str(ah[0]),
                 interpretation='Equal hazards and cumulative hazards imply equal right-censored likelihood contributions at every t, status and covariate. No native optimization claim.')

    mu_month = math.log(0.5)
    mu_day = mu_month + math.log(30)
    assert mu_month < 0 < mu_day
    median = [math.exp(mu_month), math.exp(mu_day)]
    assert math.isclose(median[1],30*median[0])
    domain = dict(mu_month=mu_month,mu_day=mu_day,median_month_day=median,
                  allowed_mu='all real numbers',positive_parameter_fit_mu='strictly positive only',
                  example_scope='Baseline-only log-logistic fit with no regression covariates; location is not a positive scale.')

    # Trace the inspected piecewise quantile branch, translated as arithmetic;
    # this is not importing or executing downloaded Julia.
    widths, rates = [F(1)], [F(1,5)]
    p = F(9,10)
    target = -math.log1p(-float(p));total_H=F(0);endpoint=F(0)
    branch = None
    for width,rate in zip(widths,rates):
        total_H += width*rate;endpoint += width
        if target < total_H:
            branch=float(endpoint)-(float(total_H)-target)/float(rate)
            break
    if branch is None:branch=float(endpoint)
    true_q = target/float(rates[-1])
    assert branch==1 and math.isclose(true_q,5*math.log(10)) and true_q>11
    assert math.isclose(-math.expm1(-float(rates[0])*true_q),float(p))
    full_mean=1/float(rates[0]);truncated_mean=(1-math.exp(-0.2))/0.2
    tail=dict(widths=[str(v) for v in widths],rates=[str(v) for v in rates],
              probability=str(p),quantile_branch=branch,correct_quantile=true_q,
              formula='5*log(10)',survival_at_grid_endpoint=math.exp(-0.2),
              full_mean=full_mean,truncated_mean_at_endpoint=truncated_mean,
              monthly_cashflow=100,expected_cashflow=100*full_mean,
              one_month_restricted_cashflow=100*truncated_mean,
              interpretation='Constant positive hazard continues beyond one-month grid endpoint. Cashflow illustration assumes no discounting, competing events or costs. Truncation changes the target, not just precision.')
    H=2.0;prob=-math.expm1(-H)
    output=dict(cumulative_hazard=H,event_probability=prob,
                stipulated_loss_if_event=100,expected_loss=100*prob,
                incorrect_hazard_as_probability_loss=100*H,
                interpretation='Cumulative hazard is not an expected lifetime, probability or monetary value.')
    report=dict(status='pass',scope='Exact/rational or elementary analytic project witnesses; no vendor execution or banking observations.',
                delayed_entry=entry,weibull_ridge=ridge,loglogistic_units=domain,
                piecewise_tail=tail,output_meaning=output,
                generator=dict(path=str(Path(__file__).relative_to(ROOT)),
                               sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()))
    OUT.mkdir(exist_ok=True)
    (OUT/'exact-witnesses.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    main()
