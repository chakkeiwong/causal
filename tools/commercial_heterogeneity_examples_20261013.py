#!/usr/bin/env python3
"""Exact generated servicing targets; no vendor execution or bank prices."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-13/commercial-heterogeneity'


def calculate():
    groups=[{'group':'lower_risk','mass':F(3,4),'propensity':F(1,10),'effect_USD':F(2),'cost_USD':F(1)},
            {'group':'higher_risk','mass':F(1,4),'propensity':F(4,5),'effect_USD':F(10),'cost_USD':F(12)}]
    ate=sum(g['mass']*g['effect_USD'] for g in groups)
    treated=sum(g['mass']*g['propensity'] for g in groups)
    att=sum(g['mass']*g['propensity']*g['effect_USD'] for g in groups)/treated
    overlap_mass=sum(g['mass']*g['propensity']*(1-g['propensity']) for g in groups)
    overlap=sum(g['mass']*g['propensity']*(1-g['propensity'])*g['effect_USD'] for g in groups)/overlap_mass
    assert ate==4 and treated==F(11,40) and att==F(86,11) and overlap==F(214,43)
    # Enumerate treatment Bernoulli states to check residual covariance and AIPW.
    eytilde_dtilde=F(0);edtilde2=F(0);aipw=F(0)
    for g in groups:
        p,e,tau=g['mass'],g['propensity'],g['effect_USD'];y0=F(8) if g['group']=='lower_risk' else F(4)
        h=y0+e*tau
        for d in [0,1]:
            w=p*(e if d else 1-e);y=y0+d*tau
            edtilde2+=w*(d-e)**2;eytilde_dtilde+=w*(d-e)*(y-h)
            score=tau+F(d)*(y-y0-tau)/e-F(1-d)*(y-y0)/(1-e)
            aipw+=w*score
    assert eytilde_dtilde/edtilde2==overlap and aipw==ate
    policy={}
    for bits in product([0,1],repeat=2):
        value=sum(g['mass']*b*(g['effect_USD']-g['cost_USD']) for g,b in zip(groups,bits))
        policy[str(bits)]=str(value)
    assert policy['(0, 0)']=='0' and policy['(1, 0)']=='3/4' and policy['(0, 1)']=='-1/2' and policy['(1, 1)']=='1/4'
    q=F(1,20);clipped=F(1,10);tau=F(10)
    raw_clipped_ipw=q*tau/clipped
    assert raw_clipped_ipw==5
    selection=sum(max(a,b) for a,b in product([-1,1],repeat=2))/4
    assert selection==.5
    return {'kind':'project_generated_exact_target_and_policy_examples','random_draws':0,
        'law':'Binary treatment independent of potential outcomes conditional on known risk group; stipulated group effects and positive treatment probabilities.',
        'groups':[{k:str(v) if isinstance(v,F) else v for k,v in g.items()} for g in groups],
        'targets':{'ATE':str(ate),'treated_fraction':str(treated),'ATET':str(att),'overlap_weighted_effect':str(overlap),
                   'po_constant_target':str(eytilde_dtilde/edtilde2),'population_mean_true_AIPW_score':str(aipw)},
        'coarsening_limit':'If the CATE conditioning X is constant but actual heterogeneity is in nuisance-only W, the constant residualized slope is e(W)(1-e(W))-weighted, not the population ATE.',
        'policy_net_USD_per_eligible_account':policy,
        'policy_limit':'Costs and effects are authored expected USD recoveries and costs over the same horizon; no observed prices, risk constraint, capacity constraint or estimated policy performance.',
        'clipping':{'true_propensity':str(q),'clipped_propensity':str(clipped),'treated_outcome':str(tau),'untreated_outcome':'0',
                    'unnormalized_IPW_target_after_floor':str(raw_clipped_ipw),'true_ATE':'10',
                    'limit':'A particular unnormalized IPW calculation; not a universal property of ratio-normalized, overlap-weighted or correctly specified AIPW estimators.'},
        'selection':{'two_equal_true_group_effects':0,'independent_Rademacher_errors':[-1,1],
                     'expected_larger_reported_effect':selection,'fresh_independent_error_mean':0,
                     'limit':'Elementary generated winner bias; not a claim that any inspected vendor implements this invalid evaluation.'}}


if __name__=='__main__':
    path=BASE/'exact-results.json';assert not path.exists()
    path.write_text(json.dumps(calculate(),indent=2)+'\n')
    print(json.dumps({'status':'pass','ATE':4,'ATET':'86/11','overlap':'214/43','net_lower_risk_only':'3/4','random_draws':0}))
