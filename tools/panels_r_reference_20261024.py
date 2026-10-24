#!/usr/bin/env python3
"""Independent panel aggregation and refusal fixtures; no upstream R execution."""
from fractions import Fraction as F
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def q(x):
 x=F(x);return dict(numerator=x.numerator,denominator=x.denominator,decimal=float(x))
def calculate():
 # Cohort 1 at t1,t2 has effects2,4;cohort2 at t2 has10;population shares3/4,1/4.
 simple=(F(3,4)*2+F(3,4)*4+F(1,4)*10)/(F(3,4)*2+F(1,4));group=F(3,4)*3+F(1,4)*10
 dynamic0=F(3,4)*2+F(1,4)*10;dynamic1=F(4);calendar1=F(2);calendar2=F(3,4)*4+F(1,4)*10
 assert (simple,group,dynamic0,dynamic1,(calendar1+calendar2)/2)==(4,F(19,4),4,4,F(15,4))
 # Stacked repeated-cross-section IF folds to units with factor one half.
 stacked=[F(-2),F(2),F(-4),F(4)];folded=[(stacked[i]+stacked[i+2])/2 for i in range(2)];unscaled=[stacked[i]+stacked[i+2] for i in range(2)]
 return dict(aggregation=dict(cells=[dict(group=1,time=1,att=2,share=q(F(3,4))),dict(group=1,time=2,att=4,share=q(F(3,4))),dict(group=2,time=2,att=10,share=q(F(1,4)))],simple=q(simple),group=q(group),dynamic_by_event=[q(dynamic0),q(dynamic1)],dynamic_overall=q((dynamic0+dynamic1)/2),calendar_by_time=[q(calendar1),q(calendar2)],calendar_overall=q((calendar1+calendar2)/2),balanced_one_lag_early_only=[2,4],balanced_overall=3),missing_cells=dict(unobserved_cell=[2,2],unavailable_true_value_not_imputed=True,available_simple=3,stipulated_full_simple=4,available_group=3,stipulated_full_group=q(F(19,4))),sampling_weights=dict(effects=[0,10],base_weights=[9,1],later_weights=[1,9],base_target=1,later_target=9,anchor_available_ids=['a'],original_ids=['a','b'],anchor_target=0),anticipation=dict(request_calendar=2,anticipation=1,cohort3_eligible=False,cohort4_eligible=True,rule='comparison cohort must adopt strictly after requested period plus anticipation'),folding=dict(stacked=[q(x) for x in stacked],folded=[q(x) for x in folded],unscaled=[q(x) for x in unscaled],variance_ratio_unscaled_to_folded=4,se_ratio=2),requested_contract=dict(cluster_requested='branch',retained_cluster='region',source_action='warn_and_remove_extra_clustering',required_adapter_action='refuse_or_return_explicit_nonconformant_status',band_requested='simultaneous',fallback='pointwise_when_critical_value_invalid_or_narrower_than_pointwise',required_band_status='pointwise_not_simultaneous'),economics=dict(total_usd=3000,requested=150,conformant=125,useful=100,per_request=20,per_conformant=24,per_useful=30,illustrative=True),native_execution=False)
if __name__=='__main__':
 p=ROOT/'docs/program/execution/2026-10-24/panels-r-v1/exact-results.json';assert not p.exists();p.write_text(json.dumps(calculate(),indent=2)+chr(10));print('Exact R-panel witnesses saved.')
