#!/usr/bin/env python3
"""Independent authored mediation contracts; no package or downloaded code."""
from fractions import Fraction as F
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def q(x):
 x=F(x);return dict(numerator=x.numerator,denominator=x.denominator,decimal=float(x))
def calculate():
 # M(t)=a*t+U; Y(t,m)=c*t+b*m+g*t*m; E(U)=m0.
 a,b,c,g,m0=F(2),F(3),F(1),F(4),F(1)
 indirect=[a*b,a*(b+g)];direct=[c+g*m0,c+g*(m0+a)];total=indirect[0]+direct[1]
 assert total==indirect[1]+direct[0]==19
 # Three illustrative Monte Carlo draws: median ratios differ from ratio of means.
 ds=[F(1),F(2),F(9)];ts=[F(1),F(4),F(10)];ratios=[d/t for d,t in zip(ds,ts)]
 ratio_of_means=sum(ds)/sum(ts);median_ratio=sorted(ratios)[1]
 assert ratio_of_means==F(4,5) and median_ratio==F(9,10)
 return dict(numerical_selection=dict(stipulated_complete_values=[1,3,100],complete_mean=q(F(104,3)),one_unresolved_value=True,finite_only_values=[1,3],finite_only_mean=2,source_status='Return failure counters;do not relabel selected finite mean as complete target'),economics=dict(total_usd=1800,requests=100,conformant=75,useful=60,per_request=18,per_conformant=24,per_useful=30),interaction=dict(mediator_shift=q(a),mediator_baseline_mean=q(m0),outcome_mediator_coefficient=q(b),outcome_direct_coefficient=q(c),interaction_coefficient=q(g),indirect=[q(v) for v in indirect],direct=[q(v) for v in direct],total=q(total),correct_pairs=[[0,1],[1,0]],incorrect_same_index_sums=[q(indirect[i]+direct[i]) for i in [0,1]],dollars_per_unit=100,mediated_value_control_usd=600,mediated_value_treated_usd=1400),ratio_summary=dict(indirect_draws=[q(v) for v in ds],total_draws=[q(v) for v in ts],median_of_draw_ratios=q(median_ratio),ratio_of_means=q(ratio_of_means)),zero_total=dict(indirect=1,direct=-1,total=0,mediated_proportion='undefined'),categorical_treatment=dict(requested=['none','offer'],available_levels=['declined','offered'],source_fallback=['declined','offered'],required_status='refuse_unmapped_treatment_levels'),sampling_weights=dict(weights=[1,9],effects=[0,10],weighted_average=9,unweighted_average=5,semantics='Sampling weights are distinct from binomial trial totals'),population_join=dict(mediator_ids=['a','b','c'],outcome_ids=['b','c','d'],intersection=['b','c'],retained_fraction=q(F(2,4))),cluster_bootstrap=dict(customers=20,visits=25,rho=q(F(3,5)),naive_variance=q(F(1,500)),cluster_variance=q(F(77,2500)),claim='Source warns cluster ignored for ordinary bootstrap;not native failure'),sensitivity=dict(interpretation='rho is a hypothetical residual association,not an identified confounding estimate',unsupported='binary logit outcome in selected medsens branch'),native_execution=False)
if __name__=='__main__':
 p=ROOT/'docs/program/execution/2026-10-24/mediation-reuse-v1/exact-results.json';assert not p.exists();p.write_text(json.dumps(calculate(),indent=2)+'\n');print('Exact authored mediation witnesses saved; no native execution.')
