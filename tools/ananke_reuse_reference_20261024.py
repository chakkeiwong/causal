#!/usr/bin/env python3
"""Authored finite examples; imports no downloaded Ananke or dependency code."""
from fractions import Fraction as F
import json, math

def calculate():
    p0,p1=F(1,5),F(2,5)
    difference=p1-p0
    odds_ratio=(p1/(1-p1))/(p0/(1-p0))
    log_odds=math.log(float(odds_ratio))
    assert difference==F(1,5) and odds_ratio==F(8,3)
    # Hypothetical identical fitted means isolate reporting semantics. They are
    # not asserted to arise from a package estimator or a bootstrap data sample.
    authored_display=lambda names: ''.join(names)
    name_groups=[['A','BC'],['AB','C']]
    assert name_groups[0]!=name_groups[1]
    assert authored_display(name_groups[0])==authored_display(name_groups[1])=='ABC'
    indicator='R_credit_score'
    inferred='X_'+indicator.split('_')[1]
    assert inferred=='X_credit' and inferred!='X_credit_score'
    costs={str(n):str(F(3000,n)) for n in [150,125,100]}
    assert list(costs.values())==['20','24','30']
    return dict(status='exact_authored_reference',downloaded_code_executed=False,
        effect_scale=dict(p0=str(p0),p1=str(p1),difference=str(difference),
            odds_ratio=str(odds_ratio),log_odds_ratio=log_odds,
            report_log_odds_false_binary_point=str(difference),
            hypothetical_constant_binary_bootstrap_endpoints=[log_odds,log_odds],
            exact_log_endpoints=['log(8/3)','log(8/3)'],
            qualification='Conditional reporting-branch witness; not observed fitted estimates or uncertainty coverage'),
        functional_names=dict(distinct_token_arrays=name_groups,joined_display='ABC',
            qualification='Bare concatenation is not an injective encoding; not a claim of identical graph identification results'),
        missingness_names=dict(indicator=indicator,source_style_lookup=inferred,
            intended_full_suffix='X_credit_score',
            qualification='Authored string operation; require injective reviewed schema instead of unrestricted names'),
        cost_usd=dict(total=3000,requested=150,finite=125,accepted=100,per_denominator=costs,
            qualification='Authored illustration; no measured cost or bank value'))

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
