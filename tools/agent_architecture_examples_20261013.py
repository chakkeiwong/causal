#!/usr/bin/env python3
"""Exact authored architecture examples: no model or vendor calls."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-13/agent-architecture'

def majority(p):
    return sum(p**sum(bits)*(1-p)**(3-sum(bits)) for bits in product([0,1],repeat=3) if sum(bits)>=2)

def main():
    q=F(1,10);gamma=F(1,20);residual=F(1,19)
    assert gamma+(1-gamma)*residual==q
    independent=majority(q);shared=gamma+(1-gamma)*majority(residual)
    assert independent==F(7,250)
    assert q**3+3*q*q*(1-q)==independent
    screening=1-F(19,20)**20
    # Two independent exact calculations: complement and first-failure enumeration.
    assert screening==sum(F(19,20)**k*F(1,20) for k in range(20))
    # Identical observed Gaussian law, two different causal interpretations.
    forward={'var_X':F(1),'cov_XY':F(1,2),'var_Y':F(1),'effect_X_to_Y':F(1,2)}
    reverse={'var_Y':F(1),'cov_XY':F(1,2),'var_X':F(1),'effect_X_to_Y':F(0)}
    assert all(forward[k]==reverse[k] for k in ['var_X','var_Y','cov_XY'])
    # Same generated population, three different target measures. No fitting.
    strata=[{'mass':F(1,4),'propensity':F(1,20),'effect_USD':F(-200)},
            {'mass':F(1,2),'propensity':F(1,2),'effect_USD':F(100)},
            {'mass':F(1,4),'propensity':F(4,5),'effect_USD':F(500)}]
    ate=sum(r['mass']*r['effect_USD'] for r in strata)
    kept=[r for r in strata if F(1,10)<=r['propensity']<=F(9,10)]
    trimmed=sum(r['mass']*r['effect_USD'] for r in kept)/sum(r['mass'] for r in kept)
    overlap=sum(r['mass']*r['propensity']*(1-r['propensity'])*r['effect_USD'] for r in strata)/sum(r['mass']*r['propensity']*(1-r['propensity']) for r in strata)
    assert (ate,trimmed,overlap)==(F(125),F(700,3),F(48200,283))
    # Independent finite population of 400: exactly assigned within each stratum.
    units=[]
    for r in strata:
        n=int(400*r['mass']);treated=int(n*r['propensity'])
        for j in range(n):
            a=int(j<treated);m0=F(1000);m1=m0+r['effect_USD'];y=m1 if a else m0
            score=m1-m0+a*(y-m1)/r['propensity']-(1-a)*(y-m0)/(1-r['propensity'])
            units.append((r['propensity'],score))
    assert sum(score for _,score in units)/400==ate
    kept_units=[score for e,score in units if F(1,10)<=e<=F(9,10)]
    assert sum(kept_units)/len(kept_units)==trimmed
    assert sum(e*(1-e)*score for e,score in units)/sum(e*(1-e) for e,_ in units)==overlap
    economics={'manual':{'tool_USD':F(0),'review_minutes':F(15),'usable_fraction':F(9,10)},'assisted_short_review':{'tool_USD':F(3),'review_minutes':F(6),'usable_fraction':F(4,5)},'assisted_long_review':{'tool_USD':F(3),'review_minutes':F(20),'usable_fraction':F(4,5)}}
    for row in economics.values():
        row['cost_per_request_USD']=row['tool_USD']+row['review_minutes']*F(120,60)
        row['cost_per_usable_USD']=row['cost_per_request_USD']/row['usable_fraction']
    assert economics['assisted_short_review']['cost_per_usable_USD']==F(75,4)
    assert economics['assisted_long_review']['cost_per_usable_USD']==F(215,4)
    assert economics['manual']['cost_per_usable_USD']==F(100,3)
    budget=(F(100,3)*F(4,5)-3)/2
    assert budget==F(71,6)
    result={'kind':'exact_generated_architecture_reference','random_draws':0,'live_calls':0,'critics':{'marginal_error':str(q),'independent_three_majority_error':str(independent),'perfect_common_error':str(q),'mixture_common_shock_probability':str(gamma),'residual_error_without_common_shock':str(residual),'mixture_majority_error':str(shared),'mixture_majority_decimal':float(shared)},'screening':{'tries':20,'per_try_false_screen_pass':str(F(1,20)),'independent_at_least_one_false_pass':str(screening),'decimal':float(screening),'arbitrary_dependence_union_bound':'1','limit':'Stipulated independent false-pass experiment; not actual model errors, p-values or repeated deterministic replay.'},'equal_law':{'forward_X_U_Y_halfX_noise':{k:str(v) for k,v in forward.items()},'reverse_Y_V_X_halfY_noise':{k:str(v) for k,v in reverse.items()},'both_residual_variances':'3/4','argument':'Any adaptive transcript kernel conditioned only on the same observed law, the same supplied documents and world-independent randomness has the same law in both causal worlds. Genuine additional scientific information changes that premise.'},'economics':{k:{a:str(v) for a,v in row.items()} for k,row in economics.items()},'assisted_review_break_even_minutes':str(budget),'limit':'Authored prices, times and usable fractions; no measured quality, invoice, bank ROI or live agent trial.'}
    result['target_measures']={'strata':[{k:str(v) for k,v in r.items()} for r in strata],
       'population_ATE_USD':str(ate),'trimmed_ATE_USD':str(trimmed),
       'overlap_ATO_USD':str(overlap),'trimmed_retained_mass':'3/4',
       'finite_population_reference_units':len(units),
       'limit':'Authored potential outcomes and known propensities; no bank observations, fitted nuisance models or repeated-sampling coverage claim.'}
    path=BASE/'exact-results.json';assert not path.exists();path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'pass','independent_majority':float(independent),'shared_majority':float(shared),'twenty_screen_false_pass':float(screening),'break_even_review_minutes':float(budget),'live_calls':0}))

if __name__=='__main__':main()
