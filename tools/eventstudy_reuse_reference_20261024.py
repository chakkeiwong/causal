#!/usr/bin/env python3
"""Authored cohort,control and covariance witnesses; no Stata execution."""
from fractions import Fraction as F
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def q(x):
 x=F(x);return dict(numerator=x.numerator,denominator=x.denominator,decimal=float(x))
def calculate():
 w=[F(3,4),F(1,4)];effects=[F(2),F(10)];V=[[F(4),F(1)],[F(1),F(9)]]
 agg=sum(w[i]*effects[i] for i in range(2));variance=sum(w[i]*V[i][j]*w[j] for i in range(2) for j in range(2));diagonal=sum(w[i]**2*V[i][i] for i in range(2));share=(effects[0]-effects[1])**2*F(1,100)
 assert agg==4 and variance==F(51,16) and diagonal==F(45,16) and share==F(16,25)
 return dict(composition=dict(cohort_effects=[2,10],horizon0_shares=[q(x) for x in w],horizon0_effect=q(agg),horizon1_shares=[1,0],horizon1_effect=2,fixed_equal_shares_effect=6,within_cohort_change=0),sample_membership=dict(weight_sample_counts=[3,1],outcome_sample_counts=[1,1],weight_sample_effect=4,outcome_sample_effect=6,claim='Conditional sample-mismatch witness; no native singleton-drop observation.'),last_control=dict(early_cohort=1,last_cohort=3,valid_calendar_times=[0,1,2],early_valid_nonnegative_lags=[0,1],invalid_early_lag=2,stipulated_early_effect=5,stipulated_late_effect=7,invalid_treated_comparison=-2,correct_early_target=5),covariance=dict(cohort_covariance=[[q(x) for x in r] for r in V],weights=[q(x) for x in w],full_aggregate_variance=q(variance),diagonal_only_variance=q(diagonal),share_variance=q(F(1,100)),gradient_share=-8,share_uncertainty=q(share),total_under_declared_zero_cross_covariance=q(variance+share),condition='First-order propagation; cross-covariance set to zero only for this authored example.'),simultaneity=dict(independent_pointwise_coverage=q(F(19,20)),coordinates=10,joint_coverage=q(F(19,20)**10),claim='Independence stipulated for illustration, not assumed for native event-study estimates.'),economics=dict(total_usd=1800,requested=90,conformant=75,useful=60,per_request=20,per_conformant=24,per_useful=30,illustrative=True),native_execution=False)
if __name__=='__main__':
 p=ROOT/'docs/program/execution/2026-10-24/eventstudy-reuse-v1/exact-results.json';assert not p.exists();p.write_text(json.dumps(calculate(),indent=2)+chr(10));print('Exact event-study witnesses saved.')
