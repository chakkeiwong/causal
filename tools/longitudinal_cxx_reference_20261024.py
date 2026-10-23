#!/usr/bin/env python3
"""Project-owned rational oracles and abstract traces; no upstream execution."""
from fractions import Fraction as F
from decimal import Decimal, localcontext
import json


def calculate():
    rows = [(0, 1, 1), (1, 2, 0), (0, 2, 0)]
    risk = sum(a < 1 <= b for a, b, _ in rows)
    assert risk == 2
    # Unit exponentiated scores and two events tied at time 1; third censored at 2.
    # The mathematical Breslow score differentiates the whole tied contribution.
    breslow = [F(2, 3)-1, F(2, 3)-1, F(2, 3)]
    # Abstract traces of the specifically inspected loops, in stable row order.
    xgb, cat = [], []
    for kind, out in [('xgb', xgb), ('cat', cat)]:
        denominator, accumulated, last_score, last_time, reciprocal = F(3), F(0), F(0), F(0), F(0)
        for label in [1, 1, -2]:
            accumulated += last_score
            if (kind == 'xgb' and last_time < abs(label)) or (kind == 'cat' and label > 0):
                denominator -= accumulated
                accumulated = F(0)
            if label > 0:
                reciprocal += 1 / denominator
            out.append(reciprocal - int(label > 0))
            last_score, last_time = F(1), abs(label)
    assert xgb == [-F(2,3),-F(1,3),F(2,3)]
    assert cat == [-F(2,3),-F(1,6),F(5,6)]
    assert sum(breslow) == 0 and sum(xgb) == -F(1, 3) and sum(cat) == 0
    # Fixed finite cohort: four prepayments at 1, two defaults at 2, four survivors.
    cif = F(6, 10)*F(2, 6)
    net = F(2, 6)
    assert cif == F(1, 5) and net == F(1, 3)
    # Same logistic AFT location exp(m)=2: changing scale changes horizon probability.
    aft_p1, aft_p2 = F(4, 5), F(2, 3)  # horizon8; sigma1 and2
    # A leaf with d=1,n=2: KM1/2, Nelson-Aalen H1/2, exp(-H) differs.
    with localcontext() as ctx:
        ctx.prec = 45
        na_surv = (-Decimal(1)/2).exp()
        na_risk = 1-na_surv
        na_margin = Decimal(450)-1000*na_risk
        values = {k: format(v, '.12f') for k, v in
                  [('exp_negative_half',na_surv),('risk',na_risk),('margin_usd',na_margin)]}
    # Authored forest aggregation example: H=(0,log4), geometric versus arithmetic.
    geometric, arithmetic = F(1, 2), (F(1)+F(1, 4))/2
    return dict(
        delayed_entry=dict(correct_increment=str(F(1,risk)),ignoring_entry=str(F(1,3))),
        tied_event_nll_scores=dict(breslow=list(map(str,breslow)),
            xgboost_inspected_loop=list(map(str,xgb)),catboost_inspected_loop=list(map(str,cat)),
            sums=list(map(str,[sum(breslow),sum(xgb),sum(cat)])),
            assumptions='Three unit scores, event/event/censor ordered labels1,1,-2; abstract arithmetic only. Full call graph and native qualification open.'),
        competing_events=dict(default_cumulative_incidence=str(cif),net_default_risk=str(net),
            stipulated_loss_usd=1000,actual_target_loss_usd=str(1000*cif),
            substituted_net_loss_usd=str(1000*net)),
        aft_output=dict(exponentiated_location=2,horizon=8,scales=[1,2],
            logistic_failure_probabilities=[str(aft_p1),str(aft_p2)],output_is_probability=False),
        leaf_output=dict(kaplan_meier_survival='1/2',nelson_aalen_hazard='1/2',
            exponentiated_hazard_reference=values,stipulated_premium_usd=450,
            stipulated_loss_usd=1000,kaplan_meier_margin_usd=-50),
        forest_aggregation=dict(exp_negative_mean_hazard=str(geometric),
            mean_exponentiated_negative_hazard=str(arithmetic),difference=str(arithmetic-geometric)),
        scope='Authored finite laws, analytic examples and abstract branch traces, not fitted software results, native failures, calibrated causal estimates, observed prices or bank outcomes.')


if __name__ == '__main__':
    print(json.dumps(calculate(),indent=2))
