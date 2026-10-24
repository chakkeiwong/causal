#!/usr/bin/env python3
"""Authored rational conformance examples; never executes a surveyed package."""
from fractions import Fraction as F
from pathlib import Path
import json,math
ROOT=Path(__file__).resolve().parents[1]
def q(x):
    x=F(x);return dict(numerator=x.numerator,denominator=x.denominator,decimal=float(x))
def calculate():
    naive=F(2)+F(3,2);causal=F(2)
    x=[F(-2),F(-1),F(1),F(2)];a=[v*v for v in x]
    mx=sum(x)/4;ma=sum(a)/4;cov=sum((u-mx)*(v-ma) for u,v in zip(x,a))/4
    assert cov==0 and a==[4,1,1,4]
    w=[F(1),F(1),F(8)];wc=[F(1),F(1),F(2)];y=[F(0),F(0),F(100)]
    avg=lambda ws:sum(u*v for u,v in zip(ws,y))/sum(ws)
    ess=lambda ws:sum(ws)**2/sum(u*u for u in ws)
    before,after=avg(w),avg(wc);assert before==80 and after==50
    # Independent disjoint miss events: 5% miss at each grid point, 10% union.
    outcomes=list(range(100));miss0=set(range(5));miss1=set(range(5,10));joint=F(len(set(outcomes)-miss0-miss1),100)
    assert joint==F(9,10)
    # Shared baseline variance is retained in the covariance of adjusted means.
    c=[F(-1),F(0),F(1)];mu=[F(0),F(1),F(2)];S=[F(1,100)]*3
    signal=sum(u*v for u,v in zip(c,mu));variance=sum(u*u*s for u,s in zip(c,S))
    V=[[F(2,100),F(1,100)],[F(1,100),F(2,100)]];d=[F(-1),F(1)]
    full=sum(d[i]*V[i][j]*d[j] for i in range(2) for j in range(2));diagonal=sum(d[i]*d[i]*V[i][i] for i in range(2))
    # Constant shift policy under two observationally equivalent Gaussian SEMs.
    return dict(confounding=dict(var_A=2,cov_A_X=1,observational_slope=q(naive),causal_slope=q(causal),dollars_per_outcome_unit=100,action_cost_usd=220,observational_net_usd=130,causal_net_usd=-20),density_units=dict(original_marginal=q(F(1,5)),original_conditional=q(F(1,10)),rescaled_marginal=q(F(1,500)),rescaled_conditional=q(F(1,1000)),ratio_original=2,ratio_rescaled=2,inverse_density_original=10,inverse_density_rescaled=1000),residual_density=dict(marginal=q(F(1,5)),standardized_residual_density=q(F(2,5)),scales=[q(2),q(F(1,2))],literal_weights=[q(F(1,2)),q(F(1,2))],proper_location_scale_weights=[q(1),q(F(1,4))],claim='Literal selected branch only; conditional-density model assumption required; no native run'),transformed_density=dict(t=4,log_scale_density=q(F(1,5)),original_scale_density=q(F(1,20)),jacobian=q(F(1,4)),claim='Fixed-dose balancing is invariant to positive dose-only factors; a parametric outcome surface need not be invariant'),balance=dict(X=[int(v) for v in x],A=[int(v) for v in a],covariance=q(cov),dependent=True,overlap=False),trimming=dict(full_population_effect=q(F(4,5)*10+F(1,5)*100),retained_population_effect=10,weighted_mean_before=q(before),winsorized_mean_after=q(after),ess_before=q(ess(w)),ess_after=q(ess(wc))),zero_weight=dict(weights=[0,0],outcomes=[0,100],source_replacement=[1,1],unweighted_mean=50,causal_status='unresolved_no_valid_weighted_population'),bands=dict(pointwise_coverage=q(F(95,100)),joint_coverage=q(joint),bootstrap_replicates_20_lower_index=math.floor(.025*20),bootstrap_replicates_40_lower_index=math.floor(.025*40)),longitudinal=dict(period_weights=[q(2),q(3)],correct_product=6,incorrect_sum=5,independent_customers=20,visits_per_customer=25,intraclass_correlation=q(F(3,5)),naive_mean_variance=q(F(1,500)),cluster_mean_variance=q(F(77,2500))),contrasts=dict(contrast=[int(v) for v in c],signal=q(signal),variance=q(variance),t_squared=q(signal*signal/variance),placebo_adjusted_full_variance=q(full),diagonal_only_variance=q(diagonal),delta=1,curve_at_doses_0_1_2=[0,2,3],effective_dose_for_one_unit=q(F(1,3)),linear_cost_per_dose=2,profit_at_doses_0_1_2=[0,0,-1],claim='Inverse response target is distinct from an optimal net-value policy'),economics=dict(total_usd=2400,requests=100,conformant=80,useful=60,per_request=24,per_conformant=30,per_useful=40),native_execution=False)
if __name__=='__main__':
    p=ROOT/'docs/program/execution/2026-10-24/dose-response-reuse-v1/exact-results.json';assert not p.exists();p.write_text(json.dumps(calculate(),indent=2)+'\n');print('Exact authored dose-response witnesses pass; no native execution.')
